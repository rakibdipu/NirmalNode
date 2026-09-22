@echo off
chcp 65001 >nul
title NirmalNode AI - Launcher

echo.
echo  ============================================================
echo   NirmalNode AI - Green IoT Air Quality Dashboard
echo   Adaptive AI + ESP32 Sensor System
echo  ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python not found! Please install Python 3.x from python.org
    echo.
    pause
    exit /b 1
)

echo  [OK] Python found.

:: Install required packages silently
echo  [..] Checking Python packages...
python -m pip install flask flask-cors pyserial scikit-learn numpy --quiet --disable-pip-version-check 2>nul
echo  [OK] All packages ready.

echo.
echo  [..] Starting NirmalNode backend server...
echo  [OK] Dashboard will open at: http://localhost:5000
echo.
echo  ==========================================================
echo   Keep this window open while using the dashboard!
echo   Press Ctrl+C to stop the server.
echo  ==========================================================
echo.

:: Open browser after 3 seconds
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

:: Start Flask server
python server.py

echo.
echo  [INFO] Server stopped.
pause
