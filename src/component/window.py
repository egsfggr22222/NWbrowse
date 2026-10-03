# -*- coding: utf-8 -*-
"""窗口进程（人 + 内核）：窗口外观 + 渲染 + 输入 + host 路由。

TitleBar 嵌在主窗口顶部。无 tabbar。
web_view 内缩一圈，外层描边 + 内层背景 + web_view 三层视觉。
web_view 裁圆角，定时兜底防止 WebView2 内部重绘重置。

pwindow：
  * 每个 window 唯一一个 pwindow（PopupWindow 组件）。
  * pwindow 是顶层窗口，点它会让 window 收到 WindowDeactivate。
  * "pwindow 被选中" 等同于 "window 被选中"，靠 is_effectively_active() 判断。

popup = URL 历史列表：
  * 不是 tab 管理器。
  * 只记录本窗口 host（含同主域）的 URL。
  * 每个新 URL → 底部追加一行，重复 URL 跳过去不追加。
  * 点击行 → 当前 web_view 加载。
  * 点行 × → 从列表里删。
  * < / > → 在列表里上下移动，并加载。
  * 关窗口清空（会话内保留）。

跨域：
  * 同主域点击 / 地址栏同主域 → 当前 web_view 加载。
  * 不同主域点击 / 地址栏跨域 → 联系 bar（bar 查窗口 / 起新窗口）。
  * 当前 web_view 不会跳去跨域。
"""

import sys
import os
import json
import time
import argparse
import ctypes
from ctypes import wintypes
from urllib.parse import urlparse, unquote, urlunparse
from window_icon import (
    default_icon,
    icon_for_window,
    apply_icon_to_window,
)

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths

from theme import Theme
from corner_mask import CornerMask
from title_bar import TitleBar
from input_box import InputBox
from settings import load_window_settings, save_window_settings
from settings import resolve_path, to_stored_path
from activity_watcher import ActivityWatcher
from popup_window import PopupWindow
from ipc import (
    IpcServer, IpcClient,
    window_channel, window_role,
    CHANNEL_BAR, CHANNEL_BROADCAST,
    MSG_NAVIGATE, MSG_QUIT, MSG_SHOW, MSG_CONFIG_CHANGED,
    MSG_LANGUAGE_CHANGED,
    MSG_DOWNLOAD_CANCEL_FOR_WINDOW,
    MSG_DOWNLOAD_START_WORKER,
    MSG_DOWNLOAD_CANCEL_WORKER,
    MSG_REVERT_TO_LAST_URL,
    MSG_PIN_RELOAD,
    MSG_PIN_STATE,
    MSG_PIN_TOGGLE_FROM_BAR,
    MSG_FAVORITE_CHANGED,
    find_windows, find_window_by_host, find_process,
)
from i18n import load as i18n_load, on_change
import password_hook

import pinned_store
import notify_store
from dom_activity import DOM_ACTIVITY_JS, DomActivityMonitor
import comtypes
import comtypes.client
from comtypes import GUID, COMMETHOD, HRESULT, IUnknown


SEARCH_ENGINES = [
    "google.com", "bing.com", "baidu.com", "sogou.com",
    "so.com", "360.cn", "yahoo.com", "duckduckgo.com",
    "yandex.com", "naver.com", "daum.net",
]

MEM_THRESHOLD_MB = 900

ROUND_TIMER_INTERVAL = 3000


try:
    from qtwebview2._bridge import BRIDGE_SCRIPT as _QTWEBVIEW_BRIDGE
except Exception:
    _QTWEBVIEW_BRIDGE = ""


_USER_SCRIPT = r"""
(function() {
    // ================================================================
    // 第一段：滚动条样式 + hover
    // ================================================================
    (function() {
        var css = [
            '::-webkit-scrollbar { width: 8px; height: 8px; background: transparent; }',
            '::-webkit-scrollbar-track { background: transparent; margin: 12px; }',
            '::-webkit-scrollbar-track-piece { background: transparent; margin: 12px; }',
            '::-webkit-scrollbar-thumb {',
            '    background: rgba(120, 120, 120, 0.04);',
            '    border-radius: 4px;',
            '    border: none;',
            '}',
            '::-webkit-scrollbar-corner { background: transparent; }',
            '::-webkit-scrollbar-button { display: none; }',
            'html.sb-hover::-webkit-scrollbar-thumb {',
            '    background: rgba(120, 120, 120, 0.75);',
            '}',
            'html.sb-hover *::-webkit-scrollbar-thumb {',
            '    background: rgba(120, 120, 120, 0.75);',
            '}'
        ].join('\n');

        function ensureStyle() {
            var head = document.head || document.documentElement;
            if (!head) return null;
            var el = document.getElementById('__sb_style');
            if (el) return el;
            var style = document.createElement('style');
            style.id = '__sb_style';
            style.type = 'text/css';
            style.appendChild(document.createTextNode(css));
            head.appendChild(style);
            return style;
        }

        if (window.__sb_installed) return;
        window.__sb_installed = true;

        var W = 14, hovering = false, pending = false;

        function setHover(on) {
            if (on === hovering) return;
            hovering = on;
            if (on) document.documentElement.classList.add('sb-hover');
            else document.documentElement.classList.remove('sb-hover');
        }

        document.addEventListener('mousemove', function(e) {
            if (pending) return;
            pending = true;
            requestAnimationFrame(function() {
                var nearRight = (window.innerWidth - e.clientX) <= W;
                var nearBottom = (window.innerHeight - e.clientY) <= W;
                setHover(nearRight || nearBottom);
                pending = false;
            });
        }, { passive: true });

        document.addEventListener('mouseleave', function() { setHover(false); });
        window.addEventListener('blur', function() { setHover(false); });

        setInterval(function() {
            if (!document.getElementById('__sb_style')) {
                ensureStyle();
            }
        }, 3000);

        try {
            var mo = new MutationObserver(function() {
                if (!document.getElementById('__sb_style')) ensureStyle();
            });
            mo.observe(document.documentElement, { childList: true, subtree: true });
        } catch (e) {}

        ensureStyle();
    })();

    // ================================================================
    // 第二段：跨域导航拦截（appnav）
    // ================================================================
    (function() {
        if (window.__appnav_installed) return;
        window.__appnav_installed = true;

        function rootHost(host) {
            if (!host) return "";
            var parts = host.split(".");
            if (parts.length <= 2) return host;
            return parts.slice(-2).join(".");
        }

        function isSameRoot(h1, h2) {
            if (!h1 || !h2) return false;
            if (h1 === h2) return true;
            return rootHost(h1) === rootHost(h2);
        }

        function reportAndBlock(e, href) {
            e.preventDefault();
            e.stopPropagation();
            try {
                if (window.ipc && window.ipc.postMessage) {
                    window.ipc.postMessage(JSON.stringify({
                        type: "appnav",
                        url: href
                    }));
                }
            } catch (err) {}
        }

        document.addEventListener("click", function(e) {
            if (e.button !== 0) return;
            if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;

            var a = null;
            try {
                a = e.target && e.target.closest ? e.target.closest("a") : null;
            } catch (err) {
                a = null;
            }
            if (!a) return;

            var href = a.href;
            if (!href) return;
            if (href.indexOf("javascript:") === 0) return;
            if (href.charAt(0) === "#") return;

            var target;
            try {
                target = new URL(href);
            } catch (err) {
                return;
            }
            if (target.protocol !== "http:" && target.protocol !== "https:") return;
            if (!target.hostname) return;

            var cur = location.hostname;
            if (isSameRoot(cur, target.hostname)) {
                return;
            }

            reportAndBlock(e, href);
        }, true);
    })();
})();
"""


INIT_SCRIPT = (_QTWEBVIEW_BRIDGE + _USER_SCRIPT
               + password_hook.PASSWORD_JS
               + DOM_ACTIVITY_JS)


def url_host(url):
    try:
        host = (urlparse(url).hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def _root_host(host):
    if not host:
        return ""
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])

def _norm_url(url):
    """规范化 URL：去 query + fragment。"""
    if not url:
        return ""
    try:
        from urllib.parse import urlsplit, urlunsplit
        parts = urlsplit(url)
        return urlunsplit((
            parts.scheme, parts.netloc, parts.path,
            "", "",
        ))
    except Exception:
        return url



def _clean_js_url(raw):
    if raw is None:
        return ""
    s = str(raw).strip()
    if not s:
        return ""

    for _ in range(3):
        if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
            s = s[1:-1].strip()
        else:
            break

    try:
        import json as _json
        if s.startswith(('"', "'")):
            s = _json.loads(s)
    except Exception:
        pass

    return s


class History:
    """历史记录转发。具体逻辑在 history_hook。"""

    @staticmethod
    def record(window, title, url=""):
        from history_hook import record
        record(window, title, url)


def _pretty_url_for_address_bar(url):
    if not url:
        return url
    try:
        p = urlparse(url)
        if not p.query:
            return url

        out = []
        for pair in p.query.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                out.append(k + "=" + unquote(v))
            else:
                out.append(unquote(pair))
        new_query = "&".join(out)

        return urlunparse((
            p.scheme, p.netloc, p.path,
            p.params, new_query, p.fragment,
        ))
    except Exception:
        return url


def _is_redirect_url(url):
    try:
        parsed = urlparse(url)
        path = parsed.path or ""
        query = parsed.query or ""
        return (
            "/link" in path
            or "/ck/" in path
            or "url=" in query
        )
    except Exception:
        return False


def set_topmost(hwnd, on=True):
    HWND_TOPMOST = -1
    HWND_NOTOPMOST = -2
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOACTIVATE = 0x0010
    try:
        ctypes.windll.user32.SetWindowPos(
            wintypes.HWND(int(hwnd)),
            HWND_TOPMOST if on else HWND_NOTOPMOST,
            0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
        )
    except Exception:
        pass


_WEBVIEW2_CLASSES = {
    "Chrome_WidgetWin_0",
    "Chrome_WidgetWin_1",
    "Chrome_WidgetWin_2",
    "Chrome_RenderWidgetHostHWND",
}


def _enum_child_hwnds(parent_hwnd):
    result = []

    def enum_proc(hwnd, lparam):
        try:
            buf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.GetClassNameW(hwnd, buf, 512)
            result.append((hwnd, buf.value))
        except Exception:
            pass
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(
        ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
    )
    try:
        ctypes.windll.user32.EnumChildWindows(
            wintypes.HWND(parent_hwnd), WNDENUMPROC(enum_proc), 0
        )
    except Exception:
        pass
    return result


