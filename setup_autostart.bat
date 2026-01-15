@echo off
REM Setup JC Agent to run at Windows startup
REM This script adds JC Agent to the Windows startup folder

echo Setting up JC Agent to launch at startup...

set "SCRIPT_DIR=%~dp0"
set "LAUNCHER=%SCRIPT_DIR%jc_launcher.pyw"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_FOLDER%\JC Agent.vbs"

REM Create a VBScript to launch Python script without console window
echo Set WshShell = CreateObject("WScript.Shell") > "%SHORTCUT%"
echo WshShell.Run "pythonw "^"%LAUNCHER%"^"" , 0, False >> "%SHORTCUT%"

echo.
echo ✓ JC Agent has been added to Windows startup!
echo   JC will automatically launch when you log in.
echo.
echo Press any key to exit...
pause > nul
