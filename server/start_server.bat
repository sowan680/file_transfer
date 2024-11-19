@echo off

REM Stop the script on error
setlocal enabledelayedexpansion

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and add it to the PATH.
    exit /b 1
)

REM Check if virtual environment exists, if not - create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies from requirements.txt
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Error: requirements.txt file not found!
    exit /b 1
)

REM Start FastAPI server using Uvicorn
set HOST=0.0.0.0
set PORT=8000

echo Starting FastAPI server on http://%HOST%:%PORT%
uvicorn server:app --host %HOST% --port %PORT% --reload

REM End of script
endlocal
