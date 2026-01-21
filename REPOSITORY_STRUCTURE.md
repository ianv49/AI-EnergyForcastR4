# Project Structure & Organization

This document describes the organization of the AI-EnergyForcastR4 repository.

## 📁 Repository Structure

```
AI-EnergyForcastR4/
│
├── 📄 README.md                 # Main project documentation
├── 📄 requirements.txt          # Python dependencies (pip install -r)
├── 📄 .env                      # Environment variables (DO NOT commit)
├── 📄 .gitignore                # Git ignore rules
│
├── 📂 dashboards/               # Visualization & UI
│   └── dashboard.py             # Streamlit dashboard
│
├── 📂 scripts/                  # Automation & utilities
│   ├── run_ingest.py            # Cross-platform ingestion automation
│   ├── run_ingest.bat           # Windows batch automation
│   └── setup_scheduler_mac.sh   # macOS Launchd scheduler setup
│
├── 📂 db/                       # Database layer
│   ├── db_connector.py          # PostgreSQL connection manager
│   ├── db_ingest.py             # Data ingestion from TXT/CSV
│   ├── sensor_stream_sim.py     # Simulated sensor data generator
│   ├── test_connection.py       # Database connection test
│   ├── api_ingest_openweather.py# OpenWeather API ingestion
│   └── schema.sql               # Database schema (reference)
│
├── 📂 api_wrappers/             # External API integrations
│   ├── openweather.py           # OpenWeather API wrapper
│   └── nasa_power.py            # NASA POWER API wrapper (pending)
│
├── 📂 sensors/                  # Sensor data collection
│   └── sensor_ingest.py         # Sensor data ingestion utilities
│
├── 📂 preprocessing/            # Data cleaning & normalization
│   └── preprocess.py            # Data preprocessing functions
│
├── 📂 data/                     # Data storage
│   ├── sensor_logs.txt          # Raw sensor logs
│   └── sensor_data.csv          # Sample CSV data
│
├── 📂 logs/                     # Application logs
│   ├── ingestion.log            # Current ingestion log (daily rotation)
│   └── ingestion.log.YYYY-MM-DD # Archived daily logs
│
├── 📂 notebooks/                # Jupyter notebooks
│   └── data_pipeline_demo.py    # Data pipeline demonstration
│
├── 📂 docs/                     # Documentation
│   ├── PHASE6_AUTOMATION.md     # Phase 6 setup guide
│   ├── PHASE6_COMPLETION.md     # Phase 6 summary
│   └── myNotes.txt              # Development notes
│
├── 📂 tests/                    # Testing
│   └── test_imports.py          # Library import tests
│
└── 📂 .git/                     # Git version control
```

---

## 📋 File Organization by Function

### 🎯 Core Application (Root Level)
- `README.md` — Main documentation
- `requirements.txt` — All dependencies
- `.env` — Configuration (secrets, credentials)
- `.gitignore` — Git exclusions

### 📊 Dashboards (`dashboards/`)
- `dashboard.py` — Streamlit web interface for visualization

### 🔧 Automation Scripts (`scripts/`)
- `run_ingest.py` — Main ingestion automation (Python, cross-platform)
- `run_ingest.bat` — Windows Task Scheduler compatibility
- `setup_scheduler_mac.sh` — macOS Launchd setup

### 🗄️ Database Layer (`db/`)
- `db_connector.py` — Connection pooling & management
- `db_ingest.py` — Data ingestion pipeline
- `sensor_stream_sim.py` — Simulated sensor data generator
- `test_connection.py` — Connection verification
- `api_ingest_openweather.py` — API data ingestion
- `schema.sql` — Database schema reference

### 🌐 External APIs (`api_wrappers/`)
- `openweather.py` — Weather API client (working)
- `nasa_power.py` — Solar radiation API client (pending)

### 📡 Sensor Integration (`sensors/`)
- `sensor_ingest.py` — Real sensor data collection

### 🧹 Data Processing (`preprocessing/`)
- `preprocess.py` — Normalization, cleaning, interpolation (pending)

### 📂 Data Storage (`data/`)
- `sensor_logs.txt` — Raw sensor readings
- `sensor_data.csv` — Sample structured data

### 📝 Documentation (`docs/`)
- `PHASE6_AUTOMATION.md` — Setup & deployment guide
- `PHASE6_COMPLETION.md` — Phase summary
- `myNotes.txt` — Development notes & progress

### ✅ Tests (`tests/`)
- `test_imports.py` — Dependency verification

### 📓 Notebooks (`notebooks/`)
- `data_pipeline_demo.py` — Interactive demonstrations

### 🔐 Logs (`logs/`)
- `ingestion.log` — Current daily log (rotated at midnight)
- `ingestion.log.2026-01-20` — Archived logs

---

## 🔄 Data Flow

```
Sensor Data Sources
    ↓
[sensors/] → Raw sensor readings
    ↓
[db/sensor_stream_sim.py] → Simulate/transform
    ↓
[db/db_ingest.py] → Normalize & insert
    ↓
PostgreSQL Database
    ↓
[dashboards/dashboard.py] ← Read & visualize
↓
[api_wrappers/openweather.py] ← External APIs
    ↓
[preprocessing/preprocess.py] ← Clean & process
    ↓
[notebooks/] ← Analysis & exploration
```

---

## 🚀 Quick Start by Function

### View Data
```bash
cd dashboards
python3 -m streamlit run dashboard.py
```

### Run Ingestion (Single)
```bash
cd scripts
python3 run_ingest.py
```

### Setup Automation (macOS)
```bash
cd scripts
chmod +x setup_scheduler_mac.sh
./setup_scheduler_mac.sh
```

### Test Database Connection
```bash
cd db
python3 test_connection.py
```

### View Documentation
```bash
cd docs
cat PHASE6_AUTOMATION.md
```

---

## 📊 Phase Progress

| Phase | Folder(s) | Status |
|-------|-----------|--------|
| 1 | `db/` | ✅ Complete |
| 2 | `db/` | ✅ Complete |
| 3 | `db/` | ✅ Complete |
| 4 | `db/` | ✅ Complete |
| 5 | `db/` | ✅ Complete |
| 6 | `scripts/` | ✅ Complete |
| 7 | `dashboards/` | ⏳ In Progress |
| 8 | `db/`, `sensors/` | ⏳ Pending |
| 9 | `preprocessing/`, `notebooks/` | ⏳ Pending |
| 10 | `scripts/` | ⏳ Pending |
| 11 | `api_wrappers/` | ⏳ Pending |

---

## 🔐 Security

- **DO NOT** commit `.env` (already in `.gitignore`)
- **DO NOT** share API keys in code
- Credentials in `db/db_connector.py` read from `.env`
- API keys in `api_wrappers/` read from `.env`

---

## 🔄 Updates Required for New Structure

When referring to files, use:
- `dashboards/dashboard.py` instead of `dashboard.py`
- `scripts/run_ingest.py` instead of `run_ingest.py`
- `docs/PHASE6_AUTOMATION.md` instead of `PHASE6_AUTOMATION.md`
- `tests/test_imports.py` instead of `test_imports.py`

---

Generated: 2026-01-21 | Platform: macOS & Windows Compatible
