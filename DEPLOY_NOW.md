# Deploy Your Changes - Quick Guide

## Step 1: Push to GitHub

### Check what changed:
```bash
git status
```

### Add all changes:
```bash
git add .
```

### Commit changes:
```bash
git commit -m "Add privacy policy, GDPR cookies, UI improvements, and email functionality"
```

### Push to GitHub:
```bash
git push origin main
```
(Or `git push origin master` if your branch is called master)

---

## Step 2: Deploy to Get Public URL

### Option 1: Render (Easiest - 5 minutes)

1. **Go to**: https://render.com
2. **Sign up/Login** (free)
3. **Click**: "New +" → "Web Service"
4. **Connect GitHub** (if not connected)
5. **Select repository**: `ai-website-audit`
6. **Configure**:
   - **Name**: `ai-website-audit`
   - **Environment**: `Python 3`
   - **Build Command**: (leave empty)
   - **Start Command**: `python3 server_standalone.py`
7. **Click**: "Create Web Service"
8. **Wait 2-3 minutes**
9. **Get URL**: `https://your-app.onrender.com`

**✅ Done! Your site is live!**

---

### Option 2: Railway (If you already have it set up)

1. **Go to**: https://railway.app
2. **Open your project**
3. **It will auto-deploy** from GitHub
4. **Get URL**: `https://your-app.railway.app`

---

### Option 3: Ngrok (Instant - 2 minutes)

**For quick testing:**

```bash
# Terminal 1: Start your server
cd /Users/ivanvasilev/ai-website-audit
python3 server_standalone.py

# Terminal 2: Create public URL
ngrok http 3000
```

**Get URL**: `https://xxxx-xx-xx-xx-xx.ngrok-free.app`

**Note**: URL changes each time you restart ngrok, but works instantly!

---

## Quick Commands Summary

```bash
# 1. Push to GitHub
git add .
git commit -m "Add privacy policy, GDPR cookies, UI improvements, and email functionality"
git push origin main

# 2. Deploy (choose one):
# - Render: Follow steps above
# - Railway: Auto-deploys from GitHub
# - Ngrok: ngrok http 3000
```

---

## What Changed?

- ✅ Privacy Policy page (GDPR compliant)
- ✅ GDPR Cookie Consent banner
- ✅ Footer with Privacy Policy link
- ✅ Real email functionality with PDF attachment
- ✅ User database for email storage
- ✅ Modern, futuristic UI/UX improvements
- ✅ Mobile-friendly PDF export
- ✅ URL input accepts any format
- ✅ Auto-scroll to payment modal

All ready to deploy! 🚀

