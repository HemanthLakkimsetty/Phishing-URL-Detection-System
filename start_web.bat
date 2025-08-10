@echo off
echo ========================================
echo    Safe URL Checker - Web Interface
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if Flask is installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
    if errorlevel 1 (
        echo ERROR: Failed to install Flask
        pause
        exit /b 1
    )
)

echo.
echo Starting Safe URL Checker Web Interface...
echo.
echo 🌐 Open your browser and go to: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Run the web interface
python web_interface.py

pause
