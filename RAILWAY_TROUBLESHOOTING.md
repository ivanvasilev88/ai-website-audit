# Railway Deployment Troubleshooting

## Issue: Server Shows "Offline" or Won't Start

### Step 1: Check Railway Logs

1. **Go to your Railway project dashboard**
2. **Click on your service**
3. **Click "Deployments" tab**
4. **Click on the latest deployment**
5. **Click "View Logs"**

Look for errors like:
- `ModuleNotFoundError`
- `Port already in use`
- `Permission denied`
- Any Python errors

### Step 2: Verify Configuration

**Check these files exist in your repo:**

✅ `Procfile` - Should contain: `web: python3 server_standalone.py`
✅ `server_standalone.py` - Main server file
✅ `railway.json` - Railway configuration (optional but helpful)

### Step 3: Common Fixes

#### Fix 1: Update Procfile

Make sure `Procfile` contains exactly:
```
web: python3 server_standalone.py
```

No extra spaces, no blank lines.

#### Fix 2: Check Python Version

Railway should auto-detect Python, but you can specify:

Create/update `runtime.txt`:
```
python-3.11.0
```

#### Fix 3: Verify Start Command

In Railway dashboard:
1. Go to **Settings** → **Service**
2. Check **"Start Command"**
3. Should be: `python3 server_standalone.py`
4. If different, change it and redeploy

#### Fix 4: Check Environment Variables

Railway automatically sets `PORT` environment variable. Make sure your code reads it:

Your code should have:
```python
port = int(os.environ.get('PORT', 3000))
```

This is already in your code! ✅

#### Fix 5: Force Redeploy

1. In Railway dashboard
2. Go to **Settings** → **Service**
3. Click **"Redeploy"**
4. Or push a new commit to trigger redeploy

### Step 4: Check Build Logs

1. **Click on your deployment**
2. **Click "Build Logs"**
3. Look for:
   - ✅ "Build successful"
   - ✅ "Deploying..."
   - ❌ Any errors

### Step 5: Verify Health Check

Railway needs to detect your service is running. Your server should:
- ✅ Listen on the PORT environment variable
- ✅ Respond to HTTP requests
- ✅ Not crash on startup

---

## Quick Fix Checklist

- [ ] `Procfile` exists and is correct
- [ ] `server_standalone.py` is in root directory
- [ ] Railway logs show no errors
- [ ] Start command is set correctly
- [ ] PORT environment variable is being read
- [ ] Server binds to `0.0.0.0` (not `localhost`)

---

## Manual Test

To test if your server works locally with Railway's setup:

```bash
# Set PORT like Railway does
export PORT=3000

# Run server
python3 server_standalone.py

# Should see: "Server running on http://0.0.0.0:3000"
```

If this works locally, it should work on Railway.

---

## Still Not Working?

1. **Check Railway Status**: https://status.railway.app
2. **View detailed logs** in Railway dashboard
3. **Try redeploying** from Railway dashboard
4. **Check if service is set to "Web Service"** (not "Worker")

---

## Alternative: Use Railway CLI

If web interface isn't working:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Deploy
railway up

# View logs
railway logs
```

