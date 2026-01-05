# Deploy for Public Testing - Step by Step

## 🚀 Quickest Method: Railway (5 minutes)

### Step 1: Prepare Your Code for Git

```bash
# Navigate to your project
cd /Users/ivanvasilev/ai-website-audit

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for public testing"
```

### Step 2: Push to GitHub

**Option A: Create New Repository on GitHub**
1. Go to [github.com](https://github.com)
2. Click "+" → "New repository"
3. Name it: `ai-website-audit`
4. Don't initialize with README
5. Click "Create repository"

**Option B: Use Existing Repository**
- If you already have a repo, skip to Step 3

**Then push your code:**
```bash
# Add your GitHub repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-website-audit.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway

1. **Go to Railway**: [railway.app](https://railway.app)

2. **Sign Up**:
   - Click "Start a New Project"
   - Choose "Login with GitHub"
   - Authorize Railway to access your GitHub

3. **Deploy**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `ai-website-audit` repository
   - Railway will automatically detect Python and start deploying

4. **Wait for Deployment** (1-2 minutes):
   - Watch the build logs
   - Wait for "Deploy successful" message

5. **Get Your Public URL**:
   - Click on your project
   - Click "Settings" tab
   - Scroll to "Domains"
   - You'll see: `your-app-name.up.railway.app`
   - **This is your public URL!** 🎉

### Step 4: Share with Test Users

**Your public URL will look like:**
```
https://your-app-name.up.railway.app
```

**Share this URL with your test users!**

---

## 📋 Alternative: Render (Also Free)

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Render

1. **Go to Render**: [render.com](https://render.com)
2. **Sign up** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect Repository**: Select your `ai-website-audit` repo
5. **Configure**:
   - **Name**: `ai-website-audit` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: (leave empty)
   - **Start Command**: `python3 server_standalone.py`
6. **Click**: "Create Web Service"
7. **Wait** for deployment (2-3 minutes)
8. **Get URL**: `https://your-app-name.onrender.com`

---

## 🔧 Manual Setup (If GitHub isn't an option)

### Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Get your URL
railway domain
```

---

## ✅ Verification Checklist

After deployment, test:

- [ ] Visit your public URL
- [ ] Test scanning a website
- [ ] Verify score displays correctly
- [ ] Check free insights show (green only)
- [ ] Verify locked insights are blurred
- [ ] Test payment flow
- [ ] Test PDF download
- [ ] Check admin page: `/admin`

---

## 🔗 Custom Domain (Optional)

### On Railway:
1. Go to project → Settings → Domains
2. Click "Generate Domain" or "Add Custom Domain"
3. Follow instructions to add your domain

### On Render:
1. Go to service → Settings → Custom Domain
2. Add your domain
3. Update DNS as instructed

---

## 📊 Monitoring

**Railway Dashboard:**
- View logs in real-time
- See deployment history
- Monitor resource usage

**Render Dashboard:**
- View logs
- See metrics
- Check deployment status

---

## 🔄 Updating Your Site

**To update after making changes:**

```bash
# Make your changes locally
# Then:

git add .
git commit -m "Your update message"
git push

# Railway/Render automatically redeploys!
```

---

## 🆘 Troubleshooting

**Site not loading?**
- Check deployment logs in Railway/Render dashboard
- Verify build completed successfully
- Check if port is set correctly (Railway sets PORT automatically)

**Getting errors?**
- Check server logs in platform dashboard
- Verify all files were pushed to GitHub
- Make sure `server_standalone.py` is in root directory

**Need help?**
- Railway docs: https://docs.railway.app
- Render docs: https://render.com/docs

---

## 🎯 Quick Start Commands

**If you already have GitHub repo:**

```bash
cd /Users/ivanvasilev/ai-website-audit
git add .
git commit -m "Ready for deployment"
git push
```

Then:
1. Go to railway.app
2. New Project → Deploy from GitHub
3. Select your repo
4. Done! Get your URL

---

## 📝 What Test Users Need

**Just share:**
- Your public URL (e.g., `https://your-app.up.railway.app`)
- Brief instructions: "Enter a website URL and click Scan"

**That's it!** No installation needed for them.

