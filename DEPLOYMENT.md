# Deployment Guide

## Quick Deployment Options

### Option 1: Railway (Easiest - Recommended)
**Free tier available, automatic HTTPS, zero config**

1. **Sign up**: Go to [railway.app](https://railway.app)
2. **Create new project**: Click "New Project"
3. **Deploy from GitHub** (recommended):
   - Connect your GitHub account
   - Select this repository
   - Railway auto-detects Python and deploys
4. **Or deploy from local**:
   - Install Railway CLI: `npm i -g @railway/cli`
   - Run: `railway login` then `railway init`
   - Run: `railway up`
5. **Get your URL**: Railway provides a public URL automatically

**Environment Variables** (optional):
- `PORT` - Railway sets this automatically
- No other config needed!

---

### Option 2: Render (Free tier)
**Free tier with automatic HTTPS**

1. **Sign up**: Go to [render.com](https://render.com)
2. **Create new Web Service**
3. **Connect repository** or upload files
4. **Settings**:
   - Build Command: (leave empty - no build needed)
   - Start Command: `python3 server_standalone.py`
   - Environment: Python 3
5. **Deploy**: Click "Create Web Service"
6. **Get URL**: Render provides `your-app.onrender.com`

---

### Option 3: Heroku (Classic option)
**Free tier discontinued, but still popular**

1. **Install Heroku CLI**: `brew install heroku/brew/heroku`
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-app-name`
4. **Deploy**: `git push heroku main`
5. **Open**: `heroku open`

**Note**: Requires a `Procfile` (see below)

---

### Option 4: DigitalOcean App Platform
**Simple deployment, pay-as-you-go**

1. **Sign up**: [digitalocean.com](https://digitalocean.com)
2. **Create App**: Connect GitHub or upload files
3. **Configure**:
   - Runtime: Python
   - Build Command: (none)
   - Run Command: `python3 server_standalone.py`
4. **Deploy**: Click "Create Resources"

---

### Option 5: PythonAnywhere (Free tier)
**Great for Python apps**

1. **Sign up**: [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Upload files**: Use Files tab to upload your project
3. **Create Web App**:
   - Go to Web tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Python 3.10
4. **Configure WSGI**:
   - Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Add: `from server_standalone import app`
5. **Reload**: Click green reload button

---

### Option 6: VPS (Most Control)
**DigitalOcean Droplet, AWS EC2, Linode, etc.**

1. **Create VPS**: Ubuntu 22.04 recommended
2. **SSH into server**: `ssh user@your-server-ip`
3. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```
4. **Upload files**: Use `scp` or `git clone`
5. **Run with systemd** (see `systemd-service.txt` below)
6. **Configure Nginx** as reverse proxy
7. **Set up SSL** with Let's Encrypt

---

## Quick Start Files

### Procfile (for Heroku/Railway)
```
web: python3 server_standalone.py
```

### runtime.txt (for Heroku)
```
python-3.11.0
```

### .gitignore
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
*.log
report_*.txt
```

---

## Production Checklist

Before deploying, make sure to:

- [ ] Update CORS settings if needed
- [ ] Set up environment variables for sensitive data
- [ ] Configure proper error logging
- [ ] Set up monitoring/analytics
- [ ] Configure email sending (SMTP) for reports
- [ ] Set up payment processing (Stripe/PayPal)
- [ ] Use a database instead of in-memory storage
- [ ] Set up SSL/HTTPS (most platforms do this automatically)
- [ ] Configure domain name (optional)

---

## Environment Variables

Create a `.env` file or set in your platform:

```bash
PORT=3000  # Most platforms set this automatically
SMTP_HOST=smtp.gmail.com  # For email sending
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-password
STRIPE_SECRET_KEY=sk_...  # For payments
```

---

## Testing Your Deployment

1. **Check server is running**: Visit your URL
2. **Test scan**: Try scanning a website
3. **Test payment**: Complete a test payment
4. **Check admin**: Visit `/admin` endpoint
5. **Test PDF**: Download a PDF report

---

## Recommended: Railway (Fastest Setup)

Railway is the easiest option:
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Zero configuration
- ✅ GitHub integration
- ✅ Auto-deploys on push

**Steps**:
1. Push code to GitHub
2. Sign up at railway.app
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Done! Get your public URL

---

## Need Help?

- Check platform-specific documentation
- Review error logs in platform dashboard
- Test locally first: `python3 server_standalone.py`
- Check firewall/security group settings on VPS

