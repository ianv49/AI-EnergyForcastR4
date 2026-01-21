# QUICK REFERENCE: Simulation Control System

## 🎯 ONE-MINUTE SETUP

### Via Dashboard:
```
1. Run: python3 -m streamlit run dashboards/dashboard.py
2. Access: http://localhost:8501
3. Left sidebar → "🌦️ Simulation Control"
4. Set interval: 2 sec
5. Set max rows: 20
6. Click "▶️ Start Simulator"
7. Watch it generate 20 rows in ~40 seconds
8. See "✅ Simulator finished" message
9. Click "🔄 Refresh Data" to see new data
```

### Via Terminal:
```bash
# Quick test (5 rows in 10 sec)
python3 db/sensor_stream_sim.py --interval 2 --max-rows 5

# Standard run (20 rows in 40 sec)
python3 db/sensor_stream_sim.py

# Continuous (1 sample/minute forever)
python3 db/sensor_stream_sim.py --interval 60 --continuous

# Stop: Press Ctrl+C
```

---

## 🎮 DASHBOARD CONTROLS

### Location: Left Sidebar → "🌦️ Simulation Control"

#### Status Badge:
- 🟢 **ACTIVE** — Simulator running right now
- ⚫ **INACTIVE** — Simulator stopped or not started

#### Configuration:
```
Interval (sec): [===●===] 2 (range: 1-60)
Max Rows: [====●===] 20 (range: 1-100)
```

#### Buttons:
```
[▶️ Start Simulator]    — Launch with current settings
[⏹️ Stop Simulator]     — Gracefully terminate running sim
```

#### Footer Indicator:
```
Last Update: 2026-01-21 19:48:30 | Records: 28 | Sim: 🟢 Active
```

---

## 📊 DEFAULT SETTINGS

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Interval | 2 seconds | Fast feedback for testing |
| Max Rows | 20 rows | ~40 seconds runtime, manageable |
| Mode | Finite (auto-stop) | Prevents infinite loops |
| Output | `data/sensor_logs.txt` | Ingestion pipeline ready |

---

## 📈 SAMPLE OUTPUT

```
🌦️ Sensor Simulator Started
   Interval: 2 sec
   Max Rows: 5
   Mode: Finite
   Output: data/sensor_logs.txt

[01/5] 2026-01-21 19:48:18 | T:25.0°C H:42.5% I:683W/m² W:5.1m/s
[02/5] 2026-01-21 19:48:20 | T:20.9°C H:62.0% I:628W/m² W:7.9m/s
[03/5] 2026-01-21 19:48:22 | T:20.2°C H:54.1% I:650W/m² W:6.1m/s
[04/5] 2026-01-21 19:48:24 | T:27.2°C H:42.9% I:353W/m² W:2.5m/s
[05/5] 2026-01-21 19:48:26 | T:24.9°C H:52.7% I:379W/m² W:2.8m/s

✅ Simulation Complete: Generated 5 rows
```

---

## 🛠️ COMMON USE CASES

### Use Case 1: Quick Demo (1 minute)
```bash
# Terminal approach
python3 db/sensor_stream_sim.py --interval 1 --max-rows 10

# Dashboard approach
- Set interval: 1 sec, max rows: 10
- Click Start
- Watch 10 rows generate in 10 seconds
```

### Use Case 2: Overnight Test (8 hours)
```bash
# Generate data every 1 minute for 8 hours
# (480 rows = 8 hours × 60 minutes)
python3 db/sensor_stream_sim.py --interval 60 --max-rows 480

# Or continuous
python3 db/sensor_stream_sim.py --interval 60 --continuous
# (manually stop with Ctrl+C)
```

### Use Case 3: Load Testing (Many rows)
```bash
# Generate 1000 rows rapidly
# (with 1-second interval = ~16.7 minutes)
python3 db/sensor_stream_sim.py --interval 1 --max-rows 1000
```

