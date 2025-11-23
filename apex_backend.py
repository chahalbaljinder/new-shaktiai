"""
APEX API Backend
Provides RESTful API endpoints for all APEX features
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
import jwt
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'

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

# ==================== AUTHENTICATION ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'email', 'password', 'designation', 'establishment']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Insert new user
        cursor.execute("""
            INSERT INTO users (
                name, email, password_hash, designation, 
                establishment, role, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, name, email
        """, (
            data['name'],
            data['email'],
            password_hash.decode('utf-8'),
            data['designation'],
            data['establishment'],
            data.get('role', 'user'),
            True
        ))
        
        user = cursor.fetchone()
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email']
            }
        }), 201
    except Exception as e:
        conn.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s AND is_active = true", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Update last login
        cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (user['id'],))
        conn.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, JWT_SECRET, algorithm=JWT_ALGORITHM)
        
        return jsonify({
            'token': token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'designation': user['designation'],
                'establishment': user['establishment'],
                'role': user['role']
            },
            'onboarding': {
                'completed': user.get('onboarding_completed', False),
                'step': user.get('onboarding_step', 0),
                'must_change_password': user.get('must_change_password', False),
                'is_first_login': user.get('is_first_login', False)
            }
        })
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== ONBOARDING & SUPERADMIN ====================

@app.route('/api/admin/create-employee', methods=['POST'])
def create_employee():
    """Superadmin creates employee with temp credentials"""
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'email', 'designation', 'establishment']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (data['email'],))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Generate temporary password (can be customized)
        temp_password = data.get('temp_password', 'Welcome@123')
        password_hash = bcrypt.hashpw(temp_password.encode('utf-8'), bcrypt.gensalt())
        
        # Insert new employee
        cursor.execute("""
            INSERT INTO users (
                name, email, password_hash, designation, establishment,
                role, is_active, created_by_admin, must_change_password,
                is_first_login, onboarding_completed, onboarding_step,
                temp_password
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, name, email, employee_id
        """, (
            data['name'],
            data['email'],
            password_hash.decode('utf-8'),
            data['designation'],
            data['establishment'],
            data.get('role', 'user'),
            True,
            True,  # created_by_admin
            True,  # must_change_password
            True,  # is_first_login
            False, # onboarding_completed
            0,     # onboarding_step
            temp_password
        ))
        
        employee = cursor.fetchone()
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Employee created successfully',
            'employee': {
                'id': employee['id'],
                'name': employee['name'],
                'email': employee['email'],
                'employee_id': employee['employee_id'],
                'temp_password': temp_password
            }
        }), 201
    except Exception as e:
        conn.rollback()
        print(f"Create employee error: {str(e)}")
        return jsonify({'error': 'Failed to create employee'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/check-onboarding', methods=['GET'])
def check_onboarding():
    """Check if user needs onboarding"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                onboarding_completed,
                onboarding_step,
                is_first_login,
                must_change_password
            FROM users WHERE id = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'needs_onboarding': not user['onboarding_completed'],
            'current_step': user['onboarding_step'] or 0,
            'is_first_login': user['is_first_login'],
            'must_change_password': user['must_change_password']
        })
    except Exception as e:
        print(f"Check onboarding error: {str(e)}")
        return jsonify({'error': 'Failed to check onboarding'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/onboarding/update-step', methods=['PUT'])
def update_onboarding_step():
    """Update user's onboarding step"""
    data = request.json
    user_id = data.get('user_id')
    step = data.get('step')
    
    if not user_id or step is None:
        return jsonify({'error': 'user_id and step required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET 
                onboarding_step = %s,
                onboarding_started_at = COALESCE(onboarding_started_at, CURRENT_TIMESTAMP),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (step, user_id))
        
        conn.commit()
        return jsonify({'success': True, 'step': step})
    except Exception as e:
        conn.rollback()
        print(f"Update onboarding step error: {str(e)}")
        return jsonify({'error': 'Failed to update step'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/auth/onboarding/complete', methods=['POST'])
def complete_onboarding():
    """Mark onboarding as complete"""
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE users 
            SET 
                onboarding_completed = TRUE,
                onboarding_step = 5,
                onboarding_completed_at = CURRENT_TIMESTAMP,
                is_first_login = FALSE,
                must_change_password = FALSE,
                temp_password = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (user_id,))
        
        conn.commit()
        return jsonify({
            'success': True,
            'message': 'Onboarding completed successfully'
        })
    except Exception as e:
        conn.rollback()
        print(f"Complete onboarding error: {str(e)}")
        return jsonify({'error': 'Failed to complete onboarding'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/employees', methods=['GET'])
def list_employees():
    """List all employees (superadmin only)"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                id, employee_id, name, email, designation, 
                department, establishment, role, is_active,
                onboarding_completed, created_at, last_login
            FROM users
            WHERE created_by_admin = TRUE
            ORDER BY created_at DESC
        """)
        
        employees = cursor.fetchall()
        return jsonify({'employees': employees})
    except Exception as e:
        print(f"List employees error: {str(e)}")
        return jsonify({'error': 'Failed to fetch employees'}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== DASHBOARD STATS ====================

@app.route('/api/dashboard/stats', methods=['GET'])
def dashboard_stats():
    """Get dashboard statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get total users
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_active = true")
        total_users = cursor.fetchone()['count']
        
        # Get total queries today
        cursor.execute("""
            SELECT COUNT(*) as count FROM knowledge_queries 
            WHERE DATE(created_at) = CURRENT_DATE
        """)
        queries_today = cursor.fetchone()['count']
        
        # Get active sessions
        cursor.execute("""
            SELECT COUNT(*) as count FROM user_sessions 
            WHERE is_active = true AND expires_at > CURRENT_TIMESTAMP
        """)
        active_sessions = cursor.fetchone()['count']
        
        # Get agent count (static for now)
        agents_running = 12
        
        return jsonify({
            'total_users': total_users,
            'queries_today': queries_today,
            'active_sessions': active_sessions,
            'agents_running': agents_running
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/dashboard/recent-queries', methods=['GET'])
def recent_queries():
    """Get recent knowledge base queries"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                kq.id,
                kq.query_text as product,
                kq.status,
                kq.response_time_ms as response_time,
                kq.created_at,
                u.name as user_name
            FROM knowledge_queries kq
            LEFT JOIN users u ON kq.user_id = u.id
            ORDER BY kq.created_at DESC
            LIMIT 5
        """)
        queries = cursor.fetchall()
        
        # Format data
        formatted_queries = []
        for q in queries:
            formatted_queries.append({
                'id': f"QRY-{str(q['id']).zfill(3)}",
                'product': q['product'][:50] if q['product'] else 'Query',
                'status': q['status'].capitalize() if q['status'] else 'Completed',
                'amount': f"{q['response_time'] / 1000:.1f}s" if q['response_time'] else '2.0s',
                'statusColor': 'text-[#10B981] bg-[#10B981]/10' if q['status'] == 'completed' else 'text-[#F59E0B] bg-[#F59E0B]/10'
            })
        
        return jsonify(formatted_queries)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/dashboard/personnel-distribution', methods=['GET'])
def personnel_distribution():
    """Get personnel distribution by establishment"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                establishment,
                COUNT(*) as count
            FROM users
            WHERE is_active = true
            GROUP BY establishment
            ORDER BY count DESC
        """)
        results = cursor.fetchall()
        
        # Map to display format
        distribution = []
        total = sum(r['count'] for r in results)
        
        establishment_map = {
            'DRDO HQ, Delhi': {'flag': '🏛️', 'name': 'Delhi HQ'},
            'DRDL, Hyderabad': {'flag': '⚙️', 'name': 'Hyderabad Labs'},
            'ADE, Bangalore': {'flag': '🔬', 'name': 'Bangalore Labs'},
        }
        
        for r in results:
            est = establishment_map.get(r['establishment'], {'flag': '📍', 'name': r['establishment']})
            distribution.append({
                'country': est['name'],
                'customers': r['count'],
                'percentage': int((r['count'] / total * 100)) if total > 0 else 0,
                'flag': est['flag']
            })
        
        # Add "Others" if needed
        if len(distribution) > 3:
            others_count = sum(d['customers'] for d in distribution[3:])
            others_pct = int((others_count / total * 100)) if total > 0 else 0
            distribution = distribution[:3] + [{
                'country': 'Other Establishments',
                'customers': others_count,
                'percentage': others_pct,
                'flag': '📍'
            }]
        
        return jsonify(distribution[:4])  # Return top 4
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== FEEDBACK / GRIEVANCE ====================

@app.route('/api/feedback', methods=['GET'])
def get_feedback():
    """Get all feedback/grievances"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get query parameters
        type_filter = request.args.get('type', 'all')
        status_filter = request.args.get('status', 'all')
        search = request.args.get('search', '')
        
        query = """
            SELECT 
                f.id,
                f.type,
                f.title as subject,
                f.description,
                f.category,
                f.priority,
                f.status,
                f.created_at as submitted_at,
                f.updated_at as last_updated,
                f.response_text,
                f.assigned_to,
                u.name as submitted_by,
                u.designation,
                u.establishment
            FROM feedback f
            LEFT JOIN users u ON f.user_id = u.id
            WHERE 1=1
        """
        params = []
        
        if type_filter != 'all':
            query += " AND f.type = %s"
            params.append(type_filter)
        
        if status_filter != 'all':
            query += " AND f.status = %s"
            params.append(status_filter)
        
        if search:
            query += " AND (f.title ILIKE %s OR f.description ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += " ORDER BY f.created_at DESC LIMIT 50"
        
        cursor.execute(query, params)
        feedbacks = cursor.fetchall()
        
        # Format response
        formatted = []
        for f in feedbacks:
            formatted.append({
                'id': f"{'FB' if f['type'] == 'feedback' else 'GR' if f['type'] == 'grievance' else 'SG'}{str(f['id']).zfill(3)}",
                'type': f['type'],
                'subject': f['subject'],
                'description': f['description'],
                'category': f['category'],
                'priority': f['priority'],
                'status': f['status'],
                'submittedBy': f'{f["submitted_by"]} ({f["designation"]})' if f['submitted_by'] else 'Anonymous',
                'establishment': f['establishment'] or 'N/A',
                'submittedAt': f['submitted_at'].isoformat() if f['submitted_at'] else None,
                'updatedAt': f['last_updated'].isoformat() if f['last_updated'] else None,
                'responseText': f['response_text'],
                'assignedTo': f['assigned_to']
            })
        
        return jsonify(formatted)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit new feedback/grievance/complaint"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Log the incoming data for debugging
        print("Received feedback data:", data)
        
        # Generate tracking number for complaints
        tracking_number = None
        if data.get('type') == 'complaint':
            import random
            tracking_number = f"COMP-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        
        cursor.execute("""
            INSERT INTO feedback (
                user_id, type, title, description, category, 
                priority, status, is_anonymous
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.get('user_id', 3),  # Default to DRDO Admin
            data.get('type', 'feedback'),
            data.get('title', ''),
            data.get('description', ''),
            data.get('category', 'General'),
            data.get('priority', 'medium'),
            'submitted' if data.get('type') != 'complaint' else 'under-review',  # Complaints go directly to review
            data.get('is_anonymous', data.get('isAnonymous', False))
        ))
        
        feedback_id = cursor.fetchone()['id']
        conn.commit()
        
        response_data = {
            'success': True,
            'id': feedback_id,
            'message': 'Complaint submitted successfully! Your complaint will be reviewed within 24 hours.' if data.get('type') == 'complaint' else 'Feedback submitted successfully'
        }
        
        if tracking_number:
            response_data['tracking_number'] = tracking_number
        
        return jsonify(response_data), 201
    except Exception as e:
        conn.rollback()
        print(f"Error submitting feedback: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/feedback/stats', methods=['GET'])
def feedback_stats():
    """Get feedback statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'under-review' THEN 1 END) as under_review,
                COUNT(CASE WHEN status = 'in-progress' THEN 1 END) as in_progress,
                COUNT(CASE WHEN status = 'resolved' THEN 1 END) as resolved,
                COUNT(CASE WHEN type = 'feedback' THEN 1 END) as feedback_count,
                COUNT(CASE WHEN type = 'grievance' THEN 1 END) as complaints,
                COUNT(CASE WHEN priority = 'urgent' OR priority = 'critical' THEN 1 END) as urgent
            FROM feedback
        """)
        stats = cursor.fetchone()
        
        return jsonify({
            'total': stats['total'],
            'feedback': stats['feedback_count'],
            'complaints': stats['complaints'],
            'pending': stats['under_review'],
            'inProgress': stats['in_progress'],
            'resolved': stats['resolved'],
            'urgent': stats['urgent']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== KNOWLEDGE BASE ====================

@app.route('/api/knowledge/query', methods=['POST'])
def knowledge_query():
    """Submit and log knowledge base query"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Log the query
        cursor.execute("""
            INSERT INTO knowledge_queries (
                user_id, query_text, response_text, 
                response_time_ms, category, status
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.get('user_id', 3),
            data['query'],
            data.get('response', ''),
            data.get('response_time', 2000),
            data.get('category', 'General'),
            'completed'
        ))
        
        query_id = cursor.fetchone()['id']
        conn.commit()
        
        return jsonify({
            'success': True,
            'query_id': query_id
        })
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== WISHES VAULT ====================

@app.route('/api/wishes', methods=['GET'])
def get_wishes():
    """Get user wishes"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM wishes 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        wishes = cursor.fetchall()
        
        return jsonify([dict(w) for w in wishes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/wishes', methods=['POST'])
def create_wish():
    """Create new wish"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO wishes (
                user_id, title, content, category, priority
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (
            data.get('user_id', 3),
            data['title'],
            data['content'],
            data.get('category', 'personal'),
            data.get('priority', 'medium')
        ))
        
        wish_id = cursor.fetchone()['id']
        conn.commit()
        
        return jsonify({
            'success': True,
            'wish_id': wish_id,
            'message': 'Wish created successfully'
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/wishes/<int:wish_id>', methods=['PUT'])
def update_wish(wish_id):
    """Update existing wish"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build dynamic update query
        update_fields = []
        values = []
        
        if 'title' in data:
            update_fields.append('title = %s')
            values.append(data['title'])
        if 'content' in data:
            update_fields.append('content = %s')
            values.append(data['content'])
        if 'category' in data:
            update_fields.append('category = %s')
            values.append(data['category'])
        if 'priority' in data:
            update_fields.append('priority = %s')
            values.append(data['priority'])
        if 'reminder_date' in data:
            update_fields.append('reminder_date = %s')
            values.append(data['reminder_date'])
        
        update_fields.append('updated_at = CURRENT_TIMESTAMP')
        values.append(wish_id)
        
        query = f"UPDATE wishes SET {', '.join(update_fields)} WHERE id = %s"
        cursor.execute(query, values)
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Wish updated successfully'
        })
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/wishes/<int:wish_id>', methods=['DELETE'])
def delete_wish(wish_id):
    """Delete a wish"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM wishes WHERE id = %s', (wish_id,))
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Wish deleted successfully'
        })
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/wishes/share', methods=['POST'])
def share_wish():
    """Share a wish via email or WhatsApp"""
    data = request.json
    wish_id = data.get('wishId')
    method = data.get('method')
    recipient = data.get('recipient')
    sender_name = data.get('senderName', 'APEX User')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get wish details
        cursor.execute('SELECT * FROM wishes WHERE id = %s', (wish_id,))
        wish = cursor.fetchone()
        
        if not wish:
            return jsonify({'error': 'Wish not found'}), 404
        
        # Log sharing history
        cursor.execute("""
            INSERT INTO sharing_history (
                wish_id, user_id, shared_with_email, shared_via, status
            ) VALUES (%s, %s, %s, %s, %s)
        """, (wish_id, wish['user_id'], recipient, method, 'sent'))
        conn.commit()
        
        response = {
            'success': True,
            'message': f'Wish shared successfully via {method}'
        }
        
        # If WhatsApp, generate URL
        if method == 'whatsapp':
            message = f"*{wish['title']}*\n\n{wish['content']}\n\n_Shared from APEX Wishes Vault by {sender_name}_"
            whatsapp_url = f"https://wa.me/{recipient.replace('+', '')}?text={message}"
            response['whatsapp_url'] = whatsapp_url
        
        return jsonify(response)
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== SETTINGS ====================

@app.route('/api/settings/profile', methods=['GET'])
def get_profile():
    """Get user profile settings"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, name, email, designation, establishment, 
                   role, profile_image, created_at, last_login
            FROM users 
            WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(dict(user))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/profile', methods=['PUT'])
def update_profile():
    """Update user profile settings"""
    data = request.json
    user_id = data.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build dynamic update query
        update_fields = []
        values = []
        
        if 'name' in data:
            update_fields.append('name = %s')
            values.append(data['name'])
        if 'email' in data:
            update_fields.append('email = %s')
            values.append(data['email'])
        if 'designation' in data:
            update_fields.append('designation = %s')
            values.append(data['designation'])
        if 'establishment' in data:
            update_fields.append('establishment = %s')
            values.append(data['establishment'])
        
        if not update_fields:
            return jsonify({'error': 'No fields to update'}), 400
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s RETURNING name, email"
        
        cursor.execute(query, values)
        updated_user = cursor.fetchone()
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': dict(updated_user)
        })
    except Exception as e:
        conn.rollback()
        print(f"Profile update error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/password', methods=['PUT'])
def change_password():
    """Change user password"""
    data = request.json
    user_id = data.get('user_id', 3)
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    is_first_time = data.get('is_first_time', False)  # For onboarding
    
    if not new_password:
        return jsonify({'error': 'New password required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get user data
        cursor.execute("SELECT password_hash, must_change_password FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # If not first time, verify current password
        if not is_first_time and current_password:
            # Check if password_hash exists and is valid
            if not user['password_hash'] or len(user['password_hash']) < 20:
                return jsonify({'error': 'Invalid password configuration. Please contact administrator.'}), 500
            
            try:
                if not bcrypt.checkpw(current_password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                    return jsonify({'error': 'Current password is incorrect'}), 401
            except Exception as bcrypt_error:
                print(f"Bcrypt error: {str(bcrypt_error)}")
                return jsonify({'error': 'Password verification failed'}), 500
        
        # Hash new password
        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        
        # Update password and clear first-time flags
        cursor.execute("""
            UPDATE users 
            SET password_hash = %s,
                must_change_password = FALSE,
                temp_password = NULL,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (new_hash.decode('utf-8'), user_id))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })
    except Exception as e:
        conn.rollback()
        print(f"Password change error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/notifications', methods=['GET'])
def get_notifications_settings():
    """Get user notification preferences"""
    user_id = request.args.get('user_id', 3)
    
    # For now, return default settings (can be stored in a preferences table later)
    return jsonify({
        'expertResponses': True,
        'wishReminders': True,
        'weeklyCheckins': True,
        'communityUpdates': False,
        'emergencyAlerts': True,
        'voiceConfirmations': True
    })

@app.route('/api/settings/notifications', methods=['PUT'])
def update_notifications_settings():
    """Update user notification preferences"""
    data = request.json
    user_id = data.get('user_id', 3)
    
    # Store in user preferences (simplified - can be enhanced with a preferences table)
    return jsonify({
        'success': True,
        'message': 'Notification preferences updated',
        'settings': data.get('settings', {})
    })

@app.route('/api/settings/export', methods=['GET'])
def export_user_data():
    """Export all user data"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get user data
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        # Get wishes
        cursor.execute("SELECT * FROM wishes WHERE user_id = %s", (user_id,))
        wishes = cursor.fetchall()
        
        # Get feedback
        cursor.execute("SELECT * FROM feedback WHERE user_id = %s", (user_id,))
        feedback = cursor.fetchall()
        
        # Get knowledge queries
        cursor.execute("SELECT * FROM knowledge_queries WHERE user_id = %s", (user_id,))
        queries = cursor.fetchall()
        
        export_data = {
            'user': dict(user) if user else {},
            'wishes': [dict(w) for w in wishes],
            'feedback': [dict(f) for f in feedback],
            'knowledge_queries': [dict(q) for q in queries],
            'export_date': datetime.now().isoformat()
        }
        
        return jsonify(export_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/stats', methods=['GET'])
def get_user_stats():
    """Get user activity statistics"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get user stats
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM wishes WHERE user_id = %s) as total_wishes,
                (SELECT COUNT(*) FROM feedback WHERE user_id = %s) as total_feedback,
                (SELECT COUNT(*) FROM knowledge_queries WHERE user_id = %s) as total_queries,
                (SELECT created_at FROM users WHERE id = %s) as member_since
        """, (user_id, user_id, user_id, user_id))
        
        stats = cursor.fetchone()
        
        return jsonify({
            'total_wishes': stats['total_wishes'],
            'total_feedback': stats['total_feedback'],
            'total_queries': stats['total_queries'],
            'member_since': stats['member_since'].isoformat() if stats['member_since'] else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== COMPREHENSIVE EMPLOYEE SETTINGS ====================

@app.route('/api/settings/employee/personal', methods=['GET', 'PUT'])
def employee_personal_info():
    """Get or update employee personal information"""
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT 
                    name, email, date_of_birth, gender, blood_group, 
                    marital_status, nationality, aadhar_number, pan_number,
                    phone, mobile_number, profile_image, photo_url
                FROM users WHERE id = %s
            """, (user_id,))
            data = cursor.fetchone()
            result = dict(data) if data else {}
            # Mask sensitive data
            if result.get('aadhar_number'):
                result['aadhar_number'] = 'XXXX-XXXX-' + result['aadhar_number'][-4:] if len(result['aadhar_number']) >= 4 else 'XXXX-XXXX-XXXX'
            return jsonify(result)
        
        else:  # PUT
            data = request.json
            cursor.execute("""
                UPDATE users SET
                    name = COALESCE(%s, name),
                    email = COALESCE(%s, email),
                    date_of_birth = %s,
                    gender = %s,
                    blood_group = %s,
                    marital_status = %s,
                    nationality = %s,
                    aadhar_number = %s,
                    pan_number = %s,
                    phone = %s,
                    mobile_number = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING name, email
            """, (
                data.get('name'), data.get('email'),
                data.get('dateOfBirth'), data.get('gender'),
                data.get('bloodGroup'), data.get('maritalStatus'),
                data.get('nationality'), data.get('aadharNumber'),
                data.get('panNumber'), data.get('phone'),
                data.get('mobileNumber'), user_id
            ))
            result = cursor.fetchone()
            conn.commit()
            return jsonify({'success': True, 'message': 'Personal info updated', 'user': dict(result)})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/contact', methods=['GET', 'PUT'])
def employee_contact_info():
    """Get or update employee contact information"""
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT 
                    email, alternate_email, phone, mobile_number,
                    emergency_contact_name, emergency_contact_number, emergency_contact_relation,
                    current_address, permanent_address, city, state, pincode
                FROM users WHERE id = %s
            """, (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute("""
                UPDATE users SET
                    alternate_email = %s,
                    mobile_number = %s,
                    emergency_contact_name = %s,
                    emergency_contact_number = %s,
                    emergency_contact_relation = %s,
                    current_address = %s,
                    permanent_address = %s,
                    city = %s,
                    state = %s,
                    pincode = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                data.get('alternateEmail'), data.get('mobileNumber'),
                data.get('emergencyContactName'), data.get('emergencyContactNumber'),
                data.get('emergencyContactRelation'), data.get('currentAddress'),
                data.get('permanentAddress'), data.get('city'),
                data.get('state'), data.get('pincode'), user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Contact info updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/employment', methods=['GET', 'PUT'])
def employee_employment_details():
    """Get or update employee employment details"""
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT 
                    employee_id, designation, department, division, section,
                    establishment, reporting_manager_id, joining_date, employment_type,
                    grade_level, salary_band, work_location, office_room, extension_number,
                    (SELECT name FROM users u2 WHERE u2.id = users.reporting_manager_id) as reporting_manager_name
                FROM users WHERE id = %s
            """, (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute("""
                UPDATE users SET
                    designation = %s,
                    department = %s,
                    division = %s,
                    section = %s,
                    establishment = %s,
                    reporting_manager_id = %s,
                    employment_type = %s,
                    grade_level = %s,
                    work_location = %s,
                    office_room = %s,
                    extension_number = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                data.get('designation'), data.get('department'),
                data.get('division'), data.get('section'),
                data.get('establishment'), data.get('reportingManagerId'),
                data.get('employmentType'), data.get('gradeLevel'),
                data.get('workLocation'), data.get('officeRoom'),
                data.get('extensionNumber'), user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Employment details updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/education', methods=['GET', 'PUT'])
def employee_education():
    """Get or update employee educational qualifications"""
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT 
                    highest_qualification, specialization, university, 
                    year_of_passing, additional_qualifications, education_certificates
                FROM users WHERE id = %s
            """, (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute("""
                UPDATE users SET
                    highest_qualification = %s,
                    specialization = %s,
                    university = %s,
                    year_of_passing = %s,
                    additional_qualifications = %s::jsonb,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                data.get('highestQualification'), data.get('specialization'),
                data.get('university'), data.get('yearOfPassing'),
                json.dumps(data.get('additionalQualifications', [])), user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Education details updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/skills', methods=['GET', 'PUT'])
def employee_skills():
    """Get or update employee skills and expertise"""
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT 
                    technical_skills, certifications, languages_known,
                    areas_of_expertise, years_of_experience, previous_organizations
                FROM users WHERE id = %s
            """, (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute("""
                UPDATE users SET
                    technical_skills = %s::jsonb,
                    certifications = %s::jsonb,
                    languages_known = %s::jsonb,
                    areas_of_expertise = %s::jsonb,
                    years_of_experience = %s,
                    previous_organizations = %s::jsonb,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                json.dumps(data.get('technicalSkills', [])),
                json.dumps(data.get('certifications', [])),
                json.dumps(data.get('languagesKnown', [])),
                json.dumps(data.get('areasOfExpertise', [])),
                data.get('yearsOfExperience'),
                json.dumps(data.get('previousOrganizations', [])),
                user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Skills updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/financial', methods=['GET', 'PUT'])
def employee_financial():
    """Get or update employee bank and financial details"""
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute("""
                SELECT 
                    bank_name, bank_account_number, ifsc_code, bank_branch,
                    pf_number, esi_number, uan_number
                FROM users WHERE id = %s
            """, (user_id,))
            data = cursor.fetchone()
            # Mask sensitive data
            if data:
                result = dict(data)
                if result.get('bank_account_number'):
                    result['bank_account_number'] = 'XXXX' + result['bank_account_number'][-4:] if len(result.get('bank_account_number', '')) >= 4 else 'XXXXXXXXXX'
                return jsonify(result)
            return jsonify({})
        
        else:  # PUT
            data = request.json
            cursor.execute("""
                UPDATE users SET
                    bank_name = %s,
                    bank_account_number = %s,
                    ifsc_code = %s,
                    bank_branch = %s,
                    pf_number = %s,
                    esi_number = %s,
                    uan_number = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                data.get('bankName'), data.get('bankAccountNumber'),
                data.get('ifscCode'), data.get('bankBranch'),
                data.get('pfNumber'), data.get('esiNumber'),
                data.get('uanNumber'), user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Financial details updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/leave', methods=['GET'])
def employee_leave():
    """Get employee leave and attendance details"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                annual_leave_balance, sick_leave_balance, casual_leave_balance,
                total_leaves_taken, attendance_percentage, shift_timings
            FROM users WHERE id = %s
        """, (user_id,))
        data = cursor.fetchone()
        return jsonify(dict(data) if data else {})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/performance', methods=['GET'])
def employee_performance():
    """Get employee performance and training details"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                last_performance_rating, last_appraisal_date, next_appraisal_date,
                trainings_completed, trainings_pending, awards_received
            FROM users WHERE id = %s
        """, (user_id,))
        data = cursor.fetchone()
        return jsonify(dict(data) if data else {})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/complete', methods=['GET'])
def employee_complete_profile():
    """Get complete employee profile (all sections)"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        data = cursor.fetchone()
        
        if not data:
            return jsonify({'error': 'User not found'}), 404
        
        profile = dict(data)
        
        # Remove/mask sensitive fields
        sensitive_fields = ['password_hash']
        for field in sensitive_fields:
            if field in profile:
                del profile[field]
        
        if profile.get('bank_account_number'):
            profile['bank_account_number'] = 'XXXX' + profile['bank_account_number'][-4:] if len(profile.get('bank_account_number', '')) >= 4 else 'XXXXXXXXXX'
        if profile.get('aadhar_number'):
            profile['aadhar_number'] = 'XXXX-XXXX-' + profile['aadhar_number'][-4:] if len(profile.get('aadhar_number', '')) >= 4 else 'XXXX-XXXX-XXXX'
        
        return jsonify(profile)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/profile-completion', methods=['GET'])
def employee_profile_completion():
    """Calculate and return profile completion percentage"""
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        data = cursor.fetchone()
        
        if not data:
            return jsonify({'error': 'User not found'}), 404
        
        profile = dict(data)
        
        # Define required fields for completion
        sections = {
            'personal': ['name', 'email', 'date_of_birth', 'gender', 'phone', 'mobile_number'],
            'contact': ['current_address', 'city', 'state', 'pincode', 'emergency_contact_name', 'emergency_contact_number'],
            'employment': ['employee_id', 'designation', 'department', 'establishment', 'joining_date'],
            'education': ['highest_qualification', 'specialization', 'university'],
            'skills': ['technical_skills', 'languages_known', 'years_of_experience'],
            'financial': ['bank_name', 'bank_account_number', 'ifsc_code', 'pf_number']
        }
        
        completion = {}
        for section, fields in sections.items():
            filled = sum(1 for field in fields if profile.get(field))
            completion[section] = {
                'percentage': round((filled / len(fields)) * 100),
                'filled': filled,
                'total': len(fields)
            }
        
        overall = round(sum(c['percentage'] for c in completion.values()) / len(sections))
        
        # Update profile completion in database
        cursor.execute(
            'UPDATE users SET profile_completion_percentage = %s WHERE id = %s',
            (overall, user_id)
        )
        conn.commit()
        
        return jsonify({
            'overall': overall,
            'sections': completion
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })

@app.route('/api/status', methods=['GET'])
def status():
    """API status endpoint"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) as count FROM users")
        user_count = cursor.fetchone()['count']
        
        return jsonify({
            'status': 'operational',
            'version': '1.0.0',
            'database': 'connected',
            'users': user_count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500
    finally:
        cursor.close()
        conn.close()

# ============================================
# SUPERADMIN MANAGEMENT ENDPOINTS
# ============================================

@app.route('/api/admin/users/list', methods=['GET'])
def list_all_users():
    """Get list of all users with their details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                id, employee_id, name, email, phone, designation, 
                department, division, establishment, role, 
                is_active, onboarding_completed, onboarding_step,
                created_by_admin, created_at, last_login
            FROM users
            ORDER BY created_at DESC
        """)
        
        users = cursor.fetchall()
        
        return jsonify({
            'users': users,
            'count': len(users)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    """Get dashboard statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Total users
        cursor.execute("SELECT COUNT(*) as count FROM users")
        total_users = cursor.fetchone()['count']
        
        # Active users
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_active = TRUE")
        active_users = cursor.fetchone()['count']
        
        # Pending onboarding
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE onboarding_completed = FALSE")
        onboarding_pending = cursor.fetchone()['count']
        
        # New this month
        cursor.execute("""
            SELECT COUNT(*) as count FROM users 
            WHERE created_at >= date_trunc('month', CURRENT_DATE)
        """)
        new_this_month = cursor.fetchone()['count']
        
        return jsonify({
            'totalUsers': total_users,
            'activeUsers': active_users,
            'onboardingPending': onboarding_pending,
            'newThisMonth': new_this_month
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_user_admin(user_id):
    """Update user details by admin"""
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build dynamic UPDATE query based on provided fields
        update_fields = []
        update_values = []
        
        allowed_fields = [
            'name', 'email', 'phone', 'designation', 'department', 
            'division', 'establishment', 'role', 'is_active', 
            'employee_id', 'grade_level', 'date_of_birth', 'gender'
        ]
        
        for field in allowed_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field])
        
        if not update_fields:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        update_values.append(user_id)
        
        query = f"""
            UPDATE users 
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id, name, email, role, is_active
        """
        
        cursor.execute(query, update_values)
        updated_user = cursor.fetchone()
        conn.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': updated_user
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user_admin(user_id):
    """Delete user by admin"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute("SELECT id, name, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prevent deleting superadmin
        if user['role'] == 'superadmin':
            return jsonify({'error': 'Cannot delete superadmin user'}), 403
        
        # Delete user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        return jsonify({
            'message': 'User deleted successfully',
            'deleted_user': user['name']
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/admin/users/<int:user_id>/reset-password', methods=['POST'])
def reset_user_password(user_id):
    """Reset user password by admin"""
    data = request.json
    new_password = data.get('new_password')
    
    if not new_password:
        return jsonify({'error': 'new_password is required'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if user exists
        cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Hash new password
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update password and set must_change_password flag
        cursor.execute("""
            UPDATE users 
            SET password = %s, 
                temp_password = %s,
                must_change_password = TRUE,
                updated_at = NOW()
            WHERE id = %s
        """, (hashed_password, new_password, user_id))
        
        conn.commit()
        
        return jsonify({
            'message': 'Password reset successfully',
            'user': user['name'],
            'email': user['email'],
            'temp_password': new_password
        })
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    print("🚀 Starting APEX API Backend...")
    print("📊 Database: Connected")
    print("🌐 API Server: http://localhost:8000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=8000, debug=True)
