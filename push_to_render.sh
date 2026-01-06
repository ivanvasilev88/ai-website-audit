#!/bin/bash

# Push Latest Changes to Render
# This will commit and push all changes so Render can deploy the latest version

echo "🚀 Pushing latest changes to Render..."
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Show what will be committed
echo "📋 Files to commit:"
git status --short
echo ""

# Stage all changes
echo "📝 Staging all changes..."
git add -A

# Commit with descriptive message
echo "💾 Committing changes..."
git commit -m "Add review-based recommendations and 9 new restaurant/bar audit checks

Features added:
- Review-Based Recommendations section (visible before payment preview)
- 9 new restaurant/bar-specific audit checks:
  * Cuisine Type Identification
  * Dietary Restrictions Information
  * Special Features & Amenities
  * Visual Content & Photo Galleries
  * Events & Calendar Information
  * Additional Services Information
  * Delivery & Takeout Information
  * Parking & Accessibility Information
  * Enhanced Review Visibility & Integration
- Enhanced review analysis framework
- Improved UI for recommendations display
- Total audit checks: 34 (up from 25)

Files changed:
- server_standalone.py: Added 9 new audit checks + review recommendations
- app.js: Recommendations display logic
- index.html: Recommendations section
- styles.css: Recommendations styling"

if [ $? -eq 0 ]; then
    echo "✅ Changes committed"
else
    echo "⚠️  No new changes to commit (or commit failed)"
fi

# Push to GitHub
echo ""
echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "🔄 Render will automatically deploy in 2-3 minutes"
    echo "📋 Check your Render dashboard: https://dashboard.render.com"
    echo ""
    echo "⏳ Wait 2-3 minutes, then refresh your Render URL"
    echo "✨ Your changes should be live!"
    echo ""
else
    echo ""
    echo "❌ Failed to push to GitHub"
    echo "💡 This might be due to:"
    echo "   - Network issues"
    echo "   - Authentication problems"
    echo "   - GitHub access issues"
    echo ""
    echo "🔧 Try running manually:"
    echo "   git push origin main"
    exit 1
fi

