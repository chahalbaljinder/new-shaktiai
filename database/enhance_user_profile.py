"""
Enhance User Profile with Comprehensive Employee Data
This script adds extensive organizational employee management fields to the users table.
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

def enhance_user_table():
    """Add comprehensive employee profile fields to users table."""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("ENHANCING USER TABLE FOR COMPREHENSIVE EMPLOYEE PROFILES")
        print("=" * 60)
        
        # Personal Information
        print("\n📋 Adding Personal Information fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS date_of_birth DATE,
            ADD COLUMN IF NOT EXISTS gender VARCHAR(20),
            ADD COLUMN IF NOT EXISTS blood_group VARCHAR(10),
            ADD COLUMN IF NOT EXISTS marital_status VARCHAR(20),
            ADD COLUMN IF NOT EXISTS nationality VARCHAR(50) DEFAULT 'Indian',
            ADD COLUMN IF NOT EXISTS aadhar_number VARCHAR(20) UNIQUE,
            ADD COLUMN IF NOT EXISTS pan_number VARCHAR(20) UNIQUE;
        """)
        print("✅ Personal information fields added")
        
        # Contact Information
        print("\n📞 Adding Contact Information fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS alternate_email VARCHAR(255),
            ADD COLUMN IF NOT EXISTS mobile_number VARCHAR(20),
            ADD COLUMN IF NOT EXISTS emergency_contact_name VARCHAR(255),
            ADD COLUMN IF NOT EXISTS emergency_contact_number VARCHAR(20),
            ADD COLUMN IF NOT EXISTS emergency_contact_relation VARCHAR(50),
            ADD COLUMN IF NOT EXISTS current_address TEXT,
            ADD COLUMN IF NOT EXISTS permanent_address TEXT,
            ADD COLUMN IF NOT EXISTS city VARCHAR(100),
            ADD COLUMN IF NOT EXISTS state VARCHAR(100),
            ADD COLUMN IF NOT EXISTS pincode VARCHAR(10);
        """)
        print("✅ Contact information fields added")
        
        # Employment Details
        print("\n💼 Adding Employment Details fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS employee_id VARCHAR(50) UNIQUE,
            ADD COLUMN IF NOT EXISTS department VARCHAR(100),
            ADD COLUMN IF NOT EXISTS division VARCHAR(100),
            ADD COLUMN IF NOT EXISTS section VARCHAR(100),
            ADD COLUMN IF NOT EXISTS reporting_manager_id INTEGER REFERENCES users(id),
            ADD COLUMN IF NOT EXISTS joining_date DATE,
            ADD COLUMN IF NOT EXISTS employment_type VARCHAR(50) DEFAULT 'Permanent',
            ADD COLUMN IF NOT EXISTS grade_level VARCHAR(20),
            ADD COLUMN IF NOT EXISTS salary_band VARCHAR(20),
            ADD COLUMN IF NOT EXISTS work_location VARCHAR(100),
            ADD COLUMN IF NOT EXISTS office_room VARCHAR(50),
            ADD COLUMN IF NOT EXISTS extension_number VARCHAR(20);
        """)
        print("✅ Employment details fields added")
        
        # Educational Qualifications
        print("\n🎓 Adding Educational Qualifications fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS highest_qualification VARCHAR(100),
            ADD COLUMN IF NOT EXISTS specialization VARCHAR(100),
            ADD COLUMN IF NOT EXISTS university VARCHAR(200),
            ADD COLUMN IF NOT EXISTS year_of_passing INTEGER,
            ADD COLUMN IF NOT EXISTS additional_qualifications JSONB DEFAULT '[]'::jsonb;
        """)
        print("✅ Educational qualifications fields added")
        
        # Skills & Expertise
        print("\n💡 Adding Skills & Expertise fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS technical_skills JSONB DEFAULT '[]'::jsonb,
            ADD COLUMN IF NOT EXISTS certifications JSONB DEFAULT '[]'::jsonb,
            ADD COLUMN IF NOT EXISTS languages_known JSONB DEFAULT '[]'::jsonb,
            ADD COLUMN IF NOT EXISTS areas_of_expertise JSONB DEFAULT '[]'::jsonb,
            ADD COLUMN IF NOT EXISTS years_of_experience DECIMAL(4,1) DEFAULT 0,
            ADD COLUMN IF NOT EXISTS previous_organizations JSONB DEFAULT '[]'::jsonb;
        """)
        print("✅ Skills & expertise fields added")
        
        # Security & Access
        print("\n🔐 Adding Security & Access fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS security_clearance_level VARCHAR(50),
            ADD COLUMN IF NOT EXISTS security_clearance_expiry DATE,
            ADD COLUMN IF NOT EXISTS access_card_number VARCHAR(50),
            ADD COLUMN IF NOT EXISTS biometric_id VARCHAR(100),
            ADD COLUMN IF NOT EXISTS two_factor_enabled BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS last_password_change TIMESTAMP,
            ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS account_locked_until TIMESTAMP;
        """)
        print("✅ Security & access fields added")
        
        # Bank & Financial Details
        print("\n💰 Adding Bank & Financial Details fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS bank_name VARCHAR(100),
            ADD COLUMN IF NOT EXISTS bank_account_number VARCHAR(50),
            ADD COLUMN IF NOT EXISTS ifsc_code VARCHAR(20),
            ADD COLUMN IF NOT EXISTS bank_branch VARCHAR(100),
            ADD COLUMN IF NOT EXISTS pf_number VARCHAR(50),
            ADD COLUMN IF NOT EXISTS esi_number VARCHAR(50),
            ADD COLUMN IF NOT EXISTS uan_number VARCHAR(50);
        """)
        print("✅ Bank & financial details fields added")
        
        # Leave & Attendance
        print("\n📅 Adding Leave & Attendance fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS annual_leave_balance DECIMAL(5,1) DEFAULT 0,
            ADD COLUMN IF NOT EXISTS sick_leave_balance DECIMAL(5,1) DEFAULT 0,
            ADD COLUMN IF NOT EXISTS casual_leave_balance DECIMAL(5,1) DEFAULT 0,
            ADD COLUMN IF NOT EXISTS total_leaves_taken DECIMAL(5,1) DEFAULT 0,
            ADD COLUMN IF NOT EXISTS attendance_percentage DECIMAL(5,2) DEFAULT 100.00,
            ADD COLUMN IF NOT EXISTS shift_timings VARCHAR(50) DEFAULT '09:00 AM - 06:00 PM';
        """)
        print("✅ Leave & attendance fields added")
        
        # Performance & Training
        print("\n📊 Adding Performance & Training fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS last_performance_rating VARCHAR(20),
            ADD COLUMN IF NOT EXISTS last_appraisal_date DATE,
            ADD COLUMN IF NOT EXISTS next_appraisal_date DATE,
            ADD COLUMN IF NOT EXISTS trainings_completed JSONB DEFAULT '[]'::jsonb,
            ADD COLUMN IF NOT EXISTS trainings_pending JSONB DEFAULT '[]'::jsonb,
            ADD COLUMN IF NOT EXISTS awards_received JSONB DEFAULT '[]'::jsonb;
        """)
        print("✅ Performance & training fields added")
        
        # System Preferences
        print("\n⚙️ Adding System Preferences fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS notification_preferences JSONB DEFAULT '{
                "expertResponses": true,
                "wishReminders": true,
                "weeklyCheckins": true,
                "communityUpdates": false,
                "emergencyAlerts": true,
                "voiceConfirmations": true,
                "email": true,
                "sms": false,
                "push": true
            }'::jsonb,
            ADD COLUMN IF NOT EXISTS privacy_settings JSONB DEFAULT '{
                "showProfile": true,
                "showEmail": false,
                "showPhone": false,
                "allowMessaging": true,
                "dataRetention": "1-year"
            }'::jsonb,
            ADD COLUMN IF NOT EXISTS appearance_settings JSONB DEFAULT '{
                "theme": "light",
                "language": "en",
                "fontSize": "medium",
                "colorScheme": "blue"
            }'::jsonb;
        """)
        print("✅ System preferences fields added")
        
        # Documents & Files
        print("\n📄 Adding Documents & Files fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS resume_url TEXT,
            ADD COLUMN IF NOT EXISTS photo_url TEXT,
            ADD COLUMN IF NOT EXISTS id_proof_url TEXT,
            ADD COLUMN IF NOT EXISTS address_proof_url TEXT,
            ADD COLUMN IF NOT EXISTS education_certificates JSONB DEFAULT '[]'::jsonb,
            ADD COLUMN IF NOT EXISTS other_documents JSONB DEFAULT '[]'::jsonb;
        """)
        print("✅ Documents & files fields added")
        
        # Metadata
        print("\n🏷️ Adding Metadata fields...")
        cursor.execute("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ADD COLUMN IF NOT EXISTS updated_by INTEGER REFERENCES users(id),
            ADD COLUMN IF NOT EXISTS profile_completion_percentage INTEGER DEFAULT 0,
            ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT false,
            ADD COLUMN IF NOT EXISTS verification_date TIMESTAMP,
            ADD COLUMN IF NOT EXISTS notes TEXT;
        """)
        print("✅ Metadata fields added")
        
        # Create indexes for performance
        print("\n🔍 Creating indexes...")
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_employee_id ON users(employee_id);
            CREATE INDEX IF NOT EXISTS idx_users_department ON users(department);
            CREATE INDEX IF NOT EXISTS idx_users_establishment ON users(establishment);
            CREATE INDEX IF NOT EXISTS idx_users_reporting_manager ON users(reporting_manager_id);
            CREATE INDEX IF NOT EXISTS idx_users_joining_date ON users(joining_date);
            CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
        """)
        print("✅ Indexes created")
        
        # Update existing users with default values
        print("\n🔄 Updating existing users with default values...")
        cursor.execute("""
            UPDATE users 
            SET 
                employee_id = 'EMP' || LPAD(id::text, 6, '0'),
                department = COALESCE(department, 'General'),
                employment_type = COALESCE(employment_type, 'Permanent'),
                work_location = COALESCE(establishment, 'Delhi HQ'),
                joining_date = COALESCE(joining_date, created_at::date),
                profile_completion_percentage = 30
            WHERE employee_id IS NULL;
        """)
        print("✅ Existing users updated")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ USER TABLE ENHANCEMENT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        # Display summary
        cursor.execute("""
            SELECT 
                column_name, 
                data_type, 
                is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'users' 
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print(f"\n📊 Total columns in users table: {len(columns)}")
        print("\nNew fields added for comprehensive employee management:")
        print("  • Personal Information (7 fields)")
        print("  • Contact Information (10 fields)")
        print("  • Employment Details (12 fields)")
        print("  • Educational Qualifications (5 fields)")
        print("  • Skills & Expertise (6 fields)")
        print("  • Security & Access (8 fields)")
        print("  • Bank & Financial Details (7 fields)")
        print("  • Leave & Attendance (6 fields)")
        print("  • Performance & Training (6 fields)")
        print("  • System Preferences (3 JSONB fields)")
        print("  • Documents & Files (6 fields)")
        print("  • Metadata (6 fields)")
        print("\n✨ Users table is now ready for comprehensive employee management!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    enhance_user_table()
