@echo off
echo ========================================
echo Office Intranet - Backend Setup
echo ========================================
echo.

cd backend

REM Check if .env exists
if exist .env (
    echo [INFO] .env file already exists
) else (
    echo [SETUP] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [IMPORTANT] Please edit backend\.env and update:
    echo   - FLASK_SECRET_KEY
    echo   - JWT_SECRET  
    echo   - ADMIN_PASSWORD_HASH (or keep default password: admin123)
    echo.
    pause
)

REM Check if venv exists
if exist venv (
    echo [INFO] Virtual environment already exists
) else (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
)

echo.
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate

echo.
echo [SETUP] Installing/updating dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server:
echo   1. Run: run_server.bat
echo   2. Access at: http://localhost:5000
echo.
echo Default admin password: admin123
echo (Change this in .env file for production)
echo.
pause
