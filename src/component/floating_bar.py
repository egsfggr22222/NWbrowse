# -*- coding: utf-8 -*-
"""悬浮长条：双窗口一起显隐 + 网址转交 + 起窗口。

bar 只做：
  * 起窗口（QProcess）
  * 收到窗口的 request_url，查 host 对应窗口：
      - 有（含主域匹配）→ 转告它，置顶、加载。
      - 没有 → 起新窗口 assign 给它。
  * 起完新窗口后，通知来源窗口拽回原 URL。
  * 起完新窗口后，让新窗口置顶前台。
  * 窗口自带内核，bar 不再通知托盘起/停内核。

Windows Job Object：bar 一死（正常退出 / 崩溃 / 被强杀），
所有 window 子进程被系统强制杀掉。

注意：bar 的颜色不跟随个性化，固定 BODY_COLOR。
"""

import ctypes
from ctypes import wintypes
import sys
import os
import json
from urllib.parse import urlparse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths
from i18n import t
from ipc import (
    IpcServer, IpcClient,
    CHANNEL_BAR, ROLE_BAR,
    MSG_SHOW, MSG_HIDE, MSG_QUIT,
    MSG_NAVIGATE,
    MSG_REVERT_TO_LAST_URL,
    MSG_PIN_RELOAD,
    MSG_PIN_STATE,
    MSG_PIN_TOGGLE_FROM_BAR,
    MSG_PIN_DATA,
    MSG_PIN_REQUEST,
    MSG_LANGUAGE_CHANGED,
    window_role,
    find_windows,
    alloc_window_id,
    cleanup_registry,
    _read_registry, ROLE_WINDOW_PREFIX,
)

import pinned_store
from window_icon import make_domain_icon


DECOY_TITLE = "__frost_layer_test__"


# ======================================================================
# Windows Job Object
# ======================================================================
class _JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", ctypes.c_uint32),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", ctypes.c_uint32),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", ctypes.c_uint32),
        ("SchedulingClass", ctypes.c_uint32),
    ]


class _IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_uint64),
        ("WriteOperationCount", ctypes.c_uint64),
        ("OtherOperationCount", ctypes.c_uint64),
        ("ReadTransferCount", ctypes.c_uint64),
        ("WriteTransferCount", ctypes.c_uint64),
        ("OtherTransferCount", ctypes.c_uint64),
    ]


class _JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation",
         _JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", _IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


_JobObjectExtendedLimitInformation = 9
_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
_PROCESS_SET_QUOTA = 0x0100
_PROCESS_TERMINATE = 0x0001


def create_kill_on_close_job():
    try:
        kernel32 = ctypes.windll.kernel32

        job = kernel32.CreateJobObjectW(None, None)
        if not job:
            print("[bar] CreateJobObject 失败")
            return None

        info = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        info.BasicLimitInformation.LimitFlags = \
            _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE

        ok = kernel32.SetInformationJobObject(
            job,
            _JobObjectExtendedLimitInformation,
            ctypes.byref(info),
            ctypes.sizeof(info),
        )
        if not ok:
            print("[bar] SetInformationJobObject 失败")
            kernel32.CloseHandle(job)
            return None

        return job
    except Exception as e:
        print("[bar] 创建 Job Object 异常:", e)
        return None


def assign_pid_to_job(job, pid):
    if not job or not pid:
        return False
    try:
        kernel32 = ctypes.windll.kernel32

        hproc = kernel32.OpenProcess(
            _PROCESS_SET_QUOTA | _PROCESS_TERMINATE,
            False,
            int(pid),
        )
        if not hproc:
            print(f"[bar] OpenProcess({pid}) 失败")
            return False

        try:
            ok = kernel32.AssignProcessToJobObject(job, hproc)
            if not ok:
                print(f"[bar] AssignProcessToJobObject({pid}) 失败")
                return False
            return True
        finally:
            kernel32.CloseHandle(hproc)
    except Exception as e:
        print(f"[bar] 分配 PID {pid} 到 Job 异常:", e)
        return False


# ======================================================================
# host 判断
# ======================================================================
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


def _hosts_related(a, b):
    if not a or not b:
        return False
    if a == b:
        return True
    if a.endswith("." + b):
        return True
    if b.endswith("." + a):
        return True
    ra = _root_host(a)
    rb = _root_host(b)
    if ra and ra == rb:
        return True
    return False


def _pid_alive(pid):
    """检查 pid 对应进程是否存活。"""
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


def _find_window_by_host_related(host):
    if not host:
        return None, None
    data = _read_registry()
    for role, entry in data.items():
        if not role.startswith(ROLE_WINDOW_PREFIX):
            continue
        # 跳过死进程
        if not _pid_alive(entry.get("pid")):
            continue
        hosts = entry.get("hosts")
        if isinstance(hosts, list):
            for h in hosts:
                if _hosts_related(host, h):
                    return role, entry
        h = entry.get("host", "")
        if _hosts_related(host, h):
            return role, entry
    return None, None


# ======================================================================
# Windows 模糊 / 置顶
# ======================================================================
class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_int),
        ("AccentFlags", ctypes.c_int),
        ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_int),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.POINTER(ACCENT_POLICY)),
        ("SizeOfData", ctypes.c_size_t),
    ]


ACCENT_ENABLE_BLURBEHIND = 3
ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
WCA_ACCENT_POLICY = 19

HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010


