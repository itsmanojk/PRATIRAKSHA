@echo off
color 0A
cls
echo.
echo ==================================================================================
echo    PRATIRAKSHA - AI Network Threat Detection System
echo    ONE-STEP PROJECT LAUNCHER
echo ==================================================================================
echo.
echo Starting both servers...
echo.

REM Change to project root
cd /d c:\Desktop\PRATIRAKSHA-Production

REM Start Backend in background
start "PRATIRAKSHA-Backend" cmd /k "cd backend && python app.py"

REM Wait for backend to initialize
timeout /t 3 /nobreak

REM Start Frontend in background
start "PRATIRAKSHA-Frontend" cmd /k "cd frontend && npm start"

REM Wait for frontend to start
timeout /t 3 /nobreak

echo.
echo ==================================================================================
echo    SUCCESS! Project is now running
echo ==================================================================================
echo.
echo [BACKEND]  http://localhost:5002  (API endpoints active)
echo [FRONTEND] http://localhost:3000  (Dashboard)
echo.
echo Opening dashboard in browser...
start http://localhost:3000
echo.
echo Both servers running. Close their windows to stop.
echo ==================================================================================
echo.
pause
