# -*- coding: utf-8 -*-
"""居中输入框组件：半透明背景、随内容自动增高、回车提交、Esc 清除、右侧放大镜按钮。"""

from loader import *
import apppaths
from theme import Theme

import math
import os


_APP_FONTS_READY = False


def _ensure_app_fonts():
    global _APP_FONTS_READY
    if _APP_FONTS_READY:
        return
    _APP_FONTS_READY = True
    try:
        from loader import load_app_fonts
        load_app_fonts()
    except Exception:
        pass


INPUT_FONT_STACK = (
    "'MiSans', "
    "'Microsoft YaHei UI', 'Microsoft YaHei', "
    "'PingFang SC', 'Noto Sans CJK SC', "
    "sans-serif"
)


class MagnifierButton(QPushButton):
    """自绘放大镜按钮：一个圆 + 一根斜手柄，整体居中，悬停时出现阴影。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("background: transparent; border: none;")

        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(0)
        self._shadow.setOffset(0, 0)
        self._shadow.setColor(QColor(0, 0, 0, 0))
        self.setGraphicsEffect(self._shadow)

    def enterEvent(self, event):
        self._shadow.setBlurRadius(12)
        self._shadow.setOffset(0, 1)
        self._shadow.setColor(QColor(0, 0, 0, 110))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._shadow.setBlurRadius(0)
        self._shadow.setOffset(0, 0)
        self._shadow.setColor(QColor(0, 0, 0, 0))
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        pen = QPen(QColor("#666666"))
        pen.setWidthF(1.4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        r = min(w, h) * 0.22
        k = r * math.cos(math.pi / 4)
        handle_len = r * 1.7

        # 圆心相对按钮中心向左上补偿，使「圆+手柄」整体居中
        cx = w / 2 - handle_len * 0.18
        cy = h / 2 - handle_len * 0.7

        painter.drawEllipse(QPointF(cx, cy), r, r)

        x1 = cx + k
        y1 = cy + k
        x2 = cx + handle_len * math.cos(math.pi / 4) + k
        y2 = cy + handle_len * math.sin(math.pi / 4) + k
        painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))


def _load_app_icon_pm(size=128):
    """读 data/icon.ico，返回一张 QPixmap。

    为什么要用 QIcon 而不是 QPixmap 直接读：
        `QPixmap("x.ico")` 取的是 ICO 里的**第一帧**，不是最大帧。
        如果哪天 ICO 被换成多尺寸且小尺寸排在最前，这里就会拿到 16x16，
        再放大到 22px 就发糊（曾经真的踩过）。
        `QIcon(path).pixmap(w, h)` 会按请求尺寸挑最合适的一帧，稳。
    """
    try:
        path = os.path.join(apppaths.RES_DIR, "data", "icon.ico")
        if not os.path.isfile(path):
            return None
        pm = QIcon(path).pixmap(size, size)
        if pm.isNull():
            pm = QPixmap(path)
        return pm if not pm.isNull() else None
    except Exception:
        return None


class EngineIconButton(QPushButton):
    """输入框左侧的引擎图标按钮。

    默认显示 data/icon.ico；
    选了引擎后，优先显示 favicon（set_pixmap），没 favicon 则显示字母（set_abbr）。
    """

    ICON_SIZE = 22

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._abbr = ""
        self._pm = None              # 引擎 favicon
        self._default_pm = None
        self._hover = False

        self.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

        # 默认图标
        try:
            pm = _load_app_icon_pm(128)
            if pm is not None:
                self._default_pm = pm
        except Exception:
            pass

    def set_abbr(self, abbr):
        """设置引擎缩写（大写 2 字母）。空字符串 = 恢复默认图标。"""
        abbr = (abbr or "").upper()
        if abbr != self._abbr:
            self._abbr = abbr
            self.update()

    def set_pixmap(self, pm):
        """设置 favicon。传 None 清掉。"""
        if pm is not None and pm.isNull():
            pm = None
        self._pm = pm
        self.update()

    def abbr(self):
        return self._abbr

    def clear_engine(self):
        """回到默认图标状态。"""
        self._abbr = ""
        self._pm = None
        self.update()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        w = self.width()
        h = self.height()
        size = min(w, h)
        dpr = self.devicePixelRatioF()

        # 圆角矩形裁切区
        radius = size * 0.28
        rect = QRectF(
            (w - size) / 2.0,
            (h - size) / 2.0,
            float(size),
            float(size),
        )
        clip = QPainterPath()
        clip.addRoundedRect(rect, radius, radius)
        painter.setClipPath(clip)

        if self._hover:
            painter.setOpacity(0.7)
        else:
            painter.setOpacity(1.0)

        # 优先级：favicon > 字母 > 默认图标
        if self._pm is not None and not self._pm.isNull():
            px = max(1, int(size * dpr))
            pm = self._pm.scaled(
                px, px,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            pm.setDevicePixelRatio(dpr)
            x = (w - pm.width() / dpr) / 2.0
            y = (h - pm.height() / dpr) / 2.0
            painter.drawPixmap(QPointF(x, y), pm)

        elif self._abbr:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(90, 90, 120))
            painter.drawRoundedRect(rect, radius, radius)

            font = painter.font()
            font.setPointSizeF(max(8.0, size * 0.42))
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(
                rect,
                Qt.AlignmentFlag.AlignCenter,
                self._abbr,
            )
        elif self._default_pm is not None and not self._default_pm.isNull():
            px = max(1, int(size * dpr))
            pm = self._default_pm.scaled(
                px, px,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            pm.setDevicePixelRatio(dpr)
            x = (w - pm.width() / dpr) / 2.0
            y = (h - pm.height() / dpr) / 2.0
            painter.drawPixmap(QPointF(x, y), pm)

        painter.setOpacity(1.0)
        painter.setClipping(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
            event.accept()
            return
        super().mousePressEvent(event)


class EnginePicker(QWidget):
    """透明长条：竖排引擎图标，宽 60，高 2 图标+间距。点图标发 selected(url)。"""

    WIDTH = 32          # 宽度（约等于按钮宽度）
    ICON_SIZE = 22      # 图标尺寸（和左侧按钮一致）
    GAP = 4
    PAD = 4
    RADIUS = 8

    selected = pyqtSignal(dict)   # {"abbr": ..., "url": ...}

    def __init__(self, engines, parent=None):
        super().__init__(parent)
        self._engines = list(engines or [])

        # 子控件：不要窗口标志，就画在 window 内部
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 高度 = 2.5 个图标 + 间距 + padding
        visible_count = min(4, max(1, len(self._engines)))
        full = int(visible_count)
        frac = visible_count - full
        h = (
            self.PAD * 2
            + full * self.ICON_SIZE
            + max(0, full - 1) * self.GAP
            + int(frac * self.ICON_SIZE)
        )
        self.setFixedSize(
            self.WIDTH,
            max(h, self.ICON_SIZE + self.PAD * 2),
        )

        self._items = []
        self._picking = False        # 正在点击图标，抑制失焦关
        self._build_ui()

        if len(self._engines) > 2:
            self.setToolTip("滚轮查看更多")

    def _build_ui(self):
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        self._scroll.viewport().setStyleSheet("background: transparent;")
        self._scroll.viewport().setContentsMargins(0, 0, 0, 0)
        self._scroll.setGeometry(
            self.PAD, self.PAD,
            self.WIDTH - self.PAD * 2,
            self.height() - self.PAD * 2,
        )

        host = QWidget()
        host.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(host)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.GAP)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch(1)

        self._items = []
        for eng in self._engines:
            btn = _EnginePickerItem(eng, host)
            btn.clicked.connect(
                lambda e=eng: self._on_item_clicked(e)
            )
            idx = layout.count() - 1
            layout.insertWidget(idx, btn)
            self._items.append(btn)

        self._scroll.setWidget(host)

    def paintEvent(self, event):
        # 完全透明：不画背景、不画描边
        pass

    def set_item_favicon(self, url, pm):
        """按 url 找到对应 item，设它的 favicon。"""
        if not url:
            return
        for item in self._items:
            eng = getattr(item, "_engine", None)
            if isinstance(eng, dict) and eng.get("url") == url:
                try:
                    item.set_pixmap(pm)
                except Exception:
                    pass
                return

    def wheelEvent(self, event):
        try:
            self._scroll.wheelEvent(event)
            return
        except Exception:
            pass
        super().wheelEvent(event)

    def popup_at(self, global_pos):
        """在 global_pos（全局 QPoint）显示。"""
        self.move(global_pos)
        self.show()
        self.raise_()
        self.activateWindow()

    def close_picker(self):
        self.hide()
        self.deleteLater()

    def _on_item_clicked(self, engine):
        """点图标：发 selected。"""
        self.selected.emit(engine)


class _EnginePickerItem(QPushButton):
    """长条里的单个引擎图标。优先显示 favicon，没有就显示字母。"""

    clicked = pyqtSignal()

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self._engine = engine
        self._is_default = bool(engine.get("_default"))
        self._abbr = (engine.get("abbr") or "??").upper()
        self._pm = None              # favicon
        self._default_pm = None      # data/icon.ico
        self._hover = False

        size = EnginePicker.ICON_SIZE
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

        if self._is_default:
            # 读 data/icon.ico
            try:
                pm = _load_app_icon_pm(128)
                if pm is not None:
                    self._default_pm = pm
            except Exception:
                pass

    def set_pixmap(self, pm):
        """设置 favicon。传 None 清掉。"""
        if pm is not None and pm.isNull():
            pm = None
        self._pm = pm
        self.update()

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        w = self.width()
        h = self.height()
        size = min(w, h)
        dpr = self.devicePixelRatioF()
        radius = size * 0.28
        rect = QRectF(
            (w - size) / 2.0,
            (h - size) / 2.0,
            float(size),
            float(size),
        )

        clip = QPainterPath()
        clip.addRoundedRect(rect, radius, radius)
        painter.setClipPath(clip)

        if self._hover:
            painter.setOpacity(0.75)
        else:
            painter.setOpacity(1.0)

        # 优先级：默认图标（_default 项）> favicon > 字母
        if self._is_default and self._default_pm is not None and not self._default_pm.isNull():
            px = max(1, int(size * dpr))
            pm = self._default_pm.scaled(
                px, px,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            pm.setDevicePixelRatio(dpr)
            x = (w - pm.width() / dpr) / 2.0
            y = (h - pm.height() / dpr) / 2.0
            painter.drawPixmap(QPointF(x, y), pm)
        elif self._pm is not None and not self._pm.isNull():
            px = max(1, int(size * dpr))
            pm = self._pm.scaled(
                px, px,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            pm.setDevicePixelRatio(dpr)
            x = (w - pm.width() / dpr) / 2.0
            y = (h - pm.height() / dpr) / 2.0
            painter.drawPixmap(QPointF(x, y), pm)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(90, 90, 120))
            painter.drawRoundedRect(rect, radius, radius)

            font = painter.font()
            font.setPointSizeF(max(8.0, size * 0.42))
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(
                rect,
                Qt.AlignmentFlag.AlignCenter,
                self._abbr,
            )

        painter.setOpacity(1.0)
        painter.setClipping(False)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
            event.accept()
            return
        super().mousePressEvent(event)


class InputBox(QFrame):
    submitted = pyqtSignal()
    escaped = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        _ensure_app_fonts()

        # 半透明容器：需要透明背景属性 + 自绘，才能让 alpha 生效
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet(
            "QTextEdit {"
            f"  font-family: {INPUT_FONT_STACK};"
            "  font-size: 16px;"
            "  color: rgba(40, 40, 40, 220);"
            "  background: transparent;"
            "  border: none;"
            "  padding: 8px;"
            "}"
        )
        self.text_edit.setFixedWidth(Theme.INPUT_WIDTH)
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.text_edit.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        self.text_edit.textChanged.connect(self._adjust_height)
        self.text_edit.installEventFilter(self)

        self.search_btn = MagnifierButton(self)
        self.search_btn.setFixedSize(
            Theme.INPUT_SEARCH_BTN_SIZE, Theme.INPUT_SEARCH_BTN_SIZE
        )
        self.search_btn.clicked.connect(self.submitted.emit)

        # 左侧引擎按钮
        self.engine_btn = EngineIconButton(self)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            Theme.INPUT_PADDING + 8, Theme.INPUT_PADDING,
            max(0, Theme.INPUT_PADDING - 2), Theme.INPUT_PADDING,
        )
        layout.setSpacing(4)
        layout.addWidget(
            self.engine_btn, 0, Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self.text_edit, 1)
        layout.addWidget(self.search_btn, 0, Qt.AlignmentFlag.AlignBottom)

        self._adjust_height()

    # ---------------- 绘制半透明圆角背景 ----------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)

        # 半透明白底
        painter.setBrush(QColor(255, 255, 255, 150))
        # 半透明边框
        painter.setPen(QPen(QColor(200, 200, 200, 160), 1.4))
        painter.drawRoundedRect(
            rect,
            Theme.INPUT_RADIUS, Theme.INPUT_RADIUS,
        )

    def text(self):
        return self.text_edit.toPlainText().strip()

    def set_engine_abbr(self, abbr):
        """设置左侧按钮显示的引擎缩写。空字符串 = 恢复默认图标。"""
        self.engine_btn.set_abbr(abbr)

    def engine_button(self):
        return self.engine_btn

    def _adjust_height(self):
        doc = self.text_edit.document()
        needed = int(doc.size().height()) + 24
        if needed > Theme.INPUT_MAX_HEIGHT:
            needed = Theme.INPUT_MAX_HEIGHT

        bg_width = (
            Theme.INPUT_WIDTH
            + Theme.INPUT_SEARCH_BTN_SIZE
            + Theme.INPUT_PADDING * 2
        )
        self.setFixedSize(bg_width, needed)

    def eventFilter(self, obj, event):
        if obj is self.text_edit and event.type() == QEvent.Type.KeyPress:
            if (event.key() == Qt.Key.Key_Return
                    and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier)):
                self.submitted.emit()
                return True
            if event.key() == Qt.Key.Key_Escape:
                self.escaped.emit()
                return True
        return super().eventFilter(obj, event)