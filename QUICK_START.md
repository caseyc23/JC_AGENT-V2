# 🚀 JC Agent - 2-Click Installation
**As Easy as Downloading from an App Store**

---

## 🎯 Get Started in 2 Minutes

### Step 1: Download

**Option A: Download ZIP** (Easiest)
1. Click the green "Code" button at the top of this page
2. Click "Download ZIP"
3. Extract the ZIP file anywhere on your computer

**Option B: Git Clone** (If you have Git)
```bash
git clone https://github.com/caseyc23/JC-agent-.git
```

### Step 2: Install

1. Open the extracted folder
2. **Double-click `EASY_INSTALL.bat`**
3. Press any key when prompted
4. Grab a coffee ☕ (installation takes 2-5 minutes)
5. Done! JC is installed

**That's it!** 🎉

---

## 📱 What the Installer Does (Automatically)

The `EASY_INSTALL.bat` file handles EVERYTHING:

✅ Checks if Python is installed (installs it if needed)  
✅ Installs all required packages  
✅ Creates a desktop shortcut "JC Agent"  
✅ Sets up auto-start on Windows login  
✅ Creates the configuration file  
✅ Launches JC for the first time  

You don't need to:
- Install Python manually
- Use command line/terminal
- Know anything about programming
- Configure anything complex

---

## 🔑 Add Your API Keys (One-Time Setup)

After installation, the installer will open a file called `.env` in Notepad.

**Just paste your API keys:**

```env
OPENROUTER_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here
```

### Where to Get API Keys?

1. **OpenRouter** (Required for AI)
   - Go to: https://openrouter.ai/
   - Sign up for free
   - Get your API key
   - Paste it in the .env file

2. **ElevenLabs** (Optional for natural voice)
   - Go to: https://elevenlabs.io/
   - Sign up
   - Get API key
   - Paste it in the .env file
   - *If you skip this, JC will use your computer's built-in voice*

**Save the file and close Notepad.**

---

## 🎮 How to Use JC

### Launch JC

**Option 1:** Double-click "JC Agent" icon on your desktop

**Option 2:** JC auto-starts when you log in to Windows (already set up!)

**Option 3:** Right-click the JC icon in your system tray (bottom-right corner)

### Talk to JC

**Voice:** Just say "Hey JC" and start talking!

**Text:** Type in the chat window

### What Can JC Do?

✅ **Research:** "Hey JC, research AI market trends"  
✅ **Tasks:** "Hey JC, add task: call John tomorrow"  
✅ **Schedule:** "Hey JC, schedule meeting at 3pm"  
✅ **Recommendations:** "Hey JC, what should I work on?"  
✅ **General Chat:** "Hey JC, tell me a joke"  

---

## ✅ System Requirements

- **OS:** Windows 10/11
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 2GB free space
- **Internet:** Required for AI features
- **Microphone:** Required for voice features

---

## ❓ Troubleshooting

### "Python not installing automatically"

**Solution:** Download Python manually:
1. Go to: https://www.python.org/downloads/
2. Download Python 3.11 or newer
3. Run installer
4. **CHECK** "Add Python to PATH"
5. Run `EASY_INSTALL.bat` again

### "Can't find JC Agent icon"

**Solution:** Check your system tray (bottom-right corner, near the clock). Click the ^ arrow to see hidden icons.

### "Voice not working"

**Solution 1:** Check microphone permissions in Windows Settings  
**Solution 2:** Use text mode instead (works without microphone)

### "Installation failed"

**Solution:** 
1. Right-click `EASY_INSTALL.bat`
2. Select "Run as Administrator"
3. Try again

---

## 📞 Need Help?

Check the detailed guides:
- **PRODUCTION_READY.md** - Technical documentation
- **DEPLOYMENT.md** - Advanced setup options
- **README.md** - Feature overview

Or open an issue: https://github.com/caseyc23/JC-agent-/issues

---

## 🎉 You're Ready!

**Installation Summary:**
1. ⬇️ Download ZIP
2. 📦 Extract folder
3. 👆 Double-click `EASY_INSTALL.bat`
4. ☕ Wait 2-5 minutes
5. 🔑 Add API keys to .env file
6. 🚀 Launch "JC Agent" from desktop

**That's it! No programming required.**

JC is now your AI business partner, ready to help you conquer the market.

---

**Built with ❤️ in memory of JC**
