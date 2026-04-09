@echo off
setlocal

echo [1/3] Checking Python...
where python >nul 2>nul
if not %errorlevel%==0 (
    echo ERROR: Python was not found in PATH.
    pause
    exit /b 1
)

echo [2/3] Installing build dependency (PyInstaller)...
python -m pip install --upgrade pip
python -m pip install pyinstaller

echo [3/3] Building DailyScheduler.exe...
python -m PyInstaller --noconfirm --clean --onefile --noconsole --name DailyScheduler main.py

if %errorlevel%==0 (
    echo.
    echo Build success: dist\DailyScheduler.exe
) else (
    echo.
    echo Build failed.
)

pause
