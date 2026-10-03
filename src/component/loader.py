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