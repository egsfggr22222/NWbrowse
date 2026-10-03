# -*- coding: utf-8 -*-
"""设置窗口：左侧导航 + 右侧堆叠页。

UI 文字从 i18n.t() 取。启动时注册 _refresh_texts 到 i18n.on_change，
语言变化时自动刷新。
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
from i18n import t, on_change


# 导航项：(page_key, i18n_key)
NAV_ITEMS = [
    ("general",  "nav.general"),
    ("history",  "nav.history"),
    ("language", "nav.language"),
]


class NavList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(160)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            "QListWidget {"
            "  background: #f5f5f5;"
            "  border: none;"
            "  outline: none;"
            "  padding: 8px 6px;"
            "  border-radius: 8px;"
            "}"
            "QListWidget::item {"
            "  height: 36px;"
            "  padding-left: 12px;"
            "  border-radius: 6px;"
            "  color: #333;"
            "  font-size: 13px;"
            "}"
            "QListWidget::item:hover {"
            "  background: #e8e8e8;"
            "}"
            "QListWidget::item:selected {"
            "  background: #e8f0fe;"
            "  color: #2f5fd0;"
            "}"
        )
        self.viewport().setStyleSheet("background: transparent;")
        for key, i18n_key in NAV_ITEMS:
            item = QListWidgetItem(t(i18n_key))
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.addItem(item)
        self.setCurrentRow(0)

    def _refresh_texts(self):
        for i, (key, i18n_key) in enumerate(NAV_ITEMS):
            if i < self.count():
                item = self.item(i)
                if item is not None:
                    item.setText(t(i18n_key))


class SettingsWindow(QWidget):

    RADIUS = 12
    WIDTH = 760
    HEIGHT = 560
    PAD = 20
    BORDER_COLOR = QColor(160, 160, 160)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start = None
        self._backend = None
        self._pages = {}
        self._on_change_cb = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self._build_ui()
        self._center_on_parent()

        # 注册语言变化回调
        self._on_change_cb = self._refresh_texts
        try:
            on_change(self._on_change_cb)
        except Exception as e:
            print("[settings] 注册语言回调失败:", e)

    def set_backend(self, backend):
        self._backend = backend
        for page in self._pages.values():
            if hasattr(page, "set_backend"):
                page.set_backend(backend)

    def _build_ui(self):
        body = QHBoxLayout(self)
        body.setContentsMargins(self.PAD, self.PAD, self.PAD, self.PAD)
        body.setSpacing(8)

        self.nav = NavList(self)
        self.nav.currentRowChanged.connect(self._on_nav_changed)
        body.addWidget(self.nav)

        self.stack = QStackedWidget(self)
        self.stack.setStyleSheet(
            "QStackedWidget { background: transparent; }"
        )
        body.addWidget(self.stack, 1)

        self.close_btn = QPushButton("×", self)
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet(
            "QPushButton {"
            "  color: #555;"
            "  background: transparent;"
            "  border: none;"
            "  font-size: 16px;"
            "}"
            "QPushButton:hover {"
            "  background: #e0e0e0;"
            "  border-radius: 6px;"
            "}"
        )
        self.close_btn.clicked.connect(self.close)
        self.close_btn.move(self.WIDTH - 28 - self.PAD, self.PAD)
        self.close_btn.raise_()

        from settings_pages import (
            GeneralPage, HistoryPage, LanguagePage,
        )
        page_classes = {
            "general": GeneralPage,
            "history": HistoryPage,
            "language": LanguagePage,
        }
        for key, _i18n in NAV_ITEMS:
            page_cls = page_classes[key]
            page = page_cls(self.stack)
            self._pages[key] = page
            self.stack.addWidget(page)

    def _on_nav_changed(self, row):
        if 0 <= row < self.stack.count():
            self.stack.setCurrentIndex(row)

    def _refresh_texts(self):
        """语言变化后刷新整个设置窗口的 UI 文字。"""
        print("[settings] _refresh_texts 被调用")
        try:
            self.nav._refresh_texts()
            print("[settings] 刷新导航成功")
        except Exception as e:
            print("[settings] 刷新导航失败:", e)

        for key, page in self._pages.items():
            if hasattr(page, "_refresh_texts"):
                try:
                    page._refresh_texts()
                    print(f"[settings] 刷新页面 {key} 成功")
                except Exception as e:
                    print(f"[settings] 刷新页面 {key} 失败:", e)

    def _center_on_parent(self):
        parent = self.parent()
        if parent is not None:
            pg = parent.geometry()
            self.move(
                pg.x() + (pg.width() - self.width()) // 2,
                pg.y() + (pg.height() - self.height()) // 2,
            )
            return

        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.left() + (screen.width() - self.width()) // 2,
            screen.top() + (screen.height() - self.height()) // 2,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(self.BORDER_COLOR, 1))
        painter.drawRoundedRect(
            QRectF(0.5, 0.5, self.width() - 1, self.height() - 1),
            self.RADIUS, self.RADIUS,
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint() - self.pos()

    def mouseMoveEvent(self, event):
        if self._drag_start and (event.buttons() & Qt.MouseButton.LeftButton):
            self.move(event.globalPosition().toPoint() - self._drag_start)

    def mouseReleaseEvent(self, event):
        self._drag_start = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)