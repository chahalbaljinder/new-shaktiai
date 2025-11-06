# Shakti-AI Docker Deployment Guide

This guide shows how to run the full stack (FastAPI backend + Next.js frontend + Postgres) using Docker.

## Overview
- Backend: Simple HTTP server in `shakti_backend.py` with direct AI integration
- Frontend: Next.js in `shakti-ai-nextjs`
- Database: PostgreSQL 15

## Files added
- `Dockerfile` (backend)
- `docker-compose.yml` (orchestration)
- `shakti-ai-nextjs/Dockerfile` (frontend)
- `.dockerignore` and `shakti-ai-nextjs/.dockerignore`

## Environment
Create `.env` at the repo root (used by docker-compose):

```
DB_HOST=db
DB_NAME=shakti_ai_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
GOOGLE_API_KEY=your-key
JWT_SECRET=your-secret
NEXT_PUBLIC_API_URL=http://frontend:3000
PYTHON_SERVICE_URL=http://backend:8000
``` 

Frontend can also have `shakti-ai-nextjs/.env.production` if needed; using compose-provided env is enough.

## Build and run

```powershell
docker compose up -d --build
```

Services:
- API: http://localhost:8000
- Frontend: http://localhost:3000
- Postgres: localhost:5432 (internal network name `db`)

## Production notes
- Use volumes for persistent Postgres data.
- Set real secrets in `.env` or your orchestrator.
- Configure CORS in `shakti_backend.py` for your domains.

## Troubleshooting
- If backend can’t reach DB, check `DB_HOST=db` and that the `db` service is healthy.
- If frontend can’t reach API in browser, set `NEXT_PUBLIC_API_URL` to the public API URL (e.g., `http://localhost:8000`). In container-to-container calls it can use `http://backend:8000`.
- Rebuild images after dependency changes.

