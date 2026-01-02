@echo off
chcp 65001 >nul
echo Starting Custom Local Server...
echo server.py is running...
echo Do not close this window.

start "" "http://localhost:8000"
python server.py
pause
