@echo off
setlocal

set "ROOT=%~dp0"
set "DIST_EXE=%ROOT%dist\DailyScheduler.exe"
set "ISS=%ROOT%installer\daily_scheduler.iss"
set "ISCC="

echo [1/4] Checking packaged EXE...
if not exist "%DIST_EXE%" (
    echo ERROR: "%DIST_EXE%" was not found.
    echo Please run build_exe.bat first.
    pause
    exit /b 1
)

echo [2/4] Locating Inno Setup compiler (ISCC.exe)...
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not defined ISCC (
    where ISCC.exe >nul 2>nul
    if %errorlevel%==0 set "ISCC=ISCC.exe"
)

if not defined ISCC (
    echo ERROR: Inno Setup 6 was not found.
    echo Install from: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

echo [3/4] Building installer...
pushd "%ROOT%installer"
"%ISCC%" "daily_scheduler.iss"
set "BUILD_CODE=%errorlevel%"
popd

if not %BUILD_CODE%==0 (
    echo.
    echo Build installer failed.
    pause
    exit /b %BUILD_CODE%
)

echo [4/4] Build installer success.
echo Output folder: installer\output
pause

