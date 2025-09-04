@echo off
REM Resume Generator Installation Script for Windows
REM This script installs the Resume Generator system on Windows

echo 🚀 Resume Generator Installation Script
echo ======================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.11 or newer.
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

python --version
echo [SUCCESS] Python is installed

REM Check if pip is available
echo [INFO] Checking pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] pip is not available. Installing pip...
    python -m ensurepip --upgrade
)

echo [SUCCESS] pip is available

REM Create virtual environment
echo [INFO] Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated

REM Install dependencies
echo [INFO] Installing Python dependencies...
if not exist requirements.txt (
    echo [ERROR] requirements.txt not found. Are you in the right directory?
    pause
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist media mkdir media
if not exist media\generated_resumes mkdir media\generated_resumes
if not exist logs mkdir logs
if not exist temp mkdir temp
if not exist content mkdir content
if not exist content\role_overrides mkdir content\role_overrides
echo [SUCCESS] Directories created

REM Set up database
echo [INFO] Setting up database...
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to run database migrations
    pause
    exit /b 1
)
echo [SUCCESS] Database migrations completed

echo [INFO] Setting up system data...
python manage.py setup_resume_system --create-superuser
if %errorlevel% neq 0 (
    echo [ERROR] Failed to set up system data
    pause
    exit /b 1
)
echo [SUCCESS] System data created

REM Test installation
echo [INFO] Testing installation...
python manage.py check
if %errorlevel% neq 0 (
    echo [ERROR] Django configuration is invalid
    pause
    exit /b 1
)
echo [SUCCESS] Django configuration is valid

REM Test database
python manage.py shell -c "from django.contrib.auth.models import User; print('Users:', User.objects.count())"
if %errorlevel% neq 0 (
    echo [ERROR] Database test failed
    pause
    exit /b 1
)
echo [SUCCESS] Database is working

echo.
echo 🎉 Installation Complete!
echo ========================
echo.
echo Your Resume Generator is ready to use!
echo.
echo Next steps:
echo 1. Start the server:
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. Open your browser:
echo    http://127.0.0.1:8000/
echo.
echo 3. Login with:
echo    Username: admin
echo    Password: admin123
echo.
echo 4. Start creating resumes!
echo.
echo For help, check the documentation in the docs\ folder
echo.
pause
