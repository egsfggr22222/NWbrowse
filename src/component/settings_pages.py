# -*- coding: utf-8 -*-
"""设置页面。每个页面只做 UI，读写走 backend 接口。

UI 文字从 i18n.t() 取。语言变化时调 _refresh_texts() 刷新。
LanguagePage 用列表 + 勾选框展示语言，支持删除非中文语言，
支持拖动导出和拖入导入语言文件。
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths
from i18n import (
    t, list_languages, import_language, export_language,
    load as i18n_load,
)


class Row(QWidget):
    def __init__(self, title, widget, hint="", parent=None):
        super().__init__(parent)
        self._widget = widget

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(12)

        left = QVBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(2)

        self._lbl = QLabel(title)
        self._lbl.setStyleSheet("font-size: 13px; color: #222;")
        left.addWidget(self._lbl)

        self._hint = None
        if hint:
            self._hint = QLabel(hint)
            self._hint.setStyleSheet("font-size: 11px; color: #888;")
            self._hint.setWordWrap(True)
            left.addWidget(self._hint)

        layout.addLayout(left, 1)
        layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignVCenter)

    def set_texts(self, title, hint=""):
        self._lbl.setText(title)
        if self._hint is not None:
            self._hint.setText(hint)


class SectionTitle(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            "font-size: 12px; color: #666;"
            "padding: 16px 20px 4px 20px;"
        )


class SettingPage(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

        # 隐藏滚动条，只保留鼠标滚轮
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
            "QScrollBar:vertical { width: 0px; background: transparent; }"
            "QScrollBar:horizontal { height: 0px; background: transparent; }"
            "QScrollBar::handle:vertical { background: transparent; }"
            "QScrollBar::handle:horizontal { background: transparent; }"
            "QScrollBar::add-line:vertical,"
            "QScrollBar::sub-line:vertical { height: 0px; }"
            "QScrollBar::add-line:horizontal,"
            "QScrollBar::sub-line:horizontal { width: 0px; }"
            "QScrollBar::add-page, QScrollBar::sub-page { background: transparent; }"
        )
        self.viewport().setStyleSheet("background: transparent;")

        self._host = QWidget()
        self._host.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._host)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.addStretch(1)

        self.setWidget(self._host)
        self._backend = None

        self._rows = []
        self._sections = []

    def set_backend(self, backend):
        self._backend = backend
        self._load_values()

    def _load_values(self):
        pass

    def _refresh_texts(self):
        pass

    def _add_section(self, title):
        idx = self._layout.count() - 1
        w = SectionTitle(title)
        self._layout.insertWidget(idx, w)
        self._sections.append(w)
        return w

    def _add_row(self, title, widget, hint=""):
        idx = self._layout.count() - 1
        row = Row(title, widget, hint)
        self._layout.insertWidget(idx, row)
        self._rows.append(row)
        return row

    def _add_widget(self, widget):
        idx = self._layout.count() - 1
        self._layout.insertWidget(idx, widget)
        return widget


class GeneralPage(SettingPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._sec_pwd = self._add_section(t("general.sec_password"))

        self.pwd_box_btn = QPushButton(t("general.password_box"))
        self.pwd_box_btn.setFixedWidth(120)
        self.pwd_box_btn.clicked.connect(self._on_open_password_box)
        self._row_pwd_box = self._add_row(
            t("general.password_box"), self.pwd_box_btn,
            t("general.password_box_hint"))

        # ---- 搜索引擎 ----
        self._sec_engine = self._add_section(t("general.sec_engine"))

        self.engine_manage_btn = QPushButton(t("general.engine_manage"))
        self.engine_manage_btn.setFixedWidth(120)
        self.engine_manage_btn.clicked.connect(self._on_open_engine_dialog)
        self._row_engine_manage = self._add_row(
            t("general.engine_manage"), self.engine_manage_btn,
            t("general.engine_manage_hint"))
        # ------------------

    # ---------------- 读值 ----------------
    def _load_values(self):
        pass

    # ---------------- 刷新文字 ----------------
    def _refresh_texts(self):
        self._sec_pwd.setText(t("general.sec_password"))
        self.pwd_box_btn.setText(t("general.password_box"))
        self._row_pwd_box.set_texts(
            t("general.password_box"), t("general.password_box_hint"))

        self._sec_engine.setText(t("general.sec_engine"))
        self.engine_manage_btn.setText(t("general.engine_manage"))
        self._row_engine_manage.set_texts(
            t("general.engine_manage"), t("general.engine_manage_hint"))

    # ---------------- 密码箱 ----------------
    def _on_open_password_box(self):
        """打开密码箱对话框。"""
        try:
            dlg = PasswordBoxDialog(self)
            dlg.exec()
        except Exception as e:
            import traceback
            print("[settings] 打开密码箱失败:", e)
            traceback.print_exc()

    # ---------------- 搜索引擎 ----------------
    def _on_open_engine_dialog(self):
        """打开搜索引擎管理对话框。"""
        try:
            dlg = SearchEngineDialog(self)
            dlg.exec()
        except Exception as e:
            import traceback
            print("[settings] 打开搜索引擎管理失败:", e)
            traceback.print_exc()


def _clear_cookie_files():
    """删所有窗口 profile 的 Cookie 文件。返回 (成功数, 失败数)。"""
    import os

    userdata = os.path.join(apppaths.APP_DIR, "userdata")

    ok = 0
    fail = 0

    if not os.path.isdir(userdata):
        return ok, fail

    for window_dir in os.listdir(userdata):
        win_path = os.path.join(userdata, window_dir)
        if not os.path.isdir(win_path):
            continue

        net_dir = os.path.join(
            win_path, "EBWebView", "Default", "Network"
        )
        if not os.path.isdir(net_dir):
            continue

        for name in ("Cookies", "Cookies-journal"):
            f = os.path.join(net_dir, name)
            if not os.path.isfile(f):
                continue
            try:
                os.remove(f)
                ok += 1
            except Exception:
                fail += 1

    return ok, fail


def _clear_cookie_files():
    """删所有窗口 profile 的 Cookie 文件。返回 (成功数, 失败数)。"""
    import os

    userdata = os.path.join(apppaths.APP_DIR, "userdata")

    ok = 0
    fail = 0

    if not os.path.isdir(userdata):
        return ok, fail

    for window_dir in os.listdir(userdata):
        win_path = os.path.join(userdata, window_dir)
        if not os.path.isdir(win_path):
            continue

        net_dir = os.path.join(
            win_path, "EBWebView", "Default", "Network"
        )
        if not os.path.isdir(net_dir):
            continue

        for name in ("Cookies", "Cookies-journal"):
            f = os.path.join(net_dir, name)
            if not os.path.isfile(f):
                continue
            try:
                os.remove(f)
                ok += 1
            except Exception:
                fail += 1

    return ok, fail


class HistoryPage(SettingPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._records = []
        self._last_history_mtime = 0

        self._sec_h = self._add_section(t("history.sec_history"))

        # ---- 筛选栏 ----
        filter_host = QWidget()
        fl = QVBoxLayout(filter_host)
        fl.setContentsMargins(20, 8, 20, 8)
        fl.setSpacing(8)

        _combo_style = (
            "QComboBox {"
            "  background: #ffffff;"
            "  color: #222222;"
            "  border: 1px solid #dcdcdc;"
            "  border-radius: 6px;"
            "  padding: 0 8px;"
            "  font-size: 12px;"
            "}"
            "QComboBox:focus { border: 1px solid #7aa7f0; }"
            "QComboBox::drop-down {"
            "  border: none;"
            "  width: 20px;"
            "}"
            "QComboBox QAbstractItemView {"
            "  background: #ffffff;"
            "  color: #222222;"
            "  border: 1px solid #dcdcdc;"
            "  selection-background-color: #e8f0fe;"
            "  selection-color: #2f5fd0;"
            "  outline: none;"
            "}"
        )

        # ---- 第一行：搜索 + 天数 + 主域 ----
        row1 = QHBoxLayout()
        row1.setSpacing(8)

        self._search_edit = QLineEdit()
        self._search_edit.setPlaceholderText(
            t("history.search_placeholder"))
        self._search_edit.setFixedHeight(32)
        self._search_edit.textChanged.connect(self._on_filter_changed)
        self._search_edit.setStyleSheet(
            "QLineEdit {"
            "  background: #fafafa;"
            "  border: 1px solid #dcdcdc;"
            "  border-radius: 6px;"
            "  padding: 0 10px;"
            "  font-size: 13px;"
            "}"
            "QLineEdit:focus { border: 1px solid #7aa7f0; }"
        )
        row1.addWidget(self._search_edit, 1)

        self._range_combo = QComboBox()
        self._range_combo.setFixedWidth(100)
        self._range_combo.setFixedHeight(32)
        self._range_combo.currentIndexChanged.connect(self._on_filter_changed)
        self._range_combo.setStyleSheet(_combo_style)
        row1.addWidget(self._range_combo)

        self._host_combo = QComboBox()
        self._host_combo.setFixedWidth(180)
        self._host_combo.setFixedHeight(32)
        self._host_combo.addItem(t("history.placeholder_host"), "")
        self._host_combo.currentIndexChanged.connect(self._on_filter_changed)
        self._host_combo.setStyleSheet(_combo_style)
        row1.addWidget(self._host_combo)

        fl.addLayout(row1)

        # ---- 记录列表（纯滚动，自动拉伸）----
        self._list = QListWidget()
        self._list.setSelectionMode(
            QListWidget.SelectionMode.ExtendedSelection)
        self._list.setStyleSheet(
            "QListWidget {"
            "  background: #fafafa;"
            "  border: 1px solid #e0e0e0;"
            "  border-radius: 6px;"
            "  font-size: 12px;"
            "  outline: none;"
            "}"
            "QListWidget::item {"
            "  height: 28px;"
            "  padding-left: 6px;"
            "}"
            "QListWidget::item:hover { background: #f0f0f0; }"
            "QListWidget::item:selected {"
            "  background: #e8f0fe;"
            "  color: #2f5fd0;"
            "}"
        )
        self._list.itemDoubleClicked.connect(self._on_history_open)
        fl.addWidget(self._list, 1)

        # ---- 底栏：全选 + 删除 + 清空 Cookie ----
        row2 = QHBoxLayout()
        row2.setSpacing(8)

        row2.addStretch(1)

        self._select_all_btn = QPushButton(t("history.select_all"))
        self._select_all_btn.setMinimumWidth(72)
        self._select_all_btn.clicked.connect(self._on_select_all)
        row2.addWidget(self._select_all_btn)

        self._del_sel_btn = QPushButton(t("history.delete_selected"))
        self._del_sel_btn.setMinimumWidth(84)
        self._del_sel_btn.clicked.connect(self._on_delete_selected)
        row2.addWidget(self._del_sel_btn)

        self._clear_cookie_btn = QPushButton(t("history.clear_cookie"))
        self._clear_cookie_btn.setMinimumWidth(100)
        self._clear_cookie_btn.clicked.connect(self._on_clear_cookie)
        row2.addWidget(self._clear_cookie_btn)

        fl.addLayout(row2)

        self._add_widget(filter_host)

        # 初始填一次
        self._rebuild_range_combo()

        # 定时刷新（每 2 秒检查 history.json 是否变化）
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setInterval(2000)
        self._refresh_timer.timeout.connect(self._auto_refresh)
        self._refresh_timer.start()

    # ------------------------------------------------------------------
    def _on_history_days_changed(self, _val):
        self._rebuild_range_combo()

    def _rebuild_range_combo(self):
        cur = self._range_combo.currentData()
        n = 30

        self._range_combo.blockSignals(True)
        self._range_combo.clear()
        self._range_combo.addItem(t("history.range_all"), 0)
        for i in range(1, n + 1):
            self._range_combo.addItem(str(i), i)

        idx = self._range_combo.findData(cur)
        self._range_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self._range_combo.blockSignals(False)

    def _refresh_texts(self):
        self._sec_h.setText(t("history.sec_history"))

        self._search_edit.setPlaceholderText(
            t("history.search_placeholder"))
        self._rebuild_range_combo()
        self._refresh_host_combo()
        self._select_all_btn.setText(t("history.select_all"))
        self._del_sel_btn.setText(t("history.delete_selected"))
        self._clear_cookie_btn.setText(t("history.clear_cookie"))
        self._reload_list()

    def _load_values(self):
        if self._backend is None:
            return

        self._rebuild_range_combo()
        self._refresh_host_combo()
        self._reload_list()

    # ------------------------------------------------------------------
    def _refresh_host_combo(self):
        try:
            from history_store import all_hosts
            hosts = all_hosts()
        except Exception:
            hosts = []

        cur = self._host_combo.currentData()
        self._host_combo.blockSignals(True)
        self._host_combo.clear()
        self._host_combo.addItem(t("history.placeholder_host"), "")
        for h in hosts:
            self._host_combo.addItem(h, h)
        idx = self._host_combo.findData(cur)
        self._host_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self._host_combo.blockSignals(False)

    def _on_filter_changed(self, *_):
        self._reload_list()

    def _on_select_all(self):
        self._list.selectAll()

    # ------------------------------------------------------------------
    # 双击历史记录：发 URL 给 bar，由 bar 分配窗口
    # ------------------------------------------------------------------
    def _on_history_open(self, item):
        if item is None:
            return
        url = item.data(Qt.ItemDataRole.UserRole)
        if not url:
            return
        self._open_url_via_bar(url)

    def _open_url_via_bar(self, url):
        try:
            import json
            from ipc import IpcClient, ROLE_BAR, MSG_NAVIGATE
            payload = json.dumps({
                "cmd": "request_url",
                "window_id": "",
                "host": "",
                "url": url,
            }, ensure_ascii=False)
            ok = IpcClient.send_to_role(
                ROLE_BAR, MSG_NAVIGATE, payload.encode("utf-8")
            )
            print(f"[history] 已发 bar: {url!r} ok={ok}")
        except Exception as e:
            print("[history] 发 bar 失败:", e)

    # ------------------------------------------------------------------
    def _on_delete_selected(self):
        items = self._list.selectedItems()
        if not items:
            return
        urls = []
        for it in items:
            u = it.data(Qt.ItemDataRole.UserRole)
            if u:
                urls.append(u)
        if not urls:
            return

        try:
            msg = t("history.delete_confirm") % len(urls)
        except Exception:
            msg = f"Delete {len(urls)} selected records?"

        box = QMessageBox(self)
        box.setWindowTitle(t("app.title"))
        box.setText(msg)
        box.setIcon(QMessageBox.Icon.Question)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if box.exec() != QMessageBox.StandardButton.Yes:
            return

        try:
            from history_store import remove_by_urls
            remove_by_urls(urls)
        except Exception as e:
            print("[history] 删除失败:", e)
            return

        self._refresh_host_combo()
        self._reload_list()

    def _on_clear_cookie(self):
        try:
            msg = t("history.clear_cookie_confirm")
        except Exception:
            msg = "Clear all cookies?"

        box = QMessageBox(self)
        box.setWindowTitle(t("app.title"))
        box.setText(msg)
        box.setIcon(QMessageBox.Icon.Warning)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if box.exec() != QMessageBox.StandardButton.Yes:
            return

        ok_count, fail_count = _clear_cookie_files()

        if fail_count:
            try:
                done_msg = t("history.clear_cookie_fail") % fail_count
            except Exception:
                done_msg = f"{fail_count} files in use."
        else:
            try:
                done_msg = t("history.clear_cookie_done") % ok_count
            except Exception:
                done_msg = f"Cleared {ok_count} cookie files."

        info = QMessageBox(self)
        info.setWindowTitle(t("app.title"))
        info.setText(done_msg)
        info.setIcon(QMessageBox.Icon.Information)
        info.exec()

    # ------------------------------------------------------------------
    def _auto_refresh(self):
        """history.json 变了就重刷。"""
        try:
            from history_store import STORE_PATH
            mtime = (
                os.path.getmtime(STORE_PATH)
                if os.path.isfile(STORE_PATH)
                else 0
            )
        except Exception:
            mtime = 0

        if mtime != self._last_history_mtime:
            self._last_history_mtime = mtime
            self._refresh_host_combo()
            self._reload_list()

    @staticmethod
    def _fmt_time(ts):
        import time as _t
        try:
            return _t.strftime("%Y-%m-%d %H:%M",
                               _t.localtime(float(ts)))
        except Exception:
            return ""

    def _reload_list(self):
        try:
            from history_store import load_history
        except Exception as e:
            print("[history] 加载 history_store 失败:", e)
            self._records = []
            self._list.clear()
            return

        days = self._range_combo.currentData() or 0
        keyword = self._search_edit.text().strip()
        host = self._host_combo.currentData() or ""

        self._records = load_history(days=days, host=host, keyword=keyword)

        self._list.clear()
        for r in self._records:
            ts = r.get("time", 0)
            title = r.get("title", "") or r.get("url", "")
            text = f"{self._fmt_time(ts)}  {title}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, r.get("url", ""))
            item.setToolTip(r.get("url", ""))
            self._list.addItem(item)


class LanguagePage(SettingPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._sec_cur = self._add_section(t("language.current"))

        # 语言列表
        lang_host = QWidget()
        lang_layout = QVBoxLayout(lang_host)
        lang_layout.setContentsMargins(20, 4, 20, 8)
        lang_layout.setSpacing(6)

        self._lang_hint = QLabel(t("language.switch_hint"))
        self._lang_hint.setStyleSheet("font-size: 11px; color: #888;")
        self._lang_hint.setWordWrap(True)
        lang_layout.addWidget(self._lang_hint)

        self.lang_list = QListWidget()
        self.lang_list.setFixedHeight(180)
        self.lang_list.setStyleSheet(
            "QListWidget {"
            "  background: #fafafa;"
            "  border: 1px solid #e0e0e0;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  outline: none;"
            "}"
            "QListWidget::item {"
            "  height: 36px;"
            "  padding-left: 8px;"
            "  border-radius: 4px;"
            "}"
            "QListWidget::item:hover {"
            "  background: #f0f0f0;"
            "}"
        )
        lang_layout.addWidget(self.lang_list)

        self._add_widget(lang_host)

        self._sec_exp = self._add_section(t("language.export"))

        export_row = QWidget()
        export_layout = QHBoxLayout(export_row)
        export_layout.setContentsMargins(20, 4, 20, 4)
        export_layout.setSpacing(12)

        self.export_icon = DraggableJsonIcon("JSON", self)
        self.export_icon.setFixedSize(48, 48)
        self.export_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.export_icon.setStyleSheet(
            "QLabel {"
            "  background: #f0f0f0;"
            "  border: 1px solid #d0d0d0;"
            "  border-radius: 8px;"
            "  font-size: 13px;"
            "  color: #555;"
            "}"
            "QLabel:hover {"
            "  background: #e8e8e8;"
            "  border: 1px solid #b8b8b8;"
            "}"
        )
        self.export_icon.setToolTip(t("language.export_hint"))
        self.export_icon.setCursor(Qt.CursorShape.OpenHandCursor)
        export_layout.addWidget(self.export_icon)

        self._exp_hint = QLabel(t("language.export_hint"))
        self._exp_hint.setStyleSheet("font-size: 11px; color: #888;")
        self._exp_hint.setWordWrap(True)
        export_layout.addWidget(self._exp_hint, 1)

        self._add_widget(export_row)

        self._sec_imp = self._add_section(t("language.import_area"))

        self.drop_area = DropArea(self)
        self.drop_area.setFixedHeight(100)
        self.drop_area.setStyleSheet(
            "QFrame {"
            "  background: #fafafa;"
            "  border: 2px dashed #cccccc;"
            "  border-radius: 8px;"
            "}"
            "QFrame:hover {"
            "  background: #f0f4ff;"
            "  border: 2px dashed #7aa7f0;"
            "}"
        )
        self.drop_area.setAcceptDrops(True)

        drop_layout = QVBoxLayout(self.drop_area)
        drop_layout.setContentsMargins(12, 12, 12, 12)
        self._drop_label = QLabel(t("language.import_area"))
        self._drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._drop_label.setStyleSheet("color: #888; font-size: 12px;")
        drop_layout.addWidget(self._drop_label)

        self._add_widget(self.drop_area)

        # 信号
        self.lang_list.itemClicked.connect(self._on_lang_clicked)
        self.drop_area.dropped.connect(self._on_file_dropped)

        self._refresh_languages()

    # ---------------- 语言列表 ----------------
    def _refresh_languages(self):
        """重建语言列表。当前语言显示对勾，非中文且非当前显示删除按钮。"""
        self.lang_list.clear()
        if self._backend is None:
            return

        cur_code = self._backend.get_language()

        for code, name in list_languages():
            item = QListWidgetItem(self.lang_list)
            item.setData(Qt.ItemDataRole.UserRole, code)

            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(8, 0, 6, 0)
            row_layout.setSpacing(6)

            name_lbl = QLabel(name)
            name_lbl.setStyleSheet("font-size: 13px; color: #333;")
            row_layout.addWidget(name_lbl)
            row_layout.addStretch(1)

            if code == cur_code:
                check = QLabel("✓")
                check.setFixedSize(24, 24)
                check.setAlignment(Qt.AlignmentFlag.AlignCenter)
                check.setStyleSheet(
                    "QLabel {"
                    "  color: #2f5fd0;"
                    "  background: #e8f0fe;"
                    "  border-radius: 12px;"
                    "  font-size: 14px;"
                    "  font-weight: bold;"
                    "}"
                )
                row_layout.addWidget(check)
            elif code != "zh-CN":
                del_btn = QPushButton("×")
                del_btn.setFixedSize(24, 24)
                del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
                del_btn.setStyleSheet(
                    "QPushButton {"
                    "  color: #888;"
                    "  background: transparent;"
                    "  border: none;"
                    "  font-size: 14px;"
                    "}"
                    "QPushButton:hover {"
                    "  color: #d04040;"
                    "  background: #f5e0e0;"
                    "  border-radius: 12px;"
                    "}"
                )
                del_btn.clicked.connect(
                    lambda _=False, c=code: self._on_delete_lang(c))
                row_layout.addWidget(del_btn)

            item.setSizeHint(row.sizeHint())
            self.lang_list.setItemWidget(item, row)

    def _on_lang_clicked(self, item):
        if item is None or self._backend is None:
            return
        code = item.data(Qt.ItemDataRole.UserRole)
        if not code:
            return
        if code == self._backend.get_language():
            return
        self._switch_language(code)

    def _switch_language(self, code):
        self._backend.set_language(code)
        self._update_export_target()

        try:
            i18n_load(code)
        except Exception as e:
            print("[language] 切换失败:", e)
            return

        try:
            from ipc import broadcast, MSG_LANGUAGE_CHANGED, ROLE_SETTINGS
            broadcast(
                MSG_LANGUAGE_CHANGED,
                code.encode("utf-8"),
                exclude_role=ROLE_SETTINGS,
            )
        except Exception as e:
            print("[language] 广播失败:", e)
        # i18n_load 触发 _refresh_texts -> _refresh_languages，列表自动刷新

    def _on_delete_lang(self, code):
        if not code:
            return
        if code == "zh-CN":
            self._show_msg(t("language.delete_default"))
            return
        if self._backend is not None and code == self._backend.get_language():
            self._show_msg(t("language.delete_current"))
            return

        path = os.path.join(apppaths.COMPONENT_DIR, "i18n", code + ".json")
        if not os.path.isfile(path):
            self._refresh_languages()
            return

        box = QMessageBox(self)
        box.setWindowTitle(t("app.title"))
        box.setText(t("language.delete_confirm") % code)
        box.setIcon(QMessageBox.Icon.Question)
        box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if box.exec() != QMessageBox.StandardButton.Yes:
            return

        try:
            os.remove(path)
        except Exception as e:
            self._show_msg(t("language.delete_fail") % str(e))
            return

        self._refresh_languages()

    def _show_msg(self, text):
        box = QMessageBox(self)
        box.setWindowTitle(t("app.title"))
        box.setText(text)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()

    def set_backend(self, backend):
        self._backend = backend
        self._update_export_target()
        self._load_values()

    def _update_export_target(self):
        code = "zh-CN"
        if self._backend is not None:
            code = self._backend.get_language() or "zh-CN"
        self.export_icon.set_language_code(code)

    def _refresh_texts(self):
        self._sec_cur.setText(t("language.current"))
        self._lang_hint.setText(t("language.switch_hint"))
        self._sec_exp.setText(t("language.export"))
        self.export_icon.setToolTip(t("language.export_hint"))
        self._exp_hint.setText(t("language.export_hint"))
        self._sec_imp.setText(t("language.import_area"))
        self._drop_label.setText(t("language.import_area"))
        self._refresh_languages()

    def _load_values(self):
        self._refresh_languages()

    def _on_file_dropped(self, path):
        try:
            code, name = import_language(path)
        except ValueError as e:
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(str(e))
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()
            return

        self._refresh_languages()

        box = QMessageBox(self)
        box.setWindowTitle(t("app.title"))
        box.setText(t("language.import_ok") % name)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()


class DraggableJsonIcon(QLabel):
    """可拖动的 JSON 图标。拖动时把当前语言文件导出到拖放目标。

    右键弹出"另存为…"。
    """

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._code = "zh-CN"
        self._drag_start = None

    def set_language_code(self, code):
        self._code = code or "zh-CN"

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.position().toPoint()
        elif event.button() == Qt.MouseButton.RightButton:
            self._show_menu(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_start is None:
            return
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.position().toPoint() - self._drag_start).manhattanLength() < 10:
            return

        drag = QDrag(self)
        mime = QMimeData()

        import tempfile
        tmp_dir = tempfile.gettempdir()
        dst = os.path.join(tmp_dir, self._code + ".json")
        if not export_language(self._code, dst):
            return

        mime.setUrls([QUrl.fromLocalFile(dst)])
        drag.setMimeData(mime)
        drag.exec(Qt.DropAction.CopyAction)
        self._drag_start = None

    def mouseReleaseEvent(self, event):
        self._drag_start = None
        super().mouseReleaseEvent(event)

    def _show_menu(self, event):
        menu = QMenu(self)
        act_save = menu.addAction(t("language.save_as"))
        act_save.triggered.connect(self._save_as)
        menu.exec(event.globalPosition().toPoint())

    def _save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            t("language.save_dialog"),
            self._code + ".json",
            "JSON (*.json)",
        )
        if not path:
            return
        ok = export_language(self._code, path)
        if not ok:
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(t("language.import_fail") % "export failed")
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()


class DropArea(QFrame):
    """接受文件拖入的区域。拖入后 emit dropped(path)。"""

    dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            event.ignore()
            return
        path = urls[0].toLocalFile()
        if not path:
            event.ignore()
            return
        self.dropped.emit(path)
        event.acceptProposedAction()


class AdvancedPage(SettingPage):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._sec_env = self._add_section(t("advanced.sec_env"))

        self.ua_global = QLineEdit()
        self.ua_global.setFixedWidth(260)
        self._row_ua = self._add_row(
            t("advanced.global_ua"), self.ua_global, t("common.need_restart"))

    def _refresh_texts(self):
        self._sec_env.setText(t("advanced.sec_env"))
        self._row_ua.set_texts(t("advanced.global_ua"),
                               t("common.need_restart"))


class WhitelistDialog(QDialog):
    """添加白名单网站：输入 host，勾选"不保存历史"。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("history.wl_dialog_title"))
        self.setFixedSize(360, 170)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        self._host_label = QLabel(t("history.wl_host_label"))
        layout.addWidget(self._host_label)

        self.host_edit = QLineEdit()
        layout.addWidget(self.host_edit)

        self.no_history = QCheckBox(t("history.wl_no_history"))
        layout.addWidget(self.no_history)

        btns = QHBoxLayout()
        btns.addStretch(1)
        cancel = QPushButton(t("common.cancel"))
        cancel.clicked.connect(self.reject)
        ok = QPushButton(t("common.ok"))
        ok.clicked.connect(self.accept)
        btns.addWidget(cancel)
        btns.addWidget(ok)
        layout.addLayout(btns)

    def values(self):
        return (
            self.host_edit.text().strip(),
            self.no_history.isChecked(),
        )


