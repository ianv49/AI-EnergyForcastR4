import psycopg2

# Database connection settings (adjust to your PostgreSQL setup)
DB_HOST = "localhost"
DB_NAME = "your_database_name"
DB_USER = "your_username"
DB_PASS = "your_password"

def ingest_logs():
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()

    # Open the sensor log file
    with open("sensor_logs.txt", "r") as f:
        for line in f:
            parts = line.strip().split(", ")
            if len(parts) == 5:
                timestamp, temp, hum, irr, wind = parts
                cur.execute(
                    """
                    INSERT INTO sensor_data (timestamp, temperature, humidity, irradiance, wind_speed)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (timestamp, float(temp), float(hum), float(irr), float(wind))
                )

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()
    print("Logs ingested successfully!")

if __name__ == "__main__":
    ingest_logs()
