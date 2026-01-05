# GitHub Setup Guide

## Option 1: Use GitHub Desktop (Easiest - No Terminal Needed!)

### Step 1: Install GitHub Desktop
1. Download from: https://desktop.github.com
2. Install and open GitHub Desktop
3. Sign in with your GitHub account

### Step 2: Publish Your Repository
1. In GitHub Desktop, click "File" → "Add Local Repository"
2. Navigate to: `/Users/ivanvasilev/ai-website-audit`
3. Click "Add Repository"
4. Click "Publish repository" button
5. Choose a name (e.g., `ai-website-audit`)
6. Make sure "Keep this code private" is UNCHECKED (for public repo)
7. Click "Publish Repository"

**Done!** Your code is now on GitHub. Skip to Railway deployment.

---

## Option 2: Use Terminal with Personal Access Token

### Step 1: Create Personal Access Token

1. **Go to GitHub**: https://github.com
2. **Click your profile** (top right) → **Settings**
3. **Scroll down** → Click **"Developer settings"** (left sidebar)
4. **Click "Personal access tokens"** → **"Tokens (classic)"**
5. **Click "Generate new token"** → **"Generate new token (classic)"**
6. **Name it**: `railway-deployment` (or any name)
7. **Select scopes**: Check **"repo"** (this gives full repository access)
8. **Click "Generate token"**
9. **COPY THE TOKEN** (you won't see it again!)
   - It looks like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Step 2: Use Token to Push

```bash
cd /Users/ivanvasilev/ai-website-audit

# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-website-audit.git

# When pushing, use your token as password
git branch -M main
git push -u origin main

# When prompted:
# Username: YOUR_GITHUB_USERNAME
# Password: PASTE_YOUR_TOKEN_HERE (the ghp_... token)
```

---

## Option 3: Use SSH Keys (More Secure)

### Step 1: Check if you have SSH key

```bash
ls -al ~/.ssh
```

If you see `id_rsa.pub` or `id_ed25519.pub`, you have a key. Skip to Step 3.

### Step 2: Generate SSH Key

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter to accept default file location
# Press Enter for no passphrase (or set one if you want)

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519
```

### Step 3: Add SSH Key to GitHub

```bash
# Copy your public key
cat ~/.ssh/id_ed25519.pub
# Or if you have id_rsa:
# cat ~/.ssh/id_rsa.pub
```

1. **Copy the entire output** (starts with `ssh-ed25519` or `ssh-rsa`)
2. **Go to GitHub** → **Settings** → **SSH and GPG keys**
3. **Click "New SSH key"**
4. **Title**: `My Mac` (or any name)
5. **Key**: Paste your key
6. **Click "Add SSH key"**

### Step 4: Use SSH URL

```bash
cd /Users/ivanvasilev/ai-website-audit

# Use SSH URL instead of HTTPS
git remote add origin git@github.com:YOUR_USERNAME/ai-website-audit.git

# Push (no password needed!)
git branch -M main
git push -u origin main
```

---

## Option 4: Create Repo on GitHub Website First

### Step 1: Create Repository on GitHub

1. **Go to**: https://github.com/new
2. **Repository name**: `ai-website-audit`
3. **Description**: (optional) "AI Website Audit Tool"
4. **Visibility**: Public (or Private if you prefer)
5. **DO NOT** check "Initialize with README"
6. **Click "Create repository"**

### Step 2: Use GitHub's Instructions

GitHub will show you commands. Use these:

```bash
cd /Users/ivanvasilev/ai-website-audit

# Initialize (if not done)
git init
git add .
git commit -m "Initial commit"

# Use the commands GitHub shows you (they'll look like):
git remote add origin https://github.com/YOUR_USERNAME/ai-website-audit.git
git branch -M main
git push -u origin main
```

**For authentication**, use Option 1 (GitHub Desktop) or Option 2 (Personal Access Token).

---

## Recommended: GitHub Desktop (Easiest!)

If you're having trouble with terminal authentication, **use GitHub Desktop**:
- ✅ No terminal commands needed
- ✅ Visual interface
- ✅ Handles authentication automatically
- ✅ Easy to use

Download: https://desktop.github.com

---

## Troubleshooting

**"Permission denied" error?**
- Use Personal Access Token (Option 2) instead of password
- Or use GitHub Desktop (Option 1)

**"Repository not found" error?**
- Make sure you created the repo on GitHub first
- Check the repository name matches exactly
- Verify your username is correct

**Still having issues?**
- Use GitHub Desktop - it's the easiest option
- Or use Railway's "Deploy from local directory" feature (if available)


