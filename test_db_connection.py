"""
Test PostgreSQL connection for SHAKTI-AI
"""
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'shakti_ai_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PORT', '5432')
}

try:
    print("Testing PostgreSQL connection...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print(f"SUCCESS! Connected to: {version}")
    print("Your database is ready for SHAKTI-AI!")
except Exception as e:
    print(f"ERROR: {e}")
    print("Check your .env file and ensure PostgreSQL is running")
