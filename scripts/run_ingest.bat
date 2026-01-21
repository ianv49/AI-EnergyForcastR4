@echo off
REM Windows Batch File for Sensor Data Ingestion
REM Run this file manually or schedule it with Task Scheduler
REM
REM To run: run_ingest.bat
REM To schedule (Windows Task Scheduler):
REM   1. Open Task Scheduler
REM   2. Create Basic Task -> "Sensor Ingestion"
REM   3. Set trigger: Daily at a specific time
REM   4. Set action: Start a program -> run_ingest.bat
REM

setlocal enabledelayedexpansion

REM Get the directory of this script
set "SCRIPT_DIR=%~dp0"

REM Navigate to repo root
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found at .venv\Scripts\activate.bat
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run ingestion
echo.
echo ============================================================
echo Energy Sensor Data Ingestion - %date% %time%
echo ============================================================
echo.

python run_ingest.py

REM Log timestamp
echo Ingestion completed at %date% %time% >> logs\batch_runs.log

echo.
echo ============================================================
echo Check logs\ingestion.log for details
echo ============================================================
echo.

REM Keep window open for 5 seconds
timeout /t 5 /nobreak

endlocal
