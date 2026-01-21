# 🗺️ NEXT SCOPE - AI Energy Forecast R4

**Generated:** January 21, 2026  
**Decision Point:** Fix Phase 8.7 OR Move to Phase 9  
**Timeline:** Q1 2026

---

## 🎯 IMMEDIATE DECISION

### Option A: Complete Phase 8.7 Web Dashboard (RECOMMENDED)
**Timeline:** 2-3 hours  
**Priority:** HIGH  
**Impact:** Completes current feature

### Option B: Jump to Phase 9 Predictive Analytics
**Timeline:** 40-60 hours  
**Priority:** MEDIUM  
**Impact:** Adds major new capability

---

## 📋 OPTION A: FIX WEB DASHBOARD DATA PIPELINE

### Task 1: Debug Database Query (1 hour)

**Objective:** Verify data is actually in the database

```bash
# Step 1: Connect to database
psql -h localhost -U postgres -d energy_db

# Step 2: Check table structure
\d sensor_data

# Step 3: Count rows
SELECT COUNT(*) FROM sensor_data;

# Step 4: Show sample data
SELECT * FROM sensor_data LIMIT 5;

# Step 5: Show column names
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'sensor_data';
```

**Expected outcomes:**
- ✅ Table exists with correct schema
- ✅ Data is being inserted by simulator
- ✅ Column names match API expectations
- ✅ Data types are correct (floats not strings)

---

### Task 2: Fix API Endpoint (1 hour)

