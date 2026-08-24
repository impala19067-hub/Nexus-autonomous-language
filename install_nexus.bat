@echo off
TITLE Nexus Language One-Click Automated Installer for Windows
chcp 65001 > nul
cls

echo =====================================================================
echo   🌌 NEXUS PROGRAMMING LANGUAGE — AUTOMATED WINDOWS INSTALLER
echo =====================================================================
echo.

SET "INSTALL_DIR=%LOCALAPPDATA%\NexusLang"

echo [1/3] Creating installation directory at:
echo       %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo.
echo [2/3] Copying Nexus binary executables and standard library...
copy /Y "%~dp0nexus.exe" "%INSTALL_DIR%\nexus.exe" >nul
if exist "%~dp0nexus_voice_tutor.exe" (
    copy /Y "%~dp0nexus_voice_tutor.exe" "%INSTALL_DIR%\nexus_voice_tutor.exe" >nul
)
if exist "%~dp0nexus_tutor.exe" (
    copy /Y "%~dp0nexus_tutor.exe" "%INSTALL_DIR%\nexus_tutor.exe" >nul
)

echo.
echo [3/3] Registering 'nexus' command in Windows User PATH...
powershell -Command "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($oldPath -notlike '*NexusLang*') { [Environment]::SetEnvironmentVariable('Path', $oldPath + ';%INSTALL_DIR%', 'User'); Write-Host '✅ PATH updated successfully.' } else { Write-Host 'ℹ️ PATH already configured.' }"

echo.
echo =====================================================================
echo   🎉 NEXUS LANGUAGE INSTALLATION COMPLETE!
echo =====================================================================
echo.
echo  You can now open any Command Prompt or PowerShell window and type:
echo.
echo     nexus info           - Display language overview & version
echo     nexus run bot.nx     - Run a Nexus script file
echo     nexus repl           - Open interactive REPL shell
echo     nexus tutor          - Launch Voice-Guided Interactive Tutor
echo.
pause
