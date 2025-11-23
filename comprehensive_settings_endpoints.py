"""
Comprehensive Employee Settings API Endpoints
Handles all employee profile data for organizational management
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import json

settings_bp = Blueprint('settings', __name__)

# This will be imported by apex_backend.py
# Add these endpoints to your apex_backend.py file

COMPREHENSIVE_SETTINGS_ENDPOINTS = """

# ==================== COMPREHENSIVE EMPLOYEE SETTINGS ====================

@app.route('/api/settings/employee/personal', methods=['GET', 'PUT'])
def employee_personal_info():
    '''Get or update employee personal information'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    name, email, date_of_birth, gender, blood_group, 
                    marital_status, nationality, aadhar_number, pan_number,
                    phone, mobile_number, profile_image, photo_url
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
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
            ''', (
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
    '''Get or update employee contact information'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    email, alternate_email, phone, mobile_number,
                    emergency_contact_name, emergency_contact_number, emergency_contact_relation,
                    current_address, permanent_address, city, state, pincode
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
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
            ''', (
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
    '''Get or update employee employment details'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    employee_id, designation, department, division, section,
                    establishment, reporting_manager_id, joining_date, employment_type,
                    grade_level, salary_band, work_location, office_room, extension_number,
                    (SELECT name FROM users u2 WHERE u2.id = users.reporting_manager_id) as reporting_manager_name
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
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
            ''', (
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
    '''Get or update employee educational qualifications'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    highest_qualification, specialization, university, 
                    year_of_passing, additional_qualifications, education_certificates
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
                UPDATE users SET
                    highest_qualification = %s,
                    specialization = %s,
                    university = %s,
                    year_of_passing = %s,
                    additional_qualifications = %s::jsonb,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (
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
    '''Get or update employee skills and expertise'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    technical_skills, certifications, languages_known,
                    areas_of_expertise, years_of_experience, previous_organizations
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
                UPDATE users SET
                    technical_skills = %s::jsonb,
                    certifications = %s::jsonb,
                    languages_known = %s::jsonb,
                    areas_of_expertise = %s::jsonb,
                    years_of_experience = %s,
                    previous_organizations = %s::jsonb,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (
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

@app.route('/api/settings/employee/security', methods=['GET', 'PUT'])
def employee_security():
    '''Get or update employee security and access details'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    security_clearance_level, security_clearance_expiry,
                    access_card_number, biometric_id, two_factor_enabled,
                    last_password_change, is_active
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
                UPDATE users SET
                    security_clearance_level = %s,
                    security_clearance_expiry = %s,
                    access_card_number = %s,
                    two_factor_enabled = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (
                data.get('securityClearanceLevel'),
                data.get('securityClearanceExpiry'),
                data.get('accessCardNumber'),
                data.get('twoFactorEnabled'),
                user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Security settings updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/financial', methods=['GET', 'PUT'])
def employee_financial():
    '''Get or update employee bank and financial details'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    bank_name, bank_account_number, ifsc_code, bank_branch,
                    pf_number, esi_number, uan_number
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            # Mask sensitive data
            if data:
                result = dict(data)
                if result.get('bank_account_number'):
                    result['bank_account_number'] = 'XXXX' + result['bank_account_number'][-4:]
                return jsonify(result)
            return jsonify({})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
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
            ''', (
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

@app.route('/api/settings/employee/leave', methods=['GET', 'PUT'])
def employee_leave():
    '''Get or update employee leave and attendance details'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    annual_leave_balance, sick_leave_balance, casual_leave_balance,
                    total_leaves_taken, attendance_percentage, shift_timings
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT (Admin only - would need role check)
            data = request.json
            cursor.execute('''
                UPDATE users SET
                    annual_leave_balance = %s,
                    sick_leave_balance = %s,
                    casual_leave_balance = %s,
                    shift_timings = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (
                data.get('annualLeaveBalance'),
                data.get('sickLeaveBalance'),
                data.get('casualLeaveBalance'),
                data.get('shiftTimings'),
                user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Leave details updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/performance', methods=['GET', 'PUT'])
def employee_performance():
    '''Get or update employee performance and training details'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    last_performance_rating, last_appraisal_date, next_appraisal_date,
                    trainings_completed, trainings_pending, awards_received
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # PUT
            data = request.json
            cursor.execute('''
                UPDATE users SET
                    trainings_completed = %s::jsonb,
                    trainings_pending = %s::jsonb,
                    awards_received = %s::jsonb,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            ''', (
                json.dumps(data.get('trainingsCompleted', [])),
                json.dumps(data.get('trainingsPending', [])),
                json.dumps(data.get('awardsReceived', [])),
                user_id
            ))
            conn.commit()
            return jsonify({'success': True, 'message': 'Performance details updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/complete', methods=['GET'])
def employee_complete_profile():
    '''Get complete employee profile (all sections)'''
    user_id = request.args.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        data = cursor.fetchone()
        
        if not data:
            return jsonify({'error': 'User not found'}), 404
        
        profile = dict(data)
        
        # Remove sensitive fields from complete profile
        sensitive_fields = ['password_hash', 'bank_account_number', 'aadhar_number']
        for field in sensitive_fields:
            if field in profile:
                if field == 'bank_account_number' and profile[field]:
                    profile[field] = 'XXXX' + profile[field][-4:]
                elif field == 'aadhar_number' and profile[field]:
                    profile[field] = 'XXXX-XXXX-' + profile[field][-4:]
                else:
                    del profile[field]
        
        return jsonify(profile)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/documents', methods=['GET', 'POST'])
def employee_documents():
    '''Get or upload employee documents'''
    user_id = request.args.get('user_id') if request.method == 'GET' else request.json.get('user_id', 3)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if request.method == 'GET':
            cursor.execute('''
                SELECT 
                    resume_url, photo_url, id_proof_url, address_proof_url,
                    education_certificates, other_documents
                FROM users WHERE id = %s
            ''', (user_id,))
            data = cursor.fetchone()
            return jsonify(dict(data) if data else {})
        
        else:  # POST
            data = request.json
            doc_type = data.get('documentType')
            doc_url = data.get('documentUrl')
            
            if doc_type in ['resume', 'photo', 'id_proof', 'address_proof']:
                cursor.execute(f'''
                    UPDATE users SET
                        {doc_type}_url = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (doc_url, user_id))
            else:
                # Add to other_documents array
                cursor.execute('''
                    UPDATE users SET
                        other_documents = other_documents || %s::jsonb,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (json.dumps([{'type': doc_type, 'url': doc_url, 'uploaded_at': datetime.now().isoformat()}]), user_id))
            
            conn.commit()
            return jsonify({'success': True, 'message': 'Document uploaded'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/settings/employee/profile-completion', methods=['GET'])
def employee_profile_completion():
    '''Calculate and return profile completion percentage'''
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

"""
