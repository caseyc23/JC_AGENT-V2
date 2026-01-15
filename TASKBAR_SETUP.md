# 🎯 JC Agent Taskbar Setup Guide

## Get JC in Your Windows Taskbar - Complete Guide

This guide will help you set up JC Agent to launch automatically from your Windows taskbar, just like any other application.

---

## ⚡ Quick Setup (Recommended)

### Option 1: Easy Install Script

1. **Run the installer:**

   ```bash
   # Double-click EASY_INSTALL.bat
   # Or run from command prompt:
   EASY_INSTALL.bat
   ```

2. **Setup autostart:**

   ```bash
   # Double-click setup_autostart.bat
   setup_autostart.bat
   ```

3. **Done!** JC will now:
   - ✅ Appear in your system tray
   - ✅ Launch automatically when Windows starts
   - ✅ Be accessible with a single click

---

## 📋 Manual Setup (For Full Control)

### Step 1: Install Dependencies

```bash
pip install pystray Pillow requests fastapi uvicorn
```

### Step 2: Configure Your API Key

1. Copy the example config:

   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

### Step 3: Test the Launcher

```bash
python jc_launcher.pyw
```

You should see a JC icon appear in your system tray!

### Step 4: Setup Auto-Start

**Method A: Using the Script (Easiest)**

```bash
setup_autostart.bat
```

**Method B: Manual Setup**

1. Press `Win + R`
2. Type: `shell:startup`
3. Create a shortcut to `jc_launcher.pyw` in that folder

---

## 🎮 How to Use JC from the Taskbar

### Using the System Tray Icon

1. **Click the JC icon** in your system tray (bottom-right corner)
2. You'll see these options:
   - **Open JC Chat** - Opens the web interface
   - **Run Command** - Opens CLI interface
   - **Check Status** - See if JC is online
   - **Settings** - Open configuration
   - **Quit** - Stop JC Agent

### Opening the Chat Interface

- Click **"Open JC Chat"** from the tray menu
- OR visit: `http://localhost:8000/chat` in your browser
- The beautiful chat UI will open automatically!

### Using Voice Commands (Future)

The `jc_voice.py` module is ready for voice integration:

```python
# Will be activated in future updates
# Natural 36-year-old male voice
# "Hey JC, what's on my schedule today?"
```

---

## 🔧 Troubleshooting

### JC Icon Doesn't Appear

**Solution 1:** Check if Python is in PATH

```bash
python --version
```

**Solution 2:** Run as administrator

```bash
# Right-click jc_launcher.pyw
# Select "Run as administrator"
```

**Solution 3:** Check dependencies

```bash
pip install --upgrade pystray Pillow requests
```

### API Not Starting

**Solution:** Check the port

```bash
# Kill any process using port 8000
netstat -ano | findstr :8000
taskkill /PID <pid_number> /F
```

### Chat Interface Not Loading

**Solution:** Verify the API is running

```bash
# Test health endpoint
curl http://localhost:8000/health
```

Should return something like (provider/model may vary):

```json
{
  "status": "ok",
  "provider": "openrouter",
  "model": "openai/gpt-4o-mini",
  "has_llm_key": false
}
```

---

## 🚀 Advanced Configuration

### Customize the System Tray Icon

Edit `jc_launcher.py` (the `.pyw` file is just a Windows-friendly stub):

```python
def create_icon_image(self, color="green"):
    # Change icon colors here
    # Options: "green", "yellow", "red"
```

### Change the API Port

Edit `.env`:

```
API_PORT=8000  # Change to your preferred port
```

### Add Custom Menu Items

Edit `jc_launcher.py`:

```python
menu = pystray.Menu(
    pystray.MenuItem("Open JC Chat", self.open_chat_interface, default=True),
    pystray.MenuItem("Run Command", self.run_command),
    # Add your custom items here!
    pystray.Menu.SEPARATOR,
    pystray.MenuItem("Quit", self.quit_app)
)
```

---

## 🎨 Customizing the Chat UI

The chat interface is in `templates/chat.html`. You can customize:

- **Colors:** Edit the gradient values
- **Avatar:** Change the "JC" text or add an image
- **Messages:** Modify the welcome message
- **Animations:** Adjust typing indicators and transitions

---

## 💡 Pro Tips

### Run JC Silently at Startup

The `.pyw` extension ensures no console window appears!

### Use Both Screens on Zenbook Duo

```python
# Keep JC on the second screen
# Drag the browser window to your preferred display
# The position will be remembered
```

### Quick Access Keyboard Shortcut

1. Right-click the JC shortcut in Startup folder
2. Properties → Shortcut tab
3. Set "Shortcut key" (e.g., `Ctrl+Alt+J`)

### Monitor Multiple Businesses

```python
# Edit config.json to add business contexts
{
  "businesses": [
    {"name": "Business 1", "focus": "E-commerce"},
    {"name": "Business 2", "focus": "Consulting"}
  ]
}
```

---

## 📱 Integration with Your Workflow

### Make JC Your Default AI Assistant

1. **Pin to Taskbar:**

   - Right-click the system tray icon
   - Select "Pin to taskbar"

2. **Browser Extension (Coming Soon):**

   - Quick access from any webpage
   - Highlight text → Ask JC

3. **Voice Activation (In Development):**
   - "Hey JC" wake word
   - Natural conversation mode

---

## 🔐 Security Best Practices

### Keep Your API Key Safe

```bash
# Never commit .env to git
# It's already in .gitignore
```

### Update Regularly

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Use Strong Passwords

When we add authentication:

```
JC_PASSWORD=your-strong-password-here
```

---

## 🎓 Next Steps

Now that JC is in your taskbar:

1. ✅ **Test the chat interface** - Click and start chatting!
2. ✅ **Check the API docs** - Visit `http://localhost:8000/docs`
3. ✅ **Explore features** - See `PRODUCTION_READY.md`
4. ✅ **Customize JC** - Edit personality in config
5. ✅ **Integrate tools** - Connect your business apps

---

## 🤝 Honoring JC's Memory

This agent represents the spirit of your wrestling partner JC:

- **Always truthful** - Never lies about capabilities
- **Pushes you forward** - Keeps you accountable
- **Smart and funny** - 36-year-old personality
- **Best partner** - Always has your back

Like a great wrestling partner, JC Agent will help you:

- Stay on task
- Push through challenges
- Celebrate victories
- Learn from setbacks

---

## 📞 Support

If you need help:

1. Check `QUICK_START.md` for quick fixes
2. Review `DEPLOYMENT.md` for detailed setup
3. See `PRODUCTION_READY.md` for advanced features
4. Open an issue on GitHub

**Remember:** JC is your AI business partner. Treat him like you would a real partner - honest communication leads to best results!

---

**Built with respect for JC's memory** 💪

_"Like a wrestling partner - always truthful, always pushing forward together."_