def enable_blur(hwnd, color=0x00000000, state=ACCENT_ENABLE_BLURBEHIND):
    accent = ACCENT_POLICY()
    accent.AccentState = state
    accent.AccentFlags = 0
    accent.GradientColor = color
    accent.AnimationId = 0

    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = WCA_ACCENT_POLICY
    data.Data = ctypes.pointer(accent)
    data.SizeOfData = ctypes.sizeof(accent)

    ctypes.windll.user32.SetWindowCompositionAttribute(
        wintypes.HWND(hwnd), ctypes.byref(data)
    )


def set_topmost(hwnd, on=True):
    ctypes.windll.user32.SetWindowPos(
        wintypes.HWND(hwnd),
        HWND_TOPMOST if on else HWND_NOTOPMOST,
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
    )


def insert_after(hwnd, after_hwnd):
    ctypes.windll.user32.SetWindowPos(
        wintypes.HWND(hwnd),
        wintypes.HWND(after_hwnd),
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
    )


# ======================================================================
# 任务栏卡片显隐（ITaskbarList）
# ======================================================================
import comtypes
import comtypes.client
from comtypes import GUID, COMMETHOD, HRESULT, IUnknown


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
            print("[bar] ITaskbarList 初始化成功")
        except Exception as e:
            print("[bar] ITaskbarList 初始化失败:", repr(e))

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


# ======================================================================
# 前台窗口变化监听
# ======================================================================
EVENT_SYSTEM_FOREGROUND = 0x0003
WINEVENT_OUTOFCONTEXT = 0x0000
WINEVENT_SKIPOWNPROCESS = 0x0002

WinEventProc = ctypes.WINFUNCTYPE(
    None,
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.HWND,
    wintypes.LONG,
    wintypes.LONG,
    wintypes.DWORD,
    wintypes.DWORD,
)


class ForegroundHook:
    def __init__(self):
        self._callback_ref = None
        self._hook = None
        self._changed = False

    def install(self):
        def _proc(hWinEventHook, event, hwnd, idObject, idChild,
                  idEventThread, dwmsEventTime):
            if event == EVENT_SYSTEM_FOREGROUND:
                self._changed = True

        self._callback_ref = WinEventProc(_proc)
        self._hook = ctypes.windll.user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_FOREGROUND,
            0,
            self._callback_ref,
            0, 0,
            WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS,
        )

    def uninstall(self):
        try:
            if self._hook:
                ctypes.windll.user32.UnhookWinEvent(self._hook)
        except Exception:
            pass
        self._hook = None
        self._callback_ref = None

    def take_changed(self):
        changed = self._changed
        self._changed = False
        return changed


# ======================================================================
# 模糊窗口
# ======================================================================
class FrostWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DECOY_TITLE)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(48, 300)

    def showEvent(self, event):
        super().showEvent(event)
        enable_blur(int(self.winId()), 0x00000000, ACCENT_ENABLE_BLURBEHIND)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))


