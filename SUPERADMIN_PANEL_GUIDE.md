# SuperAdmin Panel - Complete Guide

## Overview

The SuperAdmin Panel is a dedicated administrative dashboard that provides comprehensive user management capabilities. It's a separate, secure interface accessible only to users with the `superadmin` role.

## Features

### 1. Dashboard View
- **Statistics Cards**:
  - Total Users: Count of all registered users
  - Active Users: Number of currently active users
  - Pending Onboarding: Users who haven't completed profile setup
  - New This Month: Users created in the current month

- **Quick Actions**:
  - Create New User
  - Manage Users
  - Export Data

- **Recent Activity**:
  - List of 5 most recently created users
  - Quick status overview (Complete/Pending)

### 2. User Management View

#### User List Table
Comprehensive table with the following columns:
- **User**: Avatar, name, and email
- **Employee ID**: Unique identifier
- **Role**: User role (user, admin, manager, superadmin)
- **Department**: Department assignment
- **Onboarding**: Completion status
- **Status**: Active/Inactive indicator
- **Actions**: Dropdown menu with options

#### Filtering & Search
- **Search Bar**: Search by name, email, or employee ID
- **Role Filter**: Filter by role (All, User, Admin, Manager, SuperAdmin)
- **Status Filter**: Filter by status (All, Active, Inactive, Pending Onboarding)

#### User Actions Menu
For each user, the following actions are available:
1. **View Profile**: Complete user profile with all details
2. **Enable/Disable**: Toggle user active status
3. **Reset Password**: Generate new temporary password
4. **Delete User**: Permanently remove user (with confirmation)

### 3. Create User View

#### Form Fields
- **Full Name*** (Required)
- **Email*** (Required)
- **Designation*** (Required)
- **Department** (Optional)
- **Establishment*** (Required)
- **Role** (Dropdown: User, Admin, Manager)
- **Temporary Password*** (Required)

#### Password Generation
- **Auto-Generate Button**: Creates secure password (Welcome@XXXX format)
- **Manual Entry**: Can enter custom password
- **Show/Hide Toggle**: View password as text or hidden
- **Important Note**: User must change password on first login

## Access Control

### Route Protection
- **URL**: `/admin`
- **Access**: Only users with `role = 'superadmin'`
- **Redirects**:
  - Not logged in → Redirect to `/login`
  - Non-superadmin → Redirect to `/` (dashboard)
  - Superadmin → Show AdminPage

### Navigation Integration
- **Sidebar**: "Admin Panel" menu item appears only for superadmin users
- **Icon**: Shield icon (🛡️)
- **Position**: Second-to-last in navigation (before Settings)

## API Endpoints

### 1. List All Users
```http
GET /api/admin/users/list
```
**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "employee_id": "EMP001",
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+91-9876543210",
      "designation": "Senior Scientist",
      "department": "R&D",
      "division": "Electronics",
      "establishment": "DRDO Delhi",
      "role": "user",
      "is_active": true,
      "onboarding_completed": true,
      "onboarding_step": 5,
      "created_by_admin": true,
      "created_at": "2024-01-15T10:30:00Z",
      "last_login": "2024-01-20T14:20:00Z"
    }
  ],
  "count": 1
}
```

### 2. Get Dashboard Statistics
```http
GET /api/admin/stats
```
**Response:**
```json
{
  "totalUsers": 15,
  "activeUsers": 12,
  "onboardingPending": 3,
  "newThisMonth": 5
}
```

### 3. Create Employee
```http
POST /api/admin/create-employee
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "designation": "Scientist",
  "department": "R&D",
  "establishment": "DRDO Mumbai",
  "role": "user",
  "temp_password": "Welcome@2024"
}
```

### 4. Update User
```http
PUT /api/admin/users/{user_id}
Content-Type: application/json

{
  "name": "John Updated",
  "designation": "Senior Scientist",
  "is_active": false
}
```
**Updatable Fields:**
- name, email, phone, designation, department, division
- establishment, role, is_active, employee_id
- grade_level, date_of_birth, gender

### 5. Delete User
```http
DELETE /api/admin/users/{user_id}
```
**Protection**: Cannot delete superadmin users

### 6. Reset Password
```http
POST /api/admin/users/{user_id}/reset-password
Content-Type: application/json

