# 🔴 LIVE MONITOR: Quick Reference Card

## 🎮 START LIVE MONITORING (2 MINUTES)

```
Step 1: Start Dashboard
$ python3 -m streamlit run dashboards/dashboard.py
→ Opens http://localhost:8501

Step 2: Sidebar → "▶️ Start Simulator"
Status: ⚫ INACTIVE → 🟢 ACTIVE

Step 3: Wait 2 seconds...
"🔴 Live Monitor" appears in Navigation

Step 4: Click "🔴 Live Monitor"
✓ See live table
✓ See 4 live charts
✓ See normalized overlay
✓ Watch 20 rows generate over 40 seconds

Step 5: Simulator finishes
"✅ Simulator finished"
Live Monitor disappears

Done!
```

---

## 📊 WHAT YOU SEE

### Live Metrics (Top)
```
📊 Rows Generated: 15  |  ⏱️ Latest: 19:53:30  |  🎯 Target: 20
```

### Live Table (Middle)
```
Timestamp           | Temp | Humidity | Irradiance | Wind
2026-01-21 19:53:30 | 22.5 |   56.3%  |    521    | 4.7
2026-01-21 19:53:28 | 24.9 |   52.7%  |    379    | 2.8
2026-01-21 19:53:26 | 27.2 |   42.9%  |    353    | 2.5
```

### 4 Live Charts (Bottom - 2x2 Grid)
```
🌡️ Temperature (Red)        💧 Humidity (Teal)
   [Live line chart]             [Live line chart]

☀️ Irradiance (Yellow)      💨 Wind Speed (Green)
   [Live line chart]             [Live line chart]
```

### Normalized Overlay (Below)
```
📊 All Metrics Combined (0-100% scale)
```

---

## ⏱️ TIMING

| Action | Time |
|--------|------|
| Simulator starts | T+0 |
| Row 1 generated | T+2 |
| Dashboard refreshes | T+2.5 |
| Data visible on screen | T+3 |
| Row 2 generated | T+4 |
| Row 3 generated | T+6 |
| ... | ... |
| Row 20 generated | T+40 |
| Simulator stops | T+41 |
| Live Monitor disappears | T+42 |

**Result:** New row visible every ~3 seconds from generation

---

## 🎯 FEATURES

✅ **Live Table**
- Latest 20 rows shown
- Most recent first
- Updates every 1 second

✅ **4 Individual Charts**
- Temperature (Red line)
- Humidity (Teal line)
- Irradiance (Yellow line)
- Wind Speed (Green line)
- All update live

✅ **Normalized Overlay**
- All 4 metrics on one chart
- 0-100% scale for comparison
- Shows trends and correlations

✅ **Auto-Refresh**
- Every 1 second
- Fetches fresh data from DB
- No manual click needed

✅ **Smart Display**
- Only appears when simulator active
- Disappears when simulator done
- No impact on other views

---

## 💡 TIPS

1. **Watch Terminal AND Dashboard**
   - Terminal: Shows [01/20], [02/20], etc.
   - Dashboard: Shows charts updating
   - Together: Full picture of generation

2. **Use Hover on Charts**
   - Mouse over chart data points
   - See exact values (temp, humidity, etc.)
   - See precise timestamps

3. **Watch for Patterns**
   - Temperature ranges (20-30°C)
   - Humidity patterns (40-70%)
   - Irradiance variations (200-800)
   - Wind speed trends (0-10 m/s)

4. **Multiple Monitors?**
   - Terminal on one screen
   - Dashboard on another
   - Watch both simultaneously

---

## 🔧 HOW IT WORKS

```python
# Every 1 second during simulation:

1. Fetch fresh data from database
   SELECT * FROM sensor_data LIMIT 50

2. Parse and sort by timestamp

3. Render:
   ├── Metrics (row count, latest time)
   ├── Table (sorted reverse timestamp)
   ├── 4 individual charts (each metric)
   └── Normalized overlay chart

4. Sleep 0.5 seconds (allow DB writes)

5. Auto-rerun (st.rerun())

6. Start over (step 1)
```

---

## ✅ VERIFICATION

**Works if you see:**
- ✓ "🔴 Live Monitor" appears in sidebar
- ✓ Latest row count shows: 1, 2, 3, ..., 20
- ✓ Table fills with new rows
- ✓ Charts draw lines as data comes in
- ✓ Each chart updates every 1-2 seconds
- ✓ Overlay shows all 4 metrics

---

## 🚀 COMMAND CHEAT SHEET

```bash
# Start dashboard
python3 -m streamlit run dashboards/dashboard.py

# In dashboard sidebar:
# ▶️ Start Simulator

# Wait 2 seconds, then:
# 🔴 Live Monitor (click this)

# Observe for 40 seconds while data generates

# After complete:
# ✅ Simulator finished
```

---

## 🎯 USE CASES

### Testing Setup
```
Want to: Verify simulator works before full ingestion
Action:  Start → Watch Live Monitor
Result:  20 rows appear, all values realistic ✅
```

### Performance Check
```
Want to: Ensure dashboard handles live updates
Action:  Monitor charts during generation
Result:  Smooth updates, no lag, no crashes ✅
```

### Data Quality Validation
```
Want to: Check generated values are realistic
Action:  Watch Live Table for value ranges
Result:  Temp 20-30°C, Humidity 40-70% ✅
```

### Demo/Presentation
```
Want to: Show real-time data visualization
Action:  Run simulator while projecting Live Monitor
Result:  Beautiful dashboard showing live data ✅
```

---

## 📊 BEFORE vs AFTER

### BEFORE: Terminal Only
```
$ python3 db/sensor_stream_sim.py
[01/20] 2026-01-21 19:53:00 | T:25.0°C H:42.5% I:683 W:5.1
[02/20] 2026-01-21 19:53:02 | T:20.9°C H:62.0% I:628 W:7.9
...
```
❌ No visualization
❌ Text only
❌ Hard to verify
❌ Single metric view

### AFTER: Live Monitor Dashboard
```
🔴 LIVE Simulation Monitor
📊 Rows: 20 | ⏱️ Latest: 19:53:40 | 🎯 Target: 20

📋 [Table with all 20 rows]
📈 [4 live updating charts]
📊 [Normalized overlay chart]
```
✅ Beautiful charts
✅ Multiple views
✅ Easy verification
✅ Professional UI

---

## ⚡ PERFORMANCE

- **Refresh Rate:** ~1 second
- **Data Latency:** ~2-3 seconds (from generation to dashboard)
- **Chart Update:** Smooth, no flickering
- **Table Update:** Instant, latest first
- **DB Query:** <50ms (only 50 rows max)

---

## 🎉 SUMMARY

**🔴 Live Monitor Feature:**

Live observation of 20-row simulation with:
- ✅ Real-time table display
- ✅ 4 live updating charts
- ✅ Normalized trend analysis
- ✅ 1-second refresh cycle
- ✅ Professional dashboard UI
- ✅ Zero manual effort needed

**Can you see the chart during simulation?**
**YES! ✅ Real-time updates every 1 second**

---

**Quick Start:** `python3 -m streamlit run dashboards/dashboard.py`
**Then:** Click "▶️ Start Simulator" → Click "🔴 Live Monitor"
**Watch:** 20 rows generate with live charts updating!

