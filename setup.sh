#!/bin/bash

echo "============================================"
echo "ML Text Classification - Complete Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js is not installed or not in PATH."
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo "[1/4] Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ".env file created! Edit it if you want to configure Supabase logging."
else
    echo ".env file already exists."
fi
echo ""

echo "[2/4] Installing frontend dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install frontend dependencies."
    exit 1
fi
echo "Frontend dependencies installed successfully!"
echo ""

echo "[3/4] Installing backend dependencies..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install backend dependencies."
    cd ..
    exit 1
fi
cd ..
echo "Backend dependencies installed successfully!"
echo ""

echo "[4/4] Setup complete!"
echo ""
echo "============================================"
echo "Next Steps:"
echo "============================================"
echo "1. Start the backend server:"
echo "   - Run: ./start-backend.sh"
echo "   - Or manually: cd backend && python3 app.py"
echo ""
echo "2. Start the frontend (in a new terminal):"
echo "   - Run: npm run dev"
echo ""
echo "3. Open your browser to the URL shown by Vite"
echo "============================================"
echo ""
