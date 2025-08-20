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
COPY shakti_backend.py ./
COPY core ./core
COPY database ./database
COPY utils ./utils
COPY knowledge_base ./knowledge_base
COPY wishes_data.json ./

# Expose API port
EXPOSE 8000

# Default command uses direct Python execution for HTTP server
CMD ["python", "shakti_backend.py"]
