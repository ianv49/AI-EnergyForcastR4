#!/usr/bin/env python3
"""
Simulation Web Dashboard - Flask Backend
Provides REST API for simulation control and real-time data streaming
"""

import os
import subprocess
import psycopg2
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder=".", static_folder=".")
CORS(app)

# Global state
sim_state = {
    "active": False,
    "process": None,
    "start_time": None,
    "row_count": 0,
    "max_rows": 20
}

# Database connection details
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "energy_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password")
}


def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None


def get_latest_data():
    """Fetch latest sensor data from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cur = conn.cursor()
        cur.execute("""
            SELECT timestamp, temperature, humidity, irradiance, wind_speed
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT 20
        """)
        
        rows = cur.fetchall()
        conn.close()
        
        # Convert to list of dicts
        data = []
        for row in reversed(rows):  # Reverse to get chronological order
            data.append({
                "timestamp": row[0].isoformat() if row[0] else None,
                "temperature": float(row[1]) if row[1] else None,
                "humidity": float(row[2]) if row[2] else None,
                "irradiance": float(row[3]) if row[3] else None,
                "wind_speed": float(row[4]) if row[4] else None
            })
        
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


@app.route("/")
def index():
    """Serve the HTML dashboard"""
    return render_template("sim_dashboard.html")


@app.route("/api/status", methods=["GET"])
def get_status():
    """Get current simulation status"""
    return jsonify({
        "active": sim_state["active"],
        "start_time": sim_state["start_time"],
        "row_count": sim_state["row_count"],
        "max_rows": sim_state["max_rows"],
        "progress_percent": int((sim_state["row_count"] / sim_state["max_rows"] * 100)) if sim_state["max_rows"] > 0 else 0
    })


@app.route("/api/data", methods=["GET"])
def get_data():
    """Get latest sensor data"""
    data = get_latest_data()
    return jsonify({
        "data": data,
        "count": len(data),
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/start-sim", methods=["POST"])
def start_simulation():
    """Start the simulation process"""
    global sim_state
    
    if sim_state["active"]:
        return jsonify({"error": "Simulation already running"}), 400
    
    try:
        # Start simulator process
        script_path = Path(__file__).parent / "db" / "sensor_stream_sim.py"
        
        sim_state["process"] = subprocess.Popen(
            ["python3", str(script_path), "--interval", "2", "--max-rows", "20"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        sim_state["active"] = True
        sim_state["start_time"] = datetime.now().isoformat()
        sim_state["row_count"] = 0
        
        return jsonify({
            "status": "started",
            "message": "Simulation started",
            "timestamp": sim_state["start_time"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/stop-sim", methods=["POST"])
def stop_simulation():
    """Stop the simulation process"""
    global sim_state
    
    if not sim_state["active"]:
        return jsonify({"error": "Simulation not running"}), 400
    
    try:
        # Terminate the process
        if sim_state["process"]:
            sim_state["process"].terminate()
            try:
                sim_state["process"].wait(timeout=5)
            except subprocess.TimeoutExpired:
                sim_state["process"].kill()
        
        sim_state["active"] = False
        
        return jsonify({
            "status": "stopped",
            "message": "Simulation stopped",
            "final_row_count": sim_state["row_count"]
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/kill-all", methods=["POST"])
def kill_all():
    """Force kill all simulation processes and reset state"""
    global sim_state
    
    try:
        # Force kill the current process
        if sim_state["process"]:
            try:
                sim_state["process"].kill()
            except:
                pass
        
        # Kill any lingering sensor_stream_sim processes
        subprocess.run(
            ["pkill", "-9", "-f", "sensor_stream_sim"],
            capture_output=True
        )
        
        # Reset state
        sim_state["active"] = False
        sim_state["process"] = None
        sim_state["start_time"] = None
        sim_state["row_count"] = 0
        
        return jsonify({
            "status": "killed",
            "message": "All simulation processes terminated"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/clear-data", methods=["POST"])
def clear_data():
    """Clear sensor data from database"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        
        cur = conn.cursor()
        cur.execute("DELETE FROM sensor_data")
        conn.commit()
        
        deleted_count = cur.rowcount
        conn.close()
        
        return jsonify({
            "status": "cleared",
            "message": f"Deleted {deleted_count} rows",
            "count": deleted_count
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    PORT = 8000
    print("🚀 Simulation Web Dashboard")
    print(f"📍 Open http://localhost:{PORT} in your browser")
    print(f"⚙️  Backend running on http://0.0.0.0:{PORT}")
    app.run(debug=False, host="0.0.0.0", port=PORT)
