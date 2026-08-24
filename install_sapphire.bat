@echo off
TITLE Sapphire Language One-Click Automated Installer for Windows
chcp 65001 > nul
cls

echo =====================================================================
echo   🌌 SAPPHIRE PROGRAMMING LANGUAGE — AUTOMATED WINDOWS INSTALLER
echo =====================================================================
echo.

SET "INSTALL_DIR=%LOCALAPPDATA%\SapphireLang"

echo [1/3] Creating installation directory at:
echo       %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo.
echo [2/3] Copying Sapphire binary executables and standard library...
copy /Y "%~dp0sapphire.exe" "%INSTALL_DIR%\sapphire.exe" >nul
if exist "%~dp0sapphire_voice_tutor.exe" (
    copy /Y "%~dp0sapphire_voice_tutor.exe" "%INSTALL_DIR%\sapphire_voice_tutor.exe" >nul
)
if exist "%~dp0sapphire_tutor.exe" (
    copy /Y "%~dp0sapphire_tutor.exe" "%INSTALL_DIR%\sapphire_tutor.exe" >nul
)

echo.
echo [3/3] Registering 'sapphire' command in Windows User PATH...
powershell -Command "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($oldPath -notlike '*SapphireLang*') { [Environment]::SetEnvironmentVariable('Path', $oldPath + ';%INSTALL_DIR%', 'User'); Write-Host '✅ PATH updated successfully.' } else { Write-Host 'ℹ️ PATH already configured.' }"

echo.
echo =====================================================================
echo   🎉 SAPPHIRE LANGUAGE INSTALLATION COMPLETE!
echo =====================================================================
echo.
echo  You can now open any Command Prompt or PowerShell window and type:
echo.
echo     sapphire info           - Display language overview & version
echo     sapphire run bot.sp     - Run a Sapphire script file
echo     sapphire repl           - Open interactive REPL shell
echo     sapphire studio         - Launch Emerald Developer Studio GUI
echo     sapphire tutor          - Launch Voice-Guided Interactive Tutor
echo.
pause
