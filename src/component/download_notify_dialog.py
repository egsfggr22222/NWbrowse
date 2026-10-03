# -*- coding: utf-8 -*-
"""右下角下载通知弹窗。两种模式：

    MODE_START    开始下载   —— 显示文件名+大小，3 秒自动收回
    MODE_DONE     下载完成   —— 显示文件名，整块可点，5 秒自动收回

属于下载进程。弹窗从屏幕底部外侧滑入右下角，滑入 300ms，滑出 200ms。
多个弹窗同时存在时从下往上堆叠，每个间距 10px。

不阻塞事件循环。鼠标悬停时暂停自动收回计时。
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
from i18n import t


# ======================================================================
# 弹窗本体
# ======================================================================
class DownloadNotifyDialog(QWidget):

    MODE_START = "start"
    MODE_DONE = "done"

    WIDTH = 320
    PAD = 16
    RADIUS = 12
    MARGIN = 20
    STACK_GAP = 10

    SLIDE_IN_MS = 300
    SLIDE_OUT_MS = 200

    AUTO_HIDE_START_MS = 2000
    AUTO_HIDE_DONE_MS = 2000

    _instances = []

    def __init__(self, mode, parent=None, **kwargs):
        super().__init__(parent)

        self.mode = mode
        self.url = kwargs.get("url", "")
        self.window_id = kwargs.get("window_id", "")
        self.filename = kwargs.get("filename", "") or "download"
        self.total = int(kwargs.get("total", -1) or -1)
        self.dir = kwargs.get("dir", "")
        self.on_click = kwargs.get("on_click", None)

        self._drag_start = None
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._on_auto_hide)

        self._anim = None
        self._closing = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedWidth(self.WIDTH)

        self._build_ui()
        self._adjust_height()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self.PAD, self.PAD, self.PAD, self.PAD
        )
        layout.setSpacing(8)

        self._title_lbl = QLabel()
        f = self._title_lbl.font()
        f.setPointSize(10)
        f.setBold(True)
        self._title_lbl.setFont(f)
        self._title_lbl.setStyleSheet("color: #e6e6e6; background: transparent;")
        layout.addWidget(self._title_lbl)

        self._name_lbl = QLabel(self.filename)
        self._name_lbl.setWordWrap(True)
        self._name_lbl.setStyleSheet(
            "color: #cccccc; font-size: 12px; background: transparent;"
        )
        layout.addWidget(self._name_lbl)

        if self.mode == self.MODE_START:
            self._build_start(layout)
        elif self.mode == self.MODE_DONE:
            self._build_done(layout)

    def _build_start(self, layout):
        self._title_lbl.setText(t("download.toast_start_title"))

        size_text = ""
        if self.total > 0:
            size_text = self._fmt_size(self.total)
        self._size_lbl = QLabel(size_text)
        self._size_lbl.setStyleSheet(
            "color: #999999; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self._size_lbl)

    def _build_done(self, layout):
        self._title_lbl.setText(t("download.toast_title"))

        self._hint_lbl = QLabel(t("download.open_folder"))
        self._hint_lbl.setStyleSheet(
            "color: #7fb3ff; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self._hint_lbl)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _adjust_height(self):
        self.adjustSize()
        self.setFixedWidth(self.WIDTH)

    def _fmt_size(self, n):
        n = int(n)
        if n < 1024:
            return f"{n} B"
        if n < 1024 * 1024:
            return f"{n / 1024:.1f} KB"
        if n < 1024 * 1024 * 1024:
            return f"{n / 1024 / 1024:.2f} MB"
        return f"{n / 1024 / 1024 / 1024:.2f} GB"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        painter.setBrush(QColor(40, 40, 40, 235))
        painter.setPen(QPen(QColor(90, 90, 90, 180), 1))
        painter.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

    def _target_pos(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - self.MARGIN
        below_count = 0
        for d in DownloadNotifyDialog._instances:
            if d is self:
                continue
            below_count += 1
        y = screen.bottom() - self.height() - self.MARGIN
        y -= below_count * (self.height() + self.STACK_GAP)
        if y < screen.top() + self.MARGIN:
            y = screen.top() + self.MARGIN
        return QPoint(x, y)

    def _offscreen_pos(self):
        screen = QApplication.primaryScreen().availableGeometry()
        target = self._target_pos()
        return QPoint(target.x(), screen.bottom() + 10)

    def show_animated(self):
        DownloadNotifyDialog._instances.append(self)
        start = self._offscreen_pos()
        end = self._target_pos()
        self.move(start)
        self.show()
        self.raise_()

        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(self.SLIDE_IN_MS)
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.start()

        ms = self._auto_hide_ms()
        if ms > 0:
            self._hide_timer.start(ms)

    def hide_animated(self):
        if self._closing:
            return
        self._closing = True
        self._hide_timer.stop()

        start = self.pos()
        end = self._offscreen_pos()

        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(self.SLIDE_OUT_MS)
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._anim.finished.connect(self._on_hide_finished)
        self._anim.start()

    def _on_hide_finished(self):
        try:
            if self in DownloadNotifyDialog._instances:
                DownloadNotifyDialog._instances.remove(self)
        except Exception:
            pass
        self.close()
        self.deleteLater()

    def _auto_hide_ms(self):
        if self.mode == self.MODE_START:
            return self.AUTO_HIDE_START_MS
        if self.mode == self.MODE_DONE:
            return self.AUTO_HIDE_DONE_MS
        return 0

    def _on_auto_hide(self):
        self.hide_animated()

    def enterEvent(self, event):
        self._hide_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        ms = self._auto_hide_ms()
        if ms > 0 and not self._closing:
            self._hide_timer.start(ms)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.mode == self.MODE_DONE:
                self._open_folder()
                self.hide_animated()
            elif self.mode == self.MODE_START:
                # 点击打开下载窗口
                if self.on_click is not None:
                    try:
                        self.on_click()
                    except Exception as e:
                        print("[notify] on_click 回调失败:", e)
                self.hide_animated()

    def _open_folder(self):
        path = self.dir
        if not path or not os.path.isdir(path):
            try:
                from settings_backend import SettingsBackend
                path = SettingsBackend().get_download_dir() or ""
            except Exception:
                path = ""
        if not path or not os.path.isdir(path):
            from PyQt6.QtCore import QStandardPaths
            path = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        if path and os.path.isdir(path):
            try:
                os.startfile(path)
            except Exception as e:
                print("[notify] 打开目录失败:", e)