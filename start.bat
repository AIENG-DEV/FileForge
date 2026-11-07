@echo off
echo Starting FileForge...
echo Starting Backend on http://localhost:8000
start cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo Starting Frontend on http://localhost:5173
start cmd /k "cd frontend && npm run dev -- --host"
echo Both servers started!
pause

