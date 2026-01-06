# 🚀 Quick Deployment Guide

## Current Version Features
✅ **34 Audit Checks** (9 new restaurant/bar-specific checks)
✅ **Review-Based Recommendations** (visible before payment)
✅ **Enhanced AI Discovery Analysis** for restaurants and bars

---

## Deploy to Render (Recommended)

### Quick Deploy Script

```bash
# Run the deployment script
./deploy_to_render.sh
```

This will automatically:
1. Stage all changes
2. Commit with descriptive message
3. Push to GitHub
4. Render will auto-deploy

---

### Manual Deploy

```bash
# 1. Stage changes
git add -A

# 2. Commit
git commit -m "Add review recommendations and 9 new audit checks"

# 3. Push to GitHub
git push origin main
```

Render will automatically detect the push and deploy in 2-3 minutes.

---

## Render Configuration

### Required Settings:
- **Environment**: Python 3
- **Build Command**: (leave empty)
- **Start Command**: `python3 server_standalone.py`
- **Branch**: `main`

### Optional Environment Variables:
- `SMTP_SERVER` - For email functionality
- `SMTP_PORT` - Email port (default: 587)
- `SMTP_USER` - Email username
- `SMTP_PASSWORD` - Email password
- `FROM_EMAIL` - Sender email
- `PORT` - Auto-set by Render (don't need to set)

---

## Verify Deployment

1. Check Render dashboard: https://dashboard.render.com
2. Wait for "Live" status
3. Test your URL: `https://your-app.onrender.com`
4. Scan a restaurant website
5. Verify Review-Based Recommendations appear

---

## What's New in This Version

### New Audit Checks (9):
1. **Cuisine Type Identification** - Detects cuisine types
2. **Dietary Restrictions Information** - Vegan, gluten-free, etc.
3. **Special Features & Amenities** - Outdoor seating, live music, etc.
4. **Visual Content & Photo Galleries** - Image analysis
5. **Events & Calendar Information** - Event detection
6. **Additional Services Information** - Gift cards, catering, etc.
7. **Delivery & Takeout Information** - Service options
8. **Parking & Accessibility Information** - Accessibility details
9. **Review Visibility & Integration** (enhanced)

### New Features:
- **Review-Based Recommendations** - Shows before payment (preview mode)
- **Enhanced Review Analysis** - Analyzes review platforms and patterns
- **Improved UI** - Better recommendations display

---

## Files Changed

- `server_standalone.py` - Added 9 audit checks + review recommendations
- `app.js` - Recommendations display logic
- `index.html` - Recommendations section
- `styles.css` - Recommendations styling

---

## Support

If deployment fails:
1. Check Render logs in dashboard
2. Verify `Procfile` exists: `web: python3 server_standalone.py`
3. Ensure Python 3.11+ is selected
4. Check that all files are committed

---

**Ready? Run: `./deploy_to_render.sh`**

