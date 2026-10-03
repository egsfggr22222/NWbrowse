# -*- coding: utf-8 -*-
"""弹出子窗口：URL 历史列表。

设计：
  * 本身不做任何显隐决策，显隐由 owner window 统一控制。
  * 只声明 _owner_window，供 window 判断"我是否等同于被选中"。
  * 关闭按钮走 hide()，不销毁对象（可反复显示）。
  * _user_closed 标记：用户点 X 后，window 不再自动把它拉回来。
  * _user_opened 标记：用户从未主动打开过时，window 不自动显示。
  * 不设 WA_DeleteOnClose，不与 parent.destroyed 反向连接。

窗口外观：
  * 圆角无边框，自绘标题栏 + 自绘 × 按钮。
  * 宽度固定，高度可拖拽，限制在 MIN_H / MAX_H。
  * 黑色系，标题栏与内容同色，无文字。

favicon：
  * set_favicon(pixmap) 由 window 推送当前页图标。
  * 画在标题栏左侧（FAVICON_LEFT）。

URL 列表：
  * 纵向，每项一行，显示 URL（去掉协议头）。
  * 每项右侧一个 × 删除按钮。
  * 点击行发 url_selected(str)。
  * 点 × 发 url_closed(str)。
  * 高亮当前 URL。
  * 相同 URL 不重复追加，跳过去，位置不变。
  * 列表可滚动。
"""

from loader import *


