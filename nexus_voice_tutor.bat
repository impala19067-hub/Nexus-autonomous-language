@echo off
TITLE Nexus Language Advanced Voice-Guided Interactive Tutor
chcp 65001 > nul
cls

echo =====================================================================
echo   🔊 NEXUS PROGRAMMING LANGUAGE — ADVANCED VOICE-GUIDED TUTOR
echo =====================================================================
echo.

IF EXIST "nexus_voice_tutor.exe" (
    echo Launching compiled Standalone Nexus Voice Tutor Executable...
    echo.
    "nexus_voice_tutor.exe"
    goto END
)

IF EXIST "dist\nexus_voice_tutor.exe" (
    echo Launching compiled Standalone Nexus Voice Tutor Executable...
    echo.
    "dist\nexus_voice_tutor.exe"
    goto END
)

echo Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.10+ to run Nexus Voice Tutor.
    echo.
    pause
    exit /b 1
)

echo Launching Nexus Voice-Guided Tutor via Python...
echo.
python "%~dp0nexus_voice_tutor.py"

:END
pause
