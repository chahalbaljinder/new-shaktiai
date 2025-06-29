"""
Quick Database Setup Script for SHAKTI-AI
Run this to quickly set up PostgreSQL for the wishes vault.
"""

import os
import sys
import subprocess

def install_postgresql_windows():
    """Guide for PostgreSQL installation on Windows."""
    print("\n🛠️  POSTGRESQL SETUP FOR SHAKTI-AI")
    print("=" * 50)
    
    print("\n1. INSTALL POSTGRESQL:")
    print("   - Download from: https://www.postgresql.org/download/windows/")
    print("   - Install with default settings")
    print("   - Remember the password for 'postgres' user")
    
    print("\n2. CREATE DATABASE:")
    print("   Open Command Prompt as Administrator and run:")
    print("   createdb -U postgres shakti_ai_db")
    
    print("\n3. CONFIGURE ENVIRONMENT:")
    env_content = """# SHAKTI-AI Database Configuration
DB_HOST=localhost
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=your_actual_password_here
DB_PORT=5432"""
    
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print(f"   Created .env file at: {env_file}")
    print("   ⚠️  EDIT .env file with your actual PostgreSQL password!")
    
    print("\n4. TEST CONNECTION:")
    print("   Run: python test_db_connection.py")
    
    print("\n✅ Setup complete! Now update your .env file with the correct password.")

def create_test_script():
    """Create a simple database connection test script."""
    test_script = '''"""
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
    print(f"✅ SUCCESS! Connected to: {version}")
    print("🎉 Your database is ready for SHAKTI-AI!")
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("💡 Check your .env file and ensure PostgreSQL is running")
'''
    
    with open('test_db_connection.py', 'w') as f:
        f.write(test_script)
    
    print("Created test_db_connection.py")

if __name__ == "__main__":
    install_postgresql_windows()
    create_test_script()
