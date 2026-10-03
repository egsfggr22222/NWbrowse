@echo off
chcp 936 >nul
pushd "%~dp0"

set "ZIP=%~dp0MiSans.zip"
set "EXTRACT=%~dp0assets\_temp_misans"
set "TARGET=%~dp0assets\fonts"

echo ========== 准备目录 / Preparing folders ==========
if not exist "assets" mkdir "assets"
if not exist "%TARGET%" mkdir "%TARGET%"

echo ========== 清空目标字体目录 / Clearing target folder ==========
del /f /q "%TARGET%\*.*" >nul 2>&1
rd /s /q "%TARGET%" >nul 2>&1
mkdir "%TARGET%"

echo ========== 检查字体压缩包 / Checking font package ==========
if not exist "%ZIP%" (
    echo 未找到 MiSans.zip，正在下载 / Downloading MiSans.zip ...
    powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://hyperos.mi.com/font-download/MiSans.zip' -OutFile '%ZIP%'"
)

if not exist "%ZIP%" (
    echo.
    echo 下载失败，请手动下载 MiSans.zip 放到项目根目录
    echo Download failed. Please download MiSans.zip manually.
    echo 下载地址 / URL: https://hyperos.mi.com/font-download/MiSans.zip
    pause
    exit /b 1
)

echo ========== 解压 / Extracting ==========
if exist "%EXTRACT%" rd /s /q "%EXTRACT%"
powershell -NoProfile -Command "Expand-Archive -Path '%ZIP%' -DestinationPath '%EXTRACT%' -Force"

echo ========== 复制字体文件 / Copying fonts ==========
for /r "%EXTRACT%" %%f in (*.woff2) do copy "%%f" "%TARGET%" >nul

dir /b "%TARGET%\*.woff2" >nul 2>&1
if errorlevel 1 (
    echo 未找到 woff2，改用 ttf / No woff2, using ttf ...
    for /r "%EXTRACT%" %%f in (*.ttf) do copy "%%f" "%TARGET%" >nul
)

echo ========== 清理临时文件 / Cleaning up ==========
rd /s /q "%EXTRACT%" >nul 2>&1
del "%ZIP%" >nul 2>&1

echo.
echo 完成！字体已放入 / Done! Fonts placed in:
echo   %TARGET%
echo.
echo 文件列表 / File list:
dir /b "%TARGET%"
popd
pause