# ======================================================================
# 任务栏卡片显隐（ITaskbarList）
# ======================================================================
class ITaskbarList(IUnknown):
    _iid_ = GUID("{56FDF342-FD6D-11D0-958A-006097C9A090}")
    _methods_ = [
        COMMETHOD([], HRESULT, "HrInit"),
        COMMETHOD([], HRESULT, "AddTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "DeleteTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "ActivateTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "SetActiveAlt",
                  (["in"], wintypes.HWND, "hwnd")),
    ]


class TaskbarHelper:
    """封装 ITaskbarList。运行中动态隐藏/显示任务栏卡片。"""

    CLSID_TASKBAR_LIST = GUID("{56FDF344-FD6D-11D0-958A-006097C9A090}")

    def __init__(self):
        self._taskbar = None
        self._ok = False
        try:
            self._taskbar = comtypes.client.CreateObject(
                self.CLSID_TASKBAR_LIST,
                interface=ITaskbarList,
            )
            self._taskbar.HrInit()
            self._ok = True
            print("[window] ITaskbarList 初始化成功")
        except Exception as e:
            print("[window] ITaskbarList 初始化失败:", repr(e))

    def hide(self, hwnd):
        if not self._ok:
            return
        try:
            self._taskbar.DeleteTab(int(hwnd))
        except Exception:
            pass

    def show(self, hwnd):
        if not self._ok:
            return
        try:
            self._taskbar.AddTab(int(hwnd))
        except Exception:
            pass


