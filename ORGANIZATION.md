# Repository Organization Guide

## Project Structure

```
AI-EnergyForcastR4/
│
├── 📋 Core Application Code
│   ├── db/                      # Database layer
│   │   ├── db_connector.py     # Database connection management
│   │   ├── db_ingest.py        # Data ingestion scripts
│   │   ├── api_ingest_openweather.py  # Weather API ingestion
│   │   ├── sensor_stream_sim.py # Sensor stream simulator
│   │   ├── test_connection.py  # Connection tests
│   │   └── schema.sql          # Database schema
│   │
│   ├── sensors/                 # Sensor data handling
│   │   └── sensor_ingest.py    # Sensor data collection
│   │
│   ├── api_wrappers/            # External API integrations
│   │   ├── openweather.py      # OpenWeather API
│   │   └── nasa_power.py       # NASA POWER API
│   │
│   ├── preprocessing/           # Data processing
│   │   └── preprocess.py       # Data cleaning & normalization
│   │
│   ├── dashboards/              # Visualization
│   │   └── dashboard.py        # Main dashboard
│   │
│   ├── monitoring/              # Live monitoring & simulation
│   │   ├── sim_web_dashboard.py
│   │   ├── sim_dashboard.html
│   │   └── start_sim_dashboard.sh
│   │
│   └── scripts/                 # Automation & utilities
│       ├── run_ingest.py
│       ├── run_ingest.bat
│       ├── setup_scheduler_mac.sh
│       ├── start_dashboard.sh
│       └── automation/
│
├── 📊 Data & Logs
│   ├── data/                    # Data storage
│   │   ├── sensor_data.csv
│   │   └── sensor_logs.txt
│   │
│   └── logs/                    # Application logs
│       └── ingestion.log.YYYY-MM-DD
│
├── 📝 Documentation
│   ├── DOCUMENTATION_INDEX.md   # Start here
│   ├── README.md               # Project overview
│   ├── LIVE_MONITOR_QUICK_REF.md
│   ├── NEXT_SCOPE_2026.md     # Future roadmap
│   ├── ORGANIZATION.md         # This file
│   ├── REPOSITORY_STRUCTURE.md
│   │
│   └── docs/                    # Detailed documentation
│       ├── myNotes.txt
│       ├── PHASE6_AUTOMATION.md
│       ├── PHASE6_COMPLETION.md
│       ├── PHASE7_COMPLETION.md
│       ├── PHASE7_DASHBOARD.md
│       ├── PHASE8_LIVE_MONITOR.md
│       ├── PHASE8_QUICK_REFERENCE.md
│       ├── PHASE8_SIM_CONTROL.md
│       └── REORGANIZATION_SUMMARY.md
│
├── 🔧 Configuration & Setup
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   ├── .gitignore
│   └── .venv/                   # Virtual environment
│
├── 📦 Testing & Notebooks
│   ├── tests/
│   │   └── test_imports.py
│   │
│   └── notebooks/
│       └── data_pipeline_demo.py
│
└── 📚 Archive
    ├── phase-reports/           # Historical phase reports
    │   ├── PHASE8_*.md
    │   ├── EXECUTIVE_SUMMARY.md
    │   └── PROJECT_RECAP_*.md
    │
    └── documentation-backups/   # Backup documentation
        ├── SIM_WEB_DASHBOARD_*.md
        └── ORGANIZATION_GUIDE.txt
```

## Quick Start

1. **Environment Setup**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **View Documentation**
   - Start: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)
   - Quick reference: [LIVE_MONITOR_QUICK_REF.md](LIVE_MONITOR_QUICK_REF.md)
   - Roadmap: [NEXT_SCOPE_2026.md](NEXT_SCOPE_2026.md)

3. **Run Application**
   - Dashboard: `./scripts/start_dashboard.sh`
   - Live Monitor: `./monitoring/start_sim_dashboard.sh`

## Directory Purposes

| Folder | Purpose |
|--------|---------|
| `db/` | Database connections, ingestion, and schema |
| `sensors/` | Sensor data collection and handling |
| `api_wrappers/` | External API integrations (weather, solar, etc.) |
| `preprocessing/` | Data cleaning, normalization, interpolation |
| `dashboards/` | Data visualization and BI tools |
| `monitoring/` | Live monitoring dashboard and simulators |
| `scripts/` | Automation, scheduling, and utility scripts |
| `data/` | CSV, logs, and sensor data files |
| `logs/` | Application runtime logs |
| `docs/` | Detailed technical documentation |
| `tests/` | Test scripts and validation |
| `notebooks/` | Jupyter notebooks and exploratory code |
| `archive/` | Historical reports and old documentation |

## Key Files

- **DOCUMENTATION_INDEX.md** - Complete guide to all documentation
- **README.md** - Project overview and features
- **requirements.txt** - Python package dependencies
- **LIVE_MONITOR_QUICK_REF.md** - Quick reference for live monitoring
- **NEXT_SCOPE_2026.md** - Future development roadmap

