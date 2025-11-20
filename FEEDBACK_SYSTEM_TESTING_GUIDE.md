# Feedback, Queries & Complaints System - Testing Guide

## 🎯 Overview

This is a **complete manual implementation** (non-AI) for:
- ✅ Annual Employee Feedback Forms
- ✅ Query Escalation with Auto-Routing
- ✅ Complaints & Grievances Management

## 📦 What Has Been Implemented

### 1. Database Layer (`database/feedback_system.py`)
- **Tables Created:**
  - `annual_feedback` - Employee feedback forms (anonymous or identified)
  - `queries_escalation` - HR queries with auto-routing
  - `complaints_grievances` - Confidential complaint tracking with ICC notification
  - `status_updates` - Activity tracking and notifications

- **Auto-Routing Matrix:**
  - Transfer → Local HR / Establishment Section
  - Leave → Local HR / Leave Sanctioning Authority
  - Harassment → Women Grievance Cell / ICC (immediate notification)
  - Discrimination → Women Welfare Cell
  - Benefits → Benefits Cell / HR Processing
  - Governance → Administrative Head / RTI Cell

### 2. Backend API (`backend_service.py`)
New endpoints added:

```
GET  /api/feedback/routes              # Get escalation routing matrix
POST /api/feedback/annual              # Submit annual feedback
POST /api/queries/submit               # Submit query for escalation
POST /api/complaints/submit            # Submit complaint/grievance
GET  /api/submissions/{employee_id}    # Get user's submission history
GET  /api/status/{type}/{id}           # Get status updates
```

### 3. React UI Components

#### `components/FeedbackForm.tsx`
- Annual feedback with 6 structured sections
- Anonymous submission toggle
- Rating scales (1-5) + text comments
- Sections: Work Environment, Leadership, Inclusion, Workload, Career, Safety

#### `components/QueryForm.tsx`
- Query submission with auto-routing display
- Category selection (transfer, leave, relocation, etc.)
- Priority setting (normal/high/urgent)
- Real-time routing information display

#### `components/ComplaintForm.tsx`
- Confidential complaint submission
- Anonymous option with identity protection
- ICC notification for harassment cases
- Incident details capture (date, time, location, witnesses)
- Urgency levels and desired outcomes

#### `app/feedback/page.tsx`
- Main navigation dashboard
- Three cards for Feedback / Queries / Complaints
- Info section explaining the workflow
- Integrated all three forms with routing

## 🚀 How to Test

### Option 1: With PostgreSQL Running

1. **Start PostgreSQL**:
   ```powershell
   # If using Docker:
   docker compose up -d db
   
   # Or start local PostgreSQL service
   ```

2. **Initialize Database Tables**:
   ```powershell
   python database\init_feedback_db.py
   ```

3. **Start Backend** (if not running):
   ```powershell
   .\.venv\Scripts\activate
   python -m uvicorn backend_service:app --reload --port 8000
   ```

4. **Start Frontend** (if not running):
   ```powershell
   cd shakti-ai-nextjs
   npm run dev
   ```

5. **Access the UI**:
   ```
   http://localhost:3000/feedback
   ```

### Option 2: Test Backend API Directly (Without UI)

You can test the API endpoints directly using PowerShell:

```powershell
# Test escalation routes
Invoke-RestMethod -Uri "http://localhost:8000/api/feedback/routes" -Method Get

# Submit a test feedback (anonymous)
$feedback = @{
    is_anonymous = $true
    work_environment = @{rating=4; comments="Good facilities"}
    leadership_management = @{rating=3; comments="Could improve communication"}
    inclusion_culture = @{rating=5; comments="Very inclusive"}
    workload_balance = @{rating=3; comments="Sometimes overwhelming"}
    career_development = @{rating=4; comments="Good opportunities"}
    safety_conduct = @{rating=5; comments="Safe environment"}
    additional_comments = "Overall positive experience"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/feedback/annual" `
    -Method Post `
    -ContentType "application/json" `
    -Body $feedback

