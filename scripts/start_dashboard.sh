#!/bin/bash
# Phase 7 Dashboard Startup Script

echo "🚀 Starting Energy Sensor Dashboard (Phase 7)"
echo "================================================"
echo ""
echo "Prerequisites:"
echo "  ✓ PostgreSQL running"
echo "  ✓ Database populated with sensor data"
echo "  ✓ Virtual environment activated"
echo ""
echo "Starting Streamlit app..."
echo "📌 Access the dashboard at: http://localhost:8501"
echo ""
echo "Controls:"
echo "  • Click 'Refresh Data' to reload"
echo "  • Use sliders to adjust data range"
echo "  • Navigate between views in sidebar"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo "================================================"
echo ""

source .venv/bin/activate
python3 -m streamlit run dashboards/dashboard.py
