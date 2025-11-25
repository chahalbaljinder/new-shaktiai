"""
Fix feedback table constraint to allow 'complaint' type
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'shakti_ai_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT', '5432'),
        cursor_factory=RealDictCursor
    )

def fix_feedback_constraint():
    """Update feedback table to allow complaint type and urgent priority"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Dropping old type constraint...")
        cursor.execute("ALTER TABLE feedback DROP CONSTRAINT IF EXISTS feedback_type_check;")
        
        print("Adding new type constraint with 'complaint'...")
        cursor.execute("""
            ALTER TABLE feedback 
            ADD CONSTRAINT feedback_type_check 
            CHECK (type IN ('feedback', 'grievance', 'suggestion', 'complaint'));
        """)
        
        print("Dropping old priority constraint...")
        cursor.execute("ALTER TABLE feedback DROP CONSTRAINT IF EXISTS feedback_priority_check;")
        
        print("Adding new priority constraint with 'urgent'...")
        cursor.execute("""
            ALTER TABLE feedback 
            ADD CONSTRAINT feedback_priority_check 
            CHECK (priority IN ('low', 'medium', 'high', 'urgent', 'critical'));
        """)
        
        conn.commit()
        print("✅ Successfully updated feedback table constraints!")
        print("   Allowed types: feedback, grievance, suggestion, complaint")
        print("   Allowed priorities: low, medium, high, urgent, critical")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_feedback_constraint()
