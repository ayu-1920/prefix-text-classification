@echo off
echo ==========================================
echo ML Classification Experiment Backend
echo ==========================================
echo.

cd backend

if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo ==========================================
echo Starting Flask backend on port 5000...
echo ==========================================
echo.
echo Backend logs will be saved to backend.log
echo Press Ctrl+C to stop the server
echo.

python app.py
