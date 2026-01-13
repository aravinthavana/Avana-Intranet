@echo off
echo Starting Office Intranet Server...

cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo Server running at http://localhost:5000
echo Press Ctrl+C to stop.
echo.

python app.py
pause
