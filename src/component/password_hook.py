# -*- coding: utf-8 -*-
"""密码保存 / 填充功能（纯函数模块，不写类）。

由 window.RoundedWindow 调用：
  * install(window)            —— 注入信号、建面板
  * on_js_message(window, d)   —— 处理 JS 来的消息，返回 True 表示已处理

面板形态（两个状态，用户只能切换，不能关闭）：
  * 展开态：账密列表 + "保存当前账密"按钮
  * 收起态：只留顶部一条横条（带 ⌃）

显隐完全由"页面有没有账密输入框"决定：
  * has_pw: false -> true   面板出现（用上次的形态）
  * has_pw: true  -> false  面板消失
  * has_pw 一直 true        只更新列表

面板贴在主窗口右上角、标题栏下方，展开态 / 收起态都能沿上边缘左右拖。

存储：项目根目录 passwords.json
    {
        "bigmodel.cn": [
            {"username": "999", "password": "123"},
            ...
        ],
        ...
    }
列表只显示"当前页主域"对应的那组账密。
"""
from i18n import t
import os
import json

from loader import *


# ======================================================================
# 路径
# ======================================================================
import apppaths

STORE_PATH = os.path.join(apppaths.APP_DIR, "passwords.json")


# ======================================================================
# 注入 JS
# ======================================================================
PASSWORD_JS = r"""
(function() {
    if (window.__pw_watch_installed) return;
    window.__pw_watch_installed = true;

    function report(msg) {
        try {
            if (window.chrome && window.chrome.webview) {
                window.chrome.webview.postMessage(JSON.stringify(msg));
            } else if (window.ipc && window.ipc.postMessage) {
                window.ipc.postMessage(JSON.stringify(msg));
            }
        } catch (e) {}
    }

    function findUserInput(pwEl) {
        var form = pwEl.closest("form");
        var scope = form || document.body;
        var allInputs = scope.querySelectorAll(
            'input:not([type="password"]):not([type="hidden"])' +
            ':not([type="submit"]):not([type="button"])' +
            ':not([type="checkbox"]):not([type="radio"])' +
            ':not([type="file"]):not([type="image"])'
        );
        var result = null;
        for (var i = 0; i < allInputs.length; i++) {
            var el = allInputs[i];
            if (el.compareDocumentPosition(pwEl) &
                Node.DOCUMENT_POSITION_FOLLOWING) {
                result = el;
            } else {
                break;
            }
        }
        if (result) return result;
        return allInputs.length > 0 ? allInputs[0] : null;
    }

    function clearVal(el) {
        if (!el) return;
        try {
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, "value"
            ).set;
            setter.call(el, "");
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        } catch (e) {
            el.value = "";
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        }
    }

    function fillVal(el, val) {
        if (!el || !val) return;
        try {
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, "value"
            ).set;
            setter.call(el, val);
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        } catch (e) {
            el.value = val;
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        }
    }

    window.__pw_clear_all = function() {
        try {
            var pwInputs = document.querySelectorAll('input[type="password"]');
            for (var i = 0; i < pwInputs.length; i++) {
                clearVal(pwInputs[i]);
            }
            var allUserInputs = document.querySelectorAll(
                'input:not([type="password"]):not([type="hidden"])' +
                ':not([type="submit"]):not([type="button"])' +
                ':not([type="checkbox"]):not([type="radio"])' +
                ':not([type="file"]):not([type="image"])'
            );
            for (var j = 0; j < allUserInputs.length; j++) {
                clearVal(allUserInputs[j]);
            }
            return "ok";
        } catch (e) {
            return "err:" + e;
        }
    };

    window.__pw_fill = function(user, pw) {
        try {
            var pwInputs = document.querySelectorAll('input[type="password"]');
            if (pwInputs.length === 0) return "no_pw_input";

            var pwInput = pwInputs[0];
            var userInput = findUserInput(pwInput);

            if (pw) fillVal(pwInput, pw);
            if (userInput && user) fillVal(userInput, user);

            return "ok";
        } catch (e) {
            return "err:" + e;
        }
    };

    function currentCredential() {
        var pwInputs = document.querySelectorAll('input[type="password"]');
        for (var i = 0; i < pwInputs.length; i++) {
            var pw = pwInputs[i].value || "";
            if (!pw) continue;
            var userInput = findUserInput(pwInputs[i]);
            var user = userInput ? (userInput.value || "") : "";
            return { user: user, pw: pw };
        }
        return null;
    }

    function hasPasswordInput() {
        return document.querySelectorAll('input[type="password"]').length > 0;
    }

    setInterval(function() {
        try {
            var hasPw = hasPasswordInput();
            var c = hasPw ? currentCredential() : null;
            report({
                type: "pw_state",
                has_pw: hasPw,
                username: c ? c.user : "",
                password: c ? c.pw : "",
                url: location.href
            });
        } catch (e) {}
    }, 800);
})();
"""


