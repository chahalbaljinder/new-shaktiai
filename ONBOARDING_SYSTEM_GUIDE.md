# Employee Onboarding System - Complete Guide

## Overview

The system now includes a comprehensive employee onboarding flow where:
1. **SuperAdmin** creates employee accounts with temporary credentials
2. **Employees** receive login credentials via email/manually
3. **First-time login** triggers a 5-step onboarding wizard
4. **Profile completion** is mandatory before accessing the application
5. **Access granted** only after completing all onboarding steps

---

## System Components

### 1. Database Schema (New Fields)
- `onboarding_completed`: BOOLEAN - Whether employee completed onboarding
- `onboarding_step`: INTEGER - Current step (0-5)
- `onboarding_started_at`: TIMESTAMP - When onboarding began
- `onboarding_completed_at`: TIMESTAMP - When completed
- `is_first_login`: BOOLEAN - First time logging in
- `must_change_password`: BOOLEAN - Requires password change
- `created_by_admin`: BOOLEAN - Created by superadmin
- `temp_password`: VARCHAR(255) - Temporary password (cleared after first login)

### 2. Backend API Endpoints

#### SuperAdmin Endpoints
```bash
# Create new employee
POST /api/admin/create-employee
Body: {
  "name": "John Doe",
  "email": "john@example.com",
  "designation": "Senior Scientist",
  "establishment": "DRDO Delhi",
  "department": "R&D",
  "role": "user",
  "temp_password": "Welcome@123"
}

# List all employees
GET /api/admin/employees
```

#### Onboarding Endpoints
```bash
# Check onboarding status
GET /api/auth/check-onboarding?user_id=123

# Update onboarding step
PUT /api/auth/onboarding/update-step
Body: { "user_id": 123, "step": 2 }

# Complete onboarding
POST /api/auth/onboarding/complete
Body: { "user_id": 123 }
```

### 3. Frontend Components

#### OnboardingFlow Component
**Location**: `components/OnboardingFlow.tsx`

**5-Step Wizard**:
1. **Password Change** - Set secure password (replaces temp password)
2. **Personal Information** - Name, email, phone, DOB, gender, blood group
3. **Contact Details** - Emergency contact, addresses
4. **Employment Information** - Department, designation, division, etc.
5. **Education & Skills** - Qualifications, technical skills, experience

**Features**:
- Step-by-step validation
- Progress bar with visual indicators
- Auto-save after each step
- Cannot skip steps
- Smooth animations with Framer Motion

#### SuperAdminPanel Component
**Location**: `components/SuperAdminPanel.tsx`

**Features**:
- Create employee accounts
- Generate temporary passwords
- View all employees with onboarding status
- Search and filter employees
- Copy credentials to clipboard

---

## User Flow

### SuperAdmin Workflow

1. **Access SuperAdmin Panel**
   - Navigate to Settings → Admin section (for superadmin role)
   - Or create dedicated route `/admin` with SuperAdminPanel component

2. **Create Employee**
   ```
   - Fill employee details (name, email, designation, establishment)
   - Click "Generate Password" to create secure temp password
   - Submit form
   - Copy credentials and share with employee
   ```

3. **Monitor Employees**
   - View all created employees
   - Check onboarding completion status
   - See active/inactive status

### Employee Workflow

1. **Receive Credentials**
   ```
   Employee ID: EMP000123
   Email: john.doe@example.com
   Temporary Password: Welcome@1234
   ```

2. **First Login**
   - Go to login page
   - Enter email and temporary password
   - System detects `must_change_password = true`
   - Redirects to onboarding flow

3. **Complete Onboarding** (5 Steps)

   **Step 1: Change Password**
   - Enter new password (min 6 characters)
   - Confirm password
   - System validates and saves

   **Step 2: Personal Information**
   - Update name, email, phone
   - Add DOB, gender, blood group, marital status
   - Required fields: name, email, phone

   **Step 3: Contact Details**
   - Emergency contact (required)
   - Current and permanent address
   - City, state, pincode

   **Step 4: Employment Details**
   - Designation, department, division
   - Grade level, work location, office room
   - Extension number

   **Step 5: Education & Skills**
   - Highest degree, specialization
   - Technical skills (comma-separated)
   - Years of experience
   - (Optional step - can be completed later)

4. **Complete & Access Application**
   - After step 5, click "Complete Setup"
   - System marks `onboarding_completed = true`
   - Redirects to main dashboard
   - Full access granted

---

## Implementation Steps

### Already Completed ✅
1. ✅ Database migration (onboarding fields added)
2. ✅ Backend API endpoints created
3. ✅ OnboardingFlow component created
4. ✅ SuperAdminPanel component created
5. ✅ Main app.tsx updated to check onboarding status

### To Integrate

#### 1. Add SuperAdmin Access
Add SuperAdminPanel to your navigation based on user role:

**Option A: Add to Settings**
```typescript
// In ComprehensiveSettings.tsx
import SuperAdminPanel from './SuperAdminPanel';

// Add admin tab if user is superadmin
{user?.role === 'superadmin' && (
  <div>
    {activeTab === "admin" && <SuperAdminPanel />}
  </div>
)}
```

