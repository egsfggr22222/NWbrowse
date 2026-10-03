# -*- coding: utf-8 -*-
"""个性化窗口：主题色 + 背景图片（缩略图网格、右键删除、清空）。

UI 文字从 i18n.t() 取。启动时注册 _refresh_texts 到 i18n.on_change，
语言变化时自动刷新。关闭时注销。
"""

import os

from loader import *
from theme import Theme
from i18n import t


class ColorPanel(QWidget):
    """调色盘：主色相区 + 亮度条，当前色通过外层边框体现。"""

    color_changed = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(380, 180)
        self.setMouseTracking(True)

        self._h = 0.0
        self._s = 1.0
        self._v = 1.0

        self._hue_pix = None
        self._bar_w = 16
        self._bar_gap = 10

        self._border_w = 4
        self._border_gap = 4

        self._drag_target = None

    def _outer_rect(self):
        return self.rect().adjusted(0, 0, -1, -1)

    def _inner_rect(self):
        m = self._border_w + self._border_gap
        return self.rect().adjusted(m, m, -m - 1, -m - 1)

    def _main_rect(self):
        r = self._inner_rect()
        bw = self._bar_w + self._bar_gap
        return QRect(r.x(), r.y(), r.width() - bw, r.height())

    def _bar_rect(self):
        r = self._inner_rect()
        x = r.right() - self._bar_w + 1
        return QRect(x, r.y(), self._bar_w, r.height())

    def _build_hue_pixmap(self):
        r = self._main_rect()
        img = QImage(r.width(), r.height(), QImage.Format.Format_RGB32)
        for x in range(r.width()):
            h = x / max(1, r.width() - 1)
            for y in range(r.height()):
                v = 1.0 - y / max(1, r.height() - 1)
                img.setPixelColor(x, y, QColor.fromHsvF(h, 1.0, v))
        self._hue_pix = QPixmap.fromImage(img)

    def _build_bar_pixmap(self):
        r = self._bar_rect()
        img = QImage(r.width(), r.height(), QImage.Format.Format_RGB32)
        for y in range(r.height()):
            s = 1.0 - y / max(1, r.height() - 1)
            c = QColor.fromHsvF(self._h, s, 1.0)
            for x in range(r.width()):
                img.setPixelColor(x, y, c)
        return QPixmap.fromImage(img)

    def color(self):
        return QColor.fromHsvF(self._h, self._s, self._v)

    def set_color(self, color):
        h, s, v, _ = color.getHsvF()
        if h < 0:
            h = 0.0
        self._h, self._s, self._v = h, s, v
        self._build_hue_pixmap()
        self.update()

    def _update_from_pos(self, pos):
        main = self._main_rect()
        bar = self._bar_rect()

        if self._drag_target == "main" or (self._drag_target is None and main.contains(pos)):
            h = (pos.x() - main.x()) / max(1, main.width() - 1)
            v = 1.0 - (pos.y() - main.y()) / max(1, main.height() - 1)
            self._h = min(1.0, max(0.0, h))
            self._v = min(1.0, max(0.0, v))
            self.update()
            self.color_changed.emit(self.color())
        elif self._drag_target == "bar" or (self._drag_target is None and bar.contains(pos)):
            s = 1.0 - (pos.y() - bar.y()) / max(1, bar.height() - 1)
            self._s = min(1.0, max(0.0, s))
            self.update()
            self.color_changed.emit(self.color())

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = event.position().toPoint()
        if self._bar_rect().contains(pos):
            self._drag_target = "bar"
        elif self._main_rect().contains(pos):
            self._drag_target = "main"
        else:
            self._drag_target = None
            return
        self._update_from_pos(pos)

    def mouseMoveEvent(self, event):
        if self._drag_target and (event.buttons() & Qt.MouseButton.LeftButton):
            self._update_from_pos(event.position().toPoint())

    def mouseReleaseEvent(self, event):
        self._drag_target = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        outer = QRectF(self._outer_rect())
        pen = QPen(self.color())
        pen.setWidth(self._border_w)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(
            outer.adjusted(self._border_w / 2, self._border_w / 2,
                           -self._border_w / 2, -self._border_w / 2),
            8, 8,
        )

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        main = self._main_rect()
        bar = self._bar_rect()

        if self._hue_pix is None:
            self._build_hue_pixmap()

        painter.drawPixmap(main.topLeft(), self._hue_pix)
        painter.drawPixmap(bar.topLeft(), self._build_bar_pixmap())

        cx = main.x() + int(self._h * (main.width() - 1))
        cy = main.y() + int((1.0 - self._v) * (main.height() - 1))
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(cx - 6, cy, cx + 6, cy)
        painter.drawLine(cx, cy - 6, cx, cy + 6)

        by = bar.y() + int((1.0 - self._s) * (bar.height() - 1))
        tri = QPolygon([
            QPoint(bar.right() + 2, by),
            QPoint(bar.right() + 8, by - 5),
            QPoint(bar.right() + 8, by + 5),
        ])
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(tri)


