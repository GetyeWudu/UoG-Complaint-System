@echo off
echo Installing UoG Complaint System Dependencies...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✓ Dependencies installed successfully!
echo.
echo Next steps:
echo 1. Copy .env.example to .env and configure settings
echo 2. Run: python manage.py makemigrations
echo 3. Run: python manage.py migrate
echo 4. Run: python manage.py seed_data
echo 5. Run: python manage.py runserver
echo.
pause
