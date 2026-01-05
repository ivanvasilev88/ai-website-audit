# Deploy to Railway (5 Minutes)

## Step-by-Step Guide

### 1. Push to GitHub (if not already)
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/ai-website-audit.git
git push -u origin main
```

### 2. Deploy on Railway

1. **Go to**: [railway.app](https://railway.app)
2. **Sign up** with GitHub
3. **Click**: "New Project"
4. **Select**: "Deploy from GitHub repo"
5. **Choose** your repository
6. **Railway auto-detects** Python and deploys!

### 3. Get Your Public URL

- Railway provides a URL like: `your-app.up.railway.app`
- Share this URL with anyone!
- HTTPS is automatic ✅

### 4. (Optional) Custom Domain

1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Railway handles SSL automatically

## That's It!

Your site is now live and accessible to anyone with the URL.

## Environment Variables (Optional)

If you need to configure email or payments later:

1. Go to your project on Railway
2. Click "Variables"
3. Add:
   - `SMTP_HOST=smtp.gmail.com`
   - `SMTP_USER=your-email@gmail.com`
   - `SMTP_PASS=your-password`
   - `STRIPE_SECRET_KEY=sk_...`

## Update Your Site

Just push to GitHub:
```bash
git add .
git commit -m "Update"
git push
```

Railway automatically redeploys! 🚀

