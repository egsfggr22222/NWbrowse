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
