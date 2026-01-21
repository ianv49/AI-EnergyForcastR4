import time
import random
import os
from datetime import datetime
from pathlib import Path

# Ensure data directory exists
data_dir = Path(__file__).parent.parent / "data"
data_dir.mkdir(exist_ok=True)

# Function to simulate sensor readings
def get_sensor_data():
    return {
        "temperature": round(random.uniform(25, 40), 2),   # °C
        "humidity": round(random.uniform(40, 90), 2),      # %
        "irradiance": round(random.uniform(200, 1200), 2), # W/m^2
        "wind_speed": round(random.uniform(0, 15), 2)      # m/s
    }

if __name__ == "__main__":
    log_file = data_dir / "sensor_logs.txt"
    
    # Write header if file doesn't exist
    if not log_file.exists():
        with open(log_file, "w") as f:
            f.write("timestamp,temperature,humidity,irradiance,wind_speed\n")
    
    # Open and append sensor data
    with open(log_file, "a") as f:
        for i in range(10):  # collect 10 samples
            data = get_sensor_data()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = (
                f"{timestamp},"
                f"{data['temperature']},"
                f"{data['humidity']},"
                f"{data['irradiance']},"
                f"{data['wind_speed']}\n"
            )
            
            # Save to file
            f.write(log_line)
            
            # Show on screen
            print(f"Saved: {log_line.strip()}")
            
            # Wait 5 seconds before next reading
            time.sleep(5)
    
    print(f"✓ Data saved to {log_file}")


