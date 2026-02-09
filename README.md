# AI-EnergyForcastR4

**AI-Driven Predictive Maintenance for Renewable Energy Assets**

This project develops a cross-platform application for predictive maintenance of renewable energy assets (wind turbines, solar panels, inverters, batteries). It uses IoT sensor data, external weather/solar APIs, and AI/ML models to forecast failures and optimize maintenance schedules.

---

## 🚀 Features

- Real-time sensor data ingestion (temperature, humidity, irradiance, wind speed)
- External API integration (OpenWeather, NASA POWER, Tomorrow.io)
- Local PostgreSQL + TimescaleDB storage for time-series data
- Preprocessing scripts for normalization, cleaning, and interpolation
- Cross-platform: Raspberry Pi 4, macOS, Windows, Linux

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) | Complete navigation guide |
| [ORGANIZATION.md](ORGANIZATION.md) | Repository structure & layout |
| [LIVE_MONITOR_QUICK_REF.md](LIVE_MONITOR_QUICK_REF.md) | Quick reference guide |
| [NEXT_SCOPE_2026.md](NEXT_SCOPE_2026.md) | Future roadmap |
| `docs/` | Detailed technical documentation |
| `archive/` | Historical reports and older documentation |

---

## 🛠️ Quick Start

### 1. Setup Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or: .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Configure Database

Create `.env` file with your database credentials:
```
DB_HOST=localhost
DB_NAME=energy_forecast
DB_USER=your_user
DB_PASSWORD=your_password
DB_PORT=5432
```

### 3. Run Components

```bash
# Start dashboard
./scripts/start_dashboard.sh

# Run ingestion pipeline
python db/db_ingest.py

# Start live monitor simulator
./monitoring/start_sim_dashboard.sh
```

---

## 📁 Project Structure

```
AI-EnergyForcastR4/
├── db/                    # Database layer & ingestion
├── sensors/               # Sensor data collection
├── api_wrappers/          # External API integrations
├── preprocessing/         # Data cleaning & normalization
├── dashboards/            # Visualization
├── monitoring/            # Live monitoring & simulation
├── scripts/               # Automation & utilities
├── data/                  # Data files
├── logs/                  # Application logs
├── docs/                  # Technical documentation
├── tests/                 # Test scripts
├── notebooks/             # Demo notebooks
└── archive/               # Historical reports
```

See [ORGANIZATION.md](ORGANIZATION.md) for complete directory guide.

---

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| Database | PostgreSQL + TimescaleDB |
| Data Processing | Pandas, NumPy, Scikit-learn |
| APIs | OpenWeather, NASA POWER, Tomorrow.io |
| Visualization | Plotly, Matplotlib |
| ML/AI | PyTorch, Scikit-learn |
| IoT | MQTT (paho-mqtt) |
| Deployment | Docker, Raspberry Pi 4 |

---

## 📝 Key Files

- `requirements.txt` - Python dependencies
- `.env` - Configuration file (create locally)
- `db/schema.sql` - Database schema
- `scripts/` - Automation and utility scripts
- `monitoring/` - Live monitoring dashboard

---

## 🤝 Workflow

1. **Data Collection** → Sensors feed data to database
2. **Preprocessing** → Data cleaning and normalization
3. **Ingestion** → APIs and sensors populate TimescaleDB
4. **Analysis** → Dashboards visualize real-time and historical data
5. **Prediction** → ML models forecast failures
6. **Monitoring** → Live alerts and maintenance scheduling

---

## 📚 Archive

Historical documentation and old phase reports are stored in `archive/`:
- `archive/phase-reports/` - Completed phase reports
- `archive/documentation-backups/` - Backup documentation

---

For more information, start with [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md).
