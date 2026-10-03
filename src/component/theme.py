# -*- coding: utf-8 -*-
"""集中管理主题 / 尺寸常量。"""

from PyQt6.QtGui import QColor


class Theme:
    RADIUS = 8
    WEB_RADIUS = 10
    RESIZE_MARGIN = 8
    CORNER_MARGIN = 16
    TOP_BAR_HEIGHT = 38
    WEB_TOP_GAP = 0
    SIDE_MARGIN = 6
    BOTTOM_MARGIN = 6

    # ---------------- 颜色（运行时可改） ----------------
    # 边框主题色（比中间深）
    BG_COLOR = QColor("#d0d0d0")
    # 中间区域颜色（比边框浅，不允许纯黑）
    WEB_PLACEHOLDER_COLOR = QColor("#f5f5f7")

    # 标题栏底色，默认跟随边框主题色
    TITLE_BG_COLOR = QColor("#d0d0d0")

    # ---------------- 尺寸 ----------------
    TITLE_BTN_SIZE = 28
    TITLE_ICON_COLOR = "#555555"
    TITLE_LABEL_WIDTH = 56
    TITLE_GAP = 12

    ADDRESS_BAR_HEIGHT = 32
    ADDRESS_BAR_RADIUS = 8
    ADDRESS_BAR_MIN_WIDTH = 200

    INPUT_WIDTH = 600
    INPUT_BG_EXTRA = 8
    INPUT_MAX_HEIGHT = 300
    INPUT_PADDING = 2
    INPUT_RADIUS = 12
    INPUT_SEARCH_BTN_SIZE = 32

    MENU_RADIUS = 10

    # ---------------- 主题派生 ----------------
    # 中间色相对边框色的提亮量（HSV 的 V 通道）
    INNER_LIGHTEN = 44
    # 中间色允许的最小亮度，避免纯黑
    INNER_MIN_VALUE = 40

    @classmethod
    def apply_theme(cls, border_color):
        """根据边框主题色派生中间色。

        * 边框色 = 用户选择
        * 中间色 = 边框色在 HSV 上提亮，因此比边框浅
        * 中间色亮度不低于 INNER_MIN_VALUE，禁止纯黑
        """
        if isinstance(border_color, str):
            border_color = QColor(border_color)
        border_color = QColor(border_color)

        h, s, v, a = border_color.getHsv()
        v2 = min(255, v + cls.INNER_LIGHTEN)
        if v2 < cls.INNER_MIN_VALUE:
            v2 = cls.INNER_MIN_VALUE
        inner = QColor.fromHsv(h, s, v2, a)

        cls.BG_COLOR = border_color
        cls.TITLE_BG_COLOR = border_color
        cls.WEB_PLACEHOLDER_COLOR = inner
        return border_color, inner