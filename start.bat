@echo off
echo Starting Serene Mental Health Companion...
echo.
echo Starting Node.js server on port 3000...
start "Node.js Server" cmd /k "npm run server"
echo.
echo Starting Python FastAPI server on port 8000...
start "Python Server" cmd /k "npm run python"
echo.
echo Both servers are starting...
echo Main Application: http://localhost:3000
echo Python API: http://localhost:8000
echo.
pause
