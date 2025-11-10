@echo off
echo Setting up Okra Classifier (No TensorFlow)...
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install minimal dependencies
echo Installing dependencies...
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install Werkzeug==2.3.7
pip install Pillow==10.0.0

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To run the application:
echo python app.py
echo.
pause