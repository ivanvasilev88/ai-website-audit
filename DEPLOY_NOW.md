# 🚀 Deploy to Render - Quick Guide

## Current Status
✅ Code is ready for deployment
✅ All features implemented:
- Review-Based Recommendations (visible before payment)
- 9 new restaurant/bar audit checks
- Total: 34 audit checks

---

## Quick Deploy Steps

### Option 1: Using the Script (Easiest)

```bash
# Make script executable
chmod +x deploy_to_render.sh

# Run deployment script
./deploy_to_render.sh
```

This will:
1. Stage all changes
2. Commit with descriptive message
3. Push to GitHub
4. Render will auto-deploy

---

### Option 2: Manual Steps

#### Step 1: Commit and Push

```bash
# Stage all changes
git add -A

# Commit
git commit -m "Add review-based recommendations and 9 new restaurant/bar audit checks

- Added Review-Based Recommendations section visible before payment
- Added 9 new restaurant/bar-specific audit checks
- Enhanced review analysis framework
- Total audit checks: 34 (up from 25)"

# Push to GitHub
git push origin main
```

#### Step 2: Render Auto-Deploys

If you already have Render connected to your GitHub repo:
- ✅ Render will automatically detect the push
- ✅ It will start deploying in 1-2 minutes
- ✅ Check your Render dashboard for status

#### Step 3: Verify Deployment

1. Go to: https://dashboard.render.com
2. Click on your service
3. Wait for "Live" status
4. Copy your public URL
5. Test it!

---

## If You Don't Have Render Set Up Yet

### First Time Setup:

1. **Go to Render**: https://render.com
2. **Sign up** (free tier available)
3. **Connect GitHub**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account
   - Select repository: `ai-website-audit`
4. **Configure**:
   - **Name**: `ai-website-audit` (or any name)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Environment**: `Python 3`
   - **Build Command**: (leave empty)
   - **Start Command**: `python3 server_standalone.py`
5. **Deploy**:
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Get your URL: `https://your-app.onrender.com`

---

## Environment Variables (Optional)

If you want email functionality, add these in Render dashboard:

1. Go to your service → "Environment"
2. Add variables:
   - `SMTP_SERVER` (e.g., `smtp.gmail.com`)
   - `SMTP_PORT` (e.g., `587`)
   - `SMTP_USER` (your email)
   - `SMTP_PASSWORD` (app password)
   - `FROM_EMAIL` (your email)
   - `PORT` (usually auto-set by Render)

**Note**: Email will work without these - it will save to `emails_to_send/` folder instead.

---

## Testing Your Deployment

Once deployed, test:

1. ✅ Open your Render URL
2. ✅ Scan a restaurant website
3. ✅ Check Review-Based Recommendations appear (before payment)
4. ✅ Complete payment to see full recommendations
5. ✅ Verify all 34 audit checks are working

---

## Troubleshooting

### Deployment Fails?

1. **Check Render logs**:
   - Go to your service → "Logs"
   - Look for error messages

2. **Common issues**:
   - **Port error**: Make sure `server_standalone.py` reads `PORT` from environment
   - **Build error**: Check that all files are in the repo
   - **Start error**: Verify Start Command is `python3 server_standalone.py`

### Service Shows "Unavailable"?

1. Check logs in Render dashboard
2. Verify the service is running
3. Try restarting the service in Render dashboard

### Changes Not Showing?

1. Wait 2-3 minutes for deployment
2. Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)
3. Clear browser cache

---

## Files Changed in This Update

- ✅ `server_standalone.py` - Added 9 new audit checks + review recommendations
- ✅ `app.js` - Added recommendations display logic
- ✅ `index.html` - Added recommendations section
- ✅ `styles.css` - Added recommendations styling

---

## Next Steps After Deployment

1. ✅ Share your Render URL with test users
2. ✅ Monitor usage in Render dashboard
3. ✅ Check user database (`user_database.json`) for signups
4. ✅ Review audit results in admin panel: `/admin`

---

## Support

If you encounter issues:
1. Check Render logs
2. Verify all files are committed
3. Ensure Python 3.11+ is selected in Render
4. Check that `Procfile` exists with: `web: python3 server_standalone.py`

---

**Ready to deploy? Run:**
```bash
./deploy_to_render.sh
```

Or manually:
```bash
git add -A
git commit -m "Add review recommendations and 9 new audit checks"
git push origin main
```
