@echo off
chcp 936 >nul
pushd "%~dp0"

echo ============================================================
echo  NWbrowser 打包（PyInstaller / onedir）
echo  依赖直接取本目录 library/，构建机不需要 pip 装 PyQt6 等
echo ============================================================
echo.

set "ROOT=%~dp0"
set "LIB=%ROOT%library"
:: 产物必须放在**可写、且不受任何沙箱/受限环境管辖**的位置。
:: 放在项目目录或 DSH workspace 里会导致：Shell_NotifyIcon 被拒（托盘没图标）、
:: onefile 解压 %TEMP% 失败、子进程受限等一堆假故障。
if defined NWBROWSER_OUT (
    set "OUT=%NWBROWSER_OUT%"
) else (
    set "OUT=%USERPROFILE%\Desktop"
)
set "APP=%OUT%\NWbrowser"

:: ------------------------------------------------------------
:: PyInstaller 的 pywin32 / PyQt6 hook 会在子进程里 import 这些包，
:: 只靠 spec 里的 pathex 不够，必须同时设 PYTHONPATH。
:: ------------------------------------------------------------
set "PYTHONPATH=%LIB%;%LIB%\PyQt6;%LIB%\qtwebview2;%LIB%\pywin32;%LIB%\pywin32\win32;%LIB%\pywin32\win32\lib;%LIB%\browser-oxide"

:: ------------------------------------------------------------
:: 前置检查
:: ------------------------------------------------------------
python -c "import sys" >nul 2>&1
if errorlevel 1 (
    echo [X] 找不到 python，请先装 Python 3.10 x64 并加进 PATH
    goto :fail
)
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [X] 没装 PyInstaller，先执行:  python -m pip install pyinstaller
    goto :fail
)
if not exist "%LIB%\PyQt6\PyQt6\QtCore.pyd" (
    echo [X] 缺少 %LIB%\PyQt6，请先运行 deploy.bat
    goto :fail
)
if not exist "%LIB%\qtwebview2\wryview\_core.cp310-win_amd64.pyd" (
    echo [X] 缺少 %LIB%\qtwebview2\wryview，请先运行 deploy.bat
    goto :fail
)

:: ------------------------------------------------------------
:: 清理旧产物
:: ------------------------------------------------------------
if exist "%ROOT%build" rd /s /q "%ROOT%build"
if exist "%APP%" rd /s /q "%APP%"
if not exist "%OUT%" mkdir "%OUT%"

:: ------------------------------------------------------------
:: 构建
:: ------------------------------------------------------------
echo [1/3] PyInstaller 构建中（首次约 3~8 分钟）...
echo.
python -m PyInstaller NWbrowser.spec ^
    --noconfirm ^
    --distpath "%OUT%" ^
    --workpath "%ROOT%build"
if errorlevel 1 (
    echo.
    echo [X] 构建失败，请看上面的报错
    goto :fail
)

:: ------------------------------------------------------------
:: 把当前项目里已有的用户数据复制到 exe 旁边
:: —— 这样打包版一启动就和源码版状态一致
::     （背景图、搜索引擎、收藏、历史、密码、固定项、Cookie）
:: ------------------------------------------------------------
echo.
echo [2/3] 复制现有用户数据到 %APP% ...
for %%F in (settings.json search_engines.json favorites.json history.json downloads.json passwords.json) do (
    if exist "%ROOT%%%F" (
        copy /y "%ROOT%%%F" "%APP%\%%F" >nul
        echo    + %%F
    )
)
for %%D in (fixed userdata cache) do (
    if exist "%ROOT%%%D" (
        robocopy "%ROOT%%%D" "%APP%\%%D" /e /nfl /ndl /njh /njs /np >nul
        echo    + %%D\
    )
)

:: ------------------------------------------------------------
:: 自检
:: ------------------------------------------------------------
echo.
echo [3/3] 跑一次打包自检...
if not exist "%APP%\NWbrowser.exe" (
    echo [X] 没找到 %APP%\NWbrowser.exe
    goto :fail
)
"%APP%\NWbrowser.exe" --role selftest
if errorlevel 1 (
    echo [X] 自检失败，看 %APP%\selftest.txt
    goto :fail
)
echo   自检通过 -> %APP%\selftest.txt

echo.
echo ============================================================
echo  打包完成
echo    程序: %APP%\NWbrowser.exe
echo    数据: 和 exe 同级（settings.json / userdata / fixed ...）
echo.
echo  提示：请把整个 NWbrowser 文件夹放到可写目录（桌面、D:\Apps 等），
echo        不要放 Program Files，否则设置/历史/Cookie 存不下来。
echo ============================================================
echo.
popd
pause
exit /b 0

:fail
echo.
popd
pause
exit /b 1
