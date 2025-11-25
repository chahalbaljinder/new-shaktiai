# 🌟 SHAKTI-AI: Advanced HR & Employee Wellness Platform

> **A comprehensive AI-powered platform for DRDO employees with policy assistance, grievance management, and intelligent support systems**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2%2B-black.svg)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12%2B-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

SHAKTI-AI is an advanced HR and employee wellness platform designed specifically for DRDO employees. It combines AI-powered policy assistance (APEX RAG system), comprehensive grievance management, secure wishes vault, employee onboarding, and real-time analytics. Built with Next.js frontend, Flask backend, and PostgreSQL database.

## ✨ Key Features

### 🤖 **APEX RAG System (Policy Queries)**
- **AI-Powered Policy Assistance**: Three specialized AI agents
  - **Athena**: Legal/Policy expert (POSH, leave, maternity, transfer)
  - **Asha**: Wellness and mental health support
  - **Scribe**: Document and application generation
- **Smart Query Processing**: Category-based routing with RAG (Retrieval Augmented Generation)
- **Query History**: Track all policy questions with timestamps and responses
- **Application Generation**: Auto-generate maternity leave, CCL, transfer, grievance applications
- **Document Download**: Export applications in DOC format
- **Markdown Formatting**: Rich text responses with proper formatting

### 📋 **Comprehensive Grievance & Feedback System**
- **Multi-Type Support**: Feedback, Grievances, and Complaints
- **Status Tracking**: Real-time status updates (Submitted, Under Review, In Progress, Resolved)
- **Priority Levels**: Low, Medium, High, Urgent, Critical
- **Anonymous Submissions**: Privacy-protected feedback option
- **Admin Dashboard**: Centralized grievance management
- **Response System**: Track admin responses and resolutions
- **Search & Filter**: Advanced filtering by type, status, and category

### 👥 **Employee Management & Onboarding**
- **Multi-Step Onboarding**: Interactive 5-step employee onboarding
  - Step 1: Welcome & Profile Setup
  - Step 2: Personal Information
  - Step 3: Contact Details
  - Step 4: Education & Skills
  - Step 5: Completion & Dashboard Tour
- **Password Management**: Mandatory password change on first login
- **Profile Completion**: Track profile completion percentage
- **Comprehensive Settings**: 8 detailed settings sections
  - Personal Information (with Aadhar/PAN masking)
  - Contact Information (with emergency contacts)
  - Employment Details
  - Educational Qualifications
  - Skills & Expertise
  - Financial Details (bank info with masking)
  - Leave & Attendance
  - Performance & Training

### 🔐 **Superadmin Panel**
- **User Management**: Create, edit, delete employees
- **Bulk Operations**: Create multiple employees with temp credentials
- **Password Reset**: Admin-controlled password resets
- **Activity Monitoring**: Track onboarding status and user activity
- **Dashboard Statistics**: Real-time user metrics
- **Role-Based Access**: Superadmin, Admin, User roles

### 🔒 **Secure Wishes Vault**
- PostgreSQL-backed encrypted storage
- Contact management for trusted individuals
- Email and WhatsApp sharing capabilities
- Sharing history and preferences tracking
- Military-grade encryption (Fernet)

### 📊 **Analytics Dashboard**
- **Real-Time Stats**: Total users, queries, active sessions, agents running
- **Recent Queries**: Latest knowledge base queries with response times
- **Personnel Distribution**: User distribution by establishment
- **Feedback Stats**: Total feedback, complaints, pending, resolved
- **Visual Indicators**: Color-coded status badges and progress indicators

## 🏗️ Project Structure

