#!/bin/bash

# 🔴 Simulation Web Dashboard - Startup Script
# Starts the Flask backend and opens the browser

set -e

echo "🔴 Simulation Web Dashboard"
echo "================================"
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.7+"
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing required packages..."
    pip install flask flask-cors psycopg2-binary python-dotenv
    echo "✅ Packages installed"
fi

# Check if database is reachable
echo "🔍 Checking database connection..."
python3 -c "
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 5432)),
        database=os.getenv('DB_NAME', 'energy_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password')
    )
    conn.close()
    print('✅ Database connection OK')
except Exception as e:
    print(f'⚠️  Database warning: {e}')
" || true

echo ""
echo "🚀 Starting Flask server..."
echo "📍 Open http://localhost:5000 in your browser"
echo "⏹️  Press Ctrl+C to stop"
echo ""

# Start the Flask server
python3 sim_web_dashboard.py
