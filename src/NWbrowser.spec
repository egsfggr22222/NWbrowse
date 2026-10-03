# -*- mode: python ; coding: utf-8 -*-
"""NWbrowser PyInstaller 打包配置（onedir）。

资源落位必须和 component/apppaths.py 的约定严格对应：

    _internal/i18n/*.json      <- component/i18n/*.json   (= COMPONENT_DIR/i18n)
    _internal/assets/fonts/*   <- assets/fonts/*          (= RES_DIR/assets/fonts)
    _internal/data/*.ico       <- data/*.ico              (= RES_DIR/data)

用户数据（settings.json / history.json / userdata/ / fixed/ ...）**不打进包里**，
运行时读写 exe 同级目录 —— 也就是 APP_DIR，和源码模式的"项目根"一一对应。

构建：
    build_app.bat                                （推荐，会顺手设好 PYTHONPATH）
    python -m PyInstaller NWbrowser.spec --noconfirm

注意：PyInstaller 的 pywin32 / PyQt6 hook 会在子进程里 import 这些包，
只靠下面的 pathex 不够，**构建时必须设置 PYTHONPATH**（build_app.bat 已处理）。
"""

import os

from PyInstaller.utils.hooks import collect_submodules


# ======================================================================
# 开关
# ======================================================================
#: browser_oxide 是 ~72MB 的 Rust 原生扩展，代码里零使用点。
#: loader.py 已经改成"缺失也不报错"，所以默认不打包。要带上就改 True。
INCLUDE_BROWSER_OXIDE = False


# ======================================================================
# 路径
# ======================================================================
PROJECT_ROOT = os.path.abspath(SPECPATH)          # noqa: F821 - PyInstaller 注入
LIB = os.path.join(PROJECT_ROOT, "library")
COMPONENT = os.path.join(PROJECT_ROOT, "component")
DATA = os.path.join(PROJECT_ROOT, "data")
ASSETS = os.path.join(PROJECT_ROOT, "assets")

pathex = [
    PROJECT_ROOT,
    COMPONENT,
    LIB,
    os.path.join(LIB, "browser-oxide"),
    os.path.join(LIB, "PyQt6"),
    os.path.join(LIB, "qtwebview2"),
    os.path.join(LIB, "pywin32"),
    os.path.join(LIB, "pywin32", "win32"),
    os.path.join(LIB, "pywin32", "win32", "lib"),
]


# ======================================================================
# 随包发布的只读资源
# ======================================================================
datas = []

# 语言文件 -> _internal/i18n/
_i18n = os.path.join(COMPONENT, "i18n")
if os.path.isdir(_i18n):
    for _n in sorted(os.listdir(_i18n)):
        if _n.endswith(".json"):
            datas.append((os.path.join(_i18n, _n), "i18n"))

# 字体 -> _internal/assets/fonts/（跳过 macOS 的 ._* 与隐藏文件）
_fonts = os.path.join(ASSETS, "fonts")
if os.path.isdir(_fonts):
    for _n in sorted(os.listdir(_fonts)):
        if _n.startswith("."):
            continue
        _p = os.path.join(_fonts, _n)
        if os.path.isfile(_p):
            datas.append((_p, "assets/fonts"))

# 内置背景图 -> _internal/assets/backgrounds/
# settings.json 里以 "{RES}/assets/backgrounds/xxx.jpg" 引用，
# 运行时由 settings.resolve_path() 展开成 RES_DIR 下的真实路径。
_bgs = os.path.join(ASSETS, "backgrounds")
if os.path.isdir(_bgs):
    for _n in sorted(os.listdir(_bgs)):
        if _n.startswith("."):
            continue
        _p = os.path.join(_bgs, _n)
        if os.path.isfile(_p):
            datas.append((_p, "assets/backgrounds"))

# 图标 -> _internal/data/
if os.path.isdir(DATA):
    for _n in sorted(os.listdir(DATA)):
        _p = os.path.join(DATA, _n)
        if os.path.isfile(_p) and _n.lower().endswith((".ico", ".png")):
            datas.append((_p, "data"))


# ======================================================================
# 隐藏导入
# ======================================================================
hiddenimports = [
    # UI
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtNetwork",
    "PyQt6.QtWidgets",
    "PyQt6.sip",
    # Windows API（vendored pywin32）
    "win32api",
    "win32con",
    "win32gui",
    "pywintypes",
    "pythoncom",
    "win32com",
    "win32com.client",
    # COM（任务栏 ITaskbarList）
    "comtypes",
    "comtypes.client",
    # WebView2 内核
    "qtwebview2",
    "qtwebview2._bridge",
    "qtwebview2.widget",
    "qtwebview2._anchor",
    "wryview",
    "wryview._core",
    # qtwebview2 硬依赖 qtpy，qtpy 又依赖 packaging —— 缺一个 WebView2 就起不来
    "qtpy",
    "qtpy.QtCore",
    "qtpy.QtGui",
    "qtpy.QtWidgets",
    "qtpy.sip",
    "packaging",
    "packaging.version",
    "typing_extensions",
]

