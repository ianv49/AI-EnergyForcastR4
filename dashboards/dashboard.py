import streamlit as st
import psycopg2
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dotenv import load_dotenv
import subprocess
import threading
import time

# Load environment variables
load_dotenv()

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Energy Sensor Dashboard",
    page_icon="🌞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONNECT TO DATABASE
# ============================================
@st.cache_resource
def get_connection():
    """Create database connection (cached)"""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "energy_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", ""),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432")
    )

# ============================================
# FETCH DATA
# ============================================
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_sensor_data(limit=500):
    """Load sensor data from database"""
    try:
        conn = get_connection()
        df = pd.read_sql(
            "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT %s;",
            conn,
            params=(limit,)
        )
        conn.close()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sort by timestamp ascending for charts
        df = df.sort_values('timestamp')
        
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

# ============================================
# TITLE & DESCRIPTION
# ============================================
st.title("🌞 Energy Sensor Dashboard")
st.markdown("Real-time monitoring of renewable energy assets")

# ============================================
# SIDEBAR - CONTROLS & SIMULATION
# ============================================
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # ============================================
    # SIMULATION CONTROLS
    # ============================================
    st.subheader("🌦️ Simulation Control")
    
    # Initialize session state for simulation
    if "sim_active" not in st.session_state:
        st.session_state.sim_active = False
    if "sim_process" not in st.session_state:
        st.session_state.sim_process = None
    
    # Simulation status display
    if st.session_state.sim_active:
        st.success("🟢 Simulator is ACTIVE", icon="✅")
    else:
        st.info("⚫ Simulator is INACTIVE", icon="ℹ️")
    
    # Simulation parameters
    col1, col2 = st.columns(2)
    with col1:
        sim_interval = st.number_input("Interval (sec):", min_value=1, max_value=60, value=2, step=1)
    with col2:
        sim_rows = st.number_input("Max Rows:", min_value=1, max_value=100, value=20, step=1)
    
    # Start simulator button
    if st.button("▶️ Start Simulator", use_container_width=True, key="start_sim"):
        try:
            # Run simulator in background
            cmd = [
                "python3",
                "-u",
                "db/sensor_stream_sim.py",
                "--interval", str(sim_interval),
                "--max-rows", str(sim_rows)
            ]
            st.session_state.sim_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            st.session_state.sim_active = True
            st.success(f"✅ Simulator started! ({sim_rows} rows @ {sim_interval}s intervals)")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to start simulator: {e}")
    
    # Stop simulator button
    if st.session_state.sim_active and st.session_state.sim_process:
        if st.button("⏹️ Stop Simulator", use_container_width=True, key="stop_sim"):
            try:
                st.session_state.sim_process.terminate()
                st.session_state.sim_process.wait(timeout=2)
                st.session_state.sim_active = False
                st.info("⏹️ Simulator stopped")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error stopping simulator: {e}")
    
    # Check if simulator process has finished
    if st.session_state.sim_active and st.session_state.sim_process:
        if st.session_state.sim_process.poll() is not None:
            st.session_state.sim_active = False
            st.success("✅ Simulator finished (20 rows generated)")
            st.rerun()
    
    st.divider()
    
    # Data range selector
    st.subheader("Data Range")
    rows_to_show = st.slider("Number of rows to display:", 10, 500, 100)
    
    # Page selection
    st.subheader("Navigation")
    if st.session_state.sim_active:
        page = st.radio(
            "Choose view:",
            ["🔴 Live Monitor", "📊 Overview", "📈 Charts", "📋 Raw Data", "📊 Statistics"]
        )
    else:
        page = st.radio(
            "Choose view:",
            ["📊 Overview", "📈 Charts", "📋 Raw Data", "📊 Statistics"]
        )

# ============================================
# LOAD DATA
# ============================================
# DURING SIMULATION: All views show LIVE data (no cache)
# This ensures Overview, Charts, Raw Data, Statistics all show 20 sim rows
if st.session_state.sim_active:
    # Fetch fresh data from DB (bypasses cache)
    # Applies to ALL views during simulation
    try:
        conn = get_connection()
        df = pd.read_sql(
            "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT %s;",
            conn,
            params=(500,)
        )
        conn.close()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
    except Exception as e:
        st.error(f"Database error: {e}")
        df = pd.DataFrame()
    
    # Auto-refresh every 1 second - all views update in real-time
    time.sleep(0.5)
    st.rerun()
