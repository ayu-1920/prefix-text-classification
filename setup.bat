@echo off
echo ============================================
echo ML Text Classification - Complete Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/4] Setting up environment variables...
if not exist .env (
    echo Creating .env file from .env.example...
    copy .env.example .env >nul
    echo .env file created! Edit it if you want to configure Supabase logging.
) else (
    echo .env file already exists.
)
echo.

echo [2/4] Installing frontend dependencies...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install frontend dependencies.
    pause
    exit /b 1
)
echo Frontend dependencies installed successfully!
echo.

echo [3/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies.
    cd ..
    pause
    exit /b 1
)
cd ..
echo Backend dependencies installed successfully!
echo.

echo [4/4] Setup complete!
echo.
echo ============================================
echo Next Steps:
echo ============================================
echo 1. Start the backend server:
echo    - Run: start-backend.bat
echo    - Or manually: cd backend ^&^& python app.py
echo.
echo 2. Start the frontend (in a new terminal):
echo    - Run: npm run dev
echo.
echo 3. Open your browser to the URL shown by Vite
echo ============================================
echo.
pause