# ======================================================================
# 图标按钮
# ======================================================================
class IconButton(QPushButton):
    STYLE_WINDOW = "window"
    STYLE_CHEVRON = "chevron"

    double_clicked = pyqtSignal()
    context_menu_requested = pyqtSignal()

    def __init__(self, icon_style, parent=None):
        super().__init__(parent)
        self.icon_style = icon_style
        self._hover = False
        self._pressed = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("background: transparent; border: none;")

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._pressed = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        self.context_menu_requested.emit()
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx = w / 2
        cy = h / 2

        if self._pressed:
            color = QColor(235, 235, 235, 230)
        elif self._hover:
            color = QColor(245, 245, 245, 200)
        else:
            color = QColor(210, 210, 210, 150)

        pen = QPen(color)
        pen.setWidthF(1.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        if self.icon_style == self.STYLE_WINDOW:
            rw = min(w, h) * 0.72
            rh = rw * 0.86
            x = cx - rw / 2
            y = cy - rh / 2
            radius = rw * 0.18
            painter.drawRoundedRect(QRectF(x, y, rw, rh), radius, radius)

            bar_y = y + rh * 0.30
            painter.drawLine(QPointF(x, bar_y), QPointF(x + rw, bar_y))

            dot_r = rw * 0.07
            dot_gap = rw * 0.17
            dot_cy = y + rh * 0.15
            dot_x0 = x + rw * 0.22
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            for i in range(3):
                painter.drawEllipse(
                    QPointF(dot_x0 + i * dot_gap, dot_cy), dot_r, dot_r
                )

        elif self.icon_style == self.STYLE_CHEVRON:
            size = min(w, h) * 0.22
            v_pen = QPen(color)
            v_pen.setWidthF(1.4)
            v_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            v_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(v_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            path = QPainterPath()
            path.moveTo(cx - size, cy - size * 0.25)
            path.quadTo(cx, cy + size * 0.75, cx + size, cy - size * 0.25)
            painter.drawPath(path)


# ======================================================================
# 固定图标按钮
# ======================================================================
class PinIconButton(QPushButton):
    """滚轮区里单个固定图标。悬停变暗，开启变亮（三态亮度）。"""

    ICON_SIZE = 22

    clicked_pin = pyqtSignal(str)
    right_clicked_pin = pyqtSignal(str)

    def __init__(self, host, pixmap, parent=None):
        super().__init__(parent)
        self.host = host
        self._pm = pixmap
        self._hover = False
        self._running = False

        self.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def set_running(self, on):
        on = bool(on)
        if on != self._running:
            self._running = on
            self.update()

    def set_pixmap(self, pm):
        self._pm = pm
        self.update()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.right_clicked_pin.emit(self.host)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.rect().contains(event.position().toPoint()):
                self.clicked_pin.emit(self.host)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if self._pm is None or self._pm.isNull():
            return

        # 高分屏：按物理像素渲染，避免拉伸模糊
        dpr = self.devicePixelRatioF()
        logical_size = self.ICON_SIZE
        px_size = max(1, int(logical_size * dpr))

        pm = self._pm.scaled(
            px_size, px_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        pm.setDevicePixelRatio(dpr)

        # 用逻辑坐标居中
        w_logical = pm.width() / dpr
        h_logical = pm.height() / dpr
        x = (self.width() - w_logical) / 2.0
        y = (self.height() - h_logical) / 2.0

        # 裁成圆角矩形
        radius = logical_size * 0.28
        rect = QRectF(
            (self.width() - logical_size) / 2.0,
            (self.height() - logical_size) / 2.0,
            float(logical_size),
            float(logical_size),
        )

        clip_path = QPainterPath()
        clip_path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(clip_path)

        # 悬停 → 变暗；其他 → 正常
        if self._hover:
            painter.setOpacity(0.6)
        else:
            painter.setOpacity(1.0)

        painter.drawPixmap(QPointF(x, y), pm)
        painter.setOpacity(1.0)

        # 打开状态 → 右上角绿色小点
        painter.setClipping(False)
        if self._running:
            dot_r = 3.5
            dot_cx = self.width() - dot_r - 1
            dot_cy = dot_r + 1
            painter.setBrush(QColor(60, 200, 90))
            painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
            painter.drawEllipse(QPointF(dot_cx, dot_cy), dot_r, dot_r)


# ======================================================================
# 滚轮容器：放固定图标，可滚动
# ======================================================================
class PinScrollArea(QScrollArea):
    """透明滚轮区。只显示图标，可上下滚。"""

    EDGE_HOT = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        self.viewport().setStyleSheet("background: transparent;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._host = QWidget()
        self._host.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._host)
        self._layout.setContentsMargins(0, 4, 0, 4)
        self._layout.setSpacing(18)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._layout.addStretch(1)
        self.setWidget(self._host)

        self.viewport().setContentsMargins(0, 0, 0, 0)

        self._buttons = []
        self._pending_scroll = None      # 待恢复的滚动位置

        # 滚动范围变化时，如果有待恢复位置，恢复它
        self.verticalScrollBar().rangeChanged.connect(
            self._on_range_changed
        )

    def clear_icons(self):
        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.hide()
                w.setParent(None)
                w.deleteLater()
        self._layout.addStretch(1)
        self._buttons = []
        self._host.update()
        self.viewport().update()

    def _on_range_changed(self, min_val, max_val):
        """layout 排完、滚动范围确定后，恢复滚动位置。"""
        print(f"[pin-scroll] rangeChanged {min_val}-{max_val} "
              f"pending={self._pending_scroll}")
        if self._pending_scroll is None:
            return
        # range 不够大（刚清空时），先不恢复
        if max_val < self._pending_scroll:
            return
        try:
            self.verticalScrollBar().setValue(self._pending_scroll)
        except Exception:
            pass
        self._pending_scroll = None


    def set_icons(self, items):
        # 记当前滚动位置
        try:
            self._pending_scroll = self.verticalScrollBar().value()
        except Exception:
            self._pending_scroll = 0

        print(f"[pin-scroll] set_icons old_value={self._pending_scroll}")

        self.clear_icons()
        for it in items:
            btn = PinIconButton(it["host"], it.get("pixmap"), self._host)
            btn.set_running(it.get("running", False))
            idx = self._layout.count() - 1
            self._layout.insertWidget(idx, btn)
            self._buttons.append(btn)

        # 强制 layout 更新，触发 rangeChanged
        try:
            self._layout.activate()
            self._host.adjustSize()
        except Exception:
            pass

    def buttons(self):
        return list(self._buttons)


# ======================================================================
# 悬浮长条
# ======================================================================
class FloatingBar(QWidget):

    SHADOW_MARGIN = 12
    BAR_W = 40
    BAR_H = 260
    RADIUS = 10

    BODY_COLOR = QColor(0, 0, 0, 140)
    BODY_BORDER = QColor(120, 120, 120, 120)

    POLL_MS = 80
    JITTER_MS = 30
    JITTER_PX = 1
    FROST_PAD = 2
    RESUME_DELAY_MS = 120

    collapse_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(
            self.BAR_W + self.SHADOW_MARGIN * 2,
            self.BAR_H + self.SHADOW_MARGIN * 2,
        )

        self._drag_start = None
        self._jitter_on = False
        self._moving = False

        self._win_procs = {}
        self._win_hosts = {}

        # ---- 固定项 ----
        self._pin_scroll = None
        self._pin_buttons = {}
        self._pin_items = {}
        self._pin_dot_timer = QTimer(self)
        self._pin_dot_timer.setInterval(1500)
        self._pin_dot_timer.timeout.connect(self._refresh_pin_dots)
        self._taskbar = TaskbarHelper()
        # ------------------

        self._job = create_kill_on_close_job()
        if self._job:
            print(f"[bar] Job Object 已创建 h={self._job}")
        else:
            print("[bar] Job Object 创建失败，将退回普通 QProcess 模式")

        self._frost = FrostWindow()
        self._frost.show()

        self._build_ui()
        self._center_right()
        self._sync_frost()
        self._place_frost()

        self._hook = ForegroundHook()
        self._hook.install()

        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(self.POLL_MS)
        self._poll_timer.timeout.connect(self._poll_foreground)
        self._poll_timer.start()

        self._jitter_timer = QTimer(self)
        self._jitter_timer.setInterval(self.JITTER_MS)
        self._jitter_timer.timeout.connect(self._jitter_frost)
        self._jitter_timer.start()

        self.collapse_btn.double_clicked.connect(self.collapse_requested.emit)
        self.wake_btn.clicked.connect(self.open_default_window)
        self.wake_btn.context_menu_requested.connect(self._show_wake_menu)

        # ---- 固定项 ----
        # 启动先清一次残留 window 注册表，保证这次启动是干净态
        self._clear_all_window_registry()
        self._pin_dot_timer.start()
        QTimer.singleShot(100, self.reload_pinned)
        # ------------------

        # ---- 注册表看门狗：定时清死进程 ----
        try:
            from ipc import RegistryWatchdog
            self._watchdog = RegistryWatchdog(
                interval_ms=3000, parent=self
            )
            self._watchdog.start()
        except Exception as e:
            print("[bar] 启动 RegistryWatchdog 失败:", e)

    # ---------------- UI ----------------
    def _build_ui(self):
        self._body = QWidget(self)
        self._body.setGeometry(
            self.SHADOW_MARGIN, self.SHADOW_MARGIN,
            self.BAR_W, self.BAR_H,
        )
        self._body.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._body.setStyleSheet("background: transparent;")

        shadow = QGraphicsDropShadowEffect(self._body)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 120))
        self._body.setGraphicsEffect(shadow)

        pad = 6
        btn_h = 34
        btn_w = self.BAR_W - pad * 2
        line_w = self.BAR_W - pad * 2

        self.wake_btn = IconButton(IconButton.STYLE_WINDOW, self._body)
        self.wake_btn.setGeometry(pad, 1, btn_w, btn_h)

        self.top_line = QFrame(self._body)
        self.top_line.setGeometry(pad, btn_h, line_w, 1)
        self.top_line.setStyleSheet("background: rgba(180, 180, 180, 90);")

        bottom_pad = 0
        self.collapse_btn = IconButton(IconButton.STYLE_CHEVRON, self._body)
        self.collapse_btn.setGeometry(
            pad, self.BAR_H - bottom_pad - btn_h + 6, btn_w, btn_h
        )

        line_gap = 0
        self.bottom_line = QFrame(self._body)
        self.bottom_line.setGeometry(
            pad,
            self.BAR_H - bottom_pad - btn_h - line_gap + 12,
            line_w, 1,
        )
        self.bottom_line.setStyleSheet("background: rgba(180, 180, 180, 90);")

        # ---- 中间滚轮区 ----
        self._pin_scroll = PinScrollArea(self._body)
        self._pin_scroll.setGeometry(
            0,
            btn_h + 2,
            self.BAR_W,
            self.bottom_line.y() - btn_h - 2,
        )
        self._pin_scroll.raise_()
        self._pin_scroll.installEventFilter(self)
        self._pin_scroll.viewport().installEventFilter(self)
        # --------------------

    # ---------------- 固定项 ----------------
    def reload_pinned(self):
        """从磁盘重读固定项，刷新滚轮区。"""
        try:
            items, broken = pinned_store.load_all()

            if broken:
                self._handle_broken(broken)
                items, broken = pinned_store.load_all()

            pin_list = []
            self._pin_items = {}
            for it in items:
                host = it["host"]
                self._pin_items[host] = it

                pm = pinned_store.load_icon(host)
                if pm is None or pm.isNull():
                    # 生成字母图标：用高分屏尺寸
                    try:
                        dpr = self.devicePixelRatioF()
                    except Exception:
                        dpr = 1.0
                    px = max(64, int(64 * dpr))
                    pm = make_domain_icon(host).pixmap(px, px)

                pin_list.append({
                    "host": host,
                    "pixmap": pm,
                    "running": self._is_host_window_open(host),
                })

            self._pin_buttons = {}
            self._pin_scroll.set_icons(pin_list)

            for btn in self._pin_scroll.buttons():
                btn.clicked_pin.connect(self._on_pin_clicked)
                btn.right_clicked_pin.connect(self._on_pin_right_clicked)
                self._pin_buttons[btn.host] = btn
        except Exception as e:
            import traceback
            print("[bar] reload_pinned 异常:", e)
            traceback.print_exc()

    def _handle_broken(self, broken):
        """损坏固定项：静默删除（不阻塞）。"""
        for host in list(broken):
            try:
                pinned_store.remove(host)
                print(f"[bar] 已删除损坏固定项 {host}")
            except Exception:
                pass

    def _is_host_window_open(self, host):
        """该 host 对应的窗口进程是否存在。"""
        try:
            role, entry = _find_window_by_host_related(host)
            if not role:
                return False
            return _pid_alive(entry.get("pid"))
        except Exception:
            return False

    def _refresh_pin_dots(self):
        """定时刷新每个图标的运行状态。"""
        for host, btn in list(self._pin_buttons.items()):
            try:
                btn.set_running(self._is_host_window_open(host))
            except RuntimeError:
                self._pin_buttons.pop(host, None)
            except Exception:
                pass

    def _on_pin_clicked(self, host):
        """点图标：有窗口 → 置顶；无 → 起 df-N 带记忆。"""
        if not host:
            return

        role, entry = _find_window_by_host_related(host)
        if role and _pid_alive(entry.get("pid")):
            target_id = role.split(":", 1)[1]
            self._show_existing(target_id, retries=15)
            return

        self._open_pinned_window(host)

    def _open_pinned_window(self, host):
        """打开固定窗口：起 df-N，带 host + 记忆。"""
        item = self._pin_items.get(host)
        urls = item.get("popup_urls", []) if item else []
        last_index = item.get("last_index", -1) if item else -1

        url = ""
        if urls:
            if 0 <= last_index < len(urls):
                url = urls[last_index]
            else:
                url = urls[-1]

        wid = self._alloc_default_id()
        self._start_window(
            window_id=wid,
            host=host,
            url="",
            pinned_url=url,
        )
        QTimer.singleShot(600, lambda w=wid: self._show_existing(w, retries=15))

    def _on_pin_right_clicked(self, host):
        """右键图标：取消固定。"""
        if not host:
            return
        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)
        act = menu.addAction(t("menu.unpin"))
        act.triggered.connect(lambda: self._unpin(host))
        menu.exec(QCursor.pos())

    def _unpin(self, host):
        """删记录 + 通知 window 关开关。"""
        if not host:
            return
        pinned_store.remove(host)
        self.reload_pinned()

        try:
            role, _entry = _find_window_by_host_related(host)
            if role:
                target_id = role.split(":", 1)[1]
                payload = json.dumps({"host": host}, ensure_ascii=False)
                IpcClient.send_to_role(
                    window_role(target_id),
                    MSG_PIN_TOGGLE_FROM_BAR,
                    payload.encode("utf-8"),
                )
        except Exception as e:
            print("[bar] 通知 window 关开关失败:", e)

    def _pin_state_from_window(self, data):
        """window 上报固定开关状态。"""
        host = data.get("host", "")
        on = bool(data.get("on", False))
        if not host:
            return

        if on:
            if not pinned_store.is_pinned(host) and pinned_store.count() >= pinned_store.MAX_PINNED:
                try:
                    role, _entry = _find_window_by_host_related(host)
                    if role:
                        target_id = role.split(":", 1)[1]
                        IpcClient.send_to_role(
                            window_role(target_id),
                            MSG_PIN_TOGGLE_FROM_BAR,
                            json.dumps(
                                {"host": host, "reason": "full"},
                                ensure_ascii=False,
                            ).encode("utf-8"),
                        )
                except Exception:
                    pass
                return

            pinned_store.add(
                host,
                hosts=data.get("hosts", [host]),
                popup_urls=data.get("popup_urls", []),
                last_index=data.get("last_index", -1),
                complete_notify=data.get("complete_notify", False),
            )
        else:
            pinned_store.remove(host)

        self.reload_pinned()

    # ---------------- 窗口进程 ----------------
    def _active_window_ids(self):
        """当前真正占用的窗口 id 集合。

        注意：**必须过滤掉已死的窗口进程**。
        IPC 注册表里的条目在窗口崩溃/被杀掉时不一定会被及时清掉，
        如果把死条目也算作"占用"，`alloc_window_id` 就会一直往后编号
        （df-1、df-2、df-3…），而 WebView2 的 profile 是**按窗口 id 分目录**的
        （settings_backend.get_user_data_folder），于是每开一个新窗口
        都是一份全新的空 profile —— 表现为"Cookie 不保存、每次都要重新登录"。
        """
        active = set()
        try:
            for role, entry in find_windows().items():
                if not role.startswith("window:"):
                    continue
                wid = role.split(":", 1)[1]
                if not wid:
                    continue
                if _pid_alive(entry.get("pid")):
                    active.add(wid)
        except Exception:
            pass

        # bar 自己持有的 QProcess：只算还在跑的
        for wid, proc in self._win_procs.items():
            try:
                if proc is not None and proc.state() != QProcess.ProcessState.NotRunning:
                    active.add(wid)
            except Exception:
                active.add(wid)

        # 顺手把注册表里的死条目清掉，别让它们越积越多
        try:
            cleanup_registry()
        except Exception:
            pass

        return active

    def _alloc_default_id(self):
        return alloc_window_id("df", self._active_window_ids())

    def open_default_window(self):
        wid = self._alloc_default_id()
        self._start_window(window_id=wid, host="", url="")

    def _show_wake_menu(self):
        """右键 wake_btn：弹无痕选项。"""
        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)
        act = menu.addAction(t("menu.incognito"))
        act.triggered.connect(self.open_incognito_window)
        menu.exec(self.wake_btn.mapToGlobal(
            self.wake_btn.rect().bottomLeft()))

    def open_incognito_window(self):
        """开一个无痕窗口。"""
        wid = self._alloc_default_id()
        self._start_window(window_id=wid, host="", url="", incognito=True)

    def _start_window(self, window_id, host="", url="", incognito=False,
                      pinned_url=""):
        role = "incognito" if incognito else "window"

        args = ["--id", window_id]
        if host:
            args += ["--host", host]
        if pinned_url:
            args += ["--pinned-url", pinned_url]

        prog, argv = apppaths.role_command(role, *args)
        print(f"[DBG] _start_window role={role} prog={prog} args={argv}")

        proc = QProcess()
        proc.setProgram(prog)
        proc.setArguments(argv)
        apppaths.configure_child_proc(proc)
        self._win_procs[window_id] = proc
        if host:
            self._win_hosts[window_id] = host

        proc.finished.connect(
            lambda *_args, w=window_id: self._on_window_finished(w)
        )
        proc.start()
        print(f"[bar] 起窗口 {window_id} host={host!r} url={url!r} "
              f"incognito={incognito}")

        if self._job:
            proc.waitForStarted(3000)
            pid = proc.processId()
            if pid:
                ok = assign_pid_to_job(self._job, pid)
                print(f"[bar] window {window_id} pid={pid} "
                      f"加入 Job ok={ok}")
            else:
                print(f"[bar] window {window_id} 拿不到 PID")

        if url:
            QTimer.singleShot(0, lambda: self._assign_url(window_id, url))

        QTimer.singleShot(1500, lambda: self._show_existing(window_id))

    def _on_window_finished(self, window_id):
        proc = self._win_procs.pop(window_id, None)
        if proc is not None:
            try:
                proc.deleteLater()
            except Exception:
                pass

        host = self._win_hosts.pop(window_id, "")
        print(f"[bar] 窗口已结束 {window_id} host={host}")

    # ---------------- 网址转交 ----------------
    def _assign_url(self, window_id, url, retries=40):
        try:
            payload = json.dumps({"url": url}, ensure_ascii=False)
            ok = IpcClient.send_to_role(
                window_role(window_id),
                MSG_NAVIGATE,
                payload,
            )
            if ok:
                print(f"[bar] assign {window_id} url={url!r}")
                return
        except Exception as e:
            print("[bar] assign 异常:", e)

        if retries > 0:
            QTimer.singleShot(
                200,
                lambda: self._assign_url(window_id, url, retries - 1),
            )
        else:
            print(f"[bar] assign {window_id} 重试耗尽")

    def _navigate_existing(self, window_id, url):
        try:
            payload = json.dumps({"url": url}, ensure_ascii=False)
            IpcClient.send_to_role(
                window_role(window_id),
                MSG_NAVIGATE,
                payload,
            )
        except Exception as e:
            print("[bar] 发送 navigate 失败:", e)

    def _show_existing(self, window_id, retries=10):
        """让窗口前台。发 MSG_SHOW，窗口自己 raise + activate + set_topmost。"""
        try:
            ok = IpcClient.send_to_role(
                window_role(window_id),
                MSG_SHOW,
                b"",
            )
            if ok:
                QTimer.singleShot(
                    300,
                    lambda w=window_id: IpcClient.send_to_role(
                        window_role(w), MSG_SHOW, b"",
                    ),
                )
                return
        except Exception:
            pass

        if retries > 0:
            QTimer.singleShot(
                200,
                lambda: self._show_existing(window_id, retries - 1),
            )

    def _notify_revert(self, from_window_id):
        if not from_window_id:
            return
        try:
            IpcClient.send_to_role(
                window_role(from_window_id),
                MSG_REVERT_TO_LAST_URL,
                b"",
            )
            print(f"[bar] 已通知 {from_window_id} 拽回")
        except Exception as e:
            print(f"[bar] 通知 {from_window_id} 拽回失败: {e}")

    # ---------------- 网址转交核心 ----------------
    def handle_request_url(self, from_window_id, url, from_host=""):
        host = url_host(url)
        print(f"[DBG] bar.handle_request_url host={host} url={url[:80]!r}")
        if not host:
            self._navigate_existing(from_window_id, url)
            return

        # 1. 有同 host 窗口 → 转发给它
        role, entry = _find_window_by_host_related(host)
        print(f"[DBG] bar 步骤1：find role={role} "
              f"alive={_pid_alive(entry.get('pid')) if entry else False}")
        if role and entry and _pid_alive(entry.get("pid")):
            print("[DBG] bar 走分支 1：转发")
            target_id = role.split(":", 1)[1]
            self._navigate_existing(target_id, url)
            self._show_existing(target_id)
            return

        # 2. 没有，但该主域有固定 → 新建窗口（带固定内容）
        root = _root_host(host)
        print(f"[DBG] bar 步骤2：root={root} "
              f"is_pinned={pinned_store.is_pinned(root) if root else False}")
        if root and pinned_store.is_pinned(root):
            print("[DBG] bar 走分支 2：新建带固定窗口")
            item = self._pin_items.get(root)
            if not item:
                try:
                    item = pinned_store.load_one(root)
                except Exception:
                    item = None

            urls = item.get("popup_urls", []) if item else []
            last_index = item.get("last_index", -1) if item else -1
            pinned_url = ""
            if urls:
                if 0 <= last_index < len(urls):
                    pinned_url = urls[last_index]
                else:
                    pinned_url = urls[-1]

            wid = self._alloc_default_id()
            self._start_window(
                window_id=wid,
                host=root,
                url="",
                pinned_url=pinned_url,
            )
            self._notify_revert(from_window_id)

            QTimer.singleShot(
                1500,
                lambda u=url: self.handle_request_url("", u),
            )
            return

        # 3. 都没有 → 新建窗口，加载网址
        wid = self._alloc_default_id()
        self._start_window(window_id=wid, host=host, url=url)
        self._notify_revert(from_window_id)

    def on_window_message(self, msg_type, payload):
        if msg_type == MSG_NAVIGATE:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                return
            cmd = data.get("cmd")
            if cmd == "request_url":
                self.handle_request_url(
                    data.get("window_id", ""),
                    data.get("url", ""),
                    data.get("host", ""),
                )
            return

        if msg_type == MSG_PIN_RELOAD:
            self.reload_pinned()
            return

        if msg_type == MSG_PIN_STATE:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                return
            self._pin_state_from_window(data)
            return

    # ---------------- 几何 ----------------
    def _frost_geometry(self):
        cur_w = self.width()
        cur_h = self.height()

        base_w = self.BAR_W + self.SHADOW_MARGIN * 2
        base_h = self.BAR_H + self.SHADOW_MARGIN * 2
        scale_x = cur_w / base_w
        scale_y = cur_h / base_h

        pad = self.FROST_PAD
        m_x = int((self.SHADOW_MARGIN + 5 - pad) * scale_x)
        m_y = int((self.SHADOW_MARGIN + 5 - pad) * scale_y)
        w = int((self.BAR_W - 10 + pad * 2) * scale_x)
        h = int((self.BAR_H - 10 + pad * 2) * scale_y)

        top_left = self.mapToGlobal(QPoint(m_x, m_y))
        return top_left.x(), top_left.y(), w, h

    def _sync_frost(self):
        try:
            x, y, w, h = self._frost_geometry()
            self._frost.setGeometry(x, y, w, h)
        except Exception:
            pass

    def _place_frost(self):
        try:
            main_hwnd = int(self.winId())
            frost_hwnd = int(self._frost.winId())

            set_topmost(frost_hwnd, True)
            set_topmost(main_hwnd, True)
            insert_after(frost_hwnd, main_hwnd)
            enable_blur(frost_hwnd, 0x00000000, ACCENT_ENABLE_BLURBEHIND)
        except Exception:
            pass

    def _jitter_frost(self):
        if not self.isVisible():
            return
        if self._moving:
            return
        try:
            x, y, w, h = self._frost_geometry()
            offset = self.JITTER_PX if self._jitter_on else 0
            self._jitter_on = not self._jitter_on
            self._frost.setGeometry(x + offset, y, w, h)
        except Exception:
            pass

    def _resume_jitter(self):
        self._moving = False
        self._jitter_on = False

    def _poll_foreground(self):
        # 这是每 POLL_MS 跑一次的常驻定时器，里面要碰 win32 窗口句柄。
        # 一旦抛异常，Qt 会当成未处理异常直接把整个 bar 进程带走
        # （日志里只留下 exit_code=1），所以这里兜住并留痕。
        try:
            if not self.isVisible():
                return
            if self._hook.take_changed():
                self._sync_frost()
                self._place_frost()
        except Exception:
            import traceback
            print("[bar] _poll_foreground 异常:")
            traceback.print_exc()

    # ---------------- 显隐 ----------------
    def hide_bar(self):
        self.hide()
        try:
            self._frost.hide()
        except Exception:
            pass

    def show_bar(self):
        self.show()
        try:
            self._frost.show()
            enable_blur(int(self._frost.winId()), 0x00000000,
                        ACCENT_ENABLE_BLURBEHIND)
        except Exception:
            pass
        self._sync_frost()
        self._place_frost()

    # ---------------- 绘制 ----------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(
            self.SHADOW_MARGIN, self.SHADOW_MARGIN,
            self.BAR_W, self.BAR_H,
        )
        painter.setBrush(self.BODY_COLOR)
        painter.setPen(QPen(self.BODY_BORDER, 1))
        painter.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

    # ---------------- 位置 / 事件 ----------------
    def _center_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() + self.SHADOW_MARGIN - 20
        y = screen.top() + (screen.height() - self.height()) // 2
        self.move(x, y)

    def event(self, e):
        if e.type() in (
            QEvent.Type.WindowActivate,
            QEvent.Type.Show,
            QEvent.Type.WindowStateChange,
        ):
            QTimer.singleShot(0, self._place_frost)
        return super().event(e)

    def showEvent(self, event):
        super().showEvent(event)
        self._place_frost()

    def moveEvent(self, event):
        super().moveEvent(event)
        self._sync_frost()
        self._place_frost()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_frost()
        self._place_frost()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint() - self.pos()
            self._moving = True

    def mouseMoveEvent(self, event):
        if self._drag_start and (event.buttons() & Qt.MouseButton.LeftButton):
            self.move(event.globalPosition().toPoint() - self._drag_start)

    def mouseReleaseEvent(self, event):
        self._drag_start = None
        QTimer.singleShot(self.RESUME_DELAY_MS, self._resume_jitter)

    # ---------------- 滚轮区：滚 + 边缘拖 ----------------
    def wheelEvent(self, event):
        if self._pin_scroll is not None:
            try:
                self._pin_scroll.wheelEvent(event)
                return
            except Exception:
                pass
        super().wheelEvent(event)

    def eventFilter(self, obj, event):
        sc = self._pin_scroll
        if sc is None:
            return super().eventFilter(obj, event)

        if obj is sc or obj is sc.viewport():
            et = event.type()

            if et == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    pos = event.position().toPoint()
                    w = sc.width()
                    if pos.x() <= sc.EDGE_HOT or pos.x() >= w - sc.EDGE_HOT:
                        self._drag_start = (
                            event.globalPosition().toPoint() - self.pos()
                        )
                        self._moving = True
                        return True

            elif et == QEvent.Type.MouseMove:
                if (self._drag_start is not None
                        and (event.buttons() & Qt.MouseButton.LeftButton)):
                    self.move(
                        event.globalPosition().toPoint() - self._drag_start
                    )
                    return True

            elif et == QEvent.Type.MouseButtonRelease:
                if self._drag_start is not None:
                    self._drag_start = None
                    QTimer.singleShot(
                        self.RESUME_DELAY_MS, self._resume_jitter
                    )
                    return True

            elif et == QEvent.Type.Wheel:
                try:
                    sc.wheelEvent(event)
                except Exception:
                    pass
                return True

        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        # 1. 温柔关掉 bar 自己起的窗口进程（terminate → kill）
        self._kill_all_windows()

        # 2. 关 Job Object → 系统强杀残留子进程
        try:
            if self._job:
                ctypes.windll.kernel32.CloseHandle(self._job)
                self._job = None
                print("[bar] Job Object 已关闭，子进程将被系统回收")
        except Exception:
            pass

        # 3. 清空注册表里所有 window 条目
        self._clear_all_window_registry()

        # 4. 把固定项状态整体复位：没有任何窗口开着
        self._reset_all_pins_closed()

        # 5. 卸载 hook / 关 frost
        try:
            self._hook.uninstall()
        except Exception:
            pass
        try:
            self._frost.close()
        except Exception:
            pass
        super().closeEvent(event)

    def _clear_all_window_registry(self):
        """清掉注册表里所有 window:* 条目。"""
        try:
            from ipc import _write_registry
            data = _read_registry()
            removed = []
            for role in list(data.keys()):
                if role.startswith(ROLE_WINDOW_PREFIX):
                    del data[role]
                    removed.append(role)
            if removed:
                _write_registry(data)
                print(f"[bar] 已清理 {len(removed)} 个残留 window 条目")
        except Exception as e:
            print("[bar] 清理 window 注册表失败:", e)

    def _reset_all_pins_closed(self):
        """把每个固定项复位为『没有窗口打开』。"""
        try:
            for host, btn in list(self._pin_buttons.items()):
                try:
                    btn.set_running(False)
                except RuntimeError:
                    self._pin_buttons.pop(host, None)
                except Exception:
                    pass
        except Exception as e:
            print("[bar] 复位图标状态失败:", e)

        self._win_procs.clear()
        self._win_hosts.clear()

        try:
            if self._pin_dot_timer.isActive():
                self._pin_dot_timer.stop()
        except Exception:
            pass

        print("[bar] 所有固定项已复位为『未打开』")

    def _kill_all_windows(self):
        """关掉 bar 起的窗口进程。

        **先请它们优雅退出，再硬杀剩下的。**

        为什么不能直接杀：Windows 上 `QProcess.terminate()` 实际是
        `TerminateProcess`（硬杀），不是发 WM_CLOSE。窗口进程被瞬间干掉时，
        WebView2 还没来得及销毁自己，profile（Cookie / localStorage / 登录态）
        可能没落盘 —— 表现就是"关掉软件再打开，登录态丢了"。

        所以：先发 MSG_QUIT（window.py 收到后会 self.close()，走完整的
        closeEvent → WebView2 正常析构），给它一小段时间；还赖着不走的才强杀。

        时间预算压在 ~1.2 秒内：托盘的 quit() 只等 bar 2 秒，超时会把 bar 也杀了，
        而 bar 一死 Job Object（KILL_ON_JOB_CLOSE）就会立刻回收所有窗口。
        """
        procs = [(wid, p) for wid, p in self._win_procs.items() if p is not None]
        if not procs:
            self._win_procs.clear()
            return

        # 1) 逐个请求优雅退出
        for wid, _proc in procs:
            try:
                IpcClient.send_to_role(window_role(wid), MSG_QUIT, timeout_ms=200)
            except Exception as e:
                print(f"[bar] 请求窗口 {wid} 退出失败: {e}")

        # 2) 统一等待（总预算 1200ms，窗口多也不会拖太久）
        timer = QElapsedTimer()
        timer.start()
        for wid, proc in procs:
            try:
                if proc.state() == QProcess.ProcessState.NotRunning:
                    continue
                left = 1200 - int(timer.elapsed())
                if left > 0 and proc.waitForFinished(left):
                    print(f"[bar] 窗口 {wid} 已优雅退出")
            except Exception:
                pass

        # 3) 还没退的才强杀
        for wid, proc in procs:
            try:
                if proc.state() != QProcess.ProcessState.NotRunning:
                    print(f"[bar] 窗口 {wid} 未响应，强制结束")
                    proc.terminate()
                    if not proc.waitForFinished(1200):
                        proc.kill()
            except Exception:
                pass

        self._win_procs.clear()
        self._win_hosts.clear()


