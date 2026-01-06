# Deploy to Render - Step by Step

## Why Render?
- ✅ Free tier available
- ✅ No GitHub required (can upload manually)
- ✅ Automatic HTTPS
- ✅ Easy setup
- ✅ Permanent URL

---

## Method 1: Deploy from GitHub (If you have GitHub repo)

### Step 1: Sign Up
1. Go to: https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (or email)

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. **Connect your GitHub account** (if not connected)
3. **Select your repository**: `ai-website-audit`
4. Click **"Connect"**

### Step 3: Configure
- **Name**: `ai-website-audit` (or any name)
- **Region**: Choose closest to you
- **Branch**: `main` (or `master`)
- **Root Directory**: (leave empty)
- **Environment**: `Python 3`
- **Build Command**: (leave empty - no build needed)
- **Start Command**: `python3 server_standalone.py`

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. **Get your URL**: `https://your-app.onrender.com`

**Done!** ✅

---

## Method 2: Manual Upload (No GitHub Needed)

### Step 1: Sign Up
1. Go to: https://render.com
2. Sign up with email

### Step 2: Use Render CLI

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy
cd /Users/ivanvasilev/ai-website-audit
render deploy
```

### Step 3: Or Use Web Interface
1. Click **"New +"** → **"Web Service"**
2. Choose **"Deploy manually"**
3. Upload your project folder
4. Configure same as Method 1
5. Deploy!

---

## After Deployment

### Your Public URL
Render provides: `https://your-app.onrender.com`

### Share with Test Users
Just share this URL - no installation needed!

### Update Your Site
1. Make changes locally
2. Push to GitHub (if using GitHub method)
3. Render auto-redeploys!

---

## Troubleshooting

**Service shows "Unavailable"?**
- Check logs in Render dashboard
- Verify Start Command is correct
- Make sure PORT environment variable is being read

**Build fails?**
- Check build logs
- Verify all files are uploaded
- Make sure `server_standalone.py` is in root

---

## Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| Free Tier | ✅ Yes | ✅ Yes |
| Manual Upload | ✅ Yes | ❌ No |
| GitHub Required | ❌ No | ✅ Yes |
| Setup Time | 5 min | 5 min |
| Auto Deploy | ✅ Yes | ✅ Yes |

**Render is easier if you don't want to use GitHub!**