```
shakti-ai/
├── 🌐 shakti-ai-nextjs/          # Next.js Frontend Application
│   ├── app/                      # Next.js 14 app directory
│   │   ├── page.tsx             # Main dashboard page
│   │   ├── layout.tsx           # Root layout
│   │   └── globals.css          # Global styles
│   ├── components/              # React components
│   │   ├── Dashboard.tsx        # Main dashboard
│   │   ├── Sidebar.tsx          # Navigation sidebar
│   │   ├── Login.tsx            # Authentication
│   │   ├── Onboarding.tsx       # Employee onboarding flow
│   │   ├── PolicyQueries.tsx    # APEX policy assistant
│   │   ├── GrievanceDashboard.tsx  # Grievance management
│   │   ├── SuperAdminPanel.tsx  # Admin panel
│   │   ├── Settings.tsx         # Employee settings
│   │   └── WishesVault.tsx      # Wishes management
│   ├── package.json             # Node dependencies
│   └── tailwind.config.ts       # Tailwind CSS config
│
├── 🔧 Backend (Flask API)
│   ├── apex_backend.py          # Main Flask API server
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Environment variables
│   └── Procfile                 # Deployment config
│
├── 🧠 core/                      # AI & Agent System
│   ├── apex_crew.py             # APEX RAG system with 3 agents
│   ├── agents.py                # AI agent definitions
│   ├── crew.py                  # CrewAI configuration
│   ├── llm.py                   # Gemini LLM integration
│   └── get_voice_input.py       # Voice input handling
│
├── 🗄️ database/                  # Database Management
│   ├── db_config.py             # PostgreSQL configuration
│   ├── create_database.py       # Main database setup
│   ├── create_apex_tables.py    # APEX system tables
│   ├── create_policy_queries_table.py  # Policy queries table
│   ├── wishes_vault_db.py       # Wishes vault implementation
│   ├── feedback_system.py       # Feedback/Grievance tables
│   ├── enhance_user_profile.py  # Extended user fields
│   └── db_wishes.key           # Encryption key
│
├── 📚 knowledge_base/           # APEX Knowledge Base
│   ├── document_processor.py    # PDF processing
│   ├── kb_manager.py           # Knowledge base manager
│   ├── retriever.py            # Document retrieval
│   ├── vector_store.py         # FAISS vector storage
│   ├── raw_pdfs/               # Source PDFs by agent
│   │   ├── athena/             # Legal/Policy documents
│   │   ├── asha/               # Wellness documents
│   │   └── scribe/             # Template documents
│   ├── processed/              # Processed vector stores
│   └── metadata/               # Document metadata
│
├── 📄 Documentation
│   ├── README.md               # This file
│   ├── APEX_OVERVIEW.md        # APEX system overview
│   ├── APEX_KNOWLEDGE_BASE_GUIDE.md  # Knowledge base guide
│   ├── POLICY_QUERIES_SYSTEM_GUIDE.md  # Policy queries guide
│   ├── COMPREHENSIVE_EMPLOYEE_SYSTEM.md  # Employee management
│   ├── ONBOARDING_SYSTEM_GUIDE.md  # Onboarding documentation
│   ├── FEEDBACK_SYSTEM_TESTING_GUIDE.md  # Feedback system
│   ├── SUPERADMIN_PANEL_GUIDE.md  # Admin panel guide
│   ├── SETTINGS_COMPLETE.md    # Settings system
│   ├── DEPLOYMENT_GUIDE.md     # Deployment instructions
│   └── RAILWAY_DEPLOYMENT.md   # Railway.app deployment
│
├── 🧪 tests/                    # Testing Scripts
│   ├── test_apex_rag.py        # Test APEX system
│   ├── test_apex_agents.py     # Test individual agents
│   ├── test_backend.py         # Test Flask API
│   ├── test_onboarding.py      # Test onboarding flow
│   └── test_settings_api.py    # Test settings endpoints
│
├── 🐳 Docker Configuration
│   ├── Dockerfile              # Backend container
│   ├── docker-compose.yml      # Multi-container setup
│   └── .dockerignore          # Docker exclusions
│
└── 🛠️ Scripts & Utilities
    ├── create_superadmin.py    # Create superadmin user
    ├── create_apex_rag.py      # Initialize APEX knowledge base
    ├── setup_apex_knowledge_base.py  # Setup knowledge base
    ├── start-backend.bat       # Windows backend launcher
    └── start-full-app.bat      # Full stack launcher
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 18+ and npm
- **Python** 3.8+
- **PostgreSQL** 12+
- **Git**

### 1️⃣ Clone Repository
```bash
git clone <repository-url>
cd shakti-ai
```

### 2️⃣ Setup Backend

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Setup PostgreSQL Database
```bash
# Create database
createdb -U postgres shakti_ai_db

# Run all database setup scripts
python database/create_database.py
python database/create_apex_tables.py
python database/create_policy_queries_table.py
python database/feedback_system.py
python database/enhance_user_profile.py

# Create superadmin user
python create_superadmin.py
```

#### Configure Environment
```bash
# Create .env file with:
DB_HOST=localhost
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# JWT Configuration
JWT_SECRET=your-secret-key-change-in-production

# API Keys
GOOGLE_API_KEY=your_gemini_api_key
```

#### Initialize APEX Knowledge Base (Optional)
```bash
# Add PDFs to knowledge_base/raw_pdfs/athena/, asha/, scribe/
# Then run:
python create_apex_rag.py
```

#### Start Backend Server
```bash
python apex_backend.py
# Backend runs on http://localhost:8000
```

### 3️⃣ Setup Frontend

#### Install Node Dependencies
```bash
cd shakti-ai-nextjs
npm install
```

#### Start Development Server
```bash
npm run dev
# Frontend runs on http://localhost:3000
```

### 4️⃣ Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health

### Default Credentials
```
Superadmin:
Email: admin@drdo.in
Password: Admin@123

