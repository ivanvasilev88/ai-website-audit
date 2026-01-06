# Fix Railway "Server Offline" Issue

## Quick Fix Steps

### Step 1: Check Railway Logs

1. **Go to Railway dashboard**: https://railway.app
2. **Click on your project**
3. **Click on your service**
4. **Click "Deployments" tab**
5. **Click on the latest deployment**
6. **Click "View Logs"**

**Look for:**
- ✅ "Server running on http://0.0.0.0:XXXX"
- ✅ "Server is ready and listening"
- ❌ Any error messages

### Step 2: Verify Service Type

1. **Go to Settings** → **Service**
2. **Make sure service type is "Web Service"** (not "Worker")
3. **Start Command should be**: `python3 server_standalone.py`

### Step 3: Check These Files Are Pushed to GitHub

Make sure these files are in your GitHub repo:
- ✅ `server_standalone.py`
- ✅ `Procfile` (with: `web: python3 server_standalone.py`)
- ✅ `railway.json` (optional but helpful)
- ✅ `index.html`
- ✅ `app.js`
- ✅ `styles.css`

### Step 4: Force Redeploy

1. **In Railway dashboard**
2. **Go to your service**
3. **Click "Settings"**
4. **Scroll down to "Redeploy"**
5. **Click "Redeploy"**

Or push a new commit:
```bash
git add .
git commit -m "Fix Railway deployment"
git push
```

### Step 5: Check Environment Variables

Railway automatically sets `PORT`. Verify:
1. **Settings** → **Variables**
2. **PORT** should be automatically set (don't set it manually)
3. Your code reads it: `os.environ.get('PORT', 3000)` ✅

---

## Common Issues & Solutions

### Issue: "No logs" or "Service offline"

**Solution:**
- Check if build completed successfully
- Look at "Build Logs" tab
- Make sure Python is detected

### Issue: "Port already in use"

**Solution:**
- Railway sets PORT automatically
- Don't hardcode port 3000
- Code already uses `os.environ.get('PORT')` ✅

### Issue: "Module not found"

**Solution:**
- Your code uses only standard library ✅
- No external dependencies needed
- Should work fine

### Issue: "Service type wrong"

**Solution:**
- Must be "Web Service" not "Worker"
- Check in Settings → Service

---

## Verify Your Setup

Run this locally to test:

```bash
# Simulate Railway environment
export PORT=3000
python3 server_standalone.py
```

Should see:
```
🚀 Server running on http://0.0.0.0:3000
✅ Server is ready and listening on port 3000
```

If this works locally, it should work on Railway.

---

## Still Not Working?

1. **Share Railway logs** - Copy the error messages
2. **Check Railway status**: https://status.railway.app
3. **Try Railway CLI**:
   ```bash
   npm install -g @railway/cli
   railway login
   railway link
   railway logs
   ```

---

## Files to Commit

Make sure you commit and push:

```bash
git add Procfile railway.json server_standalone.py
git commit -m "Fix Railway deployment configuration"
git push
```

Then Railway will automatically redeploy!