else:
    # When simulator is OFF, use cache for performance
    df = load_sensor_data(rows_to_show)

if df.empty:
    st.warning("No data available. Please run ingestion first.")
    st.stop()

# ============================================
# PAGE: LIVE MONITOR (Real-Time Simulation Data)
# ============================================
if page == "🔴 Live Monitor":
    st.subheader("🔴 LIVE Simulation Monitor")
    st.markdown("*Updating every second - showing newest generated rows*")
    
    if not st.session_state.sim_active:
        st.warning("⚫ Simulator is not active. Start simulator from sidebar to begin monitoring.")
        st.stop()
    
    # Display latest rows being generated
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Rows Generated", len(df))
    
    with col2:
        if len(df) > 0:
            st.metric("⏱️ Latest", df['timestamp'].iloc[-1].strftime('%H:%M:%S'))
        else:
            st.metric("⏱️ Latest", "Waiting...")
    
    with col3:
        st.metric("🎯 Target", "20 rows")
    
    st.divider()
    
    # Real-time table of newly generated rows
    st.markdown("### 📋 Live Data Table (Latest First)")
    if not df.empty:
        display_df = df.sort_values('timestamp', ascending=False).head(20).copy()
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(
            display_df,
            use_container_width=True,
            height=400
        )
    else:
        st.info("Waiting for first data point...")
    
    st.divider()
    
    # Live updating chart - all 4 metrics
    st.markdown("### 📈 Live Charts (Updating in Real-Time)")
    
    if len(df) > 0:
        col1, col2 = st.columns(2)
        
        # Temperature & Humidity
        with col1:
            fig_temp = px.line(
                df,
                x="timestamp",
                y="temperature",
                title="🌡️ Temperature (Live)",
                markers=True,
                color_discrete_sequence=["#FF6B6B"]
            )
            fig_temp.update_layout(height=350, hovermode="x unified")
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            fig_humid = px.line(
                df,
                x="timestamp",
                y="humidity",
                title="💧 Humidity (Live)",
                markers=True,
                color_discrete_sequence=["#4ECDC4"]
            )
            fig_humid.update_layout(height=350, hovermode="x unified")
            st.plotly_chart(fig_humid, use_container_width=True)
        
        col3, col4 = st.columns(2)
        
        # Irradiance & Wind Speed
        with col3:
            fig_irrad = px.line(
                df,
                x="timestamp",
                y="irradiance",
                title="☀️ Irradiance (Live)",
                markers=True,
                color_discrete_sequence=["#FFD93D"]
            )
            fig_irrad.update_layout(height=350, hovermode="x unified")
            st.plotly_chart(fig_irrad, use_container_width=True)
        
        with col4:
            fig_wind = px.line(
                df,
                x="timestamp",
                y="wind_speed",
                title="💨 Wind Speed (Live)",
                markers=True,
                color_discrete_sequence=["#95E1D3"]
            )
            fig_wind.update_layout(height=350, hovermode="x unified")
            st.plotly_chart(fig_wind, use_container_width=True)
        
        # Multi-metric normalized overlay
        st.divider()
        st.markdown("### 📊 All Metrics Overlay (Normalized)")
        
        df_norm = df.copy()
        temp_range = df['temperature'].max() - df['temperature'].min()
        irrad_range = df['irradiance'].max() - df['irradiance'].min()
        wind_range = df['wind_speed'].max() - df['wind_speed'].min()
        
        df_norm['temp_norm'] = (df['temperature'] - df['temperature'].min()) / (temp_range + 0.001) * 100 if temp_range > 0 else 50
        df_norm['humid_norm'] = df['humidity']
        df_norm['irrad_norm'] = (df['irradiance'] - df['irradiance'].min()) / (irrad_range + 0.001) * 100 if irrad_range > 0 else 50
        df_norm['wind_norm'] = (df['wind_speed'] - df['wind_speed'].min()) / (wind_range + 0.001) * 100 if wind_range > 0 else 50
        
        fig_all = go.Figure()
        fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['temp_norm'], name='Temperature', line=dict(color='#FF6B6B'), mode='lines+markers'))
        fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['humid_norm'], name='Humidity', line=dict(color='#4ECDC4'), mode='lines+markers'))
        fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['irrad_norm'], name='Irradiance', line=dict(color='#FFD93D'), mode='lines+markers'))
        fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['wind_norm'], name='Wind Speed', line=dict(color='#95E1D3'), mode='lines+markers'))
        
        fig_all.update_layout(title="All Metrics Comparison (Normalized)", hovermode="x unified", height=400)
        st.plotly_chart(fig_all, use_container_width=True)
        
        st.info("ℹ️ Charts update every second while simulator is active. You'll see new rows appear as data is generated!")
    else:
        st.info("Waiting for data from simulator...")

