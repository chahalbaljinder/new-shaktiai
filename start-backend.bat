@echo off
echo Starting APEX Backend (shakti_backend.py)...

:: Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

:: Start the real AI backend
echo Starting shakti_backend.py on port 8000...
python shakti_backend.py
pause