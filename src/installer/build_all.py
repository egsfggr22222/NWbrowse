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

WS = r"C:\Users\computer\Desktop\DSH workspace"
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
