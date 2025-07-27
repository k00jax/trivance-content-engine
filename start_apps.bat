@echo off
echo Starting Trivance AI Content Engine...
echo.

echo Starting FastAPI Backend...
start "Backend" cmd /k "python -m uvicorn app.main:app --reload"

echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Streamlit Frontend...
start "Frontend" cmd /k "streamlit run ui/streamlit_app.py"

echo.
echo ✅ Both applications should be starting in separate windows!
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:8501
echo.
pause
