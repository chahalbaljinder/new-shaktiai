"""
Direct Database Test for SHAKTI-AI
Test the database connection without Streamlit session state issues.
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from cryptography.fernet import Fernet

# Database configuration (hardcoded for testing)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'shakti_ai_db',
    'user': 'postgres',
    'password': '8810',
    'port': '5432'
}

def test_direct_connection():
    """Test direct database connection."""
    print("🔍 Testing direct database connection...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✅ Direct connection successful!")
        print(f"   PostgreSQL: {version}")
        return True
    except Exception as e:
        print(f"❌ Direct connection failed: {e}")
        return False

def test_table_creation():
    """Test creating the wishes tables."""
    print("\n🛠️  Testing table creation...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create wishes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wishes (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                encrypted_content BYTEA NOT NULL,
                contact_name VARCHAR(255),
                contact_email VARCHAR(255),
                contact_phone VARCHAR(20),
                contact_relationship VARCHAR(100),
                sharing_preferences JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
        """)
        
        # Create sharing_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sharing_history (
                id SERIAL PRIMARY KEY,
                wish_id INTEGER REFERENCES wishes(id),
                shared_with VARCHAR(255) NOT NULL,
                sharing_method VARCHAR(50) NOT NULL,
                shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'sent',
                notes TEXT
            );
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def test_wish_operations():
    """Test basic wish operations."""
    print("\n📝 Testing wish operations...")
    
    try:
        # Generate encryption key
        key = Fernet.generate_key()
        fernet = Fernet(key)
        
        # Test data
        user_id = "test_user_123"
        wish_content = "This is a test wish for PostgreSQL integration"
        encrypted_content = fernet.encrypt(wish_content.encode())
        
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Insert test wish
        cursor.execute("""
            INSERT INTO wishes (user_id, encrypted_content, contact_name, contact_email)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (user_id, encrypted_content, "Test Contact", "test@example.com"))
        
        wish_id = cursor.fetchone()[0]
        print(f"✅ Wish created with ID: {wish_id}")
        
        # Read back the wish
        cursor.execute("""
            SELECT id, encrypted_content, contact_name, contact_email, created_at
            FROM wishes 
            WHERE user_id = %s AND is_active = TRUE;
        """, (user_id,))
        
        wish = cursor.fetchone()
        if wish:
            decrypted_content = fernet.decrypt(wish[1]).decode()
            print(f"✅ Wish retrieved: {decrypted_content}")
            print(f"   Contact: {wish[2]} ({wish[3]})")
        
        # Clean up test data
        cursor.execute("DELETE FROM wishes WHERE user_id = %s;", (user_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        print("✅ All wish operations successful!")
        return True
        
    except Exception as e:
        print(f"❌ Wish operations failed: {e}")
        return False

def main():
    print("🧪 SHAKTI-AI Database Integration Test")
    print("=" * 45)
    
    success = True
    
    if not test_direct_connection():
        success = False
    
    if success and not test_table_creation():
        success = False
    
    if success and not test_wish_operations():
        success = False
    
    if success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ PostgreSQL integration is working correctly!")
        print("✅ Database connection is stable")
        print("✅ Tables are created properly")
        print("✅ Wish operations work as expected")
        print("\n🚀 You can now run: streamlit run app.py")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("Please check the error messages above.")

if __name__ == "__main__":
    main()