class ThumbLabel(QLabel):
    """缩略图。左键选中/取消，右键弹出菜单。"""

    clicked = pyqtSignal(str)
    delete_requested = pyqtSignal(str)

    THUMB_W = 88
    THUMB_H = 54

    def __init__(self, path, selected=False, parent=None):
        super().__init__(parent)
        self.path = path
        self.setFixedSize(self.THUMB_W, self.THUMB_H)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 内置背景图在设置里存成 {RES}/... ，这里要展开成真实路径
        try:
            from settings import resolve_path
            real = resolve_path(path)
        except Exception:
            real = path

        pm = QPixmap(real)
        if not pm.isNull():
            scaled = pm.scaled(
                self.THUMB_W - 6, self.THUMB_H - 6,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.setPixmap(scaled)

        self.set_selected(selected)

    def set_selected(self, selected):
        if selected:
            self.setStyleSheet(
                "QLabel { background: #eef3fd; border: 2px solid #7aa7f0;"
                " border-radius: 6px; }"
            )
        else:
            self.setStyleSheet(
                "QLabel { background: #f5f5f5; border: 1px solid #dcdcdc;"
                " border-radius: 6px; }"
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.path)
        elif event.button() == Qt.MouseButton.RightButton:
            self._show_context_menu(event)
        super().mousePressEvent(event)

    def _show_context_menu(self, event):
        menu = QMenu(self)
        act_delete = menu.addAction(t("personalize.delete"))
        act_delete.triggered.connect(lambda: self.delete_requested.emit(self.path))
        menu.exec(event.globalPosition().toPoint())


class PersonalizeDialog(QWidget):
    """无边框个性化窗口。同一时间只应存在一个实例。"""

    theme_applied = pyqtSignal(QColor)
    background_changed = pyqtSignal(str, list)

    RADIUS = 12
    SHADOW_MARGIN = 16
    CONTENT_W = 520
    CONTENT_H = 470

    COLS = 5

    def __init__(self, current_color, images=None, current_bg="", parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(
            self.CONTENT_W + self.SHADOW_MARGIN * 2,
            self.CONTENT_H + self.SHADOW_MARGIN * 2,
        )

        self._color = QColor(current_color)
        self._images = list(images or [])
        self._current_bg = current_bg or ""
        self._drag_start = None

        self._thumb_widgets = []
        self._on_change_cb = None

        self._build_ui()
        self._apply_shadow()
        self._panel.set_color(self._color)
        self._rebuild_thumbs()

        self._center_on_parent()

        # 注册语言变化回调
        self._on_change_cb = self._refresh_texts
        try:
            from i18n import on_change
            on_change(self._on_change_cb)
        except Exception as e:
            print("[personalize] 注册语言回调失败:", e)

    def _build_ui(self):
        self._content = QFrame(self)
        self._content.setGeometry(
            self.SHADOW_MARGIN, self.SHADOW_MARGIN,
            self.CONTENT_W, self.CONTENT_H,
        )
        self._content.setStyleSheet(
            "QFrame { background: #ffffff; border-radius: 12px; }"
        )

        root = QVBoxLayout(self._content)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ---- 顶部 ----
        header = QHBoxLayout()
        header.setContentsMargins(16, 10, 10, 6)
        header.setSpacing(10)

        self._title_lbl = QLabel(t("personalize.title"), self._content)
        self._title_lbl.setStyleSheet(
            "font-size: 14px; font-weight: 600; color: #333;")
        header.addWidget(self._title_lbl)
        header.addStretch(1)

        close_btn = QPushButton("×", self._content)
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(
            "QPushButton { color: #555; background: transparent; border: none;"
            " font-size: 16px; }"
            "QPushButton:hover { background: #e0e0e0; border-radius: 6px; }"
        )
        close_btn.clicked.connect(self.close)
        header.addWidget(close_btn)

        root.addLayout(header)

        # ---- 主题色 ----
        self._sec_theme = QLabel(t("personalize.theme_color"), self._content)
        self._sec_theme.setStyleSheet(
            "font-size: 12px; color: #666; margin-left: 16px;"
        )
        root.addWidget(self._sec_theme)

        body = QHBoxLayout()
        body.setContentsMargins(16, 6, 16, 0)
        self._panel = ColorPanel(self._content)
        self._panel.color_changed.connect(self._on_panel_color)
        body.addWidget(self._panel)
        root.addLayout(body)

        # ---- 背景图片标题行 + 加号 ----
        bg_head = QHBoxLayout()
        bg_head.setContentsMargins(16, 14, 16, 0)
        bg_head.setSpacing(10)

        self._sec_bg = QLabel(t("personalize.background"), self._content)
        self._sec_bg.setStyleSheet("font-size: 12px; color: #666;")
        bg_head.addWidget(self._sec_bg)
        bg_head.addStretch(1)

        self._add_btn = QPushButton("+", self._content)
        self._add_btn.setFixedSize(24, 24)
        self._add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_btn.setToolTip(t("personalize.pick_image"))
        self._add_btn.setStyleSheet(
            "QPushButton {"
            "  background: #f5f5f5;"
            "  color: #444;"
            "  border: 1px solid #dcdcdc;"
            "  border-radius: 12px;"
            "  font-size: 15px;"
            "}"
            "QPushButton:hover { background: #ececec; border: 1px solid #cfcfcf; }"
            "QPushButton:pressed { background: #e2e2e2; }"
        )
        self._add_btn.clicked.connect(self._pick_background)
        bg_head.addWidget(self._add_btn)
        root.addLayout(bg_head)

        # ---- 分隔线 ----
        line = QFrame(self._content)
        line.setFixedHeight(1)
        line.setStyleSheet("background: #e5e5e5; margin-left: 16px; margin-right: 16px;")
        root.addWidget(line)

        # ---- 缩略图滚动区 ----
        self._scroll = QScrollArea(self._content)
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setStyleSheet(
            "QScrollArea { background: transparent; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )

        self._grid_host = QWidget()
        self._grid = QGridLayout(self._grid_host)
        self._grid.setContentsMargins(16, 10, 16, 10)
        self._grid.setSpacing(8)
        self._scroll.setWidget(self._grid_host)

        root.addWidget(self._scroll, 1)

        # ---- 底部：清空 + 取消 + 确定 ----
        bottom = QHBoxLayout()
        bottom.setContentsMargins(16, 8, 16, 12)
        bottom.setSpacing(10)

        self._clear_btn = QPushButton(t("personalize.clear"), self._content)
        self._clear_btn.setFixedSize(72, 32)
        self._clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._clear_btn.setStyleSheet(self._btn_style(primary=False))
        self._clear_btn.clicked.connect(self._on_clear_clicked)
        bottom.addWidget(self._clear_btn)

        bottom.addStretch(1)

        self._cancel_btn = QPushButton(t("common.cancel"), self._content)
        self._cancel_btn.setFixedSize(84, 32)
        self._cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_btn.setStyleSheet(self._btn_style(primary=False))
        self._cancel_btn.clicked.connect(self.close)
        bottom.addWidget(self._cancel_btn)

        self._ok_btn = QPushButton(t("common.ok"), self._content)
        self._ok_btn.setFixedSize(84, 32)
        self._ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._ok_btn.setStyleSheet(self._btn_style(primary=True))
        self._ok_btn.clicked.connect(self._on_ok)
        bottom.addWidget(self._ok_btn)

        root.addLayout(bottom)

    def _refresh_texts(self):
        """语言变化后重设所有文字。"""
        try:
            self._title_lbl.setText(t("personalize.title"))
            self._sec_theme.setText(t("personalize.theme_color"))
            self._sec_bg.setText(t("personalize.background"))
            if hasattr(self, "_add_btn"):
                self._add_btn.setToolTip(t("personalize.pick_image"))
            self._clear_btn.setText(t("personalize.clear"))
            self._cancel_btn.setText(t("common.cancel"))
            self._ok_btn.setText(t("common.ok"))
        except Exception as e:
            print("[personalize] 刷新文字失败:", e)

    def _btn_style(self, primary):
        if primary:
            return (
                "QPushButton {"
                "  background: #eef3fd;"
                "  color: #2f5fd0;"
                "  border: 1px solid #b9cdf5;"
                "  border-radius: 8px;"
                "  font-size: 13px;"
                "}"
                "QPushButton:hover {"
                "  background: #e0eafb;"
                "  border: 1px solid #9dbaf1;"
                "}"
                "QPushButton:pressed {"
                "  background: #d3e1f9;"
                "}"
            )
        return (
            "QPushButton {"
            "  background: #f5f5f5;"
            "  color: #444444;"
            "  border: 1px solid #dcdcdc;"
            "  border-radius: 8px;"
            "  font-size: 13px;"
            "}"
            "QPushButton:hover {"
            "  background: #ececec;"
            "  border: 1px solid #cfcfcf;"
            "}"
            "QPushButton:pressed {"
            "  background: #e2e2e2;"
            "}"
        )

    def _apply_shadow(self):
        shadow = QGraphicsDropShadowEffect(self._content)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self._content.setGraphicsEffect(shadow)

    def _rebuild_thumbs(self):
        for w in self._thumb_widgets:
            w.setParent(None)
            w.deleteLater()
        self._thumb_widgets = []

        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for idx, path in enumerate(self._images):
            thumb = ThumbLabel(path, selected=(path == self._current_bg))
            thumb.clicked.connect(self._on_thumb_clicked)
            thumb.delete_requested.connect(self._on_thumb_delete)
            r = idx // self.COLS
            c = idx % self.COLS
            self._grid.addWidget(thumb, r, c)
            self._thumb_widgets.append(thumb)

        rows = (len(self._images) + self.COLS - 1) // self.COLS
        self._grid.setRowStretch(rows, 1)

    def _on_thumb_clicked(self, path):
        if path == self._current_bg:
            self._current_bg = ""
        else:
            self._current_bg = path

        for t_ in self._thumb_widgets:
            t_.set_selected(t_.path == self._current_bg and self._current_bg != "")

    def _on_thumb_delete(self, path):
        if path in self._images:
            self._images.remove(path)
        if self._current_bg == path:
            self._current_bg = ""
        self._rebuild_thumbs()

    def _on_clear_clicked(self):
        if not self._images:
            return
        box = QMessageBox(self._content)
        box.setWindowTitle(t("personalize.clear_confirm_title"))
        box.setText(t("personalize.clear_confirm_text"))
        box.setIcon(QMessageBox.Icon.Question)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        box.button(QMessageBox.StandardButton.Yes).setText(t("common.ok"))
        box.button(QMessageBox.StandardButton.No).setText(t("common.cancel"))
        if box.exec() == QMessageBox.StandardButton.Yes:
            self._images = []
            self._current_bg = ""
            self._rebuild_thumbs()

    def _pick_background(self):
        path, _ = QFileDialog.getOpenFileName(
            self._content,
            t("personalize.pick_image"),
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if not path:
            return
        if path not in self._images:
            self._images.append(path)
        self._current_bg = path
        self._rebuild_thumbs()

    def _on_panel_color(self, color):
        self._color = QColor(color)

    def _on_ok(self):
        self.theme_applied.emit(QColor(self._color))
        self.background_changed.emit(self._current_bg, list(self._images))
        self.close()

    def _center_on_parent(self):
        if self.parent() is not None:
            pg = self.parent().geometry()
            self.move(
                pg.x() + (pg.width() - self.width()) // 2,
                pg.y() + (pg.height() - self.height()) // 2,
            )

    # 注意：这里原本有一段 paintEvent，画的是「五角星」，并用到了
    # self._on / self._hover / self.STAR_COLOR_* —— 那些都是 title_bar.py
    # 里收藏星标控件的成员，本类从未定义过（STAR_COLOR_ON 就定义在
    # title_bar.py:704）。属于误粘贴进来的死代码，会导致每次重绘抛
    # AttributeError: 'PersonalizeDialog' object has no attribute '_on'，
    # 个性化窗口因此画不出来（表现为"打不开"）。已删除。
    #
    # 本窗口是 FramelessWindowHint + WA_TranslucentBackground，
    # 外观完全由子控件 self._content（白色圆角 QFrame + 阴影特效）绘制，
    # 自身不需要 paintEvent。

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() < self.SHADOW_MARGIN + 44:
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

    def closeEvent(self, event):
        """关闭时注销语言回调，避免回调引用已销毁的窗口。"""
        try:
            from i18n import off_change
            if self._on_change_cb is not None:
                off_change(self._on_change_cb)
        except Exception:
            pass
        self._on_change_cb = None
        super().closeEvent(event)