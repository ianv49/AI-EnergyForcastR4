import logging
import csv
from datetime import datetime
from tabulate import tabulate
from db_connector import get_connection   # Import connection function

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def insert_sensor_data(conn, timestamp, temperature, humidity, irradiance, wind_speed):
    """Insert one row into sensor_data table, strip microseconds, skip duplicates."""
    try:
        ts = datetime.fromisoformat(timestamp).replace(microsecond=0)
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sensor_data (timestamp, temperature, humidity, irradiance, wind_speed)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (timestamp) DO NOTHING;
                """,
                (ts, temperature, humidity, irradiance, wind_speed)
            )
        conn.commit()
    except Exception as e:
        logging.error(f"Insert failed: {e}")

def ingest_text_file(conn, filepath="data/sensor_logs.txt"):
    """Read plain text log file and insert rows."""
    try:
        with open(filepath, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    timestamp, temperature, humidity, irradiance, wind_speed = parts
                    insert_sensor_data(conn, timestamp, float(temperature), float(humidity), float(irradiance), float(wind_speed))
        logging.info("Text file ingestion complete.")
    except FileNotFoundError:
        logging.warning(f"{filepath} not found.")
    except Exception as e:
        logging.error(f"Error ingesting text file: {e}")

def ingest_csv_file(conn, filepath="data/sensor_data.csv"):
    """Read CSV file and insert rows."""
    try:
        with open(filepath, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                insert_sensor_data(
                    conn,
                    row["timestamp"],
                    float(row["temperature"]),
                    float(row["humidity"]),
                    float(row["irradiance"]),
                    float(row["wind_speed"])
                )
        logging.info("CSV ingestion complete.")
    except FileNotFoundError:
        logging.warning(f"{filepath} not found.")
    except Exception as e:
        logging.error(f"Error ingesting CSV file: {e}")

def fetch_and_display(conn, limit=10):
    """Display latest rows in a pretty table."""
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT %s;", (limit,))
            rows = cur.fetchall()
            headers = [desc[0] for desc in cur.description]
            print(tabulate(rows, headers=headers, tablefmt="psql"))
    except Exception as e:
        logging.error(f"Error fetching rows: {e}")

if __name__ == "__main__":
    conn = get_connection()
    ingest_text_file(conn, "data/sensor_logs.txt")
    ingest_csv_file(conn, "data/sensor_data.csv")
    fetch_and_display(conn, limit=10)
    conn.close()
