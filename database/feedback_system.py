"""Database schema and operations for Feedback, Queries & Complaints System.

This module provides manual (non-AI) submission and tracking of:
- Annual employee feedback forms
- Query escalation to appropriate departments
- Complaints and grievances with proper routing
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Create database connection using environment variables."""
    db_host = os.getenv("DB_HOST", "localhost")
    # Override 'db' (Docker) to 'localhost' when running locally
    if db_host == "db":
        db_host = "localhost"
    
    return psycopg2.connect(
        host=db_host,
        database=os.getenv("DB_NAME", "shakti_ai_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", "5432")
    )


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
    conn = get_db_connection()
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
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_queries_status ON queries_escalation(status);
            CREATE INDEX IF NOT EXISTS idx_queries_employee ON queries_escalation(employee_id);
            CREATE INDEX IF NOT EXISTS idx_complaints_status ON complaints_grievances(status);
            CREATE INDEX IF NOT EXISTS idx_complaints_type ON complaints_grievances(complaint_type);
            CREATE INDEX IF NOT EXISTS idx_feedback_date ON annual_feedback(submission_date);
        """)
        
        conn.commit()
        print("✅ Feedback system tables created successfully")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error creating tables: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


def submit_annual_feedback(feedback_data: Dict) -> int:
    """Submit annual employee feedback form."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO annual_feedback (
                employee_name, employee_id, designation, lab_center, email,
                years_of_service, is_anonymous, work_environment,
                leadership_management, inclusion_culture, workload_balance,
                career_development, safety_conduct, additional_comments
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            feedback_data.get('employee_name') if not feedback_data.get('is_anonymous') else 'Anonymous',
            feedback_data.get('employee_id'),
            feedback_data.get('designation'),
            feedback_data.get('lab_center'),
            feedback_data.get('email'),
            feedback_data.get('years_of_service'),
            feedback_data.get('is_anonymous', False),
            psycopg2.extras.Json(feedback_data.get('work_environment', {})),
            psycopg2.extras.Json(feedback_data.get('leadership_management', {})),
            psycopg2.extras.Json(feedback_data.get('inclusion_culture', {})),
            psycopg2.extras.Json(feedback_data.get('workload_balance', {})),
            psycopg2.extras.Json(feedback_data.get('career_development', {})),
            psycopg2.extras.Json(feedback_data.get('safety_conduct', {})),
            feedback_data.get('additional_comments', '')
        ))
        
        feedback_id = cursor.fetchone()[0]
        conn.commit()
        
        # Log status update
        _log_status_update(cursor, conn, 'feedback', feedback_id, 'Submitted', 
                          'Annual feedback form submitted successfully')
        
        return feedback_id
        
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error submitting feedback: {e}")
    finally:
        cursor.close()
        conn.close()


def submit_query(query_data: Dict) -> int:
    """Submit a query for escalation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Determine routing based on category
        category = query_data.get('category', 'other')
        routing = ESCALATION_ROUTES.get(category, ESCALATION_ROUTES['other'])
        
        cursor.execute("""
            INSERT INTO queries_escalation (
                employee_name, employee_id, email, phone, query_type,
                category, subject, description, supporting_documents,
                routed_to_department, routed_to_cell, priority
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            query_data.get('employee_name'),
            query_data.get('employee_id'),
            query_data.get('email'),
            query_data.get('phone'),
            query_data.get('query_type', 'general'),
            category,
            query_data.get('subject'),
            query_data.get('description'),
            psycopg2.extras.Json(query_data.get('supporting_documents', [])),
            routing['department'],
            routing['cell'],
            query_data.get('priority', 'normal')
        ))
        
        query_id = cursor.fetchone()[0]
        conn.commit()
        
        # Log routing
        _log_status_update(cursor, conn, 'query', query_id, 'Routed',
                          f"Query routed to {routing['department']} - {routing['cell']}")
        
        return query_id
        
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error submitting query: {e}")
    finally:
        cursor.close()
        conn.close()