class _TabRow(QWidget):
    """popup 里的单个 URL 行：一行 URL + 右侧 ×。"""

    ROW_H = 30
    PAD_X = 8
    CLOSE_SIZE = 16
    CLOSE_MARGIN = 6
    RADIUS = 6

    BG_NORMAL = QColor(30, 30, 30, 0)
    BG_HOVER = QColor(60, 60, 60, 180)
    BG_SELECTED = QColor(70, 70, 70, 220)

    TEXT_NORMAL = QColor(170, 170, 170)
    TEXT_SELECTED = QColor(240, 240, 240)

    CLOSE_NORMAL = QColor(130, 130, 130)
    CLOSE_HOVER = QColor(220, 80, 80)
    CLOSE_HOVER_BG = QColor(220, 80, 80, 60)

    ACCENT = QColor(90, 150, 230)

    clicked = pyqtSignal(str)
    close_clicked = pyqtSignal(str)

    def __init__(self, url, selected, parent=None):
        super().__init__(parent)
        self._url = url or ""
        self._title = ""
        self._selected = bool(selected)
        self._hover = False
        self._close_hover = False

        self.setFixedHeight(self.ROW_H)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # ---------------- 数据 ----------------
    def url(self):
        return self._url

    def set_selected(self, on):
        on = bool(on)
        if on != self._selected:
            self._selected = on
            self.update()

    def set_url(self, url):
        url = url or ""
        if url != self._url:
            self._url = url
            self.update()
    def title(self):
        return self._title

    def set_title(self, title):
        title = title or ""
        if title != self._title:
            self._title = title
            self.update()

    # ---------------- 几何 ----------------
    def _close_rect(self):
        s = self.CLOSE_SIZE
        return QRectF(
            self.width() - self.CLOSE_MARGIN - s,
            (self.height() - s) / 2.0,
            s, s,
        )

    def _hit_close(self, pos):
        return self._close_rect().contains(QPointF(pos))

    # ---------------- 事件 ----------------
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

    # ---------------- 绘制 ----------------
    @staticmethod
    def _short_url(url):
        if not url:
            return ""
        s = str(url)
        if s.startswith("https://"):
            s = s[8:]
        elif s.startswith("http://"):
            s = s[7:]
        return s

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(0, 0, self.width(), self.height())

        if self._selected:
            painter.setBrush(self.BG_SELECTED)
        elif self._hover:
            painter.setBrush(self.BG_HOVER)
        else:
            painter.setBrush(self.BG_NORMAL)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

        if self._selected:
            bar = QRectF(2, 6, 3, self.height() - 12)
            painter.setBrush(self.ACCENT)
            painter.drawRoundedRect(bar, 1.5, 1.5)

        text_x = self.PAD_X + 6
        close_r = self._close_rect()
        text_w = max(0, close_r.left() - 4 - text_x)
        if text_w <= 0:
            return

        text_color = self.TEXT_SELECTED if self._selected else self.TEXT_NORMAL
        painter.setPen(text_color)

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

        if self._title:
            display = self._title
        else:
            display = self._short_url(self._url) or "(空白页)"
        elided = fm.elidedText(
            display,
            Qt.TextElideMode.ElideRight,
            int(text_rect.width()),
        )
        painter.drawText(
            text_rect,
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
            elided,
        )

        self._paint_close(painter, close_r)

    def _paint_close(self, painter, rect):
        if self._close_hover:
            painter.setBrush(self.CLOSE_HOVER_BG)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 4, 4)
            color = self.CLOSE_HOVER
        else:
            color = self.CLOSE_NORMAL

        pen = QPen(color)
        pen.setWidthF(1.4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        m = rect.width() * 0.30
        painter.drawLine(
            QPointF(rect.left() + m, rect.top() + m),
            QPointF(rect.right() - m, rect.bottom() - m),
        )
        painter.drawLine(
            QPointF(rect.right() - m, rect.top() + m),
            QPointF(rect.left() + m, rect.bottom() - m),
        )


class PopupWindow(QWidget):
    # ---- 尺寸 ----
    FIXED_W = 300
    INIT_H = 600
    MIN_H = 200
    MAX_H = 800

    # ---- 外观 ----
    RADIUS = 12
    TITLE_H = 36
    BORDER = 1
    RESIZE_MARGIN = 6

    BODY_COLOR = QColor(30, 30, 30, 255)
    TITLE_COLOR = QColor(30, 30, 30, 255)
    BORDER_COLOR = QColor(80, 80, 80, 200)
    CLOSE_HOVER = QColor(220, 80, 80)
    CLOSE_TEXT_COLOR = QColor(180, 180, 180)

    LIST_SPACING = 2
    LIST_TOP_PAD = 4
    LIST_BOTTOM_PAD = 4
    LIST_SIDE_PAD = 4

    # ---- favicon ----
    FAVICON_SIZE = 18
    FAVICON_LEFT = 10
    # -----------------

    url_selected = pyqtSignal(str)
    url_closed = pyqtSignal(str)

    def __init__(self, parent=None, title="弹窗"):
        super().__init__(parent)

        self._owner_window = parent
        self._user_closed = False
        self._user_opened = False

        self.setWindowFlag(Qt.WindowType.Window, True)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

        self.setWindowTitle(title)
        self._title_text = title

        self.setFixedWidth(self.FIXED_W)
        self.setMinimumHeight(self.MIN_H)
        self.setMaximumHeight(self.MAX_H)
        self.resize(self.FIXED_W, self.INIT_H)

        self._resize_edge = None
        self._start_global = None
        self._start_geo = None
        self._title_drag_start = None
        self._close_hover = False
        self._cursor = Qt.CursorShape.ArrowCursor

        self._urls = []
        self._current_url = ""
        self._rows = []

        self._favicon = None

        self._setup_ui()

    # =========================================================
    # UI
    # =========================================================
    def _setup_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(
            self.BORDER,
            self.TITLE_H,
            self.BORDER,
            self.BORDER,
        )
        outer.setSpacing(0)

        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self._scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
            "QScrollBar:vertical {"
            "  background: transparent;"
            "  width: 6px;"
            "  margin: 2px 0 2px 0;"
            "}"
            "QScrollBar::handle:vertical {"
            "  background: rgba(120,120,120,0.5);"
            "  border-radius: 3px;"
            "  min-height: 20px;"
            "}"
            "QScrollBar::handle:vertical:hover {"
            "  background: rgba(150,150,150,0.8);"
            "}"
            "QScrollBar::add-line:vertical,"
            "QScrollBar::sub-line:vertical {"
            "  height: 0;"
            "}"
            "QScrollBar::add-page:vertical,"
            "QScrollBar::sub-page:vertical {"
            "  background: transparent;"
            "}"
        )

        self._content = QWidget()
        self._content.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._content)
        self._layout.setContentsMargins(
            self.LIST_SIDE_PAD,
            self.LIST_TOP_PAD,
            self.LIST_SIDE_PAD,
            self.LIST_BOTTOM_PAD,
        )
        self._layout.setSpacing(self.LIST_SPACING)
        self._layout.addStretch(1)

        self._scroll.setWidget(self._content)
        outer.addWidget(self._scroll)

    # =========================================================
    # URL 接口
    # =========================================================
    def urls(self):
        return list(self._urls)

    def current_url(self):
        return self._current_url

    def index_of(self, url):
        if not url:
            return -1
        try:
            return self._urls.index(url)
        except ValueError:
            return -1

    def append_url(self, url):
        """URL 不存在则追加到底部，返回 index。
        URL 已存在则返回已有 index，不重复追加，位置不变。
        """
        if not url:
            return -1

        idx = self.index_of(url)
        if idx >= 0:
            return idx

        self._urls.append(url)
        idx = len(self._urls) - 1

        row = _TabRow(
            url=url,
            selected=(url == self._current_url),
            parent=self._content,
        )
        row.clicked.connect(self.url_selected.emit)
        row.close_clicked.connect(self._on_row_close)
        self._insert_row_widget(row)
        self._rows.append(row)
        return idx

    def set_current_url(self, url):
        """高亮某一行。URL 不在列表里则不做任何事。"""
        url = url or ""
        if url == self._current_url:
            return
        self._current_url = url
        for row in self._rows:
            row.set_selected(row.url() == url)

    def set_title(self, url, title):
        """更新某 URL 行的标题。"""
        if not url:
            return
        for row in self._rows:
            if row.url() == url:
                row.set_title(title)
                return

    def remove_url(self, url):
        """删除某一行。"""
        idx = self.index_of(url)
        if idx < 0:
            return
        self._urls.pop(idx)
        row = self._rows.pop(idx)

        try:
            self._layout.removeWidget(row)
        except Exception:
            pass
        row.setParent(None)
        row.deleteLater()

        if url == self._current_url:
            self._current_url = ""

    def clear_urls(self):
        self._urls = []
        self._current_url = ""
        for row in self._rows:
            try:
                self._layout.removeWidget(row)
            except Exception:
                pass
            row.setParent(None)
            row.deleteLater()
        self._rows = []

    def url_count(self):
        return len(self._urls)

    # =========================================================
    # 内部：插入行 widget（保持 stretch 在末尾）
    # =========================================================
    def _insert_row_widget(self, row):
        count = self._layout.count()
        insert_at = count
        if count > 0:
            last = self._layout.itemAt(count - 1)
            if last is not None and last.spacerItem() is not None:
                insert_at = count - 1
        self._layout.insertWidget(insert_at, row)

    def _on_row_close(self, url):
        self.url_closed.emit(url)

    # =========================================================
    # favicon
    # =========================================================
    def set_favicon(self, pixmap):
        self._favicon = (
            pixmap if (pixmap is not None and not pixmap.isNull()) else None
        )
        self.update()

    def _paint_favicon(self, painter):
        if self._favicon is None:
            return
        dpr = self.devicePixelRatioF()
        px = max(1, int(self.FAVICON_SIZE * dpr))
        pm = self._favicon.scaled(
            px, px,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        pm.setDevicePixelRatio(dpr)
        w_logical = pm.width() / dpr
        h_logical = pm.height() / dpr
        x = float(self.FAVICON_LEFT)
        y = self.BORDER + (self.TITLE_H - h_logical) / 2.0
        painter.drawPixmap(QPointF(x, y), pm)

    # =========================================================
    # 自绘：圆角背景 + × 按钮
    # =========================================================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = self.RADIUS
        outer = QRectF(
            self.BORDER / 2, self.BORDER / 2,
            self.width() - self.BORDER,
            self.height() - self.BORDER,
        )
        painter.setBrush(self.BODY_COLOR)
        painter.setPen(QPen(self.BORDER_COLOR, self.BORDER))
        painter.drawRoundedRect(outer, r, r)

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

        painter.setBrush(self.TITLE_COLOR)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

        self._paint_favicon(painter)
        self._paint_close_btn(painter)

    def _close_btn_rect(self):
        size = self.TITLE_H - 10
        return QRectF(
            self.width() - self.BORDER - size - 6,
            self.BORDER + 5,
            size, size,
        )

    def _paint_close_btn(self, painter):
        rect = self._close_btn_rect()

        if self._close_hover:
            painter.setBrush(self.CLOSE_HOVER)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, 6, 6)
            painter.setPen(QColor(255, 255, 255))
        else:
            painter.setPen(self.CLOSE_TEXT_COLOR)

        pen = painter.pen()
        pen.setWidthF(1.6)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        m = rect.width() * 0.30
        painter.drawLine(
            QPointF(rect.left() + m, rect.top() + m),
            QPointF(rect.right() - m, rect.bottom() - m),
        )
        painter.drawLine(
            QPointF(rect.right() - m, rect.top() + m),
            QPointF(rect.left() + m, rect.bottom() - m),
        )

    # =========================================================
    # 命中判定
    # =========================================================
    def _hit_close(self, pos):
        return self._close_btn_rect().contains(QPointF(pos))

    def _hit_title(self, pos):
        if pos.y() > self.TITLE_H:
            return False
        return not self._hit_close(pos)

    def _hit_edge(self, pos):
        y = pos.y()
        h = self.height()
        m = self.RESIZE_MARGIN
        top = y <= m
        bottom = y >= h - m
        if top and bottom:
            return None
        if top:
            return "t"
        if bottom:
            return "b"
        return None

    # =========================================================
    # 光标
    # =========================================================
    def _update_cursor(self, pos):
        if self._resize_edge is not None:
            cursor = Qt.CursorShape.SizeVerCursor
        elif self._hit_close(pos):
            cursor = Qt.CursorShape.PointingHandCursor
        elif self._hit_edge(pos) in ("t", "b"):
            cursor = Qt.CursorShape.SizeVerCursor
        else:
            cursor = Qt.CursorShape.ArrowCursor

        if cursor != self._cursor:
            self._cursor = cursor
            self.setCursor(cursor)

    def _update_close_hover(self, pos):
        hover = self._hit_close(pos)
        if hover != self._close_hover:
            self._close_hover = hover
            self.update()

    # =========================================================
    # 鼠标事件
    # =========================================================
    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.position().toPoint()

        if self._hit_close(pos):
            self.close()
            return

        edge = self._hit_edge(pos)
        if edge:
            self._resize_edge = edge
            self._start_global = event.globalPosition().toPoint()
            self._start_geo = self.geometry()
            self._update_cursor(pos)
            return

        if self._hit_title(pos):
            self._title_drag_start = (
                event.globalPosition().toPoint() - self.pos()
            )

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()

        self._update_close_hover(pos)
        self._update_cursor(pos)

        if (self._resize_edge and self._start_geo
                and (event.buttons() & Qt.MouseButton.LeftButton)):
            delta = event.globalPosition().toPoint() - self._start_global
            geo = self._start_geo
            x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

            if self._resize_edge == "t":
                new_h = h - delta.y()
                new_y = y + delta.y()
                if new_h < self.MIN_H:
                    new_y = y + (h - self.MIN_H)
                    new_h = self.MIN_H
                if new_h > self.MAX_H:
                    new_y = y + (h - self.MAX_H)
                    new_h = self.MAX_H
                self.setGeometry(x, new_y, w, new_h)
            elif self._resize_edge == "b":
                new_h = h + delta.y()
                new_h = max(self.MIN_H, min(self.MAX_H, new_h))
                self.setGeometry(x, y, w, new_h)
            return

        if (self._title_drag_start is not None
                and (event.buttons() & Qt.MouseButton.LeftButton)):
            self.move(
                event.globalPosition().toPoint() - self._title_drag_start
            )

    def mouseReleaseEvent(self, event):
        self._resize_edge = None
        self._start_global = None
        self._start_geo = None
        self._title_drag_start = None
        self._update_cursor(event.position().toPoint())

    def enterEvent(self, event):
        self._update_cursor(self.mapFromGlobal(QCursor.pos()))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if self._close_hover:
            self._close_hover = False
            self.update()
        if self._cursor != Qt.CursorShape.ArrowCursor:
            self._cursor = Qt.CursorShape.ArrowCursor
            self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)

    # =========================================================
    # 显隐语义
    # =========================================================
    def closeEvent(self, event):
        event.ignore()
        self._user_closed = True
        self.hide()

    def show(self):
        self._user_closed = False
        self._user_opened = True
        super().show()

    def owner_window(self):
        return self._owner_window