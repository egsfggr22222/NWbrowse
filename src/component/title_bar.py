# -*- coding: utf-8 -*-
"""自绘标题栏：菜单、刷新、标签栏切换、地址栏、窗口三键、上/下一个标签。

菜单每次弹出时重建，文字自动取最新的 t(...)，所以 _refresh_texts 是空操作。

pwindow：
  * tabs_btn 弹出唯一的 pwindow。
  * 走 window.create_popup 创建，_popup 挂到 RoundedWindow._popup，
    显隐由 window._refresh_popup_visibility 统一控制。

新增：
  * prev_tab / next_tab 信号：< / > 按钮发出，window 接收切 tab。
  * 两个按钮放在地址栏左侧（menu/reload/tabs 之后）。
  * 只在 browsing_mode 下显示，和 address_bar 同步显隐。

favicon：
  * set_favicon(pixmap) 由 window 推送当前页图标。
  * 画在最左侧（FAVICON_LEFT），menu_btn 左侧。
"""

from loader import *
from theme import Theme
from rounded_menu import RoundedMenu
from personalize_dialog import PersonalizeDialog
from i18n import t

import pinned_store


# ======================================================================
# 滑动开关（自绘）
# ======================================================================
class ToggleSwitch(QWidget):
    """自绘滑动开关。点击切换状态，发出 toggled(bool) 信号。"""

    toggled = pyqtSignal(bool)

    W = 40
    H = 20
    KNOB_MARGIN = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.W, self.H)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._on = False
        self._knob_x = self.KNOB_MARGIN
        self._anim = None

    def is_on(self):
        return self._on

    def set_on(self, on, animate=True, emit=True):
        on = bool(on)
        if on == self._on:
            return
        self._on = on

        target_x = (self.W - self.KNOB_MARGIN * 2
                    - (self.H - self.KNOB_MARGIN * 2))
        if not on:
            target_x = self.KNOB_MARGIN

        if animate:
            self._anim = QPropertyAnimation(self, b"knob_x", self)
            self._anim.setDuration(140)
            self._anim.setStartValue(self._knob_x)
            self._anim.setEndValue(target_x)
            self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
            self._anim.start()
        else:
            self._knob_x = target_x
            self.update()

        if emit:
            self.toggled.emit(on)

    def _get_knob_x(self):
        return self._knob_x

    def _set_knob_x(self, x):
        self._knob_x = x
        self.update()

    knob_x = pyqtProperty(float, _get_knob_x, _set_knob_x)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.set_on(not self._on)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track = QRectF(0, 0, self.W, self.H)
        track_color = QColor(80, 180, 100) if self._on else QColor(170, 170, 170)
        painter.setBrush(track_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(track, self.H / 2, self.H / 2)

        knob_d = self.H - self.KNOB_MARGIN * 2
        knob_rect = QRectF(
            self._knob_x, self.KNOB_MARGIN,
            knob_d, knob_d,
        )
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(QColor(0, 0, 0, 40), 1))
        painter.drawEllipse(knob_rect)


