@echo off
chcp 936
pushd "%~dp0"

echo ============================================================
echo  部署依赖到 library/
echo  断点续传 + 多代理兜底 + 失败不中断
echo ============================================================
echo.

set "FAILED="
set "ROOT=%~dp0"

:: ------------------------------------------------------------
:: 准备目录
:: ------------------------------------------------------------
if not exist "library" mkdir "library"
if not exist "library\browser-oxide" mkdir "library\browser-oxide"
if not exist "library\PyQt6" mkdir "library\PyQt6"
if not exist "library\pywin32" mkdir "library\pywin32"
if not exist "library\qtwebview2" mkdir "library\qtwebview2"


:: ============================================================
:: [1/9] browser-oxide
:: ============================================================
echo ========== [1/9] browser-oxide ==========
if exist "library\browser-oxide\browser_oxide" (
    echo   已装，跳过
) else (
    pip install browser-oxide --target "%ROOT%library\browser-oxide" --no-warn-script-location
    if errorlevel 1 (echo [!] 1/9 失败 & set FAILED=%FAILED% 1)
)


:: ============================================================
:: [2/9] PyQt6
:: ============================================================
echo.
echo ========== [2/9] PyQt6 ==========
if exist "library\PyQt6\PyQt6" (
    echo   已装，跳过
) else (
    pip install PyQt6==6.11.0 --target "%ROOT%library\PyQt6" --no-warn-script-location
    if errorlevel 1 (echo [!] 2/9 失败 & set FAILED=%FAILED% 2)
)


:: ============================================================
:: [3/9] pywin32
:: ============================================================
echo.
echo ========== [3/9] pywin32 ==========
if exist "library\pywin32\win32" (
    echo   已装，跳过
) else (
    pip install pywin32==312 --target "%ROOT%library\pywin32" --no-warn-script-location
    if errorlevel 1 (echo [!] 3/9 失败 & set FAILED=%FAILED% 3)
)


:: ============================================================
:: [4/9] qtwebview2（GitHub，五层兜底）
:: ============================================================
echo.
echo ========== [4/9] qtwebview2 ==========
if exist "library\qtwebview2\qtwebview2" (
    echo   已装，跳过
) else (
    set "QTWV_OK="

    echo   [1/5] 直连 GitHub ...
    pip install git+https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if not errorlevel 1 set "QTWV_OK=1"

    if not defined QTWV_OK (
        echo   [2/5] 代理 ghproxy.com ...
        pip install git+https://ghproxy.com/https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
        if not errorlevel 1 set "QTWV_OK=1"
    )

    if not defined QTWV_OK (
        echo   [3/5] 代理 gh-proxy.com ...
        pip install git+https://gh-proxy.com/https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
        if not errorlevel 1 set "QTWV_OK=1"
    )

    if not defined QTWV_OK (
        echo   [4/5] 代理 ghfast.top ...
        pip install git+https://ghfast.top/https://github.com/xiaosuawa/QtWebView.git --target "%ROOT%library\qtwebview2" --no-warn-script-location
        if not errorlevel 1 set "QTWV_OK=1"
    )

    if not defined QTWV_OK (
        if exist "%ROOT%QtWebView.zip" (
            echo   [5/5] 本地 QtWebView.zip ...
            if exist "%TEMP%\QtWebView" rd /s /q "%TEMP%\QtWebView"
            powershell -NoProfile -Command "Expand-Archive -Path '%ROOT%QtWebView.zip' -DestinationPath '%TEMP%\QtWebView' -Force"
            pip install "%TEMP%\QtWebView" --target "%ROOT%library\qtwebview2" --no-warn-script-location
            if not errorlevel 1 set "QTWV_OK=1"
        ) else (
            echo   [5/5] 跳过（项目根目录没有 QtWebView.zip）
        )
    )

    if not defined QTWV_OK (
        echo [!] 4/9 qtwebview2 全部失败
        set FAILED=%FAILED% 4
    ) else (
        echo   qtwebview2 安装成功
    )
)


:: ============================================================
:: [5/9] qtwebview2 核心依赖
:: ============================================================
echo.
echo ========== [5/9] qtpy + pythonnet ==========
if exist "library\qtwebview2\qtpy" (
    echo   已装，跳过
) else (
    pip install qtpy==2.4.3 pythonnet==3.1.0 --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if errorlevel 1 (echo [!] 5/9 失败 & set FAILED=%FAILED% 5)
)


:: ============================================================
:: [6/9] pythonnet 传递依赖
:: ============================================================
echo.
echo ========== [6/9] cffi / clr_loader / packaging / pycparser / typing_extensions ==========
if exist "library\qtwebview2\clr_loader" (
    echo   已装，跳过
) else (
    pip install cffi==2.1.1 clr_loader==0.3.1 packaging==26.3 pycparser==3.0 typing_extensions==4.16.0 --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if errorlevel 1 (echo [!] 6/9 失败 & set FAILED=%FAILED% 6)
)


:: ============================================================
:: [7/9] wryview
:: ============================================================
echo.
echo ========== [7/9] wryview ==========
if exist "library\qtwebview2\wryview" (
    echo   已装，跳过
) else (
    pip install wryview==0.4.0 --target "%ROOT%library\qtwebview2" --no-warn-script-location
    if errorlevel 1 (echo [!] 7/9 失败 & set FAILED=%FAILED% 7)
)


:: ============================================================
:: [8/9] comtypes
:: ============================================================
echo.
echo ========== [8/9] comtypes ==========
if exist "library\comtypes" (
    echo   已装，跳过
) else (
    pip install comtypes==1.4.17 --target "%ROOT%library" --no-warn-script-location
    if errorlevel 1 (echo [!] 8/9 失败 & set FAILED=%FAILED% 8)
)


:: ============================================================
:: [9/9] psutil + watchdog
:: ============================================================
echo.
echo ========== [9/9] psutil + watchdog ==========
if exist "library\psutil" (
    echo   已装，跳过
) else (
    pip install psutil==7.2.2 watchdog==6.0.0 --target "%ROOT%library" --no-warn-script-location
    if errorlevel 1 (echo [!] 9/9 失败 & set FAILED=%FAILED% 9)
)


:: ============================================================
:: 汇总
:: ============================================================
echo.
echo ============================================================
if "%FAILED%"=="" (
    echo  全部成功
) else (
    echo  以下步骤失败: %FAILED%
    echo.
    echo  如果第 4 步失败：
    echo    1. 重跑一次 bat（GitHub 抽风经常几分钟就好）
    echo    2. 或手动下载 QtWebView.zip 放到项目根目录再跑
    echo       下载地址: https://github.com/xiaosuawa/QtWebView
    echo       点 Code - Download ZIP
    echo    3. 或从同事那里拷 library\qtwebview2 过来
)
echo ============================================================
echo.

echo 当前 library 目录结构：
dir /b "%ROOT%library"
echo.
echo qtwebview2 目录内容：
dir /b "%ROOT%library\qtwebview2"
echo.

popd
pause