### Use Case 4: Real-time Dashboard Observation
```
1. Start dashboard (terminal 1)
   python3 -m streamlit run dashboards/dashboard.py

2. Start simulator from dashboard
   - Left sidebar → "🌦️ Simulation Control"
   - Click "▶️ Start Simulator"

3. Observe in real-time:
   - Terminal shows generation: [01/20], [02/20], etc.
   - Dashboard updates as data arrives
   - Status badge: 🟢 ACTIVE

4. Auto-completion:
   - After 20 rows, simulator stops
   - See: "✅ Simulator finished"
   - Footer shows new record count
```

---

## 🔧 ADVANCED PARAMETERS

| Flag | Range | Default | Example |
|------|-------|---------|---------|
| `--interval N` | 1-∞ | 2 sec | `--interval 60` (1 min) |
| `--max-rows N` | 1-∞ | 20 | `--max-rows 1000` |
| `--continuous` | Flag | False | `--continuous` (never stop) |

```bash
# Extreme stress test
python3 db/sensor_stream_sim.py --interval 0.1 --max-rows 10000

# Realistic production (5-min intervals, 24-hour data)
python3 db/sensor_stream_sim.py --interval 300 --max-rows 288

# Background monitoring (every 30 seconds)
python3 db/sensor_stream_sim.py --interval 30 --continuous
```

---

## ⚡ PERFORMANCE NOTES

| Scenario | Duration | Row Count | Interval |
|----------|----------|-----------|----------|
| Quick test | ~10 sec | 5 | 2 sec |
| Standard test | ~40 sec | 20 | 2 sec |
| Demo | ~1 min | 30 | 2 sec |
| Hourly data | ~1 hour | 60 | 60 sec |
| Daily data | ~1 day | 1440 | 60 sec |

---

## ❌ TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "file not found" error | Run from repo root: `cd ~/Documents/Clone/AI-EnergyForcastR4` |
| Simulator won't start | Check Python path: `which python3` |
| Dashboard shows "Inactive" | Click "Refresh Data" button |
| Data not appearing | Ingestion may be needed: run `python3 scripts/run_ingest.py` |
| Stuck simulator | Press Ctrl+C (KeyboardInterrupt handler) |

---

## 📝 EXAMPLE WORKFLOW

```bash
# Terminal 1: Start dashboard
$ python3 -m streamlit run dashboards/dashboard.py
# → Opens at http://localhost:8501

# Dashboard UI:
# 1. Left sidebar → "🌦️ Simulation Control"
# 2. Configure: Interval = 2 sec, Max Rows = 20
# 3. Click "▶️ Start Simulator"
# 4. Status changes: ⚫ INACTIVE → 🟢 ACTIVE
# 5. Watch generation in terminal
# 6. After 40 sec, see: "✅ Simulator finished"
# 7. Status: 🟢 ACTIVE → ⚫ INACTIVE
# 8. Main dashboard → Click "🔄 Refresh Data"
# 9. See 20 new rows in all views

# Results:
# ✅ 20 new sensor records generated
# ✅ Data visible in Overview metrics
# ✅ Charts updated with new trend
# ✅ Raw data table shows latest entries
# ✅ Statistics recalculated
```

---

## 📊 INTEGRATION WITH INGESTION PIPELINE

```
Simulator generates data
        ↓
    data/sensor_logs.txt (appended)
        ↓
    run_ingest.py (reads & processes)
        ↓
    PostgreSQL database (sensor_data table)
        ↓
    Dashboard (queries & displays)
        ↓
    Real-time analytics & visualization
```

---

## 🎯 PHASE 8 SUMMARY

✅ **Simulator: Rewritten from scratch**
- Was: Infinite loop, 5-min interval
- Now: Configurable, auto-stop, 2-sec default

✅ **Dashboard: Simulation control panel added**
- Start/stop buttons
- Parameter sliders
- Status indicator
- Process monitoring

✅ **Testing: All features verified working**

---

**Quick Links:**
- 📄 Detailed docs: [docs/PHASE8_SIM_CONTROL.md](PHASE8_SIM_CONTROL.md)
- 📚 Project status: [docs/myNotes.txt](myNotes.txt)
- 🔧 Simulator code: [db/sensor_stream_sim.py](db/sensor_stream_sim.py)
- 🎨 Dashboard code: [dashboards/dashboard.py](dashboards/dashboard.py)

