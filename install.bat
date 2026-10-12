@echo off
title Custom Discord RPC - Installer
echo ======================================================
echo    Installing Custom Discord RPC Dependencies
echo ======================================================
echo.

echo [*] Installing Node.js dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [!] Warning: npm install failed. Please ensure Node.js is installed.
) else (
    echo [V] Node.js dependencies installed!
)

echo.
echo [*] Installing Python GUI dependencies...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [!] Warning: pip install failed. Python GUI tray might not work.
) else (
    echo [V] Python dependencies installed!
)

echo.
echo ======================================================
echo    Installation Complete! Run start.bat to launch.
echo ======================================================
pause
