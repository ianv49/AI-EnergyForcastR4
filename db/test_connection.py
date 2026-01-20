from db_connector import get_connection

def main():
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            # Count rows
            cur.execute("SELECT COUNT(*) FROM sensor_data;")
            result = cur.fetchone()
            print("✅ Database connection test successful!")
            print(f"📊 sensor_data table has {result[0]} rows.")

            # Show first 3 rows
            cur.execute("SELECT * FROM sensor_data ORDER BY timestamp ASC LIMIT 3;")
            rows = cur.fetchall()
            print("\n🔎 Preview of first 3 rows:")
            for row in rows:
                print(row)

    except Exception as e:
        print(f"❌ Query failed: {e}")

    conn.close()

if __name__ == "__main__":
    main()