**File:** [sim_web_dashboard.py](sim_web_dashboard.py#L50-L70)  
**Function:** `get_latest_data()`

**Current code:**
```python
def get_latest_data():
    cur.execute("""
        SELECT timestamp, temperature, humidity, irradiance, wind_speed
        FROM sensor_data
        ORDER BY timestamp DESC
        LIMIT 20
    """)
```

**Issues to check:**
1. Do column names match database? (Maybe `temp` instead of `temperature`)
2. Are NULL values causing conversion errors?
3. Is timestamp format incompatible?
4. Are float conversions failing?

**Solution approach:**
```python
# Add debug logging
print("Query result:", rows)
print("Data count:", len(rows))
print("First row:", rows[0] if rows else "No data")

# Handle NULL/missing values
data.append({
    "timestamp": row[0].isoformat() if row[0] else None,
    "temperature": float(row[1]) if row[1] is not None else 0,  # Add NULL handling
    "humidity": float(row[2]) if row[2] is not None else 0,
    "irradiance": float(row[3]) if row[3] is not None else 0,
    "wind_speed": float(row[4]) if row[4] is not None else 0
})
```

---

### Task 3: Verify Frontend Receives Data (0.5 hour)

**File:** [sim_dashboard.html](sim_dashboard.html)  
**Function:** `updateDashboard()`

**Debug steps:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Start simulator
4. Look for `/api/data` requests
5. Check Response tab - should show array of objects

**What to verify:**
```javascript
// Before updating charts, log the data
const data = result.data || [];
console.log("Data received:", data);  // Should show array of 20+ objects
console.log("Data count:", data.length);  // Should show > 0

if (data.length === 0) {
    console.error("❌ No data received! Check API.");
    return;  // Don't try to render empty charts
}
```

---

### Task 4: Test End-to-End (0.5 hour)

**Complete workflow:**
1. Clear database: Click "🗑️ Clear Data"
2. Start simulator: Click "▶️ Start Simulator"
3. Wait 5 seconds
4. Check database: `SELECT COUNT(*) FROM sensor_data;`
5. Check API response: Open `http://localhost:8000/api/data` in browser
6. Verify charts show data: Look at dashboard

---

## ✅ SUCCESS CRITERIA - Phase 8.7

| Criteria | Status |
|----------|--------|
| Charts display data | ❌ → ✅ |
| Table shows 20 rows | ❌ → ✅ |
| Progress bar fills | ❌ → ✅ |
| Metrics display values | ❌ → ✅ |
| Real-time updates every 1 sec | ❌ → ✅ |
| All 4 buttons functional | ✅ → ✅ |

---

## 🤖 OPTION B: PHASE 9 PREDICTIVE ANALYTICS

### High-Level Overview

**Goal:** Add machine learning for energy forecasting

### Phase 9.1: Data Preparation (10 hours)

**Deliverables:**
- ✨ Feature engineering
- 📊 Train/test split (80/20)
- 🔢 Normalization & scaling
- ⏰ Time series features (hour, day, season)

**Output:** `features/engineered_data.csv`

---

### Phase 9.2: Model Development (20 hours)

**Model 1: ARIMA** (Time Series)
```python
# Auto-regressive model for univariate forecasting
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(train_data, order=(1,1,1))
forecast = model.forecast(steps=24)  # 24-hour ahead
```

**Model 2: Prophet** (Seasonality)
```python
# Facebook Prophet - handles seasonality well
from prophet import Prophet

model = Prophet()
model.fit(df[['ds', 'y']])
future = model.make_future_dataframe(periods=24)
forecast = model.predict(future)
```

**Model 3: LSTM** (Deep Learning)
```python
# Neural network for complex patterns
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential([
    LSTM(50, activation='relu', input_shape=(lookback, n_features)),
    Dense(25, activation='relu'),
    Dense(1)
])
```

**Model 4: XGBoost** (Ensemble)
```python
# Gradient boosting for accuracy
from xgboost import XGBRegressor

model = XGBRegressor(n_estimators=100, max_depth=5)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

**Output:** 4 trained models saved as `.pkl` files

---

### Phase 9.3: Evaluation & Selection (5 hours)

**Metrics:**
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score

**Comparison table:**
```
Model      MAE    RMSE   MAPE   R²
-----------------------------------
ARIMA      15.2   18.5   12%    0.87
Prophet    14.8   17.2   11%    0.89  ← Best
LSTM       13.5   16.1   10%    0.91  ← Tied
XGBoost    13.2   15.8   9.5%   0.92  ✨ Winner
```

**Selection:** XGBoost (best RMSE + speed)

---

### Phase 9.4: Dashboard Integration (15 hours)

**New Dashboard Views:**

#### 🔮 Forecast View
```
Next 24 Hours Prediction
┌──────────────────────────────────┐
│ 📈 Chart showing predicted values │
│ with confidence intervals (±15%)  │
│                                   │
│ Time | Forecast | Confidence      │
│ 21:00|  45.2°C  | 43.1-47.3       │
│ 22:00|  44.8°C  | 42.3-47.1       │
│ ...  |   ...    | ...             │
└──────────────────────────────────┘
```

#### ⚠️ Anomaly Detection View
```
Unusual Patterns Detected
┌──────────────────────────────────┐
│ 🔴 3 anomalies found              │
│ - Spike at 18:45 (↑25%)          │
│ - Drop at 22:30 (↓18%)           │
│ - Sustained high at 23:00        │
└──────────────────────────────────┘
```

#### 📊 Model Performance View
```
Model Accuracy Dashboard
┌──────────────────────────────────┐
│ XGBoost Model                      │
│ Accuracy: 92%                      │
│ Precision: 0.94                    │
│ Recall: 0.90                       │
│ Last trained: 2026-01-21 15:00    │
└──────────────────────────────────┘
```

---

### Phase 9.5: API Endpoints (10 hours)

**New Flask endpoints:**

```python
# Get 24-hour forecast
GET /api/forecast/24h
Response: {
    "forecasts": [
        {"time": "21:00", "temperature": 45.2, "confidence": 0.92},
        ...
    ],
    "model": "XGBoost",
    "accuracy": 0.92
}

# Get anomalies
GET /api/anomalies
Response: {
    "anomalies": [
        {"timestamp": "2026-01-21 18:45", "type": "spike", "severity": "high"},
        ...
    ],
    "count": 3
}

# Train new model
POST /api/train-model
Body: {"model_type": "XGBoost"}
Response: {"status": "training", "job_id": "abc123"}

# Get model metrics
GET /api/model-metrics
Response: {
    "mae": 13.2,
    "rmse": 15.8,
    "mape": 9.5,
    "r2": 0.92
}
```

---

## 📅 PHASE ROADMAP

```
Current: Phase 8.7 (Paused - Web Dashboard Data Issue)
   ↓
Decision Point (Next meeting)
   ↓
├─ Path A: Fix Phase 8.7 (2-3 hrs) → Complete ✅
│    ↓
│    Phase 9: Predictive Analytics (40-60 hrs)
│    ├─ 9.1: Data prep (10 hrs)
│    ├─ 9.2: Model dev (20 hrs)
│    ├─ 9.3: Evaluation (5 hrs)
│    ├─ 9.4: Dashboard (15 hrs)
│    └─ 9.5: API (10 hrs)
│
└─ Path B: Skip Phase 8.7, Jump to Phase 9
     (Same timeline as above)
```

---

## 💰 EFFORT ESTIMATES

| Task | Hours | Difficulty |
|------|-------|-----------|
| **Option A (Fix Web Dashboard)** | 2-3 | Easy |
| **Option B Phase 9.1 (Data prep)** | 10 | Medium |
| **Option B Phase 9.2 (Models)** | 20 | Hard |
| **Option B Phase 9.3 (Evaluation)** | 5 | Medium |
| **Option B Phase 9.4 (Dashboard)** | 15 | Medium |
| **Option B Phase 9.5 (API)** | 10 | Medium |
| **TOTAL Phase 9** | 60 | Hard |

---

## 🎁 PHASE 10-11 PREVIEW

### Phase 10: Deployment & Scaling
- Docker containerization
- Kubernetes orchestration
- Cloud deployment (AWS/GCP/Azure)
- CI/CD pipeline
- Performance optimization

### Phase 11: Advanced Integration
- Real-time API consumption
- Webhook notifications
- Mobile app support
- Historical data archive
- Export/reporting features

---

## 📊 SUCCESS METRICS

### Phase 8.7 Success
- ✅ Charts display data
- ✅ Tables render
- ✅ Real-time updates work
- ✅ All buttons functional

### Phase 9 Success
- ✅ Forecast accuracy > 90%
- ✅ Anomalies detected < 5% false positive
- ✅ Models train in < 2 minutes
- ✅ Dashboard shows predictions
- ✅ API responds < 500ms

---

## ⚡ RECOMMENDATION

**IMMEDIATE NEXT STEP:** Option A

**Rationale:**
1. **Low effort** (2-3 hours)
2. **High impact** (completes feature)
3. **Unblocks Phase 9** (clean data pipeline)
4. **Good demo/presentation** (working web dashboard)
5. **Builds confidence** (another completed feature)

**Then:** Phase 9 for major capability

---

## 🗣️ DECISION NEEDED

**Questions for stakeholder:**

1. ❓ Should we complete web dashboard first?
2. ❓ Or skip it and go straight to forecasting?
3. ❓ Timeline preference: quick wins vs big features?
4. ❓ Which phases have highest business value?

---

**Status:** Ready for direction  
**Estimated completion (Option A):** January 22, 2026  
**Estimated completion (Option B):** February 28, 2026