if INCLUDE_BROWSER_OXIDE:
    hiddenimports.append("browser_oxide")

# 这几个包结构不透明，整包子模块全抓。
# 注意别把 comtypes / win32com 整包抓进来：它们的 test/ demos/ 会连带拖进
# setuptools、pythonwin、pyreadline3，体积翻几倍且全无用处。
for _pkg in ("qtwebview2", "wryview"):
    try:
        hiddenimports += collect_submodules(_pkg)
    except Exception as _e:            # pragma: no cover
        print("[spec] collect_submodules(%s) 失败: %s" % (_pkg, _e))

hiddenimports = sorted(set(hiddenimports))


# ======================================================================
# 排除
# ======================================================================
excludes = [
    # 本项目用 WebView2，不用 QtWebEngine
    "PyQt6.QtWebEngineCore",
    "PyQt6.QtWebEngineWidgets",
    "PyQt6.QtWebEngineQuick",
    # Qt 全家桶里没用到的（Qt6/qml、Quick3D 动辄上百 MB）
    "PyQt6.QtQml",
    "PyQt6.QtQuick",
    "PyQt6.QtQuick3D",
    "PyQt6.QtQuickWidgets",
    "PyQt6.QtMultimedia",
    "PyQt6.QtMultimediaWidgets",
    "PyQt6.QtBluetooth",
    "PyQt6.QtNfc",
    "PyQt6.QtSensors",
    "PyQt6.QtSerialPort",
    "PyQt6.QtTest",
    "PyQt6.QtDesigner",
    "PyQt6.QtHelp",
    "PyQt6.QtSql",
    "PyQt6.QtPdf",
    "PyQt6.QtPdfWidgets",
    "PyQt6.QtPositioning",
    "PyQt6.QtRemoteObjects",
    "PyQt6.QtSpatialAudio",
    "PyQt6.QtTextToSpeech",
    "PyQt6.QtDBus",
    "PyQt6.Qsci",
    "PyQt6.uic",
    "PyQt6.lupdate",
    # pythonnet 遗留依赖（wryview 是 Rust 扩展，不需要 CLR）
    "clr",
    "clr_loader",
    "pythonnet",
    "cffi",
    "pycparser",
    # deploy.bat 装了但代码里没 import
    "psutil",
    "watchdog",
    # comtypes / win32com 的测试与示例
    "comtypes.test",
    "win32com.test",
    "win32com.demos",
    "win32com.axdebug",
    "win32com.axscript",
    "win32com.mapi",
    "win32com.ifilter",
    "win32com.directsound",
    "win32com.propsys",
    "win32com.bits",
    "win32com.taskscheduler",
    "win32com.internet",
    "win32com.servers",
    "win32com.makegw",
    "win32com.authorization",
    "win32com.adsi",
    "win32com.axcontrol",
    "pythonwin",
    "pyreadline3",
    "setuptools",
    "distutils",
    # 明显不相关的大块头
    "tkinter",
    "unittest",
    "pydoc_data",
    "lib2to3",
    "numpy",
    "PIL",
    "matplotlib",
    "IPython",
    "pytest",
]

if not INCLUDE_BROWSER_OXIDE:
    excludes.append("browser_oxide")


# ======================================================================
# 构建
# ======================================================================
a = Analysis(                                   # noqa: F821
    [os.path.join(PROJECT_ROOT, "main.py")],
    pathex=pathex,
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)                               # noqa: F821

exe = EXE(                                      # noqa: F821
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="NWbrowser",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,                 # UPX 压 Qt 的 DLL 容易把程序压坏
    console=False,             # 窗口程序；日志写 exe 同级的 nwbrowser-*.log
    disable_windowed_traceback=True,   # 关掉 PyInstaller 的窗口版异常弹窗；
                                       # 改由 main.py 的 excepthook 写
                                       # nwbrowser-crash-<角色>.log
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=os.path.join(PROJECT_ROOT, "version_info.txt"),
    icon=os.path.join(DATA, "icon.ico"),
)

coll = COLLECT(                                 # noqa: F821
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="NWbrowser",
)
