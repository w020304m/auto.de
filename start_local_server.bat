@echo off
REM Local Test Server for Handwerker Ratgeber
REM Usage: double-click this file to start local server

echo ========================================
echo Handwerker Ratgeber - Local Test Server
echo ========================================
echo.
echo Starting server on http://localhost:8080
echo Press Ctrl+C to stop the server
echo.

cd output
python -m http.server 8080
