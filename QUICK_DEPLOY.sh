#!/bin/bash

# Quick Deployment Script
# This helps you deploy to various platforms

echo "🚀 AI Website Audit - Deployment Helper"
echo "========================================"
echo ""
echo "Choose your deployment platform:"
echo "1. Railway (Recommended - Easiest)"
echo "2. Render"
echo "3. Heroku"
echo "4. Local Network (for testing on same WiFi)"
echo "5. Exit"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "📦 Railway Deployment:"
        echo "1. Push your code to GitHub"
        echo "2. Go to https://railway.app"
        echo "3. Sign up with GitHub"
        echo "4. Click 'New Project' → 'Deploy from GitHub'"
        echo "5. Select your repository"
        echo "6. Done! Railway provides a public URL"
        echo ""
        echo "See RAILWAY_DEPLOY.md for detailed steps"
        ;;
    2)
        echo ""
        echo "📦 Render Deployment:"
        echo "1. Go to https://render.com"
        echo "2. Sign up and create new Web Service"
        echo "3. Connect GitHub or upload files"
        echo "4. Settings:"
        echo "   - Build Command: (empty)"
        echo "   - Start Command: python3 server_standalone.py"
        echo "5. Deploy!"
        ;;
    3)
        echo ""
        echo "📦 Heroku Deployment:"
        echo "1. Install Heroku CLI: brew install heroku/brew/heroku"
        echo "2. heroku login"
        echo "3. heroku create your-app-name"
        echo "4. git push heroku main"
        echo "5. heroku open"
        ;;
    4)
        echo ""
        echo "🌐 Local Network Access:"
        echo "The server is already configured to accept connections from any interface."
        echo ""
        echo "To access from other devices on same WiFi:"
        echo "1. Find your local IP:"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "Not found")
        else
            IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "Not found")
        fi
        echo "   Your IP: $IP"
        echo ""
        echo "2. Start server: python3 server_standalone.py"
        echo "3. Access from other devices: http://$IP:3000"
        echo ""
        echo "Note: Make sure firewall allows port 3000"
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac


