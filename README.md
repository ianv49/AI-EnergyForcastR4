# AI-EnergyForcastR4
AI-Driven Predictive Maintenance for Renewable Energy Assets 
# AI-Driven Predictive Maintenance for Renewable Energy Assets

This project develops a cross-platform application for predictive maintenance of renewable energy assets (wind turbines, solar panels, inverters, batteries). It uses IoT sensor data, external weather/solar APIs, and AI/ML models to forecast failures and optimize maintenance schedules.

---

## 🚀 Features
- Real-time sensor data ingestion (temperature, humidity, irradiance, wind speed).
- External API integration (OpenWeather, NASA POWER, Tomorrow.io).
- Local PostgreSQL + TimescaleDB storage for time-series data.
- Preprocessing scripts for normalization, cleaning, and interpolation.
- Ready for deployment on Raspberry Pi 4, but fully compatible with Mac and Windows laptops during development.

---

## 🛠️ Development Setup

### 1. Clone Repository
```bash
AI-EnergyForcastR4/
│
├── db/                     # Database setup and connectors
│   ├── db_connector.py     # Python script to handles DB connection
│   ├── db_ingest.py        # Python script to ingestion script (imports connector)
│   ├── test_connection.py  # Python script for quick connection test
│   └── schema.sql          # SQL table definitions
│
├── data/                 
│   ├── sensor_logs.txt   # plain text log file 
│   └── sensor_data.csv   # CSV file 
│
├── .env
├── requirements.txt      # List of Python dependencies
├── README.md             # Documentation for setup and usage
├── logs/
│   └── ingestion.log         # today’s log)
│   └── ingestion.log.2026-01-20  #yesterday’s log, auto‑created at midnight
│
├── sensors/              # Scripts for sensor data (real or simulated)
│   └── sensor_ingest.py  # First script: generate or simulate sensor readings
│
├── api_wrappers/         # External API modules
│   └── openweather.py    # First wrapper: fetch weather data
│   └── nasa_power.py     # Second wrapper: fetch solar/irradiance data
│
│
├── preprocessing/        # Data cleaning scripts
│   └── preprocess.py     # First script: normalize and clean sensor logs
│
└── notebooks/            # Jupyter notebooks for demos
    └── data_pipeline_demo.ipynb  # Step-by-step interactive demo

#### my notes
'''bash
Perfect 🎉 — that package list shows your environment is now fully set up and healthy. You’ve got all the core libraries installed:
requests → API calls and HTTP requests
pandas → data handling and analysis
numpy → numerical computations
psycopg2-binary → PostgreSQL connector
scikit-learn → classical machine learning models
torch → PyTorch deep learning framework
matplotlib → static plotting
plotly → interactive charts
paho-mqtt → IoT sensor communication
Plus all their dependencies (like scipy, joblib, threadpoolctl, etc.). This means you’re ready to start coding your actual project.
PS D:\My Documents\tools\skul\bsu2024\bsu_mot512_thesis1\GithubVisualStudioCode\AI-EnergyForcastR4> python -m pip list
Package            Version
------------------ -----------
certifi            2026.1.4
charset-normalizer 3.4.4
contourpy          1.3.3
cycler             0.12.1
filelock           3.20.3
fonttools          4.61.1
fsspec             2026.1.0
idna               3.11
Jinja2             3.1.6
joblib             1.5.3
kiwisolver         1.4.9
MarkupSafe         3.0.3
matplotlib         3.10.8
mpmath             1.3.0
narwhals           2.15.0
networkx           3.6.1
numpy              2.4.1
packaging          25.0
paho-mqtt          2.1.0
pandas             2.3.3
pillow             12.1.0
pip                25.3
plotly             6.5.2
psycopg2-binary    2.9.11
pyparsing          3.3.1
python-dateutil    2.9.0.post0
pytz               2025.2
requests           2.32.5
scikit-learn       1.8.0
scipy              1.17.0
setuptools         80.9.0
six                1.17.0
sympy              1.14.0
threadpoolctl      3.6.0
torch              2.9.1
typing_extensions  4.15.0
tzdata             2025.3
urllib3            2.6.3

[always used for activating env; "venv\Scripts\activate.bat"]
[This starts PostgreSQL in the background, listening on port 5432.
Since you don’t have admin rights, it won’t be a Windows service — you’ll need to run this manually each time.
in <cmd> <"D:\My Documents\tools\postgresql\pgsql\bin\pg_ctl.exe" -D "D:\My Documents\tools\postgresql\pgsql\data" -l logfile start>]
[Stopping PostgreSQL. When you’re done, stop the server cleanly, This shuts down PostgreSQL safely:
in cmd> <"D:\My Documents\tools\postgresql\pgsql\bin\pg_ctl.exe" -D "D:\My Documents\tools\postgresql\pgsql\data" stop>]
[Restarting PostgreSQL, If you want to restart:
in cmd> <"D:\My Documents\tools\postgresql\pgsql\bin\pg_ctl.exe" -D "D:\My Documents\tools\postgresql\pgsql\data" restart>]

...notes 260119;
Phase,Item,Status
Phase 1: Environment Setup,Install PostgreSQL portable binaries,Done
Phase 1: Environment Setup,Initialize database cluster (initdb),Done
Phase 1: Environment Setup,Start PostgreSQL manually (pg_ctl),Done
Phase 1: Environment Setup,Connect with psql,Done
Phase 2: Database Schema,Create energy_db database,Done
Phase 2: Database Schema,Define sensor_data table schema,Done
Phase 2: Database Schema,Verify schema with \d sensor_data,Done
Phase 3: Python Integration,Install psycopg2 driver,Done
Phase 3: Python Integration,Create db_ingest.py script,Done
Phase 3: Python Integration,Connect Python to PostgreSQL,Done
Phase 3: Python Integration,Insert test row via Python,Done
Phase 3: Python Integration,Fetch and display rows via Python,Done
Phase 4: Log Ingestion,Adapt script to read sensor_logs.txt,Done
Phase 4: Log Ingestion,Insert multiple rows from file,Done
Phase 4: Log Ingestion,Verify ingestion with query output,Done
Phase 5: Enhancements,Handle duplicate entries (unique timestamp + ON CONFLICT),Pending
Phase 5: Enhancements,Format timestamp output (seconds only),Done
Phase 5: Enhancements,Optional: pretty table output,Pending
Phase 6: Next Steps,Automate ingestion (batch file or cron job),Pending
Phase 6: Next Steps,Extend ingestion for CSV/real sensor streams,Pending
Phase 6: Next Steps,Dashboard/visualization integration,Pending

...notes 260120;
sql password = PdM
Phase,Item,Status
Phase 1: Environment Setup,Install PostgreSQL portable binaries,Done
Phase 1: Environment Setup,Initialize database cluster (initdb),Done
Phase 1: Environment Setup,Start PostgreSQL manually (pg_ctl),Done
Phase 1: Environment Setup,Connect with psql,Done
Phase 2: Database Schema,Create energy_db database,Done
Phase 2: Database Schema,Define sensor_data table schema,Done
Phase 2: Database Schema,Verify schema with \d sensor_data,Done
Phase 3: Python Integration,Install psycopg2 driver,Done
Phase 3: Python Integration,Create db_ingest.py script,Done
Phase 3: Python Integration,Connect Python to PostgreSQL,Done
Phase 3: Python Integration,Insert test row via Python,Done
Phase 3: Python Integration,Fetch and display rows via Python,Done
Phase 4: Log Ingestion,Adapt script to read sensor_logs.txt,Done
Phase 4: Log Ingestion,Insert multiple rows from file,Done
Phase 4: Log Ingestion,Verify ingestion with query output,Done
Phase 5: Enhancements,Handle duplicate entries (unique timestamp + ON CONFLICT),Done
Phase 5: Enhancements,Format timestamp output (seconds only),Done
Phase 5: Enhancements,Pretty table output (tabulate),Done
Phase 5: Enhancements,Row count before/after ingestion,Done
Phase 5: Enhancements,Skip header line in text ingestion,Done
Phase 5: Enhancements,Modularize connection into db_connector.py,Done
Phase 5: Enhancements,Add test_connection.py script,Done
Phase 5: Enhancements,Show top/bottom rows in test script,Done
Phase 6: Next Steps,Automate ingestion (batch file or cron job),Pending
Phase 6: Next Steps,Extend ingestion for CSV/real sensor streams,Pending
Phase 6: Next Steps,Dashboard/visualization integration,Pending
Phase 6: Next Steps,Add permanent log file output (logs/ingestion.log),Done
Phase 6: Next Steps,Daily log rotation (TimedRotatingFileHandler),Done
Phase 7: Visualization & Dashboard,Plot temperature vs timestamp chart,Pending
Phase 7: Visualization & Dashboard,Add multiple charts (humidity, irradiance, wind speed),Pending
Phase 7: Visualization & Dashboard,Build simple dashboard (Streamlit or Grafana),Pending
Phase 8: Real-Time Ingestion,Simulate sensor streams (append rows every minute),Pending
Phase 8: Real-Time Ingestion,Enable continuous ingestion pipeline,Pending
Phase 9: Predictive Analytics,Calculate averages/min/max/moving averages,Pending
Phase 9: Predictive Analytics,Train ML model for forecasting (scikit-learn),Pending
Phase 10: Deployment & Scaling,Containerize with Docker,Pending
Phase 10: Deployment & Scaling,Deploy to cloud (AWS/Azure/GCP),Pending
Phase 11: Web-Sensor Data Integration,Connect to OpenWeather API for local weather data,Pending
Phase 11: Web-Sensor Data Integration,Ingest NASA POWER API for solar irradiance and climate data,Pending
Phase 11: Web-Sensor Data Integration,Integrate PVOutput API for solar PV system performance,Pending
Phase 11: Web-Sensor Data Integration,Optional: Add other APIs (NOAA, Meteostat, etc.),Pending
Phase 11: Web-Sensor Data Integration,Normalize and store web-sensor data into sensor_data table,Pending
Phase 11: Web-Sensor Data Integration,Combine local sensor + web API data for richer analytics,Pending
...Phase 6: Automate Ingestion
Step 2: Windows Batch File (simple automation)
    Open Notepad.
    Paste this:
        bat
        @echo off
        cd /d "D:\My Documents\tools\skul\bsu2024\bsu_mot512_thesis1\GithubVisualStudioCode\AI-EnergyForcastR4"
        python db\db_ingest.py
    Save as run_ingest.bat in your repo root.
    Double‑click it → ingestion runs, logs go to logs/ingestion.log.
Step 3: Schedule with Task Scheduler
    Open Task Scheduler (Windows search).
    Create a new task → “Run Ingestion Daily”.
    Set trigger → every day at 4:00 PM.
    Set action → run run_ingest.bat.
    Save → ingestion now runs automatically.

...notes 260121;
Phase,Item,Status
Phase 1: Environment Setup,Install PostgreSQL portable binaries,Done
Phase 1: Environment Setup,Initialize database cluster (initdb),Done
Phase 1: Environment Setup,Start PostgreSQL manually (pg_ctl),Done
Phase 1: Environment Setup,Connect with psql,Done
Phase 2: Database Schema,Create energy_db database,Done
Phase 2: Database Schema,Define sensor_data table schema,Done
Phase 2: Database Schema,Verify schema with \d sensor_data,Done
Phase 3: Python Integration,Install psycopg2 driver,Done
Phase 3: Python Integration,Create db_ingest.py script,Done
Phase 3: Python Integration,Connect Python to PostgreSQL,Done
Phase 3: Python Integration,Insert test row via Python,Done
Phase 3: Python Integration,Fetch and display rows via Python,Done
Phase 4: Log Ingestion,Adapt script to read sensor_logs.txt,Done
Phase 4: Log Ingestion,Insert multiple rows from file,Done
Phase 4: Log Ingestion,Verify ingestion with query output,Done
Phase 5: Enhancements,Handle duplicate entries (unique timestamp + ON CONFLICT),Done
Phase 5: Enhancements,Format timestamp output (seconds only),Done
Phase 5: Enhancements,Pretty table output (tabulate),Done
Phase 5: Enhancements,Row count before/after ingestion,Done
Phase 5: Enhancements,Skip header line in text ingestion,Done
Phase 5: Enhancements,Modularize connection into db_connector.py,Done
Phase 5: Enhancements,Add test_connection.py script,Done
Phase 5: Enhancements,Show top/bottom rows in test script,Done
Phase 6: Next Steps,Automate ingestion (batch file or cron job),Done
Phase 6: Next Steps,Extend ingestion for CSV/real sensor streams,Done (simulation script ready)
Phase 6: Next Steps,Dashboard/visualization integration,Done (Streamlit dashboard running)
Phase 6: Next Steps,Add permanent log file output (logs/ingestion.log),Done
Phase 6: Next Steps,Daily log rotation (TimedRotatingFileHandler),Done
Phase 7: Visualization & Dashboard,Plot temperature vs timestamp chart,Done
Phase 7: Visualization & Dashboard,Add multiple charts (humidity, irradiance, wind speed),Done
Phase 7: Visualization & Dashboard,Build simple dashboard (Streamlit with sidebar),Done
Phase 8: Real-Time Ingestion,Simulate sensor streams (append rows every 5minute),Done
Phase 8: Real-Time Ingestion,Enable continuous ingestion pipeline,Pending
Phase 9: Predictive Analytics,Calculate averages/min/max/moving averages,Pending
Phase 9: Predictive Analytics,Train ML model for forecasting (scikit-learn),Pending
Phase 10: Deployment & Scaling,Containerize with Docker,Pending
Phase 10: Deployment & Scaling,Deploy to cloud (AWS/Azure/GCP),Pending
Phase 11: Web-Sensor Data Integration,Connect to OpenWeather API for local weather data,Pending
Phase 11: Web-Sensor Data Integration,Ingest NASA POWER API for solar irradiance and climate data,Pending
Phase 11: Web-Sensor Data Integration,Integrate PVOutput API for solar PV system performance,Pending
Phase 11: Web-Sensor Data Integration,Optional: Add other APIs (NOAA, Meteostat, etc.),Pending
Phase 11: Web-Sensor Data Integration,Normalize and store web-sensor data into sensor_data table,Pending
Phase 11: Web-Sensor Data Integration,Combine local sensor + web API data for richer analytics,Pending
...Recap
    Use View → Terminal if `Ctrl+`` doesn’t work.
    Run dashboard → python -m streamlit run dashboard.py.
    Stop dashboard → Ctrl + C.
    Optional background run → Start-Process python "-m streamlit run dashboard.py".
    Now dashboard should run reliably.
    next to add OpenWeather API ingestion so dashboard shows both local sensor data and live weather data.
...work on mac.
...AI review of files:
    File,Type,Location,Lines,Status,Purpose,Issues
    dashboard.py,Python,root,60,Needs Update,Streamlit dashboard for data visualization,Hardcoded postgres credentials
    db_connector.py,Python,db/,28,✅ Working,Centralized DB connection handler,Uses .env variables (proper)
    db_ingest.py,Python,db/,144,✅ Working,Ingest sensor data from TXT/CSV,Proper logging with rotation
    test_connection.py,Python,db/,15,✅ Working,Verify PostgreSQL connection,Simple test script
    sensor_stream_sim.py,Python,db/,30,✅ Working,Real-time sensor data simulator,5-minute interval generation
    api_ingest_openweather.py,Python,db/,?,Pending,OpenWeather API integration,Not reviewed (likely incomplete)
    sensor_ingest.py,Python,sensors/,20,⚠️ Incomplete,Sensor data collection,Uses old path (sensor_logs.txt)
    preprocess.py,Python,preprocessing/,?,Empty,Data cleaning/normalization,No implementation yet
    openweather.py,Python,api_wrappers/,17,✅ Working,OpenWeather API wrapper,API key visible (security concern)
    nasa_power.py,Python,api_wrappers/,?,Empty,NASA POWER API wrapper,No implementation yet
    requirements.txt,Text,root,23,⚠️ Outdated,Python dependencies list,Missing: streamlit
    schema.sql,SQL,db/,?,Empty,Database schema definition,No implementation yet
    test_imports.py,Python,root,8,✅ Working,Verify library imports,Simple check
    sensor_data.csv,CSV,data/,5,✅ Complete,Sample sensor data,2 rows of data
    sensor_logs.txt,Text,data/,5,✅ Complete,Sensor logs (raw),5 rows after ingestion
    .env,Config,root,7,✅ Configured,Environment variables,Credentials properly set for macOS
    README.md,Markdown,root,258,✅ Complete,Project documentation,Well-documented
    myNotes.txt,Text,root,378,✅ Complete,Development notes,Phase tracking included
    run_ingest.bat,Batch,root,?,Incomplete,Windows automation script,Not updated for macOS
..RECAP
    ✅ WORKING & READY
    Database Layer: PostgreSQL running, 3 rows ingested successfully
    Ingestion Pipeline: db_ingest.py with proper logging & ON CONFLICT handling
    Connection Pool: db_connector.py uses .env for credentials (secure)
    Sensor Simulator: sensor_stream_sim.py generates data every 5 minutes
    API Wrapper: openweather.py fetches real weather data
    ⚠️ INCOMPLETE/NEEDS FIXES
    dashboard.py — Hardcoded credentials, needs .env update
    requirements.txt — Missing streamlit, plotly, etc.
    preprocess.py — Empty (no data cleaning logic)
    nasa_power.py — Empty (not implemented)
    schema.sql — Empty (schema created in psql, not via SQL file)
    run_ingest.bat — Windows-only (need macOS equivalent)
    sensor_ingest.py — Points to wrong file path
    🔒 SECURITY CONCERNS
    OpenWeather API key visible in openweather.py (should use .env)
    dashboard.py has hardcoded credentials
    📈 NEXT PRIORITIES
    Fix dashboard.py to use .env credentials
    Update requirements.txt with all dependencies
    Implement preprocess.py for data cleaning
    Implement nasa_power.py API wrapper
    Create macOS automation script (replace .bat)
    Test Streamlit dashboard end-to-end