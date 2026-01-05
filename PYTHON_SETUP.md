# Running with Python (No Node.js Required!)

## Quick Start

Simply run:
```bash
./start_python.sh
```

This script will:
1. Check for Python 3
2. Create a virtual environment (if needed)
3. Install dependencies
4. Start the server

## Manual Setup

### Step 1: Check Python 3
```bash
python3 --version
```
If not installed, get it from: https://www.python.org/

### Step 2: Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Server
```bash
python3 server.py
```

Or specify a different port:
```bash
python3 server.py 8080
```

### Step 5: Open in Browser
Navigate to: **http://localhost:3000**

## What's Different?

The Python version (`server.py`) does exactly the same thing as the Node.js version:
- ✅ Same audit checks (8 checks)
- ✅ Same scoring system
- ✅ Same API endpoints
- ✅ Same frontend (no changes needed)

**Technologies:**
- Flask (instead of Express)
- BeautifulSoup4 (instead of Cheerio)
- Requests (instead of Axios)

## Troubleshooting

**"python3: command not found"**
- Install Python 3 from https://www.python.org/
- Or use Homebrew: `brew install python3`

**"pip: command not found"**
- Try: `python3 -m pip install -r requirements.txt`

**Port already in use:**
- Change port: `python3 server.py 8080`
- Or kill the process using port 3000

**Import errors:**
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`



