# PRATIRAKSHA - One-Step Project Launcher (PowerShell)
# Run this script to start the entire project in one command

Write-Host "
================================================================================" -ForegroundColor Cyan
Write-Host "  PRATIRAKSHA - AI Network Threat Detection System" -ForegroundColor Green
Write-Host "  ONE-STEP PROJECT LAUNCHER" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "C:\Desktop\PRATIRAKSHA-Production"
Set-Location $projectRoot

# Start Backend
Write-Host "[1/2] Starting Backend Server (port 5002)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command {cd '$projectRoot\backend'; python app.py}" -WindowTitle "PRATIRAKSHA-Backend"

# Wait for backend initialization
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "[2/2] Starting Frontend Server (port 3000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit -Command {cd '$projectRoot\frontend'; npm start}" -WindowTitle "PRATIRAKSHA-Frontend"

# Wait for frontend to start
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "  SUCCESS! Project is running" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  [BACKEND]  " -ForegroundColor Cyan -NoNewline
Write-Host "http://localhost:5002" -ForegroundColor White
Write-Host "  [FRONTEND] " -ForegroundColor Cyan -NoNewline
Write-Host "http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "  Opening dashboard in browser..." -ForegroundColor Yellow
Write-Host ""

# Open browser
Start-Process "http://localhost:3000"

Write-Host "================================================================================" -ForegroundColor Green
Write-Host "  Both servers are running. Close the windows to stop." -ForegroundColor Yellow
Write-Host "================================================================================" -ForegroundColor Green
