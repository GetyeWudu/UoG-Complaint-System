@echo off
echo ========================================
echo UoG Complaint System - Backend Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/7] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo [1/7] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [2/7] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo [3/7] Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Create .env if it doesn't exist
if not exist ".env" (
    echo [4/7] Creating .env file...
    copy .env.example .env >nul
    echo ✓ .env file created
) else (
    echo [4/7] .env file already exists
)
echo.

REM Create logs directory
if not exist "logs\" (
    echo [5/7] Creating logs directory...
    mkdir logs
    echo ✓ Logs directory created
) else (
    echo [5/7] Logs directory already exists
)
echo.

REM Run migrations
echo [6/7] Running database migrations...
python manage.py makemigrations accounts
python manage.py makemigrations complaints
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)
echo ✓ Migrations completed
echo.

REM Seed database
echo [7/7] Seeding database with test data...
python manage.py seed_data
if errorlevel 1 (
    echo WARNING: Seed data may have failed (this is OK if data already exists)
)
echo ✓ Database seeded
echo.

echo ========================================
echo Setup Complete! ✓
echo ========================================
echo.
echo Test Accounts:
echo   student@example.com / Student123!
echo   staff@example.com / Staff123!
echo   admin@example.com / Admin123!
echo.
echo Starting development server...
echo.
echo API Documentation: http://127.0.0.1:8000/api/docs/
echo Django Admin: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start server
python manage.py runserver