# ============================================
# PAGE: OVERVIEW
# ============================================
elif page == "📊 Overview":
    st.subheader("Dashboard Overview")
    
    # Show simulation status
    if st.session_state.sim_active:
        st.success("🟢 LIVE SIMULATION ACTIVE - Data updates every 1 second", icon="✅")
    
    # Latest readings
    col1, col2, col3, col4 = st.columns(4)
    
    latest = df.iloc[-1] if len(df) > 0 else {}
    
    with col1:
        st.metric(
            "🌡️ Temperature",
            f"{latest.get('temperature', 'N/A'):.1f}°C",
            delta=f"{latest.get('temperature', 0) - df['temperature'].mean():.1f}°C",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "💧 Humidity",
            f"{latest.get('humidity', 'N/A'):.1f}%",
            delta=f"{latest.get('humidity', 0) - df['humidity'].mean():.1f}%",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "☀️ Irradiance",
            f"{latest.get('irradiance', 'N/A'):.1f} W/m²",
            delta=f"{latest.get('irradiance', 0) - df['irradiance'].mean():.1f} W/m²"
        )
    
    with col4:
        st.metric(
            "💨 Wind Speed",
            f"{latest.get('wind_speed', 'N/A'):.1f} m/s",
            delta=f"{latest.get('wind_speed', 0) - df['wind_speed'].mean():.1f} m/s"
        )
    
    st.divider()
    
    # Quick stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"📈 Total Records: {len(df)}")
    
    with col2:
        time_range = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600
        st.info(f"⏱️ Time Range: {time_range:.1f} hours")

# ============================================
# PAGE: CHARTS
# ============================================
elif page == "📈 Charts":
    st.subheader("Sensor Readings Over Time")
    
    # Show simulation status
    if st.session_state.sim_active:
        st.success("🟢 LIVE SIMULATION ACTIVE - Charts update every 1 second", icon="✅")
    
    # Temperature Chart
    st.markdown("### 🌡️ Temperature Trend")
    fig_temp = px.line(
        df,
        x="timestamp",
        y="temperature",
        title="Temperature (°C)",
        markers=True,
        color_discrete_sequence=["#FF6B6B"]
    )
    fig_temp.update_layout(hovermode="x unified", height=350)
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Humidity Chart
    st.markdown("### 💧 Humidity Trend")
    fig_humid = px.line(
        df,
        x="timestamp",
        y="humidity",
        title="Humidity (%)",
        markers=True,
        color_discrete_sequence=["#4ECDC4"]
    )
    fig_humid.update_layout(hovermode="x unified", height=350)
    st.plotly_chart(fig_humid, use_container_width=True)
    
    # Irradiance Chart
    st.markdown("### ☀️ Solar Irradiance Trend")
    fig_irrad = px.line(
        df,
        x="timestamp",
        y="irradiance",
        title="Irradiance (W/m²)",
        markers=True,
        color_discrete_sequence=["#FFD93D"]
    )
    fig_irrad.update_layout(hovermode="x unified", height=350)
    st.plotly_chart(fig_irrad, use_container_width=True)
    
    # Wind Speed Chart
    st.markdown("### 💨 Wind Speed Trend")
    fig_wind = px.line(
        df,
        x="timestamp",
        y="wind_speed",
        title="Wind Speed (m/s)",
        markers=True,
        color_discrete_sequence=["#95E1D3"]
    )
    fig_wind.update_layout(hovermode="x unified", height=350)
    st.plotly_chart(fig_wind, use_container_width=True)
    
    # Multi-metric overlay
    st.divider()
    st.markdown("### 📊 All Metrics Normalized")
    
    # Normalize data for comparison
    df_norm = df.copy()
    df_norm['temperature_norm'] = (df['temperature'] - df['temperature'].min()) / (df['temperature'].max() - df['temperature'].min()) * 100
    df_norm['humidity_norm'] = df['humidity']
    df_norm['irradiance_norm'] = (df['irradiance'] - df['irradiance'].min()) / (df['irradiance'].max() - df['irradiance'].min()) * 100
    df_norm['wind_speed_norm'] = (df['wind_speed'] - df['wind_speed'].min()) / (df['wind_speed'].max() - df['wind_speed'].min()) * 100
    
    fig_all = go.Figure()
    fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['temperature_norm'], name='Temperature', line=dict(color='#FF6B6B')))
    fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['humidity_norm'], name='Humidity', line=dict(color='#4ECDC4')))
    fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['irradiance_norm'], name='Irradiance', line=dict(color='#FFD93D')))
    fig_all.add_trace(go.Scatter(x=df_norm['timestamp'], y=df_norm['wind_speed_norm'], name='Wind Speed', line=dict(color='#95E1D3')))
    
    fig_all.update_layout(title="All Metrics Comparison (Normalized)", hovermode="x unified", height=400)
    st.plotly_chart(fig_all, use_container_width=True)

