"""Initialize feedback system tables locally."""
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg2.extras

# Escalation routing matrix
ESCALATION_ROUTES = {
    "transfer": {"department": "Local HR", "cell": "Establishment Section"},
    "leave": {"department": "Local HR", "cell": "Leave Sanctioning Authority"},
    "relocation": {"department": "Local HR", "cell": "Infrastructure/Admin Cell"},
    "harassment": {"department": "Women Grievance Cell", "cell": "Internal Complaints Committee (ICC)"},
    "discrimination": {"department": "Women Welfare Cell", "cell": "HR Department"},
    "promotion": {"department": "Establishment", "cell": "DPC Secretariat"},
    "benefits": {"department": "Benefits Cell", "cell": "HR Processing"},
    "governance": {"department": "Administrative Head", "cell": "RTI Cell (if unresolved)"},
    "safety": {"department": "Safety Officer", "cell": "Lab In-Charge"},
    "other": {"department": "HR Department", "cell": "General Queries"}
}

def initialize_feedback_tables():
    """Create database tables for feedback and complaints system."""
    conn = psycopg2.connect(
        host="localhost",
        database="shakti_ai_db",
        user="postgres",
        password="Anjo@024",
        port="5432"
    )
    cursor = conn.cursor()
    
    try:
        # Annual Feedback Forms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS annual_feedback (
                id SERIAL PRIMARY KEY,
                employee_name VARCHAR(255),
                employee_id VARCHAR(100),
                designation VARCHAR(255),
                lab_center VARCHAR(255),
                email VARCHAR(255),
                years_of_service INTEGER,
                is_anonymous BOOLEAN DEFAULT FALSE,
                
                -- Feedback sections (JSON for flexibility)
                work_environment JSONB,
                leadership_management JSONB,
                inclusion_culture JSONB,
                workload_balance JSONB,
                career_development JSONB,
                safety_conduct JSONB,
                additional_comments TEXT,
                
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'submitted',
                reviewed_by VARCHAR(255),
                review_date TIMESTAMP,
                review_notes TEXT
            );
        """)
        print("✅ Created annual_feedback table")
        
        # Queries & Escalation table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries_escalation (
                id SERIAL PRIMARY KEY,
                employee_name VARCHAR(255) NOT NULL,
                employee_id VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                
                query_type VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
                subject VARCHAR(500) NOT NULL,
                description TEXT NOT NULL,
                supporting_documents JSONB,
                
                routed_to_department VARCHAR(255),
                routed_to_cell VARCHAR(255),
                priority VARCHAR(50) DEFAULT 'normal',
                
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(50) DEFAULT 'submitted',
                assigned_to VARCHAR(255),
                response TEXT,
                response_date TIMESTAMP,
                resolution_date TIMESTAMP,
                
                escalation_level INTEGER DEFAULT 1,
                escalation_history JSONB
            );
        """)
        print("✅ Created queries_escalation table")
        
        # Complaints & Grievances table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints_grievances (
                id SERIAL PRIMARY KEY,
                complaint_number VARCHAR(100) UNIQUE,
                
                -- Complainant info (optional for anonymous)
                is_anonymous BOOLEAN DEFAULT FALSE,
                complainant_name VARCHAR(255),
                employee_id VARCHAR(100),
                designation VARCHAR(255),
                email VARCHAR(255),
                phone VARCHAR(20),
                
                -- Complaint details
                complaint_type VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
                incident_date DATE,
                incident_location VARCHAR(500),
                incident_time VARCHAR(50),
                
                persons_involved TEXT,
                witness_names TEXT,
                detailed_description TEXT NOT NULL,
                previous_attempts TEXT,
                desired_outcome TEXT,
                
                supporting_evidence JSONB,
                urgency VARCHAR(50) DEFAULT 'normal',
                
                -- Routing
                routed_to VARCHAR(255),
                icc_notified BOOLEAN DEFAULT FALSE,
                legal_notified BOOLEAN DEFAULT FALSE,
                
                -- Tracking
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                acknowledgment_sent BOOLEAN DEFAULT FALSE,
                acknowledgment_date TIMESTAMP,
                case_officer VARCHAR(255),
                status VARCHAR(50) DEFAULT 'received',
                
                -- Investigation
                investigation_started TIMESTAMP,
                investigation_notes TEXT,
                hearing_dates JSONB,
                final_report TEXT,
                action_taken TEXT,
                closure_date TIMESTAMP,
                
                -- Confidentiality
                confidentiality_level VARCHAR(50) DEFAULT 'high',
                access_log JSONB
            );
        """)
        print("✅ Created complaints_grievances table")
        
        # Status tracking and notifications
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS status_updates (
                id SERIAL PRIMARY KEY,
                reference_type VARCHAR(50) NOT NULL,
                reference_id INTEGER NOT NULL,
                update_type VARCHAR(100) NOT NULL,
                update_message TEXT NOT NULL,
                updated_by VARCHAR(255),
                update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notification_sent BOOLEAN DEFAULT FALSE
            );
        """)
        print("✅ Created status_updates table")
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_queries_status ON queries_escalation(status);
            CREATE INDEX IF NOT EXISTS idx_queries_employee ON queries_escalation(employee_id);
            CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints_grievances(status);
            CREATE INDEX IF NOT EXISTS idx_complaints_type ON complaints_grievances(complaint_type);
            CREATE INDEX IF NOT EXISTS idx_feedback_date ON annual_feedback(submission_date);
        """)
        print("✅ Created indexes")
        
        conn.commit()
        print("\n✅ Feedback system tables created successfully!")
        print("\n📋 Available tables:")
        print("  - annual_feedback")
        print("  - queries_escalation")
        print("  - complaints_grievances")
        print("  - status_updates")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creating tables: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("Initializing feedback system database tables...\n")
    initialize_feedback_tables()