# ======================================================================
# 入口
# ======================================================================
def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 加载语言（必须在 FloatingBar 创建之前）
    try:
        from settings_backend import SettingsBackend
        from i18n import load as i18n_load
        i18n_load(SettingsBackend().get_language())
    except Exception as e:
        print("[bar] 加载语言失败:", e)

    bar = FloatingBar()

    def on_message(msg_type, payload):
        if msg_type == MSG_SHOW:
            bar.show_bar()
            bar.raise_()
            bar.activateWindow()
        elif msg_type == MSG_HIDE:
            bar.hide_bar()
        elif msg_type == MSG_QUIT:
            bar.close()
            app.quit()
        elif msg_type == MSG_NAVIGATE:
            bar.on_window_message(msg_type, payload)
        elif msg_type == MSG_PIN_RELOAD:
            bar.reload_pinned()
        elif msg_type == MSG_PIN_STATE:
            bar.on_window_message(msg_type, payload)
        elif msg_type == MSG_LANGUAGE_CHANGED:
            try:
                from i18n import load as i18n_load
                code = payload.decode("utf-8")
                i18n_load(code)
                print(f"[bar] 语言已切换到 {code}")
            except Exception as e:
                print("[bar] 切换语言失败:", e)

    server = IpcServer(CHANNEL_BAR, on_message, role=ROLE_BAR)
    if not server.start():
        print("[bar] 已有实例在运行，退出")
        sys.exit(0)

    bar.collapse_requested.connect(bar.hide_bar)

    bar.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()