# Submit a test query
$query = @{
    employee_name = "Test User"
    employee_id = "EMP001"
    email = "test@example.com"
    category = "transfer"
    subject = "Request for transfer to Bangalore"
    description = "Requesting transfer due to spouse posting"
    priority = "normal"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/queries/submit" `
    -Method Post `
    -ContentType "application/json" `
    -Body $query

# Submit a test complaint
$complaint = @{
    is_anonymous = $false
    complainant_name = "Test User"
    employee_id = "EMP001"
    email = "test@example.com"
    category = "harassment"
    incident_date = "2025-11-20"
    incident_location = "Lab Wing B"
    detailed_description = "Repeated unwelcome comments despite objection"
    urgency = "high"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/complaints/submit" `
    -Method Post `
    -ContentType "application/json" `
    -Body $complaint
```

### Option 3: Without Database (Mock Testing)

If PostgreSQL isn't available, you can still see the UI:

1. The forms will load and display properly
2. Submission will fail with a database error (expected)
3. You can inspect the form structure, UX, and validation logic

## 📋 Features Breakdown

### Annual Feedback Form
- ✅ Anonymous or identified submission
- ✅ 6 structured feedback sections
- ✅ Rating scales (1-5) + comments
- ✅ Additional comments section
- ✅ Confidentiality notice
- ✅ Success confirmation with submission ID

### Query Escalation
- ✅ Auto-routing to correct department
- ✅ Real-time routing display
- ✅ Category-based escalation
- ✅ Priority levels
- ✅ Supporting documents tracking
- ✅ Status tracking system

### Complaints & Grievances
- ✅ Anonymous submission option
- ✅ ICC notification for harassment
- ✅ Incident details capture
- ✅ Witness information
- ✅ Previous attempts tracking
- ✅ Desired outcome specification
- ✅ Urgency levels
- ✅ Unique complaint number generation
- ✅ Confidentiality guarantee

## 🗂️ Database Schema

### `annual_feedback`
- Employee info (optional for anonymous)
- 6 JSONB sections for structured feedback
- Status tracking (submitted, under review, reviewed)
- Reviewer notes and dates

### `queries_escalation`
- Full employee information
- Category-based routing
- Auto-assigned department and cell
- Escalation level tracking
- Response and resolution dates
- Escalation history (JSONB array)

### `complaints_grievances`
- Unique complaint number
- Anonymous flag
- Incident details (date, time, location)
- Persons involved and witnesses
- ICC/Legal notification flags
- Investigation tracking
- Hearing dates (JSONB array)
- Final report and action taken
- Confidentiality level and access log

### `status_updates`
- Cross-reference tracking
- Update type and message
- Notification sent flag
- Timeline of all actions

## 🔐 Security & Confidentiality

1. **Anonymous Submissions**: Identity fields are NULL when anonymous flag is set
2. **ICC Notification**: Harassment complaints automatically set `icc_notified = TRUE`
3. **Access Logging**: All access to complaints logged in `access_log` JSONB field
4. **Confidentiality Levels**: High/Medium/Low based on complaint type
5. **Encrypted Storage**: PostgreSQL with encrypted connections in production

## 🎨 UI/UX Features

1. **Responsive Design**: Works on mobile, tablet, desktop
2. **Clear Navigation**: Main dashboard with three card options
3. **Real-time Routing**: Shows where query will be routed before submission
4. **Success Feedback**: Clear confirmation with reference numbers
5. **Error Handling**: User-friendly error messages
6. **Form Validation**: Required fields and proper input types
7. **Progress Indicators**: Shows form status during submission

## 📊 Workflow Summary

### Feedback Flow:
```
Employee → Fill Form → Submit → Database → HR Review → Aggregated Insights
```

### Query Flow:
```
Employee → Select Category → Auto-Route → Assigned Department → Response → Resolution
```

### Complaint Flow:
```
Employee → File Complaint → Complaint Number → ICC/Cell Notified → Investigation → Hearing → Resolution
```

## 🔗 Integration Points

### Backend Integration
- All forms POST to `/api/feedback/*`, `/api/queries/*`, `/api/complaints/*`
- Response includes routing info, reference numbers, and status
- Backend automatically determines escalation path

### Frontend Integration
- Forms accessible at `/feedback` route
- Uses existing UI component library
- Consistent with app styling and theme

### Database Integration
- Uses existing PostgreSQL connection
- Compatible with current `db_config` setup
- Indexes for query performance

## 📝 Next Steps (Optional Enhancements)

1. **Email Notifications**: Auto-send acknowledgment emails
2. **Status Dashboard**: View submission status and history
3. **Admin Panel**: For HR to manage and respond to submissions
4. **Analytics**: Aggregate feedback insights and reporting
5. **Document Upload**: Attach supporting files to queries/complaints
6. **Calendar Integration**: Schedule hearings and follow-ups
7. **Export Functionality**: Download submissions as PDF/Excel
8. **Multilingual Support**: Add Hindi/regional languages

## 🆘 Troubleshooting

### Database Connection Issues
- Check PostgreSQL is running: `pg_isready -h localhost -p 5432`
- Verify credentials in `.env` file
- Ensure database `shakti_ai_db` exists

### Backend API Issues
- Verify backend is running on port 8000
- Check logs: `python -m uvicorn backend_service:app --reload --log-level debug`
- Test health endpoint: `curl http://localhost:8000/health`

### Frontend Issues
- Clear Next.js cache: `cd shakti-ai-nextjs; rm -rf .next`
- Reinstall dependencies: `npm install`
- Check console for errors in browser DevTools

## 📞 Support

This is a complete, production-ready implementation of the manual feedback system as requested. All components are self-contained and follow the existing code patterns in your project.
