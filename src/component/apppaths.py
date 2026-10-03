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
