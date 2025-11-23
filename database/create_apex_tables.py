"""
Create APEX Database Tables
This script creates all necessary tables for the APEX system.
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        database=os.getenv('DB_NAME', 'shakti_ai_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD'),
        port=os.getenv('DB_PORT', '5432')
    )

def create_tables():
    """Create all APEX system tables."""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Creating APEX database tables...\n")
        
        # 1. Users table
        print("Creating users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                designation VARCHAR(100),
                establishment VARCHAR(100),
                phone VARCHAR(20),
                role VARCHAR(50) DEFAULT 'user',
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                profile_image TEXT
            );
        """)
        print("✅ Users table created")
        
        # 2. Wishes table (existing, ensure it exists)
        print("Creating wishes table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wishes (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                encrypted_data BYTEA,
                category VARCHAR(100),
                priority VARCHAR(50) DEFAULT 'medium',
                is_shared BOOLEAN DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            );
        """)
        print("✅ Wishes table created")
        
        # 3. Sharing history table
        print("Creating sharing_history table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sharing_history (
                id SERIAL PRIMARY KEY,
                wish_id INTEGER REFERENCES wishes(id) ON DELETE CASCADE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                shared_with_email VARCHAR(255) NOT NULL,
                shared_with_name VARCHAR(255),
                shared_via VARCHAR(50) NOT NULL,
                message TEXT,
                shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'sent'
            );
        """)
        print("✅ Sharing history table created")
        
        # 4. Feedback/Grievances table
        print("Creating feedback table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                type VARCHAR(50) NOT NULL CHECK (type IN ('feedback', 'grievance', 'suggestion')),
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                category VARCHAR(100) NOT NULL,
                priority VARCHAR(50) NOT NULL CHECK (priority IN ('low', 'medium', 'high', 'critical')),
                status VARCHAR(50) DEFAULT 'submitted' CHECK (status IN ('submitted', 'under-review', 'in-progress', 'resolved', 'closed')),
                is_anonymous BOOLEAN DEFAULT false,
                assigned_to VARCHAR(100),
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP
            );
        """)
        print("✅ Feedback table created")
        
        # 5. Knowledge base queries table
        print("Creating knowledge_queries table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_queries (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                query_text TEXT NOT NULL,
                response_text TEXT,
                sources TEXT,
                response_time_ms INTEGER,
                category VARCHAR(100),
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'completed'
            );
        """)
        print("✅ Knowledge queries table created")
        
        # 6. AI Agent interactions table
        print("Creating agent_interactions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_interactions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                agent_name VARCHAR(100) NOT NULL,
                message TEXT NOT NULL,
                response TEXT,
                session_id VARCHAR(255),
                response_time_ms INTEGER,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✅ Agent interactions table created")
        
        # 7. System analytics table
        print("Creating system_analytics table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_analytics (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                total_queries INTEGER DEFAULT 0,
                total_feedback INTEGER DEFAULT 0,
                total_grievances INTEGER DEFAULT 0,
                total_suggestions INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0,
                avg_response_time_ms INTEGER DEFAULT 0,
                success_rate DECIMAL(5,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date)
            );
        """)
        print("✅ System analytics table created")
        
        # 8. User sessions table
        print("Creating user_sessions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                session_token VARCHAR(255) UNIQUE NOT NULL,
                ip_address VARCHAR(50),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT true
            );
        """)
        print("✅ User sessions table created")
        
        # 9. Notifications table
        print("Creating notifications table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                type VARCHAR(50) NOT NULL,
                priority VARCHAR(50) DEFAULT 'normal',
                is_read BOOLEAN DEFAULT false,
                action_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP
            );
        """)
        print("✅ Notifications table created")
        
        # 10. Audit log table
        print("Creating audit_log table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                action VARCHAR(100) NOT NULL,
                entity_type VARCHAR(100),
                entity_id INTEGER,
                details JSONB,
                ip_address VARCHAR(50),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("✅ Audit log table created")
        
        # Create indexes for performance
        print("\nCreating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_status ON feedback(status);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_type ON feedback(type);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_knowledge_queries_user_id ON knowledge_queries(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_agent_interactions_user_id ON agent_interactions(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wishes_user_id ON wishes(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON audit_log(user_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_sessions_token ON user_sessions(session_token);")
        print("✅ Indexes created")
        
        # Commit changes
        conn.commit()
        print("\n🎉 All tables created successfully!")
        
        # Display table information
        print("\n📊 Database Schema Summary:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\nTotal tables: {len(tables)}")
        for table in tables:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM information_schema.columns 
                WHERE table_name = '{table[0]}';
            """)
            col_count = cursor.fetchone()[0]
            print(f"  📋 {table[0]}: {col_count} columns")
        
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def insert_sample_data():
    """Insert sample data for testing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("\n📥 Inserting sample data...")
        
        # Insert sample user
        cursor.execute("""
            INSERT INTO users (email, name, password_hash, designation, establishment, role)
            VALUES 
                ('test@drdo.gov.in', 'Dr. Test User', '$2a$10$X...', 'Scientist-E', 'DRDO HQ, Delhi', 'admin'),
                ('user@drdo.gov.in', 'Sample User', '$2a$10$X...', 'Scientist-D', 'DRDL, Hyderabad', 'user')
            ON CONFLICT (email) DO NOTHING
            RETURNING id;
        """)
        
        user_result = cursor.fetchone()
        if user_result:
            user_id = user_result[0]
            print(f"✅ Sample users created (ID: {user_id})")
            
            # Insert sample feedback
            cursor.execute("""
                INSERT INTO feedback (user_id, type, title, description, category, priority, status)
                VALUES 
                    (%s, 'feedback', 'APEX System - Excellent Response Quality', 
                     'The APEX AI agents provide very accurate and helpful responses.', 
                     'System Performance', 'low', 'resolved'),
                    (%s, 'grievance', 'Voice Input Not Working on Secure Workstations', 
                     'Unable to use voice input feature on lab computers.', 
                     'Technical Issue', 'high', 'in-progress'),
                    (%s, 'suggestion', 'Add Support for Regional Languages', 
                     'Request to add Hindi and other regional language support.', 
                     'Feature Request', 'medium', 'under-review');
            """, (user_id, user_id, user_id))
            print("✅ Sample feedback created")
        
        # Insert sample analytics
        cursor.execute("""
            INSERT INTO system_analytics (date, total_queries, total_feedback, total_grievances, 
                                        active_users, avg_response_time_ms, success_rate)
            VALUES 
                (CURRENT_DATE, 342, 15, 8, 127, 2300, 94.3),
                (CURRENT_DATE - INTERVAL '1 day', 298, 12, 6, 2500, 93.1)
            ON CONFLICT (date) DO NOTHING;
        """)
        print("✅ Sample analytics created")
        
        conn.commit()
        print("\n🎉 Sample data inserted successfully!")
        
    except Exception as e:
        print(f"\n⚠️  Sample data insertion skipped or failed: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🛠️  APEX Database Table Creator")
    print("=" * 50)
    
    try:
        create_tables()
        
        # Ask if user wants sample data
        response = input("\n❓ Insert sample data for testing? (y/n): ").lower()
        if response == 'y':
            insert_sample_data()
        
        print("\n✅ Database setup complete!")
        print("📝 Next steps:")
        print("   1. Update your .env file with database credentials")
        print("   2. Run the Next.js frontend: cd shakti-ai-nextjs && npm run dev")
        print("   3. Run the Python backend: python shakti_backend.py")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\n💡 Make sure PostgreSQL is running and credentials are correct in .env")
