# Phase 6: Automation Setup (macOS & Windows Compatible)

## Overview
Phase 6 automates the sensor data ingestion pipeline so it runs continuously without manual intervention. This guide covers both macOS and Windows setups.

---

## ✅ Updated Files (Cross-Platform)

### 1. **dashboard.py** - Fixed Credentials
- Changed from hardcoded `user="postgres"` to `os.getenv("DB_USER")`
- Now reads all credentials from `.env` file
- Works on both macOS and Windows

### 2. **requirements.txt** - Complete Dependencies
Updated with all required packages:
- `streamlit>=1.20.0` (dashboard)
- `python-dotenv>=0.20.0` (environment variables)
- `plotly>=5.0.0` (visualizations)
- `psycopg2-binary>=2.9.0` (database)

### 3. **api_wrappers/openweather.py** - Secure API Key
- API key now read from `.env` instead of hardcoded
- City name configurable via `CITY` env variable
- Works on both platforms

### 4. **.env** - Centralized Configuration
```env
DB_NAME=energy_db
DB_USER=ianvallejo
DB_HOST=localhost
DB_PORT=5432

OPENWEATHER_API_KEY=0723d71a05e58ae3f7fc91e39a901e6b
CITY=Manila
```

---

## 🚀 NEW Cross-Platform Scripts

### **run_ingest.py** - Main Ingestion Script
A Python-based automation tool that replaces the old batch file. Works on Windows, macOS, and Linux.

**Features:**
- Single run or continuous daemon mode
- Configurable interval (default: 5 minutes)
- Logging to file and console
- Cross-platform compatibility

**Usage:**
```bash
# Single ingestion
python3 run_ingest.py

# Daemon mode (every 5 minutes, Ctrl+C to stop)
python3 run_ingest.py --daemon

# Custom interval (300 seconds = 5 minutes)
python3 run_ingest.py --daemon --interval 300

# Help
python3 run_ingest.py --help
```

---

## 🔧 macOS Automation Setup

### **setup_scheduler_mac.sh** - Automated Launchd Setup

This script creates a macOS LaunchAgent that runs ingestion every 5 minutes automatically.

**Installation:**
```bash
# Make the setup script executable
chmod +x setup_scheduler_mac.sh

# Run the setup
./setup_scheduler_mac.sh
```

**What it does:**
1. Creates a `.plist` file in `~/Library/LaunchAgents/`
2. Registers the LaunchAgent with macOS
3. Ingestion now runs every 5 minutes automatically in the background

**Manual Launchd Commands:**
```bash
# Check if running
launchctl list | grep energy.sensor

# Stop the service
launchctl unload ~/Library/LaunchAgents/com.energy.sensor.ingestion.plist

# Start the service
launchctl load ~/Library/LaunchAgents/com.energy.sensor.ingestion.plist

# View logs
tail -f logs/ingestion.log
```

---

## 🪟 Windows Automation Setup

### **run_ingest.bat** - Windows Batch File

Simple batch file for Windows. Can be run manually or scheduled with Task Scheduler.

**Manual Run:**
```cmd
run_ingest.bat
```

**Schedule with Task Scheduler:**
1. Open "Task Scheduler" (Windows search: `taskschd.msc`)
2. Click "Create Basic Task..."
3. Name it: "Sensor Ingestion"
4. Set Trigger: "Daily" (or "On a schedule")
5. Set Action:
   - Program: `C:\path\to\repo\run_ingest.bat`
   - Start in: `C:\path\to\repo\`
6. Click "Finish"

The task will now run at your scheduled time.

---

## 📊 Monitoring & Logs

Both platforms write logs to the same location:
```
logs/ingestion.log       # Main ingestion logs (rotated daily)
logs/ingestion.*.log     # Rotated historical logs
```

**View logs on macOS:**
```bash
tail -f logs/ingestion.log        # Live view
cat logs/ingestion.log            # Full history
```

**View logs on Windows:**
```cmd
type logs\ingestion.log           # View file
```

---

## 🔐 Security Notes

✅ **Done:**
- API keys now in `.env` (not in source code)
- Database credentials in `.env`
- All hardcoded secrets removed

⚠️ **Important:**
- Never commit `.env` to Git
- Add `.env` to `.gitignore` (it's already there)
- Keep `.env` secure on your machine

---

## 📈 Phase 6 Checklist

- [x] Cross-platform automation script (`run_ingest.py`)
- [x] macOS scheduler setup (`setup_scheduler_mac.sh`)
- [x] Windows batch file (`run_ingest.bat`)
- [x] Remove hardcoded credentials
- [x] Update dashboard.py to use `.env`
- [x] Update openweather.py to use `.env`
- [x] Update requirements.txt with all deps
- [x] Fix sensor_ingest.py paths

---

## ✅ Next Steps (Phase 7 onwards)

- **Phase 7:** Build Streamlit dashboard
  ```bash
  python3 -m streamlit run dashboard.py
  ```

- **Phase 8:** Real-time sensor simulation
  ```bash
  python3 db/sensor_stream_sim.py
  ```

- **Phase 9:** Predictive analytics (ML models)

- **Phase 11:** OpenWeather/NASA POWER API integration

---

## 🐛 Troubleshooting

**"ModuleNotFoundError: No module named 'db_connector'"**
- Ensure you're in the repo root directory
- Run from the correct location

**"connection to server at 'localhost' failed"**
- Start PostgreSQL first
- On macOS: `brew services start postgresql@15`
- On Windows: `pg_ctl -D ... start`

**"No such file or directory: data/sensor_logs.txt"**
- Run ingestion from repo root: `cd /path/to/repo && python3 run_ingest.py`
- Or use absolute paths in `.env`

