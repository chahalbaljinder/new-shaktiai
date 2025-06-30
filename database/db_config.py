"""
PostgreSQL Database Configuration for SHAKTI-AI Wishes Vault
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
from cryptography.fernet import Fernet
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'shakti_ai_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'port': os.getenv('DB_PORT', '5432')
}

class WishesDatabase:
    def __init__(self):
        self.encryption_key = self._get_or_create_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        
    def _get_or_create_encryption_key(self):
        """Get or create encryption key for wishes."""
        key_file = os.path.join(os.path.dirname(__file__), 'db_wishes.key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        return key
    
    def _encrypt_data(self, data):
        """Encrypt sensitive data."""
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data)
    
    def _decrypt_data(self, encrypted_data):
        """Decrypt sensitive data."""
        if encrypted_data is None:
            return None
        try:
            if isinstance(encrypted_data, memoryview):
                encrypted_data = bytes(encrypted_data)
            return self.fernet.decrypt(encrypted_data).decode()
        except Exception:
            return None
    
    def get_connection(self):
        """Get database connection."""
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except Exception as e:
            if hasattr(st, 'error'):
                st.error(f"Database connection failed: {e}")
            else:
                print(f"Database connection failed: {e}")
            return None
    
    def init_database(self):
        """Initialize database tables."""
        try:
            conn = self.get_connection()
            if not conn:
                return False
                
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
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_wishes_user_id ON wishes(user_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_wishes_created_at ON wishes(created_at);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sharing_history_wish_id ON sharing_history(wish_id);")
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"Database initialization failed: {e}")
            return False
    
    def save_wish(self, user_id, content, contact_name=None, contact_email=None, 
                  contact_phone=None, contact_relationship=None, sharing_preferences=None):
        """Save a wish to the database."""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            encrypted_content = self._encrypt_data(content)
            
            cursor.execute("""
                INSERT INTO wishes (user_id, encrypted_content, contact_name, contact_email, 
                                  contact_phone, contact_relationship, sharing_preferences)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (user_id, encrypted_content, contact_name, contact_email, 
                  contact_phone, contact_relationship, json.dumps(sharing_preferences) if sharing_preferences else None))
            
            wish_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return wish_id
            
        except Exception as e:
            st.error(f"Failed to save wish: {e}")
            return False
    
    def get_wishes(self, user_id, limit=10):
        """Get wishes for a user."""
        try:
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT id, encrypted_content, contact_name, contact_email, contact_phone,
                       contact_relationship, sharing_preferences, created_at, updated_at
                FROM wishes 
                WHERE user_id = %s AND is_active = TRUE
                ORDER BY created_at DESC
                LIMIT %s;
            """, (user_id, limit))
            
            wishes = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # Decrypt content
            for wish in wishes:
                wish['content'] = self._decrypt_data(wish['encrypted_content'])
                # Handle sharing_preferences JSON properly
                if wish['sharing_preferences']:
                    if isinstance(wish['sharing_preferences'], str):
                        wish['sharing_preferences'] = json.loads(wish['sharing_preferences'])
                    elif isinstance(wish['sharing_preferences'], dict):
                        # Already a dict, keep as is
                        pass
                    else:
                        wish['sharing_preferences'] = {}
                else:
                    wish['sharing_preferences'] = {}
                del wish['encrypted_content']  # Remove encrypted data from response
            
            return wishes
            
        except Exception as e:
            st.error(f"Failed to get wishes: {e}")
            return []
    
    def update_wish(self, wish_id, user_id, content=None, contact_name=None, 
                   contact_email=None, contact_phone=None, contact_relationship=None,
                   sharing_preferences=None):
        """Update a wish."""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Build dynamic update query
            update_fields = []
            update_values = []
            
            if content is not None:
                update_fields.append("encrypted_content = %s")
                update_values.append(self._encrypt_data(content))
            
            if contact_name is not None:
                update_fields.append("contact_name = %s")
                update_values.append(contact_name)
            
            if contact_email is not None:
                update_fields.append("contact_email = %s")
                update_values.append(contact_email)
            
            if contact_phone is not None:
                update_fields.append("contact_phone = %s")
                update_values.append(contact_phone)
            
            if contact_relationship is not None:
                update_fields.append("contact_relationship = %s")
                update_values.append(contact_relationship)
            
            if sharing_preferences is not None:
                update_fields.append("sharing_preferences = %s")
                update_values.append(json.dumps(sharing_preferences))
            
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            update_values.extend([wish_id, user_id])
            
            query = f"""
                UPDATE wishes 
                SET {', '.join(update_fields)}
                WHERE id = %s AND user_id = %s;
            """
            
            cursor.execute(query, update_values)
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            return rows_affected > 0
            
        except Exception as e:
            st.error(f"Failed to update wish: {e}")
            return False
    
    def delete_wish(self, wish_id, user_id):
        """Soft delete a wish."""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE wishes 
                SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND user_id = %s;
            """, (wish_id, user_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            cursor.close()
            conn.close()
            
            return rows_affected > 0
            
        except Exception as e:
            st.error(f"Failed to delete wish: {e}")
            return False
    
    def log_sharing(self, wish_id, shared_with, sharing_method, status='sent', notes=None):
        """Log sharing activity."""
        try:
            conn = self.get_connection()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sharing_history (wish_id, shared_with, sharing_method, status, notes)
                VALUES (%s, %s, %s, %s, %s);
            """, (wish_id, shared_with, sharing_method, status, notes))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            st.error(f"Failed to log sharing: {e}")
            return False
    
    def get_sharing_history(self, user_id, limit=20):
        """Get sharing history for a user."""
        try:
            conn = self.get_connection()
            if not conn:
                return []
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT sh.*, w.contact_name, w.created_at as wish_created_at
                FROM sharing_history sh
                JOIN wishes w ON sh.wish_id = w.id
                WHERE w.user_id = %s
                ORDER BY sh.shared_at DESC
                LIMIT %s;
            """, (user_id, limit))
            
            history = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return history
            
        except Exception as e:
            st.error(f"Failed to get sharing history: {e}")
            return []

# Global database instance
wishes_db = WishesDatabase()
