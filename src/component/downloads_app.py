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