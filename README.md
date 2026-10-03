# NWbrowser

**基于 WebView2 的多进程 Windows 浏览器 —— 系统托盘主进程 + 悬浮条 + 多窗口**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![Platform](https://img.shields.io/badge/platform-Windows%2010%2B-lightgrey)
![Python](https://img.shields.io/badge/python-3.10-3776ab)

---


### 这是什么

NWbrowser 是一个 Windows 桌面浏览器。它不用 QtWebEngine，而是把微软的
**WebView2（Edge/Chromium 内核）**通过 `qtwebview2` 嵌进 Qt 界面里，
因此安装体积小、网页兼容性等同于 Edge。

它的架构不是"一个窗口一个程序"，而是**进程分工**：常驻一个系统托盘主进程，
按需拉起悬浮条、浏览器窗口、设置窗口和下载管理进程，彼此用本地 IPC 通信。
这样关掉所有窗口后，托盘仍在，随时唤回上次的会话。

### 主要特性

| 功能 | 说明 |
|---|---|
| **系统托盘常驻** | 主进程就是托盘。关窗口不退程序，托盘菜单可开新窗口/设置/下载/退出 |
| **悬浮条** | 贴边的工具条，滚动切换**固定项**，点图钉开对应站点；不占任务栏 |
| **固定项（Pinned）** | 把常用站点钉住，独立记忆每个站点的多个入口 URL 和上次浏览位置 |
| **多窗口 + 会话共享** | 站点登录态跟着站点走；无痕窗口独立隔离，不留痕迹 |
| **个性化** | 主题色 + 背景图（缩略图网格、右键删除、清空），逐窗口记忆 |
| **下载管理** | 独立下载进程，进度/完成气泡通知，支持取消与断点信息 |
| **完成提醒** | 见下方「完成提醒」小节 |
| **隐私控制** | 三级跟踪防护、第三方 Cookie 开关、权限（摄像头/麦克风/定位/通知）逐项策略 |
| **多语言** | 简体中文 / English / Русский 三套语言包，运行时热切换 |

### 完成提醒（W 态检测）

针对"页面在**没有用户操作**的情况下自己持续加载"的场景（长列表懒加载、
自动翻页、前端分片渲染等），NWbrowser 内置了一个 JS 侧的状态机：

- 用户操作（滚动/点击/键盘/跳转）后 **1000ms 内**插入的 DOM 节点 → 记为 `lazy`
- 没有用户操作时插入的节点 → 记为 `new`
- 每 300ms 归并成一条记录，只看最近 **10 条**
- **IDLE 态**：`new >= 7` → 进入 **W 态**
- **W 态**：`lazy >= 7` → 判定为人为操作触发，**不提醒**
- **5 秒没有新增**：
  - W 态 → **自然死亡** → **响一声 + 强制窗口置顶**（提醒你"它加载完了"）
  - IDLE 态 → 自然死亡但**不提醒**

开关位置：**标题栏「⋯」菜单 →「完成提醒」**。

> 这个开关是**按站点记忆**的（存在 `userdata/complete_notify.json`），
> 打开一次之后重开窗口仍然生效。

### 进程架构

```
main_app.py（托盘主进程）
├── floating_bar.py      悬浮条（同时负责调度窗口进程、持有 Job Object）
├── window.py --id df-N  浏览器窗口（每窗口一个进程）
├── settings_app.py      设置窗口
└── downloads_app.py     下载管理
        └── download_worker.py   下载工作进程（每任务一个）

        通信：QLocalServer / QLocalSocket
        注册：%TEMP%\browser_ipc_registry.json
```

- 托盘是父进程：子进程意外退出会自动重新拉起（正常退出流程除外）
- 悬浮条持有 **Job Object（KILL_ON_JOB_CLOSE）**，保证整个进程组一起回收，
  不会留下孤儿进程
- 关闭软件时先给窗口发 `MSG_QUIT` 走**优雅退出**（WebView2 正常析构、
  profile 落盘），1.2 秒内没退的才强制结束

### 运行要求

- **Windows 10 1809 及以上**（64 位）
- **WebView2 Runtime** —— Windows 11 和大部分 Windows 10 已自带；
  没有的话去 [微软官网](https://developer.microsoft.com/microsoft-edge/webview2/) 装 Evergreen 版
- 源码运行需要 **Python 3.10 x64**

### 从源码运行

```bat
:: 1. 装依赖到项目内的 library\（不污染全局 Python）
deploy.bat

:: 2. 运行
python component\main_app.py
```

> `deploy.bat` 会把依赖装进 `library\`，程序运行时从那里加载，**不需要 venv**。
> 其中 `qtwebview2` 不在 PyPI，脚本会从 GitHub 拉取（内置多个镜像兜底）。

### 打包

```bat
:: 打包成 onedir 目录（输出到 %USERPROFILE%\Desktop\NWbrowser）
browser_project\build_app.bat
```

> ⚠️ **构建产物不要放在受沙箱/受限环境管辖的目录里**，否则会出现
> "托盘没图标""onefile 解压失败"这类假故障。

### 数据存放位置

程序是**绿色**的：所有用户数据都在 exe 同级的目录下。

```
NWbrowser.exe
settings.json              设置（主题、语言、隐私开关…）
history.json               浏览历史
favorites.json             书签
downloads.json             下载记录
passwords.json             保存的登录信息
fixed\                     固定项（每个站点一个文件夹）
userdata\
  profile\EBWebView\       ← WebView2 用户数据：Cookie / 登录态 / localStorage
  search_icons\            搜索引擎图标缓存
  complete_notify.json     完成提醒的按站点开关
```

- **关闭软件不会丢登录态**（优雅退出，profile 正常落盘）
- **卸载会一并删除**这些数据（安装目录整个删掉）
- 想把数据放到别处：在 `settings.json` 里改 `env.user_data_folder`

### 许可证

**GNU General Public License v3.0 or later**（GPL-3.0-or-later）。
完整文本见 [LICENSE](LICENSE)。

```
Copyright (C) 2026 NWbrowser contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
```

### 第三方组件与声明

本项目**使用了以下第三方组件**，它们各自的许可证如下。
**MiSans 字体按其许可协议要求，在此明确声明。**

| 组件 | 版本 | 许可证 | 用途 |
|---|---|---|---|
| [PyQt6](https://pypi.org/project/PyQt6/) | 6.11.0 | **GPL-3.0-only** | Qt6 界面框架 |
| [Qt 6](https://www.qt.io/) | 6.11.0 | LGPL-3.0 / GPL-3.0 | PyQt6 底层 |
| [qtwebview2](https://github.com/xiaosuawa/QtWebView) | 2.1.1 | MIT-0 | WebView2 与 Qt 的桥接 |
| [wryview](https://pypi.org/project/wryview/) | 0.4.0 | **MPL-2.0** | WebView2 宿主（Rust） |
| [pywin32](https://pypi.org/project/pywin32/) | 312 | PSF-2.0 | Win32 API |
| [comtypes](https://pypi.org/project/comtypes/) | 1.4.17 | MIT | COM（任务栏 ITaskbarList 等） |
| [QtPy](https://pypi.org/project/QtPy/) | 2.4.3 | MIT | Qt 绑定兼容层 |
| [cffi](https://pypi.org/project/cffi/) | 2.1.1 | MIT-0 | C 扩展调用 |
| [clr_loader](https://pypi.org/project/clr-loader/) | 0.3.1 | MIT | .NET 运行时加载 |
| [packaging](https://pypi.org/project/packaging/) | 26.3 | Apache-2.0 / BSD-2-Clause | 版本解析 |
| [typing_extensions](https://pypi.org/project/typing-extensions/) | 4.16.0 | PSF-2.0 | 类型标注兼容 |
| [psutil](https://pypi.org/project/psutil/) | 7.2.2 | BSD-3-Clause | 进程与系统信息 |
| [watchdog](https://pypi.org/project/watchdog/) | 6.0.0 | Apache-2.0 | 文件系统监控 |
| [browser-oxide](https://pypi.org/project/browser-oxide/) | 0.1.3 | MIT / Apache-2.0 | （可选，默认不打包） |
| **MiSans 字体** | — | **小米 MiSans 字体知识产权许可协议** | 界面字体 |
| Microsoft **WebView2** | — | Microsoft 软件许可条款 | 浏览器内核 |

#### MiSans 字体声明

> This software uses the **MiSans** font, which is provided by Xiaomi Inc.
> MiSans is a free font for global commercial use, but per its license
> (MiSans Font Intellectual Property License Agreement), we specifically
> note here that **MiSans is used in this software as an embedded/UI font**.
>
> 本软件使用**小米 MiSans 字体**。MiSans 为全球免费商用字体，但依据其
> 许可协议要求，特此在软件中明确声明：**本软件使用了 MiSans 字体**。
>
> 字体来源：<https://hyperos.mi.com/font/>
> 不得修改 MiSans 的字形外观；不得单独销售字体文件本身。

#### 关于 PyQt6 的许可证

PyQt6 采用 **GPL-3.0-only**。因此任何基于本项目的分发都必须**同样以 GPL 兼容
的方式开源** —— 这也是本项目选择 GPL-3.0-or-later 的原因之一。
（若需闭源分发，须另行向 Riverbank Computing 购买 PyQt 商业授权。）

---

### What is this

NWbrowser is a Windows desktop browser. Instead of QtWebEngine it embeds
Microsoft **WebView2 (Edge/Chromium)** through `qtwebview2`, so the install
stays small and page compatibility matches Edge.

It is not "one window, one program". A tray-resident main process spawns the
floating bar, browser windows, the settings window and the download manager
on demand, and they talk over local IPC. Close every window and the tray is
still there to bring your session back.

### Highlights

| Feature | Description |
|---|---|
| **Tray-resident** | The tray *is* the main process. Closing windows does not quit the app |
| **Floating bar** | An edge-docked strip; scroll to switch **pinned** sites, click a pin to open it |
| **Pinned sites** | Each pinned host remembers its own entry URLs and last position |
| **Multi-window** | Login state follows the *site*, not the window; incognito windows stay isolated |
| **Personalization** | Theme color + background images, remembered per window |
| **Downloads** | Dedicated download process with progress and completion toasts |
| **Completion alert** | See "Completion alert" below |
| **Privacy** | Three tracking-protection levels, third-party cookie switch, per-capability permission policy |
| **i18n** | Simplified Chinese / English / Russian, hot-swappable |

### Completion alert (the "W state" detector)

For pages that keep loading **without any user interaction** (infinite scroll,
auto-pagination, chunked rendering), NWbrowser runs a small JS state machine:

- DOM nodes inserted **within 1000 ms** of a user action (scroll/click/key/URL
  change) are tagged `lazy`
- Nodes inserted with no recent user action are tagged `new`
- Every 300 ms the batch is folded into one record; only the latest **10** are kept
- **IDLE state**: `new >= 7` → enter **W state**
- **W state**: `lazy >= 7` → judged as user-driven, **no alert**
- **5 seconds with no new nodes**:
  - W state → **natural death** → **play a sound and force the window on top**
  - IDLE state → natural death, **silent**

Toggle: **title bar "⋯" menu → "Complete notify"**.
It is remembered **per site** (`userdata/complete_notify.json`), so it survives
window restarts.

### Process architecture

```
main_app.py (tray main process)
├── floating_bar.py      floating bar; also spawns windows, owns the Job Object
├── window.py --id df-N  browser window (one process each)
├── settings_app.py      settings window
└── downloads_app.py     download manager
        └── download_worker.py   one worker process per download

        IPC:    QLocalServer / QLocalSocket
        Registry: %TEMP%\browser_ipc_registry.json
```

- The tray is the parent: a child that dies unexpectedly is respawned
  (except during a normal quit)
- The floating bar owns a **Job Object (KILL_ON_JOB_CLOSE)**, so the whole
  process group is reclaimed together — no orphans
- On quit, windows get `MSG_QUIT` first for a **graceful shutdown** (WebView2
  tears down properly and the profile is flushed); only stragglers are killed
  after 1.2 s

### Requirements

- **Windows 10 1809 or later**, 64-bit
- **WebView2 Runtime** — bundled with Windows 11 and most Windows 10 builds;
  otherwise install the Evergreen runtime from
  [Microsoft](https://developer.microsoft.com/microsoft-edge/webview2/)
- **Python 3.10 x64** to run from source

### Run from source

```bat
:: 1. install dependencies into the project's library\ (no global pollution)
deploy.bat

:: 2. run
python component\main_app.py
```

> `deploy.bat` installs into `library\`; the app loads from there at runtime,
> so **no virtualenv is required**. `qtwebview2` is not on PyPI — the script
> pulls it from GitHub with several mirror fallbacks.

### Build

```bat
:: build an onedir bundle (outputs to %USERPROFILE%\Desktop\NWbrowser)
browser_project\build_app.bat
```

> ⚠️ Do **not** build into a sandboxed/restricted directory, or you will hit
> phantom failures such as "tray icon missing" or "onefile cannot extract".

### Where data lives

The app is portable: everything sits next to the executable.

```
NWbrowser.exe
settings.json              settings (theme, language, privacy…)
history.json               browsing history
favorites.json             bookmarks
downloads.json             download records
passwords.json             saved logins
fixed\                     pinned sites (one folder per host)
userdata\
  profile\EBWebView\       WebView2 user data: cookies / logins / localStorage
  search_icons\            cached search-engine icons
  complete_notify.json     per-site completion-alert toggle
```

- **Quitting does not lose your logins** (graceful shutdown flushes the profile)
- **Uninstalling deletes all of it** (the install directory is removed)
- To relocate: change `env.user_data_folder` in `settings.json`

### License

**GNU General Public License v3.0 or later** (GPL-3.0-or-later).
See [LICENSE](LICENSE) for the full text.

```
Copyright (C) 2026 NWbrowser contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
```

### Third-party notices

This project **bundles and uses the third-party components listed below**.
Per its license, the use of **MiSans** is explicitly noted here.

| Component | Version | License | Purpose |
|---|---|---|---|
| [PyQt6](https://pypi.org/project/PyQt6/) | 6.11.0 | **GPL-3.0-only** | Qt6 bindings |
| [Qt 6](https://www.qt.io/) | 6.11.0 | LGPL-3.0 / GPL-3.0 | UI framework |
| [qtwebview2](https://github.com/xiaosuawa/QtWebView) | 2.1.1 | MIT-0 | WebView2 ⇄ Qt bridge |
| [wryview](https://pypi.org/project/wryview/) | 0.4.0 | **MPL-2.0** | WebView2 host (Rust) |
| [pywin32](https://pypi.org/project/pywin32/) | 312 | PSF-2.0 | Win32 API |
| [comtypes](https://pypi.org/project/comtypes/) | 1.4.17 | MIT | COM (ITaskbarList, …) |
| [QtPy](https://pypi.org/project/QtPy/) | 2.4.3 | MIT | Qt binding shim |
| [cffi](https://pypi.org/project/cffi/) | 2.1.1 | MIT-0 | C extension calls |
| [clr_loader](https://pypi.org/project/clr-loader/) | 0.3.1 | MIT | .NET runtime loading |
| [packaging](https://pypi.org/project/packaging/) | 26.3 | Apache-2.0 / BSD-2-Clause | version parsing |
| [typing_extensions](https://pypi.org/project/typing-extensions/) | 4.16.0 | PSF-2.0 | typing backports |
| [psutil](https://pypi.org/project/psutil/) | 7.2.2 | BSD-3-Clause | process/system info |
| [watchdog](https://pypi.org/project/watchdog/) | 6.0.0 | Apache-2.0 | filesystem monitoring |
| [browser-oxide](https://pypi.org/project/browser-oxide/) | 0.1.3 | MIT / Apache-2.0 | optional, not bundled by default |
| **MiSans font** | — | **Xiaomi MiSans Font IP License Agreement** | UI font |
| Microsoft **WebView2** | — | Microsoft Software License Terms | browser engine |

#### MiSans notice

> This software uses the **MiSans** font, provided by Xiaomi Inc.
> MiSans is free for global commercial use; per its license
> (MiSans Font Intellectual Property License Agreement) we explicitly note
> here that **MiSans is used in this software**.
>
> Source: <https://hyperos.mi.com/font/>
> The glyph appearance of MiSans may not be altered, and the font files
> themselves may not be sold separately.

#### A note on PyQt6's license

PyQt6 is **GPL-3.0-only**. Any distribution of this project must therefore
also be open-sourced under a GPL-compatible license — one of the reasons this
project is GPL-3.0-or-later. For closed-source distribution you would need a
commercial PyQt license from Riverbank Computing.

---

## 参与贡献 / Contributing

Issue 和 Pull Request 都欢迎。
Issues and pull requests are welcome.

提交前请确保 / Before submitting, please make sure:

- 源码模式下 `python component\main_app.py` 能正常启动
- `python main.py --role selftest` 输出 `RESULT = PASS`
- 没有把个人数据（`settings.json` / `history.json` / `userdata\`）提交进来
