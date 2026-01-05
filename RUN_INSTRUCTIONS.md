# How to Run the Site Locally

## Quick Start (Easiest Method)

Simply run the startup script:

```bash
./start.sh
```

This will:
1. Install dependencies if needed
2. Start the server
3. Show you the URL to open

## Manual Method

### Step 1: Install Dependencies
```bash
npm install
```

### Step 2: Start the Server
```bash
npm start
```

Or for development with auto-reload:
```bash
npm run dev
```

### Step 3: Open in Browser
Navigate to: **http://localhost:3000**

## Testing the Site

Once the server is running:

1. **Open your browser** and go to `http://localhost:3000`
2. **Enter a website URL** (e.g., `https://example.com`)
3. **Click "Scan my site"**
4. **View the results:**
   - AI Readiness Score (0-100)
   - Detailed breakdown of 8 audit checks

## Test URLs to Try

- `https://example.com` - Basic test site
- `https://github.com` - Well-structured site
- `https://google.com` - Minimal site
- `https://wikipedia.org` - Content-rich site

## Troubleshooting

**If you get "npm: command not found":**
- Install Node.js from https://nodejs.org/
- Or use a Node version manager like nvm

**If port 3000 is already in use:**
- Change the PORT in `server.js` or set environment variable:
  ```bash
  PORT=3001 npm start
  ```

**If dependencies fail to install:**
- Make sure you have internet connection
- Try: `npm install --verbose` to see detailed errors