**Option B: Create Dedicated Route**
```typescript
// Create app/admin/page.tsx
import SuperAdminPanel from '@/components/SuperAdminPanel';

export default function AdminPage() {
  return <SuperAdminPanel />;
}
```

#### 2. Update Sidebar Navigation
```typescript
// In Sidebar.tsx
{user?.role === 'superadmin' && (
  <button
    onClick={() => setCurrentPage('admin')}
    className="nav-item"
  >
    <Users className="w-5 h-5" />
    Admin Panel
  </button>
)}
```

#### 3. Test the Flow

**Create First SuperAdmin**:
```bash
# Run this SQL to make existing user superadmin
UPDATE users 
SET role = 'superadmin', 
    onboarding_completed = TRUE,
    is_first_login = FALSE,
    must_change_password = FALSE
WHERE email = 'your-email@example.com';
```

**Test Employee Creation**:
1. Login as superadmin
2. Go to Admin Panel
3. Create test employee
4. Copy credentials
5. Logout
6. Login with employee credentials
7. Complete onboarding flow

---

## Security Features

1. **Password Requirements**
   - Minimum 6 characters
   - Must be changed on first login
   - Bcrypt hashing

2. **Data Validation**
   - Required fields checked at each step
   - Email format validation
   - Step-by-step progression (cannot skip)

3. **Access Control**
   - Unauthenticated users → Login page
   - Incomplete onboarding → Onboarding flow
   - Complete onboarding → Full application access

4. **Temporary Credentials**
   - Temp password stored for reference
   - Cleared after first password change
   - Cannot reuse temp password

---

## API Testing

### Test Employee Creation
```bash
curl -X POST http://localhost:8000/api/admin/create-employee \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Employee",
    "email": "test@example.com",
    "designation": "Scientist B",
    "establishment": "DRDO HQ",
    "department": "AI Research",
    "temp_password": "Welcome@2024"
  }'
```

### Check Onboarding Status
```bash
curl "http://localhost:8000/api/auth/check-onboarding?user_id=5"
```

### List All Employees
```bash
curl "http://localhost:8000/api/admin/employees"
```

---

## Profile Completion Tracking

The system automatically tracks profile completion:

```json
{
  "overall": 45,
  "sections": {
    "personal": { "filled": 4, "total": 6, "percentage": 67 },
    "contact": { "filled": 3, "total": 6, "percentage": 50 },
    "employment": { "filled": 5, "total": 5, "percentage": 100 },
    "education": { "filled": 0, "total": 3, "percentage": 0 },
    "skills": { "filled": 1, "total": 3, "percentage": 33 },
    "financial": { "filled": 0, "total": 4, "percentage": 0 }
  }
}
```

This appears in:
- Onboarding flow progress
- Settings overview dashboard
- Admin panel employee list

---

## Customization Options

### 1. Change Required Fields
Edit validation in `OnboardingFlow.tsx`:
```typescript
case 1: // Personal Info
  if (!personalData.name || !personalData.email || !personalData.phone) {
    showMessage("error", "Please fill all required fields");
    return false;
  }
```

### 2. Add More Steps
Add new step object to `steps` array:
```typescript
{
  id: 5,
  title: "Documents",
  description: "Upload required documents",
  icon: FileText,
  fields: ["resume", "certificates"]
}
```

### 3. Custom Password Generation
In `SuperAdminPanel.tsx`:
```typescript
const generatePassword = () => {
  // Custom logic here
  const password = `YourPattern${Math.random()}`;
  setFormData({ ...formData, temp_password: password });
};
```

### 4. Email Notifications
Add email service integration:
```python
# In apex_backend.py after employee creation
send_welcome_email(
    to=data['email'],
    name=data['name'],
    temp_password=temp_password,
    employee_id=employee['employee_id']
)
```

---

## Troubleshooting

### Issue: Onboarding doesn't show
**Solution**: Check database fields exist:
```sql
SELECT onboarding_completed, onboarding_step, must_change_password 
FROM users WHERE id = YOUR_USER_ID;
```

### Issue: Can't create employee
**Solution**: Check backend logs and verify:
- Database connection working
- All required fields provided
- Email not already registered

### Issue: Onboarding stuck on step
**Solution**: Update step manually:
```sql
UPDATE users 
SET onboarding_step = 0 
WHERE id = YOUR_USER_ID;
```

---

## Next Enhancements

1. **Email Integration**: Auto-send credentials to new employees
2. **Bulk Import**: CSV import for multiple employees
3. **Role Permissions**: Fine-grained access control
4. **Audit Logging**: Track all admin actions
5. **Password Policies**: Enforce complexity rules
6. **Account Expiry**: Temp password expiration
7. **Profile Photos**: Upload during onboarding
8. **Document Upload**: Store certificates, IDs, etc.

---

## Summary

✅ **SuperAdmin** can create employees with temporary credentials
✅ **Employees** must complete 5-step onboarding on first login
✅ **Access restricted** until profile completion
✅ **All data** auto-saved and validated
✅ **Profile tracking** shows completion percentage
✅ **Secure** password management with bcrypt
✅ **Smooth UX** with animations and progress indicators

The system is now production-ready for organizational employee management! 🎉
