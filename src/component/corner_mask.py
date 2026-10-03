# -*- coding: utf-8 -*-
"""盖在 WebView 之上、只画四个圆角的遮罩。"""

from loader import *
from theme import Theme


class CornerMask(QWidget):
    def __init__(self, parent,
                 radius=Theme.WEB_RADIUS,
                 bg_color=Theme.BG_COLOR):
        super().__init__(parent)
        self.radius = radius
        self.bg_color = bg_color
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 外矩形：整个遮罩区域
        outer = QPainterPath()
        outer.addRect(0, 0, self.width(), self.height())

        # 内圆角矩形：inset=0 时和外矩形在四条边重合，
        # outer - inner 的结果只在四个角有非零区域
        inset = 0
        inner = QPainterPath()
        inner.addRoundedRect(
            inset, inset,
            self.width() - 2 * inset,
            self.height() - 2 * inset,
            self.radius, self.radius,
        )

        painter.setBrush(self.bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(outer.subtracted(inner))