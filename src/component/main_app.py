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