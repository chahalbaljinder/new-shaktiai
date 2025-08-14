# Shakti-AI Deployment Guide

## Overview
Your Shakti-AI application consists of:
- **Frontend**: Next.js application (React-based)
- **Backend**: Python FastAPI/HTTP server with AI agents
- **Database**: PostgreSQL
- **AI Components**: LangChain, Google Gemini, Knowledge Base

## Deployment Options

### Option 1: Cloud Platform Deployment (Recommended)

#### 1.1 Vercel + Railway/Render
**Best for**: Quick deployment with minimal DevOps

**Frontend (Next.js) on Vercel:**
1. Push your code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically

**Backend on Railway/Render:**
1. Create account on Railway.app or Render.com
2. Connect GitHub repository
3. Configure Python environment
4. Set environment variables

#### 1.2 AWS/Google Cloud/Azure
**Best for**: Production-grade deployment with full control

### Option 2: VPS/Dedicated Server
**Best for**: Cost-effective solution with more control

## Step-by-Step Deployment

### Prerequisites
1. GitHub repository (your code)
2. Domain name (optional)
3. Cloud platform account
4. Environment variables ready

### Step 1: Prepare Your Code for Production

#### 1.1 Update Environment Variables
Create production environment files:

```bash
# .env.production (for Next.js)
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
PYTHON_SERVICE_URL=https://your-backend-domain.com
JWT_SECRET=your-production-jwt-secret
DB_HOST=your-production-db-host
DB_NAME=shakti_ai_db
DB_USER=your-db-user
DB_PASSWORD=your-secure-db-password
DB_PORT=5432
```

#### 1.2 Create Production Configuration Files

**Dockerfile for Python Backend:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "shakti_backend.py"]
```

**Docker Compose (Optional):**
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/shakti_ai_db
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: shakti_ai_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Step 2: Deploy Backend (Python AI Service)

#### Option A: Railway Deployment
1. Go to Railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and install dependencies
5. Set environment variables in Railway dashboard:
   - `DATABASE_URL`
   - `GOOGLE_API_KEY`
   - `JWT_SECRET`
   - Any other required variables
6. Railway will provide a public URL for your backend

#### Option B: Render Deployment
1. Sign up at Render.com
2. Create "New Web Service"
3. Connect GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python shakti_backend.py`
   - **Environment**: Python 3.11
5. Add environment variables
6. Deploy

### Step 3: Deploy Frontend (Next.js)

#### Vercel Deployment (Recommended)
1. Go to Vercel.com and sign up with GitHub
2. Click "New Project"
3. Import your repository
4. Vercel auto-detects Next.js
5. Set environment variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-railway-url.up.railway.app
   JWT_SECRET=your-production-secret
   ```
6. Deploy automatically

### Step 4: Database Setup

#### Option A: Managed Database
1. **Railway**: Add PostgreSQL service to your project
2. **Render**: Use Render PostgreSQL
3. **Supabase**: Create free PostgreSQL instance
4. **PlanetScale**: MySQL alternative

#### Option B: Self-hosted
1. Set up PostgreSQL on your VPS
2. Run your database migration scripts
3. Secure with proper firewall rules

### Step 5: Domain Configuration

1. Purchase domain from Namecheap/GoDaddy
2. Configure DNS:
   - **Frontend**: Point to Vercel
   - **Backend**: Point to Railway/Render
3. Set up SSL certificates (automatic with most platforms)

### Step 6: Production Optimizations

#### Security
1. Change all default passwords
2. Use environment variables for secrets
3. Enable CORS properly
4. Set up rate limiting
5. Use HTTPS only

#### Performance
1. Enable caching
2. Optimize images
3. Use CDN for static assets
4. Monitor performance

#### Monitoring
1. Set up error tracking (Sentry)
2. Add logging
3. Monitor uptime
4. Set up alerts

## Quick Deploy Commands

### If using Railway CLI:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy backend
railway login
railway init
railway up
```

### If using Vercel CLI:
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd shakti-ai-nextjs
vercel --prod
```

## Environment Variables Checklist

### Backend Environment Variables:
- `DATABASE_URL`
- `GOOGLE_API_KEY` (for Gemini)
- `JWT_SECRET`
- `CORS_ORIGINS`
- `PORT` (usually 8000)

### Frontend Environment Variables:
- `NEXT_PUBLIC_API_URL`
- `JWT_SECRET`
- `DATABASE_URL` (if using direct DB connection)

## Cost Estimation

### Free Tier Options:
- **Vercel**: Free for personal projects
- **Railway**: $5/month after free tier
- **Render**: Free tier available
- **Supabase**: Free PostgreSQL tier

### Paid Options:
- **AWS/GCP/Azure**: $20-50/month for small apps
- **VPS (DigitalOcean/Linode)**: $5-20/month

## Troubleshooting Common Issues

1. **CORS Errors**: Update backend CORS settings
2. **Environment Variables**: Double-check all variables are set
3. **Database Connection**: Verify connection strings
4. **Build Failures**: Check dependencies and Node.js version
5. **API Errors**: Verify backend is running and accessible

## Production Checklist

- [ ] All environment variables set
- [ ] Database configured and accessible
- [ ] CORS properly configured
- [ ] HTTPS enabled
- [ ] Error monitoring setup
- [ ] Backup strategy in place
- [ ] Domain configured
- [ ] Performance optimized
- [ ] Security hardened
- [ ] Testing completed

## Next Steps After Deployment

1. Set up monitoring and alerts
2. Configure automatic backups
3. Set up CI/CD pipeline
4. Add performance monitoring
5. Implement user analytics
6. Set up customer support tools

Would you like me to help you with any specific deployment platform or step?
