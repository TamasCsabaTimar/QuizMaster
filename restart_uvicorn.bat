@echo off
echo Restarting Python Quiz API with Uvicorn...

echo Stopping any running instances...
taskkill /f /im python.exe /fi "WINDOWTITLE eq Python Quiz API Uvicorn" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Application stopped successfully.
) else (
    echo No running instances found or could not stop the application.
)

echo Starting the application with Uvicorn...
call .\.venv\Scripts\activate.bat
start "Python Quiz API Uvicorn" cmd /k uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo Application restarted successfully with Uvicorn.