# -*- coding: utf-8 -*-
"""无痕窗口：继承 window.RoundedWindow，颜色完全独立。

- 不读 settings.json 的主题/背景
- 边框固定渐变：紫 #6a0dad → 酒红 #722f37（左上→右下）
- 网页区：边框渐变的"提亮+降饱和"版，比边框浅
- 白字、白描边
- 强制 incognito=True
- 菜单去掉『个性化』
- host 路由全部放行：任何 URL 都本窗口加载，不通知 bar，bar 也查不到它
- popup 用 IncognitoPopupWindow（半透明渐变）
- popup 记录所有 URL（因为父类的 _poll_url_once 用 _has_root_host 过滤，
  无痕下永远 True，所以全记）

进程独立：floating_bar 用 QProcess 起本文件。
不改 window.py。
"""

import sys
import os
import argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *

from theme import Theme
from title_bar import TitleBar
from i18n import load as i18n_load

from window import (
    RoundedWindow,
    set_topmost,
    INIT_SCRIPT,
    _clean_js_url,
    _pretty_url_for_address_bar,
)


# ======================================================================
# 无痕配色
# ======================================================================
GRAD_TOP_LEFT     = QColor("#6a0dad")
GRAD_BOTTOM_RIGHT = QColor("#722f37")

OUTLINE_COLOR     = QColor("#ffffff")
OUTLINE_ALPHA     = 200

TITLE_ICON_COLOR  = "#ffffff"

ADDR_BG           = "rgba(255,255,255,0.12)"
ADDR_TEXT         = "#ffffff"
ADDR_BORDER       = "rgba(255,255,255,0.45)"

CORNER_MASK_COLOR = QColor("#6a0dad")


def _lighten_for_web(color, dS=0.50, dV=0.25):
    h, s, v, a = color.getHsvF()
    s2 = max(0.0, s * (1.0 - dS))
    v2 = min(1.0, v + dV)
    return QColor.fromHsvF(h, s2, v2, a)


