@echo off
echo ================================
echo JC-Agent Windows Installer
echo ================================
echo.

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating startup directory...
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "INSTALL_DIR=%~dp0"

echo.
echo Creating desktop shortcut...
set "SHORTCUT=%USERPROFILE%\Desktop\JC-Agent.lnk"
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%SHORTCUT%'); $SC.TargetPath = 'pythonw.exe'; $SC.Arguments = '\"%INSTALL_DIR%jc_desktop.py\"'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.Save()"

echo.
echo Creating startup entry (auto-launch on login)...
set "STARTUP_SHORTCUT=%STARTUP_DIR%\JC-Agent.lnk"
powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%STARTUP_SHORTCUT%'); $SC.TargetPath = 'pythonw.exe'; $SC.Arguments = '\"%INSTALL_DIR%jc_desktop.py\"'; $SC.WorkingDirectory = '%INSTALL_DIR%'; $SC.Save()"

echo.
echo Creating .env file from template...
if not exist ".env" (
    copy .env.example .env
    echo IMPORTANT: Edit .env file and add your API keys!
) else (
    echo .env file already exists, skipping...
)

echo.
echo ================================
echo Installation Complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Double-click 'JC-Agent' on your desktop to launch
echo 3. JC-Agent will auto-start on login
echo 4. Look for the JC icon in your system tray
echo.
echo Starting JC-Agent now...
start pythonw.exe "%INSTALL_DIR%jc_desktop.py"

echo.
echo JC-Agent is running in the background!
pause
