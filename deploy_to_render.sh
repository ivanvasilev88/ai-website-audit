#!/bin/bash

# Deploy to Render - Quick Script
# This script prepares and pushes your code to GitHub, which will auto-deploy on Render

echo "🚀 Preparing deployment to Render..."
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Staging changes..."
    git add -A
    
    echo "💾 Committing changes..."
    git commit -m "Add review-based recommendations and 9 new restaurant/bar audit checks

- Added Review-Based Recommendations section visible before payment (preview mode)
- Added 9 new restaurant/bar-specific audit checks:
  * Cuisine Type Identification
  * Dietary Restrictions Information
  * Special Features & Amenities
  * Visual Content & Photo Galleries
  * Events & Calendar Information
  * Additional Services Information
  * Delivery & Takeout Information
  * Parking & Accessibility Information
- Enhanced review analysis framework
- Improved UI for recommendations display
- Total audit checks: 34 (up from 25)"
    
    echo "✅ Changes committed"
else
    echo "✅ No changes to commit"
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🔄 Render will automatically deploy in 2-3 minutes"
    echo "📋 Check your Render dashboard: https://dashboard.render.com"
    echo ""
    echo "✨ Your public URL will be: https://your-app.onrender.com"
    echo ""
else
    echo ""
    echo "❌ Failed to push to GitHub"
    echo "💡 Try running manually: git push origin main"
    exit 1
fi