class PasswordBoxDialog(QDialog):
    """密码箱：按主域分组显示已保存密码，右键删除。明文显示。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("general.password_box"))
        self.setFixedSize(560, 480)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # ---- 安全提示 ----
        warn_lbl = QLabel(t("password.warning"), self)
        warn_lbl.setWordWrap(True)
        warn_lbl.setStyleSheet(
            "color: #c06000; background: #fff8e8;"
            "border: 1px solid #f0d8a0; border-radius: 6px;"
            "padding: 8px 10px; font-size: 12px;"
        )
        root.addWidget(warn_lbl)
        # ------------------

        self._tree = QTreeWidget(self)
        self._tree.setHeaderLabels(["网站 / 账号", "密码"])
        self._tree.setColumnWidth(0, 360)
        self._tree.setStyleSheet(
            "QTreeWidget {"
            "  background: #fafafa;"
            "  border: 1px solid #e0e0e0;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  outline: none;"
            "}"
            "QTreeWidget::item { height: 26px; }"
            "QTreeWidget::item:hover { background: #f0f0f0; }"
            "QTreeWidget::item:selected {"
            "  background: #e8f0fe; color: #2f5fd0;"
            "}"
        )
        self._tree.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._on_context_menu)
        root.addWidget(self._tree, 1)

        self._empty_lbl = QLabel(t("password.empty"), self)
        self._empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_lbl.setStyleSheet("color: #999; font-size: 13px;")
        self._empty_lbl.hide()
        root.addWidget(self._empty_lbl)

        bottom = QHBoxLayout()
        bottom.addStretch(1)
        close_btn = QPushButton(t("common.close"), self)
        close_btn.setFixedWidth(90)
        close_btn.clicked.connect(self.accept)
        bottom.addWidget(close_btn)
        root.addLayout(bottom)

        self._reload()

    def _reload(self):
        """从 passwords.json 重读，重建树。"""
        self._tree.clear()
        try:
            from password_hook import list_all
            data = list_all()
        except Exception as e:
            print("[settings] 读 passwords 失败:", e)
            data = {}

        if not data:
            self._empty_lbl.show()
            return
        self._empty_lbl.hide()

        for host, items in sorted(data.items()):
            if not isinstance(items, list) or not items:
                continue
            host_node = QTreeWidgetItem(self._tree)
            host_node.setText(0, host)
            host_node.setData(0, Qt.ItemDataRole.UserRole, ("host", host))
            font = host_node.font(0)
            font.setBold(True)
            host_node.setFont(0, font)

            for idx, rec in enumerate(items):
                user = rec.get("username", "") or "(无用户名)"
                pw = rec.get("password", "") or ""
                child = QTreeWidgetItem(host_node)
                child.setText(0, user)
                child.setText(1, pw)
                child.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    ("cred", host, idx),
                )

            host_node.setExpanded(True)

    def _on_context_menu(self, pos):
        item = self._tree.itemAt(pos)
        if item is None:
            return
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return

        kind = data[0]
        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)

        if kind == "cred":
            host, idx = data[1], data[2]
            act_del = menu.addAction(t("password.delete_one"))
            act_del.triggered.connect(
                lambda: self._delete_cred(host, idx))
        elif kind == "host":
            host = data[1]
            act_del_all = menu.addAction(t("password.delete_all"))
            act_del_all.triggered.connect(
                lambda: self._delete_host(host))
        else:
            return

        menu.exec(self._tree.viewport().mapToGlobal(pos))

    def _delete_cred(self, host, index):
        try:
            from password_hook import delete_credential
            delete_credential(host, index)
        except Exception as e:
            print("[settings] 删除密码失败:", e)
        self._reload()

    def _delete_host(self, host):
        try:
            from password_hook import delete_host
            delete_host(host)
        except Exception as e:
            print("[settings] 删除站点失败:", e)
        self._reload()


class SearchEngineDialog(QDialog):
    """搜索引擎管理：列表 + 添加 + 删除。不能选引擎（选在窗口里做）。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("engine.dialog_title"))
        self.setFixedSize(560, 460)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # ---- 列表 ----
        self._list = QListWidget(self)
        self._list.setStyleSheet(
            "QListWidget {"
            "  background: #fafafa;"
            "  border: 1px solid #e0e0e0;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  outline: none;"
            "}"
            "QListWidget::item { height: 32px; padding-left: 8px; }"
            "QListWidget::item:hover { background: #f0f0f0; }"
            "QListWidget::item:selected {"
            "  background: #e8f0fe; color: #2f5fd0;"
            "}"
        )
        self._list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self._list.customContextMenuRequested.connect(self._on_context_menu)
        root.addWidget(self._list, 1)

        self._empty_lbl = QLabel(t("engine.empty"), self)
        self._empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_lbl.setStyleSheet("color: #999; font-size: 13px;")
        self._empty_lbl.hide()
        root.addWidget(self._empty_lbl)

        # ---- 添加区 ----
        add_box = QWidget(self)
        add_layout = QVBoxLayout(add_box)
        add_layout.setContentsMargins(0, 0, 0, 0)
        add_layout.setSpacing(6)

        url_label = QLabel(t("engine.url_label"), self)
        url_label.setStyleSheet("font-size: 12px; color: #555;")
        add_layout.addWidget(url_label)

        row = QHBoxLayout()
        row.setSpacing(8)

        self._url_edit = QLineEdit(self)
        self._url_edit.setPlaceholderText(t("engine.url_placeholder"))
        self._url_edit.setFixedHeight(32)
        self._url_edit.setStyleSheet(
            "QLineEdit {"
            "  background: #fafafa;"
            "  border: 1px solid #dcdcdc;"
            "  border-radius: 6px;"
            "  padding: 0 10px;"
            "  font-size: 13px;"
            "}"
            "QLineEdit:focus { border: 1px solid #7aa7f0; }"
        )
        self._url_edit.returnPressed.connect(self._on_add)
        row.addWidget(self._url_edit, 1)

        add_btn = QPushButton(t("engine.add"), self)
        add_btn.setFixedWidth(90)
        add_btn.setFixedHeight(32)
        add_btn.clicked.connect(self._on_add)
        row.addWidget(add_btn)

        add_layout.addLayout(row)
        root.addWidget(add_box)

        # ---- 底部关闭 ----
        bottom = QHBoxLayout()
        bottom.addStretch(1)
        close_btn = QPushButton(t("common.close"), self)
        close_btn.setFixedWidth(90)
        close_btn.clicked.connect(self.accept)
        bottom.addWidget(close_btn)
        root.addLayout(bottom)

        self._reload()

    def _reload(self):
        self._list.clear()
        try:
            from search_engines import load_all
            engines = load_all()
        except Exception as e:
            print("[settings] 读引擎失败:", e)
            engines = []

        if not engines:
            self._empty_lbl.show()
            return
        self._empty_lbl.hide()

        for eng in engines:
            abbr = eng.get("abbr", "") or "??"
            url = eng.get("url", "")
            item = QListWidgetItem(f"[{abbr}]  {url}")
            item.setData(Qt.ItemDataRole.UserRole, url)
            self._list.addItem(item)

    def _on_add(self):
        url = self._url_edit.text().strip()
        if not url:
            return

        # 校验
        if "%s" not in url or not url.startswith(("http://", "https://")):
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(t("engine.url_invalid"))
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()
            return

        try:
            from search_engines import add_engine
            ok = add_engine(url)
        except Exception as e:
            print("[settings] 加引擎失败:", e)
            ok = None

        if not ok:
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(t("engine.url_invalid"))
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()
            return

        self._url_edit.clear()
        self._reload()

    def _on_context_menu(self, pos):
        item = self._list.itemAt(pos)
        if item is None:
            return
        url = item.data(Qt.ItemDataRole.UserRole)
        if not url:
            return

        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)

        act_del = menu.addAction(t("engine.delete"))
        act_del.triggered.connect(lambda: self._on_delete(url))
        menu.exec(self._list.viewport().mapToGlobal(pos))

    def _on_delete(self, url):
        try:
            from search_engines import remove_engine
            remove_engine(url)
        except Exception as e:
            print("[settings] 删引擎失败:", e)
        self._reload()


