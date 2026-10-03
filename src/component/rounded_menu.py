# -*- coding: utf-8 -*-
"""圆角菜单。"""

from loader import *
from theme import Theme


class RoundedMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(
            "QMenu {"
            "  background: transparent;"
            "  border: none;"
            "  padding: 4px;"
            "}"
            "QMenu::item {"
            "  padding: 4px 20px 4px 12px;"
            "  border-radius: 4px;"
            "  color: #333333;"
            "  background: transparent;"
            "}"
            "QMenu::item:selected {"
            "  background: #e8f0fe;"
            "}"
            "QMenu::separator {"
            "  height: 1px;"
            "  background: #e0e0e0;"
            "  margin: 2px 6px;"
            "}"
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(QColor(204, 204, 204), 1))
        painter.drawRoundedRect(
            self.rect().adjusted(0, 0, -1, -1),
            Theme.MENU_RADIUS, Theme.MENU_RADIUS,
        )
        super().paintEvent(event)