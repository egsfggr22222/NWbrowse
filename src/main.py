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