# ======================================================================
# 存储
# ======================================================================
def _root_host(host):
    if not host:
        return ""
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])


def _host_of_url(url):
    try:
        from urllib.parse import urlparse
        return _root_host(urlparse(url).hostname or "")
    except Exception:
        return ""


def _load_store():
    try:
        if os.path.isfile(STORE_PATH):
            with open(STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _save_store(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[pw] 存失败:", e)


# ======================================================================
# 面板尺寸 / 颜色
# ======================================================================
PANEL_W = 240
PANEL_H_EXPANDED = 200
PANEL_H_COLLAPSED = 32    # 收起态加高，避免文字被上下边挤
TOP_MARGIN = 41           # 标题栏底部 39 + 缝隙 2
SIDE_MARGIN = 16          # 面板右侧距窗口右边
RADIUS = 8

BG_COLOR = QColor(60, 60, 60, 245)          # 深灰
BORDER_COLOR = QColor(138, 138, 138, 255)   # 浅灰
TEXT_COLOR = "#e0e0e0"
SUBTEXT_COLOR = "#a0a0a0"


# ======================================================================
# 面板控件（自绘圆角）
# ======================================================================
class _PwPanel(QFrame):
    """方形面板。子控件，parent 为主窗口。"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(
            "QFrame {"
            "  background: rgb(60, 60, 60);"
            "  border: 1px solid rgb(138, 138, 138);"
            "}"
        )


# ======================================================================
# 安装
# ======================================================================
def install(window):
    window._pw_installed = False
    window._pw_panel = None
    window._pw_expanded = True
    window._pw_visible = False
    window._pw_has_pw = False
    window._pw_cur_user = ""
    window._pw_cur_pw = ""
    window._pw_drag_offset = None
    window._pw_panel_x = None
    window._pw_hide_timer = None       # 延迟收回

    QTimer.singleShot(0, lambda: _build_panel(window))


def _build_panel(window):
    panel = _PwPanel(window)
    panel.setFixedSize(PANEL_W, PANEL_H_EXPANDED)
    panel.hide()

    outer = QVBoxLayout(panel)
    outer.setContentsMargins(10, 6, 10, 10)
    outer.setSpacing(6)

    # ---- 顶部条：标题 + 收起按钮 ----
    head = QHBoxLayout()
    head.setContentsMargins(0, 0, 0, 0)
    head.setSpacing(4)

    title = QLabel(t("password.panel_title"))
    title.setStyleSheet(
        f"color: {TEXT_COLOR}; background: transparent;"
        f"border: none; font-size: 12px;")
    head.addWidget(title)
    head.addStretch(1)

    toggle_btn = QPushButton("⌃")
    toggle_btn.setFixedSize(20, 18)
    toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    toggle_btn.setStyleSheet(
        f"QPushButton {{"
        f"  color: {SUBTEXT_COLOR}; background: transparent;"
        f"  border: none; font-size: 12px;"
        f"}}"
        f"QPushButton:hover {{ color: {TEXT_COLOR}; }}"
    )
    toggle_btn.clicked.connect(lambda: _toggle_expand(window))
    head.addWidget(toggle_btn)

    outer.addLayout(head)

    # ---- 列表 ----
    lst = QListWidget(panel)
    lst.setStyleSheet(
        f"QListWidget {{"
        f"  background: rgba(255,255,255,0.06);"
        f"  border: 1px solid rgba(255,255,255,0.15);"
        f"  color: {TEXT_COLOR};"
        f"  font-size: 12px;"
        f"  outline: none;"
        f"}}"
        f"QListWidget::item {{ height: 28px; padding-left: 6px; }}"
        f"QListWidget::item:hover {{ background: rgba(255,255,255,0.10); }}"
        f"QListWidget::item:selected {{"
        f"  background: rgba(120,170,255,0.35); color: #ffffff;"
        f"}}"
    )
    lst.itemClicked.connect(lambda item: _on_item_clicked(window, item))
    outer.addWidget(lst, 1)

    # ---- 安全提示 ----
    warn_lbl = QLabel(t("password.warning"))
    warn_lbl.setWordWrap(True)
    warn_lbl.setStyleSheet(
        "color: #e0a060; background: transparent;"
        "border: none; font-size: 10px;")
    outer.addWidget(warn_lbl)
    # ------------------

    # ---- 保存按钮 ----
    save_btn = QPushButton(t("password.save_current"))
    save_btn.setFixedHeight(28)
    save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    save_btn.setStyleSheet(
        f"QPushButton {{"
        f"  background: rgba(255,255,255,0.10);"
        f"  color: {TEXT_COLOR};"
        f"  border: 1px solid rgba(255,255,255,0.20);"
        f"  font-size: 12px;"
        f"}}"
        f"QPushButton:hover {{ background: rgba(255,255,255,0.16); }}"
        f"QPushButton:pressed {{ background: rgba(255,255,255,0.22); }}"
    )
    save_btn.clicked.connect(lambda: _on_save_clicked(window))
    outer.addWidget(save_btn)

    # 面板拖动
    panel.mousePressEvent = lambda e: _panel_mouse_press(window, e)
    panel.mouseMoveEvent = lambda e: _panel_mouse_move(window, e)
    panel.mouseReleaseEvent = lambda e: _panel_mouse_release(window, e)

    window._pw_panel = panel
    window._pw_widgets = {
        "title": title,
        "toggle": toggle_btn,
        "list": lst,
        "save": save_btn,
        "warn": warn_lbl,
    }
    window._pw_installed = True

    print(f"[DBG] pw panel built, size={panel.size()}")

    _relayout(window)


def _relayout(window):
    panel = getattr(window, "_pw_panel", None)
    if panel is None:
        return

    if window._pw_expanded:
        h = PANEL_H_EXPANDED
    else:
        h = PANEL_H_COLLAPSED
    panel.setFixedSize(PANEL_W, h)

    if window._pw_panel_x is None:
        x = window.width() - PANEL_W - SIDE_MARGIN
    else:
        x = window._pw_panel_x
        max_x = max(0, window.width() - PANEL_W)
        x = max(0, min(max_x, x))
        window._pw_panel_x = x

    y = TOP_MARGIN
    panel.move(int(x), int(y))
    panel.raise_()


# ======================================================================
# 形态切换 / 显隐
# ======================================================================
def _toggle_expand(window):
    window._pw_expanded = not window._pw_expanded
    _apply_expand(window)
    _relayout(window)


def _apply_expand(window):
    w = getattr(window, "_pw_widgets", None)
    if w is None:
        return
    show = window._pw_expanded
    w["list"].setVisible(show)
    w["save"].setVisible(show)
    if "warn" in w:
        w["warn"].setVisible(show)
    w["toggle"].setText("⌃" if show else "⌄")


def _show_panel(window):
    panel = getattr(window, "_pw_panel", None)
    if panel is None:
        return
    _apply_expand(window)
    _relayout(window)
    panel.show()
    panel.raise_()
    window._pw_visible = True
    print(f"[DBG] _show_panel visible={panel.isVisible()} "
          f"geo={panel.geometry()} parent={panel.parent()}")


def _hide_panel(window):
    panel = getattr(window, "_pw_panel", None)
    if panel is None:
        return
    panel.hide()
    window._pw_visible = False


# ======================================================================
# 列表
# ======================================================================
def _current_host(window):
    url = getattr(window, "_current_url", "") or ""
    if not url:
        try:
            wv = window.web_view
            if wv is not None:
                url = str(wv.url() or "")
        except Exception:
            url = ""
    return _host_of_url(url)


def _reload_list(window):
    w = getattr(window, "_pw_widgets", None)
    if w is None:
        return
    lst = w["list"]
    lst.clear()

    host = _current_host(window)
    if not host:
        return

    store = _load_store()
    items = store.get(host, [])
    if not isinstance(items, list):
        return

    for i, rec in enumerate(items):
        user = rec.get("username", "") or t("password.no_username")
        item = QListWidgetItem(user)
        item.setData(Qt.ItemDataRole.UserRole, i)
        lst.addItem(item)


def _on_item_clicked(window, item):
    if item is None:
        return
    idx = item.data(Qt.ItemDataRole.UserRole)
    if idx is None:
        return

    host = _current_host(window)
    if not host:
        return

    store = _load_store()
    items = store.get(host, [])
    if not isinstance(items, list):
        return
    if idx < 0 or idx >= len(items):
        return

    rec = items[idx]
    user = rec.get("username", "")
    pw = rec.get("password", "")
    if not pw:
        return

    _fill_to_page(window, user, pw)


def _on_save_clicked(window):
    user = getattr(window, "_pw_cur_user", "") or ""
    pw = getattr(window, "_pw_cur_pw", "") or ""
    if not pw:
        return

    host = _current_host(window)
    if not host:
        return

    store = _load_store()
    items = store.get(host, [])
    if not isinstance(items, list):
        items = []

    for it in items:
        if (it.get("username") == user
                and it.get("password") == pw):
            return

    items.insert(0, {"username": user, "password": pw})
    store[host] = items
    _save_store(store)
    _reload_list(window)


# ======================================================================
# 填充
# ======================================================================
def _fill_to_page(window, user, pw):
    wv = getattr(window, "web_view", None)
    if wv is None:
        return

    try:
        wv.eval_js(
            "(function(){"
            "  if (window.__pw_clear_all) return window.__pw_clear_all();"
            "  return 'no_clear_fn';"
            "})()",
            lambda r: None,
        )
    except Exception:
        pass

    def _do_fill():
        payload = json.dumps(
            {"user": user, "pw": pw}, ensure_ascii=False)
        js = f"""
        (function() {{
            var data = {payload};
            if (window.__pw_fill) {{
                return window.__pw_fill(data.user, data.pw);
            }}
            return "no_fill_fn";
        }})()
        """
        try:
            wv.eval_js(js, lambda r: None)
        except Exception:
            pass

    QTimer.singleShot(50, _do_fill)


# ======================================================================
# 拖动（沿上边缘平移）
# ======================================================================
def _panel_mouse_press(window, event):
    if event.button() != Qt.MouseButton.LeftButton:
        return
    window._pw_drag_offset = (
        event.globalPosition().toPoint().x()
        - window._pw_panel.mapToGlobal(QPoint(0, 0)).x()
    )


def _panel_mouse_move(window, event):
    if window._pw_drag_offset is None:
        return
    if not (event.buttons() & Qt.MouseButton.LeftButton):
        return

    panel = window._pw_panel
    global_x = event.globalPosition().toPoint().x()
    new_global_x = global_x - window._pw_drag_offset
    local_x = new_global_x - window.mapToGlobal(QPoint(0, 0)).x()

    max_x = max(0, window.width() - PANEL_W)
    local_x = max(0, min(max_x, local_x))
    window._pw_panel_x = local_x
    panel.move(int(local_x), TOP_MARGIN)


def _panel_mouse_release(window, event):
    window._pw_drag_offset = None


# ======================================================================
# 消息处理
# ======================================================================
def on_js_message(window, data):
    if not isinstance(data, dict):
        return False

    if data.get("type") != "pw_state":
        return False

    if getattr(window, "_pw_panel", None) is None:
        return True

    has_pw = bool(data.get("has_pw", False))
    user = data.get("username", "") or ""
    pw = data.get("password", "") or ""

    prev = getattr(window, "_pw_has_pw", False)
    window._pw_has_pw = has_pw

    window._pw_cur_user = user
    window._pw_cur_pw = pw

    # ---- 有密码框：取消待收回，按需显示 ----
    if has_pw:
        _cancel_hide(window)
        if not prev:
            _reload_list(window)
            _show_panel(window)
        else:
            _reload_list(window)
        return True

    # ---- 没有密码框：延迟 1.5 秒再收 ----
    if prev and not has_pw:
        _schedule_hide(window)
        return True

    return True


def _cancel_hide(window):
    t = getattr(window, "_pw_hide_timer", None)
    if t is not None:
        try:
            t.stop()
        except Exception:
            pass
        window._pw_hide_timer = None


def _schedule_hide(window):
    _cancel_hide(window)
    t = QTimer(window)
    t.setSingleShot(True)
    t.setInterval(1500)
    t.timeout.connect(lambda: _do_hide(window))
    t.start()
    window._pw_hide_timer = t


def _do_hide(window):
    window._pw_hide_timer = None
    if getattr(window, "_pw_has_pw", False):
        return
    _hide_panel(window)


# ======================================================================
# 供设置窗口调用的管理接口
# ======================================================================
def list_all():
    """返回全部账密：{host: [{"username", "password"}, ...]}"""
    return _load_store()


def delete_credential(host, index):
    """删 host 下第 index 条。成功返回 True。"""
    if not host:
        return False
    data = _load_store()
    items = data.get(host)
    if not isinstance(items, list):
        return False
    if index < 0 or index >= len(items):
        return False
    items.pop(index)
    if items:
        data[host] = items
    else:
        data.pop(host, None)
    _save_store(data)
    return True


def delete_host(host):
    """删 host 的全部账密。成功返回 True。"""
    if not host:
        return False
    data = _load_store()
    if host in data:
        data.pop(host)
        _save_store(data)
        return True
    return False