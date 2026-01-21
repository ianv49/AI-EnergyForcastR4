#!/usr/bin/env python3
"""
Cross-platform automation script for sensor data ingestion.
Works on Windows, macOS, and Linux.

Usage:
    python3 run_ingest.py          # Run once
    python3 run_ingest.py --daemon # Run continuously (every 5 min)
    python3 run_ingest.py --help   # Show help
"""

import sys
import os
import time
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add db folder to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "db"))

from db_connector import get_connection
from db_ingest import ingest_text_file, ingest_csv_file, count_rows

# Setup logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "ingestion.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def run_ingestion(conn):
    """Run the ingestion pipeline once."""
    try:
        before = count_rows(conn)
        logger.info(f"Starting ingestion. Rows before: {before}")
        
        ingest_text_file(conn, "data/sensor_logs.txt")
        ingest_csv_file(conn, "data/sensor_data.csv")
        
        after = count_rows(conn)
        logger.info(f"Ingestion complete. Rows after: {after}. Added: {after - before}")
        
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Cross-platform sensor data ingestion automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 run_ingest.py              # Run ingestion once
  python3 run_ingest.py --daemon     # Run every 5 minutes (Ctrl+C to stop)
  python3 run_ingest.py --interval 300  # Run every 5 minutes (300 seconds)
        """
    )
    
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="Run continuously every 5 minutes"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Interval in seconds between ingestions (default: 300 = 5 min)"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info(f"Sensor Data Ingestion Tool - {datetime.now()}")
    logger.info(f"Platform: {sys.platform}")
    logger.info("=" * 60)
    
    # Connect to database
    conn = get_connection()
    
    try:
        if args.daemon:
            logger.info(f"Running in daemon mode (interval: {args.interval}s)")
            while True:
                run_ingestion(conn)
                logger.info(f"Next ingestion in {args.interval}s...")
                time.sleep(args.interval)
        else:
            logger.info("Running single ingestion")
            run_ingestion(conn)
            logger.info("Done!")
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user. Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        conn.close()
        logger.info("Database connection closed.")


if __name__ == "__main__":
    main()
