#!/bin/bash

echo "=========================================="
echo "ML Classification Experiment Backend"
echo "=========================================="
echo ""

cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "Starting Flask backend on port 5000..."
echo "=========================================="
echo ""
echo "Backend logs will be saved to backend.log"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
