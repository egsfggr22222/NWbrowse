@echo off
chcp 936 >nul
pushd "%~dp0"
title NWbrowser 一键准备与运行

echo ============================================================
echo  NWbrowser 一键准备并运行
echo ============================================================
echo.
echo  这个脚本依次做三件事：
echo    1. 安装依赖到 library\   （deploy.bat）
echo    2. 安装 MiSans 字体      （download fonts.bat）
echo    3. 启动程序              （python main.py）
echo.
echo  已装好的步骤会自动跳过，可以放心重复运行。
echo  按 Ctrl+C 可以随时中止。
echo.
pause

echo.
echo ============================================================
echo  [1/3] 安装依赖
echo ============================================================
if exist "library\PyQt6\PyQt6" if exist "library\pywin32\win32" if exist "library\qtwebview2\qtwebview2" (
    echo   依赖已就绪，跳过。
) else (
    call "%~dp0deploy.bat"
    if errorlevel 1 (
        echo.
        echo   [X] 依赖安装失败。请检查网络后重试，或手动运行 deploy.bat 查看详细输出。
        pause
        goto :end
    )
)

echo.
echo ============================================================
echo  [2/3] 安装 MiSans 字体
echo ============================================================
if exist "assets\fonts\MiSans-Regular.woff2" (
    echo   字体已就绪，跳过。
) else (
    call "%~dp0download fonts.bat"
)

echo.
echo ============================================================
echo  [3/3] 启动 NWbrowser
echo ============================================================
echo.
echo   注意：主程序是系统托盘程序，启动后不会弹出主界面。
echo   请看任务栏右下角的通知区域，点「^」展开隐藏图标找它。
echo   托盘图标：左键打开悬浮条，右键出菜单。
echo.
timeout /t 3 /nobreak >nul
python "%~dp0main.py"

:end
popd
echo.
echo 已退出。
pause
