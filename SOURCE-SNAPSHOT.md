# NWbrowser 源码快照

> **给 AI 助手 / 新贡献者的代码地图。**
>
> 本文件把项目全部源码（`component/*.py`、`installer/*.py`、各 `.bat` /
> `.json` / `.spec` / 版本资源）拼成一份可全文检索的文档，目的是
> **一次读完整个项目**，不必逐个文件去 open —— 对 AI 助手尤其省 token。
>
> **怎么用**
> - **AI 助手**：先读这一个文件建立全局认知，需要改动时再打开对应的真实源码
> - **人**：Ctrl+F 全文搜索，比在 GitHub 上逐个点开文件快得多
>
> **注意**
> - 这是 **v1.0.0 的快照**，可能滞后于最新提交，**以实际源码为准**
> - 只在发版时重新生成，平时无需维护
> - 篇幅很长（2 万余行），网页渲染较慢，建议下载后本地查看

扫描目录：`src/`

## 项目结构

> **颜色说明**

>

> 🔴 标红：该文件/文件夹不读取内容

> ⬛ 标黑：文件夹内部全黑；文件隐身（不出现于下方内容区）

> 🟡 混杂：文件夹内部状态混杂（部分子项被标注）

>

> 以上颜色仅为用户在提取器里的手动标注，用于控制是否读取内容，

> 与文件中代码/文本的实际内容无关。

```
src/
    assets/
        backgrounds/
            spaceship.jpg
        fonts/
    component/
        i18n/
            en-US.json
            init.py
            zh-CN.json
        activity_watcher.py
        apppaths.py
        corner_mask.py
        dom_activity.py
        download_notify_dialog.py
        download_worker.py
        downloads_app.py
        downloads_store.py
        downloads_window.py
        favorites_menu.py
        favorites_store.py
        floating_bar.py
        font_scheme_handler.py
        history_hook.py
        history_store.py
        i18n.py
        inc_p_window.py
        incognito_window.py
        input_box.py
        ipc.py
        loader.py
        main_app.py
        notify_store.py
        password_hook.py
        personalize_dialog.py
        pinned_store.py
        popup_window.py
        rounded_menu.py
        search_engines.py
        search_icons.py
        settings.py
        settings_app.py
        settings_backend.py
        settings_pages.py
        settings_window.py
        styles.py
        theme.py
        title_bar.py
        window.py
        window_icon.py
    data/
        download_icon.ico
        icon.ico
        settings_icon.ico
    defaults/
        fixed/
        userdata/
            search_icons/
                baidu.com.png
                bing.com.png
                google.com.png
        favorites.json
        passwords.json
        search_engines.json
        settings.json
    fixed/
    installer/
        build_all.py
        make_icons.py
        setup.ico
        setup.py
        setup_header.png
        setup_version_info.txt
        uninstall.py
        uninstall_version_info.txt
    library/
    userdata/
        profile/
        search_icons/
            baidu.com.png
            bing.com.png
    .gitignore
    build_app.bat
    deploy.bat
    download fonts.bat
    LICENSE
    main.py
    NWbrowser.spec
    README.md
    requirements.txt
    run.bat
    search_engines.json
    THIRD-PARTY-NOTICES.txt
    version_info.txt
```

共输出 63 个文件的内容。

---

## 文件内容

### component\i18n\en-US.json (大小: 6643 | 修改时间: 2026-10-02 14:28:46 | 权限: 666)

```
{
    "_meta": {
        "code": "en-US",
        "name": "English"
    },

    "app.title": "Browser",

    "menu.personalize": "Personalize",
    "menu.settings": "Settings",
    "menu.language": "Language",
    "menu.downloads": "Downloads",
    "menu.restart": "Restart Window",
    "menu.about": "About",
    "menu.pin": "Pin",
    "menu.complete_notify": "Complete Notify",
    "menu.pin_full": "You can pin at most 24 sites. Please unpin one first.",

    "common.cancel": "Cancel",
    "common.ok": "OK",
    "common.close": "Close",
    "common.add": "Add",
    "common.delete": "Delete",
    "common.choose_dir": "Choose Directory",
    "common.need_restart": "Restart the window to take effect",

    "input.placeholder": "Enter URL",

    "tray.show_bar": "Show Floating Bar",
    "tray.hide_bar": "Hide Floating Bar",
    "tray.settings": "Settings",
    "tray.downloads": "Downloads",
    "tray.quit": "Quit",

    "nav.general": "General",
    "nav.history": "History",
    "nav.language": "Language",

    "general.sec_download": "Downloads",
    "general.download_dir": "Download File Location",
    "general.sec_password": "Passwords",
    "general.password_save": "Save Passwords",
    "general.password_save_hint": "Save passwords when login forms are submitted",
    "general.password_box": "Password Box",
    "general.password_box_hint": "View and delete saved passwords",
    "general.sec_engine": "Search Engines",
    "general.engine_manage": "Manage",
    "general.engine_manage_hint": "Add or remove search engines",

    "engine.dialog_title": "Search Engine Manager",
    "engine.empty": "No search engines",
    "engine.add": "Add",
    "engine.delete": "Delete",
    "engine.url_label": "Search URL (use %s for the query)",
    "engine.url_placeholder": "https://www.example.com/search?q=%s",
    "engine.url_invalid": "Invalid URL: must contain %s and start with http:// or https://",
    "engine.no_engine": "No search engine yet. Add one in Settings.",

    "password.warning": "The program is incomplete; passwords are stored in plain text. Do not save important passwords.",
    "password.panel_title": "Login Info",
    "password.save_current": "Save Current",
    "password.no_username": "(no username)",
    "password.empty": "No saved passwords",
    "password.delete_one": "Delete this",
    "password.delete_all": "Delete all for this site",
    "menu.unpin": "Unpin",
    "menu.incognito": "Incognito",

    "history.sec_history": "History",
    "history.save_history": "Save History",
    "history.history_days": "History Retention Days",

    "history.sec_cookie": "Cookie",
    "history.save_cookie": "Save Cookie",
    "history.save_cookie_hint": "When disabled, no cookies will be saved",

    "history.sec_whitelist": "Whitelist",
    "history.whitelist_hint": "Whitelisted websites can skip saving history.",
    "history.wl_add": "Add Website",
    "history.wl_del": "Delete Selected",
    "history.wl_dialog_title": "Add Whitelist Website",
    "history.wl_host_label": "Website Domain (e.g. example.com)",
    "history.wl_no_history": "Do Not Save History",

    "history.search_placeholder": "Search history…",
    "history.placeholder_host": "Website",
    "history.range_all": "All",
    "history.prev_page": "‹ Previous Page",
    "history.next_page": "Next Page ›",
    "history.select_all": "Select All",
    "history.delete_selected": "Delete Selected",
    "history.clear_cookie": "Clear Cookie",
    "history.page_label": "Page %d / %d",
    "history.delete_confirm": "Delete the %d selected records?",
    "history.clear_cookie_confirm": "Clear all cookies?\nSome will take effect only after restarting the browser.",
    "history.clear_cookie_done": "Cleared %d cookie files.",
    "history.clear_cookie_fail": "%d files are in use and will be cleared after restarting the browser.",

    "language.current": "Current Language",
    "language.switch_hint": "Click a language to switch. Close and reopen the settings window for it to take effect.",
    "language.export": "Export Language File",
    "language.export_hint": "Drag the icon to the desktop or a folder, or right-click to Save As.",
    "language.import_area": "Drag the translated JSON file here",
    "language.import_ok": "Language imported: %s",
    "language.import_fail": "Import failed: %s",
    "language.save_as": "Save As…",
    "language.save_dialog": "Save Language File",
    "language.delete_confirm": "Delete language %s?",
    "language.delete_default": "The default language cannot be deleted",
    "language.delete_current": "The current language cannot be deleted. Please switch to another language first",
    "language.delete_fail": "Delete failed: %s",

    "personalize.title": "Personalize",
    "personalize.theme_color": "Theme Color",
    "personalize.background": "Background Image",
    "personalize.pick_image": "Choose Image",
    "personalize.clear": "Clear",
    "personalize.clear_confirm_title": "Confirm Clear",
    "personalize.clear_confirm_text": "Clear all background images?",
    "personalize.delete": "Delete",

    "download.title": "Downloads",
    "download.empty": "No download records",
    "download.filename": "File Name",
    "download.status": "Status",
    "download.time": "Time",
    "download.path": "Save Location",
    "download.url": "Source URL",
    "download.status_downloading": "Downloading",
    "download.status_completed": "Completed",
    "download.status_failed": "Failed",
    "download.status_cancelled": "Cancelled",
    "download.status_missing": "File Not Found",
    "download.open_folder": "Open Containing Folder",
    "download.delete_file": "Delete File",
    "download.remove_record": "Remove Record",
    "download.clear_all": "Clear All Records",
    "download.clear_all_confirm": "Clear all download records? Files will not be deleted.",
    "download.notify": "Download Complete Notification",
    "download.notify_hint": "Show a notification in the bottom-right corner when a download completes",
    "download.delete_file_confirm": "Delete the file?\n%s",
    "download.delete_file_missing": "The file no longer exists.\nClear the record only?",
    "download.file_missing_hint": "The file does not exist or has been moved",
    "download.lightweight_warning": "Resume support is incomplete. Avoid downloading large files with this browser",
    "download.toast_title": "Download Complete",
    "download.toast_start_title": "Download Started",

    "about.title": "About"
}
```

### component\i18n\init.py (大小: 0 | 修改时间: 2026-10-02 20:53:35 | 权限: 666)

null

### component\i18n\zh-CN.json (大小: 6443 | 修改时间: 2026-10-02 14:28:36 | 权限: 666)

```
{
    "_meta": {
        "code": "zh-CN",
        "name": "简体中文"
    },

    "app.title": "浏览器",

    "menu.personalize": "个性化",
    "menu.settings": "设置",
    "menu.language": "语言",
    "menu.downloads": "下载",
    "menu.restart": "重启窗口",
    "menu.about": "关于",
    "menu.pin": "固定",
    "menu.complete_notify": "完成提醒",
    "menu.pin_full": "最多固定 24 个网站，请先取消一个",

    "common.cancel": "取消",
    "common.ok": "确定",
    "common.close": "关闭",
    "common.add": "添加",
    "common.delete": "删除",
    "common.choose_dir": "选择目录",
    "common.need_restart": "需重启窗口生效",

    "input.placeholder": "输入网址",

    "tray.show_bar": "显示悬浮条",
    "tray.hide_bar": "隐藏悬浮条",
    "tray.settings": "设置",
    "tray.downloads": "下载",
    "tray.quit": "退出",

    "nav.general": "常规",
    "nav.history": "历史",
    "nav.language": "语言",

    "general.sec_download": "下载",
    "general.download_dir": "下载文件位置",
    "general.sec_password": "密码",
    "general.password_save": "密码保存",
    "general.password_save_hint": "登录表单提交时保存密码",
    "general.password_box": "密码箱",
    "general.password_box_hint": "查看、删除已保存的密码",
    "general.sec_engine": "搜索引擎",
    "general.engine_manage": "管理",
    "general.engine_manage_hint": "添加或删除搜索引擎",

    "engine.dialog_title": "搜索引擎管理",
    "engine.empty": "暂无搜索引擎",
    "engine.add": "添加",
    "engine.delete": "删除",
    "engine.url_label": "搜索网址（用 %s 表示搜索词）",
    "engine.url_placeholder": "https://www.example.com/search?q=%s",
    "engine.url_invalid": "网址无效：必须含 %s，且以 http:// 或 https:// 开头",
    "engine.no_engine": "还没有搜索引擎，去设置里添加",

    "password.warning": "程序尚不完善，密码以明文保存，重要密码建议不要保存",
    "password.panel_title": "登录信息",
    "password.save_current": "保存当前信息",
    "password.no_username": "(无用户名)",
    "password.empty": "暂无保存的密码",
    "password.delete_one": "删除这条",
    "password.delete_all": "删除该站全部",
    "menu.unpin": "取消固定",
    "menu.incognito": "无痕",

    "history.sec_history": "历史记录",
    "history.save_history": "保存历史记录",
    "history.history_days": "历史记录保留天数",

    "history.sec_cookie": "Cookie",
    "history.save_cookie": "保存 Cookie",
    "history.save_cookie_hint": "关闭后所有 Cookie 都不保存",

    "history.sec_whitelist": "白名单",
    "history.whitelist_hint": "白名单网站可以不保存历史记录。",
    "history.wl_add": "添加网站",
    "history.wl_del": "删除选中",
    "history.wl_dialog_title": "添加白名单网站",
    "history.wl_host_label": "网站域名（例如 example.com）",
    "history.wl_no_history": "不保存历史记录",

    "history.search_placeholder": "查找历史记录…",
    "history.placeholder_host": "网站",
    "history.range_all": "全部",
    "history.prev_page": "‹ 上一页",
    "history.next_page": "下一页 ›",
    "history.select_all": "全选",
    "history.delete_selected": "删除选中",
    "history.clear_cookie": "清空 Cookie",
    "history.page_label": "第 %d / %d 页",
    "history.delete_confirm": "确认删除选中的 %d 条记录？",
    "history.clear_cookie_confirm": "确认清空所有 Cookie？\n部分需重启浏览器后生效。",
    "history.clear_cookie_done": "已清空 %d 个 Cookie 文件。",
    "history.clear_cookie_fail": "有 %d 个文件被占用，重启浏览器后清空。",

    "language.current": "当前语言",
    "language.switch_hint": "点选语言切换，关闭后重开设置窗口生效。",
    "language.export": "导出语言文件",
    "language.export_hint": "把图标拖到桌面或文件夹，或右键另存为。",
    "language.import_area": "把翻译好的 JSON 文件拖到这里",
    "language.import_ok": "语言已导入：%s",
    "language.import_fail": "导入失败：%s",
    "language.save_as": "另存为…",
    "language.save_dialog": "保存语言文件",
    "language.delete_confirm": "确认删除语言 %s？",
    "language.delete_default": "不能删除默认语言",
    "language.delete_current": "不能删除当前语言，请先切换到其他语言",
    "language.delete_fail": "删除失败：%s",

    "personalize.title": "个性化",
    "personalize.theme_color": "主题颜色",
    "personalize.background": "背景图片",
    "personalize.pick_image": "选择图片",
    "personalize.clear": "清空",
    "personalize.clear_confirm_title": "确认清空",
    "personalize.clear_confirm_text": "确认清空所有背景图片？",
    "personalize.delete": "删除",

    "download.title": "下载",
    "download.empty": "暂无下载记录",
    "download.filename": "文件名",
    "download.status": "状态",
    "download.time": "时间",
    "download.path": "保存位置",
    "download.url": "来源网址",
    "download.status_downloading": "下载中",
    "download.status_completed": "已完成",
    "download.status_failed": "失败",
    "download.status_cancelled": "已取消",
    "download.status_missing": "找不到文件",
    "download.open_folder": "打开所在文件夹",
    "download.delete_file": "删除文件",
    "download.remove_record": "清除记录",
    "download.clear_all": "清空全部记录",
    "download.clear_all_confirm": "确认清空所有下载记录？不会删除文件。",
    "download.notify": "下载完成提醒",
    "download.notify_hint": "下载完成后在屏幕右下角弹出提示",
    "download.delete_file_confirm": "确认删除文件？\n%s",
    "download.delete_file_missing": "文件已不存在。\n要只清除记录吗？",
    "download.file_missing_hint": "文件不存在或已被移动",
    "download.lightweight_warning": "断点续传不完善，避免用本浏览器下载大文件",
    "download.toast_title": "下载完成",
    "download.toast_start_title": "开始下载",

    "about.title": "关于"
}
```

### component\activity_watcher.py (大小: 1317 | 修改时间: 2026-09-27 23:40:54 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""全局前台窗口监听：发出 activeWindowChanged 信号。

只应在每个进程里创建一个实例（装在 QApplication 上）。
只监听 WindowActivate / WindowDeactivate，
以及 applicationStateChanged（切到别的程序）。
"""

from loader import *
from PyQt6.QtCore import pyqtSignal


class ActivityWatcher(QObject):
    activeWindowChanged = pyqtSignal(object)   # QWidget 或 None

    def __init__(self, app, parent=None):
        super().__init__(parent)
        self._app = app
        self._last = None
        app.installEventFilter(self)
        app.applicationStateChanged.connect(self._on_app_state)

    def eventFilter(self, obj, event):
        et = event.type()
        if et in (
            QEvent.Type.WindowActivate,
            QEvent.Type.WindowDeactivate,
        ):
            # 延后一拍，等 activeWindow 更新完再读
            QTimer.singleShot(0, self._emit)
        return super().eventFilter(obj, event)

    def _on_app_state(self, state):
        QTimer.singleShot(0, self._emit)

    def _emit(self):
        w = self._app.activeWindow()
        print(f"[watcher] emit active={w}")
        if w is not self._last:
            self._last = w
            self.activeWindowChanged.emit(w)
```

### component\apppaths.py (大小: 4674 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""打包兼容垫片 —— 全项目**唯一**新增的路径间接层。

背景
----
原代码到处写死::

    _HERE = os.path.dirname(os.path.abspath(__file__))
    _PROJECT_ROOT = os.path.dirname(_HERE)

源码运行时这没问题。打包（PyInstaller）后模块被塞进 PYZ，``__file__`` 变成
``<_MEIPASS>/xxx.pyc``，再取两上层目录就跑到程序目录的**外面**去了，
于是 settings.json / userdata / assets / i18n 全部找不到 —— 这正是打包后
"背景图没了、托盘空的、功能起不来"的根因。

这里把两种形态统一成两个常量
--------------------------
``RES_DIR``  只读资源根（assets/ data/ component/i18n/）
             源码 = 项目根；打包 = sys._MEIPASS
``APP_DIR``  可写数据根（settings.json history.json userdata/ fixed/ ...）
             源码 = 项目根；打包 = exe 所在目录

**源码模式下二者恒等于项目根目录**，与改造前完全一致，行为零变化。
打包后资源在 ``_internal/``（PyInstaller 自己管），用户数据躺在 exe 旁边，
和源码布局一眼对得上。

另外提供 :func:`role_command` ：把"起一个子进程"这件事在两种形态下统一。
源码是 ``python.exe component/xxx.py``，打包后磁盘上没有 .py，只能
``NWbrowser.exe --role xxx`` 复用同一个可执行文件。
"""

import os
import sys


# ======================================================================
# 运行形态
# ======================================================================
#: 是否运行在 PyInstaller 打包产物里
FROZEN = bool(getattr(sys, "frozen", False))

#: 源码模式下的项目根目录（apppaths.py 在 component/ 里，上两级）
_SOURCE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if FROZEN:
    # PyInstaller 6 onedir：datas/binaries 都在 _MEIPASS（即 _internal/）
    RES_DIR = getattr(sys, "_MEIPASS", None) or os.path.dirname(
        os.path.abspath(sys.executable)
    )
    # exe 所在目录。用户数据放这里，跟源码模式"数据在项目根"是一一对应的
    APP_DIR = os.path.dirname(os.path.abspath(sys.executable))
    # 打包后模块在顶层，没有 component/ 这个目录了
    COMPONENT_DIR = RES_DIR
else:
    RES_DIR = _SOURCE_ROOT
    APP_DIR = _SOURCE_ROOT
    COMPONENT_DIR = os.path.join(_SOURCE_ROOT, "component")


# ======================================================================
# 子进程角色
# ======================================================================
#: 角色 -> 源码模式下的脚本文件名
ROLE_SCRIPTS = {
    "bar": "floating_bar.py",
    "settings": "settings_app.py",
    "downloads": "downloads_app.py",
    "window": "window.py",
    "incognito": "incognito_window.py",
    "download-worker": "download_worker.py",
}


def role_command(role, *args):
    """返回 ``(program, arguments)``，直接喂给 ``QProcess``。

    源码模式：``python.exe <项目根>/component/<角色脚本> [args...]``
    打包模式：``NWbrowser.exe --role <角色> [args...]``
    """
    extra = [str(a) for a in args]

    if FROZEN:
        return sys.executable, ["--role", role] + extra

    script = ROLE_SCRIPTS.get(role)
    if script is None:
        raise ValueError("未知角色: %r" % (role,))
    return sys.executable, [os.path.join(COMPONENT_DIR, script)] + extra


def configure_child_proc(proc):
    """给一个 ``QProcess`` 配好标准输出通道。

    * 源码模式：``ForwardedChannels``，子进程输出直接打到终端，方便调试。
    * 打包模式：窗口程序**没有控制台**可转发，而且子进程会自己写
      ``nwbrowser-<角色>.log``；这里把子进程的标准输出/错误指到空设备，
      彻底绕开"转发管道句柄"这一整类问题（窗口程序里 std 句柄是无效的）。
    """
    try:
        from PyQt6.QtCore import QProcess
        if FROZEN:
            proc.setProcessChannelMode(
                QProcess.ProcessChannelMode.SeparateChannels
            )
            proc.setStandardOutputFile(QProcess.nullDevice())
            proc.setStandardErrorFile(QProcess.nullDevice())
        else:
            proc.setProcessChannelMode(
                QProcess.ProcessChannelMode.ForwardedChannels
            )
    except Exception:
        pass


if __name__ == "__main__":
    print("FROZEN        =", FROZEN)
    print("RES_DIR       =", RES_DIR)
    print("APP_DIR       =", APP_DIR)
    print("COMPONENT_DIR =", COMPONENT_DIR)

```

### component\corner_mask.py (大小: 1406 | 修改时间: 2026-09-21 02:44:22 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""盖在 WebView 之上、只画四个圆角的遮罩。"""

from loader import *
from theme import Theme


class CornerMask(QWidget):
    def __init__(self, parent,
                 radius=Theme.WEB_RADIUS,
                 bg_color=Theme.BG_COLOR):
        super().__init__(parent)
        self.radius = radius
        self.bg_color = bg_color
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 外矩形：整个遮罩区域
        outer = QPainterPath()
        outer.addRect(0, 0, self.width(), self.height())

        # 内圆角矩形：inset=0 时和外矩形在四条边重合，
        # outer - inner 的结果只在四个角有非零区域
        inset = 0
        inner = QPainterPath()
        inner.addRoundedRect(
            inset, inset,
            self.width() - 2 * inset,
            self.height() - 2 * inset,
            self.radius, self.radius,
        )

        painter.setBrush(self.bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(outer.subtracted(inner))
```

### component\dom_activity.py (大小: 9563 | 修改时间: 2026-10-02 10:34:41 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""DOM 节点监控：new / lazy 簇状态机。

规则（全部在 JS 里判定）：
  - 有用户操作（滚动、点击、键盘、URL 变化、加载）后 1000ms 内的插入 → lazy
  - 没有用户操作时的插入 → new
  - 每 300ms flush 一次，算一条记录
  - 窗口 10 条
  - IDLE 态：new >= 7 → 进入 W 态
  - W 态：lazy >= 7 → 非自然死亡（不提醒）
  - 5s 无新增：
        W 态   → 自然死亡（提醒）
        IDLE 态 → 自然死亡（不提醒）
  - 超时后清空窗口，回 IDLE

JS 通过 ipc.postMessage 上报以下事件：
  cluster_start
  enter_w
  natural_death          ← W 态自然死亡 → 触发 on_over（提醒 + 置顶）
  natural_death_idle
  lazy_death
  dom_added              ← 每次 flush 一条，附带统计数据

Python 侧只做事件接收与分派：
  - natural_death → 调用 on_over()
  - 其他事件     → 打日志
"""

from loader import *


# ======================================================================
# 注入的 JS
# ======================================================================
DOM_ACTIVITY_JS = r"""
(function() {
    if (window.__dom_new_lazy_test) return;
    window.__dom_new_lazy_test = true;

    var USER_ACTION_WINDOW_MS = 1000;
    var WINDOW_SIZE = 10;
    var A_RATIO_NORMAL = 7;
    var LAZY_CANCEL = 7;
    var CLUSTER_GAP_MS = 5000;

    var pending_new = 0;
    var pending_lazy = 0;
    var flush_scheduled = false;

    var window_records = [];
    var in_cluster = false;
    var in_w_state = false;
    var last_record_time = 0;

    var last_action_time = 0;

    function mark_action() {
        last_action_time = performance.now();
    }

    window.addEventListener('scroll', mark_action, true);
    document.addEventListener('click', mark_action, true);
    document.addEventListener('keydown', mark_action, true);
    document.addEventListener('mousedown', mark_action, true);

    var last_url = location.href;
    setInterval(function() {
        if (location.href !== last_url) {
            last_url = location.href;
            mark_action();
        }
    }, 200);

    window.addEventListener('load', mark_action);
    if (document.readyState === 'complete') {
        mark_action();
    }

    function report(msg) {
        try {
            if (window.ipc && window.ipc.postMessage) {
                window.ipc.postMessage(JSON.stringify(msg));
            }
        } catch (e) {}
    }

    function start_cluster() {
        in_cluster = true;
        in_w_state = false;
        window_records = [];
        report({ type: "cluster_start" });
    }

    function finish_cluster(reason) {
        if (!in_cluster) return;
        if (reason === "natural") {
            if (in_w_state) {
                report({ type: "natural_death" });
            } else {
                report({ type: "natural_death_idle" });
            }
        } else if (reason === "lazy") {
            report({ type: "lazy_death" });
        }
        in_cluster = false;
        in_w_state = false;
        window_records = [];
        last_record_time = 0;
    }

    // 5s 超时检查
    setInterval(function() {
        if (!in_cluster) return;
        if (last_record_time === 0) return;
        var gap = performance.now() - last_record_time;
        if (gap >= CLUSTER_GAP_MS) {
            finish_cluster("natural");
        }
    }, 500);

    function schedule_flush() {
        if (flush_scheduled) return;
        flush_scheduled = true;
        setTimeout(function() {
            flush_scheduled = false;
            if (pending_new > 0 || pending_lazy > 0) {
                var source = (pending_new >= pending_lazy) ? "new" : "lazy";
                var count = pending_new + pending_lazy;

                // 开簇
                if (!in_cluster) {
                    start_cluster();
                }

                window_records.push(source);
                if (window_records.length > WINDOW_SIZE) {
                    window_records.shift();
                }
                last_record_time = performance.now();

                var new_count = 0;
                var lazy_count = 0;
                for (var i = 0; i < window_records.length; i++) {
                    if (window_records[i] === "new") new_count++;
                    else if (window_records[i] === "lazy") lazy_count++;
                }

                report({
                    type: "dom_added",
                    source: source,
                    count: count,
                    win: window_records.length,
                    new_count: new_count,
                    lazy_count: lazy_count,
                    in_w: in_w_state,
                });

                if (window_records.length >= WINDOW_SIZE) {
                    if (!in_w_state && new_count >= A_RATIO_NORMAL) {
                        in_w_state = true;
                        report({ type: "enter_w" });
                    } else if (in_w_state && lazy_count >= LAZY_CANCEL) {
                        finish_cluster("lazy");
                    }
                }

                pending_new = 0;
                pending_lazy = 0;
            }
        }, 300);
    }

    function install_dom_observer() {
        var target = document.body;
        if (!target) {
            setTimeout(install_dom_observer, 200);
            return;
        }
        var mo = new MutationObserver(function(mutations) {
            var now = performance.now();
            var is_lazy = (now - last_action_time < USER_ACTION_WINDOW_MS);

            for (var i = 0; i < mutations.length; i++) {
                var m = mutations[i];
                if (m.type !== "childList") continue;
                if (m.addedNodes.length === 0) continue;

                var n = m.addedNodes.length;
                if (is_lazy) {
                    pending_lazy += n;
                } else {
                    pending_new += n;
                }
            }
            if (pending_new > 0 || pending_lazy > 0) {
                schedule_flush();
            }
        });
        mo.observe(target, { childList: true, subtree: true });
        report({ type: "dom_observer_installed" });
    }

    install_dom_observer();
})();
"""


# ======================================================================
# Python 侧监控器
# ======================================================================
class DomActivityMonitor(QObject):
    """接收 JS 状态机上报的事件，分派回调。

    window 必须提供：
      * _on_js_message 里把 type 属于本监控器的事件转发给 feed()
      * 一个回调 on_over（W 态自然死亡时调用，用于提醒 + 置顶）

    用法：
        self._dom_monitor = DomActivityMonitor(self, self._on_dom_over)
        self._dom_monitor.start()
        ...
        self._dom_monitor.feed(data)   # data 是 dict
        self._dom_monitor.stop()
    """

    EVT_CLUSTER_START      = "cluster_start"
    EVT_ENTER_W            = "enter_w"
    EVT_NATURAL_DEATH      = "natural_death"
    EVT_NATURAL_DEATH_IDLE = "natural_death_idle"
    EVT_LAZY_DEATH         = "lazy_death"
    EVT_DOM_ADDED          = "dom_added"

    # 需要转发给 feed 的所有 type
    TYPES = (
        EVT_CLUSTER_START,
        EVT_ENTER_W,
        EVT_NATURAL_DEATH,
        EVT_NATURAL_DEATH_IDLE,
        EVT_LAZY_DEATH,
        EVT_DOM_ADDED,
    )

    def __init__(self, parent, on_over):
        super().__init__(parent)
        self._parent = parent
        self._on_over = on_over
        self._active = False

    def start(self):
        self._active = True
        print("[dom] monitor started")

    def stop(self):
        self._active = False
        print("[dom] monitor stopped")

    def is_active(self):
        return self._active

    def feed(self, data):
        """收到 JS 上报的事件（dict）。"""
        if not self._active:
            return
        if not isinstance(data, dict):
            return

        t = data.get("type")

        if t == self.EVT_CLUSTER_START:
            print("[dom] cluster_start")
            return

        if t == self.EVT_ENTER_W:
            print("[dom] enter_w")
            return

        if t == self.EVT_NATURAL_DEATH:
            print("[dom] natural_death → 提醒 + 置顶")
            try:
                self._on_over()
            except Exception as e:
                import traceback
                print("[dom] on_over 回调异常:")
                traceback.print_exc()
            return

        if t == self.EVT_NATURAL_DEATH_IDLE:
            print("[dom] natural_death_idle（不提醒）")
            return

        if t == self.EVT_LAZY_DEATH:
            print("[dom] lazy_death（不提醒）")
            return

        if t == self.EVT_DOM_ADDED:
            source = data.get("source", "?")
            count = data.get("count", 0)
            win = data.get("win", 0)
            new_c = data.get("new_count", 0)
            lazy_c = data.get("lazy_count", 0)
            in_w = data.get("in_w", False)
            print(f"[dom] [{source}] +{count} win={win} "
                  f"new={new_c} lazy={lazy_c} W={in_w}")
            return
```

### component\download_notify_dialog.py (大小: 8783 | 修改时间: 2026-10-02 18:21:29 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""右下角下载通知弹窗。两种模式：

    MODE_START    开始下载   —— 显示文件名+大小，3 秒自动收回
    MODE_DONE     下载完成   —— 显示文件名，整块可点，5 秒自动收回

属于下载进程。弹窗从屏幕底部外侧滑入右下角，滑入 300ms，滑出 200ms。
多个弹窗同时存在时从下往上堆叠，每个间距 10px。

不阻塞事件循环。鼠标悬停时暂停自动收回计时。
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
from i18n import t


# ======================================================================
# 弹窗本体
# ======================================================================
class DownloadNotifyDialog(QWidget):

    MODE_START = "start"
    MODE_DONE = "done"

    WIDTH = 320
    PAD = 16
    RADIUS = 12
    MARGIN = 20
    STACK_GAP = 10

    SLIDE_IN_MS = 300
    SLIDE_OUT_MS = 200

    AUTO_HIDE_START_MS = 2000
    AUTO_HIDE_DONE_MS = 2000

    _instances = []

    def __init__(self, mode, parent=None, **kwargs):
        super().__init__(parent)

        self.mode = mode
        self.url = kwargs.get("url", "")
        self.window_id = kwargs.get("window_id", "")
        self.filename = kwargs.get("filename", "") or "download"
        self.total = int(kwargs.get("total", -1) or -1)
        self.dir = kwargs.get("dir", "")
        self.on_click = kwargs.get("on_click", None)

        self._drag_start = None
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._on_auto_hide)

        self._anim = None
        self._closing = False

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedWidth(self.WIDTH)

        self._build_ui()
        self._adjust_height()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            self.PAD, self.PAD, self.PAD, self.PAD
        )
        layout.setSpacing(8)

        self._title_lbl = QLabel()
        f = self._title_lbl.font()
        f.setPointSize(10)
        f.setBold(True)
        self._title_lbl.setFont(f)
        self._title_lbl.setStyleSheet("color: #e6e6e6; background: transparent;")
        layout.addWidget(self._title_lbl)

        self._name_lbl = QLabel(self.filename)
        self._name_lbl.setWordWrap(True)
        self._name_lbl.setStyleSheet(
            "color: #cccccc; font-size: 12px; background: transparent;"
        )
        layout.addWidget(self._name_lbl)

        if self.mode == self.MODE_START:
            self._build_start(layout)
        elif self.mode == self.MODE_DONE:
            self._build_done(layout)

    def _build_start(self, layout):
        self._title_lbl.setText(t("download.toast_start_title"))

        size_text = ""
        if self.total > 0:
            size_text = self._fmt_size(self.total)
        self._size_lbl = QLabel(size_text)
        self._size_lbl.setStyleSheet(
            "color: #999999; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self._size_lbl)

    def _build_done(self, layout):
        self._title_lbl.setText(t("download.toast_title"))

        self._hint_lbl = QLabel(t("download.open_folder"))
        self._hint_lbl.setStyleSheet(
            "color: #7fb3ff; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self._hint_lbl)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _adjust_height(self):
        self.adjustSize()
        self.setFixedWidth(self.WIDTH)

    def _fmt_size(self, n):
        n = int(n)
        if n < 1024:
            return f"{n} B"
        if n < 1024 * 1024:
            return f"{n / 1024:.1f} KB"
        if n < 1024 * 1024 * 1024:
            return f"{n / 1024 / 1024:.2f} MB"
        return f"{n / 1024 / 1024 / 1024:.2f} GB"

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        painter.setBrush(QColor(40, 40, 40, 235))
        painter.setPen(QPen(QColor(90, 90, 90, 180), 1))
        painter.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

    def _target_pos(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() - self.MARGIN
        below_count = 0
        for d in DownloadNotifyDialog._instances:
            if d is self:
                continue
            below_count += 1
        y = screen.bottom() - self.height() - self.MARGIN
        y -= below_count * (self.height() + self.STACK_GAP)
        if y < screen.top() + self.MARGIN:
            y = screen.top() + self.MARGIN
        return QPoint(x, y)

    def _offscreen_pos(self):
        screen = QApplication.primaryScreen().availableGeometry()
        target = self._target_pos()
        return QPoint(target.x(), screen.bottom() + 10)

    def show_animated(self):
        DownloadNotifyDialog._instances.append(self)
        start = self._offscreen_pos()
        end = self._target_pos()
        self.move(start)
        self.show()
        self.raise_()

        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(self.SLIDE_IN_MS)
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim.start()

        ms = self._auto_hide_ms()
        if ms > 0:
            self._hide_timer.start(ms)

    def hide_animated(self):
        if self._closing:
            return
        self._closing = True
        self._hide_timer.stop()

        start = self.pos()
        end = self._offscreen_pos()

        self._anim = QPropertyAnimation(self, b"pos", self)
        self._anim.setDuration(self.SLIDE_OUT_MS)
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self._anim.finished.connect(self._on_hide_finished)
        self._anim.start()

    def _on_hide_finished(self):
        try:
            if self in DownloadNotifyDialog._instances:
                DownloadNotifyDialog._instances.remove(self)
        except Exception:
            pass
        self.close()
        self.deleteLater()

    def _auto_hide_ms(self):
        if self.mode == self.MODE_START:
            return self.AUTO_HIDE_START_MS
        if self.mode == self.MODE_DONE:
            return self.AUTO_HIDE_DONE_MS
        return 0

    def _on_auto_hide(self):
        self.hide_animated()

    def enterEvent(self, event):
        self._hide_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        ms = self._auto_hide_ms()
        if ms > 0 and not self._closing:
            self._hide_timer.start(ms)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.mode == self.MODE_DONE:
                self._open_folder()
                self.hide_animated()
            elif self.mode == self.MODE_START:
                # 点击打开下载窗口
                if self.on_click is not None:
                    try:
                        self.on_click()
                    except Exception as e:
                        print("[notify] on_click 回调失败:", e)
                self.hide_animated()

    def _open_folder(self):
        path = self.dir
        if not path or not os.path.isdir(path):
            try:
                from settings_backend import SettingsBackend
                path = SettingsBackend().get_download_dir() or ""
            except Exception:
                path = ""
        if not path or not os.path.isdir(path):
            from PyQt6.QtCore import QStandardPaths
            path = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DownloadLocation
            )
        if path and os.path.isdir(path):
            try:
                os.startfile(path)
            except Exception as e:
                print("[notify] 打开目录失败:", e)
```

### component\download_worker.py (大小: 8777 | 修改时间: 2026-09-26 23:23:43 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""独立下载子进程：纯命令行 HTTP 请求，不碰浏览器。

由 window.py 启动。启动后不立刻下载，先等 window 发来
MSG_DOWNLOAD_START_WORKER（带 Cookie），收到后才开始。

主线程跑 Qt 事件循环收 IPC，下载在子线程。
主线程用 QTimer 轮询 _start_event，不用 threading.Event.wait 阻塞。

退出码：
  0   成功
  1   失败
  2   被取消
"""

import sys
import os
import json
import time
import argparse
import threading
import urllib.request
import urllib.error
from urllib.parse import urlparse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from ipc import (
    IpcClient, IpcServer,
    ROLE_DOWNLOADS,
    window_channel,
    MSG_DOWNLOAD_PROGRESS, MSG_DOWNLOAD_DONE,
    MSG_DOWNLOAD_START,
    MSG_DOWNLOAD_CANCEL_WORKER,
    MSG_DOWNLOAD_START_WORKER,
)
from loader import QApplication, QTimer


_cancel_flag = threading.Event()
_start_event = threading.Event()
_start_cookie = {"value": ""}


class _Cancelled(Exception):
    pass


def _make_opener(cookie, referer, user_agent):
    opener = urllib.request.build_opener()
    headers = []
    if cookie:
        headers.append(("Cookie", cookie))
    if referer:
        headers.append(("Referer", referer))
    if user_agent:
        headers.append(("User-Agent", user_agent))
    else:
        headers.append(("User-Agent", "Mozilla/5.0"))
    opener.addheaders = headers
    return opener


def _download(url, path, referer, user_agent, window_id):
    cookie = _start_cookie["value"]
    part_path = path + ".part"

    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        try:
            os.makedirs(parent, exist_ok=True)
        except Exception as e:
            return False, f"创建目录失败: {e}"

    opener = _make_opener(cookie, referer, user_agent)

    try:
        resp = opener.open(url, timeout=30)
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"URLError: {e.reason}"
    except Exception as e:
        return False, f"打开失败: {e}"

    try:
        total = int(resp.headers.get("Content-Length", -1))
    except Exception:
        total = -1

    received = 0
    last_report = 0.0

    _send_start(url, path, total, window_id)

    try:
        with open(part_path, "wb") as f:
            while True:
                if _cancel_flag.is_set():
                    raise _Cancelled()
                try:
                    chunk = resp.read(64 * 1024)
                except Exception as e:
                    return False, f"读取出错: {e}"
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                now = time.time()
                if now - last_report >= 0.5:
                    last_report = now
                    _send_progress(url, path, received, total, window_id)

    except _Cancelled:
        try:
            if os.path.isfile(part_path):
                os.remove(part_path)
        except Exception:
            pass
        _send_done(url, path, success=False, delete_partial=False,
                   window_id=window_id)
        return False, "cancelled"

    except Exception as e:
        try:
            if os.path.isfile(part_path):
                os.remove(part_path)
        except Exception:
            pass
        _send_done(url, path, success=False, delete_partial=False,
                   window_id=window_id)
        return False, f"写入出错: {e}"

    finally:
        try:
            resp.close()
        except Exception:
            pass

    try:
        if os.path.isfile(path):
            os.remove(path)
        os.rename(part_path, path)
    except Exception as e:
        return False, f"重命名失败: {e}"

    _send_progress(url, path, received, total if total > 0 else received,
                   window_id)
    _send_done(url, path, success=True, delete_partial=False,
               window_id=window_id)
    return True, "ok"


def _send_start(url, path, total, window_id):
    try:
        payload = json.dumps({
            "url": url,
            "path": path,
            "filename": os.path.basename(path),
            "total": total,
            "notify": True,
            "window_id": window_id,
        }, ensure_ascii=False)
        IpcClient.send_to_role(
            ROLE_DOWNLOADS, MSG_DOWNLOAD_START,
            payload.encode("utf-8"),
        )
    except Exception as e:
        print(f"[worker] 发开始失败: {e}")


def _send_progress(url, path, received, total, window_id):
    try:
        payload = json.dumps({
            "url": url,
            "path": path,
            "received": received,
            "total": total,
        }, ensure_ascii=False)
        IpcClient.send_to_role(
            ROLE_DOWNLOADS, MSG_DOWNLOAD_PROGRESS,
            payload.encode("utf-8"),
        )
    except Exception as e:
        print(f"[worker] 发进度失败: {e}")


def _send_done(url, path, success, delete_partial, window_id):
    try:
        payload = json.dumps({
            "url": url,
            "path": path,
            "success": bool(success),
            "delete_partial": bool(delete_partial),
        }, ensure_ascii=False)
        IpcClient.send_to_role(
            ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE,
            payload.encode("utf-8"),
        )
    except Exception as e:
        print(f"[worker] 发完成失败: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--window-id", default="")
    parser.add_argument("--referer", default="")
    parser.add_argument("--user-agent", default="")
    args = parser.parse_args()

    app = QApplication(sys.argv)

    my_channel = window_channel(args.window_id) + "_worker"

    def on_message(msg_type, payload):
        if msg_type == MSG_DOWNLOAD_START_WORKER:
            try:
                data = json.loads(payload.decode("utf-8"))
                _start_cookie["value"] = data.get("cookie", "") or ""
            except Exception:
                _start_cookie["value"] = ""
            print(f"[worker] 收到开始指令，cookie 长度="
                  f"{len(_start_cookie['value'])}")
            _start_event.set()
        elif msg_type == MSG_DOWNLOAD_CANCEL_WORKER:
            print("[worker] 收到取消")
            _cancel_flag.set()
            _start_event.set()

    server = IpcServer(my_channel, on_message, role=my_channel)
    if not server.start():
        print("[worker] 监听失败，退出")
        sys.exit(1)

    state = {
        "started": False,
        "done": False,
        "ok": False,
        "msg": "timeout",
    }

    def _do_download():
        ok, msg = _download(
            args.url, args.path,
            args.referer, args.user_agent,
            args.window_id,
        )
        state["ok"] = ok
        state["msg"] = msg
        state["done"] = True

    def check_state():
        if state["done"]:
            try:
                server.stop()
            except Exception:
                pass
            app.quit()
            return

        if _start_event.is_set() and not state["started"]:
            if _cancel_flag.is_set():
                state["done"] = True
                state["msg"] = "cancelled"
                try:
                    server.stop()
                except Exception:
                    pass
                app.quit()
                return
            state["started"] = True
            threading.Thread(target=_do_download, daemon=True).start()

        QTimer.singleShot(100, check_state)

    QTimer.singleShot(100, check_state)

    def timeout_check():
        if not state["started"] and not state["done"]:
            print("[worker] 等待开始指令超时")
            state["done"] = True
            state["msg"] = "timeout"
            try:
                server.stop()
            except Exception:
                pass
            app.quit()

    QTimer.singleShot(60000, timeout_check)

    app.exec()

    if state["ok"]:
        sys.exit(0)
    elif state["msg"] == "cancelled":
        sys.exit(2)
    else:
        print(f"[worker] 失败: {state['msg']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### component\downloads_app.py (大小: 10083 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""下载进程：常驻。管下载窗口 + 右下角弹窗 + 下载记录。

由托盘启动。监听 CHANNEL_DOWNLOADS。

  - MSG_OPEN_DOWNLOADS / MSG_DOWNLOADS_SHOW   显示下载窗口
  - MSG_DOWNLOAD_START                         worker 通知"下载已开始"，
                                               建记录 + 弹开始窗
  - MSG_DOWNLOAD_PROGRESS                      worker 报进度
  - MSG_DOWNLOAD_DONE                          worker / window 报完成
  - MSG_DOWNLOADS_REFRESH                      刷新下载窗口
  - MSG_LANGUAGE_CHANGED                       切换语言

实际下载在 window 进程启动的 download_worker.py 子进程里，
本进程只负责记录、显示、弹窗，不自己下载。
"""

import sys
import os
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths
from i18n import t
from ipc import (
    IpcServer, IpcClient,
    CHANNEL_DOWNLOADS, ROLE_DOWNLOADS,
    MSG_OPEN_DOWNLOADS, MSG_DOWNLOADS_SHOW, MSG_DOWNLOADS_REFRESH,
    MSG_DOWNLOAD_START, MSG_DOWNLOAD_PROGRESS, MSG_DOWNLOAD_DONE,
    MSG_LANGUAGE_CHANGED, MSG_QUIT,
)
from i18n import load as i18n_load
from settings_backend import SettingsBackend

from download_notify_dialog import DownloadNotifyDialog


# ======================================================================
# 入口
# ======================================================================
def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 任务栏：本进程独立 AppUserModelID
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "MyBrowser.Downloads"
        )
    except Exception as e:
        print("[downloads] 设置 AppUserModelID 失败:", e)

    # 图标
    _icon_path = os.path.join(
        apppaths.RES_DIR, "data", "download_icon.ico"
    )
    _icon = QIcon(_icon_path) if os.path.isfile(_icon_path) else QIcon()
    if not _icon.isNull():
        app.setWindowIcon(_icon)
    else:
        print(f"[downloads] 图标加载失败或不存在: {_icon_path}")

    try:
        i18n_load(SettingsBackend().get_language())
    except Exception as e:
        print("[downloads] 加载语言失败:", e)

    from downloads_window import DownloadsWindow

    win = DownloadsWindow()

    # 窗口图标
    if not _icon.isNull():
        win.setWindowIcon(_icon)

    try:
        win.set_notify_state(SettingsBackend().get_download_notify())
    except Exception:
        pass

    def _notify_on():
        try:
            return bool(SettingsBackend().get_download_notify())
        except Exception:
            return False

    def on_message(msg_type, payload):
        # ---- 显示下载窗口 ----
        if msg_type in (MSG_OPEN_DOWNLOADS, MSG_DOWNLOADS_SHOW):
            win.reload_list()
            win.show()
            win.raise_()
            win.activateWindow()
            return

        # ---- 刷新下载窗口 ----
        if msg_type == MSG_DOWNLOADS_REFRESH:
            if win.isVisible():
                win.reload_list()
            return

        # ---- 下载开始：建记录 + 弹开始窗 ----
        if msg_type == MSG_DOWNLOAD_START:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                data = {}

            url = data.get("url", "")
            path = data.get("path", "")
            filename = data.get("filename", "")
            total = int(data.get("total", -1))
            notify = bool(data.get("notify", False))
            window_id = data.get("window_id", "")

            if not url:
                return

            if not filename:
                filename = os.path.basename(path) or "download"

            try:
                from downloads_store import add_download
                add_download(
                    url, path, filename,
                    status="downloading",
                    window_id=window_id,
                )
            except Exception as e:
                print("[downloads] 建记录失败:", e)

            if notify and _notify_on():
                try:
                    def _open_downloads_win():
                        win.reload_list()
                        win.show()
                        win.raise_()
                        win.activateWindow()

                    dlg = DownloadNotifyDialog(
                        mode=DownloadNotifyDialog.MODE_START,
                        url=url,
                        filename=filename,
                        total=total,
                        on_click=_open_downloads_win,
                    )
                    dlg.show_animated()
                except Exception as e:
                    print("[downloads] 开始弹窗失败:", e)

            if win.isVisible():
                win.reload_list()
            return

        # ---- 进度 ----
        if msg_type == MSG_DOWNLOAD_PROGRESS:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                data = {}

            url = data.get("url", "")
            received = int(data.get("received", 0))
            total = int(data.get("total", -1))

            if not url:
                return

            try:
                from downloads_store import update_download_progress
                update_download_progress(url, received, total)
            except Exception as e:
                print("[downloads] 更新进度失败:", e)

            if win.isVisible():
                win.reload_list()
            return

        # ---- 完成 / 失败 ----
        if msg_type == MSG_DOWNLOAD_DONE:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                data = {}

            url = data.get("url", "")
            path = data.get("path", "")
            success = bool(data.get("success", False))
            delete_partial = bool(data.get("delete_partial", False))

            if not url:
                return

            if not path:
                try:
                    from downloads_store import get_download_by_url
                    rec = get_download_by_url(url)
                    if rec:
                        path = rec.get("path", "")
                except Exception:
                    pass

            try:
                from downloads_store import update_download_status
                if success and path:
                    update_download_status(url, path, "completed")
                else:
                    update_download_status(url, path or "", "failed")
            except Exception as e:
                print("[downloads] 更新状态失败:", e)

            if delete_partial and path:
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                        print(f"[downloads] 已删主文件 {path!r}")
                except Exception as e:
                    print("[downloads] 删主文件失败:", e)
                try:
                    part = path + ".part"
                    if os.path.isfile(part):
                        os.remove(part)
                        print(f"[downloads] 已删 .part {part!r}")
                except Exception as e:
                    print("[downloads] 删 .part 失败:", e)

            if success and path and _notify_on():
                try:
                    dlg = DownloadNotifyDialog(
                        mode=DownloadNotifyDialog.MODE_DONE,
                        url=url,
                        filename=os.path.basename(path),
                        dir=os.path.dirname(path),
                    )
                    dlg.show_animated()
                except Exception as e:
                    print("[downloads] 完成弹窗失败:", e)

            if win.isVisible():
                win.reload_list()
            return

        # ---- 切换语言 ----
        if msg_type == MSG_LANGUAGE_CHANGED:
            try:
                code = payload.decode("utf-8")
                i18n_load(code)
                if hasattr(win, "_refresh_texts"):
                    win._refresh_texts()
                win.reload_list()
            except Exception as e:
                print("[downloads] 切换语言失败:", e)
            return

        # ---- 退出 ----
        if msg_type == MSG_QUIT:
            app.quit()

    server = IpcServer(
        CHANNEL_DOWNLOADS, on_message, role=ROLE_DOWNLOADS
    )
    if not server.start():
        print("[downloads] 已有实例在运行，退出")
        sys.exit(0)

    # 上一次会话残留的"下载中"记录：只要没有任何存活窗口（说明对应
    # worker 也死了），就把它们标记成失败，避免进度条永远卡住。
    try:
        from ipc import find_windows, _pid_alive
        live = any(_pid_alive(e.get("pid"))
                   for e in find_windows().values())
        if not live:
            from downloads_store import mark_stale_downloads_failed
            if mark_stale_downloads_failed():
                print("[downloads] 已清理上次会话残留的下载记录")
    except Exception as e:
        print("[downloads] 清理残留记录失败:", e)

    # 下载进程是常驻的，一旦事件循环退出（不管是正常还是异常），
    # 下载记录 / 进度 / 完成弹窗就全失效了 —— 所以退出码必须留痕。
    print("[downloads] 进入事件循环")
    _exit_code = app.exec()
    print(f"[downloads] 事件循环退出 code={_exit_code}")
    sys.exit(_exit_code)


if __name__ == "__main__":
    main()
```

### component\downloads_store.py (大小: 5745 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""下载记录存储。读写项目根目录下的 downloads.json。

记录结构：
    [
        {
            "url": "https://example.com/file.zip",
            "path": "C:/Users/xxx/Downloads/file.zip",
            "filename": "file.zip",
            "time": 1758600000.0,
            "status": "completed",
            "progress": 100,
            "total": 10485760,
            "received": 10485760,
            "window_id": "df-0"
        },
        ...
    ]

status 取值：
    "downloading"  下载中
    "completed"    已完成
    "failed"       失败
    "cancelled"    已取消
"""

import os
import json
import time

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "downloads.json")

# 最多保留多少条
MAX_RECORDS = 500


# ======================================================================
# 底层读写
# ======================================================================
def _load():
    try:
        if os.path.isfile(STORE_PATH):
            with open(STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def _save(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ======================================================================
# 对外接口
# ======================================================================
def load_downloads():
    """读全部记录。返回 list。"""
    return _load()


def add_download(url, path, filename, status="downloading", window_id=""):
    """新增或更新一条记录。

    如果同 url 同 path 已有，就更新状态和时间，不重复加。
    新记录插在最前面。

    window_id: 发起下载的窗口进程 id（如 "df-0"），
               取消时用来定向转发给对应 window。
    """
    data = _load()

    for item in data:
        if item.get("url") == url and item.get("path") == path:
            item["status"] = status
            item["time"] = time.time()
            item["filename"] = filename or item.get("filename", "")
            item["window_id"] = window_id or item.get("window_id", "")
            # 重置进度
            item["progress"] = 0
            item["total"] = 0
            item["received"] = 0
            _save(data)
            return

    data.insert(0, {
        "url": url or "",
        "path": path or "",
        "filename": filename or "",
        "time": time.time(),
        "status": status,
        "progress": 0,
        "total": 0,
        "received": 0,
        "window_id": window_id or "",
    })

    if len(data) > MAX_RECORDS:
        data = data[:MAX_RECORDS]

    _save(data)


def update_download_status(url, path, status):
    """按 url + path 定位记录，改状态。path 为空时按 url 匹配所有。"""
    data = _load()
    changed = False
    for item in data:
        if item.get("url") != url:
            continue
        if path and item.get("path") != path:
            continue
        item["status"] = status
        changed = True
    if changed:
        _save(data)


def update_download_progress(url, received, total):
    """更新下载进度。

    received: 已收字节
    total: 总字节。为 0 表示未知，progress 记 0。
    """
    data = _load()
    changed = False
    received = int(received)
    total = int(total)

    for item in data:
        if item.get("url") != url:
            continue
        item["received"] = received
        item["total"] = total
        if total > 0:
            item["progress"] = int(received * 100 / total)
        else:
            item["progress"] = 0
        changed = True
    if changed:
        _save(data)


def get_download_by_url(url):
    """按 url 找记录。返回 dict 或 None。"""
    if not url:
        return None
    data = _load()
    for item in data:
        if item.get("url") == url:
            return item
    return None


def remove_download_by_index(index):
    """按列表索引删除一条记录。"""
    data = _load()
    if 0 <= index < len(data):
        data.pop(index)
        _save(data)


def clear_downloads():
    """清空所有记录。不删文件。"""
    _save([])


def mark_stale_downloads_failed():
    """把还停留在 downloading 状态的记录标记为 failed。

    用于下载管理进程启动时清理上一轮会话的残留：上一轮没跑完就退出的
    下载（对应的窗口 / worker 都已经死了），如果一直留在"下载中"，
    进度条会永远卡着不动。
    """
    data = _load()
    changed = False
    for item in data:
        if item.get("status") == "downloading":
            item["status"] = "failed"
            changed = True
    if changed:
        _save(data)
    return changed


def file_status(path):
    """检查文件状态。

    返回:
        "ok"       父目录存在且文件存在
        "missing"  父目录不存在，或文件不存在
    """
    if not path:
        return "missing"

    try:
        parent = os.path.dirname(path)
        if not parent:
            return "ok" if os.path.isfile(path) else "missing"

        if not os.path.isdir(parent):
            return "missing"

        if not os.path.isfile(path):
            return "missing"

        return "ok"
    except Exception:
        return "missing"
```

### component\downloads_window.py (大小: 21010 | 修改时间: 2026-09-26 17:40:22 | 权限: 666)

```
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
```

### component\favorites_menu.py (大小: 9402 | 修改时间: 2026-10-02 18:51:12 | 权限: 666)

```
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
```

### component\favorites_store.py (大小: 2999 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""收藏存储：读写项目根目录下的 favorites.json。

结构：
    [
        {"url": "https://...", "title": "页面标题", "time": 1234567890.0},
        ...
    ]

最新收藏在前。
"""

import os
import json
import time

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "favorites.json")


# ======================================================================
# 底层读写
# ======================================================================
def _load():
    try:
        if os.path.isfile(STORE_PATH):
            with open(STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def _save(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[favorites] 存失败:", e)


def _norm_url(url):
    """规范化 URL 用于比较：去 query + fragment。"""
    if not url:
        return ""
    try:
        from urllib.parse import urlsplit, urlunsplit
        parts = urlsplit(url)
        return urlunsplit((
            parts.scheme, parts.netloc, parts.path,
            "", "",
        ))
    except Exception:
        return url


# ======================================================================
# 对外接口
# ======================================================================
def load_all():
    """读全部收藏。返回 list[dict]，最新在前。"""
    return _load()


def is_favorited(url):
    """判断 URL 是否已收藏（精确字符串匹配）。"""
    if not url:
        return False
    for it in _load():
        if isinstance(it, dict):
            if it.get("url", "") == url:
                return True
    return False


def add(url, title=""):
    """新增收藏。已存在则更新 title。返回是否新增。"""
    if not url:
        return False

    data = _load()

    for it in data:
        if isinstance(it, dict) and it.get("url", "") == url:
            # 已存在 → 只更新 title
            if title:
                it["title"] = title
            _save(data)
            return False

    data.insert(0, {
        "url": url,
        "title": title or url,
        "time": time.time(),
    })
    _save(data)
    return True


def remove(url):
    """按 URL 删除（精确匹配）。成功返回 True。"""
    if not url:
        return False

    data = _load()
    new_list = []
    removed = False
    for it in data:
        if isinstance(it, dict) and it.get("url", "") == url:
            removed = True
            continue
        new_list.append(it)

    if not removed:
        return False
    _save(new_list)
    return True


def clear():
    _save([])
```

### component\floating_bar.py (大小: 58693 | 修改时间: 2026-10-03 05:02:37 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""悬浮长条：双窗口一起显隐 + 网址转交 + 起窗口。

bar 只做：
  * 起窗口（QProcess）
  * 收到窗口的 request_url，查 host 对应窗口：
      - 有（含主域匹配）→ 转告它，置顶、加载。
      - 没有 → 起新窗口 assign 给它。
  * 起完新窗口后，通知来源窗口拽回原 URL。
  * 起完新窗口后，让新窗口置顶前台。
  * 窗口自带内核，bar 不再通知托盘起/停内核。

Windows Job Object：bar 一死（正常退出 / 崩溃 / 被强杀），
所有 window 子进程被系统强制杀掉。

注意：bar 的颜色不跟随个性化，固定 BODY_COLOR。
"""

import ctypes
from ctypes import wintypes
import sys
import os
import json
from urllib.parse import urlparse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths
from i18n import t
from ipc import (
    IpcServer, IpcClient,
    CHANNEL_BAR, ROLE_BAR,
    MSG_SHOW, MSG_HIDE, MSG_QUIT,
    MSG_NAVIGATE,
    MSG_REVERT_TO_LAST_URL,
    MSG_PIN_RELOAD,
    MSG_PIN_STATE,
    MSG_PIN_TOGGLE_FROM_BAR,
    MSG_PIN_DATA,
    MSG_PIN_REQUEST,
    MSG_LANGUAGE_CHANGED,
    window_role,
    find_windows,
    alloc_window_id,
    cleanup_registry,
    _read_registry, ROLE_WINDOW_PREFIX,
)

import pinned_store
from window_icon import make_domain_icon


DECOY_TITLE = "__frost_layer_test__"


# ======================================================================
# Windows Job Object
# ======================================================================
class _JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_int64),
        ("PerJobUserTimeLimit", ctypes.c_int64),
        ("LimitFlags", ctypes.c_uint32),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", ctypes.c_uint32),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", ctypes.c_uint32),
        ("SchedulingClass", ctypes.c_uint32),
    ]


class _IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_uint64),
        ("WriteOperationCount", ctypes.c_uint64),
        ("OtherOperationCount", ctypes.c_uint64),
        ("ReadTransferCount", ctypes.c_uint64),
        ("WriteTransferCount", ctypes.c_uint64),
        ("OtherTransferCount", ctypes.c_uint64),
    ]


class _JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation",
         _JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", _IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


_JobObjectExtendedLimitInformation = 9
_JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x2000
_PROCESS_SET_QUOTA = 0x0100
_PROCESS_TERMINATE = 0x0001


def create_kill_on_close_job():
    try:
        kernel32 = ctypes.windll.kernel32

        job = kernel32.CreateJobObjectW(None, None)
        if not job:
            print("[bar] CreateJobObject 失败")
            return None

        info = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        info.BasicLimitInformation.LimitFlags = \
            _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE

        ok = kernel32.SetInformationJobObject(
            job,
            _JobObjectExtendedLimitInformation,
            ctypes.byref(info),
            ctypes.sizeof(info),
        )
        if not ok:
            print("[bar] SetInformationJobObject 失败")
            kernel32.CloseHandle(job)
            return None

        return job
    except Exception as e:
        print("[bar] 创建 Job Object 异常:", e)
        return None


def assign_pid_to_job(job, pid):
    if not job or not pid:
        return False
    try:
        kernel32 = ctypes.windll.kernel32

        hproc = kernel32.OpenProcess(
            _PROCESS_SET_QUOTA | _PROCESS_TERMINATE,
            False,
            int(pid),
        )
        if not hproc:
            print(f"[bar] OpenProcess({pid}) 失败")
            return False

        try:
            ok = kernel32.AssignProcessToJobObject(job, hproc)
            if not ok:
                print(f"[bar] AssignProcessToJobObject({pid}) 失败")
                return False
            return True
        finally:
            kernel32.CloseHandle(hproc)
    except Exception as e:
        print(f"[bar] 分配 PID {pid} 到 Job 异常:", e)
        return False


# ======================================================================
# host 判断
# ======================================================================
def url_host(url):
    try:
        host = (urlparse(url).hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def _root_host(host):
    if not host:
        return ""
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])


def _hosts_related(a, b):
    if not a or not b:
        return False
    if a == b:
        return True
    if a.endswith("." + b):
        return True
    if b.endswith("." + a):
        return True
    ra = _root_host(a)
    rb = _root_host(b)
    if ra and ra == rb:
        return True
    return False


def _pid_alive(pid):
    """检查 pid 对应进程是否存活。"""
    if not pid:
        return False
    try:
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h = ctypes.windll.kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid)
        )
        if not h:
            return False
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    except Exception:
        return True


def _find_window_by_host_related(host):
    if not host:
        return None, None
    data = _read_registry()
    for role, entry in data.items():
        if not role.startswith(ROLE_WINDOW_PREFIX):
            continue
        # 跳过死进程
        if not _pid_alive(entry.get("pid")):
            continue
        hosts = entry.get("hosts")
        if isinstance(hosts, list):
            for h in hosts:
                if _hosts_related(host, h):
                    return role, entry
        h = entry.get("host", "")
        if _hosts_related(host, h):
            return role, entry
    return None, None


# ======================================================================
# Windows 模糊 / 置顶
# ======================================================================
class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_int),
        ("AccentFlags", ctypes.c_int),
        ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_int),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.POINTER(ACCENT_POLICY)),
        ("SizeOfData", ctypes.c_size_t),
    ]


ACCENT_ENABLE_BLURBEHIND = 3
ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
WCA_ACCENT_POLICY = 19

HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001
SWP_NOACTIVATE = 0x0010


def enable_blur(hwnd, color=0x00000000, state=ACCENT_ENABLE_BLURBEHIND):
    accent = ACCENT_POLICY()
    accent.AccentState = state
    accent.AccentFlags = 0
    accent.GradientColor = color
    accent.AnimationId = 0

    data = WINDOWCOMPOSITIONATTRIBDATA()
    data.Attribute = WCA_ACCENT_POLICY
    data.Data = ctypes.pointer(accent)
    data.SizeOfData = ctypes.sizeof(accent)

    ctypes.windll.user32.SetWindowCompositionAttribute(
        wintypes.HWND(hwnd), ctypes.byref(data)
    )


def set_topmost(hwnd, on=True):
    ctypes.windll.user32.SetWindowPos(
        wintypes.HWND(hwnd),
        HWND_TOPMOST if on else HWND_NOTOPMOST,
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
    )


def insert_after(hwnd, after_hwnd):
    ctypes.windll.user32.SetWindowPos(
        wintypes.HWND(hwnd),
        wintypes.HWND(after_hwnd),
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
    )


# ======================================================================
# 任务栏卡片显隐（ITaskbarList）
# ======================================================================
import comtypes
import comtypes.client
from comtypes import GUID, COMMETHOD, HRESULT, IUnknown


class ITaskbarList(IUnknown):
    _iid_ = GUID("{56FDF342-FD6D-11D0-958A-006097C9A090}")
    _methods_ = [
        COMMETHOD([], HRESULT, "HrInit"),
        COMMETHOD([], HRESULT, "AddTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "DeleteTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "ActivateTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "SetActiveAlt",
                  (["in"], wintypes.HWND, "hwnd")),
    ]


class TaskbarHelper:
    """封装 ITaskbarList。运行中动态隐藏/显示任务栏卡片。"""

    CLSID_TASKBAR_LIST = GUID("{56FDF344-FD6D-11D0-958A-006097C9A090}")

    def __init__(self):
        self._taskbar = None
        self._ok = False
        try:
            self._taskbar = comtypes.client.CreateObject(
                self.CLSID_TASKBAR_LIST,
                interface=ITaskbarList,
            )
            self._taskbar.HrInit()
            self._ok = True
            print("[bar] ITaskbarList 初始化成功")
        except Exception as e:
            print("[bar] ITaskbarList 初始化失败:", repr(e))

    def hide(self, hwnd):
        if not self._ok:
            return
        try:
            self._taskbar.DeleteTab(int(hwnd))
        except Exception:
            pass

    def show(self, hwnd):
        if not self._ok:
            return
        try:
            self._taskbar.AddTab(int(hwnd))
        except Exception:
            pass


# ======================================================================
# 前台窗口变化监听
# ======================================================================
EVENT_SYSTEM_FOREGROUND = 0x0003
WINEVENT_OUTOFCONTEXT = 0x0000
WINEVENT_SKIPOWNPROCESS = 0x0002

WinEventProc = ctypes.WINFUNCTYPE(
    None,
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.HWND,
    wintypes.LONG,
    wintypes.LONG,
    wintypes.DWORD,
    wintypes.DWORD,
)


class ForegroundHook:
    def __init__(self):
        self._callback_ref = None
        self._hook = None
        self._changed = False

    def install(self):
        def _proc(hWinEventHook, event, hwnd, idObject, idChild,
                  idEventThread, dwmsEventTime):
            if event == EVENT_SYSTEM_FOREGROUND:
                self._changed = True

        self._callback_ref = WinEventProc(_proc)
        self._hook = ctypes.windll.user32.SetWinEventHook(
            EVENT_SYSTEM_FOREGROUND,
            EVENT_SYSTEM_FOREGROUND,
            0,
            self._callback_ref,
            0, 0,
            WINEVENT_OUTOFCONTEXT | WINEVENT_SKIPOWNPROCESS,
        )

    def uninstall(self):
        try:
            if self._hook:
                ctypes.windll.user32.UnhookWinEvent(self._hook)
        except Exception:
            pass
        self._hook = None
        self._callback_ref = None

    def take_changed(self):
        changed = self._changed
        self._changed = False
        return changed


# ======================================================================
# 模糊窗口
# ======================================================================
class FrostWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(DECOY_TITLE)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(48, 300)

    def showEvent(self, event):
        super().showEvent(event)
        enable_blur(int(self.winId()), 0x00000000, ACCENT_ENABLE_BLURBEHIND)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))


# ======================================================================
# 图标按钮
# ======================================================================
class IconButton(QPushButton):
    STYLE_WINDOW = "window"
    STYLE_CHEVRON = "chevron"

    double_clicked = pyqtSignal()
    context_menu_requested = pyqtSignal()

    def __init__(self, icon_style, parent=None):
        super().__init__(parent)
        self.icon_style = icon_style
        self._hover = False
        self._pressed = False

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet("background: transparent; border: none;")

    def enterEvent(self, event):
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self._pressed = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        self.context_menu_requested.emit()
        event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx = w / 2
        cy = h / 2

        if self._pressed:
            color = QColor(235, 235, 235, 230)
        elif self._hover:
            color = QColor(245, 245, 245, 200)
        else:
            color = QColor(210, 210, 210, 150)

        pen = QPen(color)
        pen.setWidthF(1.8)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        if self.icon_style == self.STYLE_WINDOW:
            rw = min(w, h) * 0.72
            rh = rw * 0.86
            x = cx - rw / 2
            y = cy - rh / 2
            radius = rw * 0.18
            painter.drawRoundedRect(QRectF(x, y, rw, rh), radius, radius)

            bar_y = y + rh * 0.30
            painter.drawLine(QPointF(x, bar_y), QPointF(x + rw, bar_y))

            dot_r = rw * 0.07
            dot_gap = rw * 0.17
            dot_cy = y + rh * 0.15
            dot_x0 = x + rw * 0.22
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            for i in range(3):
                painter.drawEllipse(
                    QPointF(dot_x0 + i * dot_gap, dot_cy), dot_r, dot_r
                )

        elif self.icon_style == self.STYLE_CHEVRON:
            size = min(w, h) * 0.22
            v_pen = QPen(color)
            v_pen.setWidthF(1.4)
            v_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            v_pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(v_pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            path = QPainterPath()
            path.moveTo(cx - size, cy - size * 0.25)
            path.quadTo(cx, cy + size * 0.75, cx + size, cy - size * 0.25)
            painter.drawPath(path)


# ======================================================================
# 固定图标按钮
# ======================================================================
class PinIconButton(QPushButton):
    """滚轮区里单个固定图标。悬停变暗，开启变亮（三态亮度）。"""

    ICON_SIZE = 22

    clicked_pin = pyqtSignal(str)
    right_clicked_pin = pyqtSignal(str)

    def __init__(self, host, pixmap, parent=None):
        super().__init__(parent)
        self.host = host
        self._pm = pixmap
        self._hover = False
        self._running = False

        self.setFixedSize(self.ICON_SIZE, self.ICON_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("background: transparent; border: none;")

    def set_running(self, on):
        on = bool(on)
        if on != self._running:
            self._running = on
            self.update()

    def set_pixmap(self, pm):
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.right_clicked_pin.emit(self.host)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.rect().contains(event.position().toPoint()):
                self.clicked_pin.emit(self.host)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if self._pm is None or self._pm.isNull():
            return

        # 高分屏：按物理像素渲染，避免拉伸模糊
        dpr = self.devicePixelRatioF()
        logical_size = self.ICON_SIZE
        px_size = max(1, int(logical_size * dpr))

        pm = self._pm.scaled(
            px_size, px_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        pm.setDevicePixelRatio(dpr)

        # 用逻辑坐标居中
        w_logical = pm.width() / dpr
        h_logical = pm.height() / dpr
        x = (self.width() - w_logical) / 2.0
        y = (self.height() - h_logical) / 2.0

        # 裁成圆角矩形
        radius = logical_size * 0.28
        rect = QRectF(
            (self.width() - logical_size) / 2.0,
            (self.height() - logical_size) / 2.0,
            float(logical_size),
            float(logical_size),
        )

        clip_path = QPainterPath()
        clip_path.addRoundedRect(rect, radius, radius)
        painter.setClipPath(clip_path)

        # 悬停 → 变暗；其他 → 正常
        if self._hover:
            painter.setOpacity(0.6)
        else:
            painter.setOpacity(1.0)

        painter.drawPixmap(QPointF(x, y), pm)
        painter.setOpacity(1.0)

        # 打开状态 → 右上角绿色小点
        painter.setClipping(False)
        if self._running:
            dot_r = 3.5
            dot_cx = self.width() - dot_r - 1
            dot_cy = dot_r + 1
            painter.setBrush(QColor(60, 200, 90))
            painter.setPen(QPen(QColor(255, 255, 255, 200), 1))
            painter.drawEllipse(QPointF(dot_cx, dot_cy), dot_r, dot_r)


# ======================================================================
# 滚轮容器：放固定图标，可滚动
# ======================================================================
class PinScrollArea(QScrollArea):
    """透明滚轮区。只显示图标，可上下滚。"""

    EDGE_HOT = 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet(
            "QScrollArea { background: transparent; border: none; }"
            "QScrollArea > QWidget > QWidget { background: transparent; }"
        )
        self.viewport().setStyleSheet("background: transparent;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._host = QWidget()
        self._host.setStyleSheet("background: transparent;")
        self._layout = QVBoxLayout(self._host)
        self._layout.setContentsMargins(0, 4, 0, 4)
        self._layout.setSpacing(18)
        self._layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._layout.addStretch(1)
        self.setWidget(self._host)

        self.viewport().setContentsMargins(0, 0, 0, 0)

        self._buttons = []
        self._pending_scroll = None      # 待恢复的滚动位置

        # 滚动范围变化时，如果有待恢复位置，恢复它
        self.verticalScrollBar().rangeChanged.connect(
            self._on_range_changed
        )

    def clear_icons(self):
        while self._layout.count() > 0:
            item = self._layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.hide()
                w.setParent(None)
                w.deleteLater()
        self._layout.addStretch(1)
        self._buttons = []
        self._host.update()
        self.viewport().update()

    def _on_range_changed(self, min_val, max_val):
        """layout 排完、滚动范围确定后，恢复滚动位置。"""
        print(f"[pin-scroll] rangeChanged {min_val}-{max_val} "
              f"pending={self._pending_scroll}")
        if self._pending_scroll is None:
            return
        # range 不够大（刚清空时），先不恢复
        if max_val < self._pending_scroll:
            return
        try:
            self.verticalScrollBar().setValue(self._pending_scroll)
        except Exception:
            pass
        self._pending_scroll = None


    def set_icons(self, items):
        # 记当前滚动位置
        try:
            self._pending_scroll = self.verticalScrollBar().value()
        except Exception:
            self._pending_scroll = 0

        print(f"[pin-scroll] set_icons old_value={self._pending_scroll}")

        self.clear_icons()
        for it in items:
            btn = PinIconButton(it["host"], it.get("pixmap"), self._host)
            btn.set_running(it.get("running", False))
            idx = self._layout.count() - 1
            self._layout.insertWidget(idx, btn)
            self._buttons.append(btn)

        # 强制 layout 更新，触发 rangeChanged
        try:
            self._layout.activate()
            self._host.adjustSize()
        except Exception:
            pass

    def buttons(self):
        return list(self._buttons)


# ======================================================================
# 悬浮长条
# ======================================================================
class FloatingBar(QWidget):

    SHADOW_MARGIN = 12
    BAR_W = 40
    BAR_H = 260
    RADIUS = 10

    BODY_COLOR = QColor(0, 0, 0, 140)
    BODY_BORDER = QColor(120, 120, 120, 120)

    POLL_MS = 80
    JITTER_MS = 30
    JITTER_PX = 1
    FROST_PAD = 2
    RESUME_DELAY_MS = 120

    collapse_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(
            self.BAR_W + self.SHADOW_MARGIN * 2,
            self.BAR_H + self.SHADOW_MARGIN * 2,
        )

        self._drag_start = None
        self._jitter_on = False
        self._moving = False

        self._win_procs = {}
        self._win_hosts = {}

        # ---- 固定项 ----
        self._pin_scroll = None
        self._pin_buttons = {}
        self._pin_items = {}
        self._pin_dot_timer = QTimer(self)
        self._pin_dot_timer.setInterval(1500)
        self._pin_dot_timer.timeout.connect(self._refresh_pin_dots)
        self._taskbar = TaskbarHelper()
        # ------------------

        self._job = create_kill_on_close_job()
        if self._job:
            print(f"[bar] Job Object 已创建 h={self._job}")
        else:
            print("[bar] Job Object 创建失败，将退回普通 QProcess 模式")

        self._frost = FrostWindow()
        self._frost.show()

        self._build_ui()
        self._center_right()
        self._sync_frost()
        self._place_frost()

        self._hook = ForegroundHook()
        self._hook.install()

        self._poll_timer = QTimer(self)
        self._poll_timer.setInterval(self.POLL_MS)
        self._poll_timer.timeout.connect(self._poll_foreground)
        self._poll_timer.start()

        self._jitter_timer = QTimer(self)
        self._jitter_timer.setInterval(self.JITTER_MS)
        self._jitter_timer.timeout.connect(self._jitter_frost)
        self._jitter_timer.start()

        self.collapse_btn.double_clicked.connect(self.collapse_requested.emit)
        self.wake_btn.clicked.connect(self.open_default_window)
        self.wake_btn.context_menu_requested.connect(self._show_wake_menu)

        # ---- 固定项 ----
        # 启动先清一次残留 window 注册表，保证这次启动是干净态
        self._clear_all_window_registry()
        self._pin_dot_timer.start()
        QTimer.singleShot(100, self.reload_pinned)
        # ------------------

        # ---- 注册表看门狗：定时清死进程 ----
        try:
            from ipc import RegistryWatchdog
            self._watchdog = RegistryWatchdog(
                interval_ms=3000, parent=self
            )
            self._watchdog.start()
        except Exception as e:
            print("[bar] 启动 RegistryWatchdog 失败:", e)

    # ---------------- UI ----------------
    def _build_ui(self):
        self._body = QWidget(self)
        self._body.setGeometry(
            self.SHADOW_MARGIN, self.SHADOW_MARGIN,
            self.BAR_W, self.BAR_H,
        )
        self._body.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._body.setStyleSheet("background: transparent;")

        shadow = QGraphicsDropShadowEffect(self._body)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 120))
        self._body.setGraphicsEffect(shadow)

        pad = 6
        btn_h = 34
        btn_w = self.BAR_W - pad * 2
        line_w = self.BAR_W - pad * 2

        self.wake_btn = IconButton(IconButton.STYLE_WINDOW, self._body)
        self.wake_btn.setGeometry(pad, 1, btn_w, btn_h)

        self.top_line = QFrame(self._body)
        self.top_line.setGeometry(pad, btn_h, line_w, 1)
        self.top_line.setStyleSheet("background: rgba(180, 180, 180, 90);")

        bottom_pad = 0
        self.collapse_btn = IconButton(IconButton.STYLE_CHEVRON, self._body)
        self.collapse_btn.setGeometry(
            pad, self.BAR_H - bottom_pad - btn_h + 6, btn_w, btn_h
        )

        line_gap = 0
        self.bottom_line = QFrame(self._body)
        self.bottom_line.setGeometry(
            pad,
            self.BAR_H - bottom_pad - btn_h - line_gap + 12,
            line_w, 1,
        )
        self.bottom_line.setStyleSheet("background: rgba(180, 180, 180, 90);")

        # ---- 中间滚轮区 ----
        self._pin_scroll = PinScrollArea(self._body)
        self._pin_scroll.setGeometry(
            0,
            btn_h + 2,
            self.BAR_W,
            self.bottom_line.y() - btn_h - 2,
        )
        self._pin_scroll.raise_()
        self._pin_scroll.installEventFilter(self)
        self._pin_scroll.viewport().installEventFilter(self)
        # --------------------

    # ---------------- 固定项 ----------------
    def reload_pinned(self):
        """从磁盘重读固定项，刷新滚轮区。"""
        try:
            items, broken = pinned_store.load_all()

            if broken:
                self._handle_broken(broken)
                items, broken = pinned_store.load_all()

            pin_list = []
            self._pin_items = {}
            for it in items:
                host = it["host"]
                self._pin_items[host] = it

                pm = pinned_store.load_icon(host)
                if pm is None or pm.isNull():
                    # 生成字母图标：用高分屏尺寸
                    try:
                        dpr = self.devicePixelRatioF()
                    except Exception:
                        dpr = 1.0
                    px = max(64, int(64 * dpr))
                    pm = make_domain_icon(host).pixmap(px, px)

                pin_list.append({
                    "host": host,
                    "pixmap": pm,
                    "running": self._is_host_window_open(host),
                })

            self._pin_buttons = {}
            self._pin_scroll.set_icons(pin_list)

            for btn in self._pin_scroll.buttons():
                btn.clicked_pin.connect(self._on_pin_clicked)
                btn.right_clicked_pin.connect(self._on_pin_right_clicked)
                self._pin_buttons[btn.host] = btn
        except Exception as e:
            import traceback
            print("[bar] reload_pinned 异常:", e)
            traceback.print_exc()

    def _handle_broken(self, broken):
        """损坏固定项：静默删除（不阻塞）。"""
        for host in list(broken):
            try:
                pinned_store.remove(host)
                print(f"[bar] 已删除损坏固定项 {host}")
            except Exception:
                pass

    def _is_host_window_open(self, host):
        """该 host 对应的窗口进程是否存在。"""
        try:
            role, entry = _find_window_by_host_related(host)
            if not role:
                return False
            return _pid_alive(entry.get("pid"))
        except Exception:
            return False

    def _refresh_pin_dots(self):
        """定时刷新每个图标的运行状态。"""
        for host, btn in list(self._pin_buttons.items()):
            try:
                btn.set_running(self._is_host_window_open(host))
            except RuntimeError:
                self._pin_buttons.pop(host, None)
            except Exception:
                pass

    def _on_pin_clicked(self, host):
        """点图标：有窗口 → 置顶；无 → 起 df-N 带记忆。"""
        if not host:
            return

        role, entry = _find_window_by_host_related(host)
        if role and _pid_alive(entry.get("pid")):
            target_id = role.split(":", 1)[1]
            self._show_existing(target_id, retries=15)
            return

        self._open_pinned_window(host)

    def _open_pinned_window(self, host):
        """打开固定窗口：起 df-N，带 host + 记忆。"""
        item = self._pin_items.get(host)
        urls = item.get("popup_urls", []) if item else []
        last_index = item.get("last_index", -1) if item else -1

        url = ""
        if urls:
            if 0 <= last_index < len(urls):
                url = urls[last_index]
            else:
                url = urls[-1]

        wid = self._alloc_default_id()
        self._start_window(
            window_id=wid,
            host=host,
            url="",
            pinned_url=url,
        )
        QTimer.singleShot(600, lambda w=wid: self._show_existing(w, retries=15))

    def _on_pin_right_clicked(self, host):
        """右键图标：取消固定。"""
        if not host:
            return
        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)
        act = menu.addAction(t("menu.unpin"))
        act.triggered.connect(lambda: self._unpin(host))
        menu.exec(QCursor.pos())

    def _unpin(self, host):
        """删记录 + 通知 window 关开关。"""
        if not host:
            return
        pinned_store.remove(host)
        self.reload_pinned()

        try:
            role, _entry = _find_window_by_host_related(host)
            if role:
                target_id = role.split(":", 1)[1]
                payload = json.dumps({"host": host}, ensure_ascii=False)
                IpcClient.send_to_role(
                    window_role(target_id),
                    MSG_PIN_TOGGLE_FROM_BAR,
                    payload.encode("utf-8"),
                )
        except Exception as e:
            print("[bar] 通知 window 关开关失败:", e)

    def _pin_state_from_window(self, data):
        """window 上报固定开关状态。"""
        host = data.get("host", "")
        on = bool(data.get("on", False))
        if not host:
            return

        if on:
            if not pinned_store.is_pinned(host) and pinned_store.count() >= pinned_store.MAX_PINNED:
                try:
                    role, _entry = _find_window_by_host_related(host)
                    if role:
                        target_id = role.split(":", 1)[1]
                        IpcClient.send_to_role(
                            window_role(target_id),
                            MSG_PIN_TOGGLE_FROM_BAR,
                            json.dumps(
                                {"host": host, "reason": "full"},
                                ensure_ascii=False,
                            ).encode("utf-8"),
                        )
                except Exception:
                    pass
                return

            pinned_store.add(
                host,
                hosts=data.get("hosts", [host]),
                popup_urls=data.get("popup_urls", []),
                last_index=data.get("last_index", -1),
                complete_notify=data.get("complete_notify", False),
            )
        else:
            pinned_store.remove(host)

        self.reload_pinned()

    # ---------------- 窗口进程 ----------------
    def _active_window_ids(self):
        """当前真正占用的窗口 id 集合。

        注意：**必须过滤掉已死的窗口进程**。
        IPC 注册表里的条目在窗口崩溃/被杀掉时不一定会被及时清掉，
        如果把死条目也算作"占用"，`alloc_window_id` 就会一直往后编号
        （df-1、df-2、df-3…），而 WebView2 的 profile 是**按窗口 id 分目录**的
        （settings_backend.get_user_data_folder），于是每开一个新窗口
        都是一份全新的空 profile —— 表现为"Cookie 不保存、每次都要重新登录"。
        """
        active = set()
        try:
            for role, entry in find_windows().items():
                if not role.startswith("window:"):
                    continue
                wid = role.split(":", 1)[1]
                if not wid:
                    continue
                if _pid_alive(entry.get("pid")):
                    active.add(wid)
        except Exception:
            pass

        # bar 自己持有的 QProcess：只算还在跑的
        for wid, proc in self._win_procs.items():
            try:
                if proc is not None and proc.state() != QProcess.ProcessState.NotRunning:
                    active.add(wid)
            except Exception:
                active.add(wid)

        # 顺手把注册表里的死条目清掉，别让它们越积越多
        try:
            cleanup_registry()
        except Exception:
            pass

        return active

    def _alloc_default_id(self):
        return alloc_window_id("df", self._active_window_ids())

    def open_default_window(self):
        wid = self._alloc_default_id()
        self._start_window(window_id=wid, host="", url="")

    def _show_wake_menu(self):
        """右键 wake_btn：弹无痕选项。"""
        try:
            from rounded_menu import RoundedMenu
            menu = RoundedMenu(self)
        except Exception:
            menu = QMenu(self)
        act = menu.addAction(t("menu.incognito"))
        act.triggered.connect(self.open_incognito_window)
        menu.exec(self.wake_btn.mapToGlobal(
            self.wake_btn.rect().bottomLeft()))

    def open_incognito_window(self):
        """开一个无痕窗口。"""
        wid = self._alloc_default_id()
        self._start_window(window_id=wid, host="", url="", incognito=True)

    def _start_window(self, window_id, host="", url="", incognito=False,
                      pinned_url=""):
        role = "incognito" if incognito else "window"

        args = ["--id", window_id]
        if host:
            args += ["--host", host]
        if pinned_url:
            args += ["--pinned-url", pinned_url]

        prog, argv = apppaths.role_command(role, *args)
        print(f"[DBG] _start_window role={role} prog={prog} args={argv}")

        proc = QProcess()
        proc.setProgram(prog)
        proc.setArguments(argv)
        apppaths.configure_child_proc(proc)
        self._win_procs[window_id] = proc
        if host:
            self._win_hosts[window_id] = host

        proc.finished.connect(
            lambda *_args, w=window_id: self._on_window_finished(w)
        )
        proc.start()
        print(f"[bar] 起窗口 {window_id} host={host!r} url={url!r} "
              f"incognito={incognito}")

        if self._job:
            proc.waitForStarted(3000)
            pid = proc.processId()
            if pid:
                ok = assign_pid_to_job(self._job, pid)
                print(f"[bar] window {window_id} pid={pid} "
                      f"加入 Job ok={ok}")
            else:
                print(f"[bar] window {window_id} 拿不到 PID")

        if url:
            QTimer.singleShot(0, lambda: self._assign_url(window_id, url))

        QTimer.singleShot(1500, lambda: self._show_existing(window_id))

    def _on_window_finished(self, window_id):
        proc = self._win_procs.pop(window_id, None)
        if proc is not None:
            try:
                proc.deleteLater()
            except Exception:
                pass

        host = self._win_hosts.pop(window_id, "")
        print(f"[bar] 窗口已结束 {window_id} host={host}")

    # ---------------- 网址转交 ----------------
    def _assign_url(self, window_id, url, retries=40):
        try:
            payload = json.dumps({"url": url}, ensure_ascii=False)
            ok = IpcClient.send_to_role(
                window_role(window_id),
                MSG_NAVIGATE,
                payload,
            )
            if ok:
                print(f"[bar] assign {window_id} url={url!r}")
                return
        except Exception as e:
            print("[bar] assign 异常:", e)

        if retries > 0:
            QTimer.singleShot(
                200,
                lambda: self._assign_url(window_id, url, retries - 1),
            )
        else:
            print(f"[bar] assign {window_id} 重试耗尽")

    def _navigate_existing(self, window_id, url):
        try:
            payload = json.dumps({"url": url}, ensure_ascii=False)
            IpcClient.send_to_role(
                window_role(window_id),
                MSG_NAVIGATE,
                payload,
            )
        except Exception as e:
            print("[bar] 发送 navigate 失败:", e)

    def _show_existing(self, window_id, retries=10):
        """让窗口前台。发 MSG_SHOW，窗口自己 raise + activate + set_topmost。"""
        try:
            ok = IpcClient.send_to_role(
                window_role(window_id),
                MSG_SHOW,
                b"",
            )
            if ok:
                QTimer.singleShot(
                    300,
                    lambda w=window_id: IpcClient.send_to_role(
                        window_role(w), MSG_SHOW, b"",
                    ),
                )
                return
        except Exception:
            pass

        if retries > 0:
            QTimer.singleShot(
                200,
                lambda: self._show_existing(window_id, retries - 1),
            )

    def _notify_revert(self, from_window_id):
        if not from_window_id:
            return
        try:
            IpcClient.send_to_role(
                window_role(from_window_id),
                MSG_REVERT_TO_LAST_URL,
                b"",
            )
            print(f"[bar] 已通知 {from_window_id} 拽回")
        except Exception as e:
            print(f"[bar] 通知 {from_window_id} 拽回失败: {e}")

    # ---------------- 网址转交核心 ----------------
    def handle_request_url(self, from_window_id, url, from_host=""):
        host = url_host(url)
        print(f"[DBG] bar.handle_request_url host={host} url={url[:80]!r}")
        if not host:
            self._navigate_existing(from_window_id, url)
            return

        # 1. 有同 host 窗口 → 转发给它
        role, entry = _find_window_by_host_related(host)
        print(f"[DBG] bar 步骤1：find role={role} "
              f"alive={_pid_alive(entry.get('pid')) if entry else False}")
        if role and entry and _pid_alive(entry.get("pid")):
            print("[DBG] bar 走分支 1：转发")
            target_id = role.split(":", 1)[1]
            self._navigate_existing(target_id, url)
            self._show_existing(target_id)
            return

        # 2. 没有，但该主域有固定 → 新建窗口（带固定内容）
        root = _root_host(host)
        print(f"[DBG] bar 步骤2：root={root} "
              f"is_pinned={pinned_store.is_pinned(root) if root else False}")
        if root and pinned_store.is_pinned(root):
            print("[DBG] bar 走分支 2：新建带固定窗口")
            item = self._pin_items.get(root)
            if not item:
                try:
                    item = pinned_store.load_one(root)
                except Exception:
                    item = None

            urls = item.get("popup_urls", []) if item else []
            last_index = item.get("last_index", -1) if item else -1
            pinned_url = ""
            if urls:
                if 0 <= last_index < len(urls):
                    pinned_url = urls[last_index]
                else:
                    pinned_url = urls[-1]

            wid = self._alloc_default_id()
            self._start_window(
                window_id=wid,
                host=root,
                url="",
                pinned_url=pinned_url,
            )
            self._notify_revert(from_window_id)

            QTimer.singleShot(
                1500,
                lambda u=url: self.handle_request_url("", u),
            )
            return

        # 3. 都没有 → 新建窗口，加载网址
        wid = self._alloc_default_id()
        self._start_window(window_id=wid, host=host, url=url)
        self._notify_revert(from_window_id)

    def on_window_message(self, msg_type, payload):
        if msg_type == MSG_NAVIGATE:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                return
            cmd = data.get("cmd")
            if cmd == "request_url":
                self.handle_request_url(
                    data.get("window_id", ""),
                    data.get("url", ""),
                    data.get("host", ""),
                )
            return

        if msg_type == MSG_PIN_RELOAD:
            self.reload_pinned()
            return

        if msg_type == MSG_PIN_STATE:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                return
            self._pin_state_from_window(data)
            return

    # ---------------- 几何 ----------------
    def _frost_geometry(self):
        cur_w = self.width()
        cur_h = self.height()

        base_w = self.BAR_W + self.SHADOW_MARGIN * 2
        base_h = self.BAR_H + self.SHADOW_MARGIN * 2
        scale_x = cur_w / base_w
        scale_y = cur_h / base_h

        pad = self.FROST_PAD
        m_x = int((self.SHADOW_MARGIN + 5 - pad) * scale_x)
        m_y = int((self.SHADOW_MARGIN + 5 - pad) * scale_y)
        w = int((self.BAR_W - 10 + pad * 2) * scale_x)
        h = int((self.BAR_H - 10 + pad * 2) * scale_y)

        top_left = self.mapToGlobal(QPoint(m_x, m_y))
        return top_left.x(), top_left.y(), w, h

    def _sync_frost(self):
        try:
            x, y, w, h = self._frost_geometry()
            self._frost.setGeometry(x, y, w, h)
        except Exception:
            pass

    def _place_frost(self):
        try:
            main_hwnd = int(self.winId())
            frost_hwnd = int(self._frost.winId())

            set_topmost(frost_hwnd, True)
            set_topmost(main_hwnd, True)
            insert_after(frost_hwnd, main_hwnd)
            enable_blur(frost_hwnd, 0x00000000, ACCENT_ENABLE_BLURBEHIND)
        except Exception:
            pass

    def _jitter_frost(self):
        if not self.isVisible():
            return
        if self._moving:
            return
        try:
            x, y, w, h = self._frost_geometry()
            offset = self.JITTER_PX if self._jitter_on else 0
            self._jitter_on = not self._jitter_on
            self._frost.setGeometry(x + offset, y, w, h)
        except Exception:
            pass

    def _resume_jitter(self):
        self._moving = False
        self._jitter_on = False

    def _poll_foreground(self):
        # 这是每 POLL_MS 跑一次的常驻定时器，里面要碰 win32 窗口句柄。
        # 一旦抛异常，Qt 会当成未处理异常直接把整个 bar 进程带走
        # （日志里只留下 exit_code=1），所以这里兜住并留痕。
        try:
            if not self.isVisible():
                return
            if self._hook.take_changed():
                self._sync_frost()
                self._place_frost()
        except Exception:
            import traceback
            print("[bar] _poll_foreground 异常:")
            traceback.print_exc()

    # ---------------- 显隐 ----------------
    def hide_bar(self):
        self.hide()
        try:
            self._frost.hide()
        except Exception:
            pass

    def show_bar(self):
        self.show()
        try:
            self._frost.show()
            enable_blur(int(self._frost.winId()), 0x00000000,
                        ACCENT_ENABLE_BLURBEHIND)
        except Exception:
            pass
        self._sync_frost()
        self._place_frost()

    # ---------------- 绘制 ----------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(
            self.SHADOW_MARGIN, self.SHADOW_MARGIN,
            self.BAR_W, self.BAR_H,
        )
        painter.setBrush(self.BODY_COLOR)
        painter.setPen(QPen(self.BODY_BORDER, 1))
        painter.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

    # ---------------- 位置 / 事件 ----------------
    def _center_right(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.right() - self.width() + self.SHADOW_MARGIN - 20
        y = screen.top() + (screen.height() - self.height()) // 2
        self.move(x, y)

    def event(self, e):
        if e.type() in (
            QEvent.Type.WindowActivate,
            QEvent.Type.Show,
            QEvent.Type.WindowStateChange,
        ):
            QTimer.singleShot(0, self._place_frost)
        return super().event(e)

    def showEvent(self, event):
        super().showEvent(event)
        self._place_frost()

    def moveEvent(self, event):
        super().moveEvent(event)
        self._sync_frost()
        self._place_frost()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._sync_frost()
        self._place_frost()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start = event.globalPosition().toPoint() - self.pos()
            self._moving = True

    def mouseMoveEvent(self, event):
        if self._drag_start and (event.buttons() & Qt.MouseButton.LeftButton):
            self.move(event.globalPosition().toPoint() - self._drag_start)

    def mouseReleaseEvent(self, event):
        self._drag_start = None
        QTimer.singleShot(self.RESUME_DELAY_MS, self._resume_jitter)

    # ---------------- 滚轮区：滚 + 边缘拖 ----------------
    def wheelEvent(self, event):
        if self._pin_scroll is not None:
            try:
                self._pin_scroll.wheelEvent(event)
                return
            except Exception:
                pass
        super().wheelEvent(event)

    def eventFilter(self, obj, event):
        sc = self._pin_scroll
        if sc is None:
            return super().eventFilter(obj, event)

        if obj is sc or obj is sc.viewport():
            et = event.type()

            if et == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    pos = event.position().toPoint()
                    w = sc.width()
                    if pos.x() <= sc.EDGE_HOT or pos.x() >= w - sc.EDGE_HOT:
                        self._drag_start = (
                            event.globalPosition().toPoint() - self.pos()
                        )
                        self._moving = True
                        return True

            elif et == QEvent.Type.MouseMove:
                if (self._drag_start is not None
                        and (event.buttons() & Qt.MouseButton.LeftButton)):
                    self.move(
                        event.globalPosition().toPoint() - self._drag_start
                    )
                    return True

            elif et == QEvent.Type.MouseButtonRelease:
                if self._drag_start is not None:
                    self._drag_start = None
                    QTimer.singleShot(
                        self.RESUME_DELAY_MS, self._resume_jitter
                    )
                    return True

            elif et == QEvent.Type.Wheel:
                try:
                    sc.wheelEvent(event)
                except Exception:
                    pass
                return True

        return super().eventFilter(obj, event)

    def closeEvent(self, event):
        # 1. 温柔关掉 bar 自己起的窗口进程（terminate → kill）
        self._kill_all_windows()

        # 2. 关 Job Object → 系统强杀残留子进程
        try:
            if self._job:
                ctypes.windll.kernel32.CloseHandle(self._job)
                self._job = None
                print("[bar] Job Object 已关闭，子进程将被系统回收")
        except Exception:
            pass

        # 3. 清空注册表里所有 window 条目
        self._clear_all_window_registry()

        # 4. 把固定项状态整体复位：没有任何窗口开着
        self._reset_all_pins_closed()

        # 5. 卸载 hook / 关 frost
        try:
            self._hook.uninstall()
        except Exception:
            pass
        try:
            self._frost.close()
        except Exception:
            pass
        super().closeEvent(event)

    def _clear_all_window_registry(self):
        """清掉注册表里所有 window:* 条目。"""
        try:
            from ipc import _write_registry
            data = _read_registry()
            removed = []
            for role in list(data.keys()):
                if role.startswith(ROLE_WINDOW_PREFIX):
                    del data[role]
                    removed.append(role)
            if removed:
                _write_registry(data)
                print(f"[bar] 已清理 {len(removed)} 个残留 window 条目")
        except Exception as e:
            print("[bar] 清理 window 注册表失败:", e)

    def _reset_all_pins_closed(self):
        """把每个固定项复位为『没有窗口打开』。"""
        try:
            for host, btn in list(self._pin_buttons.items()):
                try:
                    btn.set_running(False)
                except RuntimeError:
                    self._pin_buttons.pop(host, None)
                except Exception:
                    pass
        except Exception as e:
            print("[bar] 复位图标状态失败:", e)

        self._win_procs.clear()
        self._win_hosts.clear()

        try:
            if self._pin_dot_timer.isActive():
                self._pin_dot_timer.stop()
        except Exception:
            pass

        print("[bar] 所有固定项已复位为『未打开』")

    def _kill_all_windows(self):
        """关掉 bar 起的窗口进程。

        **先请它们优雅退出，再硬杀剩下的。**

        为什么不能直接杀：Windows 上 `QProcess.terminate()` 实际是
        `TerminateProcess`（硬杀），不是发 WM_CLOSE。窗口进程被瞬间干掉时，
        WebView2 还没来得及销毁自己，profile（Cookie / localStorage / 登录态）
        可能没落盘 —— 表现就是"关掉软件再打开，登录态丢了"。

        所以：先发 MSG_QUIT（window.py 收到后会 self.close()，走完整的
        closeEvent → WebView2 正常析构），给它一小段时间；还赖着不走的才强杀。

        时间预算压在 ~1.2 秒内：托盘的 quit() 只等 bar 2 秒，超时会把 bar 也杀了，
        而 bar 一死 Job Object（KILL_ON_JOB_CLOSE）就会立刻回收所有窗口。
        """
        procs = [(wid, p) for wid, p in self._win_procs.items() if p is not None]
        if not procs:
            self._win_procs.clear()
            return

        # 1) 逐个请求优雅退出
        for wid, _proc in procs:
            try:
                IpcClient.send_to_role(window_role(wid), MSG_QUIT, timeout_ms=200)
            except Exception as e:
                print(f"[bar] 请求窗口 {wid} 退出失败: {e}")

        # 2) 统一等待（总预算 1200ms，窗口多也不会拖太久）
        timer = QElapsedTimer()
        timer.start()
        for wid, proc in procs:
            try:
                if proc.state() == QProcess.ProcessState.NotRunning:
                    continue
                left = 1200 - int(timer.elapsed())
                if left > 0 and proc.waitForFinished(left):
                    print(f"[bar] 窗口 {wid} 已优雅退出")
            except Exception:
                pass

        # 3) 还没退的才强杀
        for wid, proc in procs:
            try:
                if proc.state() != QProcess.ProcessState.NotRunning:
                    print(f"[bar] 窗口 {wid} 未响应，强制结束")
                    proc.terminate()
                    if not proc.waitForFinished(1200):
                        proc.kill()
            except Exception:
                pass

        self._win_procs.clear()
        self._win_hosts.clear()


# ======================================================================
# 入口
# ======================================================================
def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 加载语言（必须在 FloatingBar 创建之前）
    try:
        from settings_backend import SettingsBackend
        from i18n import load as i18n_load
        i18n_load(SettingsBackend().get_language())
    except Exception as e:
        print("[bar] 加载语言失败:", e)

    bar = FloatingBar()

    def on_message(msg_type, payload):
        if msg_type == MSG_SHOW:
            bar.show_bar()
            bar.raise_()
            bar.activateWindow()
        elif msg_type == MSG_HIDE:
            bar.hide_bar()
        elif msg_type == MSG_QUIT:
            bar.close()
            app.quit()
        elif msg_type == MSG_NAVIGATE:
            bar.on_window_message(msg_type, payload)
        elif msg_type == MSG_PIN_RELOAD:
            bar.reload_pinned()
        elif msg_type == MSG_PIN_STATE:
            bar.on_window_message(msg_type, payload)
        elif msg_type == MSG_LANGUAGE_CHANGED:
            try:
                from i18n import load as i18n_load
                code = payload.decode("utf-8")
                i18n_load(code)
                print(f"[bar] 语言已切换到 {code}")
            except Exception as e:
                print("[bar] 切换语言失败:", e)

    server = IpcServer(CHANNEL_BAR, on_message, role=ROLE_BAR)
    if not server.start():
        print("[bar] 已有实例在运行，退出")
        sys.exit(0)

    bar.collapse_requested.connect(bar.hide_bar)

    bar.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

### component\font_scheme_handler.py (大小: 2143 | 修改时间: 2026-10-03 00:38:18 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""自定义协议 appfont:// 处理器。"""

import os

from PyQt6.QtCore import QBuffer, QIODevice, QUrl
from PyQt6.QtWebEngineCore import (
    QWebEngineUrlScheme,
    QWebEngineUrlSchemeHandler,
    QWebEngineUrlRequestJob,
)


FONT_SCHEME = b"appfont"

_HERE = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_HERE)
FONTS_DIR = os.path.join(_PROJECT_ROOT, "assets", "fonts")


_MIME_BY_EXT = {
    ".woff2": b"font/woff2",
    ".woff":  b"font/woff",
    ".ttf":   b"font/ttf",
    ".otf":   b"font/otf",
}


class FontSchemeHandler(QWebEngineUrlSchemeHandler):
    def requestStarted(self, request: QWebEngineUrlRequestJob):
        url = request.requestUrl()
        name = url.path().lstrip("/")
        if not name or "/" in name or ".." in name:
            request.fail(QWebEngineUrlRequestJob.Error.UrlNotFound)
            return

        path = os.path.join(FONTS_DIR, name)
        if not os.path.isfile(path):
            request.fail(QWebEngineUrlRequestJob.Error.UrlNotFound)
            return

        ext = os.path.splitext(name)[1].lower()
        mime = _MIME_BY_EXT.get(ext)
        if mime is None:
            request.fail(QWebEngineUrlRequestJob.Error.RequestFailed)
            return

        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError:
            request.fail(QWebEngineUrlRequestJob.Error.RequestFailed)
            return

        buf = QBuffer(parent=request)
        buf.setData(data)
        buf.open(QIODevice.OpenModeFlag.ReadOnly)
        request.reply(mime, buf)


_REGISTERED = False


def register_font_scheme():
    global _REGISTERED
    if _REGISTERED:
        return
    _REGISTERED = True

    scheme = QWebEngineUrlScheme(FONT_SCHEME)
    scheme.setFlags(
        QWebEngineUrlScheme.Flag.SecureScheme
        | QWebEngineUrlScheme.Flag.LocalAccessAllowed
        | QWebEngineUrlScheme.Flag.CorsEnabled
    )
    scheme.setSyntax(QWebEngineUrlScheme.Syntax.Host)
    QWebEngineUrlScheme.registerScheme(scheme)
```

### component\history_hook.py (大小: 1542 | 修改时间: 2026-09-29 22:47:03 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""历史记录钩子：具体逻辑在这。

由 window.History.record() 转发调用。
"""


def record(window, title, url=""):
    """记一条历史。window 是 RoundedWindow 实例。

    无痕窗口、save_history 关、非 http(s) 页面 → 不记。
    """
    # 无痕窗口不写
    if type(window).__name__ == "IncognitoWindow":
        return

    if not title:
        return

    url = url or getattr(window, "_current_url", "") or ""
    if not url.startswith(("http://", "https://")):
        return

    # save_history 关掉就不写
    try:
        from settings_backend import SettingsBackend
        if not SettingsBackend().get_save_history():
            return
    except Exception:
        pass

    # 白名单跳过
    try:
        from settings_backend import SettingsBackend
        wl = SettingsBackend().get_whitelist()
        host = _host_of(url)
        for entry in wl:
            if entry.get("host", "") == host and entry.get("no_history"):
                return
    except Exception:
        pass

    try:
        from history_store import add_history
        add_history(url, title, max_days=30)
    except Exception as e:
        print("[history_hook] 写历史失败:", e)


def _host_of(url):
    try:
        from urllib.parse import urlparse
        h = (urlparse(url).hostname or "").lower()
        if h.startswith("www."):
            h = h[4:]
        return h
    except Exception:
        return ""
```

### component\history_store.py (大小: 3366 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""历史记录存储。读写项目根目录下的 history.json。

记录结构：
    [
        {
            "url": "https://...",
            "title": "页面标题",
            "host": "bilibili.com",
            "time": 1790645040.5
        },
        ...
    ]

最新在前。
"""

import os
import json
import time

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "history.json")

MAX_RECORDS = 5000


def _load():
    try:
        if os.path.isfile(STORE_PATH):
            with open(STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []


def _save(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _host_of(url):
    try:
        from urllib.parse import urlparse
        h = (urlparse(url).hostname or "").lower()
        if h.startswith("www."):
            h = h[4:]
        return h
    except Exception:
        return ""


def add_history(url, title="", max_days=30):
    """新增一条。同 URL 同 title 跳过；同 URL 不同 title 更新。

    max_days > 0 时，写入前删掉超过 max_days 天的记录。
    """
    if not url:
        return
    data = _load()

    # 删超期
    if max_days > 0:
        cutoff = time.time() - max_days * 86400
        data = [r for r in data if r.get("time", 0) >= cutoff]

    # 同 URL 同 title → 跳过（不更新 time）
    for r in data:
        if r.get("url") == url and r.get("title") == title:
            return

    # 同 URL 不同 title → 删旧，插新
    data = [r for r in data if r.get("url") != url]

    data.insert(0, {
        "url": url,
        "title": title or "",
        "host": _host_of(url),
        "time": time.time(),
    })

    if len(data) > MAX_RECORDS:
        data = data[:MAX_RECORDS]

    _save(data)


def load_history(days=0, host="", keyword=""):
    """读记录，按条件过滤。

    days: >0 只取最近 days 天；0 = 不限
    host: 非空只取该主域
    keyword: 非空，title 或 url 任一含该关键词
    返回 list，最新在前。
    """
    data = _load()
    now = time.time()

    if days > 0:
        cutoff = now - days * 86400
        data = [r for r in data if r.get("time", 0) >= cutoff]

    if host:
        data = [r for r in data if r.get("host") == host]

    if keyword:
        kw = keyword.lower()
        data = [
            r for r in data
            if kw in (r.get("title", "") or "").lower()
            or kw in (r.get("url", "") or "").lower()
        ]

    return data


def remove_by_urls(urls):
    """按 URL 列表删除。"""
    if not urls:
        return
    s = set(urls)
    data = _load()
    data = [r for r in data if r.get("url") not in s]
    _save(data)


def clear_all():
    _save([])


def all_hosts():
    """返回出现过的所有主域（去重，排序）。"""
    data = _load()
    hosts = set()
    for r in data:
        h = r.get("host", "")
        if h:
            hosts.add(h)
    return sorted(hosts)
```

### component\i18n.py (大小: 6195 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""UI 文字国际化。

只管自己画的 UI。WebView2 内核自带的文字（右键菜单、错误页）
跟随系统语言，不在这个范围内。

语言文件放 component/i18n/<code>.json，结构：
    {
        "_meta": {"code": "zh-CN", "name": "简体中文"},
        "key1": "文字1",
        "key2": "文字2"
    }

切换语言：
    load("en-US")  # 加载并触发所有 on_change 回调
"""

import os
import json
import shutil

import apppaths


I18N_DIR = os.path.join(apppaths.COMPONENT_DIR, "i18n")

DEFAULT_CODE = "zh-CN"

_current_code = DEFAULT_CODE
_current_data = {}

# 语言变化时的回调列表
_listeners = []


# ======================================================================
# 校验
# ======================================================================
def validate_language(data):
    """校验语言 JSON 结构。不合法抛 ValueError。"""
    if not isinstance(data, dict):
        raise ValueError("语言文件必须是一个 JSON 对象")

    meta = data.get("_meta")
    if not isinstance(meta, dict):
        raise ValueError("缺少 _meta 字段")

    code = meta.get("code")
    if not isinstance(code, str) or not code.strip():
        raise ValueError("_meta.code 必须是非空字符串")

    name = meta.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("_meta.name 必须是非空字符串")

    keys = [k for k in data.keys() if k != "_meta"]
    if not keys:
        raise ValueError("语言文件里没有任何翻译条目")

    for k in keys:
        if not isinstance(data[k], str):
            raise ValueError(f"键 {k!r} 的值必须是字符串")

    return code.strip()


# ======================================================================
# 加载 / 切换
# ======================================================================
def _path(code):
    return os.path.join(I18N_DIR, code + ".json")


def _notify():
    """通知所有监听者。"""
    print(f"[i18n] _notify 触发，listeners={len(_listeners)}")
    for fn in list(_listeners):
        try:
            fn()
        except Exception as e:
            print("[i18n] on_change 回调异常:", e)


def load(code, notify=True):
    """加载指定语言。

    code 加载失败就回退到默认。
    加载成功后，如果 notify=True，触发所有 on_change 回调。
    """
    global _current_code, _current_data

    data = None
    try:
        with open(_path(code), "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[i18n] 加载 {code} 失败: {e}")
        data = None

    if not isinstance(data, dict):
        if code != DEFAULT_CODE:
            try:
                with open(_path(DEFAULT_CODE), "r", encoding="utf-8") as f:
                    data = json.load(f)
                code = DEFAULT_CODE
            except Exception:
                data = {}
        else:
            data = {}

    _current_data = data if isinstance(data, dict) else {}
    _current_code = code

    print(f"[i18n] load 完成 code={code} keys={len(_current_data)}")

    if notify:
        _notify()


def current_code():
    return _current_code


def t(key, default=""):
    """取文字。找不到就返回 default 或 key 本身。"""
    if not _current_data:
        load(_current_code, notify=False)
    v = _current_data.get(key)
    if v is None:
        print(f"[i18n] 缺失 key: {key}")
        return default or key
    return v


def on_change(fn):
    """注册语言变化回调。"""
    if fn not in _listeners:
        _listeners.append(fn)
        print(f"[i18n] on_change 注册: {fn}, 当前 listeners={len(_listeners)}")


def off_change(fn):
    """取消注册。"""
    if fn in _listeners:
        _listeners.remove(fn)
        print(f"[i18n] on_change 注销: {fn}, 当前 listeners={len(_listeners)}")


# ======================================================================
# 列出 / 导入 / 导出
# ======================================================================
def list_languages():
    """列出 i18n 目录下所有语言文件，返回 [(code, name), ...]。"""
    out = []
    if not os.path.isdir(I18N_DIR):
        return out

    for name in os.listdir(I18N_DIR):
        if not name.endswith(".json"):
            continue
        path = os.path.join(I18N_DIR, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        meta = data.get("_meta", {}) if isinstance(data, dict) else {}
        code = meta.get("code", "") or os.path.splitext(name)[0]
        label = meta.get("name", "") or code
        out.append((code, label))

    out.sort()
    return out


def import_language(src_path):
    """导入用户拖进来的语言文件。

    校验格式，通过后拷到 i18n/<code>.json。
    返回 (code, name)。不合法抛 ValueError。
    """
    if not os.path.isfile(src_path):
        raise ValueError("不是有效的文件")

    try:
        with open(src_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"不是合法的 JSON 文件：{e}")

    code = validate_language(data)
    name = data["_meta"]["name"]

    if code == DEFAULT_CODE:
        raise ValueError(f"不能覆盖默认语言 {DEFAULT_CODE}")

    os.makedirs(I18N_DIR, exist_ok=True)
    dst = _path(code)

    try:
        shutil.copyfile(src_path, dst)
    except Exception as e:
        raise ValueError(f"写入语言文件失败：{e}")

    return code, name


def export_language(code, dst_path):
    """把指定语言文件导出到 dst_path。返回是否成功。"""
    src = _path(code)
    if not os.path.isfile(src):
        return False
    try:
        shutil.copyfile(src, dst_path)
        return True
    except Exception:
        return False
```

### component\inc_p_window.py (大小: 4431 | 修改时间: 2026-09-29 17:13:18 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""无痕窗口的弹窗：半透明 + 渐变。

继承 PopupWindow，只改背景绘制。
- 背景：紫→酒红渐变，半透明
- 标题栏：比正文更透
- 其余逻辑（URL 列表、拖动、缩放、favicon）全继承
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
from popup_window import PopupWindow, _TabRow


# ======================================================================
# 配色
# ======================================================================
GRAD_TOP_LEFT     = QColor(106, 13, 173, 180)   # 紫，alpha=180
GRAD_BOTTOM_RIGHT = QColor(114, 47, 55, 180)    # 酒红，alpha=180

TITLE_ALPHA_EXTRA = -40     # 标题栏比正文再透 40
BORDER_COLOR      = QColor(255, 255, 255, 120)  # 半透明白描边


class IncognitoPopupWindow(PopupWindow):
    """无痕弹窗。只覆盖背景绘制 + 行配色。"""

    def __init__(self, parent=None, title="弹窗"):
        super().__init__(parent=parent, title=title)
        self._apply_row_style()

    def _apply_row_style(self):
        """让每一行也半透明，跟渐变协调。"""
        try:
            for row in self._rows:
                row.BG_SELECTED = QColor(255, 255, 255, 70)
                row.BG_HOVER = QColor(255, 255, 255, 40)
                row.BG_NORMAL = QColor(0, 0, 0, 0)
                row.TEXT_NORMAL = QColor(230, 230, 230)
                row.TEXT_SELECTED = QColor(255, 255, 255)
                row.ACCENT = QColor(255, 255, 255, 220)
                row.CLOSE_NORMAL = QColor(200, 200, 200)
                row.CLOSE_HOVER = QColor(255, 120, 120)
                row.CLOSE_HOVER_BG = QColor(220, 80, 80, 90)
                row.update()
        except Exception as e:
            print("[inc-popup] 改行样式失败:", e)

    def append_url(self, url):
        idx = super().append_url(url)
        # 新增行后重新上色
        self._apply_row_style()
        return idx

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = self.RADIUS
        outer = QRectF(
            self.BORDER / 2, self.BORDER / 2,
            self.width() - self.BORDER,
            self.height() - self.BORDER,
        )

        # ---- 整体：紫→酒红渐变，半透明 ----
        grad = QLinearGradient(outer.topLeft(), outer.bottomRight())
        grad.setColorAt(0.0, GRAD_TOP_LEFT)
        grad.setColorAt(1.0, GRAD_BOTTOM_RIGHT)

        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(BORDER_COLOR, self.BORDER))
        painter.drawRoundedRect(outer, r, r)

        # ---- 标题栏：比正文再透一点 ----
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

        # 标题栏：白一点，更透
        title_c = QColor(255, 255, 255, 40)
        painter.setBrush(title_c)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPath(path)

        # ---- favicon + 关闭按钮（父类方法） ----
        self._paint_favicon(painter)
        self._paint_close_btn(painter)


# ======================================================================
# 入口：单独跑，弹一个空无痕弹窗看效果
# ======================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = IncognitoPopupWindow(title="无痕弹窗测试")
    w.append_url("https://www.bing.com/")
    w.append_url("https://www.bilibili.com/")
    w.append_url("https://www.zhihu.com/")
    w.show()

    sys.exit(app.exec())
```

### component\incognito_window.py (大小: 15494 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
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
```

### component\input_box.py (大小: 19832 | 修改时间: 2026-10-03 03:50:20 | 权限: 666)

```
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
```

### component\ipc.py (大小: 12862 | 修改时间: 2026-10-02 18:43:39 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""本地 IPC：QLocalServer / QLocalSocket + 进程注册表 + 计时。

通道名约定：
    窗口：  browser_window_<id>       role = window:<id>
    窗口 worker：browser_window_<id>_worker  （下载子进程监听）
    bar：   browser_bar_channel       role = bar
    托盘：  browser_tray_channel      role = tray
    设置：  browser_settings_channel  role = settings
    下载：  browser_downloads_channel role = downloads
    广播：  browser_broadcast_channel（预留，未使用）

消息格式：
    [4 字节大端长度][1 字节类型][N 字节负载]
    长度 = 1(类型) + len(负载)
    完整消息字节数 = 4 + 长度

注册表结构（每个 role 一条）：
    {
        "window:cn.bing.com": {
            "pid": 12345,
            "channel": "browser_window_cn.bing.com",
            "time": 1758600000.0,
            "type": "default",
            "window_id": "cn.bing.com",
            "hosts": ["bing.com", "cn.bing.com"],
            "host": "cn.bing.com"
        },
        ...
    }
"""

import struct
import json
import os
import tempfile
import time

from loader import *
from PyQt6.QtNetwork import QLocalServer, QLocalSocket


IPC_TIMING = True


def _t():
    return time.perf_counter()


def _log(tag, t0, extra=""):
    if not IPC_TIMING:
        return
    dt = (time.perf_counter() - t0) * 1000
    print(f"[ipc-t] {tag} {dt:.1f}ms {extra}")


CHANNEL_BAR = "browser_bar_channel"
CHANNEL_TRAY = "browser_tray_channel"
CHANNEL_SETTINGS = "browser_settings_channel"
CHANNEL_DOWNLOADS = "browser_downloads_channel"
CHANNEL_BROADCAST = "browser_broadcast_channel"

CHANNEL_WINDOW_PREFIX = "browser_window_"

ROLE_BAR = "bar"
ROLE_TRAY = "tray"
ROLE_SETTINGS = "settings"
ROLE_DOWNLOADS = "downloads"
ROLE_WINDOW_PREFIX = "window:"


def window_channel(window_id):
    return CHANNEL_WINDOW_PREFIX + str(window_id)


def window_role(window_id):
    return ROLE_WINDOW_PREFIX + str(window_id)


MSG_SHOW = 1
MSG_HIDE = 2
MSG_PING = 3
MSG_PONG = 4
MSG_QUIT = 5
MSG_NAVIGATE = 6
MSG_CONFIG_CHANGED = 8
MSG_OPEN_SETTINGS = 9
MSG_SETTINGS_SHOW = 10
MSG_LANGUAGE_CHANGED = 11
MSG_OPEN_DOWNLOADS = 12
MSG_DOWNLOADS_SHOW = 13
MSG_DOWNLOADS_REFRESH = 14
MSG_DOWNLOAD_DONE = 16
MSG_DOWNLOAD_START = 17
MSG_DOWNLOAD_PROGRESS = 18
MSG_DOWNLOAD_CANCEL_FOR_WINDOW = 21
MSG_DOWNLOAD_CANCEL_WORKER = 22
MSG_DOWNLOAD_START_WORKER = 23
MSG_REVERT_TO_LAST_URL = 24
MSG_PIN_RELOAD = 25           # window → bar：刷新固定图标（建/删/改）
MSG_PIN_STATE = 26            # window → bar：上报固定开关状态
MSG_PIN_TOGGLE_FROM_BAR = 27  # bar → window：bar 处取消固定，让 window 关开关
MSG_PIN_DATA = 28             # window → bar：上报固定内容（host/popup/索引）
MSG_PIN_REQUEST = 29          # bar → window：向 window 请求固定内容
MSG_FAVORITE_CHANGED = 30     # 收藏变化：广播给所有窗口


HEADER = struct.Struct(">IB")
HEADER_SIZE = HEADER.size


REGISTRY_PATH = os.path.join(tempfile.gettempdir(), "browser_ipc_registry.json")


def _read_registry():
    t0 = _t()
    result = {}
    try:
        if os.path.isfile(REGISTRY_PATH):
            with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                result = data
    except Exception:
        pass
    _log("registry.read", t0, f"keys={len(result)}")
    return result


def _write_registry(data):
    t0 = _t()
    try:
        with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    _log("registry.write", t0, f"keys={len(data)}")


def register_process(role, channel, pid=None, extra=None):
    if pid is None:
        pid = os.getpid()
    data = _read_registry()
    entry = {"pid": pid, "channel": channel, "time": time.time()}
    if extra:
        entry.update(extra)
    data[role] = entry
    _write_registry(data)


def unregister_process(role):
    data = _read_registry()
    if role in data:
        del data[role]
        _write_registry(data)


def find_process(role):
    data = _read_registry()
    return data.get(role)


def find_windows(predicate=None):
    data = _read_registry()
    out = {}
    for role, entry in data.items():
        if not role.startswith(ROLE_WINDOW_PREFIX):
            continue
        if predicate is None or predicate(entry):
            out[role] = entry
    return out


def find_window_by_host(host):
    if not host:
        return None, None
    data = _read_registry()
    for role, entry in data.items():
        if not role.startswith(ROLE_WINDOW_PREFIX):
            continue
        # 跳过死进程
        if not _pid_alive(entry.get("pid")):
            continue
        hosts = entry.get("hosts")
        if isinstance(hosts, list) and host in hosts:
            return role, entry
        if entry.get("host") == host:
            return role, entry
    return None, None


def alloc_window_id(prefix, active_ids):
    used = set()
    p = prefix + "-"
    for wid in active_ids:
        if wid.startswith(p):
            try:
                used.add(int(wid[len(p):]))
            except ValueError:
                pass
    n = 0
    while n in used:
        n += 1
    return f"{prefix}-{n}"


def cleanup_registry():
    data = _read_registry()
    changed = False
    for role, entry in list(data.items()):
        pid = entry.get("pid")
        if not _pid_alive(pid):
            del data[role]
            changed = True
    if changed:
        _write_registry(data)


def _pid_alive(pid):
    if pid is None:
        return False
    try:
        import ctypes
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        h = ctypes.windll.kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid)
        )
        if not h:
            return False
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    except Exception:
        return True


def encode(msg_type, payload=b""):
    if isinstance(payload, str):
        payload = payload.encode("utf-8")
    length = 1 + len(payload)
    return HEADER.pack(length, msg_type) + payload


class MessageReader:
    def __init__(self, on_message):
        self._buf = bytearray()
        self._on_message = on_message

    def feed(self, data: bytes):
        if data:
            self._buf.extend(data)
        while True:
            if len(self._buf) < HEADER_SIZE:
                return
            length, msg_type = HEADER.unpack(bytes(self._buf[:HEADER_SIZE]))
            if length < 1:
                self._buf.clear()
                return
            total = 4 + length
            if len(self._buf) < total:
                return
            payload = bytes(self._buf[HEADER_SIZE:total])
            del self._buf[:total]
            try:
                self._on_message(msg_type, payload)
            except Exception as e:
                print("[ipc] 回调异常:", e)


class IpcServer:
    def __init__(self, channel, on_message, role=None, extra=None):
        self.channel = channel
        self._on_message = on_message
        self._role = role
        self._extra = extra
        self._server = QLocalServer()
        self._readers = {}

    def start(self):
        t0 = _t()
        QLocalServer.removeServer(self.channel)
        t1 = _t()
        if not self._server.listen(self.channel):
            QLocalServer.removeServer(self.channel)
            if not self._server.listen(self.channel):
                print(f"[ipc] 监听失败 {self.channel}:",
                      self._server.errorString())
                return False
        t2 = _t()
        self._server.newConnection.connect(self._on_new_conn)
        if self._role:
            register_process(self._role, self.channel, extra=self._extra)
        t3 = _t()
        _log("server.start", t0,
             f"channel={self.channel} "
             f"remove={1000*(t1-t0):.1f} listen={1000*(t2-t1):.1f} "
             f"reg={1000*(t3-t2):.1f}")
        return True

    def _on_new_conn(self):
        t0 = _t()
        conn = self._server.nextPendingConnection()
        reader = MessageReader(lambda t, p: self._on_message(t, p))
        self._readers[conn] = reader

        def _on_ready():
            t1 = _t()
            data = bytes(conn.readAll())
            reader.feed(data)
            _log("server.on_ready", t1,
                 f"channel={self.channel} bytes={len(data)}")

        def _on_disconn():
            self._readers.pop(conn, None)
            conn.deleteLater()

        conn.readyRead.connect(_on_ready)
        conn.disconnected.connect(_on_disconn)
        _log("server.new_conn", t0, f"channel={self.channel}")

    def stop(self):
        try:
            self._server.close()
        except Exception:
            pass
        if self._role:
            unregister_process(self._role)


class IpcClient:
    def __init__(self, channel):
        self.channel = channel

    def send(self, msg_type, payload=b"", timeout_ms=600):
        if not IPC_TIMING:
            sock = QLocalSocket()
            sock.connectToServer(self.channel)
            if not sock.waitForConnected(timeout_ms):
                return False
            sock.write(encode(msg_type, payload))
            sock.flush()
            sock.waitForBytesWritten(300)
            sock.disconnectFromServer()
            return True

        t0 = _t()
        sock = QLocalSocket()
        sock.connectToServer(self.channel)
        t1 = _t()
        if not sock.waitForConnected(timeout_ms):
            _log("client.connect 超时", t0,
                 f"channel={self.channel}")
            return False
        t2 = _t()
        sock.write(encode(msg_type, payload))
        sock.flush()
        sock.waitForBytesWritten(300)
        t3 = _t()
        sock.disconnectFromServer()
        _log("client.send", t0,
             f"channel={self.channel} type={msg_type} "
             f"connect={1000*(t1-t0):.1f} wait={1000*(t2-t1):.1f} "
             f"write={1000*(t3-t2):.1f}")
        return True

    @staticmethod
    def send_to_role(role, msg_type, payload=b"", timeout_ms=600):
        entry = find_process(role)
        if not entry:
            return False
        return IpcClient(entry["channel"]).send(
            msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_host_window(host, msg_type, payload=b"", timeout_ms=600):
        role, entry = find_window_by_host(host)
        if not role:
            return False
        return IpcClient(entry["channel"]).send(
            msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_tray(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_TRAY, msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_bar(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_BAR, msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_settings(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_SETTINGS, msg_type, payload, timeout_ms
        )

    @staticmethod
    def send_to_downloads(msg_type, payload=b"", timeout_ms=600):
        return IpcClient.send_to_role(
            ROLE_DOWNLOADS, msg_type, payload, timeout_ms
        )


# ======================================================================
# 广播：遍历注册表，给每个进程逐个发
# ======================================================================
def broadcast(msg_type, payload=b"", exclude_role=None, timeout_ms=400):
    data = _read_registry()
    count = 0
    for role, entry in data.items():
        if exclude_role and role == exclude_role:
            continue
        ch = entry.get("channel")
        if not ch:
            continue
        try:
            if IpcClient(ch).send(msg_type, payload, timeout_ms):
                count += 1
        except Exception:
            pass
    return count


class RegistryWatchdog:
    def __init__(self, interval_ms=3000, parent=None):
        self._timer = QTimer(parent)
        self._timer.setInterval(interval_ms)
        self._timer.timeout.connect(cleanup_registry)

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()
```

### component\loader.py (大小: 4070 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""环境初始化：路径、字体。

换用 qtwebview2（WebView2 / Edge 内核）后：
  * 不再需要 QtWebEngine 的 flags、进程路径、插件路径设置。
  * 不再需要 PyQt6-WebEngine。
"""

import os
import sys

import apppaths

BASE = apppaths.RES_DIR

if not apppaths.FROZEN:
    # 以下只在源码模式需要：打包后依赖已经内嵌，由 PyInstaller 负责
    # 加载 library 根（comtypes 等平级包）
    sys.path.insert(0, os.path.join(BASE, "library"))
    # 加载 browser-oxide 库
    sys.path.insert(0, os.path.join(BASE, "library", "browser-oxide"))
    # 加载 PyQt6 库
    sys.path.insert(0, os.path.join(BASE, "library", "PyQt6"))
    # 加载 pywin32 库
    sys.path.insert(0, os.path.join(BASE, "library", "pywin32"))
    # 加载 qtwebview2 库
    sys.path.insert(0, os.path.join(BASE, "library", "qtwebview2"))

    # pywin32 是"非标准"布局：扩展在 win32/，纯 py 在 win32/lib/，
    # DLL 在 pywin32_system32/。不补这几条会静默 fallback 到全局
    # site-packages 的同名包（换台机器就 import 不到）。
    _PW32 = os.path.join(BASE, "library", "pywin32")
    for _sub in (("win32", "lib"), ("win32",), ("pywin32_system32",)):
        _d = os.path.join(_PW32, *_sub)
        if os.path.isdir(_d):
            sys.path.insert(0, _d)
    _PW32_DLL = os.path.join(_PW32, "pywin32_system32")
    if os.path.isdir(_PW32_DLL):
        try:
            os.add_dll_directory(_PW32_DLL)
        except Exception:
            pass

    # 设置 Qt 平台插件路径（PyQt6 本身仍需要）
    QT_ROOT = os.path.join(BASE, "library", "PyQt6", "PyQt6", "Qt6")
else:
    # 打包后 PyQt6 被放在 _MEIPASS/PyQt6，Qt6 在其下
    QT_ROOT = os.path.join(BASE, "PyQt6", "Qt6")

_PLUGINS = os.path.join(QT_ROOT, "plugins")
if os.path.isdir(_PLUGINS):
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
        _PLUGINS, "platforms"
    )

# 将 Qt 核心库目录加入 DLL 搜索路径
for d in (os.path.join(QT_ROOT, "bin"), os.path.join(QT_ROOT, "lib")):
    if os.path.isdir(d):
        try:
            os.add_dll_directory(d)
        except Exception:
            pass

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


# 过滤 Qt 的所有日志消息
# （源码模式仍然全静默；打包模式把 Qt 自己的告警也记进日志，
#   否则窗口程序里 Qt 报的错一点痕迹都不留）
def _silent_message_handler(msg_type, context, message):
    if apppaths.FROZEN:
        try:
            print("[Qt]", message)
        except Exception:
            pass


qInstallMessageHandler(_silent_message_handler)

import win32gui
import win32con

# browser_oxide 装了但全项目没有任何使用点（72MB 原生扩展）。
# 打包时默认不带它，所以这里允许缺失，缺了也不该拦启动。
try:
    import browser_oxide            # noqa: F401
except Exception:
    browser_oxide = None


# ----------------------------------------------------------------------
# 应用字体（Qt 侧使用）
# ----------------------------------------------------------------------
_APP_FONTS_LOADED = False


def load_app_fonts():
    """把 assets/fonts/ 下的 ttf/otf/ttc 注册到 Qt。返回注册的字体族名列表。"""
    global _APP_FONTS_LOADED
    if _APP_FONTS_LOADED:
        return []
    _APP_FONTS_LOADED = True

    fonts_dir = os.path.join(BASE, "assets", "fonts")
    if not os.path.isdir(fonts_dir):
        return []

    loaded = []
    for name in os.listdir(fonts_dir):
        if name.startswith("."):
            continue
        if os.path.splitext(name)[1].lower() not in (".ttf", ".otf", ".ttc"):
            continue
        path = os.path.join(fonts_dir, name)
        fid = QFontDatabase.addApplicationFont(path)
        if fid != -1:
            loaded.extend(QFontDatabase.applicationFontFamilies(fid))
    return loaded
```

### component\main_app.py (大小: 15224 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""浏览器主进程：系统托盘 + bar 子进程 + 设置子进程 + 下载子进程 + IPC。

托盘负责：
  * 托盘图标 + 菜单
  * 起 / 停悬浮条（bar）
  * 起 / 停设置进程（settings_app）
  * 起 / 停下载进程（downloads_app），常驻
  * 配置广播
  * 语言切换
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths
from i18n import t
from ipc import (
    IpcClient, IpcServer,
    CHANNEL_BAR, ROLE_BAR,
    CHANNEL_TRAY, ROLE_TRAY,
    ROLE_SETTINGS, ROLE_DOWNLOADS,
    MSG_SHOW, MSG_HIDE, MSG_QUIT,
    MSG_OPEN_SETTINGS, MSG_SETTINGS_SHOW,
    MSG_OPEN_DOWNLOADS, MSG_DOWNLOADS_SHOW,
    MSG_LANGUAGE_CHANGED,
    find_windows, RegistryWatchdog,
)
from i18n import load, t, on_change
from settings_backend import SettingsBackend


DATA_DIR = os.path.join(apppaths.RES_DIR, "data")
ICON_NAMES = ["icon.ico", "icon.png", "app.ico", "app.png", "tray.ico", "tray.png"]


def load_tray_icon():
    if os.path.isdir(DATA_DIR):
        for name in ICON_NAMES:
            path = os.path.join(DATA_DIR, name)
            if os.path.isfile(path):
                icon = QIcon(path)
                if not icon.isNull():
                    return icon
    return None


class BrowserTray:

    def __init__(self, app):
        self.app = app
        self.bar_proc = None
        self.settings_proc = None
        self.downloads_proc = None
        self._starting = False
        self._on_change_cb = None
        self._quitting = False

        self.ipc_bar = IpcClient(CHANNEL_BAR)

        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("[tray] 警告: 系统托盘不可用，托盘图标可能不显示")

        icon = load_tray_icon()
        if icon is None:
            icon = app.style().standardIcon(QStyle.SP_ComputerIcon)
            print("[tray] 未找到 data/icon.ico，使用系统默认图标")
        else:
            print("[tray] 托盘图标已加载")

        self.tray = QSystemTrayIcon(icon, app)
        self.tray.setToolTip(t("app.title"))

        self.menu = QMenu()
        self._build_menu()
        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

        # 诊断：Qt 侧到底有没有把图标交给系统。
        # 如果这里 isVisible=True 且 sizes 非空，但屏幕上仍看不到图标，
        # 那就是 Windows 通知区域把它默认收进了溢出区（"^" 里），
        # 需要用户在 设置→个性化→任务栏→其他系统托盘图标 里打开。
        try:
            _sizes = [(s.width(), s.height()) for s in icon.availableSizes()]
            print("[tray] platform=%s trayAvailable=%s supportsMessages=%s"
                  % (app.platformName(),
                     QSystemTrayIcon.isSystemTrayAvailable(),
                     QSystemTrayIcon.supportsMessages()))
            print("[tray] iconSizes=%s tray.isVisible=%s"
                  % (_sizes, self.tray.isVisible()))
        except Exception as e:
            print("[tray] 托盘诊断失败:", e)

        self._tray_server = IpcServer(
            CHANNEL_TRAY, self._on_tray_message, role=ROLE_TRAY
        )
        if not self._tray_server.start():
            print("[tray] 托盘 IPC 监听失败（可能已有实例在跑）")

        self.watchdog = RegistryWatchdog(interval_ms=3000, parent=app)
        self.watchdog.start()

        self.start_bar()
        self.start_downloads()

        # 托盘是父进程：每 5 秒体检一次，bar / 下载进程掉了就自动拉起。
        # 这样无论子进程是崩溃、启动失败还是被杀，都能恢复，
        # 下载记录 / 进度 / 完成弹窗才不会静默失效。
        self._health_timer = QTimer(app)
        self._health_timer.setInterval(5000)
        self._health_timer.timeout.connect(self._health_check)
        self._health_timer.start()

    def _health_check(self):
        if self._quitting:
            return
        try:
            if not self._bar_running():
                self.start_bar()
            if not self._downloads_running():
                self.start_downloads()
        except Exception as e:
            print("[tray] 体检异常:", e)

        self._on_change_cb = self._refresh_texts
        try:
            on_change(self._on_change_cb)
        except Exception as e:
            print("[tray] 注册语言回调失败:", e)

    def _build_menu(self):
        """重建托盘菜单。语言切换时也调这个。"""
        self.menu.clear()
        self.menu.addAction(t("tray.show_bar"), self.show_bar)
        self.menu.addAction(t("tray.hide_bar"), self.hide_bar)
        self.menu.addSeparator()
        self.menu.addAction(t("tray.settings"), self.open_settings)
        self.menu.addAction(t("tray.downloads"), self.open_downloads)
        self.menu.addSeparator()
        self.menu.addAction(t("tray.quit"), self.quit)

    def _refresh_texts(self):
        """语言变化后刷新托盘文字。"""
        try:
            self.tray.setToolTip(t("app.title"))
        except Exception:
            pass
        self._build_menu()

    # ==========================================================
    # 托盘 IPC 消息
    # ==========================================================
    def _on_tray_message(self, msg_type, payload):
        if msg_type == MSG_SHOW:
            # 第二次双击 exe 时走这里：把悬浮条重新显示出来
            self.show_bar()
        elif msg_type == MSG_OPEN_SETTINGS:
            self.open_settings()
        elif msg_type == MSG_OPEN_DOWNLOADS:
            self.open_downloads()
        elif msg_type == MSG_LANGUAGE_CHANGED:
            try:
                code = payload.decode("utf-8")
                load(code)
                self._refresh_texts()
            except Exception as e:
                print("[tray] 切换语言失败:", e)

    # ==========================================================
    # bar 子进程
    # ==========================================================
    def start_bar(self):
        if self._bar_running() or self._starting:
            return
        self._starting = True

        try:
            self.bar_proc = QProcess()
            _prog, _args = apppaths.role_command("bar")
            self.bar_proc.setProgram(_prog)
            self.bar_proc.setArguments(_args)
            apppaths.configure_child_proc(self.bar_proc)
            self.bar_proc.finished.connect(self._on_bar_finished)
            self.bar_proc.errorOccurred.connect(self._on_bar_error)
            self.bar_proc.start()
            print(f"[tray] 已启动 bar 子进程 prog={_prog} args={_args}")
        except Exception as e:
            self._starting = False
            print("[tray] 启动 bar 子进程异常:", e)
            return

        QTimer.singleShot(800, self._clear_starting)

    def _clear_starting(self):
        self._starting = False

    def _bar_running(self):
        return (self.bar_proc is not None
                and self.bar_proc.state() != QProcess.ProcessState.NotRunning)

    def _on_bar_finished(self, exit_code, exit_status):
        self._starting = False
        print(f"[tray] bar 子进程已结束 exit_code={exit_code} "
              f"status={exit_status}")
        # 托盘是父进程：bar 意外退出就自动拉起来（正常退出流程里 _quitting=True）
        if not self._quitting:
            print("[tray] bar 意外退出，3 秒后重启")
            QTimer.singleShot(3000, self.start_bar)

    def _on_bar_error(self, error):
        self._starting = False
        print(f"[tray] bar 子进程错误: {error}")

    # ==========================================================
    # 显示 / 隐藏悬浮条
    # ==========================================================
    def show_bar(self):
        if not self._bar_running():
            self.start_bar()
            QTimer.singleShot(900, lambda: self.ipc_bar.send(MSG_SHOW))
        else:
            self.ipc_bar.send(MSG_SHOW)

    def hide_bar(self):
        if self._bar_running():
            self.ipc_bar.send(MSG_HIDE)

    # ==========================================================
    # 设置子进程
    # ==========================================================
    def _settings_running(self):
        return (self.settings_proc is not None
                and self.settings_proc.state() != QProcess.ProcessState.NotRunning)

    def _start_settings(self):
        if self._settings_running():
            return
        self.settings_proc = QProcess()
        _prog, _args = apppaths.role_command("settings")
        self.settings_proc.setProgram(_prog)
        self.settings_proc.setArguments(_args)
        apppaths.configure_child_proc(self.settings_proc)
        self.settings_proc.finished.connect(self._on_settings_finished)
        self.settings_proc.errorOccurred.connect(self._on_settings_error)
        self.settings_proc.start()
        print("[tray] 已启动设置子进程")

    def _on_settings_finished(self, exit_code, exit_status):
        print(f"[tray] 设置子进程已结束 exit_code={exit_code} "
              f"status={exit_status}")

    def _on_settings_error(self, error):
        print(f"[tray] 设置子进程错误: {error}")

    def _send_show_settings(self):
        try:
            IpcClient.send_to_role(ROLE_SETTINGS, MSG_SETTINGS_SHOW)
        except Exception as e:
            print("[tray] 发送显示设置消息失败:", e)

    def open_settings(self):
        """打开设置窗口。设置进程没起就起，起了就发显示消息。"""
        if not self._settings_running():
            self._start_settings()
            QTimer.singleShot(1200, self._send_show_settings)
        else:
            self._send_show_settings()

    # ==========================================================
    # 下载子进程
    # ==========================================================
    def _downloads_running(self):
        return (self.downloads_proc is not None
                and self.downloads_proc.state() != QProcess.ProcessState.NotRunning)

    def start_downloads(self):
        """启动下载进程（常驻）。"""
        if self._downloads_running():
            return
        try:
            self.downloads_proc = QProcess()
            _prog, _args = apppaths.role_command("downloads")
            self.downloads_proc.setProgram(_prog)
            self.downloads_proc.setArguments(_args)
            apppaths.configure_child_proc(self.downloads_proc)
            self.downloads_proc.finished.connect(self._on_downloads_finished)
            self.downloads_proc.errorOccurred.connect(self._on_downloads_error)
            self.downloads_proc.start()
            print("[tray] 已启动下载子进程")
        except Exception as e:
            print("[tray] 启动下载子进程异常:", e)

    def _on_downloads_finished(self, exit_code, exit_status):
        print(f"[tray] 下载子进程已结束 exit_code={exit_code} "
              f"status={exit_status}")
        # 下载进程是常驻的：意外退出就自动拉起，
        # 否则下载记录、进度、完成弹窗全都静默失效
        if not self._quitting:
            print("[tray] 下载进程意外退出，3 秒后重启")
            QTimer.singleShot(3000, self.start_downloads)

    def _on_downloads_error(self, error):
        print(f"[tray] 下载子进程错误: {error}")

    def _send_show_downloads(self):
        try:
            IpcClient.send_to_role(ROLE_DOWNLOADS, MSG_DOWNLOADS_SHOW)
        except Exception as e:
            print("[tray] 发送显示下载消息失败:", e)

    def open_downloads(self):
        """打开下载窗口。下载进程没起就起，起了就发显示消息。"""
        if not self._downloads_running():
            self.start_downloads()
            QTimer.singleShot(1200, self._send_show_downloads)
        else:
            self._send_show_downloads()

    # ==========================================================
    # 托盘事件
    # ==========================================================
    def _on_tray_activated(self, reason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.show_bar()

    # ==========================================================
    # 退出
    # ==========================================================
    def quit(self):
        self._quitting = True
        if self._bar_running():
            self.ipc_bar.send(MSG_QUIT)
            if not self.bar_proc.waitForFinished(2000):
                self.bar_proc.kill()

        if self._settings_running():
            try:
                IpcClient.send_to_role(ROLE_SETTINGS, MSG_QUIT)
            except Exception:
                pass
            if not self.settings_proc.waitForFinished(1500):
                self.settings_proc.kill()

        if self._downloads_running():
            try:
                IpcClient.send_to_role(ROLE_DOWNLOADS, MSG_QUIT)
            except Exception:
                pass
            if not self.downloads_proc.waitForFinished(1500):
                self.downloads_proc.kill()

        try:
            self._tray_server.stop()
        except Exception:
            pass
        try:
            self.watchdog.stop()
        except Exception:
            pass

        self.tray.hide()
        self.app.quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 单实例：托盘是唯一主进程。已经有一个托盘在跑就不再起第二个，
    # 而是让**已经在跑的那个**把悬浮条显示出来 —— 这样"再双击一次 exe"
    # 的效果是"把界面叫出来"，而不是静默什么都不发生。
    try:
        from PyQt6.QtNetwork import QLocalSocket
        _sock = QLocalSocket()
        _sock.connectToServer(CHANNEL_TRAY)
        if _sock.waitForConnected(400):
            print("[tray] 已有一个托盘实例在运行 → 让它显示悬浮条，本次退出")
            try:
                IpcClient(CHANNEL_TRAY).send(MSG_SHOW)
            except Exception as e:
                print("[tray] 通知已有实例失败:", e)
            sys.exit(0)
    except Exception as e:
        print("[tray] 单实例检查失败（忽略）:", e)

    # 读语言（在创建托盘之前）
    try:
        load(SettingsBackend().get_language())
    except Exception as e:
        print("[tray] 加载语言失败:", e)

    _ = BrowserTray(app)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

### component\notify_store.py (大小: 3193 | 修改时间: 2026-10-03 03:30:48 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""完成提醒的按站点开关（独立存储，不依赖固定项）。

背景
----
「完成提醒」= DOM 监控：IDLE 态下 new 簇占多数 → 进入 W 态；
W 态下 5 秒无新增 → 自然死亡 → 响铃 + 强制窗口置顶。

原先这个开关的状态只写在**固定项**里，而且：
  * 保存：`if host and pinned_store.is_pinned(host)` —— 没固定就不写盘
  * 恢复：读固定项的那段代码嵌在 `if is_pinned(...)` 分支里面

后果：对**没有固定**的站点打开「完成提醒」，当次会话有效，
关掉窗口就忘了，下次打开又变回关 —— 看起来像"功能丢了"。

现在单独存一份 userdata/complete_notify.json：
    { "bilibili.com": true, "bing.com": false }

固定项里的 complete_notify 仍然保留（兼容旧数据），两边**取或**。
"""

import json
import os

import apppaths

STORE_PATH = os.path.join(apppaths.APP_DIR, "userdata", "complete_notify.json")


def _normalize(host):
    """归一到主域。既接受 bilibili.com，也容忍传进来的是完整 URL。"""
    if not host:
        return ""
    h = str(host).strip().lower()
    if "//" in h:                       # https://www.bilibili.com/x -> www.bilibili.com/x
        h = h.split("//", 1)[1]
    for sep in ("/", "?", "#"):         # 去掉路径、查询、片段
        h = h.split(sep, 1)[0]
    h = h.split("@")[-1].split(":")[0]  # 去掉 user@ 和端口
    h = h.strip(".")
    if h.startswith("www."):
        h = h[4:]
    parts = h.split(".")
    if len(parts) <= 2:
        return h
    return ".".join(parts[-2:])


def load():
    """读全部记录。返回 {host: bool}。文件不存在或损坏都返回空。"""
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return {str(k): bool(v) for k, v in data.items()}
    except Exception:
        return {}


def get(host):
    """查某个站点的开关。没有记录返回 False。"""
    return bool(load().get(_normalize(host), False))


def set(host, on):  # noqa: A001 - 保持与 pinned_store 风格一致的命名
    """写某个站点的开关。返回是否成功。"""
    h = _normalize(host)
    if not h:
        return False
    data = load()
    if on:
        data[h] = True
    else:
        data.pop(h, None)
    try:
        os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
        tmp = STORE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, STORE_PATH)
        print("[notify_store] %s = %s" % (h, bool(on)))
        return True
    except Exception as e:
        print("[notify_store] 写盘失败:", e)
        return False


def is_on(host):
    """带旧数据兼容：独立存储或固定项里任一为真，就认为开着。"""
    if get(host):
        return True
    try:
        import pinned_store
        item = pinned_store.load_one(_normalize(host))
        return bool(item and item.get("complete_notify"))
    except Exception:
        return False

```

### component\password_hook.py (大小: 21302 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""密码保存 / 填充功能（纯函数模块，不写类）。

由 window.RoundedWindow 调用：
  * install(window)            —— 注入信号、建面板
  * on_js_message(window, d)   —— 处理 JS 来的消息，返回 True 表示已处理

面板形态（两个状态，用户只能切换，不能关闭）：
  * 展开态：账密列表 + "保存当前账密"按钮
  * 收起态：只留顶部一条横条（带 ⌃）

显隐完全由"页面有没有账密输入框"决定：
  * has_pw: false -> true   面板出现（用上次的形态）
  * has_pw: true  -> false  面板消失
  * has_pw 一直 true        只更新列表

面板贴在主窗口右上角、标题栏下方，展开态 / 收起态都能沿上边缘左右拖。

存储：项目根目录 passwords.json
    {
        "bigmodel.cn": [
            {"username": "999", "password": "123"},
            ...
        ],
        ...
    }
列表只显示"当前页主域"对应的那组账密。
"""
from i18n import t
import os
import json

from loader import *


# ======================================================================
# 路径
# ======================================================================
import apppaths

STORE_PATH = os.path.join(apppaths.APP_DIR, "passwords.json")


# ======================================================================
# 注入 JS
# ======================================================================
PASSWORD_JS = r"""
(function() {
    if (window.__pw_watch_installed) return;
    window.__pw_watch_installed = true;

    function report(msg) {
        try {
            if (window.chrome && window.chrome.webview) {
                window.chrome.webview.postMessage(JSON.stringify(msg));
            } else if (window.ipc && window.ipc.postMessage) {
                window.ipc.postMessage(JSON.stringify(msg));
            }
        } catch (e) {}
    }

    function findUserInput(pwEl) {
        var form = pwEl.closest("form");
        var scope = form || document.body;
        var allInputs = scope.querySelectorAll(
            'input:not([type="password"]):not([type="hidden"])' +
            ':not([type="submit"]):not([type="button"])' +
            ':not([type="checkbox"]):not([type="radio"])' +
            ':not([type="file"]):not([type="image"])'
        );
        var result = null;
        for (var i = 0; i < allInputs.length; i++) {
            var el = allInputs[i];
            if (el.compareDocumentPosition(pwEl) &
                Node.DOCUMENT_POSITION_FOLLOWING) {
                result = el;
            } else {
                break;
            }
        }
        if (result) return result;
        return allInputs.length > 0 ? allInputs[0] : null;
    }

    function clearVal(el) {
        if (!el) return;
        try {
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, "value"
            ).set;
            setter.call(el, "");
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        } catch (e) {
            el.value = "";
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        }
    }

    function fillVal(el, val) {
        if (!el || !val) return;
        try {
            var setter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, "value"
            ).set;
            setter.call(el, val);
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        } catch (e) {
            el.value = val;
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        }
    }

    window.__pw_clear_all = function() {
        try {
            var pwInputs = document.querySelectorAll('input[type="password"]');
            for (var i = 0; i < pwInputs.length; i++) {
                clearVal(pwInputs[i]);
            }
            var allUserInputs = document.querySelectorAll(
                'input:not([type="password"]):not([type="hidden"])' +
                ':not([type="submit"]):not([type="button"])' +
                ':not([type="checkbox"]):not([type="radio"])' +
                ':not([type="file"]):not([type="image"])'
            );
            for (var j = 0; j < allUserInputs.length; j++) {
                clearVal(allUserInputs[j]);
            }
            return "ok";
        } catch (e) {
            return "err:" + e;
        }
    };

    window.__pw_fill = function(user, pw) {
        try {
            var pwInputs = document.querySelectorAll('input[type="password"]');
            if (pwInputs.length === 0) return "no_pw_input";

            var pwInput = pwInputs[0];
            var userInput = findUserInput(pwInput);

            if (pw) fillVal(pwInput, pw);
            if (userInput && user) fillVal(userInput, user);

            return "ok";
        } catch (e) {
            return "err:" + e;
        }
    };

    function currentCredential() {
        var pwInputs = document.querySelectorAll('input[type="password"]');
        for (var i = 0; i < pwInputs.length; i++) {
            var pw = pwInputs[i].value || "";
            if (!pw) continue;
            var userInput = findUserInput(pwInputs[i]);
            var user = userInput ? (userInput.value || "") : "";
            return { user: user, pw: pw };
        }
        return null;
    }

    function hasPasswordInput() {
        return document.querySelectorAll('input[type="password"]').length > 0;
    }

    setInterval(function() {
        try {
            var hasPw = hasPasswordInput();
            var c = hasPw ? currentCredential() : null;
            report({
                type: "pw_state",
                has_pw: hasPw,
                username: c ? c.user : "",
                password: c ? c.pw : "",
                url: location.href
            });
        } catch (e) {}
    }, 800);
})();
"""


# ======================================================================
# 存储
# ======================================================================
def _root_host(host):
    if not host:
        return ""
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])


def _host_of_url(url):
    try:
        from urllib.parse import urlparse
        return _root_host(urlparse(url).hostname or "")
    except Exception:
        return ""


def _load_store():
    try:
        if os.path.isfile(STORE_PATH):
            with open(STORE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _save_store(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[pw] 存失败:", e)


# ======================================================================
# 面板尺寸 / 颜色
# ======================================================================
PANEL_W = 240
PANEL_H_EXPANDED = 200
PANEL_H_COLLAPSED = 32    # 收起态加高，避免文字被上下边挤
TOP_MARGIN = 41           # 标题栏底部 39 + 缝隙 2
SIDE_MARGIN = 16          # 面板右侧距窗口右边
RADIUS = 8

BG_COLOR = QColor(60, 60, 60, 245)          # 深灰
BORDER_COLOR = QColor(138, 138, 138, 255)   # 浅灰
TEXT_COLOR = "#e0e0e0"
SUBTEXT_COLOR = "#a0a0a0"


# ======================================================================
# 面板控件（自绘圆角）
# ======================================================================
class _PwPanel(QFrame):
    """方形面板。子控件，parent 为主窗口。"""

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet(
            "QFrame {"
            "  background: rgb(60, 60, 60);"
            "  border: 1px solid rgb(138, 138, 138);"
            "}"
        )


# ======================================================================
# 安装
# ======================================================================
def install(window):
    window._pw_installed = False
    window._pw_panel = None
    window._pw_expanded = True
    window._pw_visible = False
    window._pw_has_pw = False
    window._pw_cur_user = ""
    window._pw_cur_pw = ""
    window._pw_drag_offset = None
    window._pw_panel_x = None
    window._pw_hide_timer = None       # 延迟收回

    QTimer.singleShot(0, lambda: _build_panel(window))


def _build_panel(window):
    panel = _PwPanel(window)
    panel.setFixedSize(PANEL_W, PANEL_H_EXPANDED)
    panel.hide()

    outer = QVBoxLayout(panel)
    outer.setContentsMargins(10, 6, 10, 10)
    outer.setSpacing(6)

    # ---- 顶部条：标题 + 收起按钮 ----
    head = QHBoxLayout()
    head.setContentsMargins(0, 0, 0, 0)
    head.setSpacing(4)

    title = QLabel(t("password.panel_title"))
    title.setStyleSheet(
        f"color: {TEXT_COLOR}; background: transparent;"
        f"border: none; font-size: 12px;")
    head.addWidget(title)
    head.addStretch(1)

    toggle_btn = QPushButton("⌃")
    toggle_btn.setFixedSize(20, 18)
    toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    toggle_btn.setStyleSheet(
        f"QPushButton {{"
        f"  color: {SUBTEXT_COLOR}; background: transparent;"
        f"  border: none; font-size: 12px;"
        f"}}"
        f"QPushButton:hover {{ color: {TEXT_COLOR}; }}"
    )
    toggle_btn.clicked.connect(lambda: _toggle_expand(window))
    head.addWidget(toggle_btn)

    outer.addLayout(head)

    # ---- 列表 ----
    lst = QListWidget(panel)
    lst.setStyleSheet(
        f"QListWidget {{"
        f"  background: rgba(255,255,255,0.06);"
        f"  border: 1px solid rgba(255,255,255,0.15);"
        f"  color: {TEXT_COLOR};"
        f"  font-size: 12px;"
        f"  outline: none;"
        f"}}"
        f"QListWidget::item {{ height: 28px; padding-left: 6px; }}"
        f"QListWidget::item:hover {{ background: rgba(255,255,255,0.10); }}"
        f"QListWidget::item:selected {{"
        f"  background: rgba(120,170,255,0.35); color: #ffffff;"
        f"}}"
    )
    lst.itemClicked.connect(lambda item: _on_item_clicked(window, item))
    outer.addWidget(lst, 1)

    # ---- 安全提示 ----
    warn_lbl = QLabel(t("password.warning"))
    warn_lbl.setWordWrap(True)
    warn_lbl.setStyleSheet(
        "color: #e0a060; background: transparent;"
        "border: none; font-size: 10px;")
    outer.addWidget(warn_lbl)
    # ------------------

    # ---- 保存按钮 ----
    save_btn = QPushButton(t("password.save_current"))
    save_btn.setFixedHeight(28)
    save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
    save_btn.setStyleSheet(
        f"QPushButton {{"
        f"  background: rgba(255,255,255,0.10);"
        f"  color: {TEXT_COLOR};"
        f"  border: 1px solid rgba(255,255,255,0.20);"
        f"  font-size: 12px;"
        f"}}"
        f"QPushButton:hover {{ background: rgba(255,255,255,0.16); }}"
        f"QPushButton:pressed {{ background: rgba(255,255,255,0.22); }}"
    )
    save_btn.clicked.connect(lambda: _on_save_clicked(window))
    outer.addWidget(save_btn)

    # 面板拖动
    panel.mousePressEvent = lambda e: _panel_mouse_press(window, e)
    panel.mouseMoveEvent = lambda e: _panel_mouse_move(window, e)
    panel.mouseReleaseEvent = lambda e: _panel_mouse_release(window, e)

    window._pw_panel = panel
    window._pw_widgets = {
        "title": title,
        "toggle": toggle_btn,
        "list": lst,
        "save": save_btn,
        "warn": warn_lbl,
    }
    window._pw_installed = True

    print(f"[DBG] pw panel built, size={panel.size()}")

    _relayout(window)


def _relayout(window):
    panel = getattr(window, "_pw_panel", None)
    if panel is None:
        return

    if window._pw_expanded:
        h = PANEL_H_EXPANDED
    else:
        h = PANEL_H_COLLAPSED
    panel.setFixedSize(PANEL_W, h)

    if window._pw_panel_x is None:
        x = window.width() - PANEL_W - SIDE_MARGIN
    else:
        x = window._pw_panel_x
        max_x = max(0, window.width() - PANEL_W)
        x = max(0, min(max_x, x))
        window._pw_panel_x = x

    y = TOP_MARGIN
    panel.move(int(x), int(y))
    panel.raise_()


# ======================================================================
# 形态切换 / 显隐
# ======================================================================
def _toggle_expand(window):
    window._pw_expanded = not window._pw_expanded
    _apply_expand(window)
    _relayout(window)


def _apply_expand(window):
    w = getattr(window, "_pw_widgets", None)
    if w is None:
        return
    show = window._pw_expanded
    w["list"].setVisible(show)
    w["save"].setVisible(show)
    if "warn" in w:
        w["warn"].setVisible(show)
    w["toggle"].setText("⌃" if show else "⌄")


def _show_panel(window):
    panel = getattr(window, "_pw_panel", None)
    if panel is None:
        return
    _apply_expand(window)
    _relayout(window)
    panel.show()
    panel.raise_()
    window._pw_visible = True
    print(f"[DBG] _show_panel visible={panel.isVisible()} "
          f"geo={panel.geometry()} parent={panel.parent()}")


def _hide_panel(window):
    panel = getattr(window, "_pw_panel", None)
    if panel is None:
        return
    panel.hide()
    window._pw_visible = False


# ======================================================================
# 列表
# ======================================================================
def _current_host(window):
    url = getattr(window, "_current_url", "") or ""
    if not url:
        try:
            wv = window.web_view
            if wv is not None:
                url = str(wv.url() or "")
        except Exception:
            url = ""
    return _host_of_url(url)


def _reload_list(window):
    w = getattr(window, "_pw_widgets", None)
    if w is None:
        return
    lst = w["list"]
    lst.clear()

    host = _current_host(window)
    if not host:
        return

    store = _load_store()
    items = store.get(host, [])
    if not isinstance(items, list):
        return

    for i, rec in enumerate(items):
        user = rec.get("username", "") or t("password.no_username")
        item = QListWidgetItem(user)
        item.setData(Qt.ItemDataRole.UserRole, i)
        lst.addItem(item)


def _on_item_clicked(window, item):
    if item is None:
        return
    idx = item.data(Qt.ItemDataRole.UserRole)
    if idx is None:
        return

    host = _current_host(window)
    if not host:
        return

    store = _load_store()
    items = store.get(host, [])
    if not isinstance(items, list):
        return
    if idx < 0 or idx >= len(items):
        return

    rec = items[idx]
    user = rec.get("username", "")
    pw = rec.get("password", "")
    if not pw:
        return

    _fill_to_page(window, user, pw)


def _on_save_clicked(window):
    user = getattr(window, "_pw_cur_user", "") or ""
    pw = getattr(window, "_pw_cur_pw", "") or ""
    if not pw:
        return

    host = _current_host(window)
    if not host:
        return

    store = _load_store()
    items = store.get(host, [])
    if not isinstance(items, list):
        items = []

    for it in items:
        if (it.get("username") == user
                and it.get("password") == pw):
            return

    items.insert(0, {"username": user, "password": pw})
    store[host] = items
    _save_store(store)
    _reload_list(window)


# ======================================================================
# 填充
# ======================================================================
def _fill_to_page(window, user, pw):
    wv = getattr(window, "web_view", None)
    if wv is None:
        return

    try:
        wv.eval_js(
            "(function(){"
            "  if (window.__pw_clear_all) return window.__pw_clear_all();"
            "  return 'no_clear_fn';"
            "})()",
            lambda r: None,
        )
    except Exception:
        pass

    def _do_fill():
        payload = json.dumps(
            {"user": user, "pw": pw}, ensure_ascii=False)
        js = f"""
        (function() {{
            var data = {payload};
            if (window.__pw_fill) {{
                return window.__pw_fill(data.user, data.pw);
            }}
            return "no_fill_fn";
        }})()
        """
        try:
            wv.eval_js(js, lambda r: None)
        except Exception:
            pass

    QTimer.singleShot(50, _do_fill)


# ======================================================================
# 拖动（沿上边缘平移）
# ======================================================================
def _panel_mouse_press(window, event):
    if event.button() != Qt.MouseButton.LeftButton:
        return
    window._pw_drag_offset = (
        event.globalPosition().toPoint().x()
        - window._pw_panel.mapToGlobal(QPoint(0, 0)).x()
    )


def _panel_mouse_move(window, event):
    if window._pw_drag_offset is None:
        return
    if not (event.buttons() & Qt.MouseButton.LeftButton):
        return

    panel = window._pw_panel
    global_x = event.globalPosition().toPoint().x()
    new_global_x = global_x - window._pw_drag_offset
    local_x = new_global_x - window.mapToGlobal(QPoint(0, 0)).x()

    max_x = max(0, window.width() - PANEL_W)
    local_x = max(0, min(max_x, local_x))
    window._pw_panel_x = local_x
    panel.move(int(local_x), TOP_MARGIN)


def _panel_mouse_release(window, event):
    window._pw_drag_offset = None


# ======================================================================
# 消息处理
# ======================================================================
def on_js_message(window, data):
    if not isinstance(data, dict):
        return False

    if data.get("type") != "pw_state":
        return False

    if getattr(window, "_pw_panel", None) is None:
        return True

    has_pw = bool(data.get("has_pw", False))
    user = data.get("username", "") or ""
    pw = data.get("password", "") or ""

    prev = getattr(window, "_pw_has_pw", False)
    window._pw_has_pw = has_pw

    window._pw_cur_user = user
    window._pw_cur_pw = pw

    # ---- 有密码框：取消待收回，按需显示 ----
    if has_pw:
        _cancel_hide(window)
        if not prev:
            _reload_list(window)
            _show_panel(window)
        else:
            _reload_list(window)
        return True

    # ---- 没有密码框：延迟 1.5 秒再收 ----
    if prev and not has_pw:
        _schedule_hide(window)
        return True

    return True


def _cancel_hide(window):
    t = getattr(window, "_pw_hide_timer", None)
    if t is not None:
        try:
            t.stop()
        except Exception:
            pass
        window._pw_hide_timer = None


def _schedule_hide(window):
    _cancel_hide(window)
    t = QTimer(window)
    t.setSingleShot(True)
    t.setInterval(1500)
    t.timeout.connect(lambda: _do_hide(window))
    t.start()
    window._pw_hide_timer = t


def _do_hide(window):
    window._pw_hide_timer = None
    if getattr(window, "_pw_has_pw", False):
        return
    _hide_panel(window)


# ======================================================================
# 供设置窗口调用的管理接口
# ======================================================================
def list_all():
    """返回全部账密：{host: [{"username", "password"}, ...]}"""
    return _load_store()


def delete_credential(host, index):
    """删 host 下第 index 条。成功返回 True。"""
    if not host:
        return False
    data = _load_store()
    items = data.get(host)
    if not isinstance(items, list):
        return False
    if index < 0 or index >= len(items):
        return False
    items.pop(index)
    if items:
        data[host] = items
    else:
        data.pop(host, None)
    _save_store(data)
    return True


def delete_host(host):
    """删 host 的全部账密。成功返回 True。"""
    if not host:
        return False
    data = _load_store()
    if host in data:
        data.pop(host)
        _save_store(data)
        return True
    return False
```

### component\personalize_dialog.py (大小: 21457 | 修改时间: 2026-10-03 12:51:00 | 权限: 666)

```
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
```

### component\pinned_store.py (大小: 7192 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""固定项存储。每个主域一个文件夹，放在项目根目录 fixed/ 下。

目录结构：
    fixed/
        bing.com/
            info.json      { host, hosts, popup_urls, last_index, added_time }
            icon.png       图标（favicon 或主域前两字母生成）
        bilibili.com/
            ...

host 作为文件夹名时，Windows 非法字符会被替换成 "_"；
info.json 里存原始 host。
"""

import os
import re
import json
import time
import shutil

import apppaths

FIXED_DIR = os.path.join(apppaths.APP_DIR, "fixed")

MAX_PINNED = 24

_ILLEGAL = r'[\\/:*?"<>|]'


def _normalize(host):
    """把 host 归一为主域。所有 API 入口都过它。"""
    if not host:
        return ""
    h = host.strip().lower()
    if h.startswith("www."):
        h = h[4:]
    parts = h.split(".")
    if len(parts) <= 2:
        return h
    return ".".join(parts[-2:])


def _safe_name(host):
    if not host:
        return "_"
    s = re.sub(_ILLEGAL, "_", host)
    s = s.strip().strip(".")
    return s or "_"


def _ensure_dir():
    os.makedirs(FIXED_DIR, exist_ok=True)


def _host_dir(host):
    return os.path.join(FIXED_DIR, _safe_name(host))


def _info_path(host):
    return os.path.join(_host_dir(host), "info.json")


def _icon_path(host):
    return os.path.join(_host_dir(host), "icon.png")


# ======================================================================
# 读
# ======================================================================
def load_one(host):
    """读一个固定项。返回 dict 或 None。损坏抛 ValueError。"""
    host = _normalize(host)
    if not host:
        return None
    path = _info_path(host)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise ValueError(f"固定项 {host} 的 info.json 损坏：{e}")
    if not isinstance(data, dict):
        raise ValueError(f"固定项 {host} 的 info.json 格式不对")
    return {
        "host": data.get("host", host),
        "hosts": list(data.get("hosts", [])),
        "popup_urls": list(data.get("popup_urls", [])),
        "last_index": int(data.get("last_index", -1)),
        "added_time": float(data.get("added_time", 0)),
        "complete_notify": bool(data.get("complete_notify", False)),
    }


def load_all():
    """读全部固定项。返回 (items, broken)。

    items 按 added_time 升序；broken 是损坏 host 列表。
    """
    _ensure_dir()
    items = []
    broken = []
    try:
        names = os.listdir(FIXED_DIR)
    except Exception:
        return [], []

    for name in names:
        full = os.path.join(FIXED_DIR, name)
        if not os.path.isdir(full):
            continue
        info = os.path.join(full, "info.json")
        if not os.path.isfile(info):
            broken.append(name)
            continue
        try:
            with open(info, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("not dict")
        except Exception:
            broken.append(name)
            continue

        items.append({
            "host": data.get("host", name),
            "hosts": list(data.get("hosts", [])),
            "popup_urls": list(data.get("popup_urls", [])),
            "last_index": int(data.get("last_index", -1)),
            "added_time": float(data.get("added_time", 0)),
            "complete_notify": bool(data.get("complete_notify", False)),
        })

    items.sort(key=lambda x: x.get("added_time", 0))
    return items, broken


def count():
    items, _ = load_all()
    return len(items)


def is_pinned(host):
    host = _normalize(host)
    if not host:
        return False
    return os.path.isfile(_info_path(host))


# ======================================================================
# 写
# ======================================================================
def add(host, hosts=None, popup_urls=None, last_index=-1, added_time=None,
        complete_notify=False):
    """新增固定项。已存在则覆盖。超 24 返回 False。"""
    host = _normalize(host)
    if not host:
        return False
    if not is_pinned(host) and count() >= MAX_PINNED:
        return False

    d = _host_dir(host)
    os.makedirs(d, exist_ok=True)

    data = {
        "host": host,
        "hosts": list(hosts or [host]),
        "popup_urls": list(popup_urls or []),
        "last_index": int(last_index),
        "added_time": float(added_time if added_time else time.time()),
        "complete_notify": bool(complete_notify),
    }
    try:
        with open(_info_path(host), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("[pinned] 写入失败:", e)
        return False


def save_one(host, hosts=None, popup_urls=None, last_index=None,
             complete_notify=None):
    """更新固定项字段（只更新传进来的）。不新建。"""
    host = _normalize(host)
    if not host:
        return False
    cur = load_one(host)
    if cur is None:
        return False
    if hosts is not None:
        cur["hosts"] = list(hosts)
    if popup_urls is not None:
        cur["popup_urls"] = list(popup_urls)
    if last_index is not None:
        cur["last_index"] = int(last_index)
    if complete_notify is not None:
        cur["complete_notify"] = bool(complete_notify)

    try:
        with open(_info_path(host), "w", encoding="utf-8") as f:
            json.dump(cur, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print("[pinned] 更新失败:", e)
        return False


def remove(host):
    host = _normalize(host)
    if not host:
        return False
    d = _host_dir(host)
    if not os.path.isdir(d):
        return False
    try:
        shutil.rmtree(d, ignore_errors=True)
        return True
    except Exception as e:
        print("[pinned] 删除失败:", e)
        return False


# ======================================================================
# 图标
# ======================================================================
def save_icon(host, pixmap):
    host = _normalize(host)
    if not host or pixmap is None or pixmap.isNull():
        return False
    d = _host_dir(host)
    if not os.path.isdir(d):
        return False
    try:
        return bool(pixmap.save(_icon_path(host), "PNG"))
    except Exception as e:
        print("[pinned] 图标保存失败:", e)
        return False


def load_icon(host):
    from PyQt6.QtGui import QPixmap
    host = _normalize(host)
    if not host:
        return None
    p = _icon_path(host)
    if not os.path.isfile(p):
        return None
    pm = QPixmap(p)
    if pm.isNull():
        return None
    return pm
```

### component\popup_window.py (大小: 22687 | 修改时间: 2026-10-02 11:07:37 | 权限: 666)

```
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
```

### component\rounded_menu.py (大小: 1497 | 修改时间: 2026-10-02 13:49:59 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""圆角菜单。"""

from loader import *
from theme import Theme


class RoundedMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(
            "QMenu {"
            "  background: transparent;"
            "  border: none;"
            "  padding: 4px;"
            "}"
            "QMenu::item {"
            "  padding: 4px 20px 4px 12px;"
            "  border-radius: 4px;"
            "  color: #333333;"
            "  background: transparent;"
            "}"
            "QMenu::item:selected {"
            "  background: #e8f0fe;"
            "}"
            "QMenu::separator {"
            "  height: 1px;"
            "  background: #e0e0e0;"
            "  margin: 2px 6px;"
            "}"
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(QColor(204, 204, 204), 1))
        painter.drawRoundedRect(
            self.rect().adjusted(0, 0, -1, -1),
            Theme.MENU_RADIUS, Theme.MENU_RADIUS,
        )
        super().paintEvent(event)
```

### component\search_engines.py (大小: 5670 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""搜索引擎存储：读写项目根目录下的 search_engines.json。

结构：
    {
        "engines": [
            {"abbr": "BI", "url": "https://www.bing.com/search?q=%s"},
            {"abbr": "GO", "url": "https://www.google.com/search?q=%s"},
            {"abbr": "BA", "url": "https://www.baidu.com/s?wd=%s"}
        ]
    }

* abbr：图标缩写（2 个大写字母），用户加的引擎自动从 url 主域生成
* url：含 %s 占位符的搜索 URL

首次访问时，若文件不存在，自动写入预置 3 个。
"""

import os
import re
import json
from urllib.parse import urlparse, quote_plus

import apppaths


STORE_PATH = os.path.join(apppaths.APP_DIR, "search_engines.json")


# ======================================================================
# 预置
# ======================================================================
DEFAULT_ENGINES = [
    {"abbr": "BI", "url": "https://www.bing.com/search?q=%s"},
    {"abbr": "GO", "url": "https://www.google.com/search?q=%s"},
    {"abbr": "BA", "url": "https://www.baidu.com/s?wd=%s"},
]


# ======================================================================
# 底层读写
# ======================================================================
def _load_raw():
    """读文件。不存在返回 None；损坏返回 None。"""
    if not os.path.isfile(STORE_PATH):
        return None
    try:
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return None


def _save_raw(data):
    try:
        with open(STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("[engines] 存失败:", e)


def _ensure_file():
    """确保文件存在。不存在就写预置。"""
    if os.path.isfile(STORE_PATH):
        return
    _save_raw({"engines": [dict(e) for e in DEFAULT_ENGINES]})


# ======================================================================
# 对外接口
# ======================================================================
def load_all():
    """读全部引擎。返回 list[dict]，每项 {"abbr", "url"}。"""
    _ensure_file()
    data = _load_raw()
    if not isinstance(data, dict):
        return [dict(e) for e in DEFAULT_ENGINES]

    engines = data.get("engines")
    if not isinstance(engines, list):
        return [dict(e) for e in DEFAULT_ENGINES]

    out = []
    for it in engines:
        if not isinstance(it, dict):
            continue
        url = it.get("url", "")
        abbr = it.get("abbr", "") or _abbr_from_url(url)
        if not url or "%s" not in url:
            continue
        out.append({"abbr": abbr, "url": url})
    return out


def add_engine(url):
    """新增一个引擎。url 必须含 %s 且 http(s)。成功返回 abbr，失败返回 None。"""
    url = (url or "").strip()
    if not url:
        return None
    if "%s" not in url:
        return None
    if not url.startswith(("http://", "https://")):
        return None

    _ensure_file()
    data = _load_raw()
    if not isinstance(data, dict):
        data = {"engines": []}
    engines = data.get("engines")
    if not isinstance(engines, list):
        engines = []

    # 同 url 已存在 → 直接返回
    for it in engines:
        if isinstance(it, dict) and it.get("url") == url:
            return it.get("abbr") or _abbr_from_url(url)

    abbr = _abbr_from_url(url)
    engines.append({"abbr": abbr, "url": url})
    data["engines"] = engines
    _save_raw(data)
    return abbr


def remove_engine(url):
    """按 url 删除。成功返回 True。"""
    url = (url or "").strip()
    if not url:
        return False
    _ensure_file()
    data = _load_raw()
    if not isinstance(data, dict):
        return False
    engines = data.get("engines")
    if not isinstance(engines, list):
        return False

    new_list = []
    removed = False
    for it in engines:
        if isinstance(it, dict) and it.get("url") == url:
            removed = True
            continue
        new_list.append(it)

    if not removed:
        return False
    data["engines"] = new_list
    _save_raw(data)
    return True


def build_search_url(engine, query):
    """把 query 拼成搜索 URL。engine 是 dict；query 是用户输入。"""
    if not engine or not isinstance(engine, dict):
        return ""
    tpl = engine.get("url", "")
    if not tpl or "%s" not in tpl:
        return ""
    q = quote_plus(query or "")
    try:
        return tpl % q
    except Exception:
        return ""


# ======================================================================
# 缩写生成
# ======================================================================
def _abbr_from_url(url):
    """从 URL 的主域取前两字母，大写。失败返回 '??'。"""
    try:
        host = (urlparse(url).hostname or "").lower()
        if not host:
            return "??"
        if host.startswith("www."):
            host = host[4:]
        parts = host.split(".")
        if len(parts) >= 2:
            label = parts[-2]
        else:
            label = host
        label = re.sub(r"[^a-zA-Z]", "", label)
        if not label:
            return "??"
        if len(label) == 1:
            return label.upper()
        return label[:2].upper()
    except Exception:
        return "??"
```

### component\search_icons.py (大小: 5900 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""搜索引擎图标存储：把 favicon 抓到 userdata/search_icons/<主域>.png。

* 读：load_icon(engine) → QPixmap 或 None
* 抓：fetch_icon(engine_url, callback) → 异步抓，抓到存盘
* 抓取源：https://<主域>/favicon.ico

抓到 ≤64 原图存；>64 缩到 64。
"""

import os
import re
from urllib.parse import urlparse

from loader import *

import apppaths

ICON_DIR = os.path.join(apppaths.APP_DIR, "userdata", "search_icons")

MAX_SIZE = 64
_ILLEGAL = r'[\\/:*?"<>|]'


def _ensure_dir():
    os.makedirs(ICON_DIR, exist_ok=True)


def _root_host(url):
    """从 URL 取主域，如 bing.com。"""
    try:
        host = (urlparse(url).hostname or "").lower()
        if not host:
            return ""
        if host.startswith("www."):
            host = host[4:]
        parts = host.split(".")
        if len(parts) <= 2:
            return host
        return ".".join(parts[-2:])
    except Exception:
        return ""


def _host_of_engine(engine):
    if not isinstance(engine, dict):
        return ""
    return _root_host(engine.get("url", ""))


def _safe_name(host):
    if not host:
        return "_"
    s = re.sub(_ILLEGAL, "_", host)
    return s.strip().strip(".") or "_"


def _icon_path(host):
    return os.path.join(ICON_DIR, _safe_name(host) + ".png")


# ======================================================================
# 读
# ======================================================================
def load_icon(engine):
    """读本地图标。返回 QPixmap 或 None。"""
    host = _host_of_engine(engine)
    if not host:
        return None
    path = _icon_path(host)
    if not os.path.isfile(path):
        return None
    pm = QPixmap(path)
    if pm.isNull():
        return None
    return pm


# ======================================================================
# 写
# ======================================================================
def save_icon(engine, pixmap):
    """把 pixmap 存盘。超过 64 缩到 64。返回是否成功。"""
    host = _host_of_engine(engine)
    if not host or pixmap is None or pixmap.isNull():
        return False

    _ensure_dir()

    w = pixmap.width()
    h = pixmap.height()
    if max(w, h) > MAX_SIZE:
        pixmap = pixmap.scaled(
            MAX_SIZE, MAX_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    try:
        return bool(pixmap.save(_icon_path(host), "PNG"))
    except Exception as e:
        print("[engine_icon] 存盘失败:", e)
        return False


# ======================================================================
# 抓
# ======================================================================
_nam = None


def _get_nam(parent=None):
    global _nam
    if _nam is None:
        from PyQt6.QtNetwork import QNetworkAccessManager
        _nam = QNetworkAccessManager(parent)
    return _nam


def fetch_icon(engine, callback=None, parent=None):
    """异步抓 favicon。

    * engine：dict {"abbr", "url"}
    * callback：抓到后回调 callback(engine, pixmap_or_None)
                pixmap 为 None 表示失败
    * parent：QNetworkAccessManager 的 parent（一般是窗口）
    """
    host = _host_of_engine(engine)
    if not host:
        if callback:
            try:
                callback(engine, None)
            except Exception:
                pass
        return

    # 本地已有 → 直接回调
    pm = load_icon(engine)
    if pm is not None and not pm.isNull():
        if callback:
            try:
                callback(engine, pm)
            except Exception:
                pass
        return

    scheme = "https"
    try:
        p = urlparse(engine.get("url", ""))
        if p.scheme:
            scheme = p.scheme
    except Exception:
        pass

    fav_url = f"{scheme}://{host}/favicon.ico"

    from PyQt6.QtNetwork import QNetworkRequest
    nam = _get_nam(parent)
    reply = nam.get(QNetworkRequest(QUrl(fav_url)))

    def _done():
        try:
            data = bytes(reply.readAll())
            pm = QPixmap()
            pm.loadFromData(data)
            if pm.isNull():
                if callback:
                    try:
                        callback(engine, None)
                    except Exception:
                        pass
                return

            # 存盘
            save_icon(engine, pm)

            # 重新读盘，确保拿到的是缩放后的版本
            pm2 = load_icon(engine) or pm
            if callback:
                try:
                    callback(engine, pm2)
                except Exception:
                    pass
        except Exception as e:
            print("[engine_icon] 抓取回调异常:", e)
            if callback:
                try:
                    callback(engine, None)
                except Exception:
                    pass
        finally:
            reply.deleteLater()

    reply.finished.connect(_done)


def fetch_all(engines, on_one=None, parent=None):
    """批量抓。每个抓完调 on_one(engine, pixmap_or_None)。

    串行（前一个抓完再抓下一个），避免同时开太多连接。
    """
    items = list(engines or [])

    def _next(idx):
        if idx >= len(items):
            return
        eng = items[idx]

        def _cb(e, pm):
            if on_one:
                try:
                    on_one(e, pm)
                except Exception:
                    pass
            # 延迟 50ms 再抓下一个
            QTimer.singleShot(50, lambda: _next(idx + 1))

        fetch_icon(eng, _cb, parent)

    _next(0)
```

### component\settings.py (大小: 6934 | 修改时间: 2026-10-03 12:50:10 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""读写用户设置：按窗口类型区分配置。

配置结构：
{
    "windows": {
        "default": {
            "theme_color": "#d0d0d0",
            "background_images": [],
            "background_current": ""
        },
        "custom_1": { ... }
    }
}

窗口类型 mode：
    "default"  默认窗口，读写 windows.default
    "search"   搜索引擎窗口，只读 windows.default，不写
    "custom"   个性需求窗口，读写 windows.<id>
"""

import os
import json
from PyQt6.QtGui import QColor

import apppaths


SETTINGS_PATH = os.path.join(apppaths.APP_DIR, "settings.json")

DEFAULT_THEME = "#d0d0d0"

#: 内置资源的路径前缀。
#: 随包发布的背景图用这个占位符引用，例如
#:     "{RES}/assets/backgrounds/spaceship.jpg"
#: 运行时展开成 RES_DIR（源码模式=项目根，打包后=_internal）。
#: 这样 settings.json 里就不必写死绝对路径，换机器 / 换安装位置都不会失效。
RES_TOKEN = "{RES}"


def resolve_path(path):
    """把设置里的路径展开成可用路径。

    * ``{RES}/xxx``  ->  ``<RES_DIR>/xxx``（内置资源，随程序走）
    * 其它           ->  原样返回（用户自己选的绝对路径）
    """
    if not path:
        return ""
    p = str(path)
    if p.startswith(RES_TOKEN):
        rest = p[len(RES_TOKEN):].lstrip("/\\")
        return os.path.join(apppaths.RES_DIR, *rest.split("/"))
    return p


def to_stored_path(path):
    """写回设置时尽量用 ``{RES}`` 记内置资源，避免存绝对路径。"""
    if not path:
        return ""
    try:
        res = os.path.abspath(apppaths.RES_DIR)
        ap = os.path.abspath(str(path))
        if os.path.commonpath([res, ap]) == res:
            rel = os.path.relpath(ap, res).replace("\\", "/")
            return RES_TOKEN + "/" + rel
    except Exception:
        pass
    return str(path)


# ======================================================================
# 底层读写
# ======================================================================
def _default_window_data():
    return {
        "theme_color": DEFAULT_THEME,
        "background_images": [],
        "background_current": "",
    }


def _load_all():
    data = {"windows": {"default": _default_window_data()}}
    try:
        if os.path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                if "windows" in loaded and isinstance(loaded["windows"], dict):
                    data["windows"].update(loaded["windows"])
                else:
                    # 兼容旧版全局配置：把旧字段迁移到 windows.default
                    old = {}
                    for k in ("theme_color", "background_images",
                              "background_current"):
                        if k in loaded:
                            old[k] = loaded[k]
                    old_img = loaded.get("background_image")
                    if old_img and old_img not in old.get("background_images", []):
                        old.setdefault("background_images", []).insert(0, old_img)
                    if old:
                        data["windows"]["default"].update(old)
    except Exception:
        pass

    # 补全 default
    if "default" not in data["windows"]:
        data["windows"]["default"] = _default_window_data()
    else:
        base = _default_window_data()
        base.update(data["windows"]["default"])
        data["windows"]["default"] = base

    # 过滤失效图片路径。
    # 注意：先展开 {RES} 占位符再判断存在性 —— 否则内置背景图会被当成
    # "不存在的路径"直接过滤掉（这正是之前默认背景图丢失的原因之一）。
    for wid, w in data["windows"].items():
        imgs = [p for p in w.get("background_images", [])
                if p and os.path.isfile(resolve_path(p))]
        w["background_images"] = imgs
        cur = w.get("background_current", "")
        if cur and cur not in imgs:
            cur = imgs[0] if imgs else ""
        w["background_current"] = cur

    return data


def _save_all(data):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# ======================================================================
# 按窗口读写
# ======================================================================
def _resolve_key(mode, window_id):
    """把 mode + id 映射到 windows 下的 key。"""
    if mode == "default":
        return "default"
    if mode == "search":
        return "default"      # 只读 default
    if mode == "custom":
        return window_id or "default"
    return "default"


def load_window_settings(mode="default", window_id=None):
    """读某个窗口的配置。"""
    key = _resolve_key(mode, window_id)
    data = _load_all()
    w = data["windows"].get(key)
    if w is None:
        # custom 首次启动：复制 default 作为初始
        w = dict(_default_window_data())
        w.update(data["windows"]["default"])
        data["windows"][key] = w
        if mode == "custom":
            _save_all(data)
    return dict(w)


def save_window_settings(mode, window_id, settings):
    """写某个窗口的配置。search 模式不写。"""
    if mode == "search":
        return
    key = _resolve_key(mode, window_id)
    data = _load_all()
    data["windows"][key] = dict(settings)
    _save_all(data)


# ======================================================================
# 兼容旧接口：直接操作 default 窗口
# ======================================================================
def load_theme_color():
    s = load_window_settings("default", "default")
    color = QColor(s.get("theme_color", DEFAULT_THEME))
    if not color.isValid():
        color = QColor(DEFAULT_THEME)
    return color


def save_theme_color(color):
    s = load_window_settings("default", "default")
    s["theme_color"] = QColor(color).name()
    save_window_settings("default", "default", s)


def load_background_image():
    s = load_window_settings("default", "default")
    return s.get("background_current", "")


def load_background_images():
    s = load_window_settings("default", "default")
    return list(s.get("background_images", []))


def save_background_image(path, images=None):
    s = load_window_settings("default", "default")
    if images is not None:
        s["background_images"] = list(images)
    s["background_current"] = path or ""
    save_window_settings("default", "default", s)
```

### component\settings_app.py (大小: 2739 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""设置进程：独立窗口，不依附任何浏览器窗口。

托盘启动它，窗口进程通过托盘转达"打开设置"的请求。
收到 MSG_SETTINGS_SHOW 就显示窗口。
收到 MSG_LANGUAGE_CHANGED 就切换语言并刷新 UI。

启动时读语言，UI 文字从 i18n.t() 取。
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths
from i18n import t
from ipc import (
    IpcServer,
    CHANNEL_SETTINGS, ROLE_SETTINGS,
    MSG_SETTINGS_SHOW, MSG_QUIT, MSG_LANGUAGE_CHANGED,
)
from i18n import load
from settings_backend import SettingsBackend


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 任务栏：本进程独立 AppUserModelID
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "MyBrowser.Settings"
        )
    except Exception as e:
        print("[settings] 设置 AppUserModelID 失败:", e)

    # 图标
    _icon_path = os.path.join(
        apppaths.RES_DIR, "data", "settings_icon.ico"
    )
    _icon = QIcon(_icon_path) if os.path.isfile(_icon_path) else QIcon()
    if not _icon.isNull():
        app.setWindowIcon(_icon)
    else:
        print(f"[settings] 图标加载失败或不存在: {_icon_path}")

    # 读语言：必须在创建 SettingsWindow 之前
    try:
        load(SettingsBackend().get_language())
    except Exception as e:
        print("[settings] 加载语言失败:", e)

    from settings_window import SettingsWindow

    win = SettingsWindow()

    # 窗口图标
    if not _icon.isNull():
        win.setWindowIcon(_icon)

    backend = SettingsBackend()
    win.set_backend(backend)

    def on_message(msg_type, payload):
        if msg_type == MSG_SETTINGS_SHOW:
            win.show()
            win.raise_()
            win.activateWindow()
        elif msg_type == MSG_LANGUAGE_CHANGED:
            try:
                code = payload.decode("utf-8")
                load(code)
                if hasattr(win, "_refresh_texts"):
                    win._refresh_texts()
            except Exception as e:
                print("[settings] 切换语言失败:", e)
        elif msg_type == MSG_QUIT:
            app.quit()

    server = IpcServer(
        CHANNEL_SETTINGS, on_message, role=ROLE_SETTINGS
    )
    if not server.start():
        print("[settings] 已有实例在运行，退出")
        sys.exit(0)

    # 启动时不显示窗口，等托盘或窗口来消息
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

### component\settings_backend.py (大小: 11600 | 修改时间: 2026-10-03 04:54:30 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""设置后端接口。

读写 settings.json。
分两部分：
  * windows.*：每个窗口的主题、背景等（已存在）
  * env.*：环境级设置（WebView2 重建才生效）

env 段结构：
    {
        "language": "zh-CN",
        "user_agent": "",
        "proxy": "",
        "incognito": false,
        "user_data_folder": "",
        "download_dir": "",
        "download_notify": false,
        "scan_downloads": true,
        "js_enabled": true,
        "context_menu": false,
        "hotkeys": false,
        "devtools": false,
        "autofill": false,
        "password_autosave": false,
        "tracking_prevention": true,
        "tracking_level": 1,
        "smartscreen": true,
        "block_third_party_cookies": false,
        "insecure_content_allowed": false,
        "permission_camera": 0,
        "permission_mic": 0,
        "permission_geo": 0,
        "permission_notify": 0,
        "block_redirect": false,
        "block_popup": true,
        "block_ad": false,
        "save_cookie": true,
        "save_history": true,
        "history_days": 30,
        "whitelist": []
    }
"""

import os
import json

import apppaths


SETTINGS_PATH = os.path.join(apppaths.APP_DIR, "settings.json")


_DEFAULT_ENV = {
    "language": "zh-CN",
    "user_agent": "",
    "proxy": "",
    "incognito": False,
    "user_data_folder": "",
    "download_dir": "",
    "download_notify": False,
    "scan_downloads": True,
    "js_enabled": True,
    "context_menu": False,
    "hotkeys": False,
    "devtools": False,
    "autofill": False,
    "password_autosave": False,
    "tracking_prevention": True,
    "tracking_level": 1,
    "smartscreen": True,
    "block_third_party_cookies": False,
    "insecure_content_allowed": False,
    "permission_camera": 0,
    "permission_mic": 0,
    "permission_geo": 0,
    "permission_notify": 0,
    "block_redirect": False,
    "block_popup": True,
    "block_ad": False,
    "save_cookie": True,
    "save_history": True,
    "history_days": 30,
    "whitelist": [],
}


def _load_all():
    try:
        if os.path.isfile(SETTINGS_PATH):
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return {}


def _save_all(data):
    try:
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _load_env():
    data = _load_all()
    env = data.get("env", {})
    if not isinstance(env, dict):
        env = {}
    out = dict(_DEFAULT_ENV)
    out.update(env)
    return out


def _save_env(env):
    data = _load_all()
    data["env"] = env
    _save_all(data)


class SettingsBackend:
    def __init__(self, web_view=None):
        self._web_view = web_view

    # ---------------- 语言 ----------------
    def get_language(self):
        return str(_load_env().get("language", "zh-CN"))

    def set_language(self, code):
        if not code:
            return
        env = _load_env()
        env["language"] = str(code)
        _save_env(env)

    # ---------------- 常规 ----------------
    def get_js_enabled(self):
        return bool(_load_env().get("js_enabled", True))

    def set_js_enabled(self, on):
        env = _load_env()
        env["js_enabled"] = bool(on)
        _save_env(env)

    def get_context_menu_enabled(self):
        return bool(_load_env().get("context_menu", False))

    def set_context_menu_enabled(self, on):
        env = _load_env()
        env["context_menu"] = bool(on)
        _save_env(env)

    def get_hotkeys_enabled(self):
        return bool(_load_env().get("hotkeys", False))

    def set_hotkeys_enabled(self, on):
        env = _load_env()
        env["hotkeys"] = bool(on)
        _save_env(env)

    def get_devtools_enabled(self):
        return bool(_load_env().get("devtools", False))

    def set_devtools_enabled(self, on):
        env = _load_env()
        env["devtools"] = bool(on)
        _save_env(env)

    def get_autofill_enabled(self):
        return bool(_load_env().get("autofill", False))

    def set_autofill_enabled(self, on):
        env = _load_env()
        env["autofill"] = bool(on)
        _save_env(env)

    def get_password_autosave_enabled(self):
        return bool(_load_env().get("password_autosave", False))

    def set_password_autosave_enabled(self, on):
        env = _load_env()
        env["password_autosave"] = bool(on)
        _save_env(env)

    # ---------------- 隐私 ----------------
    def get_tracking_prevention(self):
        return bool(_load_env().get("tracking_prevention", True))

    def set_tracking_prevention(self, on):
        env = _load_env()
        env["tracking_prevention"] = bool(on)
        _save_env(env)

    def get_tracking_level(self):
        return int(_load_env().get("tracking_level", 1))

    def set_tracking_level(self, level):
        env = _load_env()
        env["tracking_level"] = int(level)
        _save_env(env)

    def get_smartscreen(self):
        return bool(_load_env().get("smartscreen", True))

    def set_smartscreen(self, on):
        env = _load_env()
        env["smartscreen"] = bool(on)
        _save_env(env)

    def get_block_third_party_cookies(self):
        return bool(_load_env().get("block_third_party_cookies", False))

    def set_block_third_party_cookies(self, on):
        env = _load_env()
        env["block_third_party_cookies"] = bool(on)
        _save_env(env)

    def get_user_agent(self):
        return str(_load_env().get("user_agent", ""))

    def set_user_agent(self, ua):
        env = _load_env()
        env["user_agent"] = str(ua)
        _save_env(env)

    def get_block_redirect(self):
        return bool(_load_env().get("block_redirect", False))

    def set_block_redirect(self, on):
        env = _load_env()
        env["block_redirect"] = bool(on)
        _save_env(env)

    def get_block_popup(self):
        return bool(_load_env().get("block_popup", True))

    def set_block_popup(self, on):
        env = _load_env()
        env["block_popup"] = bool(on)
        _save_env(env)

    def get_block_ad(self):
        return bool(_load_env().get("block_ad", False))

    def set_block_ad(self, on):
        env = _load_env()
        env["block_ad"] = bool(on)
        _save_env(env)

    # ---------------- 安全 ----------------
    def get_scan_downloads(self):
        return bool(_load_env().get("scan_downloads", True))

    def set_scan_downloads(self, on):
        env = _load_env()
        env["scan_downloads"] = bool(on)
        _save_env(env)

    def get_permission(self, kind):
        env = _load_env()
        key = f"permission_{kind}"
        return int(env.get(key, 0))

    def set_permission(self, kind, value):
        env = _load_env()
        key = f"permission_{kind}"
        env[key] = int(value)
        _save_env(env)

    def get_insecure_content_allowed(self):
        return bool(_load_env().get("insecure_content_allowed", False))

    def set_insecure_content_allowed(self, on):
        env = _load_env()
        env["insecure_content_allowed"] = bool(on)
        _save_env(env)

    # ---------------- 历史 ----------------
    def get_save_cookie(self):
        return bool(_load_env().get("save_cookie", True))

    def set_save_cookie(self, on):
        env = _load_env()
        env["save_cookie"] = bool(on)
        _save_env(env)

    def get_save_history(self):
        return bool(_load_env().get("save_history", True))

    def set_save_history(self, on):
        env = _load_env()
        env["save_history"] = bool(on)
        _save_env(env)

    def get_history_days(self):
        return int(_load_env().get("history_days", 30))

    def set_history_days(self, days):
        env = _load_env()
        env["history_days"] = int(days)
        _save_env(env)

    def get_whitelist(self):
        wl = _load_env().get("whitelist", [])
        if not isinstance(wl, list):
            return []
        return wl

    def set_whitelist(self, wl):
        env = _load_env()
        env["whitelist"] = list(wl or [])
        _save_env(env)

    # ---------------- 下载 ----------------
    def get_download_dir(self):
        return str(_load_env().get("download_dir", ""))

    def set_download_dir(self, path):
        env = _load_env()
        env["download_dir"] = str(path)
        _save_env(env)

    def get_download_notify(self):
        return bool(_load_env().get("download_notify", False))

    def set_download_notify(self, on):
        env = _load_env()
        env["download_notify"] = bool(on)
        _save_env(env)

    # ---------------- 环境级 ----------------
    def get_incognito(self):
        return bool(_load_env().get("incognito", False))

    def set_incognito(self, on):
        env = _load_env()
        env["incognito"] = bool(on)
        _save_env(env)

    def get_proxy(self):
        return str(_load_env().get("proxy", ""))

    def set_proxy(self, proxy):
        env = _load_env()
        env["proxy"] = str(proxy)
        _save_env(env)

    def get_user_data_folder(self, window_id=None):
        """返回 WebView2 的用户数据目录。

        **所有普通窗口共用同一份 profile**（userdata/profile）。

        为什么不再按窗口 id 分目录（原实现是 userdata/df-0、df-1、df-2…）：
            profile 决定 Cookie / localStorage / 登录态。按窗口 id 分目录时，
            同一个站点在不同窗口里就是互不相干的会话 —— 固定项点开的窗口
            每次拿到新的 id（df-3、df-4…），等于每次都开一份全新的空 profile，
            表现为"关掉窗口再打开就要重新登录"（deepseek、bilibili 都会这样）。

            浏览器的正常语义是 Cookie 跟着**站点**走、不跟窗口走，所以改成共用一份。

        无痕的隔离不靠这里：incognito_window.py 根本不传 user_data_folder。

        window_id 参数保留只为兼容调用方，不再参与路径计算。
        """
        base = str(_load_env().get("user_data_folder", ""))
        if not base:
            base = os.path.join(apppaths.APP_DIR, "userdata")

        base = os.path.join(base, "profile")

        try:
            os.makedirs(base, exist_ok=True)
        except Exception:
            pass
        return base

    def set_user_data_folder(self, path):
        env = _load_env()
        env["user_data_folder"] = str(path)
        _save_env(env)

    def get_global_user_agent(self):
        return self.get_user_agent()

    def set_global_user_agent(self, ua):
        self.set_user_agent(ua)

    def restart_environment(self):
        pass

    # ---------------- 外观 ----------------
    def get_theme_color(self):
        return "#d0d0d0"

    def set_theme_color(self, color):
        pass

    def get_background_image(self):
        return ""

    def set_background_image(self, path):
        pass

    def get_radius(self):
        return 12

    def set_radius(self, r):
        pass
```

### component\settings_pages.py (大小: 56776 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
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
```

### component\settings_window.py (大小: 7086 | 修改时间: 2026-09-29 20:41:58 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""设置窗口：左侧导航 + 右侧堆叠页。

UI 文字从 i18n.t() 取。启动时注册 _refresh_texts 到 i18n.on_change，
语言变化时自动刷新。
"""

import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
from i18n import t, on_change


# 导航项：(page_key, i18n_key)
NAV_ITEMS = [
    ("general",  "nav.general"),
    ("history",  "nav.history"),
    ("language", "nav.language"),
]


class NavList(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(160)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            "QListWidget {"
            "  background: #f5f5f5;"
            "  border: none;"
            "  outline: none;"
            "  padding: 8px 6px;"
            "  border-radius: 8px;"
            "}"
            "QListWidget::item {"
            "  height: 36px;"
            "  padding-left: 12px;"
            "  border-radius: 6px;"
            "  color: #333;"
            "  font-size: 13px;"
            "}"
            "QListWidget::item:hover {"
            "  background: #e8e8e8;"
            "}"
            "QListWidget::item:selected {"
            "  background: #e8f0fe;"
            "  color: #2f5fd0;"
            "}"
        )
        self.viewport().setStyleSheet("background: transparent;")
        for key, i18n_key in NAV_ITEMS:
            item = QListWidgetItem(t(i18n_key))
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.addItem(item)
        self.setCurrentRow(0)

    def _refresh_texts(self):
        for i, (key, i18n_key) in enumerate(NAV_ITEMS):
            if i < self.count():
                item = self.item(i)
                if item is not None:
                    item.setText(t(i18n_key))


class SettingsWindow(QWidget):

    RADIUS = 12
    WIDTH = 760
    HEIGHT = 560
    PAD = 20
    BORDER_COLOR = QColor(160, 160, 160)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start = None
        self._backend = None
        self._pages = {}
        self._on_change_cb = None

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
            | Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self._build_ui()
        self._center_on_parent()

        # 注册语言变化回调
        self._on_change_cb = self._refresh_texts
        try:
            on_change(self._on_change_cb)
        except Exception as e:
            print("[settings] 注册语言回调失败:", e)

    def set_backend(self, backend):
        self._backend = backend
        for page in self._pages.values():
            if hasattr(page, "set_backend"):
                page.set_backend(backend)

    def _build_ui(self):
        body = QHBoxLayout(self)
        body.setContentsMargins(self.PAD, self.PAD, self.PAD, self.PAD)
        body.setSpacing(8)

        self.nav = NavList(self)
        self.nav.currentRowChanged.connect(self._on_nav_changed)
        body.addWidget(self.nav)

        self.stack = QStackedWidget(self)
        self.stack.setStyleSheet(
            "QStackedWidget { background: transparent; }"
        )
        body.addWidget(self.stack, 1)

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
        self.close_btn.move(self.WIDTH - 28 - self.PAD, self.PAD)
        self.close_btn.raise_()

        from settings_pages import (
            GeneralPage, HistoryPage, LanguagePage,
        )
        page_classes = {
            "general": GeneralPage,
            "history": HistoryPage,
            "language": LanguagePage,
        }
        for key, _i18n in NAV_ITEMS:
            page_cls = page_classes[key]
            page = page_cls(self.stack)
            self._pages[key] = page
            self.stack.addWidget(page)

    def _on_nav_changed(self, row):
        if 0 <= row < self.stack.count():
            self.stack.setCurrentIndex(row)

    def _refresh_texts(self):
        """语言变化后刷新整个设置窗口的 UI 文字。"""
        print("[settings] _refresh_texts 被调用")
        try:
            self.nav._refresh_texts()
            print("[settings] 刷新导航成功")
        except Exception as e:
            print("[settings] 刷新导航失败:", e)

        for key, page in self._pages.items():
            if hasattr(page, "_refresh_texts"):
                try:
                    page._refresh_texts()
                    print(f"[settings] 刷新页面 {key} 成功")
                except Exception as e:
                    print(f"[settings] 刷新页面 {key} 失败:", e)

    def _center_on_parent(self):
        parent = self.parent()
        if parent is not None:
            pg = parent.geometry()
            self.move(
                pg.x() + (pg.width() - self.width()) // 2,
                pg.y() + (pg.height() - self.height()) // 2,
            )
            return

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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
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
```

### component\styles.py (大小: 12637 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""网页注入用的字体与滚动条 CSS / JS。

字体通过自定义协议 appfont:// 提供，由 font_scheme_handler 直接读磁盘返回。

跨导航 / SPA 动态 DOM / 内联样式覆盖 的处理：
  * 去重看 document.getElementById('__sb_style')，不用 window 标志；
  * 定时巡检：style 丢了重建；内联 font-family 出现就删掉；
  * CSS 规则不用 inherit，而是直接写完整字体栈 + 覆盖常见元素。

额外：
  * content-visibility 视窗外渲染跳过；
  * 视窗外 <img> 卸载 src，释放解码位图内存，滚回再恢复。
"""

import os

import apppaths

# ----------------------------------------------------------------------
# 路径 / 探测
# ----------------------------------------------------------------------
FONTS_DIR = os.path.join(apppaths.RES_DIR, "assets", "fonts")

FORCE_FILES = {
    400: None,
    500: None,
    700: None,
}

_EXTS = [".woff2", ".ttf", ".otf"]

_WEIGHT_KEYWORDS = {
    400: ["regular", "normal", "book", "400"],
    500: ["medium", "500"],
    700: ["bold", "700"],
}

_FMT_BY_EXT = {
    ".woff2": "woff2",
    ".ttf":   "truetype",
    ".otf":   "opentype",
}

SINGLE_WEIGHT_ONLY = False


def _list_font_files():
    if not os.path.isdir(FONTS_DIR):
        return []
    out = []
    for root, _dirs, files in os.walk(FONTS_DIR):
        for f in files:
            if f.startswith("."):
                continue
            if os.path.splitext(f)[1].lower() in _EXTS:
                out.append(os.path.join(root, f))
    return out


def _pick_file(weight):
    forced = FORCE_FILES.get(weight)
    if forced:
        path = os.path.join(FONTS_DIR, forced)
        if os.path.isfile(path):
            return path

    keywords = _WEIGHT_KEYWORDS[weight]
    candidates = []
    for path in _list_font_files():
        name = os.path.basename(path).lower()
        if "italic" in name or "oblique" in name:
            continue
        for idx, kw in enumerate(keywords):
            if kw in name:
                candidates.append((idx, path))
                break

    if not candidates:
        return None

    def sort_key(item):
        kw_idx, path = item
        ext = os.path.splitext(path)[1].lower()
        ext_rank = _EXTS.index(ext) if ext in _EXTS else 99
        return (kw_idx, ext_rank)

    candidates.sort(key=sort_key)
    return candidates[0][1]


def _font_face(family, weight):
    path = _pick_file(weight)
    if not path:
        print(f"[styles] weight={weight} 未找到字体文件")
        return ""

    name = os.path.basename(path)
    ext = os.path.splitext(name)[1].lower()
    fmt = _FMT_BY_EXT.get(ext, "truetype")
    url = "appfont:///" + name
    return (
        f"@font-face {{ font-family: '{family}'; "
        f"src: url('{url}') format('{fmt}'); "
        f"font-weight: {weight}; font-display: swap; }}"
    )


# ----------------------------------------------------------------------
# 字体 CSS
# ----------------------------------------------------------------------
def _build_font_css():
    family = "MiSans"

    if SINGLE_WEIGHT_ONLY:
        faces = _font_face(family, 400)
    else:
        faces = (
            _font_face(family, 400)
            + _font_face(family, 500)
            + _font_face(family, 700)
        )

    stack = (
        f"'{family}', -apple-system, 'Segoe UI', "
        f"'Microsoft YaHei', 'PingFang SC', sans-serif"
    )

    return f"""
{faces}
html, body {{
    font-family: {stack} !important;
}}

body, body *,
h1, h2, h3, h4, h5, h6,
p, span, a, li, ul, ol, dl, dt, dd,
div, section, article, aside, header, footer, nav, main,
td, th, table, tr, tbody, thead,
blockquote, pre, figure, figcaption,
label, input, textarea, select, button, optgroup, option,
[contenteditable], [contenteditable="true"] {{
    font-family: {stack} !important;
}}

i, em, svg, canvas,
[class*="icon"], [class*="Icon"],
[class*="fa-"], [class*="fa_"],
[class*="material"], [class*="Material"] {{
    font-family: revert !important;
}}
"""


FONT_CSS = _build_font_css()


# ----------------------------------------------------------------------
# 滚动条样式
# ----------------------------------------------------------------------
SCROLLBAR_CSS = """
::-webkit-scrollbar,
*::-webkit-scrollbar {
    width: 8px !important;
    height: 8px !important;
    background: transparent !important;
}
::-webkit-scrollbar-track,
*::-webkit-scrollbar-track {
    background: transparent !important;
    margin: 12px !important;
}
::-webkit-scrollbar-track-piece,
*::-webkit-scrollbar-track-piece {
    background: transparent !important;
    margin: 12px !important;
}
::-webkit-scrollbar-thumb,
*::-webkit-scrollbar-thumb {
    background: rgba(120, 120, 120, 0.04) !important;
    border-radius: 4px !important;
    border: none !important;
}
::-webkit-scrollbar-corner,
*::-webkit-scrollbar-corner {
    background: transparent !important;
}
::-webkit-scrollbar-button,
*::-webkit-scrollbar-button {
    display: none !important;
    background: transparent !important;
}
html.sb-hover::-webkit-scrollbar-thumb,
html.sb-hover *::-webkit-scrollbar-thumb {
    background: rgba(120, 120, 120, 0.75) !important;
}
"""


# ----------------------------------------------------------------------
# 渲染优化：视窗外元素跳过渲染
# ----------------------------------------------------------------------
RENDER_CSS = """
img, video, iframe, picture {
    content-visibility: auto;
    contain-intrinsic-size: 0 200px;
}
"""


# ----------------------------------------------------------------------
# 巡检 + 内联样式清理 + 滚动条 hover + 视窗外图片卸载
# ----------------------------------------------------------------------
MAINTENANCE_JS = """
(function() {
    // ================================================================
    // 样式巡检
    // ================================================================
    function ensureStyle() {
        var el = document.getElementById('__sb_style');
        if (el) return;
        var style = document.createElement('style');
        style.id = '__sb_style';
        style.type = 'text/css';
        style.appendChild(document.createTextNode(window.__sb_css || ''));
        (document.head || document.documentElement).appendChild(style);
    }

    function stripInlineFontFamily() {
        var nodes = document.querySelectorAll('[style*="font-family"]');
        for (var i = 0; i < nodes.length; i++) {
            var el = nodes[i];
            if (el.style && el.style.fontFamily) {
                el.style.removeProperty('font-family');
            }
        }
    }

    // ================================================================
    // 视窗外图片卸载 / 恢复
    // ================================================================
    var SB_PLACEHOLDER = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
    var SB_BUFFER = 800;      // 视窗上下各 800px 内不卸载
    var SB_MIN_SIZE = 4096;   // 小于 4KB 的图（图标等）不卸载

    // 记录每个 img 的原始属性，恢复时用
    function sbUnload(img) {
        if (img.dataset.sbOrig) return;           // 已卸载
        if (!img.src || img.src === SB_PLACEHOLDER) return;
        if (img.src.indexOf('data:') === 0) return;  // 本身是 data URI

        // 小图不卸载（图标、头像等）
        var w = img.naturalWidth || img.width || 0;
        var h = img.naturalHeight || img.height || 0;
        if (w > 0 && h > 0 && w * h < SB_MIN_SIZE) return;

        img.dataset.sbOrig = img.src;

        // 摘掉 B 站的 onload / onerror，避免占位图触发它的逻辑
        var ol = img.getAttribute('onload');
        var oe = img.getAttribute('onerror');
        if (ol !== null) img.dataset.sbOnload = ol;
        if (oe !== null) img.dataset.sbOnerror = oe;
        img.removeAttribute('onload');
        img.removeAttribute('onerror');

        img.src = SB_PLACEHOLDER;
    }

    function sbRestore(img) {
        if (!img.dataset.sbOrig) return;
        img.src = img.dataset.sbOrig;
        delete img.dataset.sbOrig;

        // 挂回 onload / onerror
        if (img.dataset.sbOnload !== undefined) {
            img.setAttribute('onload', img.dataset.sbOnload);
            delete img.dataset.sbOnload;
        }
        if (img.dataset.sbOnerror !== undefined) {
            img.setAttribute('onerror', img.dataset.sbOnerror);
            delete img.dataset.sbOnerror;
        }
    }

    function sbProcessImages() {
        var imgs = document.getElementsByTagName('img');
        var vh = window.innerHeight || document.documentElement.clientHeight;
        for (var i = 0; i < imgs.length; i++) {
            var img = imgs[i];

            // 跳过视频封面之外的特殊 img（如弹幕、图标）
            // 这里只按尺寸判断，尺寸太小就不动

            var rect = img.getBoundingClientRect();
            var top = rect.top;
            var bottom = rect.bottom;

            var inWindow = (bottom > -SB_BUFFER) && (top < vh + SB_BUFFER);

            if (inWindow) {
                sbRestore(img);
            } else {
                sbUnload(img);
            }
        }
    }

    var sbPending = false;
    function sbOnScroll() {
        if (sbPending) return;
        sbPending = true;
        requestAnimationFrame(function() {
            sbProcessImages();
            sbPending = false;
        });
    }

    // ================================================================
    // 安装
    // ================================================================
    if (!window.__sbMonitorInstalled) {
        window.__sbMonitorInstalled = true;

        var SB_W = 14, hovering = false, pending = false;

        function setHover(on) {
            if (on === hovering) return;
            hovering = on;
            if (on) document.documentElement.classList.add('sb-hover');
            else    document.documentElement.classList.remove('sb-hover');
        }

        document.addEventListener('mousemove', function(e) {
            if (pending) return;
            pending = true;
            requestAnimationFrame(function() {
                var nearRight = (window.innerWidth - e.clientX) <= SB_W;
                var nearBottom = (window.innerHeight - e.clientY) <= SB_W;
                setHover(nearRight || nearBottom);
                pending = false;
            });
        }, { passive: true });

        document.addEventListener('mouseleave', function() { setHover(false); });
        window.addEventListener('blur', function() { setHover(false); });

        // 样式巡检
        setInterval(function() {
            var el = document.getElementById('__sb_style');
            if (!el) {
                ensureStyle();
                return;
            }
            var head = document.head || document.documentElement;
            if (head.lastElementChild !== el) head.appendChild(el);
        }, 3000);

        setInterval(stripInlineFontFamily, 3000);

        // 图片卸载：滚动 + 定时
        window.addEventListener('scroll', sbOnScroll, { passive: true });
        setInterval(sbProcessImages, 1000);

        try {
            var mo = new MutationObserver(function() {
                if (!document.getElementById('__sb_style')) ensureStyle();
            });
            mo.observe(document.documentElement, { childList: true, subtree: true });
        } catch (e) {}
    }

    ensureStyle();
    stripInlineFontFamily();
    sbProcessImages();
})();
"""


# ----------------------------------------------------------------------
# 注入源（缓存）
# ----------------------------------------------------------------------
_INJECTED_SOURCE = None


def build_injected_source():
    global _INJECTED_SOURCE
    if _INJECTED_SOURCE is not None:
        return _INJECTED_SOURCE

    css = SCROLLBAR_CSS + RENDER_CSS + FONT_CSS
    _INJECTED_SOURCE = (
        "(function(){\n"
        "window.__sb_css = " + repr(css) + ";\n"
        + MAINTENANCE_JS +
        "})();\n"
    )
    print(f"[styles] injected source: {len(_INJECTED_SOURCE)//1024} KB")
    return _INJECTED_SOURCE
```

### component\theme.py (大小: 2109 | 修改时间: 2026-09-23 18:24:49 | 权限: 666)

```
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
```

### component\title_bar.py (大小: 27198 | 修改时间: 2026-10-02 18:06:55 | 权限: 666)

```
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
```

### component\window.py (大小: 107331 | 修改时间: 2026-10-03 12:51:58 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""窗口进程（人 + 内核）：窗口外观 + 渲染 + 输入 + host 路由。

TitleBar 嵌在主窗口顶部。无 tabbar。
web_view 内缩一圈，外层描边 + 内层背景 + web_view 三层视觉。
web_view 裁圆角，定时兜底防止 WebView2 内部重绘重置。

pwindow：
  * 每个 window 唯一一个 pwindow（PopupWindow 组件）。
  * pwindow 是顶层窗口，点它会让 window 收到 WindowDeactivate。
  * "pwindow 被选中" 等同于 "window 被选中"，靠 is_effectively_active() 判断。

popup = URL 历史列表：
  * 不是 tab 管理器。
  * 只记录本窗口 host（含同主域）的 URL。
  * 每个新 URL → 底部追加一行，重复 URL 跳过去不追加。
  * 点击行 → 当前 web_view 加载。
  * 点行 × → 从列表里删。
  * < / > → 在列表里上下移动，并加载。
  * 关窗口清空（会话内保留）。

跨域：
  * 同主域点击 / 地址栏同主域 → 当前 web_view 加载。
  * 不同主域点击 / 地址栏跨域 → 联系 bar（bar 查窗口 / 起新窗口）。
  * 当前 web_view 不会跳去跨域。
"""

import sys
import os
import json
import time
import argparse
import ctypes
from ctypes import wintypes
from urllib.parse import urlparse, unquote, urlunparse
from window_icon import (
    default_icon,
    icon_for_window,
    apply_icon_to_window,
)

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from loader import *
import apppaths

from theme import Theme
from corner_mask import CornerMask
from title_bar import TitleBar
from input_box import InputBox
from settings import load_window_settings, save_window_settings
from settings import resolve_path, to_stored_path
from activity_watcher import ActivityWatcher
from popup_window import PopupWindow
from ipc import (
    IpcServer, IpcClient,
    window_channel, window_role,
    CHANNEL_BAR, CHANNEL_BROADCAST,
    MSG_NAVIGATE, MSG_QUIT, MSG_SHOW, MSG_CONFIG_CHANGED,
    MSG_LANGUAGE_CHANGED,
    MSG_DOWNLOAD_CANCEL_FOR_WINDOW,
    MSG_DOWNLOAD_START_WORKER,
    MSG_DOWNLOAD_CANCEL_WORKER,
    MSG_REVERT_TO_LAST_URL,
    MSG_PIN_RELOAD,
    MSG_PIN_STATE,
    MSG_PIN_TOGGLE_FROM_BAR,
    MSG_FAVORITE_CHANGED,
    find_windows, find_window_by_host, find_process,
)
from i18n import load as i18n_load, on_change
import password_hook

import pinned_store
import notify_store
from dom_activity import DOM_ACTIVITY_JS, DomActivityMonitor
import comtypes
import comtypes.client
from comtypes import GUID, COMMETHOD, HRESULT, IUnknown


SEARCH_ENGINES = [
    "google.com", "bing.com", "baidu.com", "sogou.com",
    "so.com", "360.cn", "yahoo.com", "duckduckgo.com",
    "yandex.com", "naver.com", "daum.net",
]

MEM_THRESHOLD_MB = 900

ROUND_TIMER_INTERVAL = 3000


try:
    from qtwebview2._bridge import BRIDGE_SCRIPT as _QTWEBVIEW_BRIDGE
except Exception:
    _QTWEBVIEW_BRIDGE = ""


_USER_SCRIPT = r"""
(function() {
    // ================================================================
    // 第一段：滚动条样式 + hover
    // ================================================================
    (function() {
        var css = [
            '::-webkit-scrollbar { width: 8px; height: 8px; background: transparent; }',
            '::-webkit-scrollbar-track { background: transparent; margin: 12px; }',
            '::-webkit-scrollbar-track-piece { background: transparent; margin: 12px; }',
            '::-webkit-scrollbar-thumb {',
            '    background: rgba(120, 120, 120, 0.04);',
            '    border-radius: 4px;',
            '    border: none;',
            '}',
            '::-webkit-scrollbar-corner { background: transparent; }',
            '::-webkit-scrollbar-button { display: none; }',
            'html.sb-hover::-webkit-scrollbar-thumb {',
            '    background: rgba(120, 120, 120, 0.75);',
            '}',
            'html.sb-hover *::-webkit-scrollbar-thumb {',
            '    background: rgba(120, 120, 120, 0.75);',
            '}'
        ].join('\n');

        function ensureStyle() {
            var head = document.head || document.documentElement;
            if (!head) return null;
            var el = document.getElementById('__sb_style');
            if (el) return el;
            var style = document.createElement('style');
            style.id = '__sb_style';
            style.type = 'text/css';
            style.appendChild(document.createTextNode(css));
            head.appendChild(style);
            return style;
        }

        if (window.__sb_installed) return;
        window.__sb_installed = true;

        var W = 14, hovering = false, pending = false;

        function setHover(on) {
            if (on === hovering) return;
            hovering = on;
            if (on) document.documentElement.classList.add('sb-hover');
            else document.documentElement.classList.remove('sb-hover');
        }

        document.addEventListener('mousemove', function(e) {
            if (pending) return;
            pending = true;
            requestAnimationFrame(function() {
                var nearRight = (window.innerWidth - e.clientX) <= W;
                var nearBottom = (window.innerHeight - e.clientY) <= W;
                setHover(nearRight || nearBottom);
                pending = false;
            });
        }, { passive: true });

        document.addEventListener('mouseleave', function() { setHover(false); });
        window.addEventListener('blur', function() { setHover(false); });

        setInterval(function() {
            if (!document.getElementById('__sb_style')) {
                ensureStyle();
            }
        }, 3000);

        try {
            var mo = new MutationObserver(function() {
                if (!document.getElementById('__sb_style')) ensureStyle();
            });
            mo.observe(document.documentElement, { childList: true, subtree: true });
        } catch (e) {}

        ensureStyle();
    })();

    // ================================================================
    // 第二段：跨域导航拦截（appnav）
    // ================================================================
    (function() {
        if (window.__appnav_installed) return;
        window.__appnav_installed = true;

        function rootHost(host) {
            if (!host) return "";
            var parts = host.split(".");
            if (parts.length <= 2) return host;
            return parts.slice(-2).join(".");
        }

        function isSameRoot(h1, h2) {
            if (!h1 || !h2) return false;
            if (h1 === h2) return true;
            return rootHost(h1) === rootHost(h2);
        }

        function reportAndBlock(e, href) {
            e.preventDefault();
            e.stopPropagation();
            try {
                if (window.ipc && window.ipc.postMessage) {
                    window.ipc.postMessage(JSON.stringify({
                        type: "appnav",
                        url: href
                    }));
                }
            } catch (err) {}
        }

        document.addEventListener("click", function(e) {
            if (e.button !== 0) return;
            if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;

            var a = null;
            try {
                a = e.target && e.target.closest ? e.target.closest("a") : null;
            } catch (err) {
                a = null;
            }
            if (!a) return;

            var href = a.href;
            if (!href) return;
            if (href.indexOf("javascript:") === 0) return;
            if (href.charAt(0) === "#") return;

            var target;
            try {
                target = new URL(href);
            } catch (err) {
                return;
            }
            if (target.protocol !== "http:" && target.protocol !== "https:") return;
            if (!target.hostname) return;

            var cur = location.hostname;
            if (isSameRoot(cur, target.hostname)) {
                return;
            }

            reportAndBlock(e, href);
        }, true);
    })();
})();
"""


INIT_SCRIPT = (_QTWEBVIEW_BRIDGE + _USER_SCRIPT
               + password_hook.PASSWORD_JS
               + DOM_ACTIVITY_JS)


def url_host(url):
    try:
        host = (urlparse(url).hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        return ""


def _root_host(host):
    if not host:
        return ""
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    return ".".join(parts[-2:])

def _norm_url(url):
    """规范化 URL：去 query + fragment。"""
    if not url:
        return ""
    try:
        from urllib.parse import urlsplit, urlunsplit
        parts = urlsplit(url)
        return urlunsplit((
            parts.scheme, parts.netloc, parts.path,
            "", "",
        ))
    except Exception:
        return url



def _clean_js_url(raw):
    if raw is None:
        return ""
    s = str(raw).strip()
    if not s:
        return ""

    for _ in range(3):
        if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
            s = s[1:-1].strip()
        else:
            break

    try:
        import json as _json
        if s.startswith(('"', "'")):
            s = _json.loads(s)
    except Exception:
        pass

    return s


class History:
    """历史记录转发。具体逻辑在 history_hook。"""

    @staticmethod
    def record(window, title, url=""):
        from history_hook import record
        record(window, title, url)


def _pretty_url_for_address_bar(url):
    if not url:
        return url
    try:
        p = urlparse(url)
        if not p.query:
            return url

        out = []
        for pair in p.query.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                out.append(k + "=" + unquote(v))
            else:
                out.append(unquote(pair))
        new_query = "&".join(out)

        return urlunparse((
            p.scheme, p.netloc, p.path,
            p.params, new_query, p.fragment,
        ))
    except Exception:
        return url


def _is_redirect_url(url):
    try:
        parsed = urlparse(url)
        path = parsed.path or ""
        query = parsed.query or ""
        return (
            "/link" in path
            or "/ck/" in path
            or "url=" in query
        )
    except Exception:
        return False


def set_topmost(hwnd, on=True):
    HWND_TOPMOST = -1
    HWND_NOTOPMOST = -2
    SWP_NOMOVE = 0x0002
    SWP_NOSIZE = 0x0001
    SWP_NOACTIVATE = 0x0010
    try:
        ctypes.windll.user32.SetWindowPos(
            wintypes.HWND(int(hwnd)),
            HWND_TOPMOST if on else HWND_NOTOPMOST,
            0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE,
        )
    except Exception:
        pass


_WEBVIEW2_CLASSES = {
    "Chrome_WidgetWin_0",
    "Chrome_WidgetWin_1",
    "Chrome_WidgetWin_2",
    "Chrome_RenderWidgetHostHWND",
}


def _enum_child_hwnds(parent_hwnd):
    result = []

    def enum_proc(hwnd, lparam):
        try:
            buf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.GetClassNameW(hwnd, buf, 512)
            result.append((hwnd, buf.value))
        except Exception:
            pass
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(
        ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
    )
    try:
        ctypes.windll.user32.EnumChildWindows(
            wintypes.HWND(parent_hwnd), WNDENUMPROC(enum_proc), 0
        )
    except Exception:
        pass
    return result


# ======================================================================
# 任务栏卡片显隐（ITaskbarList）
# ======================================================================
class ITaskbarList(IUnknown):
    _iid_ = GUID("{56FDF342-FD6D-11D0-958A-006097C9A090}")
    _methods_ = [
        COMMETHOD([], HRESULT, "HrInit"),
        COMMETHOD([], HRESULT, "AddTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "DeleteTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "ActivateTab",
                  (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "SetActiveAlt",
                  (["in"], wintypes.HWND, "hwnd")),
    ]


class TaskbarHelper:
    """封装 ITaskbarList。运行中动态隐藏/显示任务栏卡片。"""

    CLSID_TASKBAR_LIST = GUID("{56FDF344-FD6D-11D0-958A-006097C9A090}")

    def __init__(self):
        self._taskbar = None
        self._ok = False
        try:
            self._taskbar = comtypes.client.CreateObject(
                self.CLSID_TASKBAR_LIST,
                interface=ITaskbarList,
            )
            self._taskbar.HrInit()
            self._ok = True
            print("[window] ITaskbarList 初始化成功")
        except Exception as e:
            print("[window] ITaskbarList 初始化失败:", repr(e))

    def hide(self, hwnd):
        if not self._ok:
            return
        try:
            self._taskbar.DeleteTab(int(hwnd))
        except Exception:
            pass

    def show(self, hwnd):
        if not self._ok:
            return
        try:
            self._taskbar.AddTab(int(hwnd))
        except Exception:
            pass


class RoundedWindow(QWidget):

    RADIUS = Theme.RADIUS
    WEB_RADIUS = Theme.WEB_RADIUS
    RESIZE_MARGIN = Theme.RESIZE_MARGIN
    CORNER_MARGIN = Theme.CORNER_MARGIN
    TOP_BAR_HEIGHT = Theme.TOP_BAR_HEIGHT
    WEB_TOP_GAP = Theme.WEB_TOP_GAP
    SIDE_MARGIN = Theme.SIDE_MARGIN
    BOTTOM_MARGIN = Theme.BOTTOM_MARGIN

    BORDER = 1
    OUTLINE_ALPHA = 180

    STAGGER_STEP = 30
    STAGGER_MAX = 8

    DL_URL_COOLDOWN = 5.0
    URL_POLL_INTERVAL = 400

    def __init__(self, mode="default", window_id="df-0",
                 host="", start_url="", pinned_url=""):
        print(f"[DBG] RoundedWindow.__init__ enter id={id(self)} "
              f"mode={mode} window_id={window_id}")
        super().__init__()
        self._mode = mode
        self._window_id = window_id
        self._start_url = start_url
        self._pinned_url = pinned_url

        self._pending_input_host = ""

        # ---- 固定状态 ----
        self._pin_on = False
        self._taskbar = TaskbarHelper()

        # ---- 搜索引擎（内存，不持久化，关窗口即清）----
        self._current_engine = None      # dict {"abbr", "url"}
        self._engine_picker = None       # EnginePicker 实例（显示中）
        self._engine_favicon_cache = {}  # url -> QPixmap
        # ------------------------------------------------

        # ---- 收藏菜单 ----
        self._fav_menu = None            # FavoritesMenu 实例
        # ------------------
        self._taskbar_timer = QTimer(self)
        self._taskbar_timer.setInterval(500)
        self._taskbar_timer.timeout.connect(self._apply_taskbar_visibility)
        # ------------------

        # ---- 完成提醒 ----
        self._complete_notify_on = False
        self._dom_monitor = DomActivityMonitor(self, self._on_dom_over)
        # ------------------

        # ---- 屏幕外最小化 ----
        self._offscreen = False
        self._pre_offscreen_pos = None
        # ----------------------

        self._hosts = set()
        self._primary_host = ""
        if host:
            self._hosts.add(host)
            self._primary_host = host

        self._has_loaded_once = bool(host)

        self._web_view = None
        self._current_url = ""

        self._popup = None
        self._activity = ActivityWatcher(QApplication.instance(), self)
        self._activity.activeWindowChanged.connect(
            self._refresh_popup_visibility
        )

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(480, 300)
        self.resize(1000, 700)

        self._resize_edge = None
        self._start_geo = None
        self._start_pos = None
        self._resizing = False
        self.setMouseTracking(True)

        self._url_settle_timer = QTimer(self)
        self._url_settle_timer.setSingleShot(True)
        self._url_settle_timer.setInterval(300)
        self._url_settle_timer.timeout.connect(self._on_url_settled)

        self._bg_path = ""
        self._bg_pixmap = None
        self._on_change_cb = None

        self._download_workers = {}
        self._dl_url = ""
        self._dl_path = ""
        self._last_dl_url_time = {}
        self._last_request_url = {}

        self._url_poll_timer = QTimer(self)
        self._url_poll_timer.setInterval(self.URL_POLL_INTERVAL)
        self._url_poll_timer.timeout.connect(self._poll_url_once)
        self._poll_busy = False
        self._addr_editing = False
        self._last_display_url = ""

        # ---- favicon 状态 ----
        self._favicon_pixmap = None
        self._favicon_cache = {}
        self._has_favicon_signal = False
        self._favicon_poll = QTimer(self)
        self._favicon_poll.setInterval(800)
        self._favicon_poll.timeout.connect(self._poll_favicon)
        self._favicon_poll.start()
        # ----------------------

        self._apply_saved_theme()

        self._setup_title_bar()
        self._setup_input_box()

        self._create_web_view()

        self._setup_corner_mask()

        try:
            password_hook.install(self)
        except Exception as e:
            print("[window] password_hook install 失败:", e)

        self.create_popup(title="标签")
        self._restore_pinned_memory()

        self._ipc_server = IpcServer(
            window_channel(self._window_id),
            self._on_ipc_message,
            role=window_role(self._window_id),
            extra={
                "type": self._mode,
                "window_id": self._window_id,
                "hosts": list(self._hosts),
                "host": self._primary_host,
            },
        )
        self._ipc_server.start()

        self._load_saved_background()
        self._apply_stagger_position()

        self._on_change_cb = self._refresh_texts
        try:
            on_change(self._on_change_cb)
        except Exception as e:
            print("[window] 注册语言回调失败:", e)

        self._round_timer = QTimer(self)
        self._round_timer.setInterval(ROUND_TIMER_INTERVAL)
        self._round_timer.timeout.connect(self._apply_round_region)
        self._round_timer.start()

        print(f"[DBG] __init__ exit id={id(self)}")

        # 启动加载：pinned_url（固定内容）优先，其次 start_url
        _boot_url = self._pinned_url or self._start_url
        if _boot_url:
            QTimer.singleShot(200, lambda u=_boot_url: self.handle_url(u))

        # 固定状态初始化：如果启动时是固定窗口，同步开关视觉 + 启动任务栏定时器
        _pin_host = self._pin_host()
        if _pin_host and pinned_store.is_pinned(_pin_host):
            self._pin_on = True
            if hasattr(self, "title_bar"):
                try:
                    self.title_bar.set_pin_switch_state(True)
                except Exception:
                    pass
            self._taskbar_timer.start()
            QTimer.singleShot(0, self._apply_taskbar_visibility)

        # ---- 完成提醒：独立恢复（不依赖固定项）----
        # 原先这段嵌在上面的 is_pinned 分支里，导致"没固定的站点打开开关，
        # 关窗就忘、下次又变回关"，看起来像功能丢了。现在独立存/读。
        try:
            if _pin_host and notify_store.is_on(_pin_host):
                self._complete_notify_on = True
                self._dom_monitor.start()
                print("[window] 完成提醒已恢复: %s" % _pin_host)
        except Exception as e:
            print("[window] 读取完成提醒状态失败:", e)

        # ---- 预抓搜索引擎图标（后台，延迟 1.5s 避免和窗口初始化抢资源）----
        QTimer.singleShot(1500, self._prefetch_engine_icons)
        # ------------------------------------------------------------

    # =========================================================
    # pwindow：创建 / 显隐判断
    # =========================================================
    def create_popup(self, title="弹窗"):
        if self._popup is None:
            self._popup = PopupWindow(parent=self, title=title)
            self._popup.url_selected.connect(self._on_popup_url_selected)
            self._popup.url_closed.connect(self._on_popup_url_closed)
            self._popup.destroyed.connect(self._on_popup_destroyed)
            self._popup.set_favicon(self._favicon_pixmap)
        return self._popup

    def _on_popup_destroyed(self, *_):
        self._popup = None

    # =========================================================
    # 固定记录
    # =========================================================
    def _root_host_of(self, url):
        try:
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

    def _restore_pinned_memory(self):
        """启动时把固定记录的 popup 列表灌回 popup，定位索引。"""
        if self._mode == "search":
            return
        host = self._pin_host()
        if not host or not pinned_store.is_pinned(host):
            return
        try:
            item = pinned_store.load_one(host)
        except ValueError as e:
            print("[window] 固定项损坏:", e)
            return
        if not item or self._popup is None:
            return

        urls = item.get("popup_urls", [])
        last_index = item.get("last_index", -1)

        for u in urls:
            self._popup.append_url(u)

        if urls:
            if 0 <= last_index < len(urls):
                self._popup.set_current_url(urls[last_index])
            else:
                self._popup.set_current_url(urls[-1])

        self._pin_on = True

    def _save_pinned_memory(self):
        """关窗时：如果固定状态开着，保存 popup_urls 和选中索引。"""
        if self._mode == "search":
            return
        if not self._pin_on:
            return
        host = self._pin_host()
        if not host or not pinned_store.is_pinned(host):
            return
        if self._popup is None:
            return
        try:
            urls = self._popup.urls()
            cur = self._popup.current_url() or ""
            last_index = -1
            if cur and cur in urls:
                last_index = urls.index(cur)
            elif urls:
                last_index = len(urls) - 1

            pinned_store.save_one(
                host,
                hosts=list(self._hosts),
                popup_urls=urls,
                last_index=last_index,
            )
        except Exception as e:
            print("[window] 保存固定记忆失败:", e)

    def _pin_host(self):
        """当前可固定的主域（key）。**始终返回主域**，不是具体 host。"""
        h = self._primary_host or self._root_host_of(self._current_url)
        if not h:
            return ""
        return self._root_host_of(h) or h

    def _pin_snapshot(self):
        """打包当前固定内容，供上报 bar。"""
        urls = []
        cur = ""
        if self._popup is not None:
            urls = self._popup.urls()
            cur = self._popup.current_url() or ""
        last_index = -1
        if cur and cur in urls:
            last_index = urls.index(cur)
        elif urls:
            last_index = len(urls) - 1

        return {
            "host": self._pin_host(),
            "hosts": list(self._hosts),
            "popup_urls": urls,
            "last_index": last_index,
            "on": self._pin_on,
            "complete_notify": bool(self._complete_notify_on),
        }

    def _notify_bar_pin_state(self):
        """上报固定状态给 bar。"""
        try:
            data = self._pin_snapshot()
            if not data["host"]:
                return
            payload = json.dumps(data, ensure_ascii=False)
            IpcClient.send_to_role(
                "bar", MSG_PIN_STATE, payload.encode("utf-8"),
            )
        except Exception as e:
            print("[window] 上报固定状态失败:", e)

    def _on_pin_switch_toggled(self, on):
        """用户在菜单里点击固定开关。"""
        host = self._pin_host()
        if not host:
            return

        if on:
            # 上限检查由 bar 做，本地直接开
            self._pin_on = True
        else:
            self._pin_on = False

        self._notify_bar_pin_state()
        self._apply_taskbar_visibility()

        # 打开固定：把当前完成提醒状态一并写盘
        if on and pinned_store.is_pinned(host):
            try:
                pinned_store.save_one(
                    host,
                    complete_notify=bool(self._complete_notify_on),
                )
            except Exception as e:
                print("[window] 保存完成提醒状态失败:", e)

    def _apply_taskbar_visibility(self):
        """根据 _pin_on 隐藏/显示任务栏卡片。"""
        try:
            hwnd = int(self.winId())
        except Exception:
            return
        if self._pin_on:
            self._taskbar.hide(hwnd)
        else:
            self._taskbar.show(hwnd)

    def _on_popup_url_selected(self, url):
        """点击 popup 里的 URL → 当前 web_view 加载。"""
        if not url:
            return
        if not self.web_view:
            return
        self._do_load(url)

    def _on_popup_url_closed(self, url):
        """点 popup 行的 ×，只从列表里删，不影响当前页面。"""
        if self._popup is not None:
            self._popup.remove_url(url)

    def is_effectively_active(self):
        active = QApplication.activeWindow()
        if active is self:
            return True
        if self._popup is not None and active is self._popup:
            return True
        return False

    def _refresh_popup_visibility(self, *_):
        p = self._popup
        if p is None:
            return

        if not getattr(p, "_user_opened", False):
            if p.isVisible():
                p.hide()
            return

        if getattr(p, "_user_closed", False):
            if p.isVisible():
                p.hide()
            return

        if (self.is_effectively_active()
                and self.isVisible()
                and not self.isMinimized()):
            if not p.isVisible():
                p.show()
                p.raise_()
        else:
            if p.isVisible():
                p.hide()

    @property
    def web_view(self):
        return self._web_view

    # =========================================================
    # web_view
    # =========================================================
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
        }

        ua = backend.get_user_agent()
        if ua:
            kwargs["user_agent"] = ua

        if backend.get_incognito():
            kwargs["incognito"] = True

        user_data = backend.get_user_data_folder(self._window_id)
        if user_data:
            kwargs["user_data_folder"] = user_data

        try:
            wv = QtWebViewWidget(**kwargs)
        except TypeError as e:
            print("[window] 创建 web_view 参数不被支持:", e)
            wv = QtWebViewWidget(
                native_child=True,
                lazyload=False,
                initialization_script=INIT_SCRIPT,
                parent=self,
            )

        try:
            wv.signals.web_message_received.connect(self._on_js_message)
        except Exception as e:
            print("[window] 接 web_message_received 失败:", e)

        try:
            wv.signals.title_changed.connect(self._on_title_changed)
        except Exception as e:
            print("[window] 接 title_changed 失败:", e)

        try:
            wv.signals.favicon_changed.connect(self._on_favicon_changed)
            self._has_favicon_signal = True
        except Exception as e:
            print("[window] 无 favicon_changed 信号，用 JS 兜底:", e)

        wv.hide()
        wv.setGeometry(0, 0, 0, 0)
        self._web_view = wv

    def _on_title_changed(self, title):
        if not title:
            return
        url = self._current_url or ""
        if not url:
            return
        if self._popup is not None:
            self._popup.set_title(url, title)
        try:
            History.record(self, title, url)
        except Exception as e:
            print("[window] _on_title_changed 异常:", e)

    # =========================================================
    # favicon
    # =========================================================
    _JS_FAVICON = """
    (function(){
        // 按优先级找，返回最大的那个图标
        function getSize(link) {
            var s = link.getAttribute("sizes");
            if (!s) return 0;
            var m = s.match(/(\\d+)/);
            return m ? parseInt(m[1], 10) : 0;
        }

        var candidates = [];

        // 1. apple-touch-icon（通常 180x180，最清晰）
        var appleLinks = document.querySelectorAll(
            'link[rel="apple-touch-icon"], link[rel="apple-touch-icon-precomposed"]'
        );
        for (var i = 0; i < appleLinks.length; i++) {
            if (appleLinks[i].href) {
                candidates.push({ href: appleLinks[i].href, size: getSize(appleLinks[i]) || 180 });
            }
        }

        // 2. 普通 icon，取最大的
        var iconLinks = document.querySelectorAll(
            'link[rel~="icon"], link[rel="shortcut icon"]'
        );
        for (var j = 0; j < iconLinks.length; j++) {
            if (iconLinks[j].href) {
                candidates.push({ href: iconLinks[j].href, size: getSize(iconLinks[j]) || 16 });
            }
        }

        if (candidates.length === 0) return "";

        // 取 size 最大的
        candidates.sort(function(a, b) { return b.size - a.size; });
        return candidates[0].href;
    })()
    """

    def _fetch_title(self, url):
        """拿 document.title，同时更新 popup 和写 history。"""
        wv = self.web_view
        if wv is None or not wv.isVisible():
            return

        def _cb(raw_title):
            try:
                title = _clean_js_url(raw_title)
                if not title:
                    return
                if self._popup is not None:
                    self._popup.set_title(url, title)
                History.record(self, title, url)
            except Exception as e:
                print(f"[window] _fetch_title 异常: {e}")

        try:
            wv.eval_js("document.title", _cb)
        except Exception:
            pass

    def _on_favicon_changed(self, icon):
        if icon is None or icon.isNull():
            return
        pm = icon.pixmap(24, 24)
        if pm.isNull():
            return
        self._favicon_pixmap = pm
        self._apply_favicon()

    def _poll_favicon(self):
        wv = self.web_view
        if wv is None or not wv.isVisible():
            return

        def _cb(href):
            try:
                href = _clean_js_url(href)
                if not href:
                    return
                if href.startswith("data:"):
                    self._favicon_from_data_uri(href)
                    return
                if href in self._favicon_cache:
                    self._favicon_pixmap = self._favicon_cache[href]
                    self._apply_favicon()
                    return
                self._download_favicon(href)
            except Exception as e:
                print("[window] favicon JS 回调异常:", e)

        try:
            wv.eval_js(self._JS_FAVICON, _cb)
        except Exception as e:
            print("[window] eval_js favicon 失败:", e)

    def _favicon_from_data_uri(self, uri):
        import base64
        try:
            header, _, b64 = uri.partition(",")
            raw = base64.b64decode(b64) if "base64" in header else b64.encode()
            pm = QPixmap()
            pm.loadFromData(raw)
            if not pm.isNull():
                self._favicon_cache[uri] = pm
                self._favicon_pixmap = pm
                self._apply_favicon()
        except Exception as e:
            print("[window] data URI 解析失败:", e)

    def _download_favicon(self, href):
        from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
        if not hasattr(self, "_nam"):
            self._nam = QNetworkAccessManager(self)
        reply = self._nam.get(QNetworkRequest(QUrl(href)))

        def _done():
            try:
                pm = QPixmap()
                pm.loadFromData(bytes(reply.readAll()))
                if not pm.isNull():
                    self._favicon_cache[href] = pm
                    self._favicon_pixmap = pm
                    self._apply_favicon()
            except Exception as e:
                print("[window] favicon 下载回调异常:", e)
            finally:
                reply.deleteLater()

        reply.finished.connect(_done)

    def _apply_favicon(self):
        if hasattr(self, "title_bar"):
            self.title_bar.set_favicon(self._favicon_pixmap)
        if self._popup is not None:
            self._popup.set_favicon(self._favicon_pixmap)
        apply_icon_to_window(
            self, self._favicon_pixmap, self._current_url or ""
        )

        # ---- 固定项图标更新（只在 favicon 真的变了才写盘）----
        try:
            pin_host = self._pin_host()
            if (self._favicon_pixmap is not None
                    and not self._favicon_pixmap.isNull()
                    and self._pin_on
                    and pin_host
                    and pinned_store.is_pinned(pin_host)):
                # 用 pixmap 的 cacheKey 判重（Qt 保证同一图返回相同值）
                fp = (self._favicon_pixmap.width(),
                      self._favicon_pixmap.height(),
                      self._favicon_pixmap.cacheKey())
                if getattr(self, "_last_saved_favicon_fp", None) != fp:
                    self._last_saved_favicon_fp = fp
                    pinned_store.save_icon(
                        pin_host, self._favicon_pixmap
                    )
                    try:
                        IpcClient.send_to_role(
                            "bar", MSG_PIN_RELOAD, b""
                        )
                    except Exception:
                        pass
        except Exception as e:
            print("[window] 同步 favicon 到固定项失败:", e)

    def _reset_favicon(self, url=""):
        self._favicon_pixmap = None
        if hasattr(self, "title_bar"):
            self.title_bar.set_favicon(None)
        if self._popup is not None:
            self._popup.set_favicon(None)

        apply_icon_to_window(self, None, url or self._current_url or "")

    # =========================================================
    # host
    # =========================================================
    def _add_host(self, host, primary=False):
        if not host:
            return
        if host in self._hosts:
            if primary and not self._primary_host:
                self._primary_host = host
            return
        self._hosts.add(host)
        if primary or not self._primary_host:
            self._primary_host = host
        self._has_loaded_once = True
        self._sync_registry()

    def _sync_registry(self):
        try:
            from ipc import register_process
            register_process(
                window_role(self._window_id),
                window_channel(self._window_id),
                extra={
                    "type": self._mode,
                    "window_id": self._window_id,
                    "hosts": list(self._hosts),
                    "host": self._primary_host,
                },
            )
        except Exception:
            pass

    def _bar_host(self):
        return self._primary_host or ""

    def _has_root_host(self, host):
        """窗口里是否有该主域。"""
        if not host:
            return False
        new_root = _root_host(host)
        if not new_root:
            return False
        for h in self._hosts:
            if h and _root_host(h) == new_root:
                return True
        return False

    def _matches_host(self, host):
        if not host:
            return False
        if host in self._hosts:
            return True
        return self._is_related_host(host)

    def _is_related_host(self, new_host):
        if not new_host:
            return False
        new_root = _root_host(new_host)
        for h in self._hosts:
            if not h:
                continue
            if new_host == h:
                return True
            if new_host.endswith("." + h):
                return True
            if h.endswith("." + new_host):
                return True
            if new_root and new_root == _root_host(h):
                return True
        return False

    def _apply_stagger_position(self):
        try:
            n = len(find_windows())
        except Exception:
            n = 0

        screen = QApplication.primaryScreen().availableGeometry()
        base_w, base_h = self.width(), self.height()
        x0 = screen.left() + (screen.width() - base_w) // 2
        y0 = screen.top() + (screen.height() - base_h) // 2

        step = (n % self.STAGGER_MAX) * self.STAGGER_STEP
        self.move(x0 + step, y0 + step)

    # =========================================================
    # 主题 / 背景
    # =========================================================
    def _apply_saved_theme(self):
        try:
            s = load_window_settings(self._mode, self._window_id)
            color = QColor(s.get("theme_color", "#d0d0d0"))
            if not color.isValid():
                color = QColor("#d0d0d0")
            border, inner = Theme.apply_theme(color)
            TitleBar.BG_COLOR = border
        except Exception as e:
            print("[window] 应用主题失败:", e)

    def _load_saved_background(self):
        try:
            s = load_window_settings(self._mode, self._window_id)
            path = s.get("background_current", "")
            if path:
                # resolve_path 负责展开 {RES} 内置资源占位符
                real = resolve_path(path)
                pm = QPixmap(real)
                if not pm.isNull():
                    self._bg_path = real
                    self._bg_pixmap = pm
        except Exception:
            pass

    def _reload_config(self):
        try:
            s = load_window_settings(self._mode, self._window_id)
            color = QColor(s.get("theme_color", "#d0d0d0"))
            if color.isValid():
                border, inner = Theme.apply_theme(color)
                self.title_bar.apply_theme_color(border)
                if hasattr(self, "corner_mask"):
                    self.corner_mask.bg_color = border
                    self.corner_mask.update()

            path = s.get("background_current", "")
            real = resolve_path(path)
            if real and os.path.isfile(real):
                pm = QPixmap(real)
                if not pm.isNull():
                    self._bg_path = real
                    self._bg_pixmap = pm
            else:
                self._bg_path = ""
                self._bg_pixmap = None
            self.update()
        except Exception as e:
            print("[window] 重读配置失败:", e)

    def _broadcast_config_changed(self):
        try:
            IpcClient(CHANNEL_BROADCAST).send(MSG_CONFIG_CHANGED, b"")
        except Exception:
            pass

    # =========================================================
    # UI
    # =========================================================
    def _setup_title_bar(self):
        self.title_bar = TitleBar(self)
        self.title_bar.BG_COLOR = Theme.TITLE_BG_COLOR
        self.title_bar.setGeometry(
            self.BORDER, self.BORDER,
            self.width() - 2 * self.BORDER,
            self.TOP_BAR_HEIGHT,
        )
        self.title_bar.raise_()

        try:
            self.title_bar.address_bar.textEdited.connect(
                self._on_addr_text_edited
            )
            self.title_bar.address_bar.editingFinished.connect(
                self._on_addr_editing_finished
            )
        except Exception:
            pass

        try:
            self.title_bar.prev_tab.connect(self._prev_url)
        except Exception:
            pass
        try:
            self.title_bar.next_tab.connect(self._next_url)
        except Exception:
            pass
        try:
            self.title_bar.toggle_pin.connect(self._on_pin_switch_toggled)
        except Exception:
            pass
        try:
            self.title_bar.toggle_complete_notify.connect(
                self._on_complete_notify_toggled
            )
        except Exception:
            pass

        try:
            self.title_bar.star_left_clicked.connect(
                self._on_star_left_clicked
            )
        except Exception as e:
            print("[window] 接收藏星左键失败:", e)

        try:
            self.title_bar.star_right_clicked.connect(
                self._on_star_right_clicked
            )
        except Exception as e:
            print("[window] 接收藏星右键失败:", e)

    def _on_addr_text_edited(self, _text):
        self._addr_editing = True

    def _on_addr_editing_finished(self):
        self._addr_editing = False

    def _setup_input_box(self):
        self.input_box = InputBox(self)
        self.input_box.submitted.connect(self.visit)
        self.input_box.escaped.connect(self.show_input_box)
        try:
            self.input_box.engine_button().clicked.connect(
                self._on_engine_btn_clicked
            )
        except Exception as e:
            print("[window] 接引擎按钮信号失败:", e)
        self._center_input_box()

    def _setup_corner_mask(self):
        self.corner_mask = CornerMask(self)
        self.corner_mask.bg_color = Theme.BG_COLOR
        self.corner_mask.hide()

    # =========================================================
    # JS → Python
    # =========================================================
    def _on_js_message(self, msg):
        try:
            data = json.loads(msg)
        except Exception:
            return

        if not isinstance(data, dict):
            return

        t = data.get("type")
        if t != "pw_state":
            print(f"[DBG] js_msg type={t!r}")

        # ---- DOM 状态机事件（new/lazy 簇）----
        try:
            from dom_activity import DomActivityMonitor
            if t in DomActivityMonitor.TYPES:
                self._dom_monitor.feed(data)
                return
        except Exception as e:
            import traceback
            print("[window] dom feed 异常:")
            traceback.print_exc()
            return

        # ---- 其他 ----
        try:
            if password_hook.on_js_message(self, data):
                return
        except Exception as e:
            print("[window] password_hook 处理失败:", e)

        if t != "appnav":
            return

        url = data.get("url", "")
        if not url:
            return

        self._handle_external_nav(url)

    def _handle_external_nav(self, url):
        """网页内点击跨域链接 → 联系 bar。同主域不会走到这里（JS 已放行）。"""
        host = url_host(url)
        if not host:
            return

        if self._has_root_host(host):
            self._do_load(url)
            return

        self.request_url(url)

    def _on_new_window(self, url):
        from wryview import NewWindowResponse

        if url:
            QTimer.singleShot(0, lambda u=url: self._resolve_and_route(u))
        return NewWindowResponse.Deny

    def _resolve_and_route(self, url):
        import urllib.request

        host = url_host(url)

        if self._matches_host(host) and _is_redirect_url(url):
            try:
                req = urllib.request.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0")
                ref = self._current_url_str()
                if ref:
                    req.add_header("Referer", ref)
                resp = urllib.request.urlopen(req, timeout=5)
                real_url = resp.geturl()
                resp.close()
                self.handle_url(real_url)
                return
            except Exception:
                pass

        self.handle_url(url)

    def _on_navigation(self, url):
        """兜底：非点击导航（地址栏、JS 跳转）也拦跨域。"""
        host = url_host(url)
        if not host:
            return True

        if not self._hosts:
            return True

        if self._matches_host(host):
            return True

        from ipc import find_process
        if not find_process("bar"):
            return True

        self.request_url(url)
        return False

    def _on_drag_drop(self, event, paths, position):
        """WebView2 拖放事件。

        返回 True 让 WebView2 自己处理文件（默认行为）。
        """
        print(f"[window] drag_drop event={event} paths={paths} pos={position}")
        return True

    # =========================================================
    # 下载
    # =========================================================
    def _on_download_started(self, url, suggested_path):
        now = time.time()
        last = self._last_dl_url_time.get(url, 0)
        if now - last < self.DL_URL_COOLDOWN:
            return False
        self._last_dl_url_time[url] = now

        cutoff = now - 60
        self._last_dl_url_time = {
            u: t for u, t in self._last_dl_url_time.items() if t > cutoff
        }

        if url.startswith("blob:") or url.startswith("data:"):
            self._dl_url = ""
            self._dl_path = suggested_path
            try:
                from ipc import ROLE_DOWNLOADS, MSG_DOWNLOAD_START
                payload = json.dumps({
                    "url": url,
                    "path": suggested_path,
                    "filename": os.path.basename(suggested_path),
                    "total": -1,
                    "notify": True,
                    "window_id": self._window_id,
                }, ensure_ascii=False)
                IpcClient.send_to_role(
                    ROLE_DOWNLOADS, MSG_DOWNLOAD_START,
                    payload.encode("utf-8"),
                )
            except Exception as e:
                print("[window] blob 开始通知失败:", e)

            QTimer.singleShot(
                500,
                lambda u=url, p=suggested_path:
                    self._poll_blob_file(u, p),
            )
            return True

        QTimer.singleShot(
            0,
            lambda u=url, p=suggested_path: self._start_http_download_safe(u, p),
        )
        return False

    def _poll_blob_file(self, url, path, last_size=-1, retries=120):
        if not path:
            return

        if not os.path.isfile(path):
            if retries <= 0:
                self._send_blob_done(url, path, success=False)
                return
            QTimer.singleShot(
                500,
                lambda: self._poll_blob_file(
                    url, path, last_size, retries - 1),
            )
            return

        try:
            size = os.path.getsize(path)
        except OSError:
            size = 0

        if size != last_size:
            QTimer.singleShot(
                500,
                lambda: self._poll_blob_file(url, path, size, retries - 1),
            )
            return

        self._send_blob_done(url, path, success=True)

    def _send_blob_done(self, url, path, success):
        try:
            from ipc import ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE
            payload = json.dumps({
                "url": url,
                "path": path,
                "success": bool(success),
                "delete_partial": False,
            }, ensure_ascii=False)
            IpcClient.send_to_role(
                ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE,
                payload.encode("utf-8"),
            )
        except Exception as e:
            print("[window] blob 完成通知失败:", e)
        self._dl_path = ""

    def _start_http_download_safe(self, url, save_path):
        try:
            self._start_http_download(url, save_path)
        except Exception:
            import traceback
            print("[window] _start_http_download 异常:")
            traceback.print_exc()

    def _start_http_download(self, url, save_path):
        referer = self._current_url_str() or ""

        user_agent = ""
        try:
            from settings_backend import SettingsBackend
            user_agent = SettingsBackend().get_user_agent() or ""
        except Exception:
            pass

        prog, argv = apppaths.role_command(
            "download-worker",
            "--url", url,
            "--path", save_path,
            "--window-id", self._window_id,
            "--referer", referer,
            "--user-agent", user_agent,
        )

        proc = QProcess(self)
        proc.setProgram(prog)
        proc.setArguments(argv)
        apppaths.configure_child_proc(proc)
        proc.finished.connect(
            lambda code, status, u=url: self._on_worker_finished(u, code, status)
        )
        proc.start()
        self._download_workers[url] = proc

        QTimer.singleShot(
            300,
            lambda u=url: self._send_cookie_to_worker(u),
        )

    def _send_cookie_to_worker(self, url, retries=60):
        worker_channel = window_channel(self._window_id) + "_worker"

        if not find_process(worker_channel):
            if retries <= 0:
                return
            QTimer.singleShot(
                500,
                lambda: self._send_cookie_to_worker(url, retries - 1),
            )
            return

        cookie_str = ""
        try:
            wv = self.web_view
            if wv is not None:
                cookies = wv.cookies_for_url(url)
                parts = [f"{c.name}={c.value}" for c in cookies]
                cookie_str = "; ".join(parts)
        except Exception:
            pass

        try:
            payload = json.dumps({"cookie": cookie_str}, ensure_ascii=False)
            ok = IpcClient(worker_channel).send(
                MSG_DOWNLOAD_START_WORKER,
                payload.encode("utf-8"),
            )
            if not ok:
                if retries <= 0:
                    return
                QTimer.singleShot(
                    500,
                    lambda: self._send_cookie_to_worker(url, retries - 1),
                )
        except Exception:
            pass

    def _on_worker_finished(self, url, exit_code, exit_status):
        self._download_workers.pop(url, None)

    def _cancel_worker(self, url):
        proc = self._download_workers.get(url)
        if proc is None:
            self._notify_cancel_done(url)
            return

        try:
            try:
                worker_channel = window_channel(self._window_id) + "_worker"
                IpcClient(worker_channel).send(
                    MSG_DOWNLOAD_CANCEL_WORKER, b"",
                )
            except Exception:
                pass

            if not proc.waitForFinished(1500):
                proc.kill()
                proc.waitForFinished(500)
        except Exception:
            pass

        self._download_workers.pop(url, None)
        self._notify_cancel_done(url)

    def _notify_cancel_done(self, url):
        try:
            from ipc import ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE
            payload = json.dumps({
                "url": url,
                "path": "",
                "success": False,
                "delete_partial": True,
            }, ensure_ascii=False)
            IpcClient.send_to_role(
                ROLE_DOWNLOADS, MSG_DOWNLOAD_DONE,
                payload.encode("utf-8"),
            )
        except Exception:
            pass

    def _on_download_completed(self, url, saved_path, success):
        pass

    # =========================================================
    # 圆角
    # =========================================================
    def _find_webview2_hwnd(self, wv=None):
        if wv is None:
            wv = self.web_view
        if wv is None:
            return 0
        try:
            parent = int(wv.winId())
        except Exception:
            return 0
        if not parent:
            return 0

        children = _enum_child_hwnds(parent)
        for hwnd, cls in children:
            if cls in _WEBVIEW2_CLASSES:
                return hwnd

        if len(children) == 1:
            return children[0][0]
        return 0

    def _apply_round_region(self, wv=None):
        if wv is None:
            wv = self.web_view
        if wv is None:
            return
        try:
            hwnd = self._find_webview2_hwnd(wv)
            if not hwnd:
                return

            rect = wintypes.RECT()
            ctypes.windll.user32.GetClientRect(
                wintypes.HWND(hwnd), ctypes.byref(rect)
            )
            w = rect.right - rect.left
            h = rect.bottom - rect.top
            if w <= 0 or h <= 0:
                return

            r = self.WEB_RADIUS * 2

            ctypes.windll.user32.SetWindowRgn(
                wintypes.HWND(hwnd), 0, True
            )
            rgn = ctypes.windll.gdi32.CreateRoundRectRgn(
                0, 0, w + 1, h + 1, r, r
            )
            ctypes.windll.user32.SetWindowRgn(
                wintypes.HWND(hwnd), rgn, True
            )
        except Exception as e:
            print(f"[window] _apply_round_region 失败: {e}")

    def apply_web_view_round(self):
        wv = self.web_view
        if wv is None:
            return
        QTimer.singleShot(50, lambda w=wv: self._apply_round_region(w))
        QTimer.singleShot(200, lambda w=wv: self._apply_round_region(w))
        QTimer.singleShot(600, lambda w=wv: self._apply_round_region(w))

    # =========================================================
    # 网址
    # =========================================================
    def handle_url(self, url):
        """地址栏、外部入口。同主域 → 当前加载；跨域 → 交给 bar。"""
        host = url_host(url)
        if not host:
            return

        if not self._hosts:
            self._pending_input_host = host
            self._do_load(url)
            return

        if self._has_root_host(host):
            self._do_load(url)
            return

        self.request_url(url)

    def request_url(self, url):
        if not url:
            return

        now = time.time()
        last = self._last_request_url.get(url, 0)
        if now - last < 1.0:
            return
        self._last_request_url[url] = now

        cutoff = now - 10
        self._last_request_url = {
            u: t for u, t in self._last_request_url.items() if t > cutoff
        }

        try:
            payload = json.dumps({
                "cmd": "request_url",
                "window_id": self._window_id,
                "host": self._bar_host(),
                "url": url,
            }, ensure_ascii=False)
            IpcClient.send_to_role("bar", MSG_NAVIGATE, payload)
        except Exception as e:
            print("[window] request_url 失败:", e)

    # =========================================================
    # IPC
    # =========================================================
    def _on_complete_notify_toggled(self, on):
        """用户点"完成提醒"开关。"""
        print(f"[DBG] _on_complete_notify_toggled on={on}")
        self._complete_notify_on = bool(on)
        if on:
            self._dom_monitor.start()
        else:
            self._dom_monitor.stop()

        host = self._pin_host()

        # 独立存储：**任何站点**都记住开关状态，重开窗口仍生效
        if host:
            try:
                notify_store.set(host, bool(on))
            except Exception as e:
                print("[window] 保存完成提醒状态失败:", e)

        # 已固定的站点，额外同步到固定项（兼容旧数据 / 固定项自己也要用）
        if host and pinned_store.is_pinned(host):
            try:
                pinned_store.save_one(host, complete_notify=bool(on))
            except Exception as e:
                print("[window] 保存完成提醒状态失败:", e)

    def _on_dom_over(self):
        """DOM 停止新增 6s，强制置顶 + 声音提示。"""
        if not self._complete_notify_on:
            return

        # 声音提示
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        except Exception as e:
            print("[window] 声音提示失败:", e)

        self._bring_to_front()

    def minimize_or_offscreen(self):
        """用户点最小化按钮。

        提醒开着 → 移到屏幕外（保持 WebView2 活跃）；
        提醒没开 → 正常最小化。
        """
        if getattr(self, "_complete_notify_on", False):
            self._move_offscreen()
        else:
            self.showMinimized()

    def _move_offscreen(self):
        """把窗口移到所在屏幕右侧之外。记住当前位置以便恢复。"""
        try:
            if self._offscreen:
                return

            self._pre_offscreen_pos = self.pos()

            screen = self.screen() or QApplication.primaryScreen()
            geo = screen.availableGeometry()
            new_x = geo.right() + 120
            new_y = self.y()

            self.move(new_x, new_y)
            self._offscreen = True
            print(f"[window] 移出屏幕 x={new_x} y={new_y}")
        except Exception as e:
            print("[window] _move_offscreen 失败:", e)

    def _restore_from_offscreen(self):
        """从屏幕外移回原位置。"""
        if not self._offscreen:
            return
        try:
            if self._pre_offscreen_pos is not None:
                self.move(self._pre_offscreen_pos)
            else:
                screen = self.screen() or QApplication.primaryScreen()
                geo = screen.availableGeometry()
                self.move(
                    geo.left() + (geo.width() - self.width()) // 2,
                    geo.top() + (geo.height() - self.height()) // 2,
                )
            print("[window] 从屏幕外移回")
        except Exception as e:
            print("[window] _restore_from_offscreen 失败:", e)
        finally:
            self._offscreen = False
            self._pre_offscreen_pos = None

    def _bring_to_front(self):
        """把窗口带到前台。最小化时用 ShowWindow(SW_RESTORE) 强制恢复。"""
        try:
            # 在屏幕外 → 先移回来
            if getattr(self, "_offscreen", False):
                self._restore_from_offscreen()

            hwnd = int(self.winId())

            # 最小化 → 用底层 ShowWindow 强制恢复（比 showNormal 更可靠）
            try:
                SW_RESTORE = 9
                SW_SHOW = 5
                user32 = ctypes.windll.user32
                if user32.IsIconic(wintypes.HWND(hwnd)):
                    user32.ShowWindow(wintypes.HWND(hwnd), SW_RESTORE)
                else:
                    user32.ShowWindow(wintypes.HWND(hwnd), SW_SHOW)
            except Exception as e:
                print("[window] ShowWindow 失败:", e)

            if self.isMinimized():
                self.showNormal()

            self.show()
            self.raise_()
            self.activateWindow()

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            fg_hwnd = user32.GetForegroundWindow()
            fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
            cur_thread = kernel32.GetCurrentThreadId()

            if fg_thread and cur_thread and fg_thread != cur_thread:
                # 附加到前台线程，绕过前台锁
                user32.AttachThreadInput(fg_thread, cur_thread, True)
                try:
                    user32.SetForegroundWindow(wintypes.HWND(hwnd))
                    user32.BringWindowToTop(wintypes.HWND(hwnd))
                    user32.SetActiveWindow(wintypes.HWND(hwnd))
                finally:
                    user32.AttachThreadInput(fg_thread, cur_thread, False)
            else:
                user32.SetForegroundWindow(wintypes.HWND(hwnd))

            set_topmost(hwnd, True)
            QTimer.singleShot(900, lambda: set_topmost(hwnd, False))
        except Exception as e:
            print("[window] _bring_to_front 失败:", e)

    def _on_ipc_message(self, msg_type, payload):
        QTimer.singleShot(
            0, lambda t=msg_type, p=payload: self._handle_ipc(t, p)
        )

    def _handle_ipc(self, msg_type, payload):
        if msg_type == MSG_QUIT:
            self.close()
            return

        if msg_type == MSG_LANGUAGE_CHANGED:
            try:
                code = payload.decode("utf-8")
                i18n_load(code)
                self._refresh_texts()
            except Exception as e:
                print("[window] 切换语言失败:", e)
            return

        if msg_type == MSG_CONFIG_CHANGED:
            if self._mode in ("default", "search"):
                self._reload_config()
            return

        if msg_type == MSG_SHOW:
            self._bring_to_front()
            return

        if msg_type == MSG_DOWNLOAD_CANCEL_FOR_WINDOW:
            try:
                data = json.loads(payload.decode("utf-8"))
                url = data.get("url", "")
            except Exception:
                url = ""
            self._cancel_worker(url)
            return

        if msg_type == MSG_REVERT_TO_LAST_URL:
            return

        if msg_type == MSG_PIN_TOGGLE_FROM_BAR:
            # bar 处取消固定 / 满 24 → 关掉本地开关
            reason = ""
            try:
                data = json.loads(payload.decode("utf-8"))
                reason = data.get("reason", "")
            except Exception:
                pass

            self._pin_on = False
            if hasattr(self, "title_bar"):
                try:
                    self.title_bar.set_pin_switch_state(False)
                except Exception:
                    pass
            self._apply_taskbar_visibility()

            # 满 24 → 弹提示
            if reason == "full":
                try:
                    from i18n import t
                    box = QMessageBox(self)
                    box.setWindowTitle(t("app.title"))
                    box.setText(t("menu.pin_full"))
                    box.setIcon(QMessageBox.Icon.Information)
                    box.exec()
                except Exception as e:
                    print("[window] 弹满 24 提示失败:", e)

            return

        if msg_type == MSG_NAVIGATE:
            try:
                data = json.loads(payload.decode("utf-8"))
            except Exception:
                return
            url = data.get("url", "")
            if url:
                self._do_load(url)
            return

        if msg_type == MSG_FAVORITE_CHANGED:
            # 收藏变化广播 → 更新自己的星
            try:
                changed_url = payload.decode("utf-8")
            except Exception:
                changed_url = ""

            my_url = self._current_url or ""
            if changed_url and my_url and _norm_url(my_url) == _norm_url(changed_url):
                self._update_star_state()
            return

    def _refresh_texts(self):
        try:
            if hasattr(self, "title_bar") and hasattr(self.title_bar, "_refresh_texts"):
                self.title_bar._refresh_texts()
        except Exception as e:
            print("[window] 刷新文字失败:", e)

        try:
            dlg = getattr(self.title_bar, "_personalize_dialog", None)
            if dlg is not None and hasattr(dlg, "_refresh_texts"):
                dlg._refresh_texts()
        except Exception:
            pass

    # =========================================================
    # 导航
    # =========================================================
    def _do_load(self, url):
        if not url:
            return

        self._reset_favicon(url)

        # 每次主动导航都刷一次星
        QTimer.singleShot(100, self._update_star_state)

        wv = self.web_view
        if wv is None:
            return

        self._current_url = url
        self._update_web_view_geometry()
        wv.show()
        self.title_bar.set_browsing_mode(True)
        self.title_bar.set_address(_pretty_url_for_address_bar(url))
        self.update()

        try:
            wv.load_url(url)
        except Exception as e:
            print(f"[window] load_url 失败: {e}")

        QTimer.singleShot(50, self._update_web_view_geometry)
        QTimer.singleShot(200, self._update_web_view_geometry)
        QTimer.singleShot(600, self._update_web_view_geometry)

        self.apply_web_view_round()

        self._url_settle_timer.start()

        self._last_display_url = ""
        self._poll_url_once()
        if not self._url_poll_timer.isActive():
            self._url_poll_timer.start()

    def _current_url_str(self):
        wv = self.web_view
        try:
            if wv is not None:
                u = wv.url()
                if u:
                    return str(u)
        except Exception:
            pass
        return self._current_url or ""

    def _poll_url_once(self):
        if self._poll_busy:
            return
        wv = self.web_view
        if wv is None or not wv.isVisible():
            return
        if self._addr_editing:
            return

        self._poll_busy = True

        def _cb(real_url):
            self._poll_busy = False
            url_str = ""
            try:
                url_str = _clean_js_url(real_url)
                if not url_str or url_str == "about:blank":
                    return

                if url_str == self._last_display_url:
                    return

                host = url_host(url_str)
                if not host:
                    return
                if not self._has_root_host(host):
                    return

                self._last_display_url = url_str
                self.title_bar.set_address(
                    _pretty_url_for_address_bar(url_str)
                )

                if not _is_redirect_url(url_str):
                    self._current_url = url_str

                if self._popup is not None:
                    self._popup.append_url(url_str)
                    self._popup.set_current_url(url_str)

                if (not self._has_favicon_signal
                        and not self._favicon_poll.isActive()):
                    self._favicon_poll.start()

                self._fetch_title(url_str)
            except Exception as e:
                print(f"[window] _poll_url_once 回调异常: {e}")
            finally:
                # 不管 URL 变没变，都刷新一次星
                try:
                    self._update_star_state(url_str)
                except Exception:
                    pass

        try:
            wv.eval_js("location.href", _cb)
        except Exception as e:
            self._poll_busy = False
            print(f"[window] _poll_url_once eval_js 失败: {e}")

    @staticmethod
    def _entry_alive(entry):
        """检查 registry 里那条记录对应的进程还在不在。"""
        if not entry:
            return False
        pid = entry.get("pid")
        if not pid:
            return False
        try:
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            h = ctypes.windll.kernel32.OpenProcess(
                PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid)
            )
            if not h:
                return False
            ctypes.windll.kernel32.CloseHandle(h)
            return True
        except Exception:
            return True

    def _on_url_settled(self):
        wv = self.web_view
        if wv is None:
            return

        def _cb(real_url):
            try:
                url_str = _clean_js_url(real_url)
                if not url_str or url_str == "about:blank":
                    return
                new_host = url_host(url_str)
                if not new_host:
                    return

                is_redirect = _is_redirect_url(url_str)

                if not self._hosts:
                    # 1. 有同 host 窗口 → 转给 bar，自毁
                    role, entry = find_window_by_host(new_host)
                    print(f"[DBG] df 新窗口访问 {new_host}，"
                          f"find_window_by_host 结果 role={role} "
                          f"alive={self._entry_alive(entry) if entry else False}")
                    if role and self._entry_alive(entry):
                        print("[DBG] 走分支 1：转给 bar + 自毁")
                        self.request_url(url_str)
                        if not self._has_loaded_once:
                            QTimer.singleShot(100, self.close)
                        return

                    # 2. 没有，但该主域有固定 → 转给 bar（bar 会新建带固定的窗口），自毁
                    root = self._root_host_of(url_str)
                    print(f"[DBG] df 新窗口访问 {new_host}，"
                          f"root={root} is_pinned="
                          f"{pinned_store.is_pinned(root) if root else False}")
                    if root and pinned_store.is_pinned(root):
                        print("[DBG] 走分支 2：转给 bar（新建带固定）+ 自毁")
                        self.request_url(url_str)
                        if not self._has_loaded_once:
                            QTimer.singleShot(100, self.close)
                        return

                    print("[DBG] 走分支 3：自己加载")
                    # 3. 都没有 → 默认窗口自己加载，获得 host
                    if self._pending_input_host:
                        self._add_host(self._pending_input_host, primary=False)
                    self._add_host(new_host, primary=True)
                    self._pending_input_host = ""
                    if not is_redirect:
                        self._current_url = url_str
                    self.title_bar.set_address(
                        _pretty_url_for_address_bar(url_str)
                    )
                elif self._matches_host(new_host):
                    if not is_redirect:
                        self._current_url = url_str
                    if new_host not in self._hosts:
                        self._add_host(new_host, primary=False)
                    self.title_bar.set_address(
                        _pretty_url_for_address_bar(url_str)
                    )
                else:
                    self._restore_address_bar()
                    self.request_url(url_str)

                if self._popup is not None and self._has_root_host(new_host):
                    self._popup.append_url(url_str)
                    self._popup.set_current_url(url_str)
            except Exception as e:
                print(f"[window] _on_url_settled 回调异常: {e}")
            finally:
                try:
                    self._update_star_state()
                except Exception:
                    pass

        try:
            wv.eval_js("location.href", _cb)
        except Exception as e:
            print(f"[window] _on_url_settled eval_js 失败: {e}")

    def _restore_address_bar(self):
        wv = self.web_view
        if wv is None:
            return

        def _cb(real_url):
            try:
                url_str = _clean_js_url(real_url)
                if url_str and url_str != "about:blank":
                    self.title_bar.set_address(
                        _pretty_url_for_address_bar(url_str)
                    )
            except Exception:
                pass

        try:
            wv.eval_js("location.href", _cb)
        except Exception:
            pass

    # =========================================================
    # < / > ：popup 列表上下
    # =========================================================
    def _prev_url(self):
        if self._popup is None:
            return
        urls = self._popup.urls()
        if not urls:
            return
        cur = self._popup.current_url()
        try:
            idx = urls.index(cur) if cur else 0
        except ValueError:
            idx = 0
        idx = max(0, idx - 1)
        self._on_popup_url_selected(urls[idx])

    def _next_url(self):
        if self._popup is None:
            return
        urls = self._popup.urls()
        if not urls:
            return
        cur = self._popup.current_url()
        try:
            idx = urls.index(cur) if cur else -1
        except ValueError:
            idx = -1
        idx = min(len(urls) - 1, idx + 1)
        self._on_popup_url_selected(urls[idx])

    # =========================================================
    # 个性化
    # =========================================================
    def apply_personalize(self, color):
        border, inner = Theme.apply_theme(color)
        self.title_bar.apply_theme_color(border)
        if hasattr(self, "corner_mask"):
            self.corner_mask.bg_color = border
            self.corner_mask.update()

        if self._mode != "search":
            s = load_window_settings(self._mode, self._window_id)
            s["theme_color"] = QColor(color).name()
            save_window_settings(self._mode, self._window_id, s)

        self._broadcast_config_changed()
        self.update()

    def apply_background_image(self, path, images=None):
        if path:
            real = resolve_path(path)
            pm = QPixmap(real)
            if pm.isNull():
                return
            self._bg_path = real
            self._bg_pixmap = pm
        else:
            self._bg_path = ""
            self._bg_pixmap = None

        if self._mode != "search":
            s = load_window_settings(self._mode, self._window_id)
            if images is not None:
                # 存盘时把内置资源转回 {RES}/... 形式，
                # 免得写死绝对路径、换安装位置就失效
                s["background_images"] = [to_stored_path(p) for p in images]
            s["background_current"] = to_stored_path(path) if path else ""
            save_window_settings(self._mode, self._window_id, s)

        self._broadcast_config_changed()
        self.update()

    def current_theme_color(self):
        s = load_window_settings(self._mode, self._window_id)
        return QColor(s.get("theme_color", "#d0d0d0"))

    def current_background_images(self):
        s = load_window_settings(self._mode, self._window_id)
        return list(s.get("background_images", []))

    def current_background_image(self):
        s = load_window_settings(self._mode, self._window_id)
        return s.get("background_current", "")

    # =========================================================
    # 绘制
    # =========================================================
    def _outline_color(self):
        base = QColor(Theme.BG_COLOR)
        return QColor(
            255 - base.red(),
            255 - base.green(),
            255 - base.blue(),
            self.OUTLINE_ALPHA,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        b = self.BORDER
        radius = 0 if self.isMaximized() else self.RADIUS

        painter.setBrush(self._outline_color())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), radius, radius)

        inner = QRectF(
            b, b,
            self.width() - 2 * b,
            self.height() - 2 * b,
        )
        inner_radius = max(0, radius - b)
        painter.setBrush(Theme.BG_COLOR)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(inner, inner_radius, inner_radius)

        try:
            x = self.SIDE_MARGIN + b
            y = self.TOP_BAR_HEIGHT + self.WEB_TOP_GAP + b
            w = self.width() - 2 * self.SIDE_MARGIN - 2 * b
            h = self.height() - y - self.BOTTOM_MARGIN - b

            if w <= 0 or h <= 0:
                return

            rect = QRectF(x, y, w, h)
            r = QRect(int(x), int(y), int(w), int(h))

            if self._bg_pixmap is not None and not self._bg_pixmap.isNull():
                scaled = self._bg_pixmap.scaled(
                    r.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation,
                )
                sx = (scaled.width() - r.width()) // 2
                sy = (scaled.height() - r.height()) // 2
                cropped = scaled.copy(sx, sy, r.width(), r.height())

                path = QPainterPath()
                path.addRoundedRect(rect, self.WEB_RADIUS, self.WEB_RADIUS)
                painter.setClipPath(path)
                painter.drawPixmap(r.topLeft(), cropped)
                painter.setClipping(False)
            else:
                painter.setBrush(Theme.WEB_PLACEHOLDER_COLOR)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(rect, self.WEB_RADIUS, self.WEB_RADIUS)
        except RuntimeError:
            pass

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if hasattr(self, "title_bar"):
                self.title_bar.update_max_icon()
                self.title_bar.update()
        elif event.type() == QEvent.Type.ActivationChange:
            # 窗口被激活（任务栏点击等）→ 若在屏幕外就移回来
            if self.isActiveWindow() and getattr(self, "_offscreen", False):
                self._restore_from_offscreen()
        super().changeEvent(event)

    # =========================================================
    # 几何
    # =========================================================
    def _center_input_box(self):
        w = self.input_box.width()
        h = self.input_box.height()
        self.input_box.move(
            (self.width() - w) // 2,
            (self.height() - h) // 2,
        )

    def _update_web_view_geometry(self):
        if self._resizing:
            return
        self._resizing = True
        try:
            wv = self.web_view
            if wv is None:
                return

            b = self.BORDER
            x = self.SIDE_MARGIN + b
            y = self.TOP_BAR_HEIGHT + self.WEB_TOP_GAP + b
            w = self.width() - 2 * self.SIDE_MARGIN - 2 * b
            h = self.height() - y - self.BOTTOM_MARGIN - b

            if w <= 0 or h <= 0:
                return

            wv.setGeometry(x, y, w, h)
        except RuntimeError:
            pass
        finally:
            self._resizing = False

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "title_bar"):
            self.title_bar.setGeometry(
                self.BORDER, self.BORDER,
                self.width() - 2 * self.BORDER,
                self.TOP_BAR_HEIGHT,
            )
        if self.input_box.isVisible():
            self._center_input_box()
        wv = self.web_view
        if wv is not None and wv.isVisible():
            self._update_web_view_geometry()
            self.apply_web_view_round()
        self._refresh_popup_visibility()

        try:
            if getattr(self, "_pw_panel", None) is not None:
                password_hook._relayout(self)
        except Exception:
            pass

    # =========================================================
    # 输入
    # =========================================================
    def show_input_box(self):
        wv = self.web_view
        if wv is not None:
            wv.hide()
        self.input_box.show()
        self._center_input_box()
        self.title_bar.set_browsing_mode(False)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.show_input_box()
        else:
            super().keyPressEvent(event)

    def visit(self):
        text = self.input_box.text()
        if not text:
            return None

        # 有当前引擎 → 一律搜索
        if self._current_engine:
            url = self._build_search_url(text)
            if url:
                self.handle_url(url)
                return url
            return None

        # 无引擎 → 现有逻辑
        if self._is_url(text):
            if not text.startswith(("http://", "https://")):
                text = "https://" + text
            self.handle_url(text)
            return text
        return None

    def visit_url(self, text):
        if not text:
            return None

        if self._current_engine:
            url = self._build_search_url(text)
            if url:
                self.handle_url(url)
                return url
            return None

        if self._is_url(text):
            if not text.startswith(("http://", "https://")):
                text = "https://" + text
            self.handle_url(text)
            return text
        return None

    def _is_url(self, text):
        if text.startswith("http://") or text.startswith("https://"):
            return True
        if " " not in text and "." in text:
            return True
        return False

    # =========================================================
    # 收藏
    # =========================================================
    def _on_star_left_clicked(self):
        """左键点星：切换收藏。"""
        url = self._current_url or ""
        if not url:
            return

        try:
            from favorites_store import is_favorited, add, remove
        except Exception as e:
            print("[window] 导入 favorites_store 失败:", e)
            return

        if is_favorited(url):
            # 已收藏 → 取消
            try:
                remove(url)
            except Exception as e:
                print("[window] 取消收藏失败:", e)
            self._update_star_state()
            self._broadcast_favorite_changed(url)
        else:
            # 未收藏 → 收藏（异步抓 title）
            self._add_favorite_with_title(url)

    def _broadcast_favorite_changed(self, url):
        """广播收藏变化给所有窗口。"""
        try:
            from ipc import broadcast, MSG_FAVORITE_CHANGED
            broadcast(
                MSG_FAVORITE_CHANGED,
                (url or "").encode("utf-8"),
            )
        except Exception as e:
            print("[window] 广播收藏变化失败:", e)

    def _add_favorite_with_title(self, url):
        """收藏当前 URL，异步拿 title。"""
        def _do_add(title):
            try:
                from favorites_store import add
                add(url, title or url)
            except Exception as e:
                print("[window] 收藏失败:", e)
            self._update_star_state()
            self._broadcast_favorite_changed(url)

        wv = self.web_view
        if wv is None or not wv.isVisible():
            _do_add("")
            return

        def _cb(raw_title):
            try:
                title = _clean_js_url(raw_title)
                _do_add(title or "")
            except Exception:
                _do_add("")

        try:
            wv.eval_js("document.title", _cb)
        except Exception:
            _do_add("")

    def _update_star_state(self, url=None):
        """更新星按钮的颜色。url 为空时用 _current_url。"""
        if not url:
            url = self._current_url or ""
        on = False
        if url:
            try:
                from favorites_store import is_favorited
                on = is_favorited(url)
            except Exception:
                on = False

        try:
            if hasattr(self, "title_bar") and hasattr(self.title_bar, "star_btn"):
                self.title_bar.star_btn.set_on(on)
        except Exception:
            pass

    def _on_star_right_clicked(self):
        """右键点星：弹收藏菜单。"""
        if self._fav_menu is not None:
            try:
                self._fav_menu.hide()
                self._fav_menu.deleteLater()
            except Exception:
                pass
            self._fav_menu = None
            return

        try:
            from favorites_menu import FavoritesMenu
            menu = FavoritesMenu(self)
        except Exception as e:
            print("[window] 创建收藏菜单失败:", e)
            return

        menu.url_selected.connect(self._on_favorite_selected)
        menu.url_closed.connect(self._on_favorite_closed)

        # 定位到星按钮下方（全局坐标）
        try:
            btn = self.title_bar.star_btn
            global_pos = btn.mapToGlobal(QPoint(0, btn.height() + 4))
        except Exception:
            global_pos = QPoint(0, 0)

        self._fav_menu = menu
        menu.popup_at(global_pos)

    def _on_favorite_selected(self, url):
        """点收藏条目（× 以外）→ 交给当前窗口访问。"""
        if not url:
            return
        self._fav_menu = None
        # 走 handle_url：自己的加载，不是的转 bar
        try:
            self.handle_url(url)
        except Exception as e:
            print("[window] 访问收藏失败:", e)

    def _on_favorite_closed(self, url):
        """菜单里删了一条收藏。"""
        self._update_star_state()
        # 广播给所有窗口
        self._broadcast_favorite_changed(url)

    # =========================================================
    # 搜索引擎
    # =========================================================
    def _build_search_url(self, query):
        """把当前引擎 + query 拼成 URL。"""
        try:
            from search_engines import build_search_url
            return build_search_url(self._current_engine, query)
        except Exception as e:
            print("[window] 拼搜索 URL 失败:", e)
            return ""

    def _on_engine_btn_clicked(self):
        """点左侧引擎按钮 → 弹透明长条。"""
        if self._engine_picker is not None:
            try:
                self._engine_picker.hide()
                self._engine_picker.deleteLater()
            except Exception:
                pass
            self._engine_picker = None
            return

        try:
            from search_engines import load_all
            engines = load_all()
        except Exception as e:
            print("[window] 读引擎列表失败:", e)
            engines = []

        if not engines:
            from i18n import t as _t
            try:
                box = QMessageBox(self)
                box.setWindowTitle(_t("app.title"))
                box.setText(_t("engine.no_engine"))
                box.setIcon(QMessageBox.Icon.Information)
                box.exec()
            except Exception as e:
                print("[window] 弹无引擎提示失败:", e)
            return

        # 顶部插入"默认"项（无引擎模式）
        engines_with_default = [{"_default": True, "abbr": "", "url": ""}]
        engines_with_default.extend(engines)

        try:
            from input_box import EnginePicker
            picker = EnginePicker(engines_with_default, self)
        except Exception as e:
            print("[window] 创建引擎长条失败:", e)
            return

        picker.selected.connect(self._on_engine_selected)

        # 把本地已有的 favicon 先塞进长条（不等网络）
        try:
            from search_icons import load_icon as _load_eng_icon
            for eng in engines:
                if eng.get("_default"):
                    continue
                pm = _load_eng_icon(eng)
                if pm is not None and not pm.isNull():
                    picker.set_item_favicon(eng.get("url", ""), pm)
        except Exception as e:
            print("[window] 读本地引擎图标失败:", e)

        # 定位到按钮下方（相对 window 局部坐标）
        btn = self.input_box.engine_button()
        try:
            # 按钮左下角在 window 坐标系里的位置
            btn_bottom_left = btn.mapTo(self, QPoint(0, btn.height()))
            local_pos = QPoint(
                btn_bottom_left.x() - 6,
                btn_bottom_left.y() + 14,
            )
        except Exception:
            local_pos = QPoint(0, 0)

        self._engine_picker = picker
        picker.popup_at(local_pos)

    def _on_engine_selected(self, engine):
        """用户从长条里选了引擎（或默认）。"""
        if engine and engine.get("_default"):
            self._clear_engine()
        else:
            self._set_engine(engine)

        # 关长条
        if self._engine_picker is not None:
            try:
                self._engine_picker.hide()
                self._engine_picker.deleteLater()
            except Exception:
                pass
            self._engine_picker = None

    def _clear_engine(self):
        """回到无引擎模式。"""
        self._current_engine = None
        try:
            btn = self.input_box.engine_button()
            btn.clear_engine()
        except Exception as e:
            print("[window] 清引擎失败:", e)

    def _set_engine(self, engine):
        """切换当前引擎。同步按钮图标 + 异步抓 favicon。"""
        if not engine or not isinstance(engine, dict):
            return
        self._current_engine = engine

        url = engine.get("url", "") or ""
        abbr = (engine.get("abbr") or "").upper()

        try:
            btn = self.input_box.engine_button()
            btn.set_pixmap(None)     # 清掉旧 favicon
            btn.set_abbr(abbr)       # 先显示字母
        except Exception:
            pass

        # 异步抓 favicon
        if url:
            self._fetch_engine_favicon(url)

    def _fetch_engine_favicon(self, engine_url):
        """给单个引擎抓 favicon。

        本地有直接用；没有走 search_icons 异步抓。
        """
        if not engine_url:
            return

        # 内存缓存命中
        if engine_url in self._engine_favicon_cache:
            pm = self._engine_favicon_cache[engine_url]
            if pm is not None and not pm.isNull():
                self._apply_engine_favicon(pm)
                return

        eng = self._current_engine or {}
        if eng.get("url") != engine_url:
            return

        try:
            from search_icons import fetch_icon
            fetch_icon(
                eng,
                lambda e, pm: self._on_engine_icon_fetched(e, pm),
                parent=self,
            )
        except Exception as e:
            print("[window] 抓引擎 favicon 失败:", e)

    def _apply_engine_favicon(self, pm):
        """把 favicon 画到引擎按钮上。"""
        try:
            btn = self.input_box.engine_button()
            btn.set_pixmap(pm)
        except Exception as e:
            print("[window] 设置引擎 favicon 失败:", e)

    def _prefetch_engine_icons(self):
        """窗口启动后，后台批量抓所有引擎的 favicon。"""
        try:
            from search_engines import load_all
            from search_icons import fetch_all
            engines = load_all()
        except Exception as e:
            print("[window] 预抓引擎图标读列表失败:", e)
            return

        if not engines:
            return

        def _on_one(engine, pm):
            self._on_engine_icon_fetched(engine, pm)

        try:
            fetch_all(engines, _on_one, parent=self)
        except Exception as e:
            print("[window] 预抓引擎图标失败:", e)

    def _on_engine_icon_fetched(self, engine, pm):
        """单个引擎图标抓完。

        * 更新长条里对应的图标（如果长条在显示）
        * 更新左侧按钮（如果这个引擎是当前引擎）
        * 缓存到内存
        """
        if not isinstance(engine, dict):
            return
        url = engine.get("url", "")

        # 缓存
        if pm is not None and not pm.isNull() and url:
            self._engine_favicon_cache[url] = pm

        # 更新长条
        picker = self._engine_picker
        if picker is not None and pm is not None and not pm.isNull():
            try:
                picker.set_item_favicon(url, pm)
            except Exception as e:
                print("[window] 更新长条图标失败:", e)

        # 更新左侧按钮（如果当前引擎就是它）
        cur_url = (self._current_engine or {}).get("url", "")
        if cur_url and cur_url == url and pm is not None and not pm.isNull():
            self._apply_engine_favicon(pm)

    # =========================================================
    # 拖拽
    # =========================================================
    def _maybe_close_engine_picker(self, event):
        """点 window 上别的地方时，关掉引擎长条。"""
        if self._engine_picker is None:
            return
        try:
            local = event.position().toPoint()
            picker_rect = self._engine_picker.geometry()
            if picker_rect.contains(local):
                return
            btn = self.input_box.engine_button()
            btn_rect = QRect(btn.mapTo(self, QPoint(0, 0)), btn.size())
            if btn_rect.contains(local):
                return
        except Exception:
            pass

        try:
            self._engine_picker.hide()
            self._engine_picker.deleteLater()
        except Exception:
            pass
        self._engine_picker = None

    def _maybe_close_favorites_menu(self, event):
        """独立窗口模式下，由 focusOut 自己关，这里空操作。"""
        pass

    def mousePressEvent(self, event):
        # 点 window 其他地方 → 关引擎长条
        self._maybe_close_engine_picker(event)

        if event.button() == Qt.MouseButton.LeftButton and not self.isMaximized():
            edge = self._get_edge(event.position().toPoint())
            if edge:
                self._resize_edge = edge
                self._start_pos = event.globalPosition().toPoint()
                self._start_geo = self.geometry()

    def mouseMoveEvent(self, event):
        if self.isMaximized():
            return

        edge = self._get_edge(event.position().toPoint())
        self._update_cursor(edge)

        if (event.buttons() & Qt.MouseButton.LeftButton
                and self._resize_edge
                and self._start_geo):
            delta = event.globalPosition().toPoint() - self._start_pos
            self._do_resize(self._resize_edge, delta)

    def mouseReleaseEvent(self, event):
        self._resize_edge = None
        self._start_geo = None
        self._start_pos = None

    def _get_edge(self, pos):
        M = self.RESIZE_MARGIN
        C = self.CORNER_MARGIN

        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        edges = []

        if x < M or (x < C and (y < C or y > h - C)):
            edges.append("l")
        if x > w - M or (x > w - C and (y < C or y > h - C)):
            edges.append("r")
        if y < M or (y < C and (x < C or x > w - C)):
            edges.append("t")
        if y > h - M or (y > h - C and (x < C or x > w - C)):
            edges.append("b")

        return "".join(edges) if edges else None

    def _update_cursor(self, edge):
        if not edge:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif edge in ("l", "r"):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge in ("t", "b"):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif edge in ("lt", "rb"):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in ("rt", "lb"):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def _do_resize(self, edge, delta):
        geo = self._start_geo
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

        if "l" in edge:
            x += delta.x()
            w -= delta.x()
        if "r" in edge:
            w += delta.x()
        if "t" in edge:
            y += delta.y()
            h -= delta.y()
        if "b" in edge:
            h += delta.y()

        if w >= self.minimumWidth() and h >= self.minimumHeight():
            self.setGeometry(x, y, w, h)

    # =========================================================
    # 生命周期
    # =========================================================
    def closeEvent(self, event):
        # 关掉引擎长条
        try:
            if self._engine_picker is not None:
                self._engine_picker.close_picker()
                self._engine_picker = None
        except Exception:
            pass

        # 关掉收藏菜单
        try:
            if self._fav_menu is not None:
                self._fav_menu._close()
                self._fav_menu = None
        except Exception:
            pass

        # 关窗保存固定记忆
        try:
            self._save_pinned_memory()
        except Exception:
            pass

        try:
            self._dom_monitor.stop()
        except Exception:
            pass

        try:
            if self._taskbar_timer.isActive():
                self._taskbar_timer.stop()
        except Exception:
            pass

        try:
            if self._popup is not None:
                self._popup.hide()
        except Exception:
            pass

        try:
            self._url_poll_timer.stop()
        except Exception:
            pass

        try:
            self._favicon_poll.stop()
        except Exception:
            pass

        try:
            if hasattr(self, "_round_timer"):
                self._round_timer.stop()
        except Exception:
            pass

        for _url, proc in list(self._download_workers.items()):
            try:
                proc.terminate()
                if not proc.waitForFinished(1000):
                    proc.kill()
            except Exception:
                pass
        self._download_workers.clear()

        try:
            if self._web_view is not None:
                self._web_view.close()
                self._web_view.setParent(None)
                self._web_view.deleteLater()
        except Exception:
            pass
        self._web_view = None

        try:
            if (hasattr(self, "title_bar")
                    and self.title_bar._personalize_dialog is not None):
                self.title_bar._personalize_dialog.close()
                self.title_bar._personalize_dialog = None
        except Exception:
            pass

        try:
            popup = getattr(
                getattr(self, "title_bar", None), "_popup", None
            )
            if popup is not None:
                try:
                    popup.close()
                except Exception:
                    pass
                self.title_bar._popup = None
        except Exception:
            pass

        try:
            t = getattr(self, "_pw_hide_timer", None)
            if t is not None:
                t.stop()
                self._pw_hide_timer = None
        except Exception:
            pass

        try:
            if getattr(self, "_pw_panel", None) is not None:
                self._pw_panel.hide()
                self._pw_panel.setParent(None)
                self._pw_panel.deleteLater()
                self._pw_panel = None
        except Exception:
            pass

        try:
            self._ipc_server.stop()
        except Exception:
            pass
        super().closeEvent(event)


def main():
    import traceback

    def _excepthook(exc_type, exc_value, exc_tb):
        traceback.print_exception(exc_type, exc_value, exc_tb)

    sys.excepthook = _excepthook

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="default",
                        choices=["default", "search", "custom"])
    parser.add_argument("--id", default="df-0")
    parser.add_argument("--host", default="")
    parser.add_argument("--url", default="")
    parser.add_argument("--pinned-url", default="")
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
        print("[window] 设应用图标失败:", e)

    try:
        from settings_backend import SettingsBackend
        i18n_load(SettingsBackend().get_language())
    except Exception as e:
        print("[window] 加载语言失败:", e)

    # 任务栏分开：本进程独立 AppUserModelID
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            f"MyBrowser.Window.{args.id}"
        )
    except Exception as e:
        print("[window] 设置 AppUserModelID 失败:", e)

    w = RoundedWindow(
        mode=args.mode,
        window_id=args.id,
        host=args.host,
        start_url=args.url,
        pinned_url=args.pinned_url,
    )

    # 窗口默认图标
    try:
        from window_icon import default_icon
        _di = default_icon()
        if not _di.isNull():
            w.setWindowIcon(_di)
    except Exception as e:
        print("[window] 设窗口默认图标失败:", e)

    w.show()

    # 启动后延迟置顶 + 抢焦点（等窗口完全创建）
    def _bring_to_front():
        try:
            w.raise_()
            w.activateWindow()
            set_topmost(int(w.winId()), True)
            QTimer.singleShot(800, lambda: set_topmost(int(w.winId()), False))
        except Exception as e:
            print("[window] bring_to_front 失败:", e)

    QTimer.singleShot(300, _bring_to_front)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

### component\window_icon.py (大小: 3941 | 修改时间: 2026-10-03 02:25:55 | 权限: 666)

```
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
```

### defaults\favorites.json (大小: 2 | 修改时间: 2026-10-02 20:43:30 | 权限: 666)

```
[]
```

### defaults\passwords.json (大小: 2 | 修改时间: 2026-10-02 13:51:00 | 权限: 666)

```
{}
```

### defaults\search_engines.json (大小: 278 | 修改时间: 2026-10-02 14:37:38 | 权限: 666)

```
{
  "engines": [
    {
      "abbr": "BI",
      "url": "https://www.bing.com/search?q=%s"
    },
    {
      "abbr": "GO",
      "url": "https://www.google.com/search?q=%s"
    },
    {
      "abbr": "BA",
      "url": "https://www.baidu.com/s?wd=%s"
    }
  ]
}
```

### defaults\settings.json (大小: 1777 | 修改时间: 2026-10-03 12:51:33 | 权限: 666)

```
{
    "windows":  {
                    "default":  {
                                    "theme_color":  "#2b2b2b",
                                    "background_images":  [
                                                              "{RES}/assets/backgrounds/spaceship.jpg"
                                                          ],
                                    "background_current":  "{RES}/assets/backgrounds/spaceship.jpg"
                                }
                },
    "env":  {
                "language":  "zh-CN",
                "user_agent":  "",
                "proxy":  "",
                "incognito":  false,
                "user_data_folder":  "",
                "download_dir":  "",
                "download_notify":  true,
                "scan_downloads":  true,
                "js_enabled":  true,
                "context_menu":  false,
                "hotkeys":  false,
                "devtools":  false,
                "autofill":  false,
                "password_autosave":  false,
                "tracking_prevention":  true,
                "tracking_level":  1,
                "smartscreen":  true,
                "block_third_party_cookies":  false,
                "insecure_content_allowed":  false,
                "permission_camera":  0,
                "permission_mic":  0,
                "permission_geo":  0,
                "permission_notify":  0,
                "block_redirect":  false,
                "block_popup":  true,
                "block_ad":  false,
                "save_cookie":  true,
                "save_history":  true,
                "history_days":  30,
                "whitelist":  [

                              ]
            }
}
```

### installer\build_all.py (大小: 9851 | 修改时间: 2026-10-03 10:56:13 | 权限: 666)

```
# -*- coding: utf-8 -*-
r"""一键构建 NWbrowser 1.0.0 安装包，输出到桌面。

串起四步：
    1. PyInstaller 构建应用（onedir）
    2. 校验包内图标
    3. 组装载荷（exe + _internal + 许可证/声明/README + _defaults 默认数据）
    4. 构建卸载器 + 安装器

产物：桌面\NWbrowser-1.0.0-Setup.exe 以及解包目录 桌面\NWbrowser\
"""

import os
import shutil
import subprocess
import sys
import zipfile

WS = r"<项目根>"
ROOT = os.path.join(WS, "browser_project")
LIB = os.path.join(ROOT, "library")
INST = os.path.join(WS, "installer")
OUT = os.path.join(WS, "NWbrowser v1.0.0")
DESKTOP = os.path.join(os.environ["USERPROFILE"], "Desktop")
APP = os.path.join(DESKTOP, "NWbrowser")

SETUP_NAME = "NWbrowser-1.0.0-Setup"

DOCS = ["LICENSE", "THIRD-PARTY-NOTICES.txt", "README.md"]
DEFAULTS = ["settings.json", "search_engines.json", "favorites.json",
            "passwords.json"]


def env_for_build():
    e = dict(os.environ)
    e["PYTHONPATH"] = ";".join([
        LIB, os.path.join(LIB, "PyQt6"), os.path.join(LIB, "qtwebview2"),
        os.path.join(LIB, "pywin32"), os.path.join(LIB, "pywin32", "win32"),
        os.path.join(LIB, "pywin32", "win32", "lib"),
        os.path.join(LIB, "browser-oxide"),
    ])
    e["PYTHONIOENCODING"] = "utf-8"
    return e


def run(cmd, cwd, env=None, label=""):
    print("    $ %s" % " ".join(str(c) for c in cmd[:4]) + (" ..." if len(cmd) > 4 else ""))
    p = subprocess.run(cmd, cwd=cwd, env=env,
                       capture_output=True, text=True, errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    for line in out.splitlines():
        if any(k in line for k in ("ERROR", "Error", "error:", "Traceback",
                                   "Build complete", "PermissionError",
                                   "拒绝访问")):
            print("      " + line.strip())
    if p.returncode != 0:
        raise RuntimeError("%s 失败 (exit=%d)" % (label or cmd[0], p.returncode))
    return out


def kill_browser():
    subprocess.run(["taskkill", "/f", "/im", "NWbrowser.exe"],
                   capture_output=True)
    import time
    time.sleep(2)


def rmtree(path):
    if not os.path.isdir(path):
        return
    for i in range(6):
        try:
            shutil.rmtree(path)
            return
        except Exception as e:
            print("    删除重试 %d: %s" % (i + 1, e))
            kill_browser()
            # 清只读属性后重试
            subprocess.run(["cmd", "/c", "attrib", "-r", "-h", "-s",
                            path + "\\*", "/s", "/d"], capture_output=True)
    if os.path.isdir(path):
        raise RuntimeError("删不掉目录: %s" % path)


def step1_build_app():
    print("[1/4] 构建应用（PyInstaller onedir）")
    kill_browser()
    rmtree(APP)
    rmtree(os.path.join(ROOT, "build"))
    for d in ("__pycache__",):
        for base, dirs, _f in os.walk(ROOT):
            if d in dirs:
                try:
                    shutil.rmtree(os.path.join(base, d))
                except Exception:
                    pass

    run([sys.executable, "-m", "PyInstaller", "NWbrowser.spec", "--noconfirm",
         "--distpath", DESKTOP, "--workpath", os.path.join(ROOT, "build")],
        cwd=ROOT, env=env_for_build(), label="PyInstaller")

    if not os.path.isfile(os.path.join(APP, "NWbrowser.exe")):
        raise RuntimeError("没有生成 NWbrowser.exe")

    # 文档随程序发放
    for name in DOCS:
        src = os.path.join(ROOT, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(APP, name))
            print("    + %s" % name)
        else:
            print("    ! 缺少 %s" % name)


def step2_verify_icon():
    print("[2/4] 校验包内图标")
    p = os.path.join(APP, "_internal", "data", "icon.ico")
    if not os.path.isfile(p):
        print("    ! 找不到 _internal/data/icon.ico")
        return
    size = os.path.getsize(p)
    print("    icon.ico = %d 字节" % size)


def step3_payload():
    print("[3/4] 组装载荷")
    stage = os.path.join(INST, "payload")
    rmtree(stage)
    os.makedirs(os.path.join(stage, "_defaults"), exist_ok=True)

    shutil.copy2(os.path.join(APP, "NWbrowser.exe"), stage)
    for name in DOCS:
        src = os.path.join(APP, name)
        if os.path.isfile(src):
            shutil.copy2(src, stage)
    subprocess.run(["robocopy", os.path.join(APP, "_internal"),
                    os.path.join(stage, "_internal"), "/e", "/nfl", "/ndl",
                    "/njh", "/njs", "/np"], capture_output=True)

    d = os.path.join(stage, "_defaults")
    for name in DEFAULTS:
        src = os.path.join(ROOT, name)
        if os.path.isfile(src):
            shutil.copy2(src, d)
    icons = os.path.join(ROOT, "userdata", "search_icons")
    if os.path.isdir(icons):
        os.makedirs(os.path.join(d, "userdata", "search_icons"), exist_ok=True)
        for n in os.listdir(icons):
            shutil.copy2(os.path.join(icons, n),
                         os.path.join(d, "userdata", "search_icons", n))
    os.makedirs(os.path.join(d, "fixed"), exist_ok=True)

    zip_path = os.path.join(INST, "payload.zip")
    if os.path.isfile(zip_path):
        os.remove(zip_path)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        # 先显式写入所有目录条目（含空目录）。
        # zipfile.write() 逐个文件写时不会为**空目录**留下记录，
        # 而 _defaults/fixed/ 就是空的 —— 少了这一步，装完就缺 fixed\ 目录。
        for base, dirs, files in os.walk(stage):
            for d in dirs:
                full = os.path.join(base, d)
                z.write(full, os.path.relpath(full, stage) + "/")
        for base, _dirs, files in os.walk(stage):
            for f in files:
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, stage))

    empty_dirs = []
    for base, dirs, files in os.walk(stage):
        for d in dirs:
            full = os.path.join(base, d)
            if not os.listdir(full):
                empty_dirs.append(os.path.relpath(full, stage))

    print("    payload.zip = %.1f MB（%d 个文件，%d 个空目录%s）"
          % (os.path.getsize(zip_path) / 1048576,
             sum(len(f) for _b, _d, f in os.walk(stage)),
             len(empty_dirs),
             ("：" + ", ".join(empty_dirs)) if empty_dirs else ""))
    return zip_path


def step4_installer(zip_path):
    print("[4/4] 构建卸载器 + 安装器")
    # 卸载器
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--noconsole",
         "--onefile", "--name", "uninstall",
         "--distpath", os.path.join(INST, "dist"),
         "--workpath", os.path.join(INST, "build_uninst"),
         "--specpath", os.path.join(INST, "build_uninst"),
         "--icon", os.path.join(INST, "setup.ico"),
         "--version-file", os.path.join(INST, "uninstall_version_info.txt"),
         "--exclude-module", "PyQt5", "--exclude-module", "PyQt6",
         "--exclude-module", "tkinter", "--exclude-module", "numpy",
         "--exclude-module", "PIL",
         os.path.join(INST, "uninstall.py")],
        cwd=WS, env=env_for_build(), label="uninstall")

    # 安装器
    os.makedirs(OUT, exist_ok=True)
    for n in os.listdir(OUT):
        if n.endswith(".exe"):
            os.remove(os.path.join(OUT, n))
    run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--noconsole",
         "--onefile", "--name", SETUP_NAME,
         "--distpath", OUT,
         "--workpath", os.path.join(INST, "build_setup"),
         "--specpath", os.path.join(INST, "build_setup"),
         "--icon", os.path.join(INST, "setup.ico"),
         "--version-file", os.path.join(INST, "setup_version_info.txt"),
         "--add-data", "%s;." % zip_path,
         "--add-data", "%s;." % os.path.join(INST, "dist", "uninstall.exe"),
         "--add-data", "%s;." % os.path.join(INST, "setup.ico"),
         "--add-data", "%s;." % os.path.join(INST, "setup_header.png"),
         "--add-data", "%s;." % os.path.join(ROOT, "LICENSE"),
         "--add-data", "%s;." % os.path.join(ROOT, "THIRD-PARTY-NOTICES.txt"),
         "--hidden-import", "win32com", "--hidden-import", "win32com.client",
         "--hidden-import", "win32timezone",
         "--hidden-import", "PyQt5.QtCore", "--hidden-import", "PyQt5.QtGui",
         "--hidden-import", "PyQt5.QtWidgets",
         "--exclude-module", "PyQt5.QtQml", "--exclude-module", "PyQt5.QtQuick",
         "--exclude-module", "PyQt5.QtMultimedia",
         "--exclude-module", "PyQt5.QtWebEngineWidgets",
         "--exclude-module", "PyQt5.QtNetwork", "--exclude-module", "tkinter",
         "--exclude-module", "numpy", "--exclude-module", "PIL",
         "--exclude-module", "PyQt6",
         os.path.join(INST, "setup.py")],
        cwd=WS, env=env_for_build(), label="setup")

    exe = os.path.join(OUT, SETUP_NAME + ".exe")
    if not os.path.isfile(exe):
        raise RuntimeError("没有生成安装包")
    return exe


def main():
    print("=" * 66)
    print(" 构建 NWbrowser 1.0.0 安装包")
    print("=" * 66)
    step1_build_app()
    step2_verify_icon()
    z = step3_payload()
    exe = step4_installer(z)

    # 复制一份到桌面
    desk_exe = os.path.join(DESKTOP, SETUP_NAME + ".exe")
    shutil.copy2(exe, desk_exe)

    import hashlib
    h = hashlib.sha256(open(exe, "rb").read()).hexdigest().upper()
    print()
    print("=" * 66)
    print(" 完成")
    print("=" * 66)
    print("  解包目录 : %s" % APP)
    print("  安装包   : %s  (%.1f MB)" % (exe, os.path.getsize(exe) / 1048576))
    print("  桌面副本 : %s" % desk_exe)
    print("  SHA256   : %s" % h)
    return 0


if __name__ == "__main__":
    sys.exit(main())

```

### installer\make_icons.py (大小: 8297 | 修改时间: 2026-10-03 03:57:59 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""把单张 128x128 的 icon.ico 补成多尺寸高清 ICO。

为什么要这么做
--------------
原来的 .ico 只有**一张 128x128**。Windows 在托盘要 16、资源管理器要 32/48、
属性对话框要 32 —— 全都是现场硬缩，细线条必然出锯齿。

原则（重要）
------------
1. **原始 128x128 那一帧原样保留，一个像素都不动** —— 大尺寸显示零损失
2. 补小尺寸（16/20/24/32/40/48/64/96），每个尺寸都从超采样基准独立重采样
3. **不做任何 alpha 增益/加粗** —— 加了会让小图变粗变糊
4. 不上采样到 256（源图只有 128，放大只会更糊）

为什么必须补小尺寸（实测证据）
------------------------------
只放一张 128 的话，Windows 在资源管理器/开始菜单要 32x32、托盘要 16x16 时，
只能拿 128 **硬缩**，用的还是快速滤波 —— 细线条会碎成锯齿。
对比实验（同一台机器，都是 Windows 自己渲染的 32x32）：

    uninstall.exe（多尺寸 ICO，含 32 帧）  -> 平滑
    NWbrowser.exe（单帧 128）              -> 明显锯齿

所以：128 原样留 + 小尺寸补帧，两个目标都满足。
尺寸覆盖 Windows 各档显示：16(托盘/小图标) 20 24 32(列表/属性) 40 48(中图标)
64 96(大图标) 128(原图)。

超采样：先把 128 用**预乘 alpha**放大到 1024，再从 1024 缩到目标尺寸；
预乘可以避免缩放时边缘发灰出暗边。

输出用经典 32bpp BMP 帧（兼容性最好，和原文件格式一致）。
"""

import os
import struct
import sys
from PIL import Image

SRC_SIZES = [16, 20, 24, 32, 40, 48, 64, 96]   # 需要生成的（不含原图那一帧）
SUPER = 1024


# ----------------------------------------------------------------------
# ICO 写入（自己拼，才能精确控制每一帧的像素）
# ----------------------------------------------------------------------
def frame_to_bmp(im):
    """把 RGBA 图编码成 ICO 里的 BMP 帧（BITMAPINFOHEADER + XOR + AND）。"""
    w, h = im.size
    px = im.convert("RGBA").load()

    # XOR：32bpp BGRA，自下而上
    xor = bytearray()
    for y in range(h - 1, -1, -1):
        for x in range(w):
            r, g, b, a = px[x, y]
            xor += bytes((b, g, r, a))

    # AND 掩码：1bpp，每行补到 4 字节，自下而上；0=不透明
    row_bytes = ((w + 31) // 32) * 4
    and_mask = bytearray()
    for y in range(h - 1, -1, -1):
        row = bytearray(row_bytes)
        for x in range(w):
            if px[x, y][3] < 128:
                row[x >> 3] |= (0x80 >> (x & 7))
        and_mask += row

    header = struct.pack("<IiiHHIIiiII", 40, w, h * 2, 1, 32, 0,
                         len(xor) + len(and_mask), 0, 0, 0, 0)
    return bytes(header) + bytes(xor) + bytes(and_mask)


def write_ico(frames, out_path):
    """frames: {边长: RGBA Image}

    帧按**从大到小**排列。这一点很重要：
    `QPixmap("x.ico")` 取的是 ICO 里的**第一帧**，不是最大帧。
    如果 16x16 排在最前，任何直接 QPixmap 读它的代码都会拿到 16x16，
    再放大就发糊（输入框左侧的引擎按钮就是这么踩的坑）。
    `QIcon` 不受影响（它按请求尺寸挑帧），Windows 也不挑顺序。
    """
    sizes = sorted(frames, reverse=True)
    blobs = [frame_to_bmp(frames[s]) for s in sizes]
    offset = 6 + 16 * len(sizes)
    with open(out_path, "wb") as f:
        f.write(struct.pack("<HHH", 0, 1, len(sizes)))
        for s, blob in zip(sizes, blobs):
            f.write(struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0,
                                1, 32, len(blob), offset))
            offset += len(blob)
        for blob in blobs:
            f.write(blob)


# ----------------------------------------------------------------------
# 图像处理
# ----------------------------------------------------------------------
def largest_frame(path):
    """取 ICO 里最大的那一帧。

    注意：新版 Pillow 的 Image.size 是只读属性，不能再写
    `im.size = (256,256)` 选帧，要用 im.ico.getimage(size)。
    """
    im = Image.open(path)
    try:
        sizes = im.ico.sizes()
        return im.ico.getimage(max(sizes)).convert("RGBA")
    except Exception:
        return im.convert("RGBA")


def premultiply(im):
    from PIL import ImageChops
    r, g, b, a = im.split()
    a3 = Image.merge("RGB", (a, a, a))
    rgb = ImageChops.multiply(Image.merge("RGB", (r, g, b)), a3)
    return Image.merge("RGBA", (*rgb.split(), a))


def unpremultiply(im):
    px = im.load()
    w, h = im.size
    out = Image.new("RGBA", (w, h))
    po = out.load()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            po[x, y] = (0, 0, 0, 0) if a == 0 else (
                min(255, r * 255 // a), min(255, g * 255 // a),
                min(255, b * 255 // a), a)
    return out


def build(src_path, out_path):
    src = largest_frame(src_path)
    w0, h0 = src.size

    # 透明区域的 RGB 归零，避免缩放时带出杂色
    px = src.load()
    for y in range(h0):
        for x in range(w0):
            r, g, b, a = px[x, y]
            if a == 0:
                px[x, y] = (0, 0, 0, 0)

    big = unpremultiply(premultiply(src).resize((SUPER, SUPER), Image.LANCZOS))

    frames = {}
    for s in SRC_SIZES:
        if s < w0:
            frames[s] = big.resize((s, s), Image.LANCZOS)
    frames[w0] = src                      # ← 原图原样，零损失

    write_ico(frames, out_path)
    return frames


def make_header(src_path, out_path, size=128, radius=26, scale=0.72):
    """安装向导深色头部用的图标：白底圆角 + 原 logo。

    logo 是黑色线条，直接放深色头部上等于看不见，所以衬一块白底板。
    原图配色一点不动。
    """
    from PIL import ImageDraw
    src = largest_frame(src_path)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(canvas).rounded_rectangle(
        [0, 0, size - 1, size - 1], radius=radius, fill=(255, 255, 255, 255))
    inner = int(size * scale)
    glyph = src.resize((inner, inner), Image.LANCZOS)
    off = (size - inner) // 2
    canvas.paste(glyph, (off, off), glyph)
    canvas.save(out_path)
    return out_path


def preview(frames, out_png, scales=(16, 24, 32, 48, 128)):
    """把各尺寸放大摆出来，直观看像素质量。"""
    from PIL import ImageDraw
    zoom = 6
    pad = 12
    cell = 128 * zoom
    W = len(scales) * (cell + pad) + pad
    H = 2 * (cell + pad) + pad
    canvas = Image.new("RGB", (W, H), (243, 243, 243))
    ImageDraw.Draw(canvas).rectangle([0, 0, W, cell + pad], fill=(28, 28, 28))
    for i, s in enumerate(scales):
        if s not in frames:
            continue
        f = frames[s].resize((s * zoom, s * zoom), Image.NEAREST)
        x = pad + i * (cell + pad)
        canvas.paste(f, (x, pad), f)
        canvas.paste(f, (x, cell + pad * 2), f)
    canvas.save(out_png)


def main():
    ws = r"<项目根>"
    data = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ws,
                                                              "browser_project", "data")
    names = ["icon.ico", "settings_icon.ico", "download_icon.ico"]
    frames = None
    for n in names:
        p = os.path.join(data, n)
        if not os.path.isfile(p):
            print("  跳过（不存在）:", p)
            continue
        before = os.path.getsize(p)
        f = build(p, p)
        after = os.path.getsize(p)
        print("  %-22s %6d -> %6d 字节   尺寸=%s"
              % (n, before, after, sorted(f)))
        if frames is None:
            frames = f

    if frames:
        preview(frames, os.path.join(ws, "_icon_quality.png"))
        print("  预览: _icon_quality.png")

    inst = os.path.join(ws, "installer")
    ico = os.path.join(inst, "setup.ico")
    if os.path.isfile(ico):
        # 安装器图标直接用生成好的 icon.ico
        import shutil
        shutil.copy2(os.path.join(data, "icon.ico"), ico)
        make_header(ico, os.path.join(inst, "setup_header.png"))
        print("  向导头部图标: installer\\setup_header.png")


if __name__ == "__main__":
    main()

```

### installer\setup.py (大小: 31168 | 修改时间: 2026-10-03 10:52:52 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""NWbrowser 安装程序（自包含，不依赖任何第三方安装工具）。

向导流程
--------
    欢迎  ->  许可协议(GPL-3.0)  ->  安装选项  ->  安装中  ->  完成

做什么
------
1. 把内嵌的 payload.zip（应用本体）解压到安装目录
2. 建开始菜单快捷方式（可选桌面快捷方式）
3. 装一个卸载器 uninstall.exe 到安装目录
4. 在「控制面板 → 程序和功能」里注册（HKCU，所以不需要管理员）
5. 可选：装完直接启动

默认安装位置
------------
%LOCALAPPDATA%\\Programs\\NWbrowser

**为什么不是 Program Files**：NWbrowser 是绿色程序，配置/历史/Cookie
都存在自己目录下。Program Files 不可写，装那儿会导致设置存不下来。

命令行（给自动化/测试用）
------------------------
    Setup.exe --silent [--dir <路径>] [--no-shortcuts] [--run]
"""

import os
import sys
import zipfile
import shutil
import subprocess

APP_NAME = "NWbrowser"
APP_DISPLAY = "NWbrowser"
APP_VERSION = "1.0.0"
APP_TAGLINE = "基于 WebView2 的多进程浏览器"
PUBLISHER = "NWbrowser contributors"
LICENSE_NAME = "GNU General Public License v3.0 or later"
LICENSE_SPDX = "GPL-3.0-or-later"
UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\NWbrowser"

ACCOUNT_URL = "https://www.gnu.org/licenses/gpl-3.0.html"

FROZEN = bool(getattr(sys, "frozen", False))
RES_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
PAYLOAD = os.path.join(RES_DIR, "payload.zip")
UNINSTALLER = os.path.join(RES_DIR, "uninstall.exe")
LICENSE_FILE = os.path.join(RES_DIR, "LICENSE")


def default_dir():
    base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    return os.path.join(base, "Programs", APP_NAME)


# ======================================================================
# 安装逻辑（GUI 与 --silent 共用）
# ======================================================================
def extract_payload(target, on_progress=None, on_log=None):
    if not os.path.isfile(PAYLOAD):
        raise RuntimeError("找不到内嵌的 payload.zip：%s" % PAYLOAD)
    os.makedirs(target, exist_ok=True)

    with zipfile.ZipFile(PAYLOAD, "r") as zf:
        items = zf.infolist()
        total = len(items)
        for i, item in enumerate(items, 1):
            zf.extract(item, target)
            if on_progress and (i % 3 == 0 or i == total):
                on_progress(i, total)
            if on_log and i % 30 == 0:
                on_log("正在解压… %d / %d" % (i, total))

    # 默认数据（设置/背景/搜索引擎图标等）随包放在 _defaults/ 下。
    # **只补目标目录里缺失的文件** —— 这样全新安装能拿到完整的默认值
    # （默认背景、主题色、搜索引擎图标），而覆盖安装不会把你已有的
    # 设置、书签、图标冲掉。
    merge_defaults(target, on_log)

    # 许可协议 + 第三方声明
    # MiSans 字体的许可协议要求「必须在软件中明确声明使用了 MiSans」，
    # 所以 THIRD-PARTY-NOTICES.txt 必须随程序一起装出去，不能只放在仓库里。
    for _name in ("LICENSE", "THIRD-PARTY-NOTICES.txt"):
        try:
            _src = os.path.join(RES_DIR, _name)
            if os.path.isfile(_src):
                shutil.copy2(_src, os.path.join(target, _name))
            elif on_log:
                on_log("声明文件缺失：%s" % _name)
        except Exception as _e:
            if on_log:
                on_log("写入 %s 失败：%s" % (_name, _e))

    exe = os.path.join(target, APP_NAME + ".exe")
    if not os.path.isfile(exe):
        raise RuntimeError("解压后没有找到 %s" % exe)
    return exe


def merge_defaults(target, on_log=None):
    """把 _defaults/ 里的默认数据补进 target（已存在的不动）。"""
    src = os.path.join(target, "_defaults")
    if not os.path.isdir(src):
        return 0, 0
    added = skipped = 0
    for root, dirs, files in os.walk(src):
        rel = os.path.relpath(root, src)
        dst_dir = target if rel == "." else os.path.join(target, rel)
        try:
            os.makedirs(dst_dir, exist_ok=True)
            # 空目录也要建（ZIP 不保存空目录，fixed/ 这类就会漏）
            for d in dirs:
                os.makedirs(os.path.join(dst_dir, d), exist_ok=True)
        except Exception as e:
            if on_log:
                on_log("默认目录创建失败 %s: %s" % (dst_dir, e))
        for name in files:
            s = os.path.join(root, name)
            d = os.path.join(dst_dir, name)
            if os.path.exists(d):
                skipped += 1
                continue
            try:
                os.makedirs(dst_dir, exist_ok=True)
                shutil.copy2(s, d)
                added += 1
                if on_log:
                    on_log("补充默认文件：%s"
                           % (name if rel == "." else os.path.join(rel, name)))
            except Exception as e:
                if on_log:
                    on_log("默认文件写入失败 %s: %s" % (d, e))
    # 用完删掉，别让它躺在安装目录里
    try:
        shutil.rmtree(src, ignore_errors=True)
    except Exception:
        pass
    if on_log:
        on_log("默认数据：新增 %d 个，保留已有 %d 个" % (added, skipped))
    return added, skipped


def make_shortcut(lnk_path, target_exe, workdir):
    os.makedirs(os.path.dirname(lnk_path), exist_ok=True)
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        lnk = shell.CreateShortCut(lnk_path)
        lnk.TargetPath = target_exe
        lnk.WorkingDirectory = workdir
        lnk.IconLocation = target_exe + ",0"
        lnk.Description = "%s - %s" % (APP_DISPLAY, APP_TAGLINE)
        lnk.Save()
        return True
    except Exception as e:
        print("[setup] 建快捷方式失败 %s: %s" % (lnk_path, e))
        return False


def install_uninstaller(target):
    exe = os.path.join(target, "uninstall.exe")
    if os.path.isfile(UNINSTALLER):
        shutil.copy2(UNINSTALLER, exe)
        return exe
    return None


def register_uninstall(target, uninstall_exe, size_kb):
    import winreg
    try:
        k = winreg.CreateKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY)
        vals = [
            ("DisplayName", "%s %s" % (APP_DISPLAY, APP_VERSION)),
            ("DisplayVersion", APP_VERSION),
            ("Publisher", PUBLISHER),
            ("InstallLocation", target),
            ("DisplayIcon", os.path.join(target, APP_NAME + ".exe") + ",0"),
            ("UninstallString", '"%s"' % (uninstall_exe or
                                          os.path.join(target, APP_NAME + ".exe"))),
            ("QuietUninstallString", '"%s" --silent' % (uninstall_exe or
                                                        os.path.join(target, APP_NAME + ".exe"))),
            ("EstimatedSize", int(size_kb)),
            ("URLInfoAbout", ACCOUNT_URL),
            ("NoModify", 1),
            ("NoRepair", 1),
        ]
        for name, value in vals:
            if isinstance(value, int):
                winreg.SetValueEx(k, name, 0, winreg.REG_DWORD, value)
            else:
                winreg.SetValueEx(k, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(k)
        return True
    except Exception as e:
        print("[setup] 注册卸载信息失败:", e)
        return False


def dir_size_kb(path):
    total = 0
    for root, _dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    return total // 1024


def do_install(target, desktop_shortcut=True, startmenu_shortcut=True,
               on_progress=None, on_log=None):
    logs = []

    def _log(m):
        logs.append(m)
        if on_log:
            on_log(m)

    _log("安装位置：%s" % target)
    if os.path.isdir(target):
        _log("目标目录已存在，将覆盖安装")
    exe = extract_payload(target, on_progress=on_progress, on_log=_log)
    _log("应用文件解压完成")

    uni = install_uninstaller(target)
    if uni:
        _log("卸载程序已就位")

    programs = os.path.join(os.environ.get("APPDATA", ""), "Microsoft",
                            "Windows", "Start Menu", "Programs")
    if startmenu_shortcut:
        if make_shortcut(os.path.join(programs, APP_DISPLAY + ".lnk"),
                         exe, target):
            _log("已创建开始菜单快捷方式")
        if uni and make_shortcut(
                os.path.join(programs, "卸载 " + APP_DISPLAY + ".lnk"),
                uni, target):
            _log("已创建开始菜单卸载入口")

    if desktop_shortcut:
        desk = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop",
                            APP_DISPLAY + ".lnk")
        if make_shortcut(desk, exe, target):
            _log("已创建桌面快捷方式")

    kb = dir_size_kb(target)
    _log("安装后占用：%.1f MB" % (kb / 1024.0))
    if register_uninstall(target, uni, kb):
        _log("已注册到「程序和功能」（当前用户，无需管理员）")

    return exe, logs


# ======================================================================
# 命令行静默安装
# ======================================================================
def silent_install(argv):
    target = default_dir()
    desktop = True
    run_after = False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--dir" and i + 1 < len(argv):
            target = argv[i + 1]
            i += 2
            continue
        if a == "--no-shortcuts":
            desktop = False
        elif a == "--run":
            run_after = True
        i += 1

    exe, logs = do_install(target, desktop_shortcut=desktop)
    for line in logs:
        print("[setup] " + line)
    print("[setup] 安装完成：%s" % exe)
    if run_after:
        subprocess.Popen([exe], cwd=target)
    return 0


# ======================================================================
# GUI：五步向导
# ======================================================================
def read_license():
    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ("GNU GENERAL PUBLIC LICENSE\nVersion 3, 29 June 2007\n\n"
                "完整文本见安装目录下的 LICENSE 文件，或访问\n%s\n"
                % ACCOUNT_URL)


def gui_main():
    from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                                 QHBoxLayout, QLabel, QLineEdit, QPushButton,
                                 QCheckBox, QProgressBar, QPlainTextEdit,
                                 QFileDialog, QMessageBox, QStackedWidget,
                                 QTextBrowser, QFrame, QSizePolicy)
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    from PyQt5.QtGui import QIcon, QPixmap, QFont

    ACCENT = "#2f6fed"
    TEXT = "#1f2430"
    MUTED = "#6b7280"

    class Worker(QThread):
        progress = pyqtSignal(int, int)
        message = pyqtSignal(str)
        done = pyqtSignal(bool, str, str)

        def __init__(self, target, desktop, startmenu):
            super().__init__()
            self.target = target
            self.desktop = desktop
            self.startmenu = startmenu

        def run(self):
            try:
                exe, _logs = do_install(
                    self.target,
                    desktop_shortcut=self.desktop,
                    startmenu_shortcut=self.startmenu,
                    on_progress=lambda d, t: self.progress.emit(d, t),
                    on_log=lambda m: self.message.emit(m))
                self.done.emit(True, exe, "")
            except Exception:
                import traceback
                self.done.emit(False, "", traceback.format_exc())

    class Wizard(QWidget):
        STEPS = ["欢迎", "许可协议", "安装选项", "正在安装", "完成"]

        def __init__(self):
            super().__init__()
            self.setWindowTitle("%s %s 安装向导" % (APP_DISPLAY, APP_VERSION))
            self.setFixedSize(780, 580)
            self._exe = ""
            self._worker = None
            self._page = 0
            self._build()
            self._goto(0)
            self._center()

        def _center(self):
            """居中显示，避免被窗口管理器丢到屏幕角落。"""
            try:
                from PyQt5.QtWidgets import QApplication
                scr = QApplication.primaryScreen().availableGeometry()
                self.move(scr.left() + (scr.width() - self.width()) // 2,
                          scr.top() + (scr.height() - self.height()) // 2)
            except Exception:
                pass

        # ---------------- 界面骨架 ----------------
        def _build(self):
            root = QVBoxLayout(self)
            root.setContentsMargins(0, 0, 0, 0)
            root.setSpacing(0)

            # ---- 顶部横幅 ----
            head = QFrame()
            head.setFixedHeight(96)
            head.setStyleSheet(
                "background: qlineargradient(x1:0,y1:0,x2:1,y2:0,"
                " stop:0 #1f2430, stop:1 #2f3a52);")
            hl = QHBoxLayout(head)
            hl.setContentsMargins(24, 14, 24, 14)
            hl.setSpacing(16)

            ico = QLabel()
            # 优先用专门做的「白底圆角 + 原 logo」图：
            # logo 是黑色线条，直接放在深色头部上几乎看不见。
            p = QPixmap(os.path.join(RES_DIR, "setup_header.png"))
            if p.isNull():
                p = QPixmap(os.path.join(RES_DIR, "setup.png"))
            if not p.isNull():
                ico.setPixmap(p.scaled(48, 48, Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation))
            hl.addWidget(ico)

            box = QVBoxLayout()
            box.setSpacing(2)
            t1 = QLabel("%s %s" % (APP_DISPLAY, APP_VERSION))
            t1.setStyleSheet("color:white; font-size:20px; font-weight:600;")
            t2 = QLabel(APP_TAGLINE)
            t2.setStyleSheet("color:#c7d0e0; font-size:12px;")
            box.addWidget(t1)
            box.addWidget(t2)
            box.addStretch(1)
            hl.addLayout(box)
            hl.addStretch(1)
            root.addWidget(head)

            # ---- 页面区 ----
            self.stack = QStackedWidget()
            self.stack.setStyleSheet("background:#ffffff;")
            root.addWidget(self.stack, 1)

            self.stack.addWidget(self._page_welcome())
            self.stack.addWidget(self._page_license())
            self.stack.addWidget(self._page_options())
            self.stack.addWidget(self._page_progress())
            self.stack.addWidget(self._page_finish())

            # ---- 底部栏 ----
            foot = QFrame()
            foot.setFixedHeight(64)
            foot.setStyleSheet("background:#f5f6f8; border-top:1px solid #e3e6ea;")
            fl = QHBoxLayout(foot)
            fl.setContentsMargins(24, 12, 24, 12)

            self.step_label = QLabel("")
            self.step_label.setStyleSheet("color:%s; font-size:12px;" % MUTED)
            fl.addWidget(self.step_label)
            fl.addStretch(1)

            self.btn_back = QPushButton("上一步")
            self.btn_back.setMinimumWidth(96)
            self.btn_back.clicked.connect(self._back)
            fl.addWidget(self.btn_back)

            self.btn_next = QPushButton("下一步")
            self.btn_next.setMinimumWidth(130)
            self.btn_next.setMinimumHeight(34)
            self.btn_next.setCursor(Qt.PointingHandCursor)
            # 直接给按钮设样式，不用 objectName 选择器 ——
            # 之前用 QPushButton#primary 在打包后没生效，按钮变成白底白字看不见
            self.btn_next.setStyleSheet(
                "QPushButton { background:#2f6fed; color:#ffffff;"
                " border:none; border-radius:6px; padding:8px 20px;"
                " font-weight:600; font-size:13px; }"
                "QPushButton:hover { background:#2559c9; }"
                "QPushButton:disabled { background:#b8c6e8; color:#ffffff; }")
            self.btn_next.setDefault(True)
            self.btn_next.clicked.connect(self._next)
            fl.addWidget(self.btn_next)

            self.btn_cancel = QPushButton("取消")
            self.btn_cancel.setMinimumWidth(84)
            self.btn_cancel.clicked.connect(self.close)
            fl.addWidget(self.btn_cancel)

            self.setStyleSheet("""
                QWidget { color: %s; font-family: "Microsoft YaHei UI","Segoe UI"; font-size: 13px; }
                QPushButton {
                    background: #ffffff; border: 1px solid #cfd6e0;
                    border-radius: 6px; padding: 7px 16px;
                }
                QPushButton:hover { background: #f0f4ff; border-color: %s; }
                QPushButton:disabled { color: #aab2bd; border-color: #e3e6ea; }
                QLineEdit { border: 1px solid #cfd6e0; border-radius: 6px; padding: 6px 8px; }
                QCheckBox { spacing: 8px; }
                QProgressBar {
                    border: 1px solid #dfe3e8; border-radius: 8px;
                    height: 16px; text-align: center; background: #f2f4f7;
                }
                QProgressBar::chunk { background: %s; border-radius: 7px; }
            """ % (TEXT, ACCENT, ACCENT))
            root.addWidget(foot)

        def _h(self, text, sub=""):
            w = QWidget()
            lay = QVBoxLayout(w)
            lay.setContentsMargins(28, 22, 28, 6)
            lay.setSpacing(4)
            t = QLabel(text)
            t.setStyleSheet("font-size:17px; font-weight:600;")
            lay.addWidget(t)
            if sub:
                s = QLabel(sub)
                s.setStyleSheet("color:%s; font-size:12px;" % MUTED)
                s.setWordWrap(True)
                lay.addWidget(s)
            return w

        # ---------------- 页 1：欢迎 ----------------
        def _page_welcome(self):
            page = QWidget()
            lay = QVBoxLayout(page)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(0)
            lay.addWidget(self._h(
                "欢迎使用 %s %s 安装向导" % (APP_DISPLAY, APP_VERSION),
                "几秒钟即可完成安装，过程中不需要管理员权限。"))

            body = QWidget()
            b = QVBoxLayout(body)
            b.setContentsMargins(28, 10, 28, 8)
            b.setSpacing(10)

            intro = QLabel(
                "NWbrowser 是一个多进程架构的浏览器：系统托盘作为主进程，"
                "按需拉起悬浮条、浏览器窗口、设置窗口与下载管理进程，"
                "内核使用 WebView2（Edge）。")
            intro.setWordWrap(True)
            intro.setStyleSheet("color:%s;" % MUTED)
            b.addWidget(intro)

            info = QLabel(
                "<table cellspacing='0' cellpadding='4'>"
                "<tr><td style='color:%s'>版本</td><td>%s</td></tr>"
                "<tr><td style='color:%s'>发布者</td><td>%s</td></tr>"
                "<tr><td style='color:%s'>许可证</td><td>%s（%s）</td></tr>"
                "<tr><td style='color:%s'>默认位置</td><td>%s</td></tr>"
                "<tr><td style='color:%s'>安装后占用</td><td>约 150 MB</td></tr>"
                "</table>"
                % (MUTED, APP_VERSION, MUTED, PUBLISHER, MUTED,
                   LICENSE_NAME, LICENSE_SPDX, MUTED, default_dir(),
                   MUTED))
            info.setTextFormat(Qt.RichText)
            b.addWidget(info)

            note = QLabel(
                "安装内容：主程序（含托盘）、浏览器窗口、设置、下载管理、"
                "卸载程序，以及 GPL-3.0 许可证文本。\n"
                "点击「下一步」继续。")
            note.setWordWrap(True)
            note.setStyleSheet("color:%s;" % MUTED)
            b.addWidget(note)
            b.addStretch(1)

            lay.addWidget(body, 1)
            return page

        # ---------------- 页 2：许可协议 ----------------
        def _page_license(self):
            page = QWidget()
            lay = QVBoxLayout(page)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(0)
            lay.addWidget(self._h(
                "许可协议",
                "%s 以 %s 发布，请阅读并接受条款。" % (APP_DISPLAY,
                                                      LICENSE_NAME)))

            body = QWidget()
            b = QVBoxLayout(body)
            b.setContentsMargins(28, 10, 28, 8)
            b.setSpacing(10)

            view = QTextBrowser()
            view.setPlainText(read_license())
            view.setStyleSheet(
                "QTextBrowser { border:1px solid #dfe3e8; border-radius:6px;"
                " background:#fbfbfc; font-family:Consolas,monospace;"
                " font-size:11px; }")
            b.addWidget(view, 1)

            self.cb_accept = QCheckBox("我已阅读并同意 %s 的条款" % LICENSE_NAME)
            self.cb_accept.stateChanged.connect(self._update_buttons)
            b.addWidget(self.cb_accept)

            lay.addWidget(body, 1)
            return page

        # ---------------- 页 3：安装选项 ----------------
        def _page_options(self):
            page = QWidget()
            lay = QVBoxLayout(page)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(0)
            lay.addWidget(self._h("安装选项", "选择安装位置与快捷方式。"))

            body = QWidget()
            b = QVBoxLayout(body)
            b.setContentsMargins(28, 10, 28, 8)
            b.setSpacing(12)

            row = QHBoxLayout()
            row.addWidget(QLabel("安装位置"))
            self.path_edit = QLineEdit(default_dir())
            row.addWidget(self.path_edit, 1)
            btn = QPushButton("浏览…")
            btn.clicked.connect(self._browse)
            row.addWidget(btn)
            b.addLayout(row)

            hint = QLabel(
                "提示：安装在当前用户目录下最省事。NWbrowser 把配置、"
                "历史、密码和 Cookie 存在自己目录里，所以"
                "<b>不建议装到 Program Files</b>（那里不可写）。")
            hint.setTextFormat(Qt.RichText)
            hint.setWordWrap(True)
            hint.setStyleSheet("color:%s; font-size:12px;" % MUTED)
            b.addWidget(hint)

            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setStyleSheet("color:#e9ecf1;")
            b.addWidget(line)

            self.cb_desktop = QCheckBox("创建桌面快捷方式")
            self.cb_desktop.setChecked(True)
            b.addWidget(self.cb_desktop)

            self.cb_startmenu = QCheckBox("创建开始菜单快捷方式（含卸载入口）")
            self.cb_startmenu.setChecked(True)
            b.addWidget(self.cb_startmenu)

            self.cb_run = QCheckBox("安装完成后立即运行 %s" % APP_DISPLAY)
            self.cb_run.setChecked(True)
            b.addWidget(self.cb_run)

            b.addStretch(1)
            lay.addWidget(body, 1)
            return page

        # ---------------- 页 4：安装中 ----------------
        def _page_progress(self):
            page = QWidget()
            lay = QVBoxLayout(page)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(0)
            lay.addWidget(self._h("正在安装", "请稍候，不要关闭窗口。"))

            body = QWidget()
            b = QVBoxLayout(body)
            b.setContentsMargins(28, 14, 28, 8)
            b.setSpacing(12)

            self.bar = QProgressBar()
            self.bar.setRange(0, 100)
            b.addWidget(self.bar)

            self.log = QPlainTextEdit()
            self.log.setReadOnly(True)
            self.log.setStyleSheet(
                "font-family:Consolas,monospace; font-size:11px;"
                " border:1px solid #e3e6ea; border-radius:6px;")
            b.addWidget(self.log, 1)

            lay.addWidget(body, 1)
            return page

        # ---------------- 页 5：完成 ----------------
        def _page_finish(self):
            page = QWidget()
            lay = QVBoxLayout(page)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(0)
            lay.addWidget(self._h("安装完成", "%s %s 已经装好了。"
                                  % (APP_DISPLAY, APP_VERSION)))

            body = QWidget()
            b = QVBoxLayout(body)
            b.setContentsMargins(28, 14, 28, 8)
            b.setSpacing(10)

            self.finish_label = QLabel("")
            self.finish_label.setWordWrap(True)
            self.finish_label.setTextFormat(Qt.RichText)
            b.addWidget(self.finish_label)

            b.addStretch(1)
            lay.addWidget(body, 1)
            return page

        # ---------------- 导航 ----------------
        def _update_buttons(self):
            last = self._page == len(self.STEPS) - 1
            self.btn_back.setEnabled(self._page in (2,) and self._worker is None)
            self.btn_next.setEnabled(True)

            if self._page == 0:
                self.btn_next.setText("下一步")
            elif self._page == 1:
                self.btn_next.setText("下一步")
                self.btn_next.setEnabled(self.cb_accept.isChecked())
            elif self._page == 2:
                self.btn_next.setText("开始安装")
            elif self._page == 3:
                self.btn_next.setText("安装中…")
                self.btn_next.setEnabled(False)
            else:
                self.btn_next.setText("完成")
            self.btn_cancel.setEnabled(self._worker is None)

        def _goto(self, idx):
            self._page = idx
            self.stack.setCurrentIndex(idx)
            self.step_label.setText(
                "第 %d / %d 步 · %s" % (idx + 1, len(self.STEPS),
                                        self.STEPS[idx]))
            self._update_buttons()

        def _back(self):
            if self._page > 0 and self._worker is None:
                self._goto(self._page - 1)

        def _next(self):
            if self._page == 0:
                self._goto(1)
            elif self._page == 1:
                if self.cb_accept.isChecked():
                    self._goto(2)
            elif self._page == 2:
                self._start_install()
            elif self._page == 4:
                self.close()

        def _browse(self):
            d = QFileDialog.getExistingDirectory(self, "选择安装位置",
                                                 self.path_edit.text())
            if d:
                base = os.path.basename(d.rstrip("\\/"))
                self.path_edit.setText(d if base.lower() == APP_NAME.lower()
                                       else os.path.join(d, APP_NAME))

        # ---------------- 执行安装 ----------------
        def _start_install(self):
            target = self.path_edit.text().strip()
            if not target:
                QMessageBox.warning(self, "提示", "请先选择安装位置。")
                return
            self._goto(3)
            self.log.appendPlainText("开始安装到：%s" % target)

            self._worker = Worker(target, self.cb_desktop.isChecked(),
                                  self.cb_startmenu.isChecked())
            self._worker.progress.connect(
                lambda d, t: self.bar.setValue(int(d * 100 / max(1, t))))
            self._worker.message.connect(self.log.appendPlainText)
            self._worker.done.connect(self._on_done)
            self._worker.start()

        def _on_done(self, ok, exe, err):
            self._worker = None
            self.bar.setValue(100)
            if not ok:
                self.log.appendPlainText(err)
                QMessageBox.critical(self, "安装失败",
                                     "安装过程中出错，详见日志。")
                self._goto(2)
                return

            self._exe = exe
            target = os.path.dirname(exe)
            ran = False
            if self.cb_run.isChecked():
                try:
                    subprocess.Popen([exe], cwd=target)
                    ran = True
                except Exception as e:
                    self.log.appendPlainText("启动失败：%s" % e)

            self.finish_label.setText(
                "<p><b>%s %s</b> 已安装到：<br><code>%s</code></p>"
                "<p>启动方式：<br>"
                "· 开始菜单搜索「%s」<br>"
                "· 桌面快捷方式（若已创建）<br>"
                "· 直接运行 <code>%s</code></p>"
                "<p>主程序是<b>系统托盘</b>。如果没看到图标，点任务栏的「^」"
                "展开隐藏图标区，或在 设置 → 个性化 → 任务栏 → "
                "其他系统托盘图标 里打开 %s。</p>"
                "<p>卸载：控制面板 → 程序和功能 → %s %s，"
                "或安装目录下的 uninstall.exe。</p>"
                "<p style='color:%s'>本程序以 %s 发布，许可证文本已随程序"
                "安装（LICENSE 文件）。</p>"
                "%s"
                % (APP_DISPLAY, APP_VERSION, target, APP_NAME, exe,
                   APP_NAME, APP_DISPLAY, APP_VERSION, MUTED,
                   LICENSE_NAME,
                   "<p style='color:%s'>已为你启动 %s。</p>"
                   % (MUTED, APP_DISPLAY) if ran else ""))
            self._goto(4)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME + " Setup")
    app.setApplicationVersion(APP_VERSION)
    # 窗口/任务栏图标必须用**多尺寸 ICO**。
    # 只给一张 256x256 的 PNG 的话，Windows 要 16x16 的小图标时拿不到合适尺寸，
    # 会退回显示通用占位图标（标题栏那个"小画框"）。
    ic = QIcon()
    for name in ("setup.ico", "setup.png"):
        p = os.path.join(RES_DIR, name)
        if os.path.isfile(p):
            ic.addFile(p)
    if not ic.isNull():
        app.setWindowIcon(ic)
    w = Wizard()
    w.show()
    return app.exec_()


def main():
    argv = sys.argv[1:]
    if "--silent" in argv:
        return silent_install(argv)
    return gui_main()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BaseException:
        import traceback
        msg = traceback.format_exc()
        try:
            with open(os.path.join(os.path.expanduser("~"), "Desktop",
                                   "nwb_setup_error.log"), "w",
                      encoding="utf-8") as f:
                f.write(msg)
        except Exception:
            pass
        raise

```

### installer\setup_version_info.txt (大小: 1122 | 修改时间: 2026-10-03 02:48:51 | 权限: 666)

```
# UTF-8
# Setup.exe 的版本资源。
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '080404B0',
          [
            StringStruct('CompanyName', 'NWbrowser contributors'),
            StringStruct('FileDescription', 'NWbrowser 1.0.0 安装程序'),
            StringStruct('FileVersion', '1.0.0.0'),
            StringStruct('InternalName', 'NWbrowser-Setup'),
            StringStruct('LegalCopyright', 'Copyright (C) 2026 NWbrowser contributors. Licensed under the GNU General Public License v3.0 or later.'),
            StringStruct('OriginalFilename', 'NWbrowser-1.0.0-Setup.exe'),
            StringStruct('ProductName', 'NWbrowser'),
            StringStruct('ProductVersion', '1.0.0.0'),
            StringStruct('Comments', 'Installs NWbrowser 1.0.0. Free software under GPL-3.0-or-later.')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [0x0804, 1200])])
  ]
)

```

### installer\uninstall.py (大小: 10537 | 修改时间: 2026-10-03 12:51:29 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""NWbrowser 卸载程序。

不用 Qt，只用 ctypes 弹系统对话框 —— 体积小（约 6MB），
也不依赖应用自己的运行库。

两阶段设计
----------
卸载器自己就住在要被删掉的安装目录里，Windows 不允许删除正在运行的 exe，
所以：

  阶段一（从安装目录运行）
      * 结束仍在跑的 NWbrowser 进程
      * 把自己复制到 %TEMP%，以 --from-temp <安装目录> 重新启动
      * **os._exit(0) 立刻退出** —— 用 sys.exit 会走 Python 清理流程，
        可能挂着不退，导致安装目录里的 uninstall.exe 一直被占用而删不掉
  阶段二（从 %TEMP% 运行）
      * 等阶段一真正退出（轮询 uninstall.exe 是否已解锁）
      * 删快捷方式、删注册表项、删安装目录
      * 安排删除 %TEMP% 里的自己

每一步都写 %TEMP%\\nwb_uninstall.log，出问题可直接看。
"""

import ctypes
import os
import shutil
import subprocess
import sys
import tempfile
import time

APP_NAME = "NWbrowser"
APP_DISPLAY = "NWbrowser 浏览器"
UNINSTALL_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\NWbrowser"

CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008
NEW_PROCESS_GROUP = 0x00000200

user32 = ctypes.WinDLL("user32", use_last_error=True)

LOG_PATH = os.path.join(tempfile.gettempdir(), "nwb_uninstall.log")


def log(msg):
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("%s  pid=%d  %s\n"
                    % (time.strftime("%H:%M:%S"), os.getpid(), msg))
    except Exception:
        pass


def msgbox(text, flags=0x40):
    """0x40=信息 0x30=警告 0x24=是/否 + 问号"""
    return user32.MessageBoxW(None, text, APP_DISPLAY + " 卸载", flags)


MB_YESNO = 0x04
MB_ICONQUESTION = 0x20
MB_ICONWARNING = 0x30
MB_ICONINFORMATION = 0x40
IDYES = 6


# ======================================================================
def kill_running():
    for image in (APP_NAME + ".exe",):
        try:
            subprocess.run(["taskkill", "/F", "/IM", image],
                           stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           creationflags=CREATE_NO_WINDOW)
            log("taskkill %s 完成" % image)
        except Exception as e:
            log("taskkill %s 异常: %s" % (image, e))
    time.sleep(0.8)


def remove_shortcuts():
    """删掉开始菜单/桌面上所有 NWbrowser 相关快捷方式。

    用通配匹配而不是硬编码文件名 —— 显示名或版本变了也不会漏删。
    """
    import glob
    removed = []
    appdata = os.environ.get("APPDATA", "")
    userprofile = os.environ.get("USERPROFILE", "")
    bases = [
        os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs"),
        os.path.join(userprofile, "Desktop"),
    ]
    patterns = []
    for base in bases:
        patterns.append(os.path.join(base, "*%s*.lnk" % APP_NAME))
        patterns.append(os.path.join(base, "*%s*.lnk" % APP_DISPLAY))

    seen = set()
    for pat in patterns:
        for p in glob.glob(pat):
            if p in seen:
                continue
            seen.add(p)
            try:
                os.remove(p)
                removed.append(p)
                log("删除快捷方式 %s" % p)
            except Exception as e:
                log("删快捷方式失败 %s: %s" % (p, e))
    return removed


def remove_registry():
    import winreg
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, UNINSTALL_KEY)
        log("删除注册项成功")
        return True
    except FileNotFoundError:
        log("注册项本来就不存在")
        return True
    except Exception as e:
        log("删注册项失败: %s" % e)
        return False


def remove_dir(path):
    """尽力删干净；返回删不掉的文件列表。"""
    if not path or not os.path.isdir(path):
        log("目录不存在，无需删除: %s" % path)
        return []

    for attempt in range(1, 6):
        failed = []
        for root, dirs, files in os.walk(path, topdown=False):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    os.remove(fp)
                except Exception:
                    failed.append(fp)
            for d in dirs:
                try:
                    os.rmdir(os.path.join(root, d))
                except Exception:
                    pass
        try:
            os.rmdir(path)
        except Exception:
            pass

        if not os.path.isdir(path):
            log("目录已删除（第 %d 次尝试）" % attempt)
            return []
        log("第 %d 次尝试后仍有 %d 个文件没删掉" % (attempt, len(failed)))
        time.sleep(0.8)

    # 最后再列一次到底剩什么
    left = []
    for root, _dirs, files in os.walk(path):
        for f in files:
            left.append(os.path.join(root, f))
    log("最终残留 %d 个文件" % len(left))
    return left


def wait_parent_exit(target, seconds=15.0):
    """等阶段一把 target\\uninstall.exe 放开（说明它进程已退出）。"""
    exe = os.path.join(target, "uninstall.exe")
    t0 = time.time()
    while time.time() - t0 < seconds:
        if not os.path.isfile(exe):
            log("uninstall.exe 已不存在，父进程应已退出")
            return True
        try:
            with open(exe, "a+b"):
                pass
            log("uninstall.exe 已可写（父进程已退出），用时 %.1fs"
                % (time.time() - t0))
            return True
        except Exception:
            time.sleep(0.25)
    log("等待父进程退出超时（%.1fs）" % seconds)
    return False


def relaunch_from_temp(target):
    try:
        tmp = os.path.join(tempfile.gettempdir(),
                           "nwb_uninstall_%d.exe" % os.getpid())
        shutil.copy2(sys.executable, tmp)
        log("已复制自身到 %s" % tmp)
        subprocess.Popen(
            [tmp, "--from-temp", target],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=DETACHED_PROCESS | NEW_PROCESS_GROUP,
            close_fds=True)
        log("已启动 %TEMP% 中的第二阶段")
        return True
    except Exception as e:
        log("启动第二阶段失败: %s" % e)
        msgbox("无法启动卸载程序：\n%s" % e, flags=MB_ICONWARNING)
        return False


def cleanup_self_from_temp():
    """从 %TEMP% 运行时，安排删掉自己。"""
    try:
        bat = os.path.join(tempfile.gettempdir(), "nwb_del_self.bat")
        with open(bat, "w", encoding="gbk") as f:
            f.write("@echo off\r\n")
            f.write("ping 127.0.0.1 -n 3 >nul\r\n")
            f.write('del /f /q "%s"\r\n' % sys.executable)
            f.write('del /f /q "%s"\r\n' % LOG_PATH)
            f.write('del /f /q "%~f0"\r\n')
        subprocess.Popen(["cmd", "/c", bat],
                         stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         creationflags=CREATE_NO_WINDOW)
        log("已安排删除 %TEMP% 中的自身")
    except Exception as e:
        log("安排自删失败: %s" % e)


# ======================================================================
def main():
    argv = sys.argv[1:]
    silent = "--silent" in argv
    from_temp = "--from-temp" in argv

    if from_temp:
        try:
            target = argv[argv.index("--from-temp") + 1]
        except Exception:
            target = ""
    else:
        target = os.path.dirname(os.path.abspath(sys.executable))

    # ---------------- 阶段一 ----------------
    if not from_temp:
        log("=== 阶段一 ===")
        log("安装目录 = %s" % target)

        if not silent:
            reply = msgbox(
                "确定要卸载 %s 吗？\n\n"
                "安装位置：%s\n\n"
                "注意：配置、历史记录、保存的密码和 Cookie 都存在这个目录里，\n"
                "卸载会一并删除。\n\n要继续吗？" % (APP_DISPLAY, target),
                flags=MB_YESNO | MB_ICONQUESTION)
            if reply != IDYES:
                log("用户取消")
                return 0

        kill_running()
        if not relaunch_from_temp(target):
            return 1
        # 关键：必须立刻硬退出，否则本进程会一直占用安装目录里的
        # uninstall.exe，第二阶段永远删不掉目录
        log("阶段一 os._exit(0)")
        sys.stdout.flush() if sys.stdout else None
        os._exit(0)

    # ---------------- 阶段二 ----------------
    log("=== 阶段二（来自 %TEMP%）===")
    log("安装目录 = %s" % target)

    wait_parent_exit(target)
    kill_running()
    removed = remove_shortcuts()
    reg_ok = remove_registry()
    failed = remove_dir(target)

    if silent:
        cleanup_self_from_temp()
        return 0 if not failed else 1

    lines = ["%s 已卸载。" % APP_DISPLAY, ""]
    lines.append("删除快捷方式：%d 个" % len(removed))
    lines.append("移除程序列表登记：%s" % ("成功" if reg_ok else "失败"))
    if failed:
        lines.append("")
        lines.append("有 %d 个文件被占用没能删掉：" % len(failed))
        for f in failed[:5]:
            lines.append("  " + f)
        lines.append("")
        lines.append("重启后可以手动删除：\n%s" % target)
    else:
        lines.append("安装目录已彻底删除。")
    msgbox("\n".join(lines), flags=MB_ICONINFORMATION)
    cleanup_self_from_temp()
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except SystemExit:
        # 正常退出路径。sys.exit() 抛的就是 SystemExit，它属于 BaseException，
        # 如果不单独接住，会被下面那个 except 当成"出错"弹一个框
        # （曾经真的这样：卸载成功却弹出 SystemExit: 0 的错误框）。
        raise
    except BaseException:
        import traceback
        log("未捕获异常:\n" + traceback.format_exc())
        try:
            msgbox("卸载程序出错：\n\n%s" % traceback.format_exc(),
                   flags=MB_ICONWARNING)
        except Exception:
            pass
        sys.exit(1)
    else:
        sys.exit(code if isinstance(code, int) else 0)

```

### installer\uninstall_version_info.txt (大小: 1045 | 修改时间: 2026-10-03 02:49:20 | 权限: 666)

```
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '080404B0',
          [
            StringStruct('CompanyName', 'NWbrowser contributors'),
            StringStruct('FileDescription', 'NWbrowser 卸载程序'),
            StringStruct('FileVersion', '1.0.0.0'),
            StringStruct('InternalName', 'NWbrowser-Uninstall'),
            StringStruct('LegalCopyright', 'Copyright (C) 2026 NWbrowser contributors. Licensed under the GNU General Public License v3.0 or later.'),
            StringStruct('OriginalFilename', 'uninstall.exe'),
            StringStruct('ProductName', 'NWbrowser'),
            StringStruct('ProductVersion', '1.0.0.0'),
            StringStruct('Comments', 'Uninstaller for NWbrowser 1.0.0')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [0x0804, 1200])])
  ]
)

```

### build_app.bat (大小: 4080 | 修改时间: 2026-10-03 11:02:54 | 权限: 777)

```
@echo off
chcp 936 >nul
pushd "%~dp0"

echo ============================================================
echo  NWbrowser 打包（PyInstaller / onedir）
echo  依赖直接取本目录 library/，构建机不需要 pip 装 PyQt6 等
echo ============================================================
echo.

set "ROOT=%~dp0"
set "LIB=%ROOT%library"
:: 产物必须放在**可写、且不受任何沙箱/受限环境管辖**的位置。
:: 放在项目目录或 DSH workspace 里会导致：Shell_NotifyIcon 被拒（托盘没图标）、
:: onefile 解压 %TEMP% 失败、子进程受限等一堆假故障。
if defined NWBROWSER_OUT (
    set "OUT=%NWBROWSER_OUT%"
) else (
    set "OUT=%USERPROFILE%\Desktop"
)
set "APP=%OUT%\NWbrowser"

:: ------------------------------------------------------------
:: PyInstaller 的 pywin32 / PyQt6 hook 会在子进程里 import 这些包，
:: 只靠 spec 里的 pathex 不够，必须同时设 PYTHONPATH。
:: ------------------------------------------------------------
set "PYTHONPATH=%LIB%;%LIB%\PyQt6;%LIB%\qtwebview2;%LIB%\pywin32;%LIB%\pywin32\win32;%LIB%\pywin32\win32\lib;%LIB%\browser-oxide"

:: ------------------------------------------------------------
:: 前置检查
:: ------------------------------------------------------------
python -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo [X] 找不到 python，请先装 Python 3.10 x64 并加进 PATH
    goto :fail
)
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [X] 没装 PyInstaller，先执行:  python -m pip install pyinstaller
    goto :fail
)
if not exist "%LIB%\PyQt6\PyQt6\QtCore.pyd" (
    echo [X] 缺少 %LIB%\PyQt6，请先运行 deploy.bat
    goto :fail
)
if not exist "%LIB%\qtwebview2\wryview\_core.cp310-win_amd64.pyd" (
    echo [X] 缺少 %LIB%\qtwebview2\wryview，请先运行 deploy.bat
    goto :fail
)

:: ------------------------------------------------------------
:: 清理旧产物
:: ------------------------------------------------------------
if exist "%ROOT%build" rd /s /q "%ROOT%build"
if exist "%APP%" rd /s /q "%APP%"
if not exist "%OUT%" mkdir "%OUT%"

:: ------------------------------------------------------------
:: 构建
:: ------------------------------------------------------------
echo [1/3] PyInstaller 构建中（首次约 3~8 分钟）...
echo.
python -m PyInstaller NWbrowser.spec ^
    --noconfirm ^
    --distpath "%OUT%" ^
    --workpath "%ROOT%build"
if errorlevel 1 (
    echo.
    echo [X] 构建失败，请看上面的报错
    goto :fail
)

:: ------------------------------------------------------------
:: 把当前项目里已有的用户数据复制到 exe 旁边
:: —— 这样打包版一启动就和源码版状态一致
::     （背景图、搜索引擎、收藏、历史、密码、固定项、Cookie）
:: ------------------------------------------------------------
echo.
echo [2/3] 复制现有用户数据到 %APP% ...
for %%F in (settings.json search_engines.json favorites.json history.json downloads.json passwords.json) do (
    if exist "%ROOT%%%F" (
        copy /y "%ROOT%%%F" "%APP%\%%F" >nul
        echo    + %%F
    )
)
for %%D in (fixed userdata cache) do (
    if exist "%ROOT%%%D" (
        robocopy "%ROOT%%%D" "%APP%\%%D" /e /nfl /ndl /njh /njs /np >nul
        echo    + %%D\
    )
)

:: ------------------------------------------------------------
:: 自检
:: ------------------------------------------------------------
echo.
echo [3/3] 跑一次打包自检...
if not exist "%APP%\NWbrowser.exe" (
    echo [X] 没找到 %APP%\NWbrowser.exe
    goto :fail
)
"%APP%\NWbrowser.exe" --role selftest
if errorlevel 1 (
    echo [X] 自检失败，看 %APP%\selftest.txt
    goto :fail
)
echo   自检通过 -> %APP%\selftest.txt

echo.
echo ============================================================
echo  打包完成
echo    程序: %APP%\NWbrowser.exe
echo    数据: 和 exe 同级（settings.json / userdata / fixed ...）
echo.
echo  提示：请把整个 NWbrowser 文件夹放到可写目录（桌面、D:\Apps 等），
echo        不要放 Program Files，否则设置/历史/Cookie 存不下来。
echo ============================================================
echo.
popd
pause
exit /b 0

:fail
echo.
popd
pause
exit /b 1

```

### deploy.bat (大小: 7301 | 修改时间: 2026-10-03 11:02:54 | 权限: 777)

```
@echo off
chcp 936
pushd "%~dp0"

echo ============================================================
echo  部署依赖到 library/
echo  断点续传 + 多代理兜底 + 失败不中断
echo ============================================================
echo.

set "FAILED="
set "ROOT=%~dp0"

:: ------------------------------------------------------------
:: 准备目录
:: ------------------------------------------------------------
if not exist "library" mkdir "library"
if not exist "library\browser-oxide" mkdir "library\browser-oxide"
if not exist "library\PyQt6" mkdir "library\PyQt6"
if not exist "library\pywin32" mkdir "library\pywin32"
if not exist "library\qtwebview2" mkdir "library\qtwebview2"


:: ============================================================
:: [1/9] browser-oxide
:: ============================================================
echo ========== [1/9] browser-oxide ==========
if exist "library\browser-oxide\browser_oxide" (
    echo   已装，跳过
) else (
    pip install browser-oxide --target "%ROOT%library\browser-oxide" --no-warn-script-location
    if errorlevel 1 (echo [!] 1/9 失败 & set FAILED=%FAILED% 1)
)


:: ============================================================
:: [2/9] PyQt6
:: ============================================================
echo.
echo ========== [2/9] PyQt6 ==========
if exist "library\PyQt6\PyQt6" (
    echo   已装，跳过
) else (
    pip install PyQt6==6.11.0 --target "%ROOT%library\PyQt6" --no-warn-script-location
    if errorlevel 1 (echo [!] 2/9 失败 & set FAILED=%FAILED% 2)
)


:: ============================================================
:: [3/9] pywin32
:: ============================================================
echo.
echo ========== [3/9] pywin32 ==========
if exist "library\pywin32\win32" (
    echo   已装，跳过
) else (
    pip install pywin32==312 --target "%ROOT%library\pywin32" --no-warn-script-location
    if errorlevel 1 (echo [!] 3/9 失败 & set FAILED=%FAILED% 3)
)


:: ============================================================
:: [4/9] qtwebview2（GitHub，五层兜底）
:: ============================================================
echo.
echo ========== [4/9] qtwebview2 ==========
if exist "library\qtwebview2\qtwebview2" (
    echo   已装，跳过
) else (
    set "QTWV_OK="

    echo   [1/5] 直连 GitHub ...
    pip install git+https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if not errorlevel 1 set "QTWV_OK=1"

    if not defined QTWV_OK (
        echo   [2/5] 代理 ghproxy.com ...
        pip install git+https://ghproxy.com/https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
        if not errorlevel 1 set "QTWV_OK=1"
    )

    if not defined QTWV_OK (
        echo   [3/5] 代理 gh-proxy.com ...
        pip install git+https://gh-proxy.com/https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
        if not errorlevel 1 set "QTWV_OK=1"
    )

    if not defined QTWV_OK (
        echo   [4/5] 代理 ghfast.top ...
        pip install git+https://ghfast.top/https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
        if not errorlevel 1 set "QTWV_OK=1"
    )

    if not defined QTWV_OK (
        if exist "%ROOT%QtWebView.zip" (
            echo   [5/5] 本地 QtWebView.zip ...
            if exist "%TEMP%\QtWebView" rd /s /q "%TEMP%\QtWebView"
            powershell -NoProfile -Command "Expand-Archive -Path '%ROOT%QtWebView.zip' -DestinationPath '%TEMP%\QtWebView' -Force"
            pip install "%TEMP%\QtWebView" --target "%ROOT%library\qtwebview2" --no-warn-script-location
            if not errorlevel 1 set "QTWV_OK=1"
        ) else (
            echo   [5/5] 跳过（项目根目录没有 QtWebView.zip）
        )
    )

    if not defined QTWV_OK (
        echo [!] 4/9 qtwebview2 全部失败
        set FAILED=%FAILED% 4
    ) else (
        echo   qtwebview2 安装成功
    )
)


:: ============================================================
:: [5/9] qtwebview2 核心依赖
:: ============================================================
echo.
echo ========== [5/9] qtpy + pythonnet ==========
if exist "library\qtwebview2\qtpy" (
    echo   已装，跳过
) else (
    pip install qtpy==2.4.3 pythonnet==3.1.0 --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if errorlevel 1 (echo [!] 5/9 失败 & set FAILED=%FAILED% 5)
)


:: ============================================================
:: [6/9] pythonnet 传递依赖
:: ============================================================
echo.
echo ========== [6/9] cffi / clr_loader / packaging / pycparser / typing_extensions ==========
if exist "library\qtwebview2\clr_loader" (
    echo   已装，跳过
) else (
    pip install cffi==2.1.1 clr_loader==0.3.1 packaging==26.3 pycparser==3.0 typing_extensions==4.16.0 --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if errorlevel 1 (echo [!] 6/9 失败 & set FAILED=%FAILED% 6)
)


:: ============================================================
:: [7/9] wryview
:: ============================================================
echo.
echo ========== [7/9] wryview ==========
if exist "library\qtwebview2\wryview" (
    echo   已装，跳过
) else (
    pip install wryview==0.4.0 --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if errorlevel 1 (echo [!] 7/9 失败 & set FAILED=%FAILED% 7)
)


:: ============================================================
:: [8/9] comtypes
:: ============================================================
echo.
echo ========== [8/9] comtypes ==========
if exist "library\comtypes" (
    echo   已装，跳过
) else (
    pip install comtypes==1.4.17 --target "%ROOT%library" --no-warn-script-location
    if errorlevel 1 (echo [!] 8/9 失败 & set FAILED=%FAILED% 8)
)


:: ============================================================
:: [9/9] psutil + watchdog
:: ============================================================
echo.
echo ========== [9/9] psutil + watchdog ==========
if exist "library\psutil" (
    echo   已装，跳过
) else (
    pip install psutil==7.2.2 watchdog==6.0.0 --target "%ROOT%library" --no-warn-script-location
    if errorlevel 1 (echo [!] 9/9 失败 & set FAILED=%FAILED% 9)
)


:: ============================================================
:: 汇总
:: ============================================================
echo.
echo ============================================================
if "%FAILED%"=="" (
    echo  全部成功
) else (
    echo  以下步骤失败: %FAILED%
    echo.
    echo  如果第 4 步失败：
    echo    1. 重跑一次 bat（GitHub 抽风经常几分钟就好）
    echo    2. 或手动下载 QtWebView.zip 放到项目根目录再跑
    echo       下载地址: https://github.com/xiaosuawa/QtWebView
    echo       点 Code - Download ZIP
    echo    3. 或从同事那里拷 library\qtwebview2 过来
)
echo ============================================================
echo.

echo 当前 library 目录结构：
dir /b "%ROOT%library"
echo.
echo qtwebview2 目录内容：
dir /b "%ROOT%library\qtwebview2"
echo.

popd
pause
```

### download fonts.bat (大小: 1746 | 修改时间: 2026-10-03 11:02:54 | 权限: 777)

```
@echo off
chcp 936 >nul
pushd "%~dp0"

set "ZIP=%~dp0MiSans.zip"
set "EXTRACT=%~dp0assets\_temp_misans"
set "TARGET=%~dp0assets\fonts"

echo ========== 准备目录 / Preparing folders ==========
if not exist "assets" mkdir "assets"
if not exist "%TARGET%" mkdir "%TARGET%"

echo ========== 清空目标字体目录 / Clearing target folder ==========
del /f /q "%TARGET%\*.*" >nul 2>&1
rd /s /q "%TARGET%" >nul 2>&1
mkdir "%TARGET%"

echo ========== 检查字体压缩包 / Checking font package ==========
if not exist "%ZIP%" (
    echo 未找到 MiSans.zip，正在下载 / Downloading MiSans.zip ...
    powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://hyperos.mi.com/font-download/MiSans.zip' -OutFile '%ZIP%'"
)

if not exist "%ZIP%" (
    echo.
    echo 下载失败，请手动下载 MiSans.zip 放到项目根目录
    echo Download failed. Please download MiSans.zip manually.
    echo 下载地址 / URL: https://hyperos.mi.com/font-download/MiSans.zip
    pause
    exit /b 1
)

echo ========== 解压 / Extracting ==========
if exist "%EXTRACT%" rd /s /q "%EXTRACT%"
powershell -NoProfile -Command "Expand-Archive -Path '%ZIP%' -DestinationPath '%EXTRACT%' -Force"

echo ========== 复制字体文件 / Copying fonts ==========
for /r "%EXTRACT%" %%f in (*.woff2) do copy "%%f" "%TARGET%" >nul

dir /b "%TARGET%\*.woff2" >nul 2>&1
if errorlevel 1 (
    echo 未找到 woff2，改用 ttf / No woff2, using ttf ...
    for /r "%EXTRACT%" %%f in (*.ttf) do copy "%%f" "%TARGET%" >nul
)

echo ========== 清理临时文件 / Cleaning up ==========
rd /s /q "%EXTRACT%" >nul 2>&1
del "%ZIP%" >nul 2>&1

echo.
echo 完成！字体已放入 / Done! Fonts placed in:
echo   %TARGET%
echo.
echo 文件列表 / File list:
dir /b "%TARGET%"
popd
pause
```

### main.py (大小: 10810 | 修改时间: 2026-10-03 03:30:39 | 权限: 666)

```
# -*- coding: utf-8 -*-
"""NWbrowser 统一入口（源码运行 / 打包运行 共用）。

打包工具（PyInstaller）只能有一个入口脚本，而本项目的托盘、悬浮条、设置、
下载、浏览器窗口、无痕窗口、下载任务各自是独立进程。这里用 ``--role``
把它们统一到同一个可执行文件上：

    源码:  python main.py
    打包:  NWbrowser.exe

    python main.py --role bar                悬浮条
    python main.py --role settings           设置窗口
    python main.py --role downloads          下载管理
    python main.py --role window    --id df-0
    python main.py --role incognito --id ig-0
    python main.py --role download-worker --url ... --path ...

子进程的实际命令由 ``component/apppaths.py`` 的 ``role_command()`` 生成：
源码模式仍是 ``python.exe component/<脚本>.py``（与改造前完全一致），
打包模式变成 ``NWbrowser.exe --role <角色>``。
"""

import os
import sys

# ----------------------------------------------------------------------
# 让 component/ 里的模块能被 import
# ----------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
if getattr(sys, "frozen", False):
    _CODE_DIR = getattr(sys, "_MEIPASS", _HERE)
else:
    _CODE_DIR = os.path.join(_HERE, "component")

if _CODE_DIR not in sys.path:
    sys.path.insert(0, _CODE_DIR)


import multiprocessing  # noqa: E402


def _pop_role(argv):
    """从 argv 里摘出 ``--role <name>``，剩下的留给各角色自己的 argparse。"""
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--role":
            del argv[i]
            if i < len(argv):
                return argv.pop(i)
            return None
        if a.startswith("--role="):
            del argv[i]
            return a.split("=", 1)[1]
        i += 1
    return None


# ----------------------------------------------------------------------
# 各角色
# ----------------------------------------------------------------------
def _run_main():
    from main_app import main
    main()


def _run_bar():
    from floating_bar import main
    main()


def _run_settings():
    from settings_app import main
    main()


def _run_downloads():
    from downloads_app import main
    main()


def _run_window():
    from window import main
    main()


def _run_incognito():
    from incognito_window import main
    main()


def _run_download_worker():
    from download_worker import main
    main()


def _run_selftest():
    """不弹 GUI，只检查打包产物的依赖/资源是否齐全。

    打包版没有控制台，所以结果写到 exe 同级的 selftest.txt。
    """
    import importlib
    import traceback

    import apppaths

    lines = [
        "frozen  = %s" % apppaths.FROZEN,
        "RES_DIR = %s" % apppaths.RES_DIR,
        "APP_DIR = %s" % apppaths.APP_DIR,
        "exe     = %s" % sys.executable,
        "cwd     = %s" % os.getcwd(),
        "",
        "--- 目录 ---",
    ]
    for label, d in (("i18n", os.path.join(apppaths.RES_DIR, "i18n")),
                     ("assets/fonts",
                      os.path.join(apppaths.RES_DIR, "assets", "fonts")),
                     ("data", os.path.join(apppaths.RES_DIR, "data")),
                     ("APP_DIR", apppaths.APP_DIR)):
        lines.append("%-14s exists=%-5s %s" % (label, os.path.isdir(d), d))

    lines += ["", "--- 模块 ---"]
    ok = True
    mods = [
        "PyQt6.QtCore", "PyQt6.QtGui", "PyQt6.QtWidgets", "PyQt6.QtNetwork",
        "win32gui", "win32con", "comtypes", "comtypes.client",
        "qtwebview2", "qtwebview2._bridge", "qtwebview2.widget", "wryview",
        "apppaths", "loader", "i18n", "theme",
        "settings", "settings_backend", "settings_pages", "settings_window",
        "history_store", "history_hook", "downloads_store", "downloads_window",
        "download_notify_dialog", "download_worker", "favorites_store",
        "favorites_menu", "password_hook", "search_engines", "search_icons",
        "pinned_store", "ipc", "window_icon", "input_box", "title_bar",
        "popup_window", "rounded_menu", "personalize_dialog", "corner_mask",
        "activity_watcher", "dom_activity", "notify_store", "main_app",
        "floating_bar",
        "downloads_app", "settings_app", "window", "incognito_window",
    ]
    for m in mods:
        try:
            importlib.import_module(m)
            lines.append("OK    %s" % m)
        except Exception as e:
            ok = False
            lines.append("FAIL  %s: %r" % (m, e))

    lines += ["", "--- 功能 ---"]
    try:
        import i18n
        lines.append("languages = %s" % (i18n.list_languages(),))
    except Exception:
        ok = False
        lines.append("languages FAIL\n" + traceback.format_exc())
    try:
        import settings
        lines.append("settings  = %s" % (settings.load_window_settings(),))
    except Exception:
        ok = False
        lines.append("settings FAIL\n" + traceback.format_exc())

    # 托盘图标能不能真的加载出来（"托盘没有内容" 的直接判据）
    try:
        from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
        from PyQt6.QtGui import QIcon
        _app = QApplication.instance() or QApplication([])
        for name in ("icon.ico", "settings_icon.ico", "download_icon.ico"):
            p = os.path.join(apppaths.RES_DIR, "data", name)
            icon = QIcon(p)
            good = os.path.isfile(p) and not icon.isNull()
            if not good:
                ok = False
            lines.append("icon %-20s exists=%-5s loadable=%s"
                         % (name, os.path.isfile(p), not icon.isNull()))
    except Exception:
        ok = False
        lines.append("icon FAIL\n" + traceback.format_exc())

    # 托盘探针：真正把 QSystemTrayIcon 显示出来，看 Qt 侧到底成不成功。
    # isVisible=True 却肉眼看不到 => Windows 把它收进了溢出区（"^"）。
    try:
        p = os.path.join(apppaths.RES_DIR, "data", "icon.ico")
        icon = QIcon(p)
        tray = QSystemTrayIcon(icon, _app)
        tray.setToolTip("NWbrowser selftest")
        tray.show()
        lines.append("platform        = %s" % _app.platformName())
        lines.append("trayAvailable   = %s" % QSystemTrayIcon.isSystemTrayAvailable())
        lines.append("supportsMessages= %s" % QSystemTrayIcon.supportsMessages())
        lines.append("iconSizes       = %s"
                     % [(s.width(), s.height()) for s in icon.availableSizes()])
        lines.append("tray.isVisible  = %s" % tray.isVisible())
    except Exception:
        lines.append("tray probe FAIL\n" + traceback.format_exc())

    # 固定项（悬浮条上那些网站）能不能读出来
    try:
        import pinned_store
        items, broken = pinned_store.load_all()
        lines.append("pinned dir = %s" % pinned_store.FIXED_DIR)
        lines.append("pinned     = %d 个 %s%s"
                     % (len(items),
                        [p.get("host") for p in items],
                        ("  损坏:%s" % broken) if broken else ""))
    except Exception:
        lines.append("pinned FAIL\n" + traceback.format_exc())

    lines += ["", "RESULT = %s" % ("PASS" if ok else "FAIL")]
    text = "\n".join(lines)

    print(text)
    try:
        with open(os.path.join(apppaths.APP_DIR, "selftest.txt"),
                  "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    sys.exit(0 if ok else 1)


_DISPATCH = {
    "main": _run_main,
    "bar": _run_bar,
    "settings": _run_settings,
    "downloads": _run_downloads,
    "window": _run_window,
    "incognito": _run_incognito,
    "download-worker": _run_download_worker,
    "selftest": _run_selftest,
}


def _install_crash_logging(role, app_dir):
    """把所有未捕获异常写进 nwbrowser-crash-<角色>.log。

    打包版是窗口程序，没有控制台；PyInstaller 自带的窗口诊断弹窗对本项目
    没用（还会以 exit code 1 静默收场），所以关掉它、自己落盘：

    * Qt 槽函数 / 定时器里的异常 → PyQt6 会调 ``sys.excepthook``，这里接住；
    * 子线程里的异常 → ``threading.excepthook``；
    * 进程启动阶段的异常 → ``main()`` 里的 try/except。
    """
    import threading
    import traceback

    crash_path = os.path.join(app_dir, "nwbrowser-crash-%s.log" % role)

    def _write(text):
        try:
            with open(crash_path, "a", encoding="utf-8") as f:
                f.write(text if text.endswith("\n") else text + "\n")
                f.write("=" * 60 + "\n")
        except Exception:
            pass

    def _hook(exc_type, exc_value, exc_tb):
        _write("".join(
            traceback.format_exception(exc_type, exc_value, exc_tb)
        ))

    sys.excepthook = _hook

    def _thread_hook(args):
        _write("".join(traceback.format_exception(
            args.exc_type, args.exc_value, args.exc_traceback
        )))

    try:
        threading.excepthook = _thread_hook
    except Exception:
        pass

    return _write


def main():
    multiprocessing.freeze_support()

    role = _pop_role(sys.argv) or "main"

    runner = _DISPATCH.get(role)
    if runner is None:
        sys.stderr.write("[main] 未知角色: %r\n" % (role,))
        sys.stderr.write("可用: %s\n" % ", ".join(sorted(_DISPATCH)))
        sys.exit(2)

    import apppaths

    # 打包后没有控制台，把 print 落到 exe 同级的日志里，方便排查
    if getattr(sys, "frozen", False):
        try:
            f = open(os.path.join(apppaths.APP_DIR,
                                  "nwbrowser-%s.log" % role),
                     "a", encoding="utf-8", buffering=1)
            sys.stdout = f
            sys.stderr = f
        except Exception:
            pass

    print("[main] role=%s frozen=%s app_dir=%s"
          % (role, apppaths.FROZEN, apppaths.APP_DIR))

    # 崩溃兜底：Qt 槽 / 定时器 / 子线程里的异常都要留证据，
    # 打包版没有控制台，没有这层会把现场丢得干干净净
    _write_crash = _install_crash_logging(role, apppaths.APP_DIR)

    try:
        runner()
    except SystemExit:
        raise
    except BaseException:
        import traceback
        _write_crash(traceback.format_exc())
        traceback.print_exc()
        sys.exit(3)


if __name__ == "__main__":
    main()

```

### README.md (大小: 17230 | 修改时间: 2026-10-03 10:52:28 | 权限: 666)

````
# NWbrowser

**基于 WebView2 的多进程 Windows 浏览器 —— 系统托盘主进程 + 悬浮条 + 多窗口**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2B-lightgrey)
![Python](https://img.shields.io/badge/python-3.10-3776ab)

---

## 中文

### 这是什么

NWbrowser 是一个 Windows 桌面浏览器。它不用 QtWebEngine，而是把微软的
**WebView2（Edge/Chromium 内核）**通过 `qtwebview2` 嵌进 Qt 界面里，
因此安装体积小、网页兼容性等同于 Edge。

它的架构不是"一个窗口一个程序"，而是**进程分工**：常驻一个系统托盘主进程，
按需拉起悬浮条、浏览器窗口、设置窗口和下载管理进程，彼此用本地 IPC 通信。
这样关掉所有窗口后，托盘仍在，随时唤回上次的会话。

### 主要特性

| 功能 | 说明 |
|---|---|
| **系统托盘常驻** | 主进程就是托盘。关窗口不退程序，托盘菜单可开新窗口/设置/下载/退出 |
| **悬浮条** | 贴边的工具条，滚动切换**固定项**，点图钉开对应站点；不占任务栏 |
| **固定项（Pinned）** | 把常用站点钉住，独立记忆每个站点的多个入口 URL 和上次浏览位置 |
| **多窗口 + 会话共享** | 站点登录态跟着站点走；无痕窗口独立隔离，不留痕迹 |
| **个性化** | 主题色 + 背景图（缩略图网格、右键删除、清空），逐窗口记忆 |
| **下载管理** | 独立下载进程，进度/完成气泡通知，支持取消与断点信息 |
| **完成提醒** | 见下方「完成提醒」小节 |
| **隐私控制** | 三级跟踪防护、第三方 Cookie 开关、权限（摄像头/麦克风/定位/通知）逐项策略 |
| **多语言** | 简体中文 / English / Русский 三套语言包，运行时热切换 |

### 完成提醒（W 态检测）

针对"页面在**没有用户操作**的情况下自己持续加载"的场景（长列表懒加载、
自动翻页、前端分片渲染等），NWbrowser 内置了一个 JS 侧的状态机：

- 用户操作（滚动/点击/键盘/跳转）后 **1000ms 内**插入的 DOM 节点 → 记为 `lazy`
- 没有用户操作时插入的节点 → 记为 `new`
- 每 300ms 归并成一条记录，只看最近 **10 条**
- **IDLE 态**：`new >= 7` → 进入 **W 态**
- **W 态**：`lazy >= 7` → 判定为人为操作触发，**不提醒**
- **5 秒没有新增**：
  - W 态 → **自然死亡** → **响一声 + 强制窗口置顶**（提醒你"它加载完了"）
  - IDLE 态 → 自然死亡但**不提醒**

开关位置：**标题栏「⋯」菜单 →「完成提醒」**。

> 这个开关是**按站点记忆**的（存在 `userdata/complete_notify.json`），
> 打开一次之后重开窗口仍然生效。

### 进程架构

```
main_app.py（托盘主进程）
├── floating_bar.py      悬浮条（同时负责调度窗口进程、持有 Job Object）
├── window.py --id df-N  浏览器窗口（每窗口一个进程）
├── settings_app.py      设置窗口
└── downloads_app.py     下载管理
        └── download_worker.py   下载工作进程（每任务一个）

        通信：QLocalServer / QLocalSocket
        注册：%TEMP%\browser_ipc_registry.json
```

- 托盘是父进程：子进程意外退出会自动重新拉起（正常退出流程除外）
- 悬浮条持有 **Job Object（KILL_ON_JOB_CLOSE）**，保证整个进程组一起回收，
  不会留下孤儿进程
- 关闭软件时先给窗口发 `MSG_QUIT` 走**优雅退出**（WebView2 正常析构、
  profile 落盘），1.2 秒内没退的才强制结束

### 运行要求

- **Windows 10 1809 及以上**（64 位）
- **WebView2 Runtime** —— Windows 11 和大部分 Windows 10 已自带；
  没有的话去 [微软官网](https://developer.microsoft.com/microsoft-edge/webview2/) 装 Evergreen 版
- 源码运行需要 **Python 3.10 x64**

### 从源码运行

```bat
:: 1. 装依赖到项目内的 library\（不污染全局 Python）
deploy.bat

:: 2. 运行
python component\main_app.py
```

> `deploy.bat` 会把依赖装进 `library\`，程序运行时从那里加载，**不需要 venv**。
> 其中 `qtwebview2` 不在 PyPI，脚本会从 GitHub 拉取（内置多个镜像兜底）。

### 打包

```bat
:: 打包成 onedir 目录（输出到 %USERPROFILE%\Desktop\NWbrowser）
browser_project\build_app.bat
```

> ⚠️ **构建产物不要放在受沙箱/受限环境管辖的目录里**，否则会出现
> "托盘没图标""onefile 解压失败"这类假故障。

### 数据存放位置

程序是**绿色**的：所有用户数据都在 exe 同级的目录下。

```
NWbrowser.exe
settings.json              设置（主题、语言、隐私开关…）
history.json               浏览历史
favorites.json             书签
downloads.json             下载记录
passwords.json             保存的登录信息
fixed\                     固定项（每个站点一个文件夹）
userdata\
  profile\EBWebView\       ← WebView2 用户数据：Cookie / 登录态 / localStorage
  search_icons\            搜索引擎图标缓存
  complete_notify.json     完成提醒的按站点开关
```

- **关闭软件不会丢登录态**（优雅退出，profile 正常落盘）
- **卸载会一并删除**这些数据（安装目录整个删掉）
- 想把数据放到别处：在 `settings.json` 里改 `env.user_data_folder`

### 许可证

**GNU General Public License v3.0 or later**（GPL-3.0-or-later）。
完整文本见 [LICENSE](LICENSE)。

```
Copyright (C) 2026 NWbrowser contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
```

### 第三方组件与声明

本项目**使用了以下第三方组件**，它们各自的许可证如下。
**MiSans 字体按其许可协议要求，在此明确声明。**

| 组件 | 版本 | 许可证 | 用途 |
|---|---|---|---|
| [PyQt6](https://pypi.org/project/PyQt6/) | 6.11.0 | **GPL-3.0-only** | Qt6 界面框架 |
| [Qt 6](https://www.qt.io/) | 6.11.0 | LGPL-3.0 / GPL-3.0 | PyQt6 底层 |
| [qtwebview2](https://github.com/xiaosuawa/QtWebView) | 2.1.1 | MIT-0 | WebView2 与 Qt 的桥接 |
| [wryview](https://pypi.org/project/wryview/) | 0.4.0 | **MPL-2.0** | WebView2 宿主（Rust） |
| [pywin32](https://pypi.org/project/pywin32/) | 312 | PSF-2.0 | Win32 API |
| [comtypes](https://pypi.org/project/comtypes/) | 1.4.17 | MIT | COM（任务栏 ITaskbarList 等） |
| [QtPy](https://pypi.org/project/QtPy/) | 2.4.3 | MIT | Qt 绑定兼容层 |
| [cffi](https://pypi.org/project/cffi/) | 2.1.1 | MIT-0 | C 扩展调用 |
| [clr_loader](https://pypi.org/project/clr-loader/) | 0.3.1 | MIT | .NET 运行时加载 |
| [packaging](https://pypi.org/project/packaging/) | 26.3 | Apache-2.0 / BSD-2-Clause | 版本解析 |
| [typing_extensions](https://pypi.org/project/typing-extensions/) | 4.16.0 | PSF-2.0 | 类型标注兼容 |
| [psutil](https://pypi.org/project/psutil/) | 7.2.2 | BSD-3-Clause | 进程与系统信息 |
| [watchdog](https://pypi.org/project/watchdog/) | 6.0.0 | Apache-2.0 | 文件系统监控 |
| [browser-oxide](https://pypi.org/project/browser-oxide/) | 0.1.3 | MIT / Apache-2.0 | （可选，默认不打包） |
| **MiSans 字体** | — | **小米 MiSans 字体知识产权许可协议** | 界面字体 |
| Microsoft **WebView2** | — | Microsoft 软件许可条款 | 浏览器内核 |

#### MiSans 字体声明

> This software uses the **MiSans** font, which is provided by Xiaomi Inc.
> MiSans is a free font for global commercial use, but per its license
> (MiSans Font Intellectual Property License Agreement), we specifically
> note here that **MiSans is used in this software as an embedded/UI font**.
>
> 本软件使用**小米 MiSans 字体**。MiSans 为全球免费商用字体，但依据其
> 许可协议要求，特此在软件中明确声明：**本软件使用了 MiSans 字体**。
>
> 字体来源：<https://hyperos.mi.com/font/>
> 不得修改 MiSans 的字形外观；不得单独销售字体文件本身。

#### 关于 PyQt6 的许可证

PyQt6 采用 **GPL-3.0-only**。因此任何基于本项目的分发都必须**同样以 GPL 兼容
的方式开源** —— 这也是本项目选择 GPL-3.0-or-later 的原因之一。
（若需闭源分发，须另行向 Riverbank Computing 购买 PyQt 商业授权。）

---

## English

### What is this

NWbrowser is a Windows desktop browser. Instead of QtWebEngine it embeds
Microsoft **WebView2 (Edge/Chromium)** through `qtwebview2`, so the install
stays small and page compatibility matches Edge.

It is not "one window, one program". A tray-resident main process spawns the
floating bar, browser windows, the settings window and the download manager
on demand, and they talk over local IPC. Close every window and the tray is
still there to bring your session back.

### Highlights

| Feature | Description |
|---|---|
| **Tray-resident** | The tray *is* the main process. Closing windows does not quit the app |
| **Floating bar** | An edge-docked strip; scroll to switch **pinned** sites, click a pin to open it |
| **Pinned sites** | Each pinned host remembers its own entry URLs and last position |
| **Multi-window** | Login state follows the *site*, not the window; incognito windows stay isolated |
| **Personalization** | Theme color + background images, remembered per window |
| **Downloads** | Dedicated download process with progress and completion toasts |
| **Completion alert** | See "Completion alert" below |
| **Privacy** | Three tracking-protection levels, third-party cookie switch, per-capability permission policy |
| **i18n** | Simplified Chinese / English / Russian, hot-swappable |

### Completion alert (the "W state" detector)

For pages that keep loading **without any user interaction** (infinite scroll,
auto-pagination, chunked rendering), NWbrowser runs a small JS state machine:

- DOM nodes inserted **within 1000 ms** of a user action (scroll/click/key/URL
  change) are tagged `lazy`
- Nodes inserted with no recent user action are tagged `new`
- Every 300 ms the batch is folded into one record; only the latest **10** are kept
- **IDLE state**: `new >= 7` → enter **W state**
- **W state**: `lazy >= 7` → judged as user-driven, **no alert**
- **5 seconds with no new nodes**:
  - W state → **natural death** → **play a sound and force the window on top**
  - IDLE state → natural death, **silent**

Toggle: **title bar "⋯" menu → "Complete notify"**.
It is remembered **per site** (`userdata/complete_notify.json`), so it survives
window restarts.

### Process architecture

```
main_app.py (tray main process)
├── floating_bar.py      floating bar; also spawns windows, owns the Job Object
├── window.py --id df-N  browser window (one process each)
├── settings_app.py      settings window
└── downloads_app.py     download manager
        └── download_worker.py   one worker process per download

        IPC:    QLocalServer / QLocalSocket
        Registry: %TEMP%\browser_ipc_registry.json
```

- The tray is the parent: a child that dies unexpectedly is respawned
  (except during a normal quit)
- The floating bar owns a **Job Object (KILL_ON_JOB_CLOSE)**, so the whole
  process group is reclaimed together — no orphans
- On quit, windows get `MSG_QUIT` first for a **graceful shutdown** (WebView2
  tears down properly and the profile is flushed); only stragglers are killed
  after 1.2 s

### Requirements

- **Windows 10 1809 or later**, 64-bit
- **WebView2 Runtime** — bundled with Windows 11 and most Windows 10 builds;
  otherwise install the Evergreen runtime from
  [Microsoft](https://developer.microsoft.com/microsoft-edge/webview2/)
- **Python 3.10 x64** to run from source

### Run from source

```bat
:: 1. install dependencies into the project's library\ (no global pollution)
deploy.bat

:: 2. run
python component\main_app.py
```

> `deploy.bat` installs into `library\`; the app loads from there at runtime,
> so **no virtualenv is required**. `qtwebview2` is not on PyPI — the script
> pulls it from GitHub with several mirror fallbacks.

### Build

```bat
:: build an onedir bundle (outputs to %USERPROFILE%\Desktop\NWbrowser)
browser_project\build_app.bat
```

> ⚠️ Do **not** build into a sandboxed/restricted directory, or you will hit
> phantom failures such as "tray icon missing" or "onefile cannot extract".

### Where data lives

The app is portable: everything sits next to the executable.

```
NWbrowser.exe
settings.json              settings (theme, language, privacy…)
history.json               browsing history
favorites.json             bookmarks
downloads.json             download records
passwords.json             saved logins
fixed\                     pinned sites (one folder per host)
userdata\
  profile\EBWebView\       WebView2 user data: cookies / logins / localStorage
  search_icons\            cached search-engine icons
  complete_notify.json     per-site completion-alert toggle
```

- **Quitting does not lose your logins** (graceful shutdown flushes the profile)
- **Uninstalling deletes all of it** (the install directory is removed)
- To relocate: change `env.user_data_folder` in `settings.json`

### License

**GNU General Public License v3.0 or later** (GPL-3.0-or-later).
See [LICENSE](LICENSE) for the full text.

```
Copyright (C) 2026 NWbrowser contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
```

### Third-party notices

This project **bundles and uses the third-party components listed below**.
Per its license, the use of **MiSans** is explicitly noted here.

| Component | Version | License | Purpose |
|---|---|---|---|
| [PyQt6](https://pypi.org/project/PyQt6/) | 6.11.0 | **GPL-3.0-only** | Qt6 bindings |
| [Qt 6](https://www.qt.io/) | 6.11.0 | LGPL-3.0 / GPL-3.0 | UI framework |
| [qtwebview2](https://github.com/xiaosuawa/QtWebView) | 2.1.1 | MIT-0 | WebView2 ⇄ Qt bridge |
| [wryview](https://pypi.org/project/wryview/) | 0.4.0 | **MPL-2.0** | WebView2 host (Rust) |
| [pywin32](https://pypi.org/project/pywin32/) | 312 | PSF-2.0 | Win32 API |
| [comtypes](https://pypi.org/project/comtypes/) | 1.4.17 | MIT | COM (ITaskbarList, …) |
| [QtPy](https://pypi.org/project/QtPy/) | 2.4.3 | MIT | Qt binding shim |
| [cffi](https://pypi.org/project/cffi/) | 2.1.1 | MIT-0 | C extension calls |
| [clr_loader](https://pypi.org/project/clr-loader/) | 0.3.1 | MIT | .NET runtime loading |
| [packaging](https://pypi.org/project/packaging/) | 26.3 | Apache-2.0 / BSD-2-Clause | version parsing |
| [typing_extensions](https://pypi.org/project/typing-extensions/) | 4.16.0 | PSF-2.0 | typing backports |
| [psutil](https://pypi.org/project/psutil/) | 7.2.2 | BSD-3-Clause | process/system info |
| [watchdog](https://pypi.org/project/watchdog/) | 6.0.0 | Apache-2.0 | filesystem monitoring |
| [browser-oxide](https://pypi.org/project/browser-oxide/) | 0.1.3 | MIT / Apache-2.0 | optional, not bundled by default |
| **MiSans font** | — | **Xiaomi MiSans Font IP License Agreement** | UI font |
| Microsoft **WebView2** | — | Microsoft Software License Terms | browser engine |

#### MiSans notice

> This software uses the **MiSans** font, provided by Xiaomi Inc.
> MiSans is free for global commercial use; per its license
> (MiSans Font Intellectual Property License Agreement) we explicitly note
> here that **MiSans is used in this software**.
>
> Source: <https://hyperos.mi.com/font/>
> The glyph appearance of MiSans may not be altered, and the font files
> themselves may not be sold separately.

#### A note on PyQt6's license

PyQt6 is **GPL-3.0-only**. Any distribution of this project must therefore
also be open-sourced under a GPL-compatible license — one of the reasons this
project is GPL-3.0-or-later. For closed-source distribution you would need a
commercial PyQt license from Riverbank Computing.

---

## 参与贡献 / Contributing

Issue 和 Pull Request 都欢迎。
Issues and pull requests are welcome.

提交前请确保 / Before submitting, please make sure:

- 源码模式下 `python component\main_app.py` 能正常启动
- `python main.py --role selftest` 输出 `RESULT = PASS`
- 没有把个人数据（`settings.json` / `history.json` / `userdata\`）提交进来

````

### requirements.txt (大小: 653 | 修改时间: 2026-10-03 00:38:18 | 权限: 666)

```
# browser_project 依赖清单
# 需要 Python 3.10 (x64, Windows)
#
# 一键部署请运行 deploy.bat
# 本文件仅作为依赖清单参考，不能直接 pip install -r
#
# 注意：qtwebview2 不在 PyPI，需从 GitHub 装，见 deploy.bat

# ---- 核心引擎 ----
browser-oxide

# ---- UI 框架 ----
PyQt6==6.11.0
pywin32==312

# ---- WebView2 内核（qtwebview2 从 GitHub 装）----
qtpy==2.4.3
pythonnet==3.1.0
wryview==0.4.0
cffi==2.1.1
clr_loader==0.3.1
packaging==26.3
pycparser==3.0
typing_extensions==4.16.0

# ---- Windows API ----
comtypes==1.4.17

# ---- 系统监控 ----
psutil==7.2.2
watchdog==6.0.0
```

### run.bat (大小: 1801 | 修改时间: 2026-10-03 11:03:20 | 权限: 777)

```
@echo off
chcp 936 >nul
pushd "%~dp0"
title NWbrowser 一键准备与运行

echo ============================================================
echo  NWbrowser 一键准备并运行
echo ============================================================
echo.
echo  这个脚本依次做三件事：
echo    1. 安装依赖到 library\   （deploy.bat）
echo    2. 安装 MiSans 字体      （download fonts.bat）
echo    3. 启动程序              （python main.py）
echo.
echo  已装好的步骤会自动跳过，可以放心重复运行。
echo  按 Ctrl+C 可以随时中止。
echo.
pause

echo.
echo ============================================================
echo  [1/3] 安装依赖
echo ============================================================
if exist "library\PyQt6\PyQt6" if exist "library\pywin32\win32" if exist "library\qtwebview2\qtwebview2" (
    echo   依赖已就绪，跳过。
) else (
    call "%~dp0deploy.bat"
    if errorlevel 1 (
        echo.
        echo   [X] 依赖安装失败。请检查网络后重试，或手动运行 deploy.bat 查看详细输出。
        pause
        goto :end
    )
)

echo.
echo ============================================================
echo  [2/3] 安装 MiSans 字体
echo ============================================================
if exist "assets\fonts\MiSans-Regular.woff2" (
    echo   字体已就绪，跳过。
) else (
    call "%~dp0download fonts.bat"
)

echo.
echo ============================================================
echo  [3/3] 启动 NWbrowser
echo ============================================================
echo.
echo   注意：主程序是系统托盘程序，启动后不会弹出主界面。
echo   请看任务栏右下角的通知区域，点「^」展开隐藏图标找它。
echo   托盘图标：左键打开悬浮条，右键出菜单。
echo.
timeout /t 3 /nobreak >nul
python "%~dp0main.py"

:end
popd
echo.
echo 已退出。
pause

```

### search_engines.json (大小: 278 | 修改时间: 2026-10-03 11:49:12 | 权限: 666)

```
{
  "engines": [
    {
      "abbr": "BI",
      "url": "https://www.bing.com/search?q=%s"
    },
    {
      "abbr": "GO",
      "url": "https://www.google.com/search?q=%s"
    },
    {
      "abbr": "BA",
      "url": "https://www.baidu.com/s?wd=%s"
    }
  ]
}
```

### THIRD-PARTY-NOTICES.txt (大小: 7073 | 修改时间: 2026-10-03 10:52:36 | 权限: 666)

```
NWbrowser 第三方组件与字体声明
================================================================
Third-Party Notices and Font Attribution
================================================================

本文件是 README「第三方组件与声明」一节的独立副本，随程序一起分发。
This file is a standalone copy of the "Third-party notices" section of the
README, distributed alongside the program.


1. MiSans 字体声明（重要）
----------------------------------------------------------------

本软件使用了 **MiSans 字体**。

MiSans 由小米（Xiaomi Inc.）提供，为全球免费商用字体。但依据其许可协议
《MiSans 字体知识产权许可协议》的要求，使用方**必须在软件中明确注明使用了
MiSans 字体**。本文件即该声明。

  * 字体来源：https://hyperos.mi.com/font/
  * 许可协议：https://hyperos.mi.com/font/

限制：
  * 不得修改 MiSans 的字形外观或其组成部分
  * 不得单独销售字体文件本身
  * 可以调整字重、字距等排版参数

本软件在 assets/fonts/ 下以 woff2 形式内嵌了 MiSans 的多个字重，
仅用于界面显示。


1. MiSans Font Notice (IMPORTANT)
----------------------------------------------------------------

This software uses the **MiSans** font.

MiSans is provided by Xiaomi Inc. and is free for global commercial use.
However, its license — the *MiSans Font Intellectual Property License
Agreement* — requires that software embedding the font **explicitly note
that MiSans is used**. This file serves as that notice.

  * Source:  https://hyperos.mi.com/font/
  * License: https://hyperos.mi.com/font/

Restrictions:
  * The glyph appearance of MiSans and its components may not be altered
  * The font files themselves may not be sold separately
  * Adjusting weight, spacing and similar typographic parameters is allowed

This software embeds several MiSans weights as woff2 under assets/fonts/,
used solely for UI rendering.


2. 第三方软件组件
----------------------------------------------------------------

组件                       版本       许可证                    用途
--------------------------------------------------------------------------
PyQt6                      6.11.0     GPL-3.0-only              Qt6 界面框架
Qt 6                       6.11.0     LGPL-3.0 / GPL-3.0        UI 底层
qtwebview2                 2.1.1      MIT-0                     WebView2 桥接
wryview                    0.4.0      MPL-2.0                   WebView2 宿主(Rust)
pywin32                    312        PSF-2.0                   Win32 API
comtypes                   1.4.17     MIT                       COM
QtPy                       2.4.3      MIT                       Qt 绑定兼容层
cffi                       2.1.1      MIT-0                     C 扩展调用
clr_loader                 0.3.1      MIT                       .NET 运行时加载
packaging                  26.3       Apache-2.0 / BSD-2-Clause 版本解析
typing_extensions          4.16.0     PSF-2.0                   类型标注兼容
psutil                     7.2.2      BSD-3-Clause              进程/系统信息
watchdog                   6.0.0      Apache-2.0                文件系统监控
browser-oxide              0.1.3      MIT / Apache-2.0          可选，默认不打包
Microsoft WebView2         —          Microsoft 软件许可条款     浏览器内核


2. Third-Party Software Components
----------------------------------------------------------------

Component                  Version    License                   Purpose
--------------------------------------------------------------------------
PyQt6                      6.11.0     GPL-3.0-only              Qt6 bindings
Qt 6                       6.11.0     LGPL-3.0 / GPL-3.0        UI framework
qtwebview2                 2.1.1      MIT-0                     WebView2 bridge
wryview                    0.4.0      MPL-2.0                   WebView2 host (Rust)
pywin32                    312        PSF-2.0                   Win32 API
comtypes                   1.4.17     MIT                       COM
QtPy                       2.4.3      MIT                       Qt binding shim
cffi                       2.1.1      MIT-0                     C extension calls
clr_loader                 0.3.1      MIT                       .NET runtime loading
packaging                  26.3       Apache-2.0 / BSD-2-Clause version parsing
typing_extensions          4.16.0     PSF-2.0                   typing backports
psutil                     7.2.2      BSD-3-Clause              process/system info
watchdog                   6.0.0      Apache-2.0                filesystem monitoring
browser-oxide              0.1.3      MIT / Apache-2.0           optional, not bundled
Microsoft WebView2         —          Microsoft Software        browser engine
                                      License Terms


3. 关于 PyQt6 的许可证（分发者必读）
----------------------------------------------------------------

PyQt6 采用 **GPL-3.0-only**。因此任何基于本项目的分发都必须同样以
GPL 兼容的方式开源。这也是本项目选择 GPL-3.0-or-later 的原因之一。

若需闭源分发，须另行向 Riverbank Computing 购买 PyQt 商业授权。


3. A Note on PyQt6's License (FOR DISTRIBUTORS)
----------------------------------------------------------------

PyQt6 is **GPL-3.0-only**. Any distribution of this project must therefore
also be open-sourced under a GPL-compatible license — one of the reasons this
project is GPL-3.0-or-later.

For closed-source distribution you would need a commercial PyQt license from
Riverbank Computing.


4. 本项目自身
----------------------------------------------------------------

NWbrowser
Copyright (C) 2026 NWbrowser contributors

本程序是自由软件：你可以依据自由软件基金会发布的 GNU 通用公共许可证
（第三版或任何更新版本）的条款重新分发和/或修改它。

本程序分发时希望它有用，但不提供任何担保，甚至不提供适销性或特定用途
适用性的默示担保。详情请见 GNU 通用公共许可证。

完整许可证文本见随附的 LICENSE 文件，或访问：
https://www.gnu.org/licenses/gpl-3.0.html


4. This Project
----------------------------------------------------------------

NWbrowser
Copyright (C) 2026 NWbrowser contributors

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

The full license text is in the accompanying LICENSE file, or at:
https://www.gnu.org/licenses/gpl-3.0.html

```

### version_info.txt (大小: 1185 | 修改时间: 2026-10-03 02:48:47 | 权限: 666)

```
# UTF-8
# PyInstaller 版本资源：让 exe 属性页显示正确的产品信息。
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '080404B0',
          [
            StringStruct('CompanyName', 'NWbrowser contributors'),
            StringStruct('FileDescription', 'NWbrowser 浏览器'),
            StringStruct('FileVersion', '1.0.0.0'),
            StringStruct('InternalName', 'NWbrowser'),
            StringStruct('LegalCopyright', 'Copyright (C) 2026 NWbrowser contributors. Licensed under the GNU General Public License v3.0 or later.'),
            StringStruct('OriginalFilename', 'NWbrowser.exe'),
            StringStruct('ProductName', 'NWbrowser'),
            StringStruct('ProductVersion', '1.0.0.0'),
            StringStruct('Comments', 'Free software under GPL-3.0-or-later. Comes with ABSOLUTELY NO WARRANTY.')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [0x0804, 1200])])
  ]
)

```