class IncognitoWindow(RoundedWindow):
    """无痕窗口。"""

    def __init__(self, mode="default", window_id="ig-0",
                 host="", start_url=""):
        super().__init__(
            mode=mode,
            window_id=window_id,
            host=host,
            start_url=start_url,
        )
    def _apply_favicon(self):
        """无痕窗口：标题栏/popup 用 favicon，但窗口图标不变。"""
        if hasattr(self, "title_bar"):
            self.title_bar.set_favicon(self._favicon_pixmap)
        if self._popup is not None:
            self._popup.set_favicon(self._favicon_pixmap)
        # 不调 apply_icon_to_window —— 窗口图标保持默认

    def _reset_favicon(self, url=""):
        """无痕窗口：清 favicon，但窗口图标保持默认。"""
        self._favicon_pixmap = None
        if hasattr(self, "title_bar"):
            self.title_bar.set_favicon(None)
        if self._popup is not None:
            self._popup.set_favicon(None)
        # 不调 apply_icon_to_window —— 窗口图标保持默认
    # ==========================================================
    # popup：用 IncognitoPopupWindow
    # ==========================================================
    def create_popup(self, title="弹窗"):
        if self._popup is None:
            from inc_p_window import IncognitoPopupWindow
            self._popup = IncognitoPopupWindow(parent=self, title=title)
            self._popup.url_selected.connect(self._on_popup_url_selected)
            self._popup.url_closed.connect(self._on_popup_url_closed)
            self._popup.destroyed.connect(self._on_popup_destroyed)
            self._popup.set_favicon(self._favicon_pixmap)
        return self._popup

    # ==========================================================
    # host 路由：全部放行，不通知 bar
    # ==========================================================
    def _add_host(self, host, primary=False):
        """无痕窗口不记 host。"""
        pass

    def _has_root_host(self, host):
        return True

    def _matches_host(self, host):
        return True

    def _is_related_host(self, new_host):
        return True

    def request_url(self, url):
        """无痕窗口不通知 bar，自己加载。"""
        if url:
            self._do_load(url)

    def _on_navigation(self, url):
        """无痕窗口不拦导航。"""
        return True

    def _on_url_settled(self):
        """无痕窗口：URL 稳定后只更新地址栏和 popup，不做路由。

        避免父类逻辑里 find_window_by_host 命中后 self.close()。
        """
        wv = self.web_view
        if wv is None:
            return

        def _cb(real_url):
            try:
                url_str = _clean_js_url(real_url)
                if not url_str or url_str == "about:blank":
                    return
                if not url_str.startswith(
                        ("http://", "https://", "file://")):
                    return

                self._current_url = url_str
                self.title_bar.set_address(
                    _pretty_url_for_address_bar(url_str)
                )

                if self._popup is not None:
                    self._popup.append_url(url_str)
                    self._popup.set_current_url(url_str)
            except Exception as e:
                print(f"[incognito] _on_url_settled 回调异常: {e}")

        try:
            wv.eval_js("location.href", _cb)
        except Exception as e:
            print(f"[incognito] _on_url_settled eval_js 失败: {e}")

    # ==========================================================
    # 创建 WebView：强制 incognito=True
    # ==========================================================
    def _create_web_view(self):
        from qtwebview2 import QtWebViewWidget
        from settings_backend import SettingsBackend

        backend = SettingsBackend()

        kwargs = {
            "native_child": True,
            "lazyload": True,
            "debug": True,
            "initialization_script": INIT_SCRIPT,
            "download_started_handler": self._on_download_started,
            "download_completed_handler": self._on_download_completed,
            "new_window_handler": self._on_new_window,
            "navigation_handler": self._on_navigation,
            "parent": self,
            "incognito": True,
        }

        ua = backend.get_user_agent()
        if ua:
            kwargs["user_agent"] = ua

        # 无痕窗口不传 user_data_folder

        try:
            wv = QtWebViewWidget(**kwargs)
        except TypeError as e:
            print("[incognito] 创建 web_view 参数不被支持:", e)
            wv = QtWebViewWidget(
                native_child=True,
                lazyload=False,
                initialization_script=INIT_SCRIPT,
                parent=self,
            )

        try:
            wv.signals.web_message_received.connect(self._on_js_message)
        except Exception as e:
            print("[incognito] 接 web_message_received 失败:", e)

        try:
            wv.signals.title_changed.connect(self._on_title_changed)
        except Exception as e:
            print("[incognito] 接 title_changed 失败:", e)

        try:
            wv.signals.favicon_changed.connect(self._on_favicon_changed)
            self._has_favicon_signal = True
        except Exception as e:
            print("[incognito] 无 favicon_changed 信号，用 JS 兜底:", e)

        wv.hide()
        wv.setGeometry(0, 0, 0, 0)
        self._web_view = wv

    # ==========================================================
    # 颜色 / 背景：不读 settings
    # ==========================================================
    def _apply_saved_theme(self):
        Theme.apply_theme(GRAD_TOP_LEFT)
        TitleBar.BG_COLOR = QColor(0, 0, 0, 0)
        TitleBar.ICON_COLOR = TITLE_ICON_COLOR

    def _load_saved_background(self):
        self._bg_path = ""
        self._bg_pixmap = None

    def _reload_config(self):
        pass

    def apply_personalize(self, color):
        pass

    def apply_background_image(self, path, images=None):
        pass

    def current_theme_color(self):
        return QColor(GRAD_TOP_LEFT)

    def current_background_images(self):
        return []

    def current_background_image(self):
        return ""

    # ==========================================================
    # 标题栏：改色 + 菜单去个性化
    # ==========================================================
    def _setup_title_bar(self):
        super()._setup_title_bar()

        tb = self.title_bar
        tb.BG_COLOR = QColor(0, 0, 0, 0)
        tb.ICON_COLOR = TITLE_ICON_COLOR

        try:
            tb._icon_color = QColor(TITLE_ICON_COLOR)
            tb.refresh_button_styles()
        except Exception:
            pass

        try:
            tb.address_bar.setStyleSheet(
                "QLineEdit {"
                f"  background: {ADDR_BG};"
                f"  border-radius: {Theme.ADDRESS_BAR_RADIUS}px;"
                f"  border: 1px solid {ADDR_BORDER};"
                "  padding: 0 10px;"
                f"  color: {ADDR_TEXT};"
                "  font-size: 13px;"
                "}"
                f"QLineEdit:focus {{ border: 1px solid {ADDR_TEXT}; }}"
            )
        except Exception:
            pass

        # 替换菜单方法 + 重连信号
        tb._show_menu = self._incognito_show_menu
        try:
            tb.menu_btn.clicked.disconnect()
        except Exception:
            pass
        tb.menu_btn.clicked.connect(self._incognito_show_menu)

    def _incognito_show_menu(self):
        """无痕窗口菜单：无『个性化』。"""
        from rounded_menu import RoundedMenu
        from i18n import t

        tb = self.title_bar
        menu = RoundedMenu(tb)
        act_settings = menu.addAction(t("menu.settings"))
        act_downloads = menu.addAction(t("menu.downloads"))

        act_settings.triggered.connect(tb._open_settings)
        act_downloads.triggered.connect(tb._open_downloads)

        pos = tb.menu_btn.mapToGlobal(tb.menu_btn.rect().bottomLeft())
        menu.exec(pos)

    # ==========================================================
    # 角落遮罩
    # ==========================================================
    def _setup_corner_mask(self):
        super()._setup_corner_mask()
        try:
            self.corner_mask.bg_color = CORNER_MASK_COLOR
            self.corner_mask.update()
        except Exception:
            pass

    # ==========================================================
    # 描边
    # ==========================================================
    def _outline_color(self):
        c = QColor(OUTLINE_COLOR)
        c.setAlpha(OUTLINE_ALPHA)
        return c

    # ==========================================================
    # 绘制
    # ==========================================================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        b = self.BORDER
        radius = 0 if self.isMaximized() else self.RADIUS

        grad_rect = QRectF(self.rect())
        grad = QLinearGradient(
            grad_rect.topLeft(),
            grad_rect.bottomRight(),
        )
        grad.setColorAt(0.0, GRAD_TOP_LEFT)
        grad.setColorAt(1.0, GRAD_BOTTOM_RIGHT)

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), radius, radius)

        outline = QColor(OUTLINE_COLOR)
        outline.setAlpha(OUTLINE_ALPHA)
        painter.setPen(QPen(outline, b))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(
            QRectF(
                b / 2.0, b / 2.0,
                self.width() - b,
                self.height() - b,
            ),
            radius, radius,
        )

        try:
            x = self.SIDE_MARGIN + b
            y = self.TOP_BAR_HEIGHT + self.WEB_TOP_GAP + b
            w = self.width() - 2 * self.SIDE_MARGIN - 2 * b
            h = self.height() - y - self.BOTTOM_MARGIN - b
            if w <= 0 or h <= 0:
                return

            rect = QRectF(x, y, w, h)
            web_c1 = _lighten_for_web(GRAD_TOP_LEFT)
            web_c2 = _lighten_for_web(GRAD_BOTTOM_RIGHT)

            web_grad = QLinearGradient(
                rect.topLeft(),
                rect.bottomRight(),
            )
            web_grad.setColorAt(0.0, web_c1)
            web_grad.setColorAt(1.0, web_c2)

            painter.setBrush(QBrush(web_grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(rect, self.WEB_RADIUS, self.WEB_RADIUS)
        except RuntimeError:
            pass


# ======================================================================
# 入口
# ======================================================================
def main():
    import traceback

    def _excepthook(exc_type, exc_value, exc_tb):
        traceback.print_exception(exc_type, exc_value, exc_tb)

    sys.excepthook = _excepthook

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="default",
                        choices=["default", "search", "custom"])
    parser.add_argument("--id", default="ig-0")
    parser.add_argument("--host", default="")
    parser.add_argument("--url", default="")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 应用默认图标（任务栏兜底）
    try:
        from window_icon import default_icon
        _di = default_icon()
        if not _di.isNull():
            app.setWindowIcon(_di)
    except Exception as e:
        print("[incognito] 设应用图标失败:", e)

    try:
        from settings_backend import SettingsBackend
        i18n_load(SettingsBackend().get_language())
    except Exception as e:
        print("[incognito] 加载语言失败:", e)

    # 任务栏分开：本进程独立 AppUserModelID
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            f"MyBrowser.Incognito.{args.id}"
        )
    except Exception as e:
        print("[incognito] 设置 AppUserModelID 失败:", e)

    w = IncognitoWindow(
        mode=args.mode,
        window_id=args.id,
        host=args.host,
        start_url=args.url,
    )

    # 窗口默认图标
    try:
        from window_icon import default_icon
        _di = default_icon()
        if not _di.isNull():
            w.setWindowIcon(_di)
    except Exception as e:
        print("[incognito] 设窗口默认图标失败:", e)

    w.show()

    def _bring_to_front():
        try:
            w.raise_()
            w.activateWindow()
            set_topmost(int(w.winId()), True)
            QTimer.singleShot(800, lambda: set_topmost(int(w.winId()), False))
        except Exception as e:
            print("[incognito] bring_to_front 失败:", e)

    QTimer.singleShot(300, _bring_to_front)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()