def submit_complaint(complaint_data: Dict) -> str:
    """Submit a complaint or grievance."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Generate complaint number
        complaint_number = f"COMP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Determine routing
        category = complaint_data.get('category', 'other')
        routing = ESCALATION_ROUTES.get(category, ESCALATION_ROUTES['other'])
        
        # Special handling for harassment - notify ICC
        icc_notified = category == 'harassment'
        
        cursor.execute("""
            INSERT INTO complaints_grievances (
                complaint_number, is_anonymous, complainant_name, employee_id,
                designation, email, phone, complaint_type, category,
                incident_date, incident_location, incident_time,
                persons_involved, witness_names, detailed_description,
                previous_attempts, desired_outcome, supporting_evidence,
                urgency, routed_to, icc_notified
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            complaint_number,
            complaint_data.get('is_anonymous', False),
            complaint_data.get('complainant_name') if not complaint_data.get('is_anonymous') else 'Anonymous',
            complaint_data.get('employee_id'),
            complaint_data.get('designation'),
            complaint_data.get('email'),
            complaint_data.get('phone'),
            complaint_data.get('complaint_type', 'grievance'),
            category,
            complaint_data.get('incident_date'),
            complaint_data.get('incident_location'),
            complaint_data.get('incident_time'),
            complaint_data.get('persons_involved'),
            complaint_data.get('witness_names'),
            complaint_data.get('detailed_description'),
            complaint_data.get('previous_attempts'),
            complaint_data.get('desired_outcome'),
            psycopg2.extras.Json(complaint_data.get('supporting_evidence', [])),
            complaint_data.get('urgency', 'normal'),
            routing['cell'],
            icc_notified
        ))
        
        complaint_id = cursor.fetchone()[0]
        conn.commit()
        
        # Log submission
        _log_status_update(cursor, conn, 'complaint', complaint_id, 'Received',
                          f"Complaint {complaint_number} received and routed to {routing['cell']}")
        
        return complaint_number
        
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error submitting complaint: {e}")
    finally:
        cursor.close()
        conn.close()


def get_my_submissions(employee_id: str, submission_type: str = 'all') -> List[Dict]:
    """Retrieve submission history for an employee."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        results = []
        
        if submission_type in ['all', 'feedback']:
            cursor.execute("""
                SELECT id, submission_date, status, is_anonymous
                FROM annual_feedback
                WHERE employee_id = %s
                ORDER BY submission_date DESC;
            """, (employee_id,))
            results.extend([{**row, 'type': 'feedback'} for row in cursor.fetchall()])
        
        if submission_type in ['all', 'query']:
            cursor.execute("""
                SELECT id, submission_date, status, category, subject, routed_to_department
                FROM queries_escalation
                WHERE employee_id = %s
                ORDER BY submission_date DESC;
            """, (employee_id,))
            results.extend([{**row, 'type': 'query'} for row in cursor.fetchall()])
        
        if submission_type in ['all', 'complaint']:
            cursor.execute("""
                SELECT id, complaint_number, submission_date, status, category, is_anonymous
                FROM complaints_grievances
                WHERE employee_id = %s
                ORDER BY submission_date DESC;
            """, (employee_id,))
            results.extend([{**row, 'type': 'complaint'} for row in cursor.fetchall()])
        
        return results
        
    finally:
        cursor.close()
        conn.close()


def get_status_updates(reference_type: str, reference_id: int) -> List[Dict]:
    """Get status update history for a submission."""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT update_type, update_message, updated_by, update_date
            FROM status_updates
            WHERE reference_type = %s AND reference_id = %s
            ORDER BY update_date DESC;
        """, (reference_type, reference_id))
        
        return cursor.fetchall()
        
    finally:
        cursor.close()
        conn.close()


def _log_status_update(cursor, conn, ref_type: str, ref_id: int, 
                       update_type: str, message: str):
    """Internal helper to log status updates."""
    cursor.execute("""
        INSERT INTO status_updates (reference_type, reference_id, update_type, update_message)
        VALUES (%s, %s, %s, %s);
    """, (ref_type, ref_id, update_type, message))
    conn.commit()


if __name__ == "__main__":
    initialize_feedback_tables()
