"""
Add onboarding fields to users table
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

def add_onboarding_fields():
    """Add onboarding related fields to users table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Adding onboarding fields to users table...")
        
        # Add onboarding related fields
        onboarding_fields = [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS onboarding_completed BOOLEAN DEFAULT FALSE",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS onboarding_step INTEGER DEFAULT 0",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS onboarding_started_at TIMESTAMP",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS onboarding_completed_at TIMESTAMP",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_first_login BOOLEAN DEFAULT TRUE",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS must_change_password BOOLEAN DEFAULT TRUE",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_by_admin BOOLEAN DEFAULT FALSE",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS temp_password VARCHAR(255)",
        ]
        
        for field_query in onboarding_fields:
            try:
                cursor.execute(field_query)
                print(f"✓ Executed: {field_query[:80]}...")
            except Exception as e:
                print(f"✗ Error: {str(e)}")
        
        conn.commit()
        print("\n✓ Onboarding fields added successfully!")
        
        # Check current state
        cursor.execute("""
            SELECT 
                column_name, 
                data_type, 
                column_default,
                is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            AND column_name IN (
                'onboarding_completed', 'onboarding_step', 
                'is_first_login', 'must_change_password', 
                'created_by_admin'
            )
            ORDER BY column_name
        """)
        
        columns = cursor.fetchall()
        print("\n=== Onboarding Fields in Users Table ===")
        for col in columns:
            print(f"  {col['column_name']}: {col['data_type']} (Default: {col['column_default']})")
        
        # Update existing users to mark them as onboarded
        cursor.execute("""
            UPDATE users 
            SET 
                onboarding_completed = TRUE,
                onboarding_step = 5,
                is_first_login = FALSE,
                must_change_password = FALSE,
                created_by_admin = FALSE
            WHERE id IS NOT NULL
        """)
        updated = cursor.rowcount
        conn.commit()
        print(f"\n✓ Updated {updated} existing users as already onboarded")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error adding onboarding fields: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_onboarding_fields()
    print("\n=== Onboarding setup complete! ===")
