# -*- coding: utf-8 -*-
"""窗口图标工具：favicon 优先，没有就用主域名字符串在内存生成图标。

不落盘，纯内存 QPixmap -> QIcon。
"""

import os

from loader import *


import apppaths

DEFAULT_ICON_PATH = os.path.join(apppaths.RES_DIR, "data", "icon.ico")


# ======================================================================
# 默认图标（data/icon.ico）
# ======================================================================
_default_icon_cache = None


def default_icon():
    """读 data/icon.ico。读不到返回空 QIcon。带缓存。"""
    global _default_icon_cache
    if _default_icon_cache is not None:
        return _default_icon_cache

    if os.path.isfile(DEFAULT_ICON_PATH):
        _default_icon_cache = QIcon(DEFAULT_ICON_PATH)
    else:
        _default_icon_cache = QIcon()
    return _default_icon_cache


# ======================================================================
# 主域名字符串 -> 内存图标
# ======================================================================
def make_domain_icon(host,
                     size=64,
                     color_top="#5a5a7a",
                     color_bottom="#3a3a5a",
                     text_color="#ffffff"):
    """把主域名字符串画成图标（内存，不落盘）。

    host: 如 "www.bilibili.com" -> 取 "bilibili" -> 显示 "BI"
    size: 图标像素尺寸，默认 64
    """
    if not host:
        return QIcon()

    # 取主域
    parts = host.split(".")
    if len(parts) >= 2:
        label = parts[-2]
    else:
        label = host

    label = label.upper()
    text = label[:2] if len(label) > 1 else label[:1]

    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

    rect = QRectF(0, 0, size, size)
    grad = QLinearGradient(rect.topLeft(), rect.bottomRight())
    grad.setColorAt(0.0, QColor(color_top))
    grad.setColorAt(1.0, QColor(color_bottom))
    painter.setBrush(QBrush(grad))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(rect)

    font = QFont()
    font.setPointSize(int(size * 0.42))
    font.setBold(True)
    painter.setFont(font)
    painter.setPen(QColor(text_color))
    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

    painter.end()
    return QIcon(pm)


# ======================================================================
# 对外的统一入口：给窗口挑一个图标
# ======================================================================
def icon_for_window(favicon_pixmap, url, **domain_kwargs):
    """
    favicon_pixmap: QPixmap 或 None
    url: 当前 URL
    返回 QIcon
    """
    # 1. 有 favicon 用 favicon
    if favicon_pixmap is not None and not favicon_pixmap.isNull():
        return QIcon(favicon_pixmap)

    # 2. 没 favicon，用主域名字符串生成
    host = _url_host(url)
    if host:
        return make_domain_icon(host, **domain_kwargs)

    # 3. 都没有，用默认 data/icon.ico
    return default_icon()


def _url_host(url):
    """从 URL 取 host（去 www.）。"""
    if not url:
        return ""
    try:
        from urllib.parse import urlparse
        host = (urlparse(url).hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def apply_icon_to_window(window, favicon_pixmap, url, **domain_kwargs):
    """给窗口设图标。返回设的 QIcon。"""
    icon = icon_for_window(favicon_pixmap, url, **domain_kwargs)
    try:
        window.setWindowIcon(icon)
    except Exception as e:
        print("[window_icon] setWindowIcon 失败:", e)
    return icon