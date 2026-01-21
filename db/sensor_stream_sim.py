import time
from datetime import datetime
import random
import sys
import argparse

# File where simulated sensor data will be appended
log_file = "data/sensor_logs.txt"

# ============================================
# CONFIGURATION
# ============================================
INTERVAL_SEC = 2        # Interval between readings (seconds)
MAX_ROWS = 20           # Maximum rows to generate before stopping
ROW_COUNTER = 0         # Track rows generated in this session

# ============================================
# ARGUMENT PARSING
# ============================================
parser = argparse.ArgumentParser(description="Sensor data stream simulator")
parser.add_argument(
    "--continuous",
    action="store_true",
    help="Run continuously (default: stop after MAX_ROWS)"
)
parser.add_argument(
    "--interval",
    type=int,
    default=INTERVAL_SEC,
    help=f"Interval between readings in seconds (default: {INTERVAL_SEC})"
)
parser.add_argument(
    "--max-rows",
    type=int,
    default=MAX_ROWS,
    help=f"Maximum rows to generate before stopping (default: {MAX_ROWS})"
)

args = parser.parse_args()
INTERVAL_SEC = args.interval
MAX_ROWS = args.max_rows

print(f"\n🌦️ Sensor Simulator Started")
print(f"   Interval: {INTERVAL_SEC} sec")
print(f"   Max Rows: {MAX_ROWS}")
print(f"   Mode: {'Continuous' if args.continuous else 'Finite'}")
print(f"   Output: {log_file}\n")

# ============================================
# SIMULATION LOOP
# ============================================
try:
    while True:
        # Generate fake sensor values
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature = round(random.uniform(20, 30), 2)   # Celsius
        humidity = round(random.uniform(40, 70), 2)      # %
        irradiance = round(random.uniform(200, 800), 2)  # W/m²
        wind_speed = round(random.uniform(0, 10), 2)     # m/s

        # Format row
        row = f"{timestamp},{temperature},{humidity},{irradiance},{wind_speed}\n"

        # Append to log file
        with open(log_file, "a") as f:
            f.write(row)

        ROW_COUNTER += 1
        print(f"[{ROW_COUNTER:02d}/{MAX_ROWS}] {timestamp} | T:{temperature:.1f}°C H:{humidity:.1f}% I:{irradiance:.0f}W/m² W:{wind_speed:.1f}m/s")

        # Check if we've reached max rows
        if not args.continuous and ROW_COUNTER >= MAX_ROWS:
            print(f"\n✅ Simulation Complete: Generated {ROW_COUNTER} rows\n")
            break

        # Wait before next reading
        time.sleep(INTERVAL_SEC)

except KeyboardInterrupt:
    print(f"\n⏹️  Simulation Stopped by User: Generated {ROW_COUNTER} rows\n")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error: {e}\n")
    sys.exit(1)
