#!/bin/bash

# Quick Deployment Script for Public Testing
# This script helps you deploy to Railway

echo "🚀 AI Website Audit - Public Deployment"
echo "========================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Check if files are committed
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ All files are committed"
else
    echo "📝 Staging files..."
    git add .
    echo "💾 Committing changes..."
    git commit -m "Ready for public deployment"
    echo "✅ Files committed"
    echo ""
fi

# Check if remote exists
if git remote get-url origin > /dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    echo "✅ GitHub remote found: $REMOTE_URL"
    echo ""
    echo "Next steps:"
    echo "1. Push to GitHub: git push -u origin main"
    echo "2. Go to https://railway.app"
    echo "3. Sign up with GitHub"
    echo "4. Click 'New Project' → 'Deploy from GitHub repo'"
    echo "5. Select your repository"
    echo "6. Get your public URL!"
else
    echo "⚠️  No GitHub remote found"
    echo ""
    echo "To set up GitHub:"
    echo "1. Go to https://github.com and create a new repository"
    echo "2. Then run:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/ai-website-audit.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "Then deploy on Railway:"
    echo "1. Go to https://railway.app"
    echo "2. Sign up with GitHub"
    echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
    echo "4. Select your repository"
    echo "5. Get your public URL!"
fi

echo ""
echo "📚 For detailed instructions, see: PUBLIC_DEPLOYMENT.md"
echo ""


