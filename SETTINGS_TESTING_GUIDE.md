# Settings Page - Quick Testing Guide

## Access the Settings Page

1. **Open your browser**: http://localhost:3000
2. **Login** (if not already logged in):
   - Email: `admin@drdo.gov.in`
   - Password: `admin123`
3. **Navigate to Settings**: Click "Settings" in the sidebar

## Testing Checklist

### ✅ Profile Tab

**What to test**:
1. Check that your profile data loads automatically:
   - Name: "DRDO Admin Updated" (or current name)
   - Email: "admin@drdo.gov.in"
   - Designation: "Senior Administrator" (or current)
   - Establishment: "Delhi HQ"

2. **Update Profile**:
   - Change your name to something new
   - Click "Save Changes"
   - Look for green success message: "Profile updated successfully!"
   - Refresh the page - changes should persist

3. **View Activity Stats**:
   - Check the three stat cards show real numbers:
     - Total Wishes: (your actual count)
     - Feedback Submitted: (your actual count)
     - Knowledge Queries: (your actual count)
   - Verify "Member since" date is correct

**Expected Behavior**:
- ✅ Form fields populated on load
- ✅ Save button shows "Saving..." during request
- ✅ Success message appears and auto-dismisses
- ✅ Stats cards show accurate numbers
- ✅ Data persists after page refresh

---

### 🔒 Security Tab

**What to test**:
1. Click "Change Password" button
2. Modal should open with three fields:
   - Current Password
   - New Password
   - Confirm New Password

3. **Test Password Change**:
   - Enter current password: `admin123`
   - Enter new password: `newpass123`
   - Confirm new password: `newpass123`
   - Click "Change Password"
   - Look for success message

4. **Test Password Show/Hide**:
   - Click eye icons to toggle password visibility
   - Each field should have independent toggle

5. **Test Validation**:
   - Try mismatched passwords → Error: "New passwords don't match"
   - Try password less than 6 chars → Error: "Password must be at least 6 characters"
   - Try wrong current password → Error: "Current password is incorrect"

**Expected Behavior**:
- ✅ Modal opens with backdrop blur
- ✅ Show/hide toggles work for each field
- ✅ Validation errors show as red messages
- ✅ Success closes modal and shows green message
- ✅ Cancel button closes modal without changes

---

### 🔔 Notifications Tab

**What to test**:
1. View all 6 notification toggles:
   - Expert Responses (default: ON)
   - Wish Reminders (default: ON)
   - Weekly Checkins (default: ON)
   - Community Updates (default: OFF)
   - Emergency Alerts (default: ON)
   - Voice Confirmations (default: ON)

2. **Toggle notifications**:
   - Click any toggle switch
   - Watch it flip immediately
   - See success message: "Notification settings updated"
   - Refresh page - toggle state should persist

**Expected Behavior**:
- ✅ All toggles show correct initial state
- ✅ Clicking toggle flips it instantly
- ✅ Success message appears on each change
- ✅ Settings persist after page refresh
- ✅ No need to click "Save" button

---

### 💾 Data & Privacy Tab

**What to test**:
1. **Export Data**:
   - Click "Export My Data" button
   - Button shows "Exporting..." during request
   - JSON file downloads automatically
   - Filename format: `apex-data-export-2025-11-23.json`

2. **Verify Export Contents**:
   - Open the downloaded JSON file
   - Check it contains:
     ```json
     {
       "user": { "name": "...", "email": "..." },
       "wishes": [ ... ],
       "feedback": [ ... ],
       "knowledge_queries": [ ... ],
       "export_date": "2025-11-23T23:30:14.326657"
     }
     ```

3. **Privacy Information**:
   - Read the blue privacy notice
   - Verify it mentions encryption and security

**Expected Behavior**:
- ✅ Export button triggers download
- ✅ File downloads without page refresh
- ✅ JSON is properly formatted
- ✅ All user data included in export
- ✅ Success message appears after download

---

## Visual Indicators

### Success Messages (Green)
```
✓ Profile updated successfully!
✓ Password changed successfully!
✓ Notification settings updated
✓ Data exported successfully!
```

### Error Messages (Red)
```
✗ Current password is incorrect
✗ New passwords don't match
✗ Failed to update profile
```

### Loading States
```
Saving...
Changing...
Exporting...
```

---

## Browser Console Testing

Open Developer Tools (F12) and check:

1. **Network Tab**:
   - Profile update: `PUT /api/settings/profile` → 200
   - Password change: `PUT /api/settings/password` → 200
   - Notifications: `PUT /api/settings/notifications` → 200
   - Export: `GET /api/settings/export` → 200

2. **Console Tab**:
   - No errors related to Settings component
   - API calls logged successfully

---

## Common Issues & Fixes

### Profile doesn't load
- **Check**: Is backend running on port 8000?
- **Fix**: Run `python apex_backend.py`

### Changes don't persist
- **Check**: Is database running?
- **Fix**: Run `docker start shakti-db`

### Export downloads empty file
- **Check**: Do you have any wishes/feedback created?
- **Fix**: Create some test data first

### Password change fails
- **Check**: Are you using the correct current password?
- **Fix**: Try login credentials: `admin123`

---

## Quick API Test (Command Line)

Test all endpoints manually:

```powershell
# Test profile GET
curl http://localhost:8000/api/settings/profile?user_id=3

# Test profile UPDATE
curl -X PUT http://localhost:8000/api/settings/profile `
  -H "Content-Type: application/json" `
  -d '{"user_id":3,"name":"Test Name","email":"admin@drdo.gov.in"}'

# Test notifications GET
curl http://localhost:8000/api/settings/notifications?user_id=3

# Test stats GET
curl http://localhost:8000/api/settings/stats?user_id=3

# Test export GET
curl http://localhost:8000/api/settings/export?user_id=3
```

---

## Success Criteria ✅

**Settings page is working correctly when**:
- ✅ All 4 tabs render without errors
- ✅ Profile data loads from database
- ✅ Profile updates save and persist
- ✅ Password change works with validation
- ✅ Notification toggles save instantly
- ✅ Activity stats show real numbers
- ✅ Data export downloads complete JSON
- ✅ Success/error messages display properly
- ✅ All loading states show during API calls
- ✅ Dark mode styling works correctly

---

## Next: What to Test

After verifying Settings works:

1. **Dashboard**: Check if stats still load correctly
2. **Wishes Vault**: Create/edit/delete wishes
3. **Feedback**: Submit feedback
4. **Logout/Login**: Test with updated password
5. **Create new user**: Test Settings with fresh account

---

## Need Help?

- Backend logs: Check terminal running `apex_backend.py`
- Frontend logs: Check terminal running `npm run dev`
- Database: `docker logs shakti-db`
- Full test: Run `python test_settings_api.py`
