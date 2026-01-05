# Quick Start Guide

## Current Status

✅ **Complete Features:**
- Beautiful landing page with modern UI
- Website scanning functionality
- AI audit system (8 checks)
- Score calculation and display
- Error handling
- Responsive design
- Comprehensive test suite

## To Run the Website

### Step 1: Install Dependencies
```bash
npm install
```

This will install:
- express (web server)
- axios (HTTP requests)
- cheerio (HTML parsing)
- cors (CORS support)

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

## Testing the Application

### Manual Testing
1. Open http://localhost:3000 in your browser
2. Enter a website URL (e.g., `https://example.com`)
3. Click "Scan my site"
4. View the AI readiness score and detailed audit results

### Automated Testing
```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage
```

## What the Audit Checks

The system checks for:
1. **Title Tag** - Presence of `<title>` tag
2. **Meta Description** - Meta description (50+ chars preferred)
3. **Structured Data** - JSON-LD or microdata (Schema.org)
4. **Semantic HTML** - Use of header, nav, main, article, etc.
5. **Image Alt Text** - Alt attributes on images
6. **Heading Hierarchy** - Proper h1/h2 structure
7. **Open Graph Tags** - Social media meta tags
8. **Robots Meta** - Crawlability (not blocked by noindex)

## Project Structure

```
ai-website-audit/
├── server.js          # Express server + audit logic
├── app.js             # Frontend JavaScript
├── index.html         # Landing page
├── styles.css         # Styling
├── server.test.js     # Test suite
├── jest.config.js     # Jest configuration
└── package.json       # Dependencies & scripts
```

