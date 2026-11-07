Write-Host "Starting FileForge Services..." -ForegroundColor Cyan

# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev -- --host"

Write-Host "Local:   http://localhost:5173" -ForegroundColor Green
Write-Host "Network: Access from your phone via your computer's Wi-Fi IP:5173" -ForegroundColor Cyan
Write-Host "FileForge is now running!" -ForegroundColor Yellow