class TitleBar(QFrame):

    HEIGHT = Theme.TOP_BAR_HEIGHT
    BTN_SIZE = Theme.TITLE_BTN_SIZE
    ICON_COLOR = Theme.TITLE_ICON_COLOR
    LABEL_WIDTH = Theme.TITLE_LABEL_WIDTH
    GAP = Theme.TITLE_GAP
    BG_COLOR = Theme.TITLE_BG_COLOR

    ICON_MAX = "□"
    ICON_RESTORE = "⧉"
    ICON_RELOAD = "⟳"
    ICON_LOADING = "⟳"
    ICON_TABS = "☰"
    ICON_PREV = "‹"
    ICON_NEXT = "›"
    ICON_STAR = "★"

    # ---- favicon ----
    FAVICON_SIZE = 20
    FAVICON_LEFT = 12
    # -----------------

    # ---- 新增信号 ----
    prev_tab = pyqtSignal()
    next_tab = pyqtSignal()
    toggle_pin = pyqtSignal(bool)         # 固定开关
    toggle_complete_notify = pyqtSignal(bool)  # 完成提醒开关
    star_left_clicked = pyqtSignal()      # 左键点星：切换收藏
    star_right_clicked = pyqtSignal()     # 右键点星：弹收藏菜单

    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self._drag_start = None
        self._personalize_dialog = None
        self._popup = None                      # 缓存弹窗引用
        self._favicon = None                    # 当前 favicon (QPixmap)

        self.browsing_mode = False
        self._loading = False

        self._btn_font_sizes = {}
        self._icon_color = QColor(self.ICON_COLOR)

        self._pin_switch_state = False

        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setFixedHeight(self.HEIGHT)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self._setup_ui()
        self._relayout()

    def _refresh_texts(self):
        # 菜单每次弹出时重建，文字自动取最新，无需额外刷新
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = 0 if self.parent_window.isMaximized() else self.parent_window.RADIUS
        w, h = self.width(), self.height()

        path = QPainterPath()
        if r <= 0:
            path.addRect(0, 0, w, h)
        else:
            path.moveTo(r, 0)
            path.lineTo(w - r, 0)
            path.arcTo(w - 2 * r, 0, 2 * r, 2 * r, 90, -90)
            path.lineTo(w, h)
            path.lineTo(0, h)
            path.lineTo(0, r)
            path.arcTo(0, 0, 2 * r, 2 * r, 180, -90)
            path.closeSubpath()

        painter.setBrush(self.BG_COLOR)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

        # ---- favicon ----
        if self._favicon is not None:
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
            fx = float(self.FAVICON_LEFT)
            fy = (self.HEIGHT - h_logical) / 2.0
            painter.drawPixmap(QPointF(fx, fy), pm)
        # -----------------

    def _setup_ui(self):
        self.menu_btn = QPushButton("⋯", self)
        self.menu_btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
        self.menu_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_font_sizes[self.menu_btn] = 30
        self.menu_btn.clicked.connect(self._show_menu)

        self.reload_btn = QPushButton(self.ICON_RELOAD, self)
        self.reload_btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
        self.reload_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_font_sizes[self.reload_btn] = 22
        self.reload_btn.clicked.connect(self._on_reload)

        self.tabs_btn = QPushButton(self.ICON_TABS, self)
        self.tabs_btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
        self.tabs_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_font_sizes[self.tabs_btn] = 16
        self.tabs_btn.clicked.connect(self._on_tabs)

        # ---- 新增：< / > ----
        self.prev_btn = QPushButton(self.ICON_PREV, self)
        self.prev_btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
        self.prev_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_font_sizes[self.prev_btn] = 22
        self.prev_btn.clicked.connect(self._on_prev_tab)

        self.next_btn = QPushButton(self.ICON_NEXT, self)
        self.next_btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
        self.next_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_font_sizes[self.next_btn] = 22
        self.next_btn.clicked.connect(self._on_next_tab)
        # ---------------------

        # ---- 收藏星按钮 ----
        self.star_btn = _StarButton(self)
        self.star_btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
        self.star_btn.left_clicked.connect(self.star_left_clicked.emit)
        self.star_btn.right_clicked.connect(self.star_right_clicked.emit)
        # --------------------

        self.address_bar = QLineEdit(self)
        self.address_bar.setFixedHeight(Theme.ADDRESS_BAR_HEIGHT)
        self.address_bar.setStyleSheet(
            "QLineEdit {"
            "  background: white;"
            f"  border-radius: {Theme.ADDRESS_BAR_RADIUS}px;"
            "  border: 1px solid #cccccc;"
            "  padding: 0 10px;"
            "  color: #333333;"
            "  font-size: 13px;"
            "}"
            "QLineEdit:focus {"
            "  border: 1px solid #7aa7f0;"
            "}"
        )
        self.address_bar.returnPressed.connect(self._on_address_submit)

        self.min_btn = QPushButton("−", self)
        self.max_btn = QPushButton(self.ICON_MAX, self)
        self.close_btn = QPushButton("×", self)
        for btn, slot in (
            (self.min_btn, self._on_min),
            (self.max_btn, self._on_max),
            (self.close_btn, self._on_close),
        ):
            btn.setFixedSize(self.BTN_SIZE, self.BTN_SIZE)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self._btn_font_sizes[btn] = 15
            btn.clicked.connect(slot)

        self.refresh_button_styles()

    def _derive_icon_color(self):
        base = QColor(self.BG_COLOR)
        return QColor(255 - base.red(), 255 - base.green(), 255 - base.blue())

    def _derive_hover_colors(self):
        base = QColor(self.BG_COLOR)
        h, s, v, a = base.getHsv()
        hover = QColor.fromHsv(h, s, max(0, v - 22), a)
        pressed = QColor.fromHsv(h, s, max(0, v - 38), a)
        return hover, pressed

    def refresh_button_styles(self):
        self._icon_color = self._derive_icon_color()
        hover, pressed = self._derive_hover_colors()
        icon = self._icon_color.name()

        for btn, size in self._btn_font_sizes.items():
            btn.setStyleSheet(
                "QPushButton {"
                f"  color: {icon};"
                "  background: transparent;"
                "  border: none;"
                f"  font-size: {size}px;"
                "}"
                "QPushButton:hover {"
                f"  background: {hover.name()};"
                "  border-radius: 8px;"
                "}"
                "QPushButton:pressed {"
                f"  background: {pressed.name()};"
                "  border-radius: 8px;"
                "}"
            )

    def _relayout(self):
        y = (self.HEIGHT - self.BTN_SIZE) // 2
        gap = self.GAP

        # ---- favicon 让位 ----
        x = self.FAVICON_LEFT + self.FAVICON_SIZE + gap
        # ----------------------
        self.menu_btn.move(x, y)
        x += self.BTN_SIZE + gap
        self.reload_btn.move(x, y)
        x += self.BTN_SIZE + gap
        self.tabs_btn.move(x, y)
        x += self.BTN_SIZE + gap

        # ---- 新增：< / > ----
        self.prev_btn.move(x, y)
        x += self.BTN_SIZE + gap
        self.next_btn.move(x, y)
        x += self.BTN_SIZE + gap

        # ---- 收藏星 ----
        self.star_btn.move(x, y)
        x += self.BTN_SIZE + gap
        # ---------------

        right_reserved = self.BTN_SIZE * 3 + 16 + gap * 2

        addr_x = x + gap
        addr_w = self.width() - addr_x - right_reserved - gap
        if addr_w < Theme.ADDRESS_BAR_MIN_WIDTH:
            addr_w = Theme.ADDRESS_BAR_MIN_WIDTH
        addr_y = (self.HEIGHT - Theme.ADDRESS_BAR_HEIGHT) // 2
        self.address_bar.setGeometry(
            addr_x, addr_y, addr_w, Theme.ADDRESS_BAR_HEIGHT
        )

        self.close_btn.move(self.width() - self.BTN_SIZE - 16, y)
        self.max_btn.move(self.width() - self.BTN_SIZE * 2 - 16 - gap, y)
        self.min_btn.move(self.width() - self.BTN_SIZE * 3 - 16 - gap * 2, y)

        if self.browsing_mode:
            self.address_bar.show()
            self.reload_btn.show()
            self.tabs_btn.show()
            self.prev_btn.show()
            self.next_btn.show()
            self.star_btn.show()
        else:
            self.address_bar.hide()
            self.reload_btn.hide()
            self.tabs_btn.hide()
            self.prev_btn.hide()
            self.next_btn.hide()
            self.star_btn.hide()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._relayout()

    def set_browsing_mode(self, browsing):
        self.browsing_mode = browsing
        self._relayout()

    def set_engine_mode(self, engine):
        pass

    def set_loading(self, loading):
        if loading == self._loading:
            return
        self._loading = loading
        self.reload_btn.setText(
            self.ICON_LOADING if loading else self.ICON_RELOAD
        )

    def set_address(self, url):
        if url:
            self.address_bar.setText(url)

    def set_favicon(self, pixmap):
        self._favicon = (
            pixmap if (pixmap is not None and not pixmap.isNull()) else None
        )
        self.update()

    def update_history_label(self, position):
        pass

    def update_max_icon(self):
        if self.parent_window.isMaximized():
            self.max_btn.setText(self.ICON_RESTORE)
        else:
            self.max_btn.setText(self.ICON_MAX)

    def apply_theme_color(self, color):
        self.BG_COLOR = QColor(color)
        self.refresh_button_styles()
        self.update()

    # ---------------- 菜单 ----------------
    def _show_menu(self):
        menu = RoundedMenu(self)
        act_personalize = menu.addAction(t("menu.personalize"))
        act_settings = menu.addAction(t("menu.settings"))
        act_downloads = menu.addAction(t("menu.downloads"))

        # ---- 固定开关行（有 host 才显示）----
        host = self._current_pin_host()
        if host:
            menu.addSeparator()

            row_widget = QWidget()
            row_widget.setStyleSheet("background: transparent;")
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(16, 6, 16, 6)
            row_layout.setSpacing(12)

            lbl = QLabel(t("menu.pin"))
            lbl.setStyleSheet("color: #333333; font-size: 13px;")
            row_layout.addWidget(lbl)
            row_layout.addStretch(1)

            sw = ToggleSwitch(row_widget)
            try:
                sw.set_on(pinned_store.is_pinned(host),
                          animate=False, emit=False)
            except Exception:
                pass
            sw.toggled.connect(self._on_pin_switch_toggled)
            row_layout.addWidget(sw)

            act = QWidgetAction(menu)
            act.setDefaultWidget(row_widget)
            menu.addAction(act)
        # ------------------------------------

        # ---- 完成提醒开关行（有 host 才显示）----
        if host:
            row_widget2 = QWidget()
            row_widget2.setStyleSheet("background: transparent;")
            row_layout2 = QHBoxLayout(row_widget2)
            row_layout2.setContentsMargins(16, 6, 16, 6)
            row_layout2.setSpacing(12)

            lbl2 = QLabel(t("menu.complete_notify"))
            lbl2.setStyleSheet("color: #333333; font-size: 13px;")
            row_layout2.addWidget(lbl2)
            row_layout2.addStretch(1)

            sw2 = ToggleSwitch(row_widget2)
            try:
                sw2.set_on(bool(getattr(self.parent_window,
                                        "_complete_notify_on", False)),
                           animate=False, emit=False)
            except Exception:
                pass
            sw2.toggled.connect(self._on_complete_notify_toggled)
            row_layout2.addWidget(sw2)

            act2 = QWidgetAction(menu)
            act2.setDefaultWidget(row_widget2)
            menu.addAction(act2)
        # -------------------------------------------

        act_personalize.triggered.connect(self._open_personalize)
        act_settings.triggered.connect(self._open_settings)
        act_downloads.triggered.connect(self._open_downloads)

        pos = self.menu_btn.mapToGlobal(self.menu_btn.rect().bottomLeft())
        menu.exec(pos)

    def _current_pin_host(self):
        """取父窗口当前主域（作为固定 key）。没有就返回空。"""
        try:
            win = self.parent_window
            url = getattr(win, "_current_url", "") or ""
            if not url:
                return ""
            from urllib.parse import urlparse
            h = (urlparse(url).hostname or "").lower()
            if not h:
                return ""
            parts = h.split(".")
            if len(parts) <= 2:
                return h
            return ".".join(parts[-2:])
        except Exception:
            return ""

    def _on_pin_switch_toggled(self, on):
        """固定开关被用户点击。"""
        self.toggle_pin.emit(bool(on))

    def _on_complete_notify_toggled(self, on):
        """完成提醒开关被用户点击。"""
        self.toggle_complete_notify.emit(bool(on))

    def set_pin_switch_state(self, on):
        """供 window 调用：同步开关视觉状态（不触发 toggled）。

        注意：因为开关是临时构建在菜单里的，菜单关闭就销毁，
        所以这里只更新一个缓存值，供下次 _show_menu 时初始化。
        """
        self._pin_switch_state = bool(on)

    # ---------------- 弹窗（tabs_btn） ----------------
    def _on_tabs(self):
        """弹出 pwindow。走 window.create_popup，显隐由 window 统一管。"""
        win = self.parent_window

        try:
            if hasattr(win, "create_popup"):
                # 走 window：pwindow 挂到 RoundedWindow._popup
                self._popup = win.create_popup(title="弹窗")
            else:
                # 兜底：父窗口不是 RoundedWindow
                from popup_window import PopupWindow
                self._popup = PopupWindow(parent=win, title="弹窗")
        except Exception as e:
            print("[title_bar] 打开弹窗失败:", e)
            return

        try:
            self._popup.show()
            self._popup.raise_()
            self._popup.activateWindow()
        except RuntimeError:
            self._popup = None
            self._on_tabs()

    # ---------------- tab 切换 ----------------
    def _on_prev_tab(self):
        self.prev_tab.emit()

    def _on_next_tab(self):
        self.next_tab.emit()

    # ---------------- 其它 ----------------
    def _open_personalize(self):
        if self._personalize_dialog is not None:
            try:
                self._personalize_dialog.show()
                self._personalize_dialog.raise_()
                self._personalize_dialog.activateWindow()
                return
            except RuntimeError:
                self._personalize_dialog = None

        win = self.parent_window
        dlg = PersonalizeDialog(
            win.current_theme_color(),
            win.current_background_images(),
            win.current_background_image(),
            win,
        )
        dlg.theme_applied.connect(win.apply_personalize)
        dlg.background_changed.connect(win.apply_background_image)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()
        self._personalize_dialog = dlg

    def _open_settings(self):
        """通知托盘打开设置进程。"""
        try:
            from ipc import IpcClient, ROLE_TRAY, MSG_OPEN_SETTINGS
            IpcClient.send_to_role(ROLE_TRAY, MSG_OPEN_SETTINGS)
        except Exception as e:
            print("[title_bar] 请求打开设置失败:", e)

    def _open_downloads(self):
        """通知托盘打开下载进程。"""
        try:
            from ipc import IpcClient, ROLE_TRAY, MSG_OPEN_DOWNLOADS
            IpcClient.send_to_role(ROLE_TRAY, MSG_OPEN_DOWNLOADS)
        except Exception as e:
            print("[title_bar] 请求打开下载失败:", e)

    def _restart_window(self):
        try:
            self.parent_window.restart_web_view()
        except Exception as e:
            print("[title_bar] 重启失败:", e)

    def _on_reload(self):
        try:
            self.parent_window.web_view.reload()
        except Exception:
            pass

    def _on_address_submit(self):
        text = self.address_bar.text().strip()
        if text:
            self.parent_window.visit_url(text)

    def _on_min(self):
        if hasattr(self.parent_window, "minimize_or_offscreen"):
            self.parent_window.minimize_or_offscreen()
        else:
            self.parent_window.showMinimized()

    def _on_max(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()

    def _on_close(self):
        self.parent_window.close()

    # ---------------- 光标 ----------------
    def _set_cursor_for_edge(self, edge):
        if edge in ("l", "r"):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge in ("t", "b"):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif edge in ("lt", "rb"):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in ("rt", "lb"):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    # ---------------- 拖拽 ----------------
    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return

        win = self.parent_window
        global_pos = event.globalPosition().toPoint()
        win_pos = win.mapFromGlobal(global_pos)
        edge = win._get_edge(win_pos)
        if edge:
            win._resize_edge = edge
            win._start_pos = global_pos
            win._start_geo = win.geometry()
            event.accept()
            return

        if win.isMaximized():
            local_pos = event.position().toPoint()
            local_x = local_pos.x()
            local_y = local_pos.y()
            old_width = self.width()

            win.showNormal()

            new_w = win.width()
            ratio = local_x / max(1, old_width)
            target_x = global_pos.x() - int(new_w * ratio)
            target_y = global_pos.y() - local_y

            win.move(target_x, target_y)
            self._drag_start = global_pos - win.pos()
            return

        self._drag_start = global_pos - win.pos()

    def mouseMoveEvent(self, event):
        win = self.parent_window
        global_pos = event.globalPosition().toPoint()
        win_pos = win.mapFromGlobal(global_pos)
        edge = win._get_edge(win_pos)
        self._set_cursor_for_edge(edge)

        if win._resize_edge is not None and win._start_geo is not None:
            win.mouseMoveEvent(event)
            return

        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_start is not None:
            win.move(event.globalPosition().toPoint() - self._drag_start)

    def mouseReleaseEvent(self, event):
        win = self.parent_window
        if win._resize_edge is not None:
            win.mouseReleaseEvent(event)
            return
        self._drag_start = None

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._on_max()


class _StarButton(QPushButton):
    """自绘五角星按钮。白色 = 未收藏，蓝色 = 已收藏。"""

    STAR_COLOR_ON = QColor(60, 140, 230)    # 已收藏：蓝
    STAR_COLOR_OFF = QColor(255, 255, 255)  # 未收藏：白
    STAR_BORDER = QColor(100, 100, 100, 160)  # 白星的细描边

    left_clicked = pyqtSignal()
    right_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._on = False
        self._hover = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")
        self.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(
            lambda _pos: self.right_clicked.emit()
        )

    def set_on(self, on):
        on = bool(on)
        if on != self._on:
            self._on = on
            self.update()

    def is_on(self):
        return self._on

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.left_clicked.emit()
            event.accept()
            return
        # 右键由 customContextMenuRequested 处理
        super().mousePressEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2.0, h / 2.0
        outer_r = min(w, h) * 0.36
        inner_r = outer_r * 0.42

        # 五角星路径
        import math
        path = QPainterPath()
        for i in range(10):
            r = outer_r if i % 2 == 0 else inner_r
            angle = -math.pi / 2 + i * math.pi / 5
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()

        if self._on:
            fill = self.STAR_COLOR_ON
            painter.setPen(Qt.PenStyle.NoPen)
        else:
            fill = self.STAR_COLOR_OFF
            pen = QPen(self.STAR_BORDER)
            pen.setWidthF(1.0)
            painter.setPen(pen)

        if self._hover:
            painter.setOpacity(0.75)
        else:
            painter.setOpacity(1.0)

        painter.setBrush(fill)
        painter.drawPath(path)
        painter.setOpacity(1.0)