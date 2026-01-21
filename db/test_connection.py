import psycopg2

try:
    conn = psycopg2.connect(
        dbname="energy_db",
        user="ianvallejo",
        password="",
        host="localhost",
        port="5432"
    )
    print("✓ Connected to PostgreSQL successfully!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data LIMIT 5;")
    print("✓ Table query successful!")
    
    conn.close()
    print("✓ Connection closed.")
except Exception as e:
    print(f"✗ Error: {e}")
