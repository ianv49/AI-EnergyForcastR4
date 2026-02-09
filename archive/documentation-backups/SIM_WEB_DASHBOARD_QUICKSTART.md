# 🔴 Simulation Web Dashboard - Quick Start

## ⚡ What This Is

A **local HTML dashboard** for simulation testing ONLY (not for live web sensor data).

Features:
- ▶️ **Start Simulator** button - Starts 20-row, 2-second generation
- ⏹️ **Stop Simulator** button - Kills the background process
- 🗑️ **Clear Data** button - Resets database
- 📊 **Real-time charts** - Temperature, Humidity, Irradiance, Wind Speed
- 📋 **Live data table** - All 20 rows as they generate
- 📈 **Progress bar** - Shows simulation progress

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies

```bash
pip install flask flask-cors psycopg2-binary python-dotenv
```

### 2️⃣ Start the Server

```bash
python3 sim_web_dashboard.py
```

Output:
```
🚀 Simulation Web Dashboard
📍 Open http://localhost:5000 in your browser
⚙️  Backend running on http://0.0.0.0:5000
```

### 3️⃣ Open in Browser

Open your browser and go to:
```
http://localhost:5000
```

---

## 🎮 How to Use

### Start Simulation
1. Click **▶️ Start Simulator** button
2. Status changes to 🟢 **ACTIVE**
3. Charts and table start filling with data
4. Every 2 seconds = 1 new row (20 rows total ≈ 40 seconds)

### Stop Simulation
1. Click **⏹️ Stop Simulator** button
2. Background process terminates immediately
3. Status changes to ⚫ **STOPPED**
4. Data stays in database (can review)

### Clear Data
1. Click **🗑️ Clear Data** button
2. Confirm deletion
3. Database is wiped, ready for fresh simulation

---

## 📊 Dashboard Views

### Status Section
- **Status Badge**: Shows 🟢 ACTIVE or ⚫ INACTIVE
- **Record Count**: How many rows generated (0-20)
- **Simulation Time**: How long simulator has been running
- **Latest Values**: Temperature & Humidity from newest row
- **Progress Bar**: Visual 0%-100% completion

### Charts (4 Real-Time Graphs)
- 🌡️ **Temperature Trend** - Shows all temps generated
- 💧 **Humidity Trend** - Shows all humidity values
- ☀️ **Irradiance Trend** - Shows solar irradiance
- 💨 **Wind Speed Trend** - Shows wind speeds

### Data Table
- Latest 20 rows from database
- Sortable columns (timestamp, temperature, humidity, irradiance, wind_speed)
- Shows exact values with 2 decimal precision

---

## 📁 Files

| File | Purpose |
|------|---------|
| `sim_web_dashboard.py` | Flask backend (API + process control) |
| `sim_dashboard.html` | Frontend (charts, table, buttons) |

---

## 🔌 API Endpoints

The Flask backend provides these REST endpoints:

```
GET  http://localhost:5000/api/status     → Get sim status + row count
GET  http://localhost:5000/api/data       → Get latest 20 rows
POST http://localhost:5000/api/start-sim  → Start simulator
POST http://localhost:5000/api/stop-sim   → Stop simulator
POST http://localhost:5000/api/clear-data → Delete all rows from DB
```

---

## ⚙️ Configuration

The backend uses `.env` for database connection:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=energy_db
DB_USER=postgres
DB_PASSWORD=password
```

Default values in code if `.env` not found.

---

## 🎯 Use Cases

✅ **Testing**: Verify simulator generates correct data format
✅ **Development**: See real-time data flow during development  
✅ **Debugging**: Check database writes are working
✅ **Demo**: Show simulation to team/stakeholders

❌ **NOT FOR**: Live web sensor data collection (use Streamlit dashboard instead)

---

## 🛑 Stopping the Server

Press **Ctrl+C** in terminal to stop Flask server.

⚠️ Make sure to click **⏹️ Stop Simulator** first to kill background process!

---

## 📝 Notes

- **Simulator requires**: `db/sensor_stream_sim.py` (must exist)
- **Database required**: PostgreSQL with `sensor_data` table
- **Port 5000**: Make sure it's not in use
- **Auto-refresh**: Dashboard updates every 1 second
- **20 rows**: Simulator stops automatically at 20 rows

---

## ✅ Success Indicators

✅ Buttons are clickable
✅ Status badge changes color when sim active
✅ Charts show data points appearing in real-time
✅ Table fills with new rows as simulation progresses
✅ Progress bar fills to 100%
✅ Stop button kills background process

---

**Status**: ✅ Ready for Testing

Start Flask server → Open browser → Click "Start Simulator" → Watch real-time data! 🚀

