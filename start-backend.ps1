# Start APEX Backend using shakti_backend.py
Write-Host "Starting APEX Backend (shakti_backend.py)..." -ForegroundColor Green

# Activate virtual environment if it exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
}

# Start the real AI backend
Write-Host "Starting shakti_backend.py on port 8000..." -ForegroundColor Cyan
python shakti_backend.py