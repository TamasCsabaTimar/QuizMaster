@echo off
echo Restarting Python Quiz API...

echo Stopping any running instances...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Python Quiz API" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Application stopped successfully.
) else (
    echo No running instances found or could not stop the application.
)

echo Starting the application...
call .\.venv\Scripts\activate.bat
start "Python Quiz API" python main.py
echo Application restarted successfully.