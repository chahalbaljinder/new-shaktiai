# SHAKTI-AI Railway Deployment Guide

## 🚀 Deployment Status: READY ✅

The SHAKTI-AI backend is now fully configured for Railway deployment with all necessary configuration files.

## 📁 Deployment Files Created

### Core Deployment Files
- **`Procfile`** - Defines the web service start command
- **`nixpacks.toml`** - Nixpacks build configuration 
- **`railway.json`** - Railway platform specific settings
- **`runtime.txt`** - Python version specification

### Dependencies & Environment
- **`requirements.txt`** - Updated with deployment-ready Python packages
- **`.env.production.example`** - Production environment template
- **`.gitignore`** - Enhanced to exclude deployment artifacts

## 🔧 Pre-Deployment Checklist

### 1. Environment Variables (Required)
Set these in Railway's environment variables:

```bash
# Database (Required)
DATABASE_URL=postgresql://username:password@host:port/database

# API Keys (Required) 
GOOGLE_API_KEY=your-google-gemini-api-key

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 2. Database Setup
- Create a PostgreSQL database in Railway
- The app will auto-initialize tables on first run

### 3. Port Configuration
- Railway automatically provides `$PORT` environment variable
- The app is configured to use this automatically

## 🛠 Railway Deployment Steps

### 1. Connect Repository
```bash
# Push your changes to GitHub
git commit -m "Add Railway deployment configuration"
git push origin review-nextjs
```

### 2. Railway Setup
1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Select the `new-shaktiai` repository
4. Choose the `review-nextjs` branch

### 3. Configure Environment
Add these environment variables in Railway:
- `GOOGLE_API_KEY` - Your Google Gemini API key
- `DATABASE_URL` - Will be auto-provided by Railway PostgreSQL
- `SMTP_*` variables - For email functionality (optional)

### 4. Deploy
Railway will automatically:
1. Detect the Python project
2. Install dependencies from `requirements.txt`
3. Build using Nixpacks configuration
4. Start the service with the Procfile command

## 🔍 Build Process

Railway will execute:
```bash
# Setup phase
python3, postgresql_16.dev, ffmpeg, gcc, pkg-config installed

# Install phase
python -m venv --copies /opt/venv
. /opt/venv/bin/activate && pip install --upgrade pip
. /opt/venv/bin/activate && pip install -r requirements.txt

# Start phase
. /opt/venv/bin/activate && uvicorn backend_service:app --host 0.0.0.0 --port $PORT
```

## 🧪 Health Checks

The service includes health endpoints:
- `GET /` - Basic service status
- `GET /health` - Detailed health check with timestamp

## 📋 Service Endpoints

Once deployed, your service will provide:

### Core APIs
- `GET /api/agents/list` - Available AI agents
- `POST /api/agents/chat` - Chat with AI agents
- `GET /api/wishes/list` - Fetch wishes
- `POST /api/wishes/create` - Create new wish
- `POST /api/wishes/share` - Share wishes via email/WhatsApp

### Voice APIs  
- `POST /api/voice/speech-to-text` - Convert audio to text
- `POST /api/voice/direct-speech-to-text` - Direct microphone access

### Utility APIs
- `GET /api/email/test` - Test SMTP configuration
- `GET /api/email/setup-instructions` - Email setup guide

## 🔒 Security Features

- CORS configured for frontend origins
- Input validation with Pydantic models
- Error handling with proper HTTP status codes
- Secure environment variable handling
- Database connection security

## 📊 Performance Optimizations

- FastAPI with Uvicorn for high performance
- Async/await support for concurrent requests
- Efficient database queries
- Proper error handling and logging
- Resource cleanup for temporary files

## 🐛 Troubleshooting

### Common Issues

**Build Fails - Missing Dependencies**
```bash
# Check requirements.txt has all needed packages
# Problematic packages are commented out with alternatives
```

**Service Won't Start**
```bash
# Check Railway logs for detailed error messages
# Verify environment variables are set correctly
```

**Database Connection Fails**
```bash
# Ensure DATABASE_URL is provided by Railway PostgreSQL service
# Check database service is running and accessible
```

**Audio Processing Fails**
```bash
# FFmpeg is included in nixpacks.toml
# Some audio packages are disabled for deployment compatibility
```

## 🌐 Post-Deployment

### Frontend Integration
Update your Next.js frontend's API endpoints to use the Railway URL:
```typescript
// In your Next.js .env.local
NEXT_PUBLIC_API_URL=https://your-app-name.railway.app
```

### Testing
1. Test health endpoint: `https://your-app.railway.app/health`
2. Verify AI agents: `https://your-app.railway.app/api/agents/list`
3. Test database: Create and fetch wishes
4. Verify email: Test SMTP configuration

## 📈 Monitoring

Railway provides:
- Real-time logs
- Resource usage metrics
- Deployment history
- Custom domains
- SSL certificates

## 🎉 Success!

Your SHAKTI-AI backend is now production-ready and deployed on Railway!

---

**Last Updated**: August 2025  
**Status**: ✅ Deployment Ready  
**Platform**: Railway.app  
**Technology**: Python FastAPI + PostgreSQL
