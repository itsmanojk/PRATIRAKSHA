@echo off
color 0A
cls
echo.
echo ==================================================================================
echo    PRATIRAKSHA - AI Network Threat Detection System
echo ==================================================================================
echo.
echo Starting project in 3 seconds...
echo Press CTRL+C to stop any server
echo.
timeout /t 3 /nobreak

echo.
echo [1/2] Starting Backend Server on port 5002...
echo.
start "PRATIRAKSHA Backend" cmd /k cd /d c:\Desktop\PRATIRAKSHA-Production\backend && python app.py

echo.
timeout /t 5 /nobreak

echo.
echo [2/2] Starting Frontend Server on port 3000...
echo.
start "PRATIRAKSHA Frontend" cmd /k cd /d c:\Desktop\PRATIRAKSHA-Production\frontend && npm start

echo.
echo ==================================================================================
echo    PROJECT STARTED SUCCESSFULLY
echo ==================================================================================
echo.
echo Dashboard URL: http://localhost:3000
echo Backend API: http://localhost:5002
echo.
echo Both servers are running in separate windows.
echo Close the windows to stop the servers.
echo.
pause
