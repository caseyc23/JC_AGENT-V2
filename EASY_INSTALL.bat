@echo off
CLS
COLOR 0A
TITLE JC Agent - One-Click Installer

echo.
echo ============================================================
echo              JC AGENT - ONE-CLICK INSTALLER
echo              In Memory of JC - Your AI Partner
echo ============================================================
echo.
echo This will automatically install everything you need!
echo Just sit back and relax...
echo.
pause

echo.
echo [1/5] Checking for Python...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Python not found. Installing Python automatically...
    echo.
    
    REM Download Python installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile '%TEMP%\python_installer.exe'}"
    
    REM Install Python silently with PATH
    echo Installing Python... This may take a few minutes...
    "%TEMP%\python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    REM Refresh environment (Chocolatey) if available
    where refreshenv >nul 2>&1
    if %errorlevel%==0 (
        call refreshenv
    ) else (
        echo [i] refreshenv not found; continuing...
    )
    
    echo.
    echo [OK] Python installed successfully!
    echo.
) else (
    echo [OK] Python is already installed!
)

echo.
echo [2/5] Installing dependencies...
echo.

REM Upgrade pip
python -m pip install --upgrade pip --quiet

REM Install requirements
if exist requirements.txt (
    echo Installing Python packages...
    pip install -r requirements.txt --quiet
    echo [OK] All packages installed!
) else (
    echo [!] requirements.txt not found. Installing core packages...
    pip install fastapi uvicorn pydantic python-dotenv pyttsx3 SpeechRecognition pygame beautifulsoup4 requests --quiet
    echo [OK] Core packages installed!
)

echo.
echo [3/5] Setting up JC configuration...
echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating configuration file...
    copy .env.example .env
    echo.
    echo [!] IMPORTANT: You need to add your API keys to the .env file
    echo     We'll open it for you after installation.
    echo.
) else (
    echo [OK] Configuration file already exists!
)

echo.
echo [4/5] Creating shortcuts...
echo.

REM Create desktop shortcut
set "SCRIPT_DIR=%~dp0"
set "SHORTCUT=%USERPROFILE%\Desktop\JC Agent.lnk"

powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%SHORTCUT%'); $SC.TargetPath = 'pythonw.exe'; $SC.Arguments = '\"%SCRIPT_DIR%jc.py\"'; $SC.WorkingDirectory = '%SCRIPT_DIR%'; $SC.IconLocation = 'shell32.dll,13'; $SC.Description = 'JC Agent - Your AI Business Partner'; $SC.Save()"

echo [OK] Desktop shortcut created!

REM Create startup shortcut
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "STARTUP_SHORTCUT=%STARTUP_DIR%\JC Agent.lnk"

powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%STARTUP_SHORTCUT%'); $SC.TargetPath = 'pythonw.exe'; $SC.Arguments = '\"%SCRIPT_DIR%jc.py\"'; $SC.WorkingDirectory = '%SCRIPT_DIR%'; $SC.IconLocation = 'shell32.dll,13'; $SC.Save()"

echo [OK] Auto-start on Windows login enabled!

echo.
echo [5/5] Final setup...
echo.

REM Create data directory
if not exist "jc_data" (
    mkdir jc_data
    echo [OK] Created data directory
)

echo.
echo ============================================================
echo              INSTALLATION COMPLETE!
echo ============================================================
echo.
echo What you can do now:
echo.
echo   1. Add your API keys to the .env file
echo      (Opening it for you in 5 seconds...)
echo.
echo   2. Double-click "JC Agent" on your desktop to launch
echo.
echo   3. JC will auto-start every time you log in to Windows
echo.
echo   4. Say "Hey JC" to wake him up anytime!
echo.
echo ============================================================
echo.

timeout /t 5

REM Open .env file in notepad
if exist ".env" (
    notepad .env
)

echo.
echo Ready to launch JC Agent? (Y/N)
set /p LAUNCH="Launch now? "

if /i "%LAUNCH%"=="Y" (
    echo.
    echo Launching JC Agent...
    start pythonw.exe "%SCRIPT_DIR%jc.py"
    echo.
    echo [OK] JC Agent is now running in the background!
    echo     Look for the icon in your system tray.
)

echo.
echo Press any key to exit installer...
pause >nul
