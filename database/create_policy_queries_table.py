"""
Create policy_queries table for APEX RAG system
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_policy_queries_table():
    """Create the policy_queries table."""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'shakti_ai_db'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432')
        )
        cursor = conn.cursor()
        
        print("🔍 Checking if policy_queries table exists...")
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'policy_queries'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("✅ policy_queries table already exists")
            return
        
        print("📝 Creating policy_queries table...")
        
        # Create table
        cursor.execute("""
            CREATE TABLE policy_queries (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                query TEXT NOT NULL,
                category VARCHAR(50) DEFAULT 'general',
                response TEXT,
                status VARCHAR(20) DEFAULT 'pending',
                response_time VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX idx_policy_queries_user_id ON policy_queries(user_id);
            CREATE INDEX idx_policy_queries_created_at ON policy_queries(created_at DESC);
            CREATE INDEX idx_policy_queries_category ON policy_queries(category);
        """)
        
        conn.commit()
        print("✅ policy_queries table created successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    create_policy_queries_table()