class RoundedWindow(QWidget):

    RADIUS = Theme.RADIUS
    WEB_RADIUS = Theme.WEB_RADIUS
    RESIZE_MARGIN = Theme.RESIZE_MARGIN
    CORNER_MARGIN = Theme.CORNER_MARGIN
    TOP_BAR_HEIGHT = Theme.TOP_BAR_HEIGHT
    WEB_TOP_GAP = Theme.WEB_TOP_GAP
    SIDE_MARGIN = Theme.SIDE_MARGIN
    BOTTOM_MARGIN = Theme.BOTTOM_MARGIN

    BORDER = 1
    OUTLINE_ALPHA = 180

    STAGGER_STEP = 30
    STAGGER_MAX = 8

    DL_URL_COOLDOWN = 5.0
    URL_POLL_INTERVAL = 400

    def __init__(self, mode="default", window_id="df-0",
                 host="", start_url="", pinned_url=""):
        print(f"[DBG] RoundedWindow.__init__ enter id={id(self)} "
              f"mode={mode} window_id={window_id}")
        super().__init__()
        self._mode = mode
        self._window_id = window_id
        self._start_url = start_url
        self._pinned_url = pinned_url

        self._pending_input_host = ""

        # ---- 固定状态 ----
        self._pin_on = False
        self._taskbar = TaskbarHelper()

        # ---- 搜索引擎（内存，不持久化，关窗口即清）----
        self._current_engine = None      # dict {"abbr", "url"}
        self._engine_picker = None       # EnginePicker 实例（显示中）
        self._engine_favicon_cache = {}  # url -> QPixmap
        # ------------------------------------------------

        # ---- 收藏菜单 ----
        self._fav_menu = None            # FavoritesMenu 实例
        # ------------------
        self._taskbar_timer = QTimer(self)
        self._taskbar_timer.setInterval(500)
        self._taskbar_timer.timeout.connect(self._apply_taskbar_visibility)
        # ------------------

        # ---- 完成提醒 ----
        self._complete_notify_on = False
        self._dom_monitor = DomActivityMonitor(self, self._on_dom_over)
        # ------------------

        # ---- 屏幕外最小化 ----
        self._offscreen = False
        self._pre_offscreen_pos = None
        # ----------------------

        self._hosts = set()
        self._primary_host = ""
        if host:
            self._hosts.add(host)
            self._primary_host = host

        self._has_loaded_once = bool(host)

        self._web_view = None
        self._current_url = ""

        self._popup = None
        self._activity = ActivityWatcher(QApplication.instance(), self)
        self._activity.activeWindowChanged.connect(
            self._refresh_popup_visibility
        )

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(480, 300)
        self.resize(1000, 700)

        self._resize_edge = None
        self._start_geo = None
        self._start_pos = None
        self._resizing = False
        self.setMouseTracking(True)

        self._url_settle_timer = QTimer(self)
        self._url_settle_timer.setSingleShot(True)
        self._url_settle_timer.setInterval(300)
        self._url_settle_timer.timeout.connect(self._on_url_settled)

        self._bg_path = ""
        self._bg_pixmap = None
        self._on_change_cb = None

        self._download_workers = {}
        self._dl_url = ""
        self._dl_path = ""
        self._last_dl_url_time = {}
        self._last_request_url = {}

        self._url_poll_timer = QTimer(self)
        self._url_poll_timer.setInterval(self.URL_POLL_INTERVAL)
        self._url_poll_timer.timeout.connect(self._poll_url_once)
        self._poll_busy = False
        self._addr_editing = False
        self._last_display_url = ""

        # ---- favicon 状态 ----
        self._favicon_pixmap = None
        self._favicon_cache = {}
        self._has_favicon_signal = False
        self._favicon_poll = QTimer(self)
        self._favicon_poll.setInterval(800)
        self._favicon_poll.timeout.connect(self._poll_favicon)
        self._favicon_poll.start()
        # ----------------------

        self._apply_saved_theme()

        self._setup_title_bar()
        self._setup_input_box()

        self._create_web_view()

        self._setup_corner_mask()

        try:
            password_hook.install(self)
        except Exception as e:
            print("[window] password_hook install 失败:", e)

        self.create_popup(title="标签")
        self._restore_pinned_memory()

        self._ipc_server = IpcServer(
            window_channel(self._window_id),
            self._on_ipc_message,
            role=window_role(self._window_id),
            extra={
                "type": self._mode,
                "window_id": self._window_id,
                "hosts": list(self._hosts),
                "host": self._primary_host,
            },
        )
        self._ipc_server.start()

        self._load_saved_background()
        self._apply_stagger_position()

        self._on_change_cb = self._refresh_texts
        try:
            on_change(self._on_change_cb)
        except Exception as e:
            print("[window] 注册语言回调失败:", e)

        self._round_timer = QTimer(self)
        self._round_timer.setInterval(ROUND_TIMER_INTERVAL)
        self._round_timer.timeout.connect(self._apply_round_region)
        self._round_timer.start()

        print(f"[DBG] __init__ exit id={id(self)}")

        # 启动加载：pinned_url（固定内容）优先，其次 start_url
        _boot_url = self._pinned_url or self._start_url
        if _boot_url:
            QTimer.singleShot(200, lambda u=_boot_url: self.handle_url(u))

        # 固定状态初始化：如果启动时是固定窗口，同步开关视觉 + 启动任务栏定时器
        _pin_host = self._pin_host()
        if _pin_host and pinned_store.is_pinned(_pin_host):
            self._pin_on = True
            if hasattr(self, "title_bar"):
                try:
                    self.title_bar.set_pin_switch_state(True)
                except Exception:
                    pass
            self._taskbar_timer.start()
            QTimer.singleShot(0, self._apply_taskbar_visibility)

        # ---- 完成提醒：独立恢复（不依赖固定项）----
        # 原先这段嵌在上面的 is_pinned 分支里，导致"没固定的站点打开开关，
        # 关窗就忘、下次又变回关"，看起来像功能丢了。现在独立存/读。
        try:
            if _pin_host and notify_store.is_on(_pin_host):
                self._complete_notify_on = True
                self._dom_monitor.start()
                print("[window] 完成提醒已恢复: %s" % _pin_host)
        except Exception as e:
            print("[window] 读取完成提醒状态失败:", e)

        # ---- 预抓搜索引擎图标（后台，延迟 1.5s 避免和窗口初始化抢资源）----
        QTimer.singleShot(1500, self._prefetch_engine_icons)
        # ------------------------------------------------------------

    # =========================================================
    # pwindow：创建 / 显隐判断
    # =========================================================
    def create_popup(self, title="弹窗"):
        if self._popup is None:
            self._popup = PopupWindow(parent=self, title=title)
            self._popup.url_selected.connect(self._on_popup_url_selected)
            self._popup.url_closed.connect(self._on_popup_url_closed)
            self._popup.destroyed.connect(self._on_popup_destroyed)
            self._popup.set_favicon(self._favicon_pixmap)
        return self._popup

    def _on_popup_destroyed(self, *_):
        self._popup = None

    # =========================================================
    # 固定记录
    # =========================================================
    def _root_host_of(self, url):
        try:
            from urllib.parse import urlparse
            h = (urlparse(url).hostname or "").lower()
            if not h:
                return ""
            parts = h.split(".")
            if len(parts) <= 2:
                return h
            return ".".join(parts[-2:])
        except Exception:
            return ""

    def _restore_pinned_memory(self):
        """启动时把固定记录的 popup 列表灌回 popup，定位索引。"""
        if self._mode == "search":
            return
        host = self._pin_host()
        if not host or not pinned_store.is_pinned(host):
            return
        try:
            item = pinned_store.load_one(host)
        except ValueError as e:
            print("[window] 固定项损坏:", e)
            return
        if not item or self._popup is None:
            return

        urls = item.get("popup_urls", [])
        last_index = item.get("last_index", -1)

        for u in urls:
            self._popup.append_url(u)

        if urls:
            if 0 <= last_index < len(urls):
                self._popup.set_current_url(urls[last_index])
            else:
                self._popup.set_current_url(urls[-1])

        self._pin_on = True

    def _save_pinned_memory(self):
        """关窗时：如果固定状态开着，保存 popup_urls 和选中索引。"""
        if self._mode == "search":
            return
        if not self._pin_on:
            return
        host = self._pin_host()
        if not host or not pinned_store.is_pinned(host):
            return
        if self._popup is None:
            return
        try:
            urls = self._popup.urls()
            cur = self._popup.current_url() or ""
            last_index = -1
            if cur and cur in urls:
                last_index = urls.index(cur)
            elif urls:
                last_index = len(urls) - 1

            pinned_store.save_one(
                host,
                hosts=list(self._hosts),
                popup_urls=urls,
                last_index=last_index,
            )
        except Exception as e:
            print("[window] 保存固定记忆失败:", e)

    def _pin_host(self):
        """当前可固定的主域（key）。**始终返回主域**，不是具体 host。"""
        h = self._primary_host or self._root_host_of(self._current_url)
        if not h:
            return ""
        return self._root_host_of(h) or h

    def _pin_snapshot(self):
        """打包当前固定内容，供上报 bar。"""
        urls = []
        cur = ""
        if self._popup is not None:
            urls = self._popup.urls()
            cur = self._popup.current_url() or ""
        last_index = -1
        if cur and cur in urls:
            last_index = urls.index(cur)
        elif urls:
            last_index = len(urls) - 1

        return {
            "host": self._pin_host(),
            "hosts": list(self._hosts),
            "popup_urls": urls,
            "last_index": last_index,
            "on": self._pin_on,
            "complete_notify": bool(self._complete_notify_on),
        }

    def _notify_bar_pin_state(self):
        """上报固定状态给 bar。"""
        try:
            data = self._pin_snapshot()
            if not data["host"]:
                return
            payload = json.dumps(data, ensure_ascii=False)
            IpcClient.send_to_role(
                "bar", MSG_PIN_STATE, payload.encode("utf-8"),
            )
        except Exception as e:
            print("[window] 上报固定状态失败:", e)

    def _on_pin_switch_toggled(self, on):
        """用户在菜单里点击固定开关。"""
        host = self._pin_host()
        if not host:
            return

        if on:
            # 上限检查由 bar 做，本地直接开
            self._pin_on = True
        else:
            self._pin_on = False

        self._notify_bar_pin_state()
        self._apply_taskbar_visibility()

        # 打开固定：把当前完成提醒状态一并写盘
        if on and pinned_store.is_pinned(host):
            try:
                pinned_store.save_one(
                    host,
                    complete_notify=bool(self._complete_notify_on),
                )
            except Exception as e:
                print("[window] 保存完成提醒状态失败:", e)

    def _apply_taskbar_visibility(self):
        """根据 _pin_on 隐藏/显示任务栏卡片。"""
        try:
            hwnd = int(self.winId())
        except Exception:
            return
        if self._pin_on:
            self._taskbar.hide(hwnd)
        else:
            self._taskbar.show(hwnd)

    def _on_popup_url_selected(self, url):
        """点击 popup 里的 URL → 当前 web_view 加载。"""
        if not url:
            return
        if not self.web_view:
            return
        self._do_load(url)

    def _on_popup_url_closed(self, url):
        """点 popup 行的 ×，只从列表里删，不影响当前页面。"""
        if self._popup is not None:
            self._popup.remove_url(url)

    def is_effectively_active(self):
        active = QApplication.activeWindow()
        if active is self:
            return True
        if self._popup is not None and active is self._popup:
            return True
        return False

    def _refresh_popup_visibility(self, *_):
        p = self._popup
        if p is None:
            return

        if not getattr(p, "_user_opened", False):
            if p.isVisible():
                p.hide()
            return

        if getattr(p, "_user_closed", False):
            if p.isVisible():
                p.hide()
            return

        if (self.is_effectively_active()
                and self.isVisible()
                and not self.isMinimized()):
            if not p.isVisible():
                p.show()
                p.raise_()
        else:
            if p.isVisible():
                p.hide()

    @property
    def web_view(self):
        return self._web_view

    # =========================================================
    # web_view
    # =========================================================
    def _create_web_view(self):
        from qtwebview2 import QtWebViewWidget
        from settings_backend import SettingsBackend

        backend = SettingsBackend()

        kwargs = {
            "native_child": True,
            "lazyload": True,
            "debug": True,
            "initialization_script": INIT_SCRIPT,
            "download_started_handler": self._on_download_started,
            "download_completed_handler": self._on_download_completed,
            "new_window_handler": self._on_new_window,
            "navigation_handler": self._on_navigation,
            "parent": self,
        }

        ua = backend.get_user_agent()
        if ua:
            kwargs["user_agent"] = ua

        if backend.get_incognito():
            kwargs["incognito"] = True

        user_data = backend.get_user_data_folder(self._window_id)
        if user_data:
            kwargs["user_data_folder"] = user_data

        try:
            wv = QtWebViewWidget(**kwargs)
        except TypeError as e:
            print("[window] 创建 web_view 参数不被支持:", e)
            wv = QtWebViewWidget(
                native_child=True,
                lazyload=False,
                initialization_script=INIT_SCRIPT,
                parent=self,
            )

        try:
            wv.signals.web_message_received.connect(self._on_js_message)
        except Exception as e:
            print("[window] 接 web_message_received 失败:", e)

        try:
            wv.signals.title_changed.connect(self._on_title_changed)
        except Exception as e:
            print("[window] 接 title_changed 失败:", e)

        try:
            wv.signals.favicon_changed.connect(self._on_favicon_changed)
            self._has_favicon_signal = True
        except Exception as e:
            print("[window] 无 favicon_changed 信号，用 JS 兜底:", e)

        wv.hide()
        wv.setGeometry(0, 0, 0, 0)
        self._web_view = wv

    def _on_title_changed(self, title):
        if not title:
            return
        url = self._current_url or ""
        if not url:
            return
        if self._popup is not None:
            self._popup.set_title(url, title)
        try:
            History.record(self, title, url)
        except Exception as e:
            print("[window] _on_title_changed 异常:", e)

    # =========================================================
    # favicon
    # =========================================================
    _JS_FAVICON = """
    (function(){
        // 按优先级找，返回最大的那个图标
        function getSize(link) {
            var s = link.getAttribute("sizes");
            if (!s) return 0;
            var m = s.match(/(\\d+)/);
            return m ? parseInt(m[1], 10) : 0;
        }

        var candidates = [];

        // 1. apple-touch-icon（通常 180x180，最清晰）
        var appleLinks = document.querySelectorAll(
            'link[rel="apple-touch-icon"], link[rel="apple-touch-icon-precomposed"]'
        );
        for (var i = 0; i < appleLinks.length; i++) {
            if (appleLinks[i].href) {
                candidates.push({ href: appleLinks[i].href, size: getSize(appleLinks[i]) || 180 });
            }
        }

        // 2. 普通 icon，取最大的
        var iconLinks = document.querySelectorAll(
            'link[rel~="icon"], link[rel="shortcut icon"]'
        );
        for (var j = 0; j < iconLinks.length; j++) {
            if (iconLinks[j].href) {
                candidates.push({ href: iconLinks[j].href, size: getSize(iconLinks[j]) || 16 });
            }
        }

        if (candidates.length === 0) return "";

        // 取 size 最大的
        candidates.sort(function(a, b) { return b.size - a.size; });
        return candidates[0].href;
    })()
    """

    def _fetch_title(self, url):
        """拿 document.title，同时更新 popup 和写 history。"""
        wv = self.web_view
        if wv is None or not wv.isVisible():
            return

        def _cb(raw_title):
            try:
                title = _clean_js_url(raw_title)
                if not title:
                    return
                if self._popup is not None:
                    self._popup.set_title(url, title)
                History.record(self, title, url)
            except Exception as e:
                print(f"[window] _fetch_title 异常: {e}")

        try:
            wv.eval_js("document.title", _cb)
        except Exception:
            pass

    def _on_favicon_changed(self, icon):
        if icon is None or icon.isNull():
            return
        pm = icon.pixmap(24, 24)
        if pm.isNull():
            return
        self._favicon_pixmap = pm
        self._apply_favicon()

    def _poll_favicon(self):
        wv = self.web_view
        if wv is None or not wv.isVisible():
            return

        def _cb(href):
            try:
                href = _clean_js_url(href)
                if not href:
                    return
                if href.startswith("data:"):
                    self._favicon_from_data_uri(href)
                    return
                if href in self._favicon_cache:
                    self._favicon_pixmap = self._favicon_cache[href]
                    self._apply_favicon()
                    return
                self._download_favicon(href)
            except Exception as e:
                print("[window] favicon JS 回调异常:", e)

        try:
            wv.eval_js(self._JS_FAVICON, _cb)
        except Exception as e:
            print("[window] eval_js favicon 失败:", e)

    def _favicon_from_data_uri(self, uri):
        import base64
        try:
            header, _, b64 = uri.partition(",")
            raw = base64.b64decode(b64) if "base64" in header else b64.encode()
            pm = QPixmap()
            pm.loadFromData(raw)
            if not pm.isNull():
                self._favicon_cache[uri] = pm
                self._favicon_pixmap = pm
                self._apply_favicon()
        except Exception as e:
            print("[window] data URI 解析失败:", e)

    def _download_favicon(self, href):
        from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
        if not hasattr(self, "_nam"):
            self._nam = QNetworkAccessManager(self)
        reply = self._nam.get(QNetworkRequest(QUrl(href)))

        def _done():
            try:
                pm = QPixmap()
                pm.loadFromData(bytes(reply.readAll()))
                if not pm.isNull():
                    self._favicon_cache[href] = pm
                    self._favicon_pixmap = pm
                    self._apply_favicon()
            except Exception as e:
                print("[window] favicon 下载回调异常:", e)
            finally:
                reply.deleteLater()

        reply.finished.connect(_done)

    def _apply_favicon(self):
        if hasattr(self, "title_bar"):
            self.title_bar.set_favicon(self._favicon_pixmap)
        if self._popup is not None:
            self._popup.set_favicon(self._favicon_pixmap)
        apply_icon_to_window(
            self, self._favicon_pixmap, self._current_url or ""
        )

        # ---- 固定项图标更新（只在 favicon 真的变了才写盘）----
        try:
            pin_host = self._pin_host()
            if (self._favicon_pixmap is not None
                    and not self._favicon_pixmap.isNull()
                    and self._pin_on
                    and pin_host
                    and pinned_store.is_pinned(pin_host)):
                # 用 pixmap 的 cacheKey 判重（Qt 保证同一图返回相同值）
                fp = (self._favicon_pixmap.width(),
                      self._favicon_pixmap.height(),
                      self._favicon_pixmap.cacheKey())
                if getattr(self, "_last_saved_favicon_fp", None) != fp:
                    self._last_saved_favicon_fp = fp
                    pinned_store.save_icon(
                        pin_host, self._favicon_pixmap
                    )
                    try:
                        IpcClient.send_to_role(
                            "bar", MSG_PIN_RELOAD, b""
                        )
                    except Exception:
                        pass
        except Exception as e:
            print("[window] 同步 favicon 到固定项失败:", e)

    def _reset_favicon(self, url=""):
        self._favicon_pixmap = None
        if hasattr(self, "title_bar"):
            self.title_bar.set_favicon(None)
        if self._popup is not None:
            self._popup.set_favicon(None)

        apply_icon_to_window(self, None, url or self._current_url or "")

    # =========================================================
    # host
    # =========================================================
    def _add_host(self, host, primary=False):
        if not host:
            return
        if host in self._hosts:
            if primary and not self._primary_host:
                self._primary_host = host
            return
        self._hosts.add(host)
        if primary or not self._primary_host:
            self._primary_host = host
        self._has_loaded_once = True
        self._sync_registry()

    def _sync_registry(self):
        try:
            from ipc import register_process
            register_process(
                window_role(self._window_id),
                window_channel(self._window_id),
                extra={
                    "type": self._mode,
                    "window_id": self._window_id,
                    "hosts": list(self._hosts),
                    "host": self._primary_host,
                },
            )
        except Exception:
            pass

    def _bar_host(self):
        return self._primary_host or ""

    def _has_root_host(self, host):
        """窗口里是否有该主域。"""
        if not host:
            return False
        new_root = _root_host(host)
        if not new_root:
            return False
        for h in self._hosts:
            if h and _root_host(h) == new_root:
                return True
        return False

    def _matches_host(self, host):
        if not host:
            return False
        if host in self._hosts:
            return True
        return self._is_related_host(host)

    def _is_related_host(self, new_host):
        if not new_host:
            return False
        new_root = _root_host(new_host)
        for h in self._hosts:
            if not h:
                continue
            if new_host == h:
                return True
            if new_host.endswith("." + h):
                return True
            if h.endswith("." + new_host):
                return True
            if new_root and new_root == _root_host(h):
                return True
        return False

    def _apply_stagger_position(self):
        try:
            n = len(find_windows())
        except Exception:
            n = 0

        screen = QApplication.primaryScreen().availableGeometry()
        base_w, base_h = self.width(), self.height()
        x0 = screen.left() + (screen.width() - base_w) // 2
        y0 = screen.top() + (screen.height() - base_h) // 2

        step = (n % self.STAGGER_MAX) * self.STAGGER_STEP
        self.move(x0 + step, y0 + step)

    # =========================================================
    # 主题 / 背景
    # =========================================================
    def _apply_saved_theme(self):
        try:
            s = load_window_settings(self._mode, self._window_id)
            color = QColor(s.get("theme_color", "#d0d0d0"))
            if not color.isValid():
                color = QColor("#d0d0d0")
            border, inner = Theme.apply_theme(color)
            TitleBar.BG_COLOR = border
        except Exception as e:
            print("[window] 应用主题失败:", e)

    def _load_saved_background(self):
        try:
            s = load_window_settings(self._mode, self._window_id)
            path = s.get("background_current", "")
            if path:
                # resolve_path 负责展开 {RES} 内置资源占位符
                real = resolve_path(path)
                pm = QPixmap(real)
                if not pm.isNull():
                    self._bg_path = real
                    self._bg_pixmap = pm
        except Exception:
            pass

    def _reload_config(self):
        try:
            s = load_window_settings(self._mode, self._window_id)
            color = QColor(s.get("theme_color", "#d0d0d0"))
            if color.isValid():
                border, inner = Theme.apply_theme(color)
                self.title_bar.apply_theme_color(border)
                if hasattr(self, "corner_mask"):
                    self.corner_mask.bg_color = border
                    self.corner_mask.update()

            path = s.get("background_current", "")
            real = resolve_path(path)
            if real and os.path.isfile(real):
                pm = QPixmap(real)
                if not pm.isNull():
                    self._bg_path = real
                    self._bg_pixmap = pm
            else:
                self._bg_path = ""
                self._bg_pixmap = None
            self.update()
        except Exception as e:
            print("[window] 重读配置失败:", e)

    def _broadcast_config_changed(self):
        try:
            IpcClient(CHANNEL_BROADCAST).send(MSG_CONFIG_CHANGED, b"")
        except Exception:
            pass

    # =========================================================
    # UI
    # =========================================================
    def _setup_title_bar(self):
        self.title_bar = TitleBar(self)
        self.title_bar.BG_COLOR = Theme.TITLE_BG_COLOR
        self.title_bar.setGeometry(
            self.BORDER, self.BORDER,
            self.width() - 2 * self.BORDER,
            self.TOP_BAR_HEIGHT,
        )
        self.title_bar.raise_()

        try:
            self.title_bar.address_bar.textEdited.connect(
                self._on_addr_text_edited
            )
            self.title_bar.address_bar.editingFinished.connect(
                self._on_addr_editing_finished
            )
        except Exception:
            pass

        try:
            self.title_bar.prev_tab.connect(self._prev_url)
        except Exception:
            pass
        try:
            self.title_bar.next_tab.connect(self._next_url)
        except Exception:
            pass
        try:
            self.title_bar.toggle_pin.connect(self._on_pin_switch_toggled)
        except Exception:
            pass
        try:
            self.title_bar.toggle_complete_notify.connect(
                self._on_complete_notify_toggled
            )
        except Exception:
            pass

        try:
            self.title_bar.star_left_clicked.connect(
                self._on_star_left_clicked
            )
        except Exception as e:
            print("[window] 接收藏星左键失败:", e)

        try:
            self.title_bar.star_right_clicked.connect(
                self._on_star_right_clicked
            )
        except Exception as e:
            print("[window] 接收藏星右键失败:", e)

    def _on_addr_text_edited(self, _text):
        self._addr_editing = True

    def _on_addr_editing_finished(self):
        self._addr_editing = False

    def _setup_input_box(self):
        self.input_box = InputBox(self)
        self.input_box.submitted.connect(self.visit)
        self.input_box.escaped.connect(self.show_input_box)
        try:
            self.input_box.engine_button().clicked.connect(
                self._on_engine_btn_clicked
            )
        except Exception as e:
            print("[window] 接引擎按钮信号失败:", e)
        self._center_input_box()

    def _setup_corner_mask(self):
        self.corner_mask = CornerMask(self)
        self.corner_mask.bg_color = Theme.BG_COLOR
        self.corner_mask.hide()

    # =========================================================
    # JS → Python
    # =========================================================
    def _on_js_message(self, msg):
        try:
            data = json.loads(msg)
        except Exception:
            return

        if not isinstance(data, dict):
            return

        t = data.get("type")
        if t != "pw_state":
            print(f"[DBG] js_msg type={t!r}")

        # ---- DOM 状态机事件（new/lazy 簇）----
        try:
            from dom_activity import DomActivityMonitor
            if t in DomActivityMonitor.TYPES:
                self._dom_monitor.feed(data)
                return
        except Exception as e:
            import traceback
            print("[window] dom feed 异常:")
            traceback.print_exc()
            return

        # ---- 其他 ----
        try:
            if password_hook.on_js_message(self, data):
                return
        except Exception as e:
            print("[window] password_hook 处理失败:", e)

        if t != "appnav":
            return

        url = data.get("url", "")
        if not url:
            return

        self._handle_external_nav(url)

    def _handle_external_nav(self, url):
        """网页内点击跨域链接 → 联系 bar。同主域不会走到这里（JS 已放行）。"""
        host = url_host(url)
        if not host:
            return

        if self._has_root_host(host):
            self._do_load(url)
            return

        self.request_url(url)

    def _on_new_window(self, url):
        from wryview import NewWindowResponse

        if url:
            QTimer.singleShot(0, lambda u=url: self._resolve_and_route(u))
        return NewWindowResponse.Deny

    def _resolve_and_route(self, url):
        import urllib.request

        host = url_host(url)

        if self._matches_host(host) and _is_redirect_url(url):
            try:
                req = urllib.request.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0")
                ref = self._current_url_str()
                if ref:
                    req.add_header("Referer", ref)
                resp = urllib.request.urlopen(req, timeout=5)
                real_url = resp.geturl()
                resp.close()
                self.handle_url(real_url)
                return
            except Exception:
                pass

        self.handle_url(url)

    def _on_navigation(self, url):
        """兜底：非点击导航（地址栏、JS 跳转）也拦跨域。"""
        host = url_host(url)
        if not host:
            return True

        if not self._hosts:
            return True

        if self._matches_host(host):
            return True

        from ipc import find_process
        if not find_process("bar"):
            return True

        self.request_url(url)
        return False

    def _on_drag_drop(self, event, paths, position):
        """WebView2 拖放事件。

        返回 True 让 WebView2 自己处理文件（默认行为）。
        """
        print(f"[window] drag_drop event={event} paths={paths} pos={position}")
        return True

    # =========================================================
    # 下载
    # =========================================================
    def _on_download_started(self, url, suggested_path):
        now = time.time()
        last = self._last_dl_url_time.get(url, 0)
        if now - last < self.DL_URL_COOLDOWN:
            return False
        self._last_dl_url_time[url] = now

        cutoff = now - 60
        self._last_dl_url_time = {
            u: t for u, t in self._last_dl_url_time.items() if t > cutoff
        }

        if url.startswith("blob:") or url.startswith("data:"):
            self._dl_url = ""
            self._dl_path = suggested_path
            try:
                from ipc import ROLE_DOWNLOADS, MSG_DOWNLOAD_START
                payload = json.dumps({
                    "url": url,
                    "path": suggested_path,
                    "filename": os.path.basename(suggested_path),
                    "total": -1,
                    "notify": True,
                    "window_id": self._window_id,
                }, ensure_ascii=False)
                IpcClient.send_to_role(
                    ROLE_DOWNLOADS, MSG_DOWNLOAD_START,
                    payload.encode("utf-8"),
                )
            except Exception as e:
                print("[window] blob 开始通知失败:", e)

            QTimer.singleShot(
                500,
                lambda u=url, p=suggested_path:
                    self._poll_blob_file(u, p),
            )
            return True

        QTimer.singleShot(
            0,
            lambda u=url, p=suggested_path: self._start_http_download_safe(u, p),
        )
        return False

    def _poll_blob_file(self, url, path, last_size=-1, retries=120):
        if not path:
            return

        if not os.path.isfile(path):
            if retries <= 0:
                self._send_blob_done(url, path, success=False)
                return
            QTimer.singleShot(
                500,
                lambda: self._poll_blob_file(
                    url, path, last_size, retries - 1),
            )
            return

        try:
            size = os.path.getsize(path)
        except OSError:
            size = 0

        if size != last_size:
            QTimer.singleShot(
                500,
                lambda: self._poll_blob_file(url, path, size, retries - 1),
            )
            return

        self._send_blob_done(url, path, success=True)

    def _send_blob_done(self, url, path, success):
        try:
            from ipc import ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE
            payload = json.dumps({
                "url": url,
                "path": path,
                "success": bool(success),
                "delete_partial": False,
            }, ensure_ascii=False)
            IpcClient.send_to_role(
                ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE,
                payload.encode("utf-8"),
            )
        except Exception as e:
            print("[window] blob 完成通知失败:", e)
        self._dl_path = ""

    def _start_http_download_safe(self, url, save_path):
        try:
            self._start_http_download(url, save_path)
        except Exception:
            import traceback
            print("[window] _start_http_download 异常:")
            traceback.print_exc()

    def _start_http_download(self, url, save_path):
        referer = self._current_url_str() or ""

        user_agent = ""
        try:
            from settings_backend import SettingsBackend
            user_agent = SettingsBackend().get_user_agent() or ""
        except Exception:
            pass

        prog, argv = apppaths.role_command(
            "download-worker",
            "--url", url,
            "--path", save_path,
            "--window-id", self._window_id,
            "--referer", referer,
            "--user-agent", user_agent,
        )

        proc = QProcess(self)
        proc.setProgram(prog)
        proc.setArguments(argv)
        apppaths.configure_child_proc(proc)
        proc.finished.connect(
            lambda code, status, u=url: self._on_worker_finished(u, code, status)
        )
        proc.start()
        self._download_workers[url] = proc

        QTimer.singleShot(
            300,
            lambda u=url: self._send_cookie_to_worker(u),
        )

    def _send_cookie_to_worker(self, url, retries=60):
        worker_channel = window_channel(self._window_id) + "_worker"

        if not find_process(worker_channel):
            if retries <= 0:
                return
            QTimer.singleShot(
                500,
                lambda: self._send_cookie_to_worker(url, retries - 1),
            )
            return

        cookie_str = ""
        try:
            wv = self.web_view
            if wv is not None:
                cookies = wv.cookies_for_url(url)
                parts = [f"{c.name}={c.value}" for c in cookies]
                cookie_str = "; ".join(parts)
        except Exception:
            pass

        try:
            payload = json.dumps({"cookie": cookie_str}, ensure_ascii=False)
            ok = IpcClient(worker_channel).send(
                MSG_DOWNLOAD_START_WORKER,
                payload.encode("utf-8"),
            )
            if not ok:
                if retries <= 0:
                    return
                QTimer.singleShot(
                    500,
                    lambda: self._send_cookie_to_worker(url, retries - 1),
                )
        except Exception:
            pass

    def _on_worker_finished(self, url, exit_code, exit_status):
        self._download_workers.pop(url, None)

    def _cancel_worker(self, url):
        proc = self._download_workers.get(url)
        if proc is None:
            self._notify_cancel_done(url)
            return

        try:
            try:
                worker_channel = window_channel(self._window_id) + "_worker"
                IpcClient(worker_channel).send(
                    MSG_DOWNLOAD_CANCEL_WORKER, b"",
                )
            except Exception:
                pass

            if not proc.waitForFinished(1500):
                proc.kill()
                proc.waitForFinished(500)
        except Exception:
            pass

        self._download_workers.pop(url, None)
        self._notify_cancel_done(url)

    def _notify_cancel_done(self, url):
        try:
            from ipc import ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE
            payload = json.dumps({
                "url": url,
                "path": "",
                "success": False,
                "delete_partial": True,
            }, ensure_ascii=False)
            IpcClient.send_to_role(
                ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE,
                payload.encode("utf-8"),
            )
        except Exception:
            pass

    def _on_download_completed(self, url, saved_path, success):
        pass

    # =========================================================
    # 圆角
    # =========================================================
    def _find_webview2_hwnd(self, wv=None):
        if wv is None:
            wv = self.web_view
        if wv is None:
            return 0
        try:
            parent = int(wv.winId())
        except Exception:
            return 0
        if not parent:
            return 0

        children = _enum_child_hwnds(parent)
        for hwnd, cls in children:
            if cls in _WEBVIEW2_CLASSES:
                return hwnd

        if len(children) == 1:
            return children[0][0]
        return 0

    def _apply_round_region(self, wv=None):
        if wv is None:
            wv = self.web_view
        if wv is None:
            return
        try:
            hwnd = self._find_webview2_hwnd(wv)
            if not hwnd:
                return

            rect = wintypes.RECT()
            ctypes.windll.user32.GetClientRect(
                wintypes.HWND(hwnd), ctypes.byref(rect)
            )
            w = rect.right - rect.left
            h = rect.bottom - rect.top
            if w <= 0 or h <= 0:
                return

            r = self.WEB_RADIUS * 2

            ctypes.windll.user32.SetWindowRgn(
                wintypes.HWND(hwnd), 0, True
            )
            rgn = ctypes.windll.gdi32.CreateRoundRectRgn(
                0, 0, w + 1, h + 1, r, r
            )
            ctypes.windll.user32.SetWindowRgn(
                wintypes.HWND(hwnd), rgn, True
            )
        except Exception as e:
            print(f"[window] _apply_round_region 失败: {e}")

    def apply_web_view_round(self):
        wv = self.web_view
        if wv is None:
            return
        QTimer.singleShot(50, lambda w=wv: self._apply_round_region(w))
        QTimer.singleShot(200, lambda w=wv: self._apply_round_region(w))
        QTimer.singleShot(600, lambda w=wv: self._apply_round_region(w))

    # =========================================================
    # 网址
    # =========================================================
    def handle_url(self, url):
        """地址栏、外部入口。同主域 → 当前加载；跨域 → 交给 bar。"""
        host = url_host(url)
        if not host:
            return

        if not self._hosts:
            self._pending_input_host = host
            self._do_load(url)
            return

        if self._has_root_host(host):
            self._do_load(url)
            return

        self.request_url(url)

    def request_url(self, url):
        if not url:
            return

        now = time.time()
        last = self._last_request_url.get(url, 0)
        if now - last < 1.0:
            return
        self._last_request_url[url] = now

        cutoff = now - 10
        self._last_request_url = {
            u: t for u, t in self._last_request_url.items() if t > cutoff
        }

        try:
            payload = json.dumps({
                "cmd": "request_url",
                "window_id": self._window_id,
                "host": self._bar_host(),
                "url": url,
            }, ensure_ascii=False)
            IpcClient.send_to_role("bar", MSG_NAVIGATE, payload)
        except Exception as e:
            print("[window] request_url 失败:", e)

    # =========================================================
    # IPC
    # =========================================================
    def _on_complete_notify_toggled(self, on):
        """用户点"完成提醒"开关。"""
        print(f"[DBG] _on_complete_notify_toggled on={on}")
        self._complete_notify_on = bool(on)
        if on:
            self._dom_monitor.start()
        else:
            self._dom_monitor.stop()

        host = self._pin_host()

        # 独立存储：**任何站点**都记住开关状态，重开窗口仍生效
        if host:
            try:
                notify_store.set(host, bool(on))
            except Exception as e:
                print("[window] 保存完成提醒状态失败:", e)

        # 已固定的站点，额外同步到固定项（兼容旧数据 / 固定项自己也要用）
        if host and pinned_store.is_pinned(host):
            try:
                pinned_store.save_one(host, complete_notify=bool(on))
            except Exception as e:
                print("[window] 保存完成提醒状态失败:", e)

    def _on_dom_over(self):
        """DOM 停止新增 6s，强制置顶 + 声音提示。"""
        if not self._complete_notify_on:
            return

        # 声音提示
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception as e:
            print("[window] 声音提示失败:", e)

        self._bring_to_front()

    def minimize_or_offscreen(self):
        """用户点最小化按钮。

        提醒开着 → 移到屏幕外（保持 WebView2 活跃）；
        提醒没开 → 正常最小化。
        """
        if getattr(self, "_complete_notify_on", False):
            self._move_offscreen()
        else:
            self.showMinimized()

    def _move_offscreen(self):
        """把窗口移到所在屏幕右侧之外。记住当前位置以便恢复。"""
        try:
            if self._offscreen:
                return

            self._pre_offscreen_pos = self.pos()

            screen = self.screen() or QApplication.primaryScreen()
            geo = screen.availableGeometry()
            new_x = geo.right() + 120
            new_y = self.y()

            self.move(new_x, new_y)
            self._offscreen = True
            print(f"[window] 移出屏幕 x={new_x} y={new_y}")
        except Exception as e:
            print("[window] _move_offscreen 失败:", e)

    def _restore_from_offscreen(self):
        """从屏幕外移回原位置。"""
        if not self._offscreen:
            return
        try:
            if self._pre_offscreen_pos is not None:
                self.move(self._pre_offscreen_pos)
            else:
                screen = self.screen() or QApplication.primaryScreen()
                geo = screen.availableGeometry()
                self.move(
                    geo.left() + (geo.width() - self.width()) // 2,
                    geo.top() + (geo.height() - self.height()) // 2,
                )
            print("[window] 从屏幕外移回")
        except Exception as e:
            print("[window] _restore_from_offscreen 失败:", e)
        finally:
            self._offscreen = False
            self._pre_offscreen_pos = None

    def _bring_to_front(self):
        """把窗口带到前台。最小化时用 ShowWindow(SW_RESTORE) 强制恢复。"""
        try:
            # 在屏幕外 → 先移回来
            if getattr(self, "_offscreen", False):
                self._restore_from_offscreen()

            hwnd = int(self.winId())

            # 最小化 → 用底层 ShowWindow 强制恢复（比 showNormal 更可靠）
            try:
                SW_RESTORE = 9
                SW_SHOW = 5
                user32 = ctypes.windll.user32
                if user32.IsIconic(wintypes.HWND(hwnd)):
                    user32.ShowWindow(wintypes.HWND(hwnd), SW_RESTORE)
                else:
                    user32.ShowWindow(wintypes.HWND(hwnd), SW_SHOW)
            except Exception as e:
                print("[window] ShowWindow 失败:", e)

            if self.isMinimized():
                self.showNormal()

            self.show()
            self.raise_()
            self.activateWindow()

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            fg_hwnd = user32.GetForegroundWindow()
            fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
            cur_thread = kernel32.GetCurrentThreadId()

            if fg_thread and cur_thread and fg_thread != cur_thread:
                # 附加到前台线程，绕过前台锁
                user32.AttachThreadInput(fg_thread, cur_thread, True)
                try:
                    user32.SetForegroundWindow(wintypes.HWND(hwnd))
                    user32.BringWindowToTop(wintypes.HWND(hwnd))
                    user32.SetActiveWindow(wintypes.HWND(hwnd))
                finally:
                    user32.AttachThreadInput(fg_thread, cur_thread, False)
            else:
                user32.SetForegroundWindow(wintypes.HWND(hwnd))

            set_topmost(hwnd, True)
            QTimer.singleShot(900, lambda: set_topmost(hwnd, False))
        except Exception as e:
            print("[window] _bring_to_front 失败:", e)

    def _on_ipc_message(self, msg_type, payload):
        QTimer.singleShot(
            0, lambda t=msg_type, p=payload: self._handle_ipc(t, p)
        )

    def _handle_ipc(self, msg_type, payload):
        if msg_type == MSG_QUIT:
            self.close()
            return

        if msg_type == MSG_LANGUAGE_CHANGED:
            try:
                code = payload.decode("utf-8")
                i18n_load(code)
                self._refresh_texts()
            except Exception as e:
                print("[window] 切换语言失败:", e)
            return

        if msg_type == MSG_CONFIG_CHANGED:
            if self._mode in ("default", "search"):
                self._reload_config()
            return

        if msg_type == MSG_SHOW:
            self._bring_to_front()
            return

        if msg_type == MSG_DOWNLOAD_CANCEL_FOR_WINDOW:
            try:
                data = json.loads(payload.decode("utf-8"))
                url = data.get("url", "")
            except Exception:
                url = ""
            self._cancel_worker(url)
            return

        if msg_type == MSG_REVERT_TO_LAST_URL:
            return

        if msg_type == MSG_PIN_TOGGLE_FROM_BAR:
            # bar 处取消固定 / 满 24 → 关掉本地开关
            reason = ""
            try:
                data = json.loads(payload.decode("utf-8"))
                reason = data.get("reason", "")
            except Exception:
                pass

            self._pin_on = False
            if hasattr(self, "title_bar"):
                try:
                    self.title_bar.set_pin_switch_state(False)
                except Exception:
                    pass
            self._apply_taskbar_visibility()

            # 满 24 → 弹提示
            if reason == "full":
                try:
                    from i18n import t
                    box = QMessageBox(self)
                    box.setWindowTitle(t("app.title"))
                    box.setText(t("menu.pin_full"))
                    box.setIcon(QMessageBox.Icon.Information)
                    box.exec()
                except Exception as e:
                    print("[window] 弹满 24 提示失败:", e)

            return

        if msg_type == MSG_NAVIGATE:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                return
            url = data.get("url", "")
            if url:
                self._do_load(url)
            return

        if msg_type == MSG_FAVORITE_CHANGED:
            # 收藏变化广播 → 更新自己的星
            try:
                changed_url = payload.decode("utf-8")
            except Exception:
                changed_url = ""

            my_url = self._current_url or ""
            if changed_url and my_url and _norm_url(my_url) == _norm_url(changed_url):
                self._update_star_state()
            return

    def _refresh_texts(self):
        try:
            if hasattr(self, "title_bar") and hasattr(self.title_bar, "_refresh_texts"):
                self.title_bar._refresh_texts()
        except Exception as e:
            print("[window] 刷新文字失败:", e)

        try:
            dlg = getattr(self.title_bar, "_personalize_dialog", None)
            if dlg is not None and hasattr(dlg, "_refresh_texts"):
                dlg._refresh_texts()
        except Exception:
            pass

    # =========================================================
    # 导航
    # =========================================================
    def _do_load(self, url):
        if not url:
            return

        self._reset_favicon(url)

        # 每次主动导航都刷一次星
        QTimer.singleShot(100, self._update_star_state)

        wv = self.web_view
        if wv is None:
            return

        self._current_url = url
        self._update_web_view_geometry()
        wv.show()
        self.title_bar.set_browsing_mode(True)
        self.title_bar.set_address(_pretty_url_for_address_bar(url))
        self.update()

        try:
            wv.load_url(url)
        except Exception as e:
            print(f"[window] load_url 失败: {e}")

        QTimer.singleShot(50, self._update_web_view_geometry)
        QTimer.singleShot(200, self._update_web_view_geometry)
        QTimer.singleShot(600, self._update_web_view_geometry)

        self.apply_web_view_round()

        self._url_settle_timer.start()

        self._last_display_url = ""
        self._poll_url_once()
        if not self._url_poll_timer.isActive():
            self._url_poll_timer.start()

    def _current_url_str(self):
        wv = self.web_view
        try:
            if wv is not None:
                u = wv.url()
                if u:
                    return str(u)
        except Exception:
            pass
        return self._current_url or ""

    def _poll_url_once(self):
        if self._poll_busy:
            return
        wv = self.web_view
        if wv is None or not wv.isVisible():
            return
        if self._addr_editing:
            return

        self._poll_busy = True

        def _cb(real_url):
            self._poll_busy = False
            url_str = ""
            try:
                url_str = _clean_js_url(real_url)
                if not url_str or url_str == "about:blank":
                    return

                if url_str == self._last_display_url:
                    return

                host = url_host(url_str)
                if not host:
                    return
                if not self._has_root_host(host):
                    return

                self._last_display_url = url_str
                self.title_bar.set_address(
                    _pretty_url_for_address_bar(url_str)
                )

                if not _is_redirect_url(url_str):
                    self._current_url = url_str

                if self._popup is not None:
                    self._popup.append_url(url_str)
                    self._popup.set_current_url(url_str)

                if (not self._has_favicon_signal
                        and not self._favicon_poll.isActive()):
                    self._favicon_poll.start()

                self._fetch_title(url_str)
            except Exception as e:
                print(f"[window] _poll_url_once 回调异常: {e}")
            finally:
                # 不管 URL 变没变，都刷新一次星
                try:
                    self._update_star_state(url_str)
                except Exception:
                    pass

        try:
            wv.eval_js("location.href", _cb)
        except Exception as e:
            self._poll_busy = False
            print(f"[window] _poll_url_once eval_js 失败: {e}")

    @staticmethod
    def _entry_alive(entry):
        """检查 registry 里那条记录对应的进程还在不在。"""
        if not entry:
            return False
        pid = entry.get("pid")
        if not pid:
            return False
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            h = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid)
            )
            if not h:
                return False
            ctypes.windll.kernel32.CloseHandle(h)
            return True
        except Exception:
            return True

    def _on_url_settled(self):
        wv = self.web_view
        if wv is None:
            return

        def _cb(real_url):
            try:
                url_str = _clean_js_url(real_url)
                if not url_str or url_str == "about:blank":
                    return
                new_host = url_host(url_str)
                if not new_host:
                    return

                is_redirect = _is_redirect_url(url_str)

                if not self._hosts:
                    # 1. 有同 host 窗口 → 转给 bar，自毁
                    role, entry = find_window_by_host(new_host)
                    print(f"[DBG] df 新窗口访问 {new_host}，"
                          f"find_window_by_host 结果 role={role} "
                          f"alive={self._entry_alive(entry) if entry else False}")
                    if role and self._entry_alive(entry):
                        print("[DBG] 走分支 1：转给 bar + 自毁")
                        self.request_url(url_str)
                        if not self._has_loaded_once:
                            QTimer.singleShot(100, self.close)
                        return

                    # 2. 没有，但该主域有固定 → 转给 bar（bar 会新建带固定的窗口），自毁
                    root = self._root_host_of(url_str)
                    print(f"[DBG] df 新窗口访问 {new_host}，"
                          f"root={root} is_pinned="
                          f"{pinned_store.is_pinned(root) if root else False}")
                    if root and pinned_store.is_pinned(root):
                        print("[DBG] 走分支 2：转给 bar（新建带固定）+ 自毁")
                        self.request_url(url_str)
                        if not self._has_loaded_once:
                            QTimer.singleShot(100, self.close)
                        return

                    print("[DBG] 走分支 3：自己加载")
                    # 3. 都没有 → 默认窗口自己加载，获得 host
                    if self._pending_input_host:
                        self._add_host(self._pending_input_host, primary=False)
                    self._add_host(new_host, primary=True)
                    self._pending_input_host = ""
                    if not is_redirect:
                        self._current_url = url_str
                    self.title_bar.set_address(
                        _pretty_url_for_address_bar(url_str)
                    )
                elif self._matches_host(new_host):
                    if not is_redirect:
                        self._current_url = url_str
                    if new_host not in self._hosts:
                        self._add_host(new_host, primary=False)
                    self.title_bar.set_address(
                        _pretty_url_for_address_bar(url_str)
                    )
                else:
                    self._restore_address_bar()
                    self.request_url(url_str)

                if self._popup is not None and self._has_root_host(new_host):
                    self._popup.append_url(url_str)
                    self._popup.set_current_url(url_str)
            except Exception as e:
                print(f"[window] _on_url_settled 回调异常: {e}")
            finally:
                try:
                    self._update_star_state()
                except Exception:
                    pass

        try:
            wv.eval_js("location.href", _cb)
        except Exception as e:
            print(f"[window] _on_url_settled eval_js 失败: {e}")

    def _restore_address_bar(self):
        wv = self.web_view
        if wv is None:
            return

        def _cb(real_url):
            try:
                url_str = _clean_js_url(real_url)
                if url_str and url_str != "about:blank":
                    self.title_bar.set_address(
                        _pretty_url_for_address_bar(url_str)
                    )
            except Exception:
                pass

        try:
            wv.eval_js("location.href", _cb)
        except Exception:
            pass

    # =========================================================
    # < / > ：popup 列表上下
    # =========================================================
    def _prev_url(self):
        if self._popup is None:
            return
        urls = self._popup.urls()
        if not urls:
            return
        cur = self._popup.current_url()
        try:
            idx = urls.index(cur) if cur else 0
        except ValueError:
            idx = 0
        idx = max(0, idx - 1)
        self._on_popup_url_selected(urls[idx])

    def _next_url(self):
        if self._popup is None:
            return
        urls = self._popup.urls()
        if not urls:
            return
        cur = self._popup.current_url()
        try:
            idx = urls.index(cur) if cur else -1
        except ValueError:
            idx = -1
        idx = min(len(urls) - 1, idx + 1)
        self._on_popup_url_selected(urls[idx])

    # =========================================================
    # 个性化
    # =========================================================
    def apply_personalize(self, color):
        border, inner = Theme.apply_theme(color)
        self.title_bar.apply_theme_color(border)
        if hasattr(self, "corner_mask"):
            self.corner_mask.bg_color = border
            self.corner_mask.update()

        if self._mode != "search":
            s = load_window_settings(self._mode, self._window_id)
            s["theme_color"] = QColor(color).name()
            save_window_settings(self._mode, self._window_id, s)

        self._broadcast_config_changed()
        self.update()

    def apply_background_image(self, path, images=None):
        if path:
            real = resolve_path(path)
            pm = QPixmap(real)
            if pm.isNull():
                return
            self._bg_path = real
            self._bg_pixmap = pm
        else:
            self._bg_path = ""
            self._bg_pixmap = None

        if self._mode != "search":
            s = load_window_settings(self._mode, self._window_id)
            if images is not None:
                # 存盘时把内置资源转回 {RES}/... 形式，
                # 免得写死绝对路径、换安装位置就失效
                s["background_images"] = [to_stored_path(p) for p in images]
            s["background_current"] = to_stored_path(path) if path else ""
            save_window_settings(self._mode, self._window_id, s)

        self._broadcast_config_changed()
        self.update()

    def current_theme_color(self):
        s = load_window_settings(self._mode, self._window_id)
        return QColor(s.get("theme_color", "#d0d0d0"))

    def current_background_images(self):
        s = load_window_settings(self._mode, self._window_id)
        return list(s.get("background_images", []))

    def current_background_image(self):
        s = load_window_settings(self._mode, self._window_id)
        return s.get("background_current", "")

    # =========================================================
    # 绘制
    # =========================================================
    def _outline_color(self):
        base = QColor(Theme.BG_COLOR)
        return QColor(
            255 - base.red(),
            255 - base.green(),
            255 - base.blue(),
            self.OUTLINE_ALPHA,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        b = self.BORDER
        radius = 0 if self.isMaximized() else self.RADIUS

        painter.setBrush(self._outline_color())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), radius, radius)

        inner = QRectF(
            b, b,
            self.width() - 2 * b,
            self.height() - 2 * b,
        )
        inner_radius = max(0, radius - b)
        painter.setBrush(Theme.BG_COLOR)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(inner, inner_radius, inner_radius)

        try:
            x = self.SIDE_MARGIN + b
            y = self.TOP_BAR_HEIGHT + self.WEB_TOP_GAP + b
            w = self.width() - 2 * self.SIDE_MARGIN - 2 * b
            h = self.height() - y - self.BOTTOM_MARGIN - b

            if w <= 0 or h <= 0:
                return

            rect = QRectF(x, y, w, h)
            r = QRect(int(x), int(y), int(w), int(h))

            if self._bg_pixmap is not None and not self._bg_pixmap.isNull():
                scaled = self._bg_pixmap.scaled(
                    r.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
                sx = (scaled.width() - r.width()) // 2
                sy = (scaled.height() - r.height()) // 2
                cropped = scaled.copy(sx, sy, r.width(), r.height())

                path = QPainterPath()
                path.addRoundedRect(rect, self.WEB_RADIUS, self.WEB_RADIUS)
                painter.setClipPath(path)
                painter.drawPixmap(r.topLeft(), cropped)
                painter.setClipping(False)
            else:
                painter.setBrush(Theme.WEB_PLACEHOLDER_COLOR)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(rect, self.WEB_RADIUS, self.WEB_RADIUS)
        except RuntimeError:
            pass

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if hasattr(self, "title_bar"):
                self.title_bar.update_max_icon()
                self.title_bar.update()
        elif event.type() == QEvent.Type.ActivationChange:
            # 窗口被激活（任务栏点击等）→ 若在屏幕外就移回来
            if self.isActiveWindow() and getattr(self, "_offscreen", False):
                self._restore_from_offscreen()
        super().changeEvent(event)

    # =========================================================
    # 几何
    # =========================================================
    def _center_input_box(self):
        w = self.input_box.width()
        h = self.input_box.height()
        self.input_box.move(
            (self.width() - w) // 2,
            (self.height() - h) // 2,
        )

    def _update_web_view_geometry(self):
        if self._resizing:
            return
        self._resizing = True
        try:
            wv = self.web_view
            if wv is None:
                return

            b = self.BORDER
            x = self.SIDE_MARGIN + b
            y = self.TOP_BAR_HEIGHT + self.WEB_TOP_GAP + b
            w = self.width() - 2 * self.SIDE_MARGIN - 2 * b
            h = self.height() - y - self.BOTTOM_MARGIN - b

            if w <= 0 or h <= 0:
                return

            wv.setGeometry(x, y, w, h)
        except RuntimeError:
            pass
        finally:
            self._resizing = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "title_bar"):
            self.title_bar.setGeometry(
                self.BORDER, self.BORDER,
                self.width() - 2 * self.BORDER,
                self.TOP_BAR_HEIGHT,
            )
        if self.input_box.isVisible():
            self._center_input_box()
        wv = self.web_view
        if wv is not None and wv.isVisible():
            self._update_web_view_geometry()
            self.apply_web_view_round()
        self._refresh_popup_visibility()

        try:
            if getattr(self, "_pw_panel", None) is not None:
                password_hook._relayout(self)
        except Exception:
            pass

    # =========================================================
    # 输入
    # =========================================================
    def show_input_box(self):
        wv = self.web_view
        if wv is not None:
            wv.hide()
        self.input_box.show()
        self._center_input_box()
        self.title_bar.set_browsing_mode(False)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.show_input_box()
        else:
            super().keyPressEvent(event)

    def visit(self):
        text = self.input_box.text()
        if not text:
            return None

        # 有当前引擎 → 一律搜索
        if self._current_engine:
            url = self._build_search_url(text)
            if url:
                self.handle_url(url)
                return url
            return None

        # 无引擎 → 现有逻辑
        if self._is_url(text):
            if not text.startswith(("http://", "https://")):
                text = "https://" + text
            self.handle_url(text)
            return text
        return None

    def visit_url(self, text):
        if not text:
            return None

        if self._current_engine:
            url = self._build_search_url(text)
            if url:
                self.handle_url(url)
                return url
            return None

        if self._is_url(text):
            if not text.startswith(("http://", "https://")):
                text = "https://" + text
            self.handle_url(text)
            return text
        return None

    def _is_url(self, text):
        if text.startswith("http://") or text.startswith("https://"):
            return True
        if " " not in text and "." in text:
            return True
        return False

    # =========================================================
    # 收藏
    # =========================================================
    def _on_star_left_clicked(self):
        """左键点星：切换收藏。"""
        url = self._current_url or ""
        if not url:
            return

        try:
            from favorites_store import is_favorited, add, remove
        except Exception as e:
            print("[window] 导入 favorites_store 失败:", e)
            return

        if is_favorited(url):
            # 已收藏 → 取消
            try:
                remove(url)
            except Exception as e:
                print("[window] 取消收藏失败:", e)
            self._update_star_state()
            self._broadcast_favorite_changed(url)
        else:
            # 未收藏 → 收藏（异步抓 title）
            self._add_favorite_with_title(url)

    def _broadcast_favorite_changed(self, url):
        """广播收藏变化给所有窗口。"""
        try:
            from ipc import broadcast, MSG_FAVORITE_CHANGED
            broadcast(
                MSG_FAVORITE_CHANGED,
                (url or "").encode("utf-8"),
            )
        except Exception as e:
            print("[window] 广播收藏变化失败:", e)

    def _add_favorite_with_title(self, url):
        """收藏当前 URL，异步拿 title。"""
        def _do_add(title):
            try:
                from favorites_store import add
                add(url, title or url)
            except Exception as e:
                print("[window] 收藏失败:", e)
            self._update_star_state()
            self._broadcast_favorite_changed(url)

        wv = self.web_view
        if wv is None or not wv.isVisible():
            _do_add("")
            return

        def _cb(raw_title):
            try:
                title = _clean_js_url(raw_title)
                _do_add(title or "")
            except Exception:
                _do_add("")

        try:
            wv.eval_js("document.title", _cb)
        except Exception:
            _do_add("")

    def _update_star_state(self, url=None):
        """更新星按钮的颜色。url 为空时用 _current_url。"""
        if not url:
            url = self._current_url or ""
        on = False
        if url:
            try:
                from favorites_store import is_favorited
                on = is_favorited(url)
            except Exception:
                on = False

        try:
            if hasattr(self, "title_bar") and hasattr(self.title_bar, "star_btn"):
                self.title_bar.star_btn.set_on(on)
        except Exception:
            pass

    def _on_star_right_clicked(self):
        """右键点星：弹收藏菜单。"""
        if self._fav_menu is not None:
            try:
                self._fav_menu.hide()
                self._fav_menu.deleteLater()
            except Exception:
                pass
            self._fav_menu = None
            return

        try:
            from favorites_menu import FavoritesMenu
            menu = FavoritesMenu(self)
        except Exception as e:
            print("[window] 创建收藏菜单失败:", e)
            return

        menu.url_selected.connect(self._on_favorite_selected)
        menu.url_closed.connect(self._on_favorite_closed)

        # 定位到星按钮下方（全局坐标）
        try:
            btn = self.title_bar.star_btn
            global_pos = btn.mapToGlobal(QPoint(0, btn.height() + 4))
        except Exception:
            global_pos = QPoint(0, 0)

        self._fav_menu = menu
        menu.popup_at(global_pos)

    def _on_favorite_selected(self, url):
        """点收藏条目（× 以外）→ 交给当前窗口访问。"""
        if not url:
            return
        self._fav_menu = None
        # 走 handle_url：自己的加载，不是的转 bar
        try:
            self.handle_url(url)
        except Exception as e:
            print("[window] 访问收藏失败:", e)

    def _on_favorite_closed(self, url):
        """菜单里删了一条收藏。"""
        self._update_star_state()
        # 广播给所有窗口
        self._broadcast_favorite_changed(url)

    # =========================================================
    # 搜索引擎
    # =========================================================
    def _build_search_url(self, query):
        """把当前引擎 + query 拼成 URL。"""
        try:
            from search_engines import build_search_url
            return build_search_url(self._current_engine, query)
        except Exception as e:
            print("[window] 拼搜索 URL 失败:", e)
            return ""

    def _on_engine_btn_clicked(self):
        """点左侧引擎按钮 → 弹透明长条。"""
        if self._engine_picker is not None:
            try:
                self._engine_picker.hide()
                self._engine_picker.deleteLater()
            except Exception:
                pass
            self._engine_picker = None
            return

        try:
            from search_engines import load_all
            engines = load_all()
        except Exception as e:
            print("[window] 读引擎列表失败:", e)
            engines = []

        if not engines:
            from i18n import t as _t
            try:
                box = QMessageBox(self)
                box.setWindowTitle(_t("app.title"))
                box.setText(_t("engine.no_engine"))
                box.setIcon(QMessageBox.Icon.Information)
                box.exec()
            except Exception as e:
                print("[window] 弹无引擎提示失败:", e)
            return

        # 顶部插入"默认"项（无引擎模式）
        engines_with_default = [{"_default": True, "abbr": "", "url": ""}]
        engines_with_default.extend(engines)

        try:
            from input_box import EnginePicker
            picker = EnginePicker(engines_with_default, self)
        except Exception as e:
            print("[window] 创建引擎长条失败:", e)
            return

        picker.selected.connect(self._on_engine_selected)

        # 把本地已有的 favicon 先塞进长条（不等网络）
        try:
            from search_icons import load_icon as _load_eng_icon
            for eng in engines:
                if eng.get("_default"):
                    continue
                pm = _load_eng_icon(eng)
                if pm is not None and not pm.isNull():
                    picker.set_item_favicon(eng.get("url", ""), pm)
        except Exception as e:
            print("[window] 读本地引擎图标失败:", e)

        # 定位到按钮下方（相对 window 局部坐标）
        btn = self.input_box.engine_button()
        try:
            # 按钮左下角在 window 坐标系里的位置
            btn_bottom_left = btn.mapTo(self, QPoint(0, btn.height()))
            local_pos = QPoint(
                btn_bottom_left.x() - 6,
                btn_bottom_left.y() + 14,
            )
        except Exception:
            local_pos = QPoint(0, 0)

        self._engine_picker = picker
        picker.popup_at(local_pos)

    def _on_engine_selected(self, engine):
        """用户从长条里选了引擎（或默认）。"""
        if engine and engine.get("_default"):
            self._clear_engine()
        else:
            self._set_engine(engine)

        # 关长条
        if self._engine_picker is not None:
            try:
                self._engine_picker.hide()
                self._engine_picker.deleteLater()
            except Exception:
                pass
            self._engine_picker = None

    def _clear_engine(self):
        """回到无引擎模式。"""
        self._current_engine = None
        try:
            btn = self.input_box.engine_button()
            btn.clear_engine()
        except Exception as e:
            print("[window] 清引擎失败:", e)

    def _set_engine(self, engine):
        """切换当前引擎。同步按钮图标 + 异步抓 favicon。"""
        if not engine or not isinstance(engine, dict):
            return
        self._current_engine = engine

        url = engine.get("url", "") or ""
        abbr = (engine.get("abbr") or "").upper()

        try:
            btn = self.input_box.engine_button()
            btn.set_pixmap(None)     # 清掉旧 favicon
            btn.set_abbr(abbr)       # 先显示字母
        except Exception:
            pass

        # 异步抓 favicon
        if url:
            self._fetch_engine_favicon(url)

    def _fetch_engine_favicon(self, engine_url):
        """给单个引擎抓 favicon。

        本地有直接用；没有走 search_icons 异步抓。
        """
        if not engine_url:
            return

        # 内存缓存命中
        if engine_url in self._engine_favicon_cache:
            pm = self._engine_favicon_cache[engine_url]
            if pm is not None and not pm.isNull():
                self._apply_engine_favicon(pm)
                return

        eng = self._current_engine or {}
        if eng.get("url") != engine_url:
            return

        try:
            from search_icons import fetch_icon
            fetch_icon(
                eng,
                lambda e, pm: self._on_engine_icon_fetched(e, pm),
                parent=self,
            )
        except Exception as e:
            print("[window] 抓引擎 favicon 失败:", e)

    def _apply_engine_favicon(self, pm):
        """把 favicon 画到引擎按钮上。"""
        try:
            btn = self.input_box.engine_button()
            btn.set_pixmap(pm)
        except Exception as e:
            print("[window] 设置引擎 favicon 失败:", e)

    def _prefetch_engine_icons(self):
        """窗口启动后，后台批量抓所有引擎的 favicon。"""
        try:
            from search_engines import load_all
            from search_icons import fetch_all
            engines = load_all()
        except Exception as e:
            print("[window] 预抓引擎图标读列表失败:", e)
            return

        if not engines:
            return

        def _on_one(engine, pm):
            self._on_engine_icon_fetched(engine, pm)

        try:
            fetch_all(engines, _on_one, parent=self)
        except Exception as e:
            print("[window] 预抓引擎图标失败:", e)

    def _on_engine_icon_fetched(self, engine, pm):
        """单个引擎图标抓完。

        * 更新长条里对应的图标（如果长条在显示）
        * 更新左侧按钮（如果这个引擎是当前引擎）
        * 缓存到内存
        """
        if not isinstance(engine, dict):
            return
        url = engine.get("url", "")

        # 缓存
        if pm is not None and not pm.isNull() and url:
            self._engine_favicon_cache[url] = pm

        # 更新长条
        picker = self._engine_picker
        if picker is not None and pm is not None and not pm.isNull():
            try:
                picker.set_item_favicon(url, pm)
            except Exception as e:
                print("[window] 更新长条图标失败:", e)

        # 更新左侧按钮（如果当前引擎就是它）
        cur_url = (self._current_engine or {}).get("url", "")
        if cur_url and cur_url == url and pm is not None and not pm.isNull():
            self._apply_engine_favicon(pm)

    # =========================================================
    # 拖拽
    # =========================================================
    def _maybe_close_engine_picker(self, event):
        """点 window 上别的地方时，关掉引擎长条。"""
        if self._engine_picker is None:
            return
        try:
            local = event.position().toPoint()
            picker_rect = self._engine_picker.geometry()
            if picker_rect.contains(local):
                return
            btn = self.input_box.engine_button()
            btn_rect = QRect(btn.mapTo(self, QPoint(0, 0)), btn.size())
            if btn_rect.contains(local):
                return
        except Exception:
            pass

        try:
            self._engine_picker.hide()
            self._engine_picker.deleteLater()
        except Exception:
            pass
        self._engine_picker = None

    def _maybe_close_favorites_menu(self, event):
        """独立窗口模式下，由 focusOut 自己关，这里空操作。"""
        pass

    def mousePressEvent(self, event):
        # 点 window 其他地方 → 关引擎长条
        self._maybe_close_engine_picker(event)

        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            edge = self._get_edge(event.position().toPoint())
            if edge:
                self._resize_edge = edge
                self._start_pos = event.globalPosition().toPoint()
                self._start_geo = self.geometry()

    def mouseMoveEvent(self, event):
        if self.isMaximized():
            return

        edge = self._get_edge(event.position().toPoint())
        self._update_cursor(edge)

        if (event.buttons() & Qt.MouseButton.LeftButton
                and self._resize_edge
                and self._start_geo):
            delta = event.globalPosition().toPoint() - self._start_pos
            self._do_resize(self._resize_edge, delta)

    def mouseReleaseEvent(self, event):
        self._resize_edge = None
        self._start_geo = None
        self._start_pos = None

    def _get_edge(self, pos):
        M = self.RESIZE_MARGIN
        C = self.CORNER_MARGIN

        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        edges = []

        if x < M or (x < C and (y < C or y > h - C)):
            edges.append("l")
        if x > w - M or (x > w - C and (y < C or y > h - C)):
            edges.append("r")
        if y < M or (y < C and (x < C or x > w - C)):
            edges.append("t")
        if y > h - M or (y > h - C and (x < C or x > w - C)):
            edges.append("b")

        return "".join(edges) if edges else None

    def _update_cursor(self, edge):
        if not edge:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif edge in ("l", "r"):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge in ("t", "b"):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif edge in ("lt", "rb"):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in ("rt", "lb"):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _do_resize(self, edge, delta):
        geo = self._start_geo
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

        if "l" in edge:
            x += delta.x()
            w -= delta.x()
        if "r" in edge:
            w += delta.x()
        if "t" in edge:
            y += delta.y()
            h -= delta.y()
        if "b" in edge:
            h += delta.y()

        if w >= self.minimumWidth() and h >= self.minimumHeight():
            self.setGeometry(x, y, w, h)

    # =========================================================
    # 生命周期
    # =========================================================
    def closeEvent(self, event):
        # 关掉引擎长条
        try:
            if self._engine_picker is not None:
                self._engine_picker.close_picker()
                self._engine_picker = None
        except Exception:
            pass

        # 关掉收藏菜单
        try:
            if self._fav_menu is not None:
                self._fav_menu._close()
                self._fav_menu = None
        except Exception:
            pass

        # 关窗保存固定记忆
        try:
            self._save_pinned_memory()
        except Exception:
            pass

        try:
            self._dom_monitor.stop()
        except Exception:
            pass

        try:
            if self._taskbar_timer.isActive():
                self._taskbar_timer.stop()
        except Exception:
            pass

        try:
            if self._popup is not None:
                self._popup.hide()
        except Exception:
            pass

        try:
            self._url_poll_timer.stop()
        except Exception:
            pass

        try:
            self._favicon_poll.stop()
        except Exception:
            pass

        try:
            if hasattr(self, "_round_timer"):
                self._round_timer.stop()
        except Exception:
            pass

        for _url, proc in list(self._download_workers.items()):
            try:
                proc.terminate()
                if not proc.waitForFinished(1000):
                    proc.kill()
            except Exception:
                pass
        self._download_workers.clear()

        try:
            if self._web_view is not None:
                self._web_view.close()
                self._web_view.setParent(None)
                self._web_view.deleteLater()
        except Exception:
            pass
        self._web_view = None

        try:
            if (hasattr(self, "title_bar")
                    and self.title_bar._personalize_dialog is not None):
                self.title_bar._personalize_dialog.close()
                self.title_bar._personalize_dialog = None
        except Exception:
            pass

        try:
            popup = getattr(
                getattr(self, "title_bar", None), "_popup", None
            )
            if popup is not None:
                try:
                    popup.close()
                except Exception:
                    pass
                self.title_bar._popup = None
        except Exception:
            pass

        try:
            t = getattr(self, "_pw_hide_timer", None)
            if t is not None:
                t.stop()
                self._pw_hide_timer = None
        except Exception:
            pass

        try:
            if getattr(self, "_pw_panel", None) is not None:
                self._pw_panel.hide()
                self._pw_panel.setParent(None)
                self._pw_panel.deleteLater()
                self._pw_panel = None
        except Exception:
            pass

        try:
            self._ipc_server.stop()
        except Exception:
            pass
        super().closeEvent(event)


