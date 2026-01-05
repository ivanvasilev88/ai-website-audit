#!/bin/bash

# Fix GitHub Remote URL

echo "🔧 Fixing GitHub Remote Configuration"
echo "======================================"
echo ""

cd /Users/ivanvasilev/ai-website-audit

# Remove the placeholder remote
echo "Removing old remote..."
git remote remove origin 2>/dev/null || echo "No remote to remove"

echo ""
echo "✅ Remote removed!"
echo ""
echo "Next steps:"
echo ""
echo "Option 1: Let GitHub Desktop create the repo (Easiest)"
echo "  1. In GitHub Desktop, click 'Publish repository'"
echo "  2. It will create a new repository for you"
echo ""
echo "Option 2: Create repo on GitHub first, then update remote"
echo "  1. Go to https://github.com/new"
echo "  2. Create repository named 'ai-website-audit'"
echo "  3. Then run:"
echo "     git remote add origin https://github.com/YOUR_USERNAME/ai-website-audit.git"
echo "     (Replace YOUR_USERNAME with your actual GitHub username)"
echo ""

