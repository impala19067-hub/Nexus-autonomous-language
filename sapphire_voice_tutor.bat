@echo off
TITLE Sapphire Language Advanced Voice-Guided Interactive Tutor
chcp 65001 > nul
cls

echo =====================================================================
echo   🔊 SAPPHIRE PROGRAMMING LANGUAGE — ADVANCED VOICE-GUIDED TUTOR
echo =====================================================================
echo.

IF EXIST "sapphire_voice_tutor.exe" (
    echo Launching compiled Standalone Sapphire Voice Tutor Executable...
    echo.
    "sapphire_voice_tutor.exe"
    goto END
)

IF EXIST "dist\sapphire_voice_tutor.exe" (
    echo Launching compiled Standalone Sapphire Voice Tutor Executable...
    echo.
    "dist\sapphire_voice_tutor.exe"
    goto END
)

echo Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.10+ to run Sapphire Voice Tutor.
    echo.
    pause
    exit /b 1
)

echo Launching Sapphire Voice-Guided Tutor via Python...
echo.
python "%~dp0sapphire_voice_tutor.py"

:END
pause
