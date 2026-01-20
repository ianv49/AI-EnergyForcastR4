import os
import sys
import psycopg2
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def get_connection():
    """Create and return a PostgreSQL connection using .env variables."""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "energy_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "PdM"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")
        )
        logger.info("Connected to PostgreSQL successfully.")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        sys.exit(1)

