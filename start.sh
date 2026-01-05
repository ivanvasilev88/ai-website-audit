#!/bin/bash

# AI Website Audit - Startup Script

echo "🚀 Starting AI Website Audit Tool..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Please make sure Node.js and npm are installed."
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

npm start

