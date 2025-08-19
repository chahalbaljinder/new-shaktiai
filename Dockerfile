# Backend Dockerfile
FROM python:3.11-slim

# System deps (optional: uncomment if you need ffmpeg or build tools)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     ffmpeg build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend_service.py ./
COPY core ./core
COPY database ./database
COPY utils ./utils
COPY knowledge_base ./knowledge_base

# Expose API port
EXPOSE 8000

# Default command uses uvicorn to serve FastAPI app
CMD ["python", "-m", "uvicorn", "backend_service:app", "--host", "0.0.0.0", "--port", "8000"]