def main():
    import traceback

    def _excepthook(exc_type, exc_value, exc_tb):
        traceback.print_exception(exc_type, exc_value, exc_tb)

    sys.excepthook = _excepthook

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="default",
                        choices=["default", "search", "custom"])
    parser.add_argument("--id", default="df-0")
    parser.add_argument("--host", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--pinned-url", default="")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 应用默认图标（任务栏兜底）
    try:
        from window_icon import default_icon
        _di = default_icon()
        if not _di.isNull():
            app.setWindowIcon(_di)
    except Exception as e:
        print("[window] 设应用图标失败:", e)

    try:
        from settings_backend import SettingsBackend
        i18n_load(SettingsBackend().get_language())
    except Exception as e:
        print("[window] 加载语言失败:", e)

    # 任务栏分开：本进程独立 AppUserModelID
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            f"MyBrowser.Window.{args.id}"
        )
    except Exception as e:
        print("[window] 设置 AppUserModelID 失败:", e)

    w = RoundedWindow(
        mode=args.mode,
        window_id=args.id,
        host=args.host,
        start_url=args.url,
        pinned_url=args.pinned_url,
    )

    # 窗口默认图标
    try:
        from window_icon import default_icon
        _di = default_icon()
        if not _di.isNull():
            w.setWindowIcon(_di)
    except Exception as e:
        print("[window] 设窗口默认图标失败:", e)

    w.show()

    # 启动后延迟置顶 + 抢焦点（等窗口完全创建）
    def _bring_to_front():
        try:
            w.raise_()
            w.activateWindow()
            set_topmost(int(w.winId()), True)
            QTimer.singleShot(800, lambda: set_topmost(int(w.winId()), False))
        except Exception as e:
            print("[window] bring_to_front 失败:", e)

    QTimer.singleShot(300, _bring_to_front)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()