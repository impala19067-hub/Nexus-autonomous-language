@echo off
TITLE Nexus Language Autonomous Interactive Tutor
chcp 65001 > nul
cls

echo =================================================================
echo   🌌 NEXUS PROGRAMMING LANGUAGE — AUTONOMOUS INTERACTIVE TUTOR
echo =================================================================
echo.

IF EXIST "dist\nexus_tutor.exe" (
    echo Launching compiled Nexus Tutor executable...
    echo.
    "dist\nexus_tutor.exe"
    goto END
)

IF EXIST "nexus_tutor.exe" (
    echo Launching compiled Nexus Tutor executable...
    echo.
    "nexus_tutor.exe"
    goto END
)

echo Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.10+ to run Nexus Language Tutor.
    echo.
    pause
    exit /b 1
)

echo Launching Nexus Interactive Tutor via Python Engine...
echo.
python "%~dp0nexus_tutor.py"

:END
pause
