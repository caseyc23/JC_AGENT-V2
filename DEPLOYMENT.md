# 🚀 JC-Agent Deployment Guide - Asus Zenbook Duo

## Quick Start (Windows)

### Prerequisites
1. **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
   - ⚠️ During installation, CHECK "Add Python to PATH"
2. **Git** (optional) - For cloning the repo

### One-Click Installation

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/caseyc23/JC-agent-.git
   cd JC-agent-
   ```
   
   OR download ZIP from GitHub and extract it

2. **Run the Installer**
   - Double-click `install_windows.bat`
   - The installer will:
     - Install all Python dependencies
     - Create desktop shortcut
     - Add JC-Agent to Windows startup
     - Create `.env` file from template
     - Launch JC-Agent automatically

3. **Configure Your API Keys**
   - Edit `.env` file with your favorite text editor
   - Add your API keys:
     ```
     OPENROUTER_API_KEY=your_key_here
     HUGGINGFACE_API_KEY=your_key_here
     ```

4. **Launch JC-Agent**
   - Double-click the "JC-Agent" icon on your desktop
   - OR it will auto-start on next login
   - Look for the JC icon in your system tray (bottom-right)

---

## System Tray Features

Once running, JC-Agent lives in your taskbar system tray with:

### 🎯 Quick Actions
- **Double-click tray icon** → Opens main dashboard
- **Right-click** → Context menu:
  - Open Dashboard
  - Quick Chat
  - Business Assistant
  - Task Manager
  - Settings
  - Quit

### 🤖 What JC-Agent Can Do

1. **Business Partner Mode**
   - Schedule management
   - Email automation
   - Task tracking
   - Meeting reminders
   - Project organization

2. **Full System Access**
   - File management
   - Application launching
   - System automation
   - Web browsing assistance
   - Multi-screen optimization (perfect for Zenbook Duo!)

3. **AI-Powered Assistance**
   - Natural language commands
   - Context-aware responses
   - Learning your preferences
   - Multi-provider AI (OpenRouter, HuggingFace, local models)

---

## API Server (Advanced)

JC-Agent also runs a local API server on `http://127.0.0.1:8000`

### Start API Server
```bash
python agent_api.py
```

### API Endpoints

- `POST /chat` - Send messages to JC
- `POST /task` - Create/manage tasks
- `GET /status` - Check agent status
- `GET /docs` - Interactive API documentation

### Example Usage
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Help me organize my day"}'
```

---

## Folder Structure

```
JC-agent-/
├── agent_api.py          # FastAPI backend server
├── jc_desktop.py         # Desktop GUI with system tray
├── requirements.txt      # Python dependencies
├── .env                  # Your API keys (create from .env.example)
├── .env.example          # Template for environment variables
├── .gitignore           # Git ignore rules
├── install_windows.bat   # Windows installer script
├── README.md            # Project overview
└── DEPLOYMENT.md        # This file
```

---

## Zenbook Duo Optimization

JC-Agent is optimized for dual-screen setups:

- **Main Screen**: Dashboard and primary interface
- **Second Screen**: Task lists, calendars, notifications
- **Screen Switching**: Automatic window placement
- **Touch Support**: Full touchscreen compatibility

---

## Troubleshooting

### JC-Agent won't start
1. Check Python is installed: `python --version`
2. Verify dependencies: `pip install -r requirements.txt`
3. Check `.env` file has valid API keys
4. Look for errors in `jc_agent.log`

### System tray icon missing
1. Check Task Manager → JC-Agent is running
2. Restart the application
3. Check Windows notification settings

### API server issues
1. Verify port 8000 is not in use
2. Check firewall settings
3. Try `python agent_api.py --host 127.0.0.1 --port 8000`

---

## Uninstall

1. Delete desktop shortcut
2. Remove from startup folder: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\JC-Agent.lnk`
3. Delete the JC-agent folder

---

## Support

For issues or questions:
- GitHub Issues: [JC-agent-/issues](https://github.com/caseyc23/JC-agent-/issues)
- Check logs: `jc_agent.log`

---

**🎉 You're all set! JC-Agent is now your personal AI business partner on your Asus Zenbook Duo!**