{
  "new_password": "Reset@1234"
}
```
**Behavior:**
- Hashes and stores new password
- Saves temp_password (plain text for admin reference)
- Sets must_change_password = TRUE
- User forced to change on next login

## User Workflows

### Workflow 1: Create New Employee
1. SuperAdmin clicks "Create User" button or navigates to Create view
2. Fills out form:
   - Enter name, email, designation, establishment
   - Select department (optional)
   - Select role (User/Admin/Manager)
3. Click "Generate Password" button (or enter manually)
4. Click "Create User"
5. Success message displays with confirmation
6. User appears in Users list with "Pending Onboarding" status
7. **Share credentials** with employee:
   - Employee ID (auto-generated)
   - Email
   - Temporary password

### Workflow 2: View User Profile
1. Navigate to Users tab
2. Click three-dot menu (⋮) on user row
3. Select "View Profile"
4. Modal displays with 4 sections:
   - **Personal Information**: Name, email, phone, DOB, gender, blood group
   - **Employment Details**: Employee ID, designation, department, division, establishment, grade
   - **Contact Information**: Emergency contact, phone, city, state
   - **Account Status**: Active/Inactive, role, onboarding status, last login

### Workflow 3: Disable/Enable User
1. Navigate to Users tab
2. Click three-dot menu (⋮) on user row
3. Select "Disable" (if active) or "Enable" (if inactive)
4. System immediately updates user status
5. Success message confirms action
6. User list refreshes showing updated status

### Workflow 4: Reset User Password
1. Navigate to Users tab
2. Click three-dot menu (⋮) on user row
3. Select "Reset Password"
4. Confirmation modal appears
5. Click "Reset Password"
6. System generates new temporary password (Reset@XXXX format)
7. Success message displays new password
8. **Important**: Copy and share new password with user
9. User must change password on next login

### Workflow 5: Delete User
1. Navigate to Users tab
2. Click three-dot menu (⋮) on user row
3. Select "Delete User"
4. Confirmation modal appears with warning
5. Click "Delete User" to confirm
6. System permanently deletes user and all data
7. Success message confirms deletion
8. User removed from list

### Workflow 6: Search and Filter Users
1. Navigate to Users tab
2. **Search**:
   - Type in search bar
   - Searches name, email, employee ID
   - Results update in real-time
3. **Filter by Role**:
   - Select from dropdown (All, User, Admin, Manager, SuperAdmin)
   - Table updates to show only matching users
4. **Filter by Status**:
   - Select from dropdown (All, Active, Inactive, Pending Onboarding)
   - Table updates accordingly
5. Filters can be combined for precise results

## Security Features

### 1. Access Control
- Route-level protection with role verification
- Automatic redirect for unauthorized access
- No UI elements visible to non-superadmin users

### 2. Data Protection
- Cannot delete superadmin users (prevents lockout)
- Password hashing using bcrypt
- Temporary passwords stored separately for admin reference
- JWT-based authentication

### 3. Audit Trail
- Created_at timestamps for all users
- Created_by_admin flag tracks admin-created accounts
- Last_login tracking
- Onboarding timestamp tracking

## Database Schema

### New Fields Added
The following fields support the SuperAdmin functionality:

```sql
-- User management fields
is_active BOOLEAN DEFAULT TRUE
created_by_admin BOOLEAN DEFAULT FALSE
created_at TIMESTAMP DEFAULT NOW()
updated_at TIMESTAMP DEFAULT NOW()
last_login TIMESTAMP

-- Onboarding tracking fields
onboarding_completed BOOLEAN DEFAULT FALSE
onboarding_step INTEGER DEFAULT 0
onboarding_started_at TIMESTAMP
onboarding_completed_at TIMESTAMP
is_first_login BOOLEAN DEFAULT TRUE
must_change_password BOOLEAN DEFAULT TRUE
temp_password VARCHAR(255)
```

## UI Components

### 1. SuperAdminDashboard.tsx
**Location**: `components/SuperAdminDashboard.tsx`
**Lines**: ~1000
**Features**:
- Three main views: Dashboard, Users, Create
- Statistics cards with real-time data
- Sortable, filterable user table
- Create user form with validation
- User profile modal
- Password reset modal
- Delete confirmation modal
- Success/error notifications
- Loading states
- Responsive design
- Dark mode support

### 2. AdminPage.tsx
**Location**: `app/admin/page.tsx`
**Lines**: ~50
**Features**:
- Route protection
- Role verification
- Loading state
- Access denied screen
- Auto-redirect for unauthorized users

### 3. Sidebar Integration
**Location**: `components/Sidebar.tsx`
**Changes**:
- Dynamic navigation based on user role
- Shield icon for Admin Panel
- Conditional rendering for superadmin
- Next.js router integration for navigation

## Testing Guide

### 1. Access Control Testing
```bash
# Test 1: Non-logged in user
1. Navigate to http://localhost:3000/admin
2. Should redirect to /login

# Test 2: Regular user
1. Login as regular user (role != 'superadmin')
2. Navigate to /admin
3. Should redirect to /
4. Sidebar should NOT show "Admin Panel"

# Test 3: SuperAdmin user
1. Login as superadmin
2. Navigate to /admin or click "Admin Panel" in sidebar
3. Should see SuperAdmin Dashboard
```

### 2. User Management Testing
```bash
# Test 1: Create User
curl -X POST http://localhost:8000/api/admin/create-employee \
-H "Content-Type: application/json" \
-d '{
  "name": "Test User",
  "email": "test@example.com",
  "designation": "Scientist",
  "establishment": "DRDO Delhi",
  "role": "user",
  "temp_password": "Welcome@2024"
}'

