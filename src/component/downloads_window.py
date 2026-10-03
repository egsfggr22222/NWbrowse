# -*- coding: utf-8 -*-
"""下载记录窗口。列表 + 展开详情 + 右键菜单 + 进度条 + 取消按钮。"""

import os
import sys
import time
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
from i18n import t
from downloads_store import (
    load_downloads, remove_download_by_index,
    clear_downloads, file_status,
)


# ======================================================================
# 标题行：画绿色进度条
# ======================================================================
class HeadFrame(QFrame):
    """行的标题区。下载中时按 progress 画绿色进度条。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0
        self._downloading = False

    def set_progress(self, progress, downloading):
        self._progress = max(0, min(100, int(progress)))
        self._downloading = bool(downloading)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        if not self._downloading or self._progress <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceOver)

        path = QPainterPath()
        path.addRoundedRect(
            QRectF(0.5, 0.5, self.width() - 1, self.height() - 1),
            8, 8,
        )
        painter.setClipPath(path)

        w = int(self.width() * self._progress / 100)
        painter.fillRect(
            QRect(0, 0, w, self.height()),
            QColor(120, 200, 120, 110),
        )
        painter.end()


# ======================================================================
# 一行记录
# ======================================================================
class DownloadRow(QWidget):

    def __init__(self, index, record, parent=None):
        super().__init__(parent)
        self.index = index
        self.record = record

        self._expanded = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---- 标题行 ----
        self._head = HeadFrame(self)
        self._head.setFixedHeight(40)
        self._head.setCursor(Qt.CursorShape.PointingHandCursor)
        self._head.setStyleSheet(
            "QFrame {"
            "  background: #fafafa;"
            "  border: 1px solid #e0e0e0;"
            "  border-radius: 8px;"
            "}"
            "QFrame:hover {"
            "  background: #f0f0f0;"
            "}"
        )

        head_layout = QHBoxLayout(self._head)
        head_layout.setContentsMargins(12, 0, 8, 0)
        head_layout.setSpacing(8)

        self._name_lbl = QLabel()
        self._name_lbl.setStyleSheet(
            "font-size: 13px; color: #333; background: transparent;")
        head_layout.addWidget(self._name_lbl)
        head_layout.addStretch(1)

        # 展开/收起图标
        self._chevron = QLabel("∨")
        self._chevron.setFixedSize(20, 20)
        self._chevron.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._chevron.setStyleSheet(
            "font-size: 12px; color: #888; background: transparent;")
        self._chevron.hide()
        head_layout.addWidget(self._chevron)

        # 取消按钮
        self._cancel_btn = QPushButton("×")
        self._cancel_btn.setFixedSize(20, 20)
        self._cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_btn.setStyleSheet(
            "QPushButton {"
            "  color: #888;"
            "  background: transparent;"
            "  border: none;"
            "  font-size: 14px;"
            "}"
            "QPushButton:hover {"
            "  color: #d04040;"
            "  background: #f5e0e0;"
            "  border-radius: 10px;"
            "}"
        )
        self._cancel_btn.clicked.connect(self._on_cancel_click)
        self._cancel_btn.hide()
        head_layout.addWidget(self._cancel_btn)

        layout.addWidget(self._head)

        # ---- 详情区 ----
        self._detail = QFrame(self)
        self._detail.setStyleSheet(
            "QFrame {"
            "  background: #ffffff;"
            "  border: 1px solid #e0e0e0;"
            "  border-top: none;"
            "  border-bottom-left-radius: 8px;"
            "  border-bottom-right-radius: 8px;"
            "}"
        )
        self._detail.setVisible(False)

        det_layout = QVBoxLayout(self._detail)
        det_layout.setContentsMargins(14, 8, 14, 10)
        det_layout.setSpacing(4)

        self._det_url = QLabel()
        self._det_path = QLabel()
        self._det_time = QLabel()
        self._det_status = QLabel()
        for lbl in (self._det_url, self._det_path,
                    self._det_time, self._det_status):
            lbl.setStyleSheet(
                "font-size: 12px; color: #666; background: transparent;")
            lbl.setWordWrap(True)
            det_layout.addWidget(lbl)

        layout.addWidget(self._detail)

        # 事件
        self._head.mousePressEvent = self._on_head_click
        self._head.mouseDoubleClickEvent = self._on_head_dbl_click
        self._head.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self._head.customContextMenuRequested.connect(self._on_context_menu)

        self._apply_record()

    # ---------------- 刷新 ----------------
    def _apply_record(self):
        r = self.record
        name = r.get("filename", "") or os.path.basename(r.get("path", "")) or "?"
        self._name_lbl.setText(name)

        status = r.get("status", "")
        status_text = self._status_text(status)
        is_downloading = (status == "downloading")

        # 进度
        progress = int(r.get("progress", 0))
        self._head.set_progress(progress, is_downloading)

        # 文件缺失（只在 completed / failed 时检查）
        missing = False
        if status in ("completed", "failed"):
            if file_status(r.get("path", "")) == "missing":
                missing = True

        if missing:
            self._name_lbl.setText(name + "  ·  " + t("download.status_missing"))
            self._name_lbl.setStyleSheet(
                "font-size: 13px; color: #c04040; background: transparent;")
        else:
            self._name_lbl.setStyleSheet(
                "font-size: 13px; color: #333; background: transparent;")

        # 右侧图标
        if is_downloading:
            self._chevron.hide()
            self._cancel_btn.show()
        else:
            self._cancel_btn.hide()
            self._chevron.show()
            self._chevron.setText("∧" if self._expanded else "∨")

        # 详情
        self._det_url.setText(f"{t('download.url')}: {r.get('url', '')}")
        self._det_path.setText(f"{t('download.path')}: {r.get('path', '')}")
        ts = r.get("time", 0)
        time_str = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(ts)) if ts else ""
        self._det_time.setText(f"{t('download.time')}: {time_str}")
        self._det_status.setText(f"{t('download.status')}: {status_text}")

    def _refresh_texts(self):
        """语言切换时刷新本行的文字。"""
        self._apply_record()

    def _status_text(self, status):
        m = {
            "downloading": t("download.status_downloading"),
            "completed": t("download.status_completed"),
            "failed": t("download.status_failed"),
            "cancelled": t("download.status_cancelled"),
        }
        return m.get(status, status)

    # ---------------- 展开 / 收起 ----------------
    def _on_head_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.record.get("status") == "downloading":
                return
            self._toggle_expand()

    def _toggle_expand(self):
        self._expanded = not self._expanded
        self._detail.setVisible(self._expanded)
        self._chevron.setText("∧" if self._expanded else "∨")

    def collapse(self):
        if self._expanded:
            self._expanded = False
            self._detail.setVisible(False)
            self._chevron.setText("∨")

    def is_expanded(self):
        return self._expanded

    # ---------------- 双击 ----------------
    def _on_head_dbl_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._open_folder()

    def _open_folder(self):
        path = self.record.get("path", "")
        if not path:
            return
        parent = os.path.dirname(path)
        if not parent or not os.path.isdir(parent):
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(t("download.file_missing_hint"))
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()
            return
        try:
            os.startfile(parent)
        except Exception as e:
            print("[downloads] 打开文件夹失败:", e)

    # ---------------- 取消 ----------------
    def _on_cancel_click(self):
        """取消下载。

        直接定向转发 MSG_DOWNLOAD_CANCEL_FOR_WINDOW 给发起下载的 window 进程。
        window 收到后：先发取消给 worker，再杀 worker，最后通知下载进程删残留。
        """
        url = self.record.get("url", "")
        path = self.record.get("path", "")
        window_id = self.record.get("window_id", "")

        if url and window_id:
            try:
                from ipc import (
                    IpcClient, window_role,
                    MSG_DOWNLOAD_CANCEL_FOR_WINDOW,
                )
                payload = json.dumps({
                    "url": url,
                    "path": path,
                    "window_id": window_id,
                }, ensure_ascii=False)
                ok = IpcClient.send_to_role(
                    window_role(window_id),
                    MSG_DOWNLOAD_CANCEL_FOR_WINDOW,
                    payload.encode("utf-8"),
                )
                print(f"[downloads] 已直接转发取消给 window {window_id} "
                      f"(ok={ok})")
            except Exception as e:
                print("[downloads] 直接转发取消失败:", e)
        else:
            print(f"[downloads] 取消失败：url={url!r} window_id={window_id!r}")

        try:
            from downloads_store import update_download_status
            update_download_status(url, path, "cancelled")
        except Exception as e:
            print("[downloads] 标记取消失败:", e)

        w = self.window()
        if hasattr(w, "reload_list"):
            w.reload_list()

    # ---------------- 右键菜单 ----------------
    def _on_context_menu(self, pos):
        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self._head)
        except Exception:
            menu = QMenu(self._head)

        act_open = menu.addAction(t("download.open_folder"))
        menu.addSeparator()
        act_del_file = menu.addAction(t("download.delete_file"))
        act_del_record = menu.addAction(t("download.remove_record"))

        act_open.triggered.connect(self._open_folder)
        act_del_file.triggered.connect(self._delete_file)
        act_del_record.triggered.connect(self._remove_record)

        global_pos = self._head.mapToGlobal(pos)
        menu.exec(global_pos)

    def _delete_file(self):
        path = self.record.get("path", "")
        if not path or not os.path.isfile(path):
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(t("download.delete_file_missing"))
            box.setIcon(QMessageBox.Icon.Question)
            box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if box.exec() == QMessageBox.StandardButton.Yes:
                self._remove_record()
            return

        box = QMessageBox(self)
        box.setWindowTitle(t("app.title"))
        box.setText(t("download.delete_file_confirm") % path)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if box.exec() != QMessageBox.StandardButton.Yes:
            return

        try:
            os.remove(path)
        except Exception as e:
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(str(e))
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()
            return
        self._remove_record()

    def _remove_record(self):
        remove_download_by_index(self.index)
        w = self.window()
        if hasattr(w, "reload_list"):
            w.reload_list()


# ======================================================================
# 下载窗口
# ======================================================================
class DownloadsWindow(QWidget):

    RADIUS = 12
    WIDTH = 620
    HEIGHT = 520
    PAD = 20
    BORDER_COLOR = QColor(160, 160, 160)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self._rows = []
        self._build_ui()
        self._center_screen()

    def _build_ui(self):
        body = QVBoxLayout(self)
        body.setContentsMargins(self.PAD, self.PAD, self.PAD, self.PAD)
        body.setSpacing(8)

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.addStretch(1)

        self.close_btn = QPushButton("×", self)
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet(
            "QPushButton {"
            "  color: #555;"
            "  background: transparent;"
            "  border: none;"
            "  font-size: 16px;"
            "}"
            "QPushButton:hover {"
            "  background: #e0e0e0;"
            "  border-radius: 6px;"
            "}"
        )
        self.close_btn.clicked.connect(self.close)
        title_row.addWidget(self.close_btn)
        body.addLayout(title_row)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )

        self._host = QWidget()
        self._host.setStyleSheet("background: transparent;")
        self._rows_layout = QVBoxLayout(self._host)
        self._rows_layout.setContentsMargins(0, 0, 0, 0)
        self._rows_layout.setSpacing(6)
        self._rows_layout.addStretch(1)
        self.scroll.setWidget(self._host)

        body.addWidget(self.scroll, 1)

        self._empty_lbl = QLabel(t("download.empty"), self)
        self._empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_lbl.setStyleSheet("font-size: 13px; color: #999;")
        self._empty_lbl.hide()
        body.addWidget(self._empty_lbl)

        self._warn_lbl = QLabel(t("download.lightweight_warning"), self)
        self._warn_lbl.setWordWrap(True)
        self._warn_lbl.setStyleSheet(
            "font-size: 11px; color: #a06000;"
            "padding: 4px 2px;"
        )
        body.addWidget(self._warn_lbl)

        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)
        bottom.setSpacing(8)

        self.clear_btn = QPushButton(t("download.clear_all"))
        self.clear_btn.setFixedWidth(120)
        self.clear_btn.clicked.connect(self._on_clear_all)
        bottom.addWidget(self.clear_btn)

        bottom.addStretch(1)

        self._notify_lbl = QLabel(t("download.notify"))
        self._notify_lbl.setStyleSheet("font-size: 12px; color: #555;")
        bottom.addWidget(self._notify_lbl)

        self.notify_toggle = QCheckBox()
        self.notify_toggle.toggled.connect(self._on_notify_toggled)
        bottom.addWidget(self.notify_toggle)

        body.addLayout(bottom)

        self.reload_list()

    def _refresh_texts(self):
        """语言切换时刷新窗口上的固定文字。"""
        try:
            self._empty_lbl.setText(t("download.empty"))
        except Exception:
            pass
        try:
            self.clear_btn.setText(t("download.clear_all"))
        except Exception:
            pass
        try:
            self._notify_lbl.setText(t("download.notify"))
        except Exception:
            pass
        try:
            self._warn_lbl.setText(t("download.lightweight_warning"))
        except Exception:
            pass

        # 行里的文字
        for r in self._rows:
            if hasattr(r, "_refresh_texts"):
                try:
                    r._refresh_texts()
                except Exception:
                    pass

    def set_notify_state(self, on):
        self.notify_toggle.blockSignals(True)
        self.notify_toggle.setChecked(bool(on))
        self.notify_toggle.blockSignals(False)

    def _on_notify_toggled(self, on):
        try:
            from settings_backend import SettingsBackend
            SettingsBackend().set_download_notify(on)
        except Exception as e:
            print("[downloads] 保存提醒设置失败:", e)

    def _on_clear_all(self):
        box = QMessageBox(self)
        box.setWindowTitle(t("app.title"))
        box.setText(t("download.clear_all_confirm"))
        box.setIcon(QMessageBox.Icon.Question)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if box.exec() != QMessageBox.StandardButton.Yes:
            return
        clear_downloads()
        self.reload_list()

    def reload_list(self):
        for r in self._rows:
            r.setParent(None)
            r.deleteLater()
        self._rows = []

        data = load_downloads()
        if not data:
            self._empty_lbl.show()
            return
        self._empty_lbl.hide()

        for i, rec in enumerate(data):
            row = DownloadRow(i, rec, self._host)
            idx = self._rows_layout.count() - 1
            self._rows_layout.insertWidget(idx, row)
            self._rows.append(row)

    def collapse_all_except(self, keep):
        for r in self._rows:
            if r is not keep and r.is_expanded():
                r.collapse()

    # ---------------- 窗口拖动 / 收起 ----------------
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            for r in self._rows:
                if r.is_expanded():
                    r.collapse()
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

    def _center_screen(self):
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.left() + (screen.width() - self.width()) // 2,
            screen.top() + (screen.height() - self.height()) // 2,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(self.BORDER_COLOR, 1))
        painter.drawRoundedRect(
            QRectF(0.5, 0.5, self.width() - 1, self.height() - 1),
            self.RADIUS, self.RADIUS,
        )