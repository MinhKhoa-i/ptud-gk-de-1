#!/bin/bash

echo "Starting installation of the project..."

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH. Please install Python 3."
    exit 1
fi

# Kiểm tra pip
if ! python3 -m pip --version &> /dev/null; then
    echo "Error: pip is not installed. Please install pip for Python 3."
    exit 1
fi

# Tạo và kích hoạt virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment. Ensure virtualenv is supported."
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

# Cài đặt dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies. Check requirements.txt."
    exit 1
fi

# Chạy ứng dụng
echo "Starting Flask application..."
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
if [ $? -ne 0 ]; then
    echo "Error: Failed to start application. Check app.py for errors."
    exit 1
fi

echo "Installation and setup complete! Access the app at http://127.0.0.1:5000"