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