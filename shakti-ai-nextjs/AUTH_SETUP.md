# SHAKTI-AI Authentication Setup

## 🎯 Quick Fix for Login Issues

Your login wasn't working because:
1. **Missing `/me` API route** - Now fixed ✅
2. **Missing `/logout` API route** - Now fixed ✅  
3. **Missing users table** - Now auto-created ✅
4. **Poor error handling** - Now improved ✅

## 🚀 Quick Start

### Option 1: Windows Batch File
```cmd
cd shakti-ai-nextjs
start-dev.bat
```

### Option 2: PowerShell Script  
```powershell
cd shakti-ai-nextjs
.\start-dev.ps1
```

### Option 3: Manual Setup
```bash
cd shakti-ai-nextjs
npm install
npm run init-db
npm run dev
```

## 🧪 Test Login

Once the server is running, use these credentials:
- **Email:** `test@example.com`
- **Password:** `test123`

## 🔧 What Was Fixed

### 1. API Routes Completed
- ✅ `/api/auth/login` - Working
- ✅ `/api/auth/register` - Working  
- ✅ `/api/auth/me` - **FIXED** (was empty)
- ✅ `/api/auth/logout` - **FIXED** (was empty)

### 2. Database Setup
- ✅ Auto-creates `users` table
- ✅ Creates test user automatically
- ✅ Proper password hashing

### 3. Better Error Handling
- ✅ Loading states in UI
- ✅ Error messages shown to user
- ✅ Console logging for debugging
- ✅ Form validation

### 4. Environment Variables
- ✅ JWT secret in `.env.local`
- ✅ Database credentials updated

## 🐛 If Login Still Doesn't Work

1. **Check the browser console** (F12) for error messages
2. **Verify PostgreSQL is running**
3. **Check database credentials in `.env.local`**
4. **Run database initialization manually:**
   ```bash
   npm run init-db
   ```

## 🔐 Authentication Flow

1. User fills login form
2. Frontend sends POST to `/api/auth/login`
3. Backend verifies credentials
4. JWT token saved in httpOnly cookie
5. User state updated in React context
6. App shows authenticated interface

## 🛠️ Troubleshooting

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -h localhost -U postgres -d shakti_ai_db
```

### Reset Test User
```sql
DELETE FROM users WHERE email = 'test@example.com';
```
Then run `npm run init-db` again.

### Clear Browser Data
- Clear cookies and localStorage
- Hard refresh (Ctrl+Shift+R)

## 📝 Environment Setup

Make sure your `.env.local` has:
```env
DB_HOST=localhost
DB_NAME=shakti_ai_db  
DB_USER=postgres
DB_PASSWORD=Anjo@024
DB_PORT=5432
JWT_SECRET=your-super-secret-key-change-this-in-production
```

---

**🎉 Your authentication should now work perfectly!**
