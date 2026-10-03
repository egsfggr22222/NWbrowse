# -*- coding: utf-8 -*-
"""无痕窗口的弹窗：半透明 + 渐变。

继承 PopupWindow，只改背景绘制。
- 背景：紫→酒红渐变，半透明
- 标题栏：比正文更透
- 其余逻辑（URL 列表、拖动、缩放、favicon）全继承
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
from popup_window import PopupWindow, _TabRow


# ======================================================================
# 配色
# ======================================================================
GRAD_TOP_LEFT     = QColor(106, 13, 173, 180)   # 紫，alpha=180
GRAD_BOTTOM_RIGHT = QColor(114, 47, 55, 180)    # 酒红，alpha=180

TITLE_ALPHA_EXTRA = -40     # 标题栏比正文再透 40
BORDER_COLOR      = QColor(255, 255, 255, 120)  # 半透明白描边


class IncognitoPopupWindow(PopupWindow):
    """无痕弹窗。只覆盖背景绘制 + 行配色。"""

    def __init__(self, parent=None, title="弹窗"):
        super().__init__(parent=parent, title=title)
        self._apply_row_style()

    def _apply_row_style(self):
        """让每一行也半透明，跟渐变协调。"""
        try:
            for row in self._rows:
                row.BG_SELECTED = QColor(255, 255, 255, 70)
                row.BG_HOVER = QColor(255, 255, 255, 40)
                row.BG_NORMAL = QColor(0, 0, 0, 0)
                row.TEXT_NORMAL = QColor(230, 230, 230)
                row.TEXT_SELECTED = QColor(255, 255, 255)
                row.ACCENT = QColor(255, 255, 255, 220)
                row.CLOSE_NORMAL = QColor(200, 200, 200)
                row.CLOSE_HOVER = QColor(255, 120, 120)
                row.CLOSE_HOVER_BG = QColor(220, 80, 80, 90)
                row.update()
        except Exception as e:
            print("[inc-popup] 改行样式失败:", e)

    def append_url(self, url):
        idx = super().append_url(url)
        # 新增行后重新上色
        self._apply_row_style()
        return idx

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = self.RADIUS
        outer = QRectF(
            self.BORDER / 2, self.BORDER / 2,
            self.width() - self.BORDER,
            self.height() - self.BORDER,
        )

        # ---- 整体：紫→酒红渐变，半透明 ----
        grad = QLinearGradient(outer.topLeft(), outer.bottomRight())
        grad.setColorAt(0.0, GRAD_TOP_LEFT)
        grad.setColorAt(1.0, GRAD_BOTTOM_RIGHT)

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(BORDER_COLOR, self.BORDER))
        painter.drawRoundedRect(outer, r, r)

        # ---- 标题栏：比正文再透一点 ----
        title_rect = QRectF(
            self.BORDER, self.BORDER,
            self.width() - 2 * self.BORDER,
            self.TITLE_H,
        )
        ir = max(0, r - self.BORDER)
        path = QPainterPath()
        path.moveTo(title_rect.left(), title_rect.bottom())
        path.lineTo(title_rect.left(), title_rect.top() + ir)
        path.arcTo(
            title_rect.left(), title_rect.top(),
            2 * ir, 2 * ir, 180, -90,
        )
        path.lineTo(title_rect.right() - ir, title_rect.top())
        path.arcTo(
            title_rect.right() - 2 * ir, title_rect.top(),
            2 * ir, 2 * ir, 90, -90,
        )
        path.lineTo(title_rect.right(), title_rect.bottom())
        path.closeSubpath()

        # 标题栏：白一点，更透
        title_c = QColor(255, 255, 255, 40)
        painter.setBrush(title_c)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

        # ---- favicon + 关闭按钮（父类方法） ----
        self._paint_favicon(painter)
        self._paint_close_btn(painter)


# ======================================================================
# 入口：单独跑，弹一个空无痕弹窗看效果
# ======================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = IncognitoPopupWindow(title="无痕弹窗测试")
    w.append_url("https://www.bing.com/")
    w.append_url("https://www.bilibili.com/")
    w.append_url("https://www.zhihu.com/")
    w.show()

    sys.exit(app.exec())