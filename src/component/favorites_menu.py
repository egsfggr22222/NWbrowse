# -*- coding: utf-8 -*-
"""收藏下拉菜单：无边框小窗口，QListWidget 列表，每行 title + ×。

* 白底圆角 + 阴影
* 宽 300，高 800
* 每行显示收藏的 title，右侧一个 × 删除按钮
* 点行（× 以外）→ emit url_selected(url)
* 点 × → emit url_closed(url)
* 点窗口外 → 自动关闭（QApplication.installEventFilter）
* 数据从 favorites_store.load_all() 读
"""

import os

from loader import *


class _FavRow(QWidget):
    """单行：title（左）+ × （右）。"""

    ROW_H = 28
    PAD_X = 10
    CLOSE_SIZE = 18
    CLOSE_MARGIN = 6

    BG_NORMAL = QColor(255, 255, 255, 0)
    BG_HOVER = QColor(240, 240, 240)
    TEXT_COLOR = QColor(60, 60, 60)
    CLOSE_NORMAL = QColor(140, 140, 140)
    CLOSE_HOVER = QColor(220, 80, 80)
    CLOSE_HOVER_BG = QColor(220, 80, 80, 60)

    clicked = pyqtSignal(str)
    close_clicked = pyqtSignal(str)

    def __init__(self, url, title, parent=None):
        super().__init__(parent)
        self._url = url or ""
        self._title = title or url or ""
        self._hover = False
        self._close_hover = False

        self.setFixedHeight(self.ROW_H)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(self._url)

    def _close_rect(self):
        s = self.CLOSE_SIZE
        return QRectF(
            self.width() - self.CLOSE_MARGIN - s,
            (self.height() - s) / 2.0,
            s, s,
        )

    def _hit_close(self, pos):
        return self._close_rect().contains(QPointF(pos))

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._close_hover = False
        self.update()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        hover = self._hit_close(event.position().toPoint())
        if hover != self._close_hover:
            self._close_hover = hover
            self.update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.position().toPoint()
        if self._hit_close(pos):
            self.close_clicked.emit(self._url)
            return
        self.clicked.emit(self._url)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(0, 0, self.width(), self.height())
        if self._hover:
            painter.setBrush(self.BG_HOVER)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 4, 4)

        text_x = self.PAD_X
        close_r = self._close_rect()
        text_w = max(0, close_r.left() - 4 - text_x)
        if text_w > 0:
            painter.setPen(self.TEXT_COLOR)
            font = painter.font()
            base = font.pointSizeF()
            if base <= 0:
                base = 9.0
            font.setPointSizeF(max(8.5, base))
            painter.setFont(font)

            fm = painter.fontMetrics()
            text_rect = QRectF(
                text_x,
                (self.height() - fm.height()) / 2.0,
                text_w,
                fm.height(),
            )
            elided = fm.elidedText(
                self._title,
                Qt.TextElideMode.ElideRight,
                int(text_rect.width()),
            )
            painter.drawText(
                text_rect,
                int(Qt.AlignmentFlag.AlignLeft |
                    Qt.AlignmentFlag.AlignVCenter),
                elided,
            )

        # ×
        if self._close_hover:
            painter.setBrush(self.CLOSE_HOVER_BG)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(close_r, 4, 4)
            color = self.CLOSE_HOVER
        else:
            color = self.CLOSE_NORMAL

        pen = QPen(color)
        pen.setWidthF(1.4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        m = close_r.width() * 0.30
        painter.drawLine(
            QPointF(close_r.left() + m, close_r.top() + m),
            QPointF(close_r.right() - m, close_r.bottom() - m),
        )
        painter.drawLine(
            QPointF(close_r.right() - m, close_r.top() + m),
            QPointF(close_r.left() + m, close_r.bottom() - m),
        )


class FavoritesMenu(QWidget):
    """收藏下拉菜单。"""

    WIDTH = 300
    HEIGHT = 200
    RADIUS = 10
    PAD = 6

    url_selected = pyqtSignal(str)
    url_closed = pyqtSignal(str)

    _all_menus = []

    def __init__(self, parent=None):
        super().__init__(parent)

        # 普通窗口：不置顶、不抢焦点、无边框
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Popup
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self._rows = []
        self._build_ui()

        FavoritesMenu._all_menus.append(self)

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(
            self.PAD, self.PAD, self.PAD, self.PAD
        )
        outer.setSpacing(0)

        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
            "QScrollBar:vertical {"
            "  background: transparent; width: 6px;"
            "  margin: 2px 0;"
            "}"
            "QScrollBar::handle:vertical {"
            "  background: rgba(120,120,120,0.5);"
            "  border-radius: 3px; min-height: 20px;"
            "}"
            "QScrollBar::handle:vertical:hover {"
            "  background: rgba(120,120,120,0.8);"
            "}"
            "QScrollBar::add-line:vertical,"
            "QScrollBar::sub-line:vertical { height: 0; }"
            "QScrollBar::add-page:vertical,"
            "QScrollBar::sub-page:vertical { background: transparent; }"
        )

        self._host = QWidget()
        self._host.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._host)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addStretch(1)

        self._scroll.setWidget(self._host)
        outer.addWidget(self._scroll)

        self._reload()

    def _reload(self):
        while self._layout.count():
            item = self._layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
        self._layout.addStretch(1)
        self._rows = []

        try:
            from favorites_store import load_all
            data = load_all()
        except Exception as e:
            print("[fav-menu] 读收藏失败:", e)
            data = []

        for it in data:
            if not isinstance(it, dict):
                continue
            url = it.get("url", "")
            title = it.get("title", "") or url
            if not url:
                continue

            row = _FavRow(url, title, self._host)
            row.clicked.connect(self._on_row_clicked)
            row.close_clicked.connect(self._on_row_close)
            idx = self._layout.count() - 1
            self._layout.insertWidget(idx, row)
            self._rows.append(row)

    def _on_row_clicked(self, url):
        self.url_selected.emit(url)
        self._close()

    def _on_row_close(self, url):
        try:
            from favorites_store import remove
            remove(url)
        except Exception as e:
            print("[fav-menu] 删除失败:", e)
        self._reload()
        # 通知 window：这条收藏被删了
        self.url_closed.emit(url)

    def popup_at(self, global_pos):
        """在 global_pos（全局 QPoint）显示。"""
        self.move(global_pos)
        self.show()
        self.raise_()
        self.activateWindow()

    def _close(self):
        try:
            FavoritesMenu._all_menus.remove(self)
        except Exception:
            pass
        self.hide()
        self.deleteLater()





    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(QColor(220, 220, 220), 1))
        painter.drawRoundedRect(rect, self.RADIUS, self.RADIUS)