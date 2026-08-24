@echo off
TITLE Sapphire Language Autonomous Interactive Tutor
chcp 65001 > nul
cls

echo =================================================================
echo   🌌 SAPPHIRE PROGRAMMING LANGUAGE — AUTONOMOUS INTERACTIVE TUTOR
echo =================================================================
echo.

IF EXIST "dist\sapphire_tutor.exe" (
    echo Launching compiled Sapphire Tutor executable...
    echo.
    "dist\sapphire_tutor.exe"
    goto END
)

IF EXIST "sapphire_tutor.exe" (
    echo Launching compiled Sapphire Tutor executable...
    echo.
    "sapphire_tutor.exe"
    goto END
)

echo Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.10+ to run Sapphire Language Tutor.
    echo.
    pause
    exit /b 1
)

echo Launching Sapphire Interactive Tutor via Python Engine...
echo.
python "%~dp0sapphire_tutor.py"

:END
pause