# ============================================
# PAGE: RAW DATA
# ============================================
elif page == "📋 Raw Data":
    st.subheader("Raw Sensor Data")
    
    # Show simulation status
    if st.session_state.sim_active:
        st.success("🟢 LIVE SIMULATION ACTIVE - Table updates every 1 second", icon="✅")
    
    # Display table
    st.dataframe(
        df.sort_values('timestamp', ascending=False),
        use_container_width=True,
        height=500
    )
    
    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ============================================
# PAGE: STATISTICS
# ============================================
elif page == "📊 Statistics":
    st.subheader("Statistical Summary")
    
    # Show simulation status
    if st.session_state.sim_active:
        st.success("🟢 LIVE SIMULATION ACTIVE - Statistics update every 1 second", icon="✅")
    
    stats_data = {
        'Metric': ['Temperature (°C)', 'Humidity (%)', 'Irradiance (W/m²)', 'Wind Speed (m/s)'],
        'Min': [
            f"{df['temperature'].min():.2f}",
            f"{df['humidity'].min():.2f}",
            f"{df['irradiance'].min():.2f}",
            f"{df['wind_speed'].min():.2f}"
        ],
        'Max': [
            f"{df['temperature'].max():.2f}",
            f"{df['humidity'].max():.2f}",
            f"{df['irradiance'].max():.2f}",
            f"{df['wind_speed'].max():.2f}"
        ],
        'Mean': [
            f"{df['temperature'].mean():.2f}",
            f"{df['humidity'].mean():.2f}",
            f"{df['irradiance'].mean():.2f}",
            f"{df['wind_speed'].mean():.2f}"
        ],
        'Std Dev': [
            f"{df['temperature'].std():.2f}",
            f"{df['humidity'].std():.2f}",
            f"{df['irradiance'].std():.2f}",
            f"{df['wind_speed'].std():.2f}"
        ]
    }
    
    stats_df = pd.DataFrame(stats_data)
    st.dataframe(stats_df, use_container_width=True)
    
    # Correlation matrix
    st.markdown("### 📊 Correlation Matrix")
    numeric_cols = ['temperature', 'humidity', 'irradiance', 'wind_speed']
    corr_matrix = df[numeric_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale="RdBu",
        zmin=-1,
        zmax=1,
        title="Sensor Parameter Correlations"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption(f"📅 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col2:
    st.caption(f"📊 Records: {len(df)}")

with col3:
    sim_status = "🟢 Active" if st.session_state.get("sim_active", False) else "⚫ Inactive"
    st.caption(f"Sim: {sim_status}")

st.caption("🌞 AI-EnergyForcastR4 | Phase 7+8 Enhanced Dashboard")
