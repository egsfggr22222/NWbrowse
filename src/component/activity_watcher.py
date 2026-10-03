# -*- coding: utf-8 -*-
"""全局前台窗口监听：发出 activeWindowChanged 信号。

只应在每个进程里创建一个实例（装在 QApplication 上）。
只监听 WindowActivate / WindowDeactivate，
以及 applicationStateChanged（切到别的程序）。
"""

from loader import *
from PyQt6.QtCore import pyqtSignal


class ActivityWatcher(QObject):
    activeWindowChanged = pyqtSignal(object)   # QWidget 或 None

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self._last = None
        app.installEventFilter(self)
        app.applicationStateChanged.connect(self._on_app_state)

    def eventFilter(self, obj, event):
        et = event.type()
        if et in (
            QEvent.Type.WindowActivate,
            QEvent.Type.WindowDeactivate,
        ):
            # 延后一拍，等 activeWindow 更新完再读
            QTimer.singleShot(0, self._emit)
        return super().eventFilter(obj, event)

    def _on_app_state(self, state):
        QTimer.singleShot(0, self._emit)

    def _emit(self):
        w = self._app.activeWindow()
        print(f"[watcher] emit active={w}")
        if w is not self._last:
            self._last = w
            self.activeWindowChanged.emit(w)