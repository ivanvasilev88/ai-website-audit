#!/bin/bash

# Quick Ngrok Setup - Get Public URL in 2 Minutes

echo "🚀 Quick Public URL Setup with Ngrok"
echo "====================================="
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "📦 Ngrok not found. Installing..."
    echo ""
    echo "Option 1: Download from https://ngrok.com/download"
    echo "Option 2: Install via Homebrew: brew install ngrok"
    echo ""
    read -p "Press Enter after installing ngrok, or type 'skip' to use alternative: " response
    
    if [ "$response" != "skip" ] && ! command -v ngrok &> /dev/null; then
        echo "❌ Ngrok still not found. Please install it first."
        exit 1
    fi
fi

echo "✅ Ngrok found!"
echo ""
echo "Starting server and creating public URL..."
echo ""

# Start server in background
echo "1. Starting local server..."
python3 server_standalone.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ Server failed to start. Check for errors above."
    exit 1
fi

echo "✅ Server started on port 3000"
echo ""
echo "2. Creating public URL with ngrok..."
echo ""

# Start ngrok
ngrok http 3000 &
NGROK_PID=$!

sleep 3

echo ""
echo "✅ Public URL created!"
echo ""
echo "📝 Your public URL will be shown above (look for 'Forwarding' line)"
echo "📝 It will look like: https://xxxx-xx-xx-xx-xx.ngrok-free.app"
echo ""
echo "🛑 To stop: Press Ctrl+C, then run: kill $SERVER_PID $NGROK_PID"
echo ""
echo "💡 Keep this terminal open to keep the URL active"
echo ""

# Wait for user interrupt
wait

