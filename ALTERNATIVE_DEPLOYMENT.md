# Alternative Deployment Options - Quick Public Links

## Option 1: Render (Easiest Alternative)

### Step 1: Sign Up
1. Go to: https://render.com
2. Sign up with email (or GitHub)

### Step 2: Deploy
1. Click **"New +"** → **"Web Service"**
2. **Connect GitHub** (if you have repo) OR **"Deploy manually"**
3. If manual:
   - Upload your project folder
   - Or use Render CLI
4. **Configure**:
   - **Name**: `ai-website-audit`
   - **Environment**: `Python 3`
   - **Build Command**: (leave empty)
   - **Start Command**: `python3 server_standalone.py`
5. **Click "Create Web Service"**
6. **Wait 2-3 minutes**
7. **Get URL**: `https://your-app.onrender.com`

**Free tier available!**

---

## Option 2: Fly.io (Great for Python)

### Step 1: Install Fly CLI
```bash
# On Mac:
curl -L https://fly.io/install.sh | sh

# Or via Homebrew:
brew install flyctl
```

### Step 2: Deploy
```bash
cd /Users/ivanvasilev/ai-website-audit

# Login
fly auth login

# Launch app
fly launch

# Follow prompts:
# - App name: ai-website-audit (or auto-generated)
# - Region: Choose closest
# - PostgreSQL: No
# - Redis: No

# Deploy
fly deploy
```

**Get URL**: `https://your-app.fly.dev`

---

## Option 3: PythonAnywhere (Free Tier)

### Step 1: Sign Up
1. Go to: https://www.pythonanywhere.com
2. Sign up for free account

### Step 2: Upload Files
1. Go to **"Files"** tab
2. **Upload** all your project files:
   - `server_standalone.py`
   - `index.html`
   - `app.js`
   - `styles.css`
   - All other files

### Step 3: Create Web App
1. Go to **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **Python 3.10**
5. Click **"Next"** → **"Next"**

### Step 4: Configure WSGI
1. Click on the WSGI file link
2. Replace content with:
```python
import sys
path = '/home/YOUR_USERNAME/ai-website-audit'
if path not in sys.path:
    sys.path.append(path)

from server_standalone import run_server
import os

# PythonAnywhere sets PORT automatically
port = int(os.environ.get('PORT', 8000))
run_server(port=port, host='0.0.0.0')
```

3. **Save**

### Step 5: Reload
1. Go back to **"Web"** tab
2. Click **green "Reload"** button
3. **Get URL**: `https://YOUR_USERNAME.pythonanywhere.com`

---

## Option 4: Replit (Super Easy)

### Step 1: Sign Up
1. Go to: https://replit.com
2. Sign up (free)

### Step 2: Create Repl
1. Click **"Create Repl"**
2. Choose **"Python"**
3. Name: `ai-website-audit`

### Step 3: Upload Files
1. **Upload** all your files to Replit
2. Or use **"Upload folder"**

### Step 4: Run
1. Click **"Run"** button
2. Replit provides public URL automatically
3. **Get URL**: `https://your-app.repl.co`

**Free tier available!**

---

## Option 5: Ngrok (Local Server + Public URL)

### Step 1: Install Ngrok
```bash
# Download from: https://ngrok.com/download
# Or via Homebrew:
brew install ngrok
```

### Step 2: Start Your Server Locally
```bash
cd /Users/ivanvasilev/ai-website-audit
python3 server_standalone.py
```

### Step 3: Create Public Tunnel
```bash
# In a new terminal:
ngrok http 3000
```

### Step 4: Get Public URL
Ngrok will show:
```
Forwarding: https://xxxx-xx-xx-xx-xx.ngrok-free.app -> http://localhost:3000
```

**Share this URL!** (Works as long as your local server is running)

**Free tier**: URLs change on restart, but works great for testing!

---

## Option 6: Cloudflare Tunnel (Free, Permanent)

### Step 1: Install Cloudflared
```bash
brew install cloudflare/cloudflare/cloudflared
```

### Step 2: Start Server
```bash
python3 server_standalone.py
```

### Step 3: Create Tunnel
```bash
cloudflared tunnel --url http://localhost:3000
```

**Get permanent URL!**

---

## Option 7: LocalTunnel (Simplest)

### Step 1: Install
```bash
npm install -g localtunnel
```

### Step 2: Start Server
```bash
python3 server_standalone.py
```

### Step 3: Create Tunnel
```bash
# In new terminal:
lt --port 3000
```

**Get URL**: `https://xxxx.loca.lt`

---

## Quick Comparison

| Service | Difficulty | Free? | Setup Time |
|---------|-----------|-------|------------|
| **Render** | Easy | ✅ Yes | 5 min |
| **Ngrok** | Very Easy | ✅ Yes | 2 min |
| **Replit** | Very Easy | ✅ Yes | 3 min |
| **Fly.io** | Medium | ✅ Yes | 10 min |
| **PythonAnywhere** | Medium | ✅ Yes | 15 min |
| **LocalTunnel** | Very Easy | ✅ Yes | 2 min |

---

## Recommended: Ngrok (Fastest for Testing)

**2 minutes to get a public URL:**

```bash
# Terminal 1: Start server
cd /Users/ivanvasilev/ai-website-audit
python3 server_standalone.py

# Terminal 2: Create public URL
ngrok http 3000
```

**Share the ngrok URL!** Works immediately.

---

## Recommended: Render (Best for Permanent)

**5 minutes, permanent URL:**

1. Go to render.com
2. New Web Service
3. Deploy from GitHub (or manual upload)
4. Start Command: `python3 server_standalone.py`
5. Done!

**Get permanent URL that doesn't change.**

