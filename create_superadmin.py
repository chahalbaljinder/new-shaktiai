"""
Create SuperAdmin User
Run this to create/update a superadmin account
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import bcrypt

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

def create_superadmin():
    """Create or update superadmin user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("\n=== SuperAdmin Setup ===\n")
    
    # Get details
    email = input("Enter superadmin email (default: admin@drdo.gov.in): ").strip() or "admin@drdo.gov.in"
    name = input("Enter superadmin name (default: SuperAdmin): ").strip() or "SuperAdmin"
    password = input("Enter password (default: Admin@123): ").strip() or "Admin@123"
    
    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing = cursor.fetchone()
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        if existing:
            print(f"\n✓ User exists with ID {existing['id']}, updating to superadmin...")
            
            cursor.execute("""
                UPDATE users 
                SET 
                    name = %s,
                    password_hash = %s,
                    role = 'superadmin',
                    is_active = TRUE,
                    onboarding_completed = TRUE,
                    onboarding_step = 5,
                    is_first_login = FALSE,
                    must_change_password = FALSE,
                    created_by_admin = FALSE,
                    temp_password = NULL,
                    designation = 'System Administrator',
                    establishment = 'DRDO HQ',
                    updated_at = CURRENT_TIMESTAMP
                WHERE email = %s
                RETURNING id, name, email, employee_id
            """, (name, password_hash.decode('utf-8'), email))
        else:
            print("\n✓ Creating new superadmin user...")
            
            cursor.execute("""
                INSERT INTO users (
                    name, email, password_hash, role, designation, establishment,
                    is_active, onboarding_completed, onboarding_step,
                    is_first_login, must_change_password, created_by_admin
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, name, email, employee_id
            """, (
                name, email, password_hash.decode('utf-8'), 
                'superadmin', 'System Administrator', 'DRDO HQ',
                True, True, 5, False, False, False
            ))
        
        user = cursor.fetchone()
        conn.commit()
        
        print("\n" + "="*60)
        print("✓ SUPERADMIN CREATED SUCCESSFULLY!")
        print("="*60)
        print(f"\nEmployee ID: {user['employee_id']}")
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Password: {password}")
        print(f"Role: superadmin")
        print("\n" + "="*60)
        print("\nYou can now:")
        print("1. Login with these credentials")
        print("2. Access the SuperAdmin Panel")
        print("3. Create employee accounts")
        print("="*60 + "\n")
        
    except Exception as e:
        conn.rollback()
        print(f"\n✗ Error: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_superadmin()
