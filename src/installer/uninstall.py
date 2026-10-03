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
