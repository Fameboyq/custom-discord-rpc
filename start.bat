@echo off
title Custom Discord RPC
echo ======================================================
echo    Launching Custom Discord RPC
echo ======================================================
echo.

if not exist node_modules\discord-rpc (
    echo [*] First run detected. Installing dependencies...
    call install.bat
)

echo [*] Starting Discord RPC background engine...
start "" /B node index.js

echo [*] Starting System Tray Control Panel...
start "" /B pythonw tray_app.py

echo [V] Custom Discord RPC is now running in background!
echo [V] Check your Discord profile and system tray icon.
timeout /t 3 >nul
exit
