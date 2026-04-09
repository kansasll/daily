@echo off
setlocal
echo Starting Daily Scheduler...

set "ROOT=%~dp0"
set "EXE1=%ROOT%DailyScheduler.exe"
set "EXE2=%ROOT%dist\DailyScheduler.exe"

if exist "%EXE1%" (
    start "" "%EXE1%"
    goto :eof
)

if exist "%EXE2%" (
    start "" "%EXE2%"
    goto :eof
)

where python >nul 2>nul
if %errorlevel%==0 (
    python "%ROOT%main.py"
    goto :eof
)

echo.
echo ERROR: Python and packaged EXE were not found.
echo Please run build_exe.bat to package this project, or install Python 3.8+.
pause
