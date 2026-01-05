#!/bin/bash

# AI Website Audit - Python Startup Script

echo "🐍 Starting AI Website Audit Tool (Python version)..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "   Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies."
        exit 1
    fi
    echo "✅ Dependencies installed!"
    echo ""
fi

# Start the server
echo "🌐 Starting server on http://localhost:3000"
echo "📝 Open your browser and navigate to: http://localhost:3000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python3 server.py


