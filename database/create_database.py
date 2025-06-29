"""
Create SHAKTI-AI Database
This script creates the PostgreSQL database for SHAKTI-AI wishes vault.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()

def create_database():
    """Create the SHAKTI-AI database."""
    
    # Connect to PostgreSQL server (not to a specific database)
    try:
        # Connection parameters without database name
        conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        print("Connecting to PostgreSQL server...")
        conn = psycopg2.connect(**conn_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        db_name = os.getenv('DB_NAME', 'shakti_ai_db')
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ Database '{db_name}' already exists!")
        else:
            # Create database
            print(f"Creating database '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Database '{db_name}' created successfully!")
        
        cursor.close()
        conn.close()
        
        # Now test connection to the new database
        print("\nTesting connection to the new database...")
        test_connection()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Common solutions:")
        print("   1. Check if PostgreSQL is running")
        print("   2. Verify your password in .env file")
        print("   3. Ensure PostgreSQL is installed")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_connection():
    """Test connection to the SHAKTI-AI database."""
    try:
        conn_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'shakti_ai_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD'),
            'port': os.getenv('DB_PORT', '5432')
        }
        
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ SUCCESS! Connected to: {version}")
        print("🎉 Your database is ready for SHAKTI-AI!")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    print("🛠️  SHAKTI-AI Database Creator")
    print("=" * 40)
    
    if create_database():
        print("\n🎉 Database setup complete!")
        print("Next step: Run 'streamlit run app.py' to start SHAKTI-AI")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your PostgreSQL installation and .env configuration")
