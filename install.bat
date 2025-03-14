@echo off
echo Starting installation of the project...

:: Kiểm tra Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH. Please install Python and add it to PATH.
    pause
    exit /b 1
)

:: Kiểm tra pip
python -m pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: pip is not installed. Please install pip.
    pause
    exit /b 1
)

:: Cập nhật pip (tùy chọn)
echo Updating pip...
python.exe -m pip install --upgrade pip

:: Tạo và kích hoạt virtual environment
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create virtual environment. Ensure virtualenv is installed.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

echo Activating virtual environment...
call venv\Scripts\activate

:: Cài đặt dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install dependencies. Check requirements.txt.
    pause
    exit /b 1
)

:: Kiểm tra file database
echo Checking database...
if not exist instance\database.db (
    echo Warning: Database file instance\database.db not found. It will be created when the app starts.
)

:: Chạy ứng dụng
echo Starting Flask application...
set FLASK_APP=tiny_app.py
set FLASK_ENV=development
flask run
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to start application. Check tiny_app.py for errors.
    pause
    exit /b 1
)

echo Installation and setup complete! Access the app at http://127.0.0.1:5000
pause