class PasswordBoxDialog(QDialog):
    """密码箱：按主域分组显示已保存密码，右键删除。明文显示。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("general.password_box"))
        self.setFixedSize(560, 480)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # ---- 安全提示 ----
        warn_lbl = QLabel(t("password.warning"), self)
        warn_lbl.setWordWrap(True)
        warn_lbl.setStyleSheet(
            "color: #c06000; background: #fff8e8;"
            "border: 1px solid #f0d8a0; border-radius: 6px;"
            "padding: 8px 10px; font-size: 12px;"
        )
        root.addWidget(warn_lbl)
        # ------------------

        self._tree = QTreeWidget(self)
        self._tree.setHeaderLabels(["网站 / 账号", "密码"])
        self._tree.setColumnWidth(0, 360)
        self._tree.setStyleSheet(
            "QTreeWidget {"
            "  background: #fafafa;"
            "  border: 1px solid #e0e0e0;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  outline: none;"
            "}"
            "QTreeWidget::item { height: 26px; }"
            "QTreeWidget::item:hover { background: #f0f0f0; }"
            "QTreeWidget::item:selected {"
            "  background: #e8f0fe; color: #2f5fd0;"
            "}"
        )
        self._tree.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._on_context_menu)
        root.addWidget(self._tree, 1)

        self._empty_lbl = QLabel(t("password.empty"), self)
        self._empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_lbl.setStyleSheet("color: #999; font-size: 13px;")
        self._empty_lbl.hide()
        root.addWidget(self._empty_lbl)

        bottom = QHBoxLayout()
        bottom.addStretch(1)
        close_btn = QPushButton(t("common.close"), self)
        close_btn.setFixedWidth(90)
        close_btn.clicked.connect(self.accept)
        bottom.addWidget(close_btn)
        root.addLayout(bottom)

        self._reload()

    def _reload(self):
        """从 passwords.json 重读，重建树。"""
        self._tree.clear()
        try:
            from password_hook import list_all
            data = list_all()
        except Exception as e:
            print("[settings] 读 passwords 失败:", e)
            data = {}

        if not data:
            self._empty_lbl.show()
            return
        self._empty_lbl.hide()

        for host, items in sorted(data.items()):
            if not isinstance(items, list) or not items:
                continue
            host_node = QTreeWidgetItem(self._tree)
            host_node.setText(0, host)
            host_node.setData(0, Qt.ItemDataRole.UserRole, ("host", host))
            font = host_node.font(0)
            font.setBold(True)
            host_node.setFont(0, font)

            for idx, rec in enumerate(items):
                user = rec.get("username", "") or "(无用户名)"
                pw = rec.get("password", "") or ""
                child = QTreeWidgetItem(host_node)
                child.setText(0, user)
                child.setText(1, pw)
                child.setData(
                    0,
                    Qt.ItemDataRole.UserRole,
                    ("cred", host, idx),
                )

            host_node.setExpanded(True)

    def _on_context_menu(self, pos):
        item = self._tree.itemAt(pos)
        if item is None:
            return
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return

        kind = data[0]
        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)

        if kind == "cred":
            host, idx = data[1], data[2]
            act_del = menu.addAction(t("password.delete_one"))
            act_del.triggered.connect(
                lambda: self._delete_cred(host, idx))
        elif kind == "host":
            host = data[1]
            act_del_all = menu.addAction(t("password.delete_all"))
            act_del_all.triggered.connect(
                lambda: self._delete_host(host))
        else:
            return

        menu.exec(self._tree.viewport().mapToGlobal(pos))

    def _delete_cred(self, host, index):
        try:
            from password_hook import delete_credential
            delete_credential(host, index)
        except Exception as e:
            print("[settings] 删除密码失败:", e)
        self._reload()

    def _delete_host(self, host):
        try:
            from password_hook import delete_host
            delete_host(host)
        except Exception as e:
            print("[settings] 删除站点失败:", e)
        self._reload()


class SearchEngineDialog(QDialog):
    """搜索引擎管理：列表 + 添加 + 删除。不能选引擎（选在窗口里做）。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(t("engine.dialog_title"))
        self.setFixedSize(560, 460)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        # ---- 列表 ----
        self._list = QListWidget(self)
        self._list.setStyleSheet(
            "QListWidget {"
            "  background: #fafafa;"
            "  border: 1px solid #e0e0e0;"
            "  border-radius: 6px;"
            "  font-size: 13px;"
            "  outline: none;"
            "}"
            "QListWidget::item { height: 32px; padding-left: 8px; }"
            "QListWidget::item:hover { background: #f0f0f0; }"
            "QListWidget::item:selected {"
            "  background: #e8f0fe; color: #2f5fd0;"
            "}"
        )
        self._list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self._list.customContextMenuRequested.connect(self._on_context_menu)
        root.addWidget(self._list, 1)

        self._empty_lbl = QLabel(t("engine.empty"), self)
        self._empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_lbl.setStyleSheet("color: #999; font-size: 13px;")
        self._empty_lbl.hide()
        root.addWidget(self._empty_lbl)

        # ---- 添加区 ----
        add_box = QWidget(self)
        add_layout = QVBoxLayout(add_box)
        add_layout.setContentsMargins(0, 0, 0, 0)
        add_layout.setSpacing(6)

        url_label = QLabel(t("engine.url_label"), self)
        url_label.setStyleSheet("font-size: 12px; color: #555;")
        add_layout.addWidget(url_label)

        row = QHBoxLayout()
        row.setSpacing(8)

        self._url_edit = QLineEdit(self)
        self._url_edit.setPlaceholderText(t("engine.url_placeholder"))
        self._url_edit.setFixedHeight(32)
        self._url_edit.setStyleSheet(
            "QLineEdit {"
            "  background: #fafafa;"
            "  border: 1px solid #dcdcdc;"
            "  border-radius: 6px;"
            "  padding: 0 10px;"
            "  font-size: 13px;"
            "}"
            "QLineEdit:focus { border: 1px solid #7aa7f0; }"
        )
        self._url_edit.returnPressed.connect(self._on_add)
        row.addWidget(self._url_edit, 1)

        add_btn = QPushButton(t("engine.add"), self)
        add_btn.setFixedWidth(90)
        add_btn.setFixedHeight(32)
        add_btn.clicked.connect(self._on_add)
        row.addWidget(add_btn)

        add_layout.addLayout(row)
        root.addWidget(add_box)

        # ---- 底部关闭 ----
        bottom = QHBoxLayout()
        bottom.addStretch(1)
        close_btn = QPushButton(t("common.close"), self)
        close_btn.setFixedWidth(90)
        close_btn.clicked.connect(self.accept)
        bottom.addWidget(close_btn)
        root.addLayout(bottom)

        self._reload()

    def _reload(self):
        self._list.clear()
        try:
            from search_engines import load_all
            engines = load_all()
        except Exception as e:
            print("[settings] 读引擎失败:", e)
            engines = []

        if not engines:
            self._empty_lbl.show()
            return
        self._empty_lbl.hide()

        for eng in engines:
            abbr = eng.get("abbr", "") or "??"
            url = eng.get("url", "")
            item = QListWidgetItem(f"[{abbr}]  {url}")
            item.setData(Qt.ItemDataRole.UserRole, url)
            self._list.addItem(item)

    def _on_add(self):
        url = self._url_edit.text().strip()
        if not url:
            return

        # 校验
        if "%s" not in url or not url.startswith(("http://", "https://")):
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(t("engine.url_invalid"))
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()
            return

        try:
            from search_engines import add_engine
            ok = add_engine(url)
        except Exception as e:
            print("[settings] 加引擎失败:", e)
            ok = None

        if not ok:
            box = QMessageBox(self)
            box.setWindowTitle(t("app.title"))
            box.setText(t("engine.url_invalid"))
            box.setIcon(QMessageBox.Icon.Warning)
            box.exec()
            return

        self._url_edit.clear()
        self._reload()

    def _on_context_menu(self, pos):
        item = self._list.itemAt(pos)
        if item is None:
            return
        url = item.data(Qt.ItemDataRole.UserRole)
        if not url:
            return

        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)

        act_del = menu.addAction(t("engine.delete"))
        act_del.triggered.connect(lambda: self._on_delete(url))
        menu.exec(self._list.viewport().mapToGlobal(pos))

    def _on_delete(self, url):
        try:
            from search_engines import remove_engine
            remove_engine(url)
        except Exception as e:
            print("[settings] 删引擎失败:", e)
        self._reload()