# Test 2: List Users
curl http://localhost:8000/api/admin/users/list

# Test 3: Update User
curl -X PUT http://localhost:8000/api/admin/users/1 \
-H "Content-Type: application/json" \
-d '{"is_active": false}'

# Test 4: Reset Password
curl -X POST http://localhost:8000/api/admin/users/1/reset-password \
-H "Content-Type: application/json" \
-d '{"new_password": "Reset@2024"}'

# Test 5: Delete User
curl -X DELETE http://localhost:8000/api/admin/users/1
```

### 3. UI Testing Checklist
- [ ] Dashboard statistics load correctly
- [ ] User table displays all users
- [ ] Search filters users in real-time
- [ ] Role filter works correctly
- [ ] Status filter works correctly
- [ ] Create user form validates required fields
- [ ] Password generator creates secure passwords
- [ ] View profile shows all user data
- [ ] Enable/Disable toggles user status
- [ ] Reset password generates new password
- [ ] Delete user shows confirmation modal
- [ ] Success/error messages display properly
- [ ] Loading states show during API calls
- [ ] Responsive design works on mobile
- [ ] Dark mode styling correct

## Troubleshooting

### Issue 1: "Admin Panel" not showing in sidebar
**Cause**: User role is not 'superadmin'
**Solution**:
1. Check user role in database:
   ```sql
   SELECT id, name, email, role FROM users WHERE email = 'your-email@example.com';
   ```
2. Update role if needed:
   ```sql
   UPDATE users SET role = 'superadmin' WHERE email = 'your-email@example.com';
   ```
3. Logout and login again

### Issue 2: Access denied when navigating to /admin
**Cause**: Auth context not updated or user not logged in
**Solution**:
1. Check browser console for errors
2. Verify JWT token in localStorage
3. Logout and login again
4. Check network tab for auth API response

### Issue 3: Users not loading in table
**Cause**: Backend API not running or database connection issue
**Solution**:
1. Check backend server is running on port 8000
2. Check browser console for API errors
3. Test API endpoint directly:
   ```bash
   curl http://localhost:8000/api/admin/users/list
   ```
4. Check database connection in apex_backend.py

### Issue 4: Cannot delete superadmin user
**Cause**: Protection mechanism to prevent lockout
**Solution**: This is intentional. Cannot delete users with role='superadmin'

### Issue 5: Password reset not working
**Cause**: bcrypt import or password hashing issue
**Solution**:
1. Check apex_backend.py has bcrypt imported
2. Verify password hashing function:
   ```python
   import bcrypt
   hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
   ```

## Best Practices

### 1. User Creation
- Always generate strong passwords (use auto-generate)
- Include full name and proper email
- Assign appropriate role (most users should be 'user')
- Set correct establishment for organizational structure
- Share credentials securely (email, encrypted message, etc.)

### 2. User Management
- Disable users instead of deleting when possible
- Reset passwords only when necessary
- Regularly review active users
- Monitor onboarding completion rates
- Export user data periodically for backup

### 3. Security
- Never share superadmin credentials
- Limit superadmin role to 1-2 trusted individuals
- Regularly audit user access logs
- Review and remove inactive users
- Ensure all users complete onboarding

### 4. Performance
- Use filters to reduce table size for large user lists
- Export data in batches for large datasets
- Monitor API response times
- Index database tables for faster queries

## Future Enhancements

### Planned Features
1. **Bulk Operations**:
   - CSV import for multiple users
   - Bulk enable/disable
   - Bulk role assignment

2. **Advanced Analytics**:
   - User activity charts
   - Login frequency graphs
   - Department-wise distribution
   - Onboarding completion trends

3. **Audit Logging**:
   - Track all admin actions
   - Log user modifications
   - Export audit reports

4. **Email Integration**:
   - Automated credential emails
   - Password reset emails
   - Welcome emails for new users

5. **Advanced Filters**:
   - Date range filters
   - Custom field filters
   - Saved filter presets

6. **Role Management**:
   - Custom roles
   - Permission matrix
   - Role-based access control

## Support

For issues or questions:
1. Check this documentation
2. Review Troubleshooting section
3. Check API logs in terminal
4. Inspect browser console for errors
5. Verify database connection and data

## Summary

The SuperAdmin Panel provides a complete, secure, and user-friendly interface for managing all users in the APEX system. With comprehensive features for creating, viewing, editing, and deleting users, along with powerful filtering and search capabilities, it enables efficient administration of the entire user base.

Key capabilities:
- ✅ Create users with temporary credentials
- ✅ View complete user profiles
- ✅ Enable/disable user access
- ✅ Reset passwords
- ✅ Delete users (with protection)
- ✅ Search and filter users
- ✅ Dashboard statistics
- ✅ Role-based access control
- ✅ Responsive design
- ✅ Dark mode support

The system is production-ready and fully integrated with the existing APEX application.