Test User:
Email: priya.sharma@drdo.in
Password: Priya@123
```

## 🔧 Configuration

### Backend Environment Variables (.env)
```env
# Database Configuration
DB_HOST=localhost
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# JWT Authentication
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256

# API Keys
GOOGLE_API_KEY=your_gemini_api_key_here

# Email Configuration (Optional - for sharing features)
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Application Settings
FLASK_ENV=development
PORT=8000
```

### Frontend Configuration
Located in `shakti-ai-nextjs/`:
- API endpoint: `http://localhost:8000` (configurable in components)
- Authentication: JWT token stored in localStorage
- Dark mode support via Tailwind CSS

### Database Schema
**Main Tables:**
- `users` - Employee profiles with comprehensive fields
- `policy_queries` - APEX query history
- `feedback` - Grievances and feedback
- `wishes` - Encrypted wishes vault
- `sharing_history` - Wish sharing tracking
- `knowledge_queries` - General knowledge base queries
- `user_sessions` - Session management

### Required APIs
- **Google Gemini API**: For APEX AI agents (get from https://makersuite.google.com/app/apikey)
- **No other external APIs required** for core functionality

## 🎮 Usage Guide

### For Employees

#### 1. **Login & Onboarding**
- First-time login requires password change
- Complete 5-step onboarding process
- Set up profile, contact info, education, and skills

#### 2. **Policy Queries (APEX)**
- Navigate to "Policy Queries" from sidebar
- Select policy category (POSH, Leave, Maternity, Transfer, General)
- Ask questions in natural language
- View AI-powered responses with sources
- Check query history with timestamps
- Click any query to see full details in modal

#### 3. **Generate Applications**
- Go to "Applications" tab in Policy Queries
- Select application type:
  - Maternity Leave Application
  - Child Care Leave (CCL)
  - Transfer Request
  - Grievance Application
  - Policy Clarification Request
- Provide optional details
- Generate application with AI
- Download in DOC format

#### 4. **Submit Feedback/Grievances**
- Access "Grievance Dashboard" from sidebar
- Choose type: Feedback, Grievance, or Complaint
- Fill in details with category and priority
- Track status: Submitted → Under Review → In Progress → Resolved
- View admin responses

#### 5. **Manage Profile**
- Access "Settings" from sidebar
- Update 8 different sections:
  - Personal Information
  - Contact Information
  - Employment Details
  - Education & Qualifications
  - Skills & Expertise
  - Financial Details
  - Leave & Attendance (view only)
  - Performance & Training (view only)
- Track profile completion percentage

#### 6. **Wishes Vault**
- Store personal wishes securely
- Add trusted contacts
- Share via email or WhatsApp
- View sharing history

### For Administrators

#### **Superadmin Panel**
- Access from sidebar (superadmin role only)
- View dashboard statistics
- Create new employees with temp credentials
- Edit user details
- Reset passwords
- Delete users (except superadmin)
- Track onboarding status

#### **Manage Grievances**
- View all feedback/grievances
- Filter by type, status, category
- Update status and add responses
- Assign to team members
- Monitor resolution progress

## 🧪 Testing

### Backend API Tests
```bash
# Test APEX system
python test_apex_rag.py
python test_apex_agents.py

# Test backend endpoints
python test_backend.py

# Test onboarding flow
python test_onboarding.py

# Test settings API
python test_settings_api.py
```

### Frontend Testing
```bash
cd shakti-ai-nextjs
npm run test
npm run lint
```

### Manual Testing Checklist
- [ ] User registration and login
- [ ] Onboarding flow completion
- [ ] Policy query submission and response
- [ ] Application generation and download
- [ ] Grievance submission and tracking
- [ ] Profile updates across all sections
- [ ] Superadmin user creation
- [ ] Password change functionality
- [ ] Wishes vault creation and sharing

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication with 7-day expiry
- **Password Security**: Bcrypt hashing with salt rounds
- **Data Encryption**: Fernet encryption for sensitive wishes data
- **Data Masking**: Automatic masking of Aadhar, PAN, bank account numbers
- **SQL Injection Protection**: Parameterized queries throughout
- **CORS Configuration**: Controlled cross-origin requests
- **Session Management**: Secure session handling with database tracking
- **Role-Based Access**: Superadmin, Admin, User role separation
- **Privacy Controls**: Anonymous feedback/grievance submissions
- **Audit Trail**: Comprehensive logging of user activities

## 🛠️ Development

### Technology Stack

**Frontend:**
- Next.js 14.2.8 (React 18)
- TypeScript
- Tailwind CSS 3.4.1
- Framer Motion (animations)
- Lucide React (icons)

**Backend:**
- Flask 2.3+
- Python 3.8+
- CrewAI (multi-agent framework)
- LangChain (RAG pipeline)
- Google Gemini API (LLM)

**Database:**
- PostgreSQL 12+
- psycopg2 (Python adapter)
- FAISS (vector storage)

**AI/ML:**
- APEX RAG System (3 specialized agents)
- Gemini 2.0 Flash (language model)
- Vector embeddings with FAISS
- Document processing pipeline

### Adding New Features

#### Add New APEX Agent
1. Define agent in `core/apex_crew.py`
2. Create knowledge base folder in `knowledge_base/raw_pdfs/`
3. Add PDF documents
4. Run `python create_apex_rag.py`
5. Update agent routing in `apex_backend.py`

#### Add New API Endpoint
1. Add route in `apex_backend.py`
2. Implement JWT authentication check
3. Add database queries as needed
4. Update frontend API calls
5. Test with `test_backend.py`

#### Add New Frontend Component
1. Create component in `shakti-ai-nextjs/components/`
2. Add navigation in `Sidebar.tsx`
3. Add route case in `app/page.tsx`
4. Style with Tailwind CSS
5. Add Framer Motion animations

### Database Schema Extensions
```sql
-- Example: Add new field to users table
ALTER TABLE users ADD COLUMN new_field VARCHAR(255);

-- Create new table
CREATE TABLE new_feature (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Contributing Guidelines
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow existing code structure and naming conventions
4. Add tests for new features
5. Update documentation
6. Commit changes (`git commit -m 'Add AmazingFeature'`)
7. Push to branch (`git push origin feature/AmazingFeature`)
8. Open Pull Request

## 📊 Performance & Scalability

- **Database Optimization**: PostgreSQL with strategic indexes on frequently queried columns
- **Connection Pooling**: Efficient database connection management
- **Vector Search**: FAISS for fast semantic search (<100ms queries)
- **Caching Strategy**: Session-based caching in frontend
- **API Response Times**: <2s for APEX queries, <500ms for standard endpoints
- **Concurrent Users**: Supports 100+ simultaneous users
- **Document Processing**: Batch processing for RAG knowledge base
- **Frontend Performance**: Next.js optimizations, code splitting, lazy loading

### Scalability Considerations
- Horizontal scaling with load balancer
- Database replication for read-heavy workloads
- Redis caching layer (optional)
- CDN for static assets
- Microservices architecture ready

## 🆘 Troubleshooting

### Common Issues

**1. Database Connection Failed**
```bash
# Check PostgreSQL service
# Windows:
net start postgresql-x64-17

# Linux:
sudo systemctl status postgresql

# Verify credentials in .env file
# Test connection:
psql -U postgres -d shakti_ai_db
```

**2. APEX Not Responding**
```bash
# Test APEX initialization
python -c "from core.apex_crew import Apex; apex = Apex(); print('Success')"

# Check if knowledge base exists
ls knowledge_base/processed/

# Rebuild knowledge base if needed
python create_apex_rag.py
```

**3. Frontend Build Errors**
```bash
cd shakti-ai-nextjs
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**4. JWT Token Issues**
- Clear localStorage in browser DevTools
- Check JWT_SECRET matches between frontend and backend
- Verify token expiry (default 7 days)

**5. Missing Dependencies**
```bash
# Backend
pip install -r requirements.txt --upgrade

# Frontend
cd shakti-ai-nextjs
npm install --legacy-peer-deps
```

**6. Port Already in Use**
```bash
# Windows - Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**7. Database Migration Issues**
```bash
# Drop and recreate database (WARNING: Deletes all data)
dropdb -U postgres shakti_ai_db
createdb -U postgres shakti_ai_db
python database/create_database.py
# Run all other database setup scripts
```

## 📈 Roadmap

### Phase 1 (Completed ✅)
- [x] APEX RAG system with 3 specialized agents
- [x] Policy queries with category-based routing
- [x] Application generation and download
- [x] Comprehensive grievance management
- [x] Employee onboarding system
- [x] Superadmin panel
- [x] 8-section employee settings
- [x] Wishes vault with encryption
- [x] JWT authentication
- [x] Dashboard analytics

### Phase 2 (In Progress 🚧)
- [ ] **Mobile App**: React Native companion
- [ ] **Advanced Analytics**: User behavior insights and reporting
- [ ] **Email Notifications**: Automated grievance updates
- [ ] **Document Templates**: Pre-filled application templates
- [ ] **Bulk Operations**: Excel import/export for admin
- [ ] **Advanced Search**: Full-text search across all modules
- [ ] **Chatbot Widget**: Embedded APEX assistant

### Phase 3 (Planned 📋)
- [ ] **Multi-Language Support**: Hindi, Regional languages
- [ ] **Video Tutorials**: In-app help videos
- [ ] **Performance Reviews**: 360-degree feedback system
- [ ] **Leave Management**: Complete leave workflow
- [ ] **Attendance Tracking**: Biometric integration
- [ ] **Training Portal**: Online courses and certifications
- [ ] **Document Management**: Centralized document repository
- [ ] **Announcements**: Organization-wide broadcasting

### Phase 4 (Future 🔮)
- [ ] **AI Voice Assistant**: Voice-based APEX interaction
- [ ] **Predictive Analytics**: Employee churn prediction
- [ ] **Integration APIs**: HRMS, Payroll, Biometric systems
- [ ] **Mobile Attendance**: GPS-based check-in
- [ ] **Advanced Reporting**: Custom report builder
- [ ] **Workflow Automation**: Approval workflows
- [ ] **Knowledge Base Expansion**: More policy documents
- [ ] **Real-time Chat**: Inter-employee messaging

## 🤝 Support & Contact

### Documentation
- **Installation Guide**: See `DEPLOYMENT_GUIDE.md`
- **APEX System**: See `APEX_OVERVIEW.md` and `APEX_KNOWLEDGE_BASE_GUIDE.md`
- **Policy Queries**: See `POLICY_QUERIES_SYSTEM_GUIDE.md`
- **Employee Management**: See `COMPREHENSIVE_EMPLOYEE_SYSTEM.md`
- **Onboarding**: See `ONBOARDING_SYSTEM_GUIDE.md`
- **Feedback System**: See `FEEDBACK_SYSTEM_TESTING_GUIDE.md`
- **Admin Panel**: See `SUPERADMIN_PANEL_GUIDE.md`
- **Settings**: See `SETTINGS_COMPLETE.md`

### Getting Help
- **Issues**: Report bugs via GitHub Issues
- **Feature Requests**: Submit via GitHub Discussions
- **Documentation**: Check `docs/` folder for detailed guides
- **Community**: Join our development community

### For DRDO Employees
- Contact your HR department for access
- Default credentials provided during onboarding
- First-time login requires password change
- Complete profile for full feature access

## 📄 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout user

#### Policy Queries (APEX)
- `GET /policy-queries` - Get query history
- `POST /policy-queries` - Submit new policy query
- `POST /generate-application` - Generate application

#### Feedback & Grievances
- `GET /feedback` - Get all feedback (with filters)
- `POST /feedback` - Submit feedback/grievance
- `PUT /feedback/{id}` - Update feedback status
- `GET /feedback/stats` - Get feedback statistics

#### Employee Management
- `GET /settings/employee/personal` - Get personal info
- `PUT /settings/employee/personal` - Update personal info
- `GET /settings/employee/complete` - Get complete profile
- `GET /settings/employee/profile-completion` - Get completion %

#### Admin (Superadmin only)
- `GET /admin/users/list` - List all users
- `POST /admin/create-employee` - Create new employee
- `PUT /admin/users/{id}` - Update user
- `DELETE /admin/users/{id}` - Delete user
- `POST /admin/users/{id}/reset-password` - Reset password

See `apex_backend.py` for complete API reference.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Next.js**: Modern React framework for production
- **Flask**: Lightweight and powerful Python web framework
- **CrewAI**: Cutting-edge multi-agent AI framework
- **Google Gemini**: Advanced language model API
- **PostgreSQL**: Robust and reliable database system
- **Tailwind CSS**: Utility-first CSS framework
- **Framer Motion**: Production-ready animation library
- **LangChain**: Framework for building LLM applications
- **FAISS**: Efficient similarity search library
- **DRDO**: For the opportunity to build this platform
- **Open Source Community**: For endless inspiration and support

---

<div align="center">

**🌟 SHAKTI-AI: Empowering DRDO Employees Through AI-Powered HR Solutions 🌟**

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/chahalbaljinder/new-shaktiai)
[![Python](https://img.shields.io/badge/Built%20with-Python%20%26%20TypeScript-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Powered%20by-Next.js%20%26%20Flask-black.svg)](https://nextjs.org/)

### 🚀 **Features**: Policy Queries | Grievance Management | Employee Onboarding | AI Agents | Analytics

</div>
