# AI in the Terminal - Complete Guide

Welcome to the companion guide for NetworkChuck's "AI in the Terminal" video! This repository contains everything you need to follow along and master AI tools in the terminal.

## 📺 Watch the Video

[![AI in the Terminal - NetworkChuck](https://img.youtube.com/vi/MsQACpcuTkU/maxresdefault.jpg)](https://youtu.be/MsQACpcuTkU)

**[▶️ Watch on YouTube: AI in the Terminal](https://youtu.be/MsQACpcuTkU)**

## 🎯 What You'll Learn

This guide covers how to:

- Break free from browser-based AI limitations
- Use **Gemini CLI**, **Claude Code**, **Codex**, and **opencode** in your terminal
- Maintain persistent context across sessions with context files
- Deploy AI agents for specialized tasks
- Run multiple AI tools simultaneously on the same project
- Sync context files across different AI tools
- Build custom workflows for maximum productivity

## 🚀 Why Terminal AI?

**Browser AI problems:**

- Lost context after scrolling too far
- Multiple scattered chats across different platforms
- No file system access
- Copy/paste hell
- Limited control over your work

**Terminal AI advantages:**

- ✅ **Persistent context** - Your work lives in files, not chat windows
- ✅ **File system access** - Read and write files directly
- ✅ **Multiple AI tools** working together on the same project
- ✅ **Complete control** - Everything stored locally on your hard drive
- ✅ **Professional workflows** - Build custom agents and automation
- ✅ **10x faster** - No more context switching or copy/paste

## 📚 Guide Structure

### Getting Started

1. [Prerequisites](docs/01-prerequisites.md) - What you need before starting
2. [Quick Start](docs/02-quickstart.md) - Get up and running in 5 minutes

### Individual Tools

3. [Gemini CLI Guide](docs/03-gemini-cli.md) - Google's free terminal AI
4. [Claude Code Guide](docs/04-claude-code.md) - The most powerful terminal AI
5. [Codex Guide](docs/05-codex.md) - ChatGPT in your terminal
6. [opencode Guide](docs/06-opencode.md) - Open-source with local model support

### Advanced Workflows

7. [Context Files Explained](docs/07-context-files.md) - Master persistent context
8. [Multi-Tool Workflow](docs/08-multi-tool-workflow.md) - Use all tools simultaneously
9. [AI Agents Deep Dive](docs/09-agents.md) - Deploy specialized AI workers
10. [Output Styles & Customization](docs/10-customization.md) - Make AI work YOUR way

### Real-World Examples

11. [Productivity Workflows](docs/11-productivity-workflows.md) - Writing, research, planning
12. [Development Workflows](docs/12-development-workflows.md) - Coding and debugging
13. [Homelab & IT Workflows](docs/13-homelab-workflows.md) - Sysadmin tasks

### Reference

14. [Command Cheat Sheet](docs/14-cheat-sheet.md) - Quick reference for all commands
15. [Troubleshooting](docs/15-troubleshooting.md) - Common issues and solutions
16. [FAQ](docs/16-faq.md) - Frequently asked questions

## 🎬 Follow Along with the Video

Each section of this guide corresponds to a segment in the video:

- **0:00-1:26** - The Problem → [Prerequisites](docs/01-prerequisites.md)
- **1:27-4:14** - Gemini CLI Demo → [Gemini CLI Guide](docs/03-gemini-cli.md)
- **8:44-14:26** - Claude Code → [Claude Code Guide](docs/04-claude-code.md)
- **18:03-19:25** - Multi-Tool Workflow → [Multi-Tool Workflow](docs/08-multi-tool-workflow.md)
- **20:31-24:48** - Real Workflow Demo → [Productivity Workflows](docs/11-productivity-workflows.md)
- **26:32-30:00** - opencode → [opencode Guide](docs/06-opencode.md)

## ⚡ Quick Start (5 Minutes)

Want to start right now? Here's the fastest path:

```bash
# Install Gemini CLI (FREE)
npm install -g @google/generative-ai-cli

# Create a test project
mkdir my-ai-project
cd my-ai-project

# Launch Gemini
gemini

# Try your first command
# Ask: "Create a plan for learning Python"
```

[Continue to full Quick Start guide →](docs/02-quickstart.md)

## 💰 Pricing Breakdown

| Tool            | Free Tier                   | Paid Option                    | Best For                      |
| --------------- | --------------------------- | ------------------------------ | ----------------------------- |
| **Gemini CLI**  | ✅ Generous free tier       | Google One AI Premium ($20/mo) | Getting started, research     |
| **Claude Code** | ❌ No free tier             | Claude Pro ($20/mo)            | Professional work, agents     |
| **Codex**       | Limited free                | ChatGPT Plus ($20/mo)          | Analysis, high-level thinking |
| **opencode**    | ✅ Free (Grok/local models) | Provider subscription          | Flexibility, experimentation  |

**Chuck's Recommendation:** Start with Gemini CLI (free), then get Claude Pro if you can only choose one paid subscription.

## 🔗 Official Links

- [Gemini CLI Documentation](https://ai.google.dev/gemini-api/docs/cli)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs/claude-code)
- [Codex Documentation](https://platform.openai.com/docs/tools/codex)
- [opencode Repository](https://github.com/stackblitz-labs/opencode)

## 🛡️ Security Note (from the video)

**TwinGate Sponsor Message:** If you're giving AI access to your computer, make sure your remote access is secured properly. Traditional VPNs give full network access - consider zero-trust solutions like TwinGate for granular control.

[Learn about TwinGate](https://twingate.com/networkchuck)

## 🙏 Credits

**Created by:** NetworkChuck
**Video:** [AI in the Terminal](https://youtu.be/MsQACpcuTkU)
**Guide Maintained by:** NetworkChuck community

## 📝 Contributing

Found an error? Want to add a workflow? Submit a pull request or open an issue!

## ⚖️ License

This guide is provided as a free companion to the NetworkChuck video. Feel free to use, share, and modify for personal and educational use.

---

**Ready to get started?** → [Prerequisites](docs/01-prerequisites.md)

**Have questions?** → [FAQ](docs/16-faq.md)

**Need help?** → [Troubleshooting](docs/15-troubleshooting.md)

---

# docs/01-prerequisites.md

# Prerequisites

Before diving into AI terminal tools, let's make sure you have everything you need.

## Required

### 1. Terminal Access

You need a terminal/command line:

- **macOS**: Built-in Terminal app (Cmd+Space, type "Terminal")
- **Linux**: Any terminal emulator (usually Ctrl+Alt+T)
- **Windows**:
  - Windows Subsystem for Linux (WSL) - **Recommended**
  - PowerShell
  - Git Bash

#### Why WSL for Windows?

Chuck uses WSL (Ubuntu) in the video. It provides a Linux environment on Windows, which most terminal tools are optimized for.

**Install WSL:** [Chuck's WSL video](https://www.youtube.com/watch?v=[WSL_VIDEO_ID])

```powershell
# In PowerShell (Admin)
wsl --install
```

### 2. Node.js & npm

Most terminal AI tools are installed via npm (Node Package Manager).

**Check if you have it:**

```bash
node --version
npm --version
```

**Don't have it?** Install from [nodejs.org](https://nodejs.org/) (LTS version recommended)

### 3. A Google Account (for Gemini CLI)

- Any free Gmail account works
- No Google One AI Premium required for basic usage

### 4. AI Subscriptions (Optional but Recommended)

| Tool        | Free Option                 | Paid Option                  | Chuck's Take                         |
| ----------- | --------------------------- | ---------------------------- | ------------------------------------ |
| Gemini CLI  | ✅ Generous free tier       | Google One AI Premium $20/mo | "Start here - it's FREE"             |
| Claude Code | ❌ Requires Claude Pro      | Claude Pro $20/mo            | "This is my daily driver - worth it" |
| Codex       | Limited free                | ChatGPT Plus $20/mo          | "Good for analysis"                  |
| opencode    | ✅ Grok free / Local models | Various providers            | "Great for experimentation"          |

**Chuck's Recommendation:**

> "If you can only pay for one AI subscription, Claude Pro is the one I would choose."

## Recommended

### 5. Git (Optional but Useful)

Chuck treats his projects like code - version control for everything.

**Check if installed:**

```bash
git --version
```

**Install:**

- macOS: `xcode-select --install`
- Linux: `sudo apt install git` (Ubuntu/Debian)
- Windows: [git-scm.com](https://git-scm.com/)

### 6. Text Editor

You'll be editing context files. Any text editor works:

- **Terminal-based**: nano (easiest), vim, emacs
- **GUI**: VS Code, Sublime Text, Notepad++

### 7. Basic Terminal Skills

You should be comfortable with:

- Navigating directories (`cd`, `ls`/`dir`)
- Creating directories (`mkdir`)
- Basic file operations (`cat`, `nano`)
- Understanding file paths

**New to terminal?** Don't worry - Chuck walks through everything in the video!

## System Requirements

### Minimum

- **RAM**: 4GB (8GB recommended)
- **Storage**: 1GB free space
- **Internet**: Required for cloud AI models
- **OS**: macOS 10.15+, Ubuntu 20.04+, Windows 10+ (with WSL)

### Recommended for Local Models (opencode)

- **RAM**: 16GB+
- **Storage**: 10GB+ (for model files)
- **Ollama installed** (for local models)

## Permissions & Security

### What These Tools Can Access

⚠️ **Important Security Note:**

Terminal AI tools can:

- ✅ Read files in directories you open them in
- ✅ Write files to your system
- ✅ Execute bash commands
- ✅ Access your Obsidian vault (or any files)
- ✅ Run Python/bash scripts

This is POWERFUL but requires responsibility.

### Chuck's Security Tips

1. **Start in a test directory** - Don't open AI tools in your root or home directory initially
2. **Review file permissions** - Claude Code asks permission by default (good!)
3. **Use `--dangerously-skip-permissions` carefully** - Only when you trust what you're doing
4. **Secure your remote access** - If using AI on remote servers, use zero-trust tools like TwinGate

### Dangerous Mode Flag

Many tools have a "skip permissions" mode:

```bash
# Claude Code without safety checks
claude --dangerously-skip-permissions

# Use this ONLY when you know what you're doing
# Chuck uses it for speed in the video
```

## Quick Environment Check

Run this to verify you're ready:

```bash
# Check terminal
echo "Terminal works!"

# Check Node.js
node --version && npm --version

# Check available space
df -h .

# Create test directory
mkdir -p ~/ai-terminal-test
cd ~/ai-terminal-test
echo "Setup complete! Ready to install tools."
```

## What's Next?

✅ Prerequisites complete? → [Quick Start Guide](02-quickstart.md)

❓ Having issues? → [Troubleshooting](15-troubleshooting.md)

---

[← Back to README](../README.md) | [Next: Quick Start →](02-quickstart.md)

# docs/02-quickstart.md

# Quick Start Guide

Get up and running with AI in the terminal in **5 minutes**.

## Choose Your Path

### Path A: Free Start (Gemini CLI)

**Best for:** First-timers, budget-conscious users, testing the concept

### Path B: Power User Start (Claude Code)

**Best for:** Professionals ready to commit, agent users, serious workflows

## Path A: Free Start (Gemini CLI)

### Step 1: Install (30 seconds)

**Linux / macOS / WSL:**

```bash
npm install -g @google/generative-ai-cli
```

**macOS (Homebrew):**

```bash
brew install gemini-cli
```

**Permission error?** Add `sudo`:

```bash
sudo npm install -g @google/generative-ai-cli
```

### Step 2: Create Project (10 seconds)

```bash
mkdir ai-test-project
cd ai-test-project
```

### Step 3: Launch & Login (1 minute)

```bash
gemini
```

**First launch:**

1. Browser opens automatically
2. Sign in with Google account (any Gmail works!)
3. Click "Allow"
4. Return to terminal - you're in!

### Step 4: Your First Task (2 minutes)

**Try this:**

```bash
> How do I make the best cup of coffee?
```

**Watch it:**

- Search the web
- Craft response
- Return results

**Now try this (the magic part):**

```bash
> Research the top 5 coffee brewing methods.
  Create a comparison document called coffee-methods.md
```

**Gemini asks:** "Create file?" → Type `y`

**Check it out:**

```bash
ls
# You'll see: coffee-methods.md

cat coffee-methods.md
# Your research, saved locally!
```

### Step 5: Create Context File (1 minute)

**The game-changer:**

```bash
> /init
```

Gemini analyzes your project and creates `gemini.md`

**Now exit and reopen:**

```bash
exit
gemini
```

**Try this:**

```bash
> Continue working on the coffee project
```

**It remembers!** No re-explaining needed.

### ✅ You're Done! (5 minutes total)

**What you learned:**

- ✅ Gemini can create files
- ✅ Context files persist knowledge
- ✅ No more re-explaining your project
- ✅ Everything stored locally

**Next steps:**

- [Full Gemini CLI Guide](03-gemini-cli.md)
- [Understanding Context Files](07-context-files.md)

---

## Path B: Power User Start (Claude Code)

**Requirements:**

- Claude Pro subscription ($20/mo)
- Node.js installed

### Step 1: Install (30 seconds)

```bash
npm install -g @anthropic-ai/claude-code
```

**Permission error?**

```bash
sudo npm install -g @anthropic-ai/claude-code
```

### Step 2: Create Project (10 seconds)

```bash
mkdir my-project
cd my-project
```

### Step 3: Launch & Authenticate (1 minute)

```bash
claude
```

**First launch:**

1. Browser opens for authentication
2. Login with Claude Pro account
3. Approve directory access
4. Return to terminal

### Step 4: Create Context File (30 seconds)

```bash
> /init
```

Claude analyzes directory and creates `claude.md`

### Step 5: Create Your First Agent (2 minutes)

**This is where it gets powerful:**

```bash
> /agents
```

**Select:** "Create new agent"

**Choose:** "Project-specific agent"

**Name it:** `research-expert`

**Describe it:**

```
You are a research specialist. When given a topic:
1. Search for authoritative sources
2. Compile key findings
3. Create structured summaries
```

**Configure:**

- Tools: All tools
- Model: Sonnet

**Press Enter** to save

### Step 6: Deploy Your Agent (1 minute)

```bash
> @research-expert
  Research zero-trust network architecture.
  Create a summary document.
```

**Watch your agent work:**

- Fresh context window (200K tokens!)
- Independent research
- Returns results

**Check the file:**

```bash
ls
cat zero-trust-summary.md
```

### ✅ You're Done! (5 minutes total)

**What you learned:**

- ✅ Claude Code basics
- ✅ Agent creation
- ✅ Context persistence
- ✅ Agent deployment

**Next steps:**

- [Full Claude Code Guide](04-claude-code.md)
- [AI Agents Deep Dive](09-agents.md)
- [Output Styles Guide](10-customization.md)

---

## Quick Comparison

| Feature            | Gemini CLI   | Claude Code |
| ------------------ | ------------ | ----------- |
| **Cost**           | Free         | $20/mo      |
| **Setup Time**     | 2 min        | 3 min       |
| **Best Feature**   | Web research | AI agents   |
| **Context File**   | gemini.md    | claude.md   |
| **Learning Curve** | Easy         | Medium      |

**Chuck's recommendation:**

> "Start with Gemini CLI. It's FREE. But if you can afford one subscription, Claude Pro is the one I'd choose."

---

## Common First-Time Issues

### "Command not found"

```bash
# Reload your shell
source ~/.bashrc
# or
source ~/.zshrc

# Or close and reopen terminal
```

### "Permission denied"

```bash
# Run with sudo
sudo npm install -g [package-name]
```

### "Node.js not found"

Install from [nodejs.org](https://nodejs.org/) (LTS version)

### Context file not loading

```bash
# Verify you're in the right directory
pwd
ls gemini.md

# Recreate if needed
> /init
```

---

## What to Try Next

### Beginner Tasks

1. **Research task:** Ask Gemini to research a topic and create a summary
2. **Writing task:** Ask Claude to write a blog intro
3. **File organization:** Create a project structure and let AI populate it

### Intermediate Tasks

4. **Create an agent:** Make a specialized agent for your work
5. **Multi-session work:** Exit, reopen, verify context loads
6. **File manipulation:** Update existing files with AI help

### Advanced Tasks

7. **Multiple AIs:** Run Gemini and Claude simultaneously
8. **Context syncing:** Keep gemini.md and claude.md in sync
9. **Custom output style:** Create personality for your work

---

## 5-Minute Challenges

### Challenge 1: Coffee Research (Gemini)

**Goal:** Research, create file, reload context

```bash
mkdir coffee-challenge
cd coffee-challenge
gemini

> Research French press vs pour-over coffee.
  Create comparison-chart.md

> /init

exit
gemini

> Add a recommendation section to comparison-chart.md
  based on taste preferences
```

**Success if:** File created and AI remembers project without re-explaining

### Challenge 2: Agent Deploy (Claude)

**Goal:** Create and use an agent

```bash
mkdir agent-challenge
cd agent-challenge
claude

> /agents
# Create "homelab-helper" agent
# Instructions: "Expert in homelab hardware and networking"

> @homelab-helper
  What's the best budget NAS for a home lab?
```

**Success if:** Agent responds with detailed recommendations

### Challenge 3: Multi-Tool (Advanced)

**Goal:** Use Gemini and Claude together

```bash
mkdir multi-tool-challenge
cd multi-tool-challenge

# Terminal 1:
gemini
> Research the top 3 text editors
> /init

# Terminal 2:
claude
> /init
> Read the research and write a blog post intro
```

**Success if:** Claude reads Gemini's research file

---

## Next Steps by Interest

### I want to use AI for writing

→ [Productivity Workflows](11-productivity-workflows.md)
→ [Output Styles Guide](10-customization.md)

### I want to use AI for coding

→ [Development Workflows](12-development-workflows.md)
→ [Claude Code Guide](04-claude-code.md)

### I want to use AI for IT/homelab work

→ [Homelab Workflows](13-homelab-workflows.md)
→ [AI Agents Guide](09-agents.md)

### I want to understand the concepts deeply

→ [Context Files Explained](07-context-files.md)
→ [Multi-Tool Workflow](08-multi-tool-workflow.md)

---

## Questions?

**"Which tool should I start with?"**

- Free: Gemini CLI
- Professional: Claude Code
- Experimental: opencode

**"Do I need all three?"**

- No! Start with one
- Add others as you see benefits
- Chuck uses all three for different strengths

**"How much does this cost?"**

- Gemini CLI: FREE
- Claude Code: $20/mo (Claude Pro)
- opencode: Free (Grok) or various providers

**"Is this just for developers?"**

- NO! Chuck uses it for video scripts
- Works for writing, research, planning, any text work
- Coding is just one use case

---

**Ready to dive deeper?** → [Full Guide Navigation](../README.md)

**Having issues?** → [Troubleshooting](15-troubleshooting.md)

**Want the commands?** → [Cheat Sheet](14-cheat-sheet.md)

---

[← Back to Prerequisites](01-prerequisites.md) | [Next: Gemini CLI →](03-gemini-cli.md)

# docs/03-gemini-cli.md

# Gemini CLI Complete Guide

**Video Timestamp:** 1:27-4:14

Gemini CLI is Google's terminal AI tool. It's **FREE** (with generous limits) and perfect for getting started with terminal AI.

## Why Start with Gemini CLI?

Chuck's reasoning:

> "We're diving straight into Gemini CLI first. Why? Because it has a very generous free tier. That's right, you heard it - FREE."

**Best for:**

- ✅ Getting started (no credit card required)
- ✅ Research and web searches
- ✅ File creation and manipulation
- ✅ Learning context file workflows
- ✅ Writing and content creation

## Installation

### Linux / WSL / macOS

```bash
# Install globally with npm
npm install -g @google/generative-ai-cli
```

**Permission error?** Run with sudo:

```bash
sudo npm install -g @google/generative-ai-cli
```

### macOS (Alternative with Homebrew)

```bash
brew install gemini-cli
```

### Verify Installation

```bash
gemini --version
```

## First Launch

### 1. Create a Project Directory

Chuck's approach from the video:

```bash
# Create a new directory for your project
mkdir coffee-project
cd coffee-project

# Launch Gemini
gemini
```

**Why create a directory first?**

- Gemini can read/write files in the current directory
- Keeps your work organized
- Context files will be saved here

### 2. Initial Setup

First time you run `gemini`:

1. **Sign in with Google account** - Opens browser automatically
2. **Authorize the CLI** - Click "Allow"
3. **Return to terminal** - You're logged in!

```
     _____                 _       _    ____ _     ___
    / ____|               (_)     (_)  / ___| |   |_ _|
   | |  __  ___ _ __ ___  _ _ __  _  | |   | |    | |
   | | |_ |/ _ \ '_ ` _ \| | '_ \| | | |   | |    | |
   | |__| |  __/ | | | | | | | | | | | |___| |___ | |
    \_____|\___|_| |_| |_|_|_| |_|_|  \____|_____|___|

   Welcome to Gemini CLI!
```

## Basic Usage

### Your First Question

```bash
# Just start typing after the prompt
> How do I make the best cup of coffee in the world?
```

**What happens:**

1. Gemini searches the web (if relevant)
2. "Herding digital cats..." (loading message)
3. Response appears with formatting

### Key Interface Elements

```
> Your question here

Herding digital cats... 🐱 (processing)
Crafting the guide... ✨ (generating response)

[Response appears]

99% context left
```

**Context indicator:** Shows how much of your conversation window remains

## The Superpower: File System Access

### Creating Files

Chuck's demo from the video:

```bash
> I really want you to find the best way to make coffee.
  Research the top 10 sites, only reputable sources,
  and then compile the results into a document named best-coffee-method.
  And then create me a blog plan, just an outline.
```

**Gemini will ask:**

```
📝 Do you want me to create a file for you? (y/n)
```

Type `y` and hit enter.

**Result:**

```
Created files:
- best-coffee-method.md
- coffee-blog-outline.md
```

### Reading Files

Gemini automatically reads files in your current directory when relevant.

```bash
> What files are in this directory?
> Read the coffee blog outline and suggest improvements
> Add a new section to best-coffee-method.md about water temperature
```

## The Game-Changer: Context Files

### The `/init` Command

**Video Timestamp:** 4:00-4:14

This is THE feature that changes everything:

```bash
> /init
```

**What it does:**

1. Analyzes your current directory
2. Reads all files in the project
3. Creates a `gemini.md` context file
4. Saves project understanding for future sessions

**Gemini asks:**

```
📝 Create Gemini.md context file? (y/n)
```

Say yes!

### What's in gemini.md?

```bash
# View your context file
cat gemini.md
```

**Example content:**

```markdown
# Project: Coffee Blog Series

## Overview

This project involves researching and creating content about coffee brewing methods.

## Current Files

- best-coffee-method.md: Research compilation
- coffee-blog-outline.md: Blog series outline

## Project Goals

- Create comprehensive coffee brewing guide
- Develop blog series structure
```

### Using Context Across Sessions

**The magic moment from the video:**

1. Close your Gemini session (Ctrl+C or type `exit`)
2. Open a NEW Gemini session: `gemini`
3. Notice it loads `gemini.md` automatically

```
Loading context from gemini.md... ✓
100% context left (fresh session)
```

Now try:

```bash
> Write the intro for blog post 1 in the coffee series
```

**No additional context needed!** It knows what you're working on.

Chuck's reaction:

> "I didn't give it ANY context. It just knew. This is a new chat session."

## Real-World Workflow (from the video)

### Chuck's Actual Video Project

**Video Timestamp:** 5:48-6:09

```bash
# Navigate to video project
cd ~/Projects/531-ai-terminal

# Launch Gemini
gemini

# It loads the context file automatically
# Ask about project status
> Where are we at in the project?
```

**Gemini responds with:**

- Current phase
- Completed tasks
- Next steps
- Referenced documents

### Updating Context

```bash
> Update the gemini.md file with:
  - We completed the coffee brewing research
  - Next step is writing the first blog post
  - Decision made: Focus on pour-over method first
```

Gemini updates the file. Next session? It remembers everything.

## Available Commands

### View All Tools

```bash
> /tools
```

**Shows capabilities:**

- Web search
- File read/write
- Code execution
- Data analysis

### Common Commands

```bash
> /init           # Create context file
> /tools          # Show available tools
> /help           # Show help
> exit            # Exit Gemini (or Ctrl+C)
```

## Context Window Management

### What is Context?

Every AI has a "context window" - how much conversation it can remember.

**Browser AI:** Hides this from you (you hit limits unexpectedly)
**Gemini CLI:** Shows you exactly where you're at

```
99% context left  ← Plenty of room
50% context left  ← Halfway through
10% context left  ← Start new session or summarize
```

### When Context Gets Low

**Option 1:** Start a new session

```bash
# Exit current session
exit

# Start fresh
gemini
# Context file loads automatically!
```

**Option 2:** Ask Gemini to update context file

```bash
> Summarize our conversation and update gemini.md with key decisions
```

## Tips from Chuck

### 1. One Directory = One Project

```bash
# Good: Separate projects
~/coffee-project/      → One Gemini session
~/video-script/        → Another Gemini session
~/homelab-docs/        → Another Gemini session
```

### 2. Let Gemini Create Your Context File

Don't write `gemini.md` manually - let `/init` analyze your project.

### 3. Update Context as You Work

```bash
> Add to gemini.md: We decided to use the French press method instead
```

### 4. Context Files = Your Project Memory

Think of `gemini.md` as your project's brain:

- Current state
- Decisions made
- Files to reference
- Next steps

## Advanced: Multiple Gemini Sessions

**From the video:** Chuck opens multiple terminal tabs with different Gemini sessions.

```bash
# Terminal Tab 1: Coffee project
cd ~/coffee-project
gemini

# Terminal Tab 2: Video project
cd ~/video-script
gemini

# Terminal Tab 3: Homelab docs
cd ~/homelab-docs
gemini
```

Each session loads its own context file - no mixing!

## Example Workflows

### Research Workflow

```bash
mkdir research-project
cd research-project
gemini

> Research the top 5 enterprise NAS solutions for small business.
  Include pricing, features, and pros/cons.
  Create a comparison document called nas-comparison.md

> /init

> Based on the research, write a recommendation for a 10-person company
  with 5TB storage needs. Save as nas-recommendation.md
```

### Writing Workflow

```bash
mkdir blog-series
cd blog-series
gemini

> Help me plan a 5-part blog series about network security basics.
  Create an outline file.

> /init

> Write the introduction for part 1. Save as part-1-intro.md

# Later (new session):
gemini

> Review the part-1-intro and suggest improvements
```

### Obsidian Integration

**As mentioned in the video:**

```bash
# Navigate to your Obsidian vault
cd ~/Obsidian/MyVault
gemini

> Read my daily note for today and summarize key tasks

> Create a new note about [topic] with backlinks to related notes
```

Gemini can access ALL your Obsidian notes because they're just markdown files!

## Troubleshooting

### "Permission Denied" on Install

```bash
# Use sudo
sudo npm install -g @google/generative-ai-cli
```

### "Command not found: gemini"

```bash
# Reload your shell
source ~/.bashrc  # or ~/.zshrc

# Or close and reopen terminal
```

### Context File Not Loading

```bash
# Make sure you're in the right directory
pwd
ls gemini.md

# Recreate if needed
> /init
```

### Web Search Not Working

Gemini needs internet access. Check your connection.

## Pricing & Limits

### Free Tier

- **Generous usage limits** (exact limits vary)
- **Gemini 2.5 Pro model** (latest and greatest!)
- **Web search included**
- **No credit card required**

### Google One AI Premium ($20/mo)

- Higher rate limits
- Priority access
- Integrated with other Google services

**Chuck's take:**

> "Everyone has a Google account, and yes, this can be a free regular Gmail account."

## What's Next?

Now that you understand Gemini CLI, you're ready for the big leagues:

➡️ [Claude Code Guide](04-claude-code.md) - Chuck's daily driver with AI agents

Or explore:

- [Context Files Deep Dive](07-context-files.md)
- [Productivity Workflows](11-productivity-workflows.md)

---

[← Back to Prerequisites](01-prerequisites.md) | [Next: Claude Code →](04-claude-code.md)

# docs/04-claude-code.md

# Claude Code Complete Guide

**Video Timestamp:** 8:44-14:26

Claude Code is Anthropic's terminal AI tool - Chuck's daily driver. It's the most powerful tool covered in the video.

## Why Claude Code?

Chuck's endorsement:

> "I use Claude Code for pretty much everything. It's my default. And here's why: it has a feature that changes the game - **agents**."

> "If you can only pay for one AI subscription, Claude Pro is the one I would choose, especially for the last feature I'm going to show you." _(Output Styles)_

**Best for:**

- ✅ Professional workflows with AI agents
- ✅ Complex multi-step tasks
- ✅ Custom personalities (Output Styles)
- ✅ Planning mode for strategic thinking
- ✅ Maximum control and customization

**Requires:** Claude Pro subscription ($20/mo)

## Installation

### All Platforms (npm)

```bash
# Install globally
npm install -g @anthropic-ai/claude-code

# Or with sudo if needed
sudo npm install -g @anthropic-ai/claude-code
```

### Verify Installation

```bash
claude --version
```

## First Launch & Setup

### Basic Launch

```bash
# Navigate to your project
cd coffee-project

# Launch Claude Code
claude
```

### Initial Login

First time:

1. Prompted to login with Claude Pro account
2. Opens browser for authentication
3. Select directory permissions (approve access to current folder)

**Permission prompt:**

```
📁 Allow Claude Code to access /Users/you/coffee-project? (y/n)
```

**Chuck's take:** "It's security first. It asks permission for most things, and that's good."

## Interface Overview

### TUI (Terminal User Interface)

```
┌─ Claude Code ──────────────────────────────────────┐
│ 💭 Thinking...                                      │
│                                                     │
│ [Your question here]                                │
│                                                     │
│ [Claude's response]                                 │
│                                                     │
│ Context: 42% used (85,234 tokens)                  │
│ Mode: Normal | Thinking: ON                        │
└─────────────────────────────────────────────────────┘
```

### Toggle Thinking Mode

Press **TAB** to turn thinking on/off:

```
Thinking: OFF  →  Press TAB  →  Thinking: ON
```

**Thinking mode:** See Claude's internal reasoning process

## Context Files: claude.md

### Initialize Context

```bash
> /init
```

Same concept as Gemini, but creates `claude.md`:

```markdown
# Project: Coffee Project

## Overview

[Claude analyzes your directory and creates context]

## Files

- best-coffee-method.md
- coffee-blog-outline.md

## Goals

[Project objectives]
```

### View Context Usage

```bash
> /context
```

**Shows detailed breakdown:**

```
Context Usage: 85,234 tokens (42% used)

Loaded Files:
- claude.md (1,234 tokens)
- best-coffee-method.md (2,456 tokens)
- coffee-blog-outline.md (890 tokens)

Conversation: 80,654 tokens
```

**Chuck's observation:**

> "With Claude, that doesn't really matter too much as long as you know how to use their most powerful feature: **agents**."

## 🚀 Agents: The Game-Changer

### What Are Agents?

**From the video:**

> "Claude was like, 'Cool, I've got a task, but it's not for me. I'm gonna delegate this task to one of my employees or coworkers.' This is another Claude instance... He's giving him a fresh set of instructions and get this: a **fresh context window**."

**Key concept:** Agents are separate Claude instances with:

- ✅ Fresh context window (200K tokens each)
- ✅ Specialized instructions
- ✅ Custom tool access
- ✅ Independent memory

### Create Your First Agent

**Video Timestamp:** 10:41-11:20

```bash
> /agents
```

**Menu appears:**

```
┌─ Agent Management ─────────────────────────┐
│ 1. Create new agent                        │
│ 2. View agents                             │
│ 3. Edit agent                              │
│ 4. Delete agent                            │
└────────────────────────────────────────────┘
```

#### Step-by-Step Agent Creation

**From Chuck's demo:**

1. **Select "Create new agent"**

2. **Choose scope:**

   ```
   📁 Project-specific agent (coffee-project)
   🌍 Personal agent (available everywhere)
   ```

   Chuck chooses: "Just this project"

3. **Describe the agent:**

   ```
   Name: homelab-guru
   Description: Expert in homelab hardware, networking, and infrastructure
   ```

4. **Configure:**

   ```
   Tools: [x] All tools
   Model: Sonnet 4.5
   Color: Auto
   ```

5. **Press Enter to save, ESC to exit**

**Agent created!** 🎉

### Using Agents

#### Deploy an Agent

**Chuck's example:**

```bash
> @homelab-guru
  Research document and create a buying guide.
  Make sure you reference the research we made in @nas-rec-folder
```

**What happens:**

1. Main Claude sees the task
2. Delegates to `homelab-guru` agent
3. Agent gets fresh 200K context window
4. Agent works independently
5. Returns results to main Claude

**Visual in terminal:**

```
┌─ Agent: homelab-guru ──────────────────────┐
│ 🔍 Researching NAS solutions...             │
│ 📊 Context: 15% used (30,000 tokens)       │
└────────────────────────────────────────────┘
```

#### Reference Files with @

```bash
# Reference specific files
> @homelab-guru create a summary of @nas-comparison.md

# Reference folders
> @homelab-guru review all documents in @research-folder
```

### Multiple Agents Simultaneously

**Video Timestamp:** 13:50-14:04

**Chuck's incredible demo:**

```bash
> Launch @homelab-guru to research the best proxmox servers.
  At the same time, use a general agent to find the best pizza place in Dallas.
  And another @homelab-guru to find the best graphics card for gaming.
  Put it all together in a comprehensive report.
```

**What happens:**

- 🤖 Agent 1: Proxmox server research
- 🍕 Agent 2: Pizza recommendations
- 🎮 Agent 3: Graphics card research
- 📊 Main Claude: Compiles all results

**Chuck's reaction:**

> "I feel so powerful right now. This is so fun!"

### Pre-Built Agents from the Video

#### 1. Homelab Guru

```bash
Agent: homelab-guru
Purpose: Network equipment, server recommendations, homelab setup
Tools: All
Model: Sonnet
```

#### 2. Brutal Critic

```bash
Agent: brutal-critic
Purpose: Ruthlessly review scripts/outlines against NetworkChuck framework
Personality: Intentionally harsh, framework-focused
Tools: Read, Web Search
Model: Sonnet
```

**Chuck's use case:**

> "I want it to be super mean. So that when it DID tell me I did a good job, I knew it was good."

#### 3. Gemini Research Agent

```bash
Agent: gemini-research
Purpose: Use Gemini CLI in headless mode for research tasks
Tools: Bash (to run gemini -p)
Model: Sonnet
```

**Chuck's example:**

```bash
> @gemini-research find the best AI terminal videos on YouTube
```

Agent runs:

```bash
gemini -p "find the top 10 AI terminal videos on YouTube"
```

## 🎨 Output Styles: Custom Personalities

**Video Timestamp:** 16:31-17:27

**Chuck's discovery:**

> "I'm embarrassed to say I just found this out while making this video."

### What Are Output Styles?

**System prompts** that control:

- How Claude responds
- Persona and tone
- Domain expertise
- Task-specific behaviors

### View Output Styles

```bash
> /output-style
```

**Default styles:**

```
📋 Available Output Styles:
- code (default) - Optimized for software development
- concise - Brief, to-the-point responses
- detailed - Comprehensive explanations
```

### Create Custom Output Style

**Chuck's demo:**

```bash
> /output-style new
```

**Prompt:**

```
Name: homelab-expert
Description: You are a homelab expert designed to help me create
the best homelab possible.
```

**More complex example (Chuck's actual script-writing style):**

```bash
Name: networkchuck-scriptwriter
Description:
You are an AI assistant specialized in writing NetworkChuck YouTube scripts.
You understand:
- Hook psychology and CTR optimization
- Viewer retention patterns
- NetworkChuck's energetic, coffee-fueled voice
- Educational entertainment balance
- The "you" voice (viewer as hero)

Always:
- Keep lines short and punchy
- Add coffee transitions between segments
- Use "Let's go!" at key moments
- Explain complex topics simply
- Add pattern breaks every 20-40 seconds
```

### Activate Output Style

```bash
> /output-style

# Select from list, or it activates on next launch
```

**Verify:**

```
Current Output Style: networkchuck-scriptwriter ✓
```

**Chuck's actual usage:**

> "I'm using the output style right now to make this video. This is what it looks like. It's pretty intense, optimized for what I do."

### Scope: Project vs Global

**Project-specific:**

- Lives in `.claude/output-styles/` in current project
- Only available in this project

**Global:**

- Lives in `~/.config/claude/output-styles/`
- Available in all projects

## 🎯 Planning Mode

**Video Timestamp:** 17:39-17:54

### Activate Planning Mode

Press **Shift+Tab** to toggle:

```
Mode: Normal  →  Shift+Tab  →  Mode: Planning
```

### How It Works

1. You give Claude a task
2. Claude creates a detailed plan
3. You review and approve
4. Claude executes the plan

**Example:**

```bash
> Refactor the authentication system to use JWT tokens
```

**Planning mode response:**

```
📋 Plan:
1. Review current authentication implementation
2. Install jsonwebtoken package
3. Create JWT utility functions
4. Update login endpoint
5. Add token verification middleware
6. Update protected routes
7. Add token refresh logic
8. Update tests

Approve this plan? (y/n/edit)
```

Type `y` to execute, or `edit` to modify.

**Chuck's take:**

> "This will put a very well thought-out plan together, and then you approve it. And then it just does it."

## 🎮 Advanced Features

### Resume Previous Session

**From the video:** "Yes, you can do that."

```bash
# Resume last session
claude -r

# Choose from recent sessions
```

### Dangerous Mode (Skip Permissions)

**Video Timestamp:** 14:36-14:52

```bash
# Launch without permission prompts
claude --dangerously-skip-permissions
```

⚠️ **Warning:** Claude will execute actions without asking

**Chuck's take:**

> "This is Claude without training wheels."

**Use when:**

- You trust your instructions completely
- You want maximum speed
- You're doing repetitive tasks

### Combine Flags

```bash
# Resume previous session + dangerous mode
claude -r --dangerously-skip-permissions
```

## Real-World Workflows

### 1. Outline Review with Brutal Critic

**Video Timestamp:** 12:56-13:05

```bash
# Working on a YouTube script
> @brutal-critic review my outline at @outline.md
```

**Agent launches with fresh context:**

- Reads outline.md
- Applies NetworkChuck framework
- Returns ruthless critique

**Chuck's result:** "8.2/10 - Not bad!"

### 2. Cross-Tool Research

**Video Timestamp:** 16:06-16:17

```bash
> Find the best AI terminal videos on YouTube.
  Use the @gemini-research agent.
```

**What happens:**

- Claude deploys gemini-research agent
- Agent runs: `gemini -p "search YouTube for AI terminal videos"`
- Gemini returns top 10 results
- Claude compiles into report

**Chuck's observation:**

> "We're having an AI use an AI right now!"

### 3. Context-Protected Reviews

**Video Timestamp:** 12:27-12:35

**Problem:** Your main conversation is 85K tokens deep with the outline

**Solution:** Deploy fresh agent with 200K tokens

```bash
> @brutal-critic review my current work
```

**Why this matters:**

- Main context: 85K tokens (cluttered with iterations)
- Agent context: 0K tokens (fresh eyes)
- No bias from previous conversation

**Chuck's take:**

> "I want a fresh cup of coffee. Ready to go. Fresh eyes."

## Tips from Chuck

### 1. Protect Your Context

> "I use agents all the time to **protect my context** and avoid any kind of weird bias."

**Strategy:** Delegate reviews, research, and analysis to agents

### 2. One Project = One Claude Session

```bash
# Terminal Tab 1: Video script
cd ~/video-project
claude

# Terminal Tab 2: Homelab docs
cd ~/homelab-project
claude
```

### 3. Name Agents by Function

**Good names:**

- `homelab-guru`
- `brutal-critic`
- `research-assistant`
- `code-reviewer`

**Bad names:**

- `agent1`
- `test`
- `bob`

### 4. Give Agents Specific Instructions

**Vague:**

```
You are helpful.
```

**Specific:**

```
You are a homelab expert specializing in enterprise NAS solutions.
When making recommendations:
- Consider budget constraints
- Explain technical trade-offs
- Provide specific product recommendations
- Include pricing and availability
```

## Agent Management

### List All Agents

```bash
> /agents
```

**View:**

- Project agents (local to current directory)
- Personal agents (available everywhere)

### Edit an Agent

```bash
> /agents
# Select "Edit agent"
# Choose agent
# Modify instructions
```

### Delete an Agent

```bash
> /agents
# Select "Delete agent"
# Confirm
```

## Hidden Features

### Paste Images

**From the video:**

> "You can paste images into your terminal."

```bash
# In Claude Code session
> Analyze this screenshot
[Paste image]
```

### Custom Hooks

**From the video mention:**

> "They have prompts, hooks, custom status lines."

Advanced: Create event-triggered actions

### Status Line Customization

Customize your terminal status bar with project info

## Troubleshooting

### "Not authorized" Error

Ensure you have:

1. Active Claude Pro subscription
2. Logged in correctly: `claude auth login`

### Agent Not Working

```bash
# Verify agent exists
> /agents

# Check agent configuration
> /agents
# Select "View agents"
```

### Context Not Loading

```bash
# Recreate context file
> /init
```

### Permission Denied on Files

```bash
# Relaunch with directory approval
claude
# Approve file access when prompted
```

## Pricing

**Requires:** Claude Pro ($20/mo)

**Includes:**

- Access to Claude Code terminal tool
- Use your existing web subscription
- No separate API key needed
- Unlimited-ish usage (fair use policy)

**Chuck's recommendation:**

> "If you already pay for Claude Pro, which starts at like 20 bucks a month, you can log into the terminal with this subscription and use it. So yeah, you don't have to use API keys."

## Comparison: Gemini vs Claude

| Feature            | Gemini CLI      | Claude Code       |
| ------------------ | --------------- | ----------------- |
| **Price**          | Free            | $20/mo            |
| **Agents**         | ❌ No           | ✅ Yes            |
| **Output Styles**  | ❌ No           | ✅ Yes            |
| **Planning Mode**  | ❌ No           | ✅ Yes            |
| **Context Window** | 200K            | 200K (per agent!) |
| **Best For**       | Getting started | Professional work |

**Chuck's verdict:**

> "Gemini's not even close to the best one."

## What's Next?

**Master these features:**

1. Create 2-3 specialized agents for your work
2. Design a custom output style
3. Practice delegating tasks to agents
4. Try planning mode on complex tasks

**Then explore:**
➡️ [Multi-Tool Workflow](08-multi-tool-workflow.md) - Use Claude + Gemini + Codex simultaneously

---

[← Back to Gemini CLI](03-gemini-cli.md) | [Next: Codex →](05-codex.md)

# docs/05-codex.md

# Codex (ChatGPT CLI) Guide

**Video mentions:** 18:07-18:28, 18:54-19:13

Codex is OpenAI's terminal tool that brings ChatGPT to the command line.

## Overview

**Chuck's usage:**

> "I find ChatGPT is very good at analyzing things from a high view. Gemini and Claude are very good at the work, the deep work."

**Best for:**

- High-level analysis
- Strategic thinking
- Quality review
- Different perspective from Claude/Gemini

## Installation

```bash
npm install -g @openai/codex-cli

# Or follow official OpenAI documentation
```

## Basic Usage

### Launch

```bash
cd your-project
codex
```

### Context File

Uses **agents.md** (same as opencode)

```bash
> /init
```

Creates `agents.md` in your project directory.

## Chuck's Workflow

**In multi-tool setup:**

```bash
# Terminal 1: Claude (writing)
claude
> Write a hook for this video, authority angle

# Terminal 2: Gemini (research)
gemini
> Write a hook on discovery angle

# Terminal 3: Codex (review)
codex
> Review both hooks and compare their strengths
```

**Chuck's observation:**

> "They're all using the same context, different roles."

## Role in Multi-Tool Workflow

### When to Use Codex

**✅ Use Codex for:**

- Reviewing Claude's output
- High-level strategy
- Comparing approaches
- Ensuring clarity
- Catching issues Claude/Gemini miss

**❌ Don't use Codex for:**

- Deep technical writing (Claude better)
- Current web research (Gemini better)
- Long-form content creation

### Typical Workflow

```bash
# 1. Claude creates
claude
> Write a technical blog post about ZFS

# 2. Gemini researches
gemini
> Verify technical accuracy and find recent benchmarks

# 3. Codex reviews
codex
> Review the blog post at blog.md
  Check: clarity, flow, technical accuracy, audience fit
```

## Context File Syncing

**Important:** Codex uses `agents.md`

**Sync with other tools:**

```bash
# In Claude terminal
claude
> Sync claude.md content to gemini.md and agents.md
```

**Now all three tools share context!**

## Pricing

**Requires:** ChatGPT Plus ($20/mo) or API key

- ChatGPT Plus: Use existing subscription
- API key: Pay per token usage

## Comparison

| Feature          | Codex     | Claude Code | Gemini CLI |
| ---------------- | --------- | ----------- | ---------- |
| **Strength**     | Analysis  | Deep work   | Research   |
| **Context File** | agents.md | claude.md   | gemini.md  |
| **Cost**         | $20/mo    | $20/mo      | Free       |
| **Best For**     | Review    | Creating    | Research   |

## Tips from Chuck

### 1. Use for High-Level Analysis

> "ChatGPT is very good at analyzing things from a high view."

**Good prompts:**

```bash
> Review this architecture and identify weaknesses
> Is this explanation clear for beginners?
> Compare these two approaches strategically
```

### 2. Last Step in Pipeline

```
Claude writes → Gemini verifies → Codex reviews
```

### 3. Different Perspective

When Claude and Gemini agree, ask Codex for a third opinion:

```bash
> Claude and Gemini both recommend approach A.
  What do you think? Any risks we're missing?
```

## Official Documentation

[OpenAI Codex Documentation](https://platform.openai.com/docs/tools/codex)

## What's Next?

**Understand multi-tool workflows:**

➡️ [Multi-Tool Workflow Guide](08-multi-tool-workflow.md)

➡️ [Context Files Explained](07-context-files.md)

---

[← Back to Claude Code](04-claude-code.md) | [Next: opencode →](06-opencode.md)

# docs/06-opencode.md

# opencode Complete Guide

**Video Timestamp:** 26:32-30:00

opencode is the **open-source** terminal AI tool that supports multiple providers and local models.

## Why opencode?

**Chuck's take:**

> "There's a tool that's actually open-source. You can use any model you want with this open-source alternative, and it might be the best tool of all of them. I'm still testing it."

**Key advantages:**

- ✅ **Open source** - Community-driven development
- ✅ **Multiple providers** - Claude, OpenAI, Grok, Gemini, local models
- ✅ **Grok free tier** - Free usage with X/Twitter integration
- ✅ **Local models** - Run Ollama models completely offline
- ✅ **Claude Pro login** - Use existing subscription (like Claude Code)
- ✅ **Session sharing** - Share your AI sessions with others
- ✅ **Timeline feature** - Time-travel through conversations

**Best for:**

- Experimentation with different models
- Local/offline AI usage
- Cost optimization (mix free + paid)
- Open-source preference

## Installation

### Quick Install (Recommended)

```bash
curl -fsSL https://opencode.sh/install.sh | sh
```

**Reload your shell:**

```bash
source ~/.bashrc
# or for zsh:
source ~/.zshrc
```

### Manual Install (npm)

```bash
npm install -g @opencodenet/cli
```

### Verify Installation

```bash
opencode --version
```

## First Launch

### Basic Launch

```bash
cd your-project
opencode
```

**First time experience:**

- Launches with **Grok Fast** model by default (FREE!)
- Beautiful TUI interface
- Reads current directory automatically

### The Interface

```
┌─ opencode ──────────────────────────────────────────┐
│                                                      │
│  🚀 Welcome to opencode                              │
│  Model: grok-fast-1                                  │
│                                                      │
│  > Your prompt here                                  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Chuck's reaction:**

> "Nice TUI, terminal user interface."

## Free Tier: Grok Integration

### What is Grok?

**From the video:**

- X/Twitter's AI model
- Free tier available through opencode partnership
- Fast inference
- Good for general tasks

### Using Grok (Default)

**Just launch opencode:**

```bash
opencode
```

**Already on Grok Fast by default!**

```bash
> Help me plan a homelab project
```

**No API key needed!** Partnership with X provides free access.

**Chuck's take:**

> "They have a deal with Grok AI that allows you to use this for free for a while."

## Model Management

### View Available Models

```bash
# In opencode session
> /model
```

**Shows:**

```
Available Models:
- grok-fast-1 (FREE - current)
- claude-sonnet-4
- claude-opus-4
- gpt-4
- gemini-2.5-pro
- llama-3.2 (local via Ollama)
```

### Switch Models

**Video Timestamp:** 27:57-28:21

```bash
> /model
# Select from list

# Or specify directly
> /model claude-sonnet-4
> /model grok-fast-1
> /model llama-3.2
```

**Chuck switching live:**

```bash
> /model claude-sonnet-4
# "Cool, what's our next step?"

> /model grok-fast-1
# "While it's doing that, I can do /sessions"
```

### Model Switching Mid-Conversation

**The power move:**

```bash
# Start with Claude for deep thinking
> /model claude-sonnet-4
> Create a comprehensive system architecture

# Switch to Grok for quick follow-up
> /model grok-fast-1
> Summarize that in bullet points
```

**Chuck's observation:**

> "I can switch models midway."

## Provider Authentication

### Login with Claude Pro

**Video Timestamp:** 28:35-28:46

```bash
opencode auth login
```

**Select:** "Anthropic"

**Browser opens:**

1. Login with Claude Pro account
2. Copy authorization code
3. Paste in terminal

**Now you have access to:**

- Claude Sonnet 4.5
- Claude Opus 4
- Uses your existing subscription!

**Chuck's endorsement:**

> "The fact that you can log in and use your Claude Pro subscription... that's next level."

### Other Providers

**OpenAI (ChatGPT):**

```bash
opencode auth login
# Select: OpenAI
# Enter API key
```

**Google (Gemini):**

```bash
opencode auth login
# Select: Google
# Authenticate with Google account
```

### Check Auth Status

```bash
opencode auth whoami
```

## Local Models with Ollama

### Prerequisites

**Install Ollama first:**

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows (WSL)
curl -fsSL https://ollama.com/install.sh | sh
```

### Pull a Model

**Chuck uses Llama 3.2:**

```bash
ollama pull llama-3.2
```

**Check available models:**

```bash
ollama list
```

### Configure opencode for Local Models

**Video Timestamp:** 27:40-28:01

**Edit config:**

```bash
nano ~/.config/opencode/opencode.jsonc
```

**Add model configuration:**

```jsonc
{
  "model": "llama-3.2",
  "provider": "ollama"
}
```

**Save and exit**

### Use Local Model

```bash
opencode
# Loads with llama-3.2

# Or switch in session
> /model llama-3.2
```

**Chuck trying it:**

> "Hey cool, Llama works!"

**Benefits:**

- ✅ Completely offline
- ✅ No API costs
- ✅ Privacy (data never leaves machine)
- ✅ Great for sensitive work

## Advanced Features

### Session Sharing

**Video Timestamp:** 29:19-29:33

**Share your conversation:**

```bash
> /share
```

**Returns:** URL copied to clipboard

**Paste in browser:**

```
https://opencode.net/session/abc123...
```

**Chuck's amazement:**

> "I can share my session with people. That's pretty neat."

**Live demo feature:**

> "Wait, is it live? Oh, you can share your session with people!"

### Session Timeline

**Video Timestamp:** 29:33-29:44

**Time-travel through conversation:**

```bash
> /timeline
```

**Shows:**

```
Session Timeline:
├─ 10:23 - Started session
├─ 10:25 - Asked about homelab setup
├─ 10:28 - Created plan document
├─ 10:30 - Switched to Llama 3.2
└─ 10:32 - Generated cost analysis
```

**Select any point to restore:**

```bash
# Click on timestamp
# Session rewinds to that point
```

**Chuck's reaction:**

> "We can jump back in time and restore. I want that in real life!"

### Session Management

**View all sessions:**

```bash
> /sessions
```

**Shows:**

```
Recent Sessions:
1. homelab-planning (active)
2. blog-writing (1 hour ago)
3. research-project (yesterday)
```

**Switch sessions:**

```bash
# Select from list
# Or start new:
> /sessions
# Choose "New session"
```

### Headless Mode

**Run opencode without TUI:**

```bash
opencode --headless "Write a blog intro about ZFS"
```

**Output goes directly to stdout**

### Export Session

**From video mention:**

```bash
opencode --export-session session-id
```

**Exports as JSON data**

## Context Files: agents.md

### Initialize Context

```bash
> /init
```

**Creates:** `agents.md` (not agent.md or opencode.md)

**Why "agents.md"?**

- opencode follows proposed standard
- Claude Code's Codex uses agents.md
- Trying to standardize across tools

### Sync with Other Tools

**When using opencode + Claude + Gemini:**

```bash
# Use Claude to sync all three
claude
> Sync claude.md content to gemini.md and agents.md
```

**Chuck's workflow:**

> "They're trying to make it a standard. They're all the same."

## Feature Showcase (from video)

### 1. Agents Support

**Video Timestamp:** 29:45-29:51

```bash
opencode agents create my-agent
```

**Similar to Claude Code agents**

### 2. Headless Server

```bash
opencode server start
```

**Then attach from another terminal:**

```bash
opencode server attach
```

### 3. Session Export

```bash
opencode export --format json > session.json
```

### 4. Rich Formatting

- Markdown rendering
- Code syntax highlighting
- Table support

## Real-World Usage

### Cost Optimization Strategy

**Mix free and paid models:**

```bash
# Free: Grok for research
> /model grok-fast-1
> Research top 5 NAS options

# Paid: Claude for writing
> /model claude-sonnet-4
> Write a comprehensive buying guide based on research

# Free: Local for experimentation
> /model llama-3.2
> Generate 5 alternative titles
```

### Privacy-First Workflow

**Sensitive work uses local models:**

```bash
# Switch to local
> /model llama-3.2

# Work on sensitive documents
> Review this confidential file...

# No data sent to cloud ✓
```

### Model Comparison

**Get multiple perspectives:**

```bash
# Ask Claude
> /model claude-sonnet-4
> What's the best homelab storage solution?

# Save Claude's answer, then ask Grok
> /model grok-fast-1
> What's the best homelab storage solution?

# Compare responses
```

## Chuck's Real Usage

**From the video:**

```bash
cd ~/Projects/531-ai-terminal
opencode

# It loads agents.md automatically
> Where are we in the project?

# Grok responds with project status
```

**Then switches models:**

```bash
> /model claude-sonnet-4
> Continue working on the script
```

**All in one session, same context!**

## Configuration

### Config File Location

```bash
~/.config/opencode/opencode.jsonc
```

### Example Configuration

```jsonc
{
  "model": "claude-sonnet-4",
  "provider": "anthropic",
  "theme": "dark",
  "thinking": true,
  "temperature": 0.7,
  "maxTokens": 4096
}
```

### Edit Config

```bash
nano ~/.config/opencode/opencode.jsonc
```

## Command Reference

### In-Session Commands

```bash
/model              # Change model
/share              # Share session
/timeline           # View timeline
/sessions           # Manage sessions
/init               # Create agents.md
/help               # Show help
exit                # Exit opencode
```

### CLI Commands

```bash
opencode                    # Launch
opencode auth login         # Authenticate provider
opencode auth whoami        # Check auth status
opencode --version          # Version info
opencode --headless "..."   # Headless mode
opencode --help             # Help
```

## Troubleshooting

### "Command not found: opencode"

```bash
# Reload shell
source ~/.bashrc
source ~/.zshrc

# Or reinstall
curl -fsSL https://opencode.sh/install.sh | sh
```

### Local Model Not Working

```bash
# Verify Ollama is running
ollama list

# Pull model if missing
ollama pull llama-3.2

# Check config
cat ~/.config/opencode/opencode.jsonc
```

### Authentication Issues

```bash
# Re-authenticate
opencode auth login

# Check status
opencode auth whoami

# Clear auth and retry
rm -rf ~/.config/opencode/auth
opencode auth login
```

### Context File Not Loading

```bash
# Verify file exists
ls agents.md

# Recreate
> /init
```

## Comparison: opencode vs Others

| Feature                | opencode    | Claude Code    | Gemini CLI     |
| ---------------------- | ----------- | -------------- | -------------- |
| **Cost**               | Free (Grok) | $20/mo         | Free           |
| **Local Models**       | ✅ Yes      | ❌ No          | ❌ No          |
| **Multiple Providers** | ✅ Yes      | ❌ Claude only | ❌ Gemini only |
| **Session Sharing**    | ✅ Yes      | ❌ No          | ❌ No          |
| **Timeline Feature**   | ✅ Yes      | ❌ No          | ❌ No          |
| **Agents**             | ✅ Yes      | ✅ Yes         | ❌ No          |
| **Open Source**        | ✅ Yes      | ❌ No          | ❌ No          |

**Chuck's verdict:**

> "It might be the best tool of all of them. I'm still testing it."

## When to Use opencode

**✅ Choose opencode for:**

- Experimentation with different models
- Cost optimization (mix free/paid)
- Privacy needs (local models)
- Open-source preference
- Model comparison workflows
- Session sharing needs

**❌ Choose Claude Code instead for:**

- Production workflows (more mature)
- Complex agent setups
- Output styles
- Planning mode

**❌ Choose Gemini CLI instead for:**

- Simplest setup
- Pure Google ecosystem
- Getting started (easiest learning curve)

## The Developers

**From Chuck's mention:**

> "What's fun is I've been following these guys on Twitter before they started making this code. This guy Dax, these guys are killing it."

**GitHub:** [stackblitz-labs/opencode](https://github.com/stackblitz-labs/opencode)

**Community:** Active development, responsive maintainers

## Future Potential

**Why Chuck is excited:**

1. **Open source** → Community contributions
2. **Multi-provider** → Use best model for each task
3. **Local models** → Privacy + cost control
4. **Standards push** → agents.md adoption
5. **Feature velocity** → Rapid development

**Chuck's strategy:**

> "If a new, greater, better AI comes out, I'm ready for it."

opencode enables this with provider flexibility.

## What's Next?

**Get started with opencode:**

1. Install it (2 minutes)
2. Try Grok free tier (no auth needed)
3. Experiment with model switching
4. Try local models if privacy-conscious
5. Use for cost-optimized workflows

**Then explore:**
➡️ [Multi-Tool Workflow](08-multi-tool-workflow.md) - Use opencode with Claude/Gemini

➡️ [Command Cheat Sheet](14-cheat-sheet.md) - Quick opencode commands

---

[← Back to Codex](05-codex.md) | [Next: Context Files →](07-context-files.md)

# docs/07-context-files.md

# Context Files Explained

**The Secret Weapon of Terminal AI**

Context files are THE feature that makes terminal AI 10x better than browser AI. This guide explains everything.

## The Browser Problem

**Chuck's frustration:**

> "You're in the browser. You're asking questions, research mode. You're diving deep into a project. Can't even see your scroll bar anymore. And this is your fifth chat because ChatGPT lost its context or its mind."

**What goes wrong:**

- 📜 Infinite scrolling (lose track of conversation)
- 🗂️ Multiple scattered chats (context split across 20 tabs)
- 📋 Copy/paste chaos (trying to save important parts)
- 🔄 Re-explaining context every new chat
- 💾 No way to "save" your project state

## The Terminal Solution: Context Files

### What Are Context Files?

**Simple answer:** Markdown files that tell AI what your project is about.

**Each tool has its own:**

- Gemini CLI: `gemini.md`
- Claude Code: `claude.md`
- Codex: `agents.md`

### The Magic

**Every time you launch the AI in a directory:**

1. Tool looks for its context file
2. Loads it automatically
3. Immediately understands your project
4. No re-explaining needed!

**Chuck's aha moment:**

> "It can access your Obsidian vault, all your notes, because those are just files sitting there on your hard drive."

## How Context Files Work

### Visual Representation

```
my-project/
├── gemini.md          ← Gemini reads this
├── claude.md          ← Claude reads this
├── agents.md          ← Codex reads this
├── project-files/
│   ├── research.md
│   ├── outline.md
│   └── draft.md
```

**When you launch:**

```bash
cd my-project
gemini

# Loading context from gemini.md... ✓
```

### Anatomy of a Context File

**Example `claude.md`:**

```markdown
# Project: Coffee Blog Series

## Overview

Creating a comprehensive blog series about coffee brewing methods,
targeted at home coffee enthusiasts.

## Current Phase

Research complete, writing first draft

## Key Files

- research/coffee-methods.md - Compiled research
- outlines/series-outline.md - 5-part series structure
- drafts/part-1.md - First draft (in progress)

## Decisions Made

- Focus on pour-over, French press, and espresso
- Avoid super technical chemistry details
- Include beginner-friendly equipment recommendations

## Next Steps

1. Complete part-1.md draft
2. Get feedback on tone/style
3. Create equipment recommendations list

## Reference Documents

- Brand guidelines in guidelines.md
- Target audience research in audience-profile.md
```

### What to Include

**✅ DO include:**

- Project overview
- Current phase/status
- Key files and their purpose
- Major decisions made
- Next steps
- Links to reference documents

**❌ DON'T include:**

- Full project content (just reference files)
- Conversation history (let AI build this naturally)
- Temporary notes (keep focused)

## Creating Context Files

### Method 1: Let AI Do It (Recommended)

**Gemini CLI:**

```bash
cd your-project
gemini
> /init
```

**Claude Code:**

```bash
cd your-project
claude
> /init
```

**What happens:**

1. AI scans your directory
2. Reads your files
3. Asks clarifying questions
4. Generates context file

**Chuck's approach:**

> "Let's take a look at it. And while we didn't do much in this project, it knows what's going on."

### Method 2: Manual Creation

```bash
# Create manually
nano gemini.md

# Or use your AI to help!
gemini
> Create a gemini.md file describing this project
```

## Using Context Files

### Fresh Session = Full Context

**The killer demo from the video:**

1. **First session:**

   ```bash
   gemini
   > Research coffee brewing methods and create a blog outline
   > /init
   ```

2. **Close and reopen (NEW session):**
   ```bash
   gemini
   # Context loaded automatically
   > Write the intro for blog post 1 in the coffee series
   ```

**Chuck's reaction:**

> "I didn't give it ANY context. It just knew. This is a new chat session."

### Updating Context

**As you work, update the file:**

```bash
> Update gemini.md to reflect:
  - Research phase complete
  - First draft started
  - Decision: Focus on pour-over method first
```

**Or update manually:**

```bash
nano gemini.md
# Edit and save
```

**Next session automatically loads the updates!**

## Real-World Example: Chuck's Video Project

**Video Timestamp:** 5:48-6:09

### The Setup

```bash
cd ~/Projects/531-ai-terminal
ls
```

**Files present:**

```
gemini.md
claude.md
agents.md
531-script.md
research/
  ├── claude-code-research.md
  ├── gemini-cli-research.md
  └── opencode-research.md
```

### The Workflow

**Chuck opens a fresh Gemini session:**

```bash
gemini

# Loads gemini.md automatically
```

**Asks with ZERO additional context:**

```bash
> Where are we at in the project?
```

**Gemini responds:**

```
Based on your project files:

Current Status: Script writing phase (100% complete)
- All segments finished (307 lines, ~17 min runtime)
- Hook finalized
- Ready for filming

Key Files:
- 531-script.md (complete script)
- research/ folder (comprehensive research on all tools)
- session-summary.md (session history)

Next Steps:
- Optional script polish
- OR proceed to filming
```

**Chuck's amazement:**

> "Are you seeing this? This has completely changed the way I create or do anything now."

## Multi-Tool Context Syncing

**Video Timestamp:** 18:28-18:40

### The Challenge

You want to use:

- ✅ Gemini CLI
- ✅ Claude Code
- ✅ Codex

All on the SAME project... how do you keep context in sync?

### Chuck's Solution

**Two-step process:**

#### Step 1: Same Directory

```bash
# All tools launched from same directory
cd my-project

# Terminal Tab 1
gemini

# Terminal Tab 2
claude

# Terminal Tab 3
codex
```

#### Step 2: Sync Context Files

**Make sure these files say the same thing:**

- `gemini.md`
- `claude.md`
- `agents.md`

**Chuck's method:**

```bash
# Use one AI to sync the others
claude

> Read claude.md and update both gemini.md and agents.md
  to match, ensuring all three context files are synchronized
```

**Result:**

```
my-project/
├── gemini.md    ← Same content
├── claude.md    ← Same content
├── agents.md    ← Same content
```

### Why This Works

**From Chuck:**

> "Everything I'm doing, talking with these three different AIs on a project... It's not tied in a browser. It's not tied in a GUI. It's just this folder right here on my hard drive."

**Each AI:**

- Reads its own context file
- Sees the same project state
- Works on the same files
- No copy/paste between tools!

## Advanced Context Strategies

### 1. Layered Context

**Structure:**

```
project/
├── claude.md              ← Main context
├── docs/
│   ├── framework.md       ← Reference in claude.md
│   ├── brand-guide.md     ← Reference in claude.md
│   └── audience.md        ← Reference in claude.md
```

**In claude.md:**

```markdown
## Reference Documents

For detailed guidelines, see:

- docs/framework.md - Scriptwriting framework
- docs/brand-guide.md - Brand voice guidelines
- docs/audience.md - Target audience research
```

**AI reads main context, pulls in references as needed.**

### 2. Session Summaries

**Chuck uses an agent for this (from video):**

```bash
> @script-session-closer run

# Agent does:
# 1. Summarizes current session
# 2. Updates context files (all three!)
# 3. Updates session-summary.md
# 4. Commits to git
```

**Result:** Next session picks up EXACTLY where you left off.

### 3. Multiple Projects

**Keep them separate:**

```bash
~/coffee-project/
  ├── gemini.md      ← Coffee project context

~/video-script/
  ├── gemini.md      ← Video project context

~/homelab-docs/
  ├── gemini.md      ← Homelab context
```

**No cross-contamination!**

### 4. Decision Log

**Track major decisions in context:**

```markdown
## Decision Log

### 2025-10-15: Brew Method Selection

**Decision:** Focus on pour-over primarily
**Reasoning:** Most beginner-friendly, popular, equipment accessible
**Impact:** Affects equipment recommendations and tutorial structure

### 2025-10-20: Series Length

**Decision:** 5 parts instead of 3
**Reasoning:** Too much content to compress, better to go deep
**Impact:** Updated outline, adjusted timeline
```

## Context File Best Practices

### ✅ DO

1. **Update regularly** - After major work sessions
2. **Be concise** - Don't dump entire project
3. **Reference files** - Don't duplicate content
4. **Track decisions** - Why you chose something matters
5. **Sync across tools** - If using multiple AIs
6. **Version control** - Commit to git

### ❌ DON'T

1. **Include sensitive data** - Context files are readable
2. **Copy/paste everything** - Reference instead
3. **Let it get stale** - Update as project evolves
4. **Over-explain** - AI is smart, be concise
5. **Forget to sync** - When using multiple tools

## Context vs Conversation

### Understanding the Difference

**Context Window:**

- Current conversation messages
- Loaded files
- Context file content
- **Limited size** (200K tokens)

**Context File:**

- Project knowledge
- Persistent across sessions
- **Unlimited size** (within reason)
- Your project's "memory"

### Example

**Session 1 (85K tokens used):**

```
Conversation: 80K tokens
Context file: 2K tokens
Loaded files: 3K tokens
```

**Session 2 (NEW session, 2K tokens used):**

```
Conversation: 0K tokens (fresh start!)
Context file: 2K tokens (loaded automatically)
Loaded files: 0K tokens (not loaded yet)
```

**The magic:** Context file gives you project knowledge WITHOUT burning conversation tokens.

## The "It's Just a Folder" Philosophy

**Chuck's most important point:**

> "I can copy and paste that folder anywhere. All the work, all the decisions, all the context - it's mine."

### What This Means

**Your project = A folder containing:**

- Context files
- Work products
- Reference documents
- Research
- Drafts

**No vendor lock-in:**

- ✅ Works with any AI tool (that supports context files)
- ✅ Stored locally (you own it)
- ✅ Portable (copy to any machine)
- ✅ Version controlled (use git)

**Chuck's freedom:**

> "If a new, greater, better AI comes out, I'm ready for it because all my stuff is right here on my hard drive."

## Troubleshooting

### Context File Not Loading

```bash
# Check you're in right directory
pwd
ls *.md

# Verify filename (case-sensitive)
ls gemini.md    # ✓ Correct
ls Gemini.md    # ✗ Wrong
ls GEMINI.md    # ✗ Wrong

# Recreate if needed
> /init
```

### Context Seems Outdated

```bash
# AI might be caching old version
> Reload gemini.md and re-read the project

# Or restart session
exit
gemini
```

### Multiple Context Files Conflicting

**When using multiple AIs, ensure synced:**

```bash
# Use one AI to sync
claude
> Read claude.md and make gemini.md and agents.md identical
```

### Too Much Context

**If context file gets huge (>5K words):**

1. **Move details to separate docs**
2. **Reference them in main context**
3. **Keep main context concise**

## Summary: Why Context Files Win

| Browser AI                  | Terminal AI + Context Files |
| --------------------------- | --------------------------- |
| 📜 Infinite scroll hell     | 📁 Clean context file       |
| 🔄 Re-explain every session | ✅ Auto-loads on launch     |
| 🗂️ 20 scattered chats       | 📋 One project folder       |
| 📋 Copy/paste nightmare     | 🔗 Direct file access       |
| 🏢 Vendor lock-in           | 🆓 You own everything       |

**Chuck's verdict:**

> "I own my context. Nothing annoys me more than when ChatGPT tries to fence me in, give me vendor lock-in. No, I reject that."

## What's Next?

**Now that you understand context files:**

➡️ [Multi-Tool Workflow](08-multi-tool-workflow.md) - Use context files across multiple AIs

➡️ [Productivity Workflows](11-productivity-workflows.md) - Real examples using context files

---

[← Back to Claude Code](04-claude-code.md) | [Next: Multi-Tool Workflow →](08-multi-tool-workflow.md)

# docs/08-multi-tool-workflow.md

# Multi-Tool Workflow Guide

**Video Timestamp:** 18:03-19:25

**The Ultimate Power Move:** Using Gemini CLI, Claude Code, and Codex simultaneously on the same project.

## Why Use Multiple AI Tools?

**Chuck's philosophy:**

> "I will use all AI. I'll use the best AI. No one can stop me."

### Each AI Has Strengths

**Gemini CLI:**

- ✅ Fast web research
- ✅ Current information (web search built-in)
- ✅ Quick iterations

**Claude Code:**

- ✅ Deep analysis and planning
- ✅ Long-form writing
- ✅ Agents for specialized tasks

**Codex (ChatGPT):**

- ✅ High-level analysis
- ✅ Strategic thinking
- ✅ Different perspective

### Chuck's Strategy

**From the video:**

> "I find ChatGPT is very good at analyzing things from a high view. Gemini and Claude are very good at the work, the deep work."

## The Setup: Two Simple Steps

### Step 1: Same Directory

**All AI tools must work from the SAME project folder:**

```bash
cd ~/my-project
```

**Open multiple terminal tabs/windows:**

```bash
# Terminal Tab 1: Claude
cd ~/my-project
claude

# Terminal Tab 2: Gemini
cd ~/my-project
gemini

# Terminal Tab 3: Codex
cd ~/my-project
codex
```

**Result:** All three AIs can access the same files!

### Step 2: Sync Context Files

**Ensure these files have identical content:**

- `claude.md`
- `gemini.md`
- `agents.md` (for Codex)

**Chuck's method:**

```bash
# In Claude terminal
> Read claude.md and sync it to gemini.md and agents.md.
  Make sure all three files have identical project context.
```

**Verification:**

```bash
# In project directory
diff claude.md gemini.md
diff claude.md agents.md

# Should show: "Files are identical" or no output
```

## The Power: Parallel Workflows

**Video Timestamp:** 18:45-19:01

### Chuck's Live Demo

**The command:**

```bash
# In Claude terminal
> Write a hook for this video, authority angle.
  Write it to authority-hook.md

# In Gemini terminal
> Write a hook on a discovery angle.
  Write it to discovery-hook.md

# In Codex terminal
> Review both hooks and compare their strengths
```

**What happens:**

- 🎯 Claude: Writes authority-focused hook
- 🔍 Gemini: Writes discovery-focused hook
- 📊 Codex: Analyzes and compares both

**Chuck's observation:**

> "They're all using the same context, different roles. You have three different AIs working on the same thing at the same time. No copying and pasting. They can see each other's work."

## Real-World Workflow Examples

### Example 1: Content Creation

**Scenario:** Writing a technical blog post

```bash
# TERMINAL 1: Claude (long-form writing)
claude
> Write the introduction section for the ZFS storage blog post.
  Save to sections/intro.md

# TERMINAL 2: Gemini (research)
gemini
> Research the latest ZFS performance benchmarks.
  Compile findings in research/zfs-benchmarks.md

# TERMINAL 3: Codex (review)
codex
> Review the intro in sections/intro.md and check if it aligns
  with the benchmarks research. Suggest improvements.
```

**Result:**

- Claude writes deep content
- Gemini gathers current data
- Codex ensures quality and alignment

### Example 2: Homelab Planning

**Scenario:** Designing a new homelab setup

```bash
# TERMINAL 1: Claude (planning)
claude
> Create a detailed homelab architecture plan.
  Include network diagram, hardware specs, and budget.
  Save to homelab-plan.md

# TERMINAL 2: Gemini (current prices/availability)
gemini
> Research current pricing for enterprise NAS systems.
  Check availability of the hardware in the homelab plan.
  Save to pricing-research.md

# TERMINAL 3: Codex (risk analysis)
codex
> Review homelab-plan.md and identify potential issues:
  - Single points of failure
  - Budget overruns
  - Compatibility problems
  Save analysis to risk-assessment.md
```

### Example 3: Video Script Writing (Chuck's Process)

**Video Timestamp:** 18:41-19:25

**Chuck's actual workflow:**

```bash
# TERMINAL 1: Claude with script-writing output style
claude
> Continue working on Segment 3 of the AI Terminal script.
  Reference the outline at outline.md

# TERMINAL 2: Gemini with research focus
gemini
> Verify the technical accuracy of the Claude Code section.
  Cross-check commands and features against official docs.

# TERMINAL 3: Codex for high-level review
codex
> Read the current script at script.md.
  Evaluate narrative flow and retention strategy.
  Does it deliver on the hook promise?
```

**Chuck's approach:**

> "I'm using all three right now to work on this video script."

## File-Based Collaboration

### How AIs "See" Each Other's Work

**The secret:** Everything is just files!

```
my-project/
├── claude.md              ← Shared context
├── gemini.md              ← Shared context
├── agents.md              ← Shared context
├── research/
│   ├── topic-a.md        ← Gemini wrote this
│   └── topic-b.md        ← Gemini wrote this
├── drafts/
│   ├── section-1.md      ← Claude wrote this
│   └── section-2.md      ← Claude wrote this
└── reviews/
    └── analysis.md       ← Codex wrote this
```

**When Claude asks:**

```bash
> Review the research in research/ folder
```

**Claude sees:**

- ✅ Files Gemini created
- ✅ Their exact content
- ✅ Timestamps
- ✅ Everything!

**No copy/paste. No export/import. Just files.**

## Specialized Roles Strategy

### Assign Each AI a Role

**Based on strengths from video:**

#### Claude → Deep Work

```bash
# Long-form writing
# Complex planning
# Agent deployment
# Custom output styles
```

#### Gemini → Research & Speed

```bash
# Web research
# Fast iterations
# Current information
# Quick file creation
```

#### Codex → Analysis & Review

```bash
# High-level strategy
# Quality review
# Competitive analysis
# Meta-thinking
```

### Role Assignment in Practice

**In your context files:**

**claude.md:**

```markdown
# Project: Technical Blog Series

## Claude's Role

Primary writer for long-form content.

- Draft all blog posts
- Create detailed technical explanations
- Deploy agents for specialized sections
```

**gemini.md:**

```markdown
# Project: Technical Blog Series

## Gemini's Role

Research and verification specialist.

- Gather current technical information
- Verify accuracy of claims
- Find supporting examples and case studies
```

**agents.md:**

```markdown
# Project: Technical Blog Series

## Codex's Role

Strategic reviewer and analyst.

- Review drafts for clarity and flow
- Ensure technical accuracy
- Validate against target audience needs
```

## Context Syncing Strategies

### Manual Sync

**After major changes:**

```bash
# Update all three manually
nano claude.md
nano gemini.md
nano agents.md
```

**Or use one AI to update others:**

```bash
# In Claude terminal
> I just made major updates to claude.md (added new project phase).
  Update gemini.md and agents.md to match.
```

### Automated Sync (Chuck's Method)

**Using a Claude agent:**

```bash
# In Claude terminal
> @context-sync-agent
  Read claude.md and sync to gemini.md and agents.md.
  Ensure all three files are identical.
```

**Agent does:**

1. Reads `claude.md`
2. Overwrites `gemini.md` with same content
3. Overwrites `agents.md` with same content
4. Confirms sync complete

### Git-Based Sync

**For ultimate control:**

```bash
# After each session, commit context files
git add *.md
git commit -m "Update project context: research phase complete"

# All terminals pull latest
git pull
```

**Each AI automatically loads updated context on next launch.**

## Communication Patterns

### Cross-AI References

**Gemini creates file → Claude uses it:**

```bash
# GEMINI TERMINAL
gemini
> Research ZFS performance. Save to zfs-research.md

# CLAUDE TERMINAL (moments later)
claude
> Read zfs-research.md and write a blog intro incorporating
  those performance numbers. Save to blog-intro.md
```

### Review Loops

**Claude writes → Codex reviews → Claude revises:**

```bash
# CLAUDE TERMINAL
claude
> Write the authentication section. Save to auth-section.md

# CODEX TERMINAL
codex
> Review auth-section.md for security concerns.
  Save feedback to reviews/auth-feedback.md

# CLAUDE TERMINAL
claude
> Read reviews/auth-feedback.md and revise auth-section.md
  to address the security concerns.
```

### Parallel Tasks

**All three work simultaneously:**

```bash
# CLAUDE: Long task
> Create comprehensive system architecture document

# GEMINI: Quick research
> Find 5 examples of similar architectures in production

# CODEX: Analysis
> Analyze current requirements and identify gaps
```

**All running at once, no waiting!**

## Advanced: Cross-Tool Agents

**Video Timestamp:** 16:06-16:17

### Claude Agent Uses Gemini

**Chuck's demo:**

```bash
# In Claude terminal
> @gemini-research find the best AI terminal videos on YouTube
```

**What happens:**

1. Claude deploys `gemini-research` agent
2. Agent runs: `gemini -p "search YouTube for top AI terminal videos"`
3. Gemini performs search (better at current info)
4. Returns results to Claude agent
5. Claude compiles final report

**Chuck's amazement:**

> "We're having an AI use an AI right now!"

### Create Gemini Research Agent

**In Claude:**

```bash
> /agents
# Create new agent

Name: gemini-research
Description: Uses Gemini CLI in headless mode for research tasks.
              Gemini excels at web search and current information.

Instructions:
You are a research specialist that uses Gemini CLI to gather information.

When given a research task:
1. Format it as a clear search query
2. Run: gemini -p "your search query here"
3. Compile and summarize the results

You have access to Bash tool to run gemini command.

Tools: Bash, Read, Write
Model: Sonnet
```

**Usage:**

```bash
> @gemini-research What are the latest Proxmox features?
> @gemini-research Find pricing for enterprise SSDs
> @gemini-research Research zero-trust network solutions
```

## Managing Multiple Terminal Windows

### Terminal Layouts

**Chuck's setup (visible in video):**

```
┌─────────────────┬─────────────────┬─────────────────┐
│  CLAUDE         │  GEMINI         │  CODEX          │
│                 │                 │                 │
│  Deep work      │  Research       │  Analysis       │
│  Writing        │  Web search     │  Review         │
│  Agents         │  Fast iteration │  Strategy       │
└─────────────────┴─────────────────┴─────────────────┘
```

**Tools for multi-terminal:**

- **tmux** (Linux/Mac) - Terminal multiplexer
- **Windows Terminal** (Windows) - Native tabs/panes
- **iTerm2** (Mac) - Split panes
- **Terminator** (Linux) - Multiple terminals

### Quick Switching

**tmux example:**

```bash
# Start tmux session for project
tmux new -s ai-project

# Window 1: Claude
claude

# Create new window: Ctrl+B, C
# Window 2: Gemini
gemini

# Create new window: Ctrl+B, C
# Window 3: Codex
codex

# Switch windows: Ctrl+B, [0-9]
```

## Workflow Optimization Tips

### 1. Primary AI for Context Updates

**Choose ONE AI to maintain context files:**

```bash
# Claude is "source of truth"
# Only Claude updates context files
# Others sync from Claude's version
```

**Why:** Prevents conflicts, single source of truth

### 2. Clear File Naming

**Make it obvious who created what:**

```
research-gemini-zfs-performance.md    ← Gemini research
draft-claude-section-1.md             ← Claude draft
review-codex-analysis.md              ← Codex review
```

### 3. Session Start Ritual

**Every work session:**

```bash
# 1. Pull latest (if using git)
git pull

# 2. Check context sync
diff claude.md gemini.md

# 3. Launch all three AIs
# Terminal 1: claude
# Terminal 2: gemini
# Terminal 3: codex

# 4. Verify each loaded context
# (Check context indicators in each terminal)
```

### 4. Session End Ritual

**Chuck's approach (using agent):**

```bash
# In Claude terminal
> @script-session-closer run
```

**Agent does:**

- Summarizes session
- Updates all context files
- Syncs gemini.md and agents.md
- Commits to git

**Manual version:**

```bash
# 1. Update context files
> Update claude.md with today's progress

# 2. Sync to other files
> Copy claude.md content to gemini.md and agents.md

# 3. Commit
git add .
git commit -m "Session end: [what you accomplished]"
git push
```

## The "It's Just a Folder" Philosophy

**Chuck's key insight:**

> "Everything I'm doing, talking with these three different AIs on a project... It's not tied in a browser. It's not tied in a GUI. It's just this folder right here on my hard drive."

### What This Enables

```
my-project/     ← This is ALL you need
├── claude.md
├── gemini.md
├── agents.md
└── all-your-work-files/
```

**You can:**

- ✅ Copy to another computer
- ✅ Backup easily
- ✅ Version control with git
- ✅ Switch AI tools anytime
- ✅ Share with team (just the folder!)

**Chuck's freedom:**

> "I can copy and paste that folder anywhere. All the work, all the decisions, all the context - it's mine. I own my context."

## Troubleshooting

### AIs Seem Out of Sync

```bash
# Check context files
diff claude.md gemini.md

# Re-sync
claude
> Sync all context files from claude.md
```

### File Conflicts

**Two AIs editing same file:**

```bash
# Solution: Assign clear responsibilities
# Claude: Writes sections/1.md
# Gemini: Writes research/1.md
# Never overlap!
```

### Context Drift

**Over time, conversations diverge:**

```bash
# Regular re-sync
# Every 30-60 minutes:
> @context-sync-agent run
```

## Summary: Multi-Tool Benefits

| Single AI           | Multi-Tool Workflow        |
| ------------------- | -------------------------- |
| One perspective     | Three perspectives         |
| One strength        | Combined strengths         |
| Sequential tasks    | Parallel tasks             |
| One context window  | Three independent contexts |
| Vendor lock-in risk | Tool agnostic              |

**Chuck's verdict:**

> "I will use the best AI. No one can stop me. If a new greater better AI comes out, I'm ready for it."

## What's Next?

**Master the multi-tool workflow:**

➡️ [Productivity Workflows](11-productivity-workflows.md) - Real examples using multiple AIs

➡️ [AI Agents Deep Dive](09-agents.md) - Advanced agent strategies

---

[← Back to Context Files](07-context-files.md) | [Next: AI Agents →](09-agents.md)

# docs/09-agents.md

# Coming Soon

This guide is currently being developed. Check back soon!

In the meantime, explore:

- [README](../README.md) - Main guide
- [Command Cheat Sheet](14-cheat-sheet.md) - Quick reference
- [FAQ](16-faq.md) - Common questions

---

[← Back to README](../README.md)

# docs/10-customization.md

# Coming Soon

This guide is currently being developed. Check back soon!

In the meantime, explore:

- [README](../README.md) - Main guide
- [Command Cheat Sheet](14-cheat-sheet.md) - Quick reference
- [FAQ](16-faq.md) - Common questions

---

[← Back to README](../README.md)

# docs/11-productivity-workflows.md

# Coming Soon

This guide is currently being developed. Check back soon!

In the meantime, explore:

- [README](../README.md) - Main guide
- [Command Cheat Sheet](14-cheat-sheet.md) - Quick reference
- [FAQ](16-faq.md) - Common questions

---

[← Back to README](../README.md)

# docs/12-development-workflows.md

# Coming Soon

This guide is currently being developed. Check back soon!

In the meantime, explore:

- [README](../README.md) - Main guide
- [Command Cheat Sheet](14-cheat-sheet.md) - Quick reference
- [FAQ](16-faq.md) - Common questions

---

[← Back to README](../README.md)

# docs/13-homelab-workflows.md

# Coming Soon

This guide is currently being developed. Check back soon!

In the meantime, explore:

- [README](../README.md) - Main guide
- [Command Cheat Sheet](14-cheat-sheet.md) - Quick reference
- [FAQ](16-faq.md) - Common questions

---

[← Back to README](../README.md)

# docs/14-cheat-sheet.md

# Command Cheat Sheet

Quick reference for all AI terminal tools covered in the video.

## Installation Commands

### Gemini CLI

```bash
# Linux/macOS/WSL (npm)
npm install -g @google/generative-ai-cli

# With sudo (if permission error)
sudo npm install -g @google/generative-ai-cli

# macOS (Homebrew)
brew install gemini-cli
```

### Claude Code

```bash
# All platforms (npm)
npm install -g @anthropic-ai/claude-code

# With sudo
sudo npm install -g @anthropic-ai/claude-code
```

### Codex (ChatGPT CLI)

```bash
# Installation command
npm install -g @openai/codex-cli

# Or follow OpenAI documentation
```

### opencode

```bash
# Installation (one command - from video)
curl -fsSL https://opencode.sh/install.sh | sh

# Reload shell
source ~/.bashrc
# or
source ~/.zshrc
```

## Launch Commands

### Basic Launch

```bash
gemini              # Launch Gemini CLI
claude              # Launch Claude Code
codex               # Launch Codex
opencode            # Launch opencode
```

### Launch with Flags

```bash
# Claude Code
claude -r                               # Resume previous session
claude --dangerously-skip-permissions   # Skip safety prompts
claude -r --dangerously-skip-permissions  # Both flags combined

# Gemini CLI
gemini -p "your prompt here"           # Headless mode (one-shot)

# opencode
opencode --model claude-sonnet-4       # Specify model
```

## In-Session Commands

### Gemini CLI

```bash
/init               # Create gemini.md context file
/tools              # Show available tools
/help               # Show help
exit                # Exit Gemini (or Ctrl+C)
```

### Claude Code

```bash
/init               # Create claude.md context file
/context            # Show context usage details
/agents             # Agent management menu
/output-style       # Output style management
exit                # Exit Claude (or Ctrl+C)
```

**Keyboard shortcuts:**

```bash
Tab                 # Toggle thinking mode
Shift+Tab           # Toggle planning mode
Ctrl+C              # Interrupt/exit
Ctrl+O              # View agent details (when agent running)
```

### opencode

```bash
/model              # Change AI model
/share              # Share current session
/timeline           # View session timeline
/sessions           # View all sessions
exit                # Exit opencode
```

## Project Setup

### Create New Project

```bash
# Standard workflow
mkdir my-project
cd my-project

# Launch AI and create context
gemini
> /init

# Verify context file created
ls *.md
```

### Multi-Tool Project Setup

```bash
# Create project
mkdir my-project
cd my-project

# Initialize all three context files
# Terminal 1
gemini
> /init

# Terminal 2
claude
> /init

# Terminal 3
codex
> /init

# Sync context files
claude
> Sync claude.md to gemini.md and agents.md
```

## Context File Management

### Create Context Files

```bash
# Let AI create it
> /init

# Manual creation
nano gemini.md      # Edit manually
nano claude.md
nano agents.md
```

### Update Context

```bash
# Ask AI to update
> Update gemini.md with: [your updates]

# Manual edit
nano gemini.md
```

### Sync Context Files

```bash
# Use Claude to sync
claude
> Read claude.md and make gemini.md and agents.md identical
```

### View Context

```bash
# View file contents
cat gemini.md
cat claude.md
cat agents.md

# In Claude, check context usage
> /context
```

## Agent Commands (Claude Code)

### Agent Management

```bash
> /agents                      # Open agent menu
> /agents                      # Then: "Create new agent"
> /agents                      # Then: "View agents"
> /agents                      # Then: "Edit agent"
> /agents                      # Then: "Delete agent"
```

### Deploy Agents

```bash
> @agent-name do a task
> @homelab-guru research NAS options
> @brutal-critic review my script
```

### Multi-Agent Tasks

```bash
> @agent1 do task A, @agent2 do task B, and compile results
```

## Output Styles (Claude Code)

### Manage Output Styles

```bash
> /output-style                # View available styles
> /output-style new            # Create new style
> /output-style                # Select active style
```

### Create Output Style

```bash
> /output-style new

# Then describe the style:
Name: my-expert
Description: You are an expert in [domain]...
```

## File Operations

### Create Files

```bash
# Ask AI to create
> Create a file named project-plan.md with [content]

# Manual creation
nano project-plan.md
```

### Read Files

```bash
# AI reads files automatically when mentioned
> Read project-plan.md and summarize

# Reference with @
> Review @project-plan.md
```

### Update Files

```bash
# AI updates
> Update project-plan.md to add [new section]

# Manual edit
nano project-plan.md
```

### List Files

```bash
# Terminal command
ls
ls -la

# AI command
> What files are in this directory?
> Show me all markdown files
```

## Git Integration

### Initialize Repository

```bash
git init
git add .
git commit -m "Initial commit"
```

### Regular Commits

```bash
# After work session
git add .
git commit -m "Session summary: [what you did]"
git push
```

### Chuck's Automated Approach

```bash
# Using session-closer agent
> @script-session-closer run

# Agent automatically:
# - Summarizes session
# - Updates context files
# - Commits to git
```

## Multi-Terminal Workflows

### Open Multiple Terminals

```bash
# Terminal 1: Claude
cd ~/my-project
claude

# Terminal 2: Gemini
cd ~/my-project
gemini

# Terminal 3: Codex
cd ~/my-project
codex
```

### tmux (Advanced)

```bash
# Start tmux session
tmux new -s ai-work

# Create windows
Ctrl+B, C           # New window
Ctrl+B, [0-9]       # Switch to window N
Ctrl+B, "           # Split horizontal
Ctrl+B, %           # Split vertical
```

## opencode Specific Commands

### Model Management

```bash
# View available models
> /model

# Switch to specific model
> /model claude-sonnet-4
> /model grok-fast
> /model llama-3.2
```

### Configuration

```bash
# Edit config file
nano ~/.config/opencode/opencode.jsonc

# Example config for local model
{
  "model": "llama-3.2"
}
```

### Authentication

```bash
# Login with Claude Pro
opencode auth login
# Select "Anthropic"
# Paste auth code from browser

# Verify login
opencode auth whoami
```

### Session Management

```bash
> /sessions         # View all sessions
> /timeline         # View current session timeline
> /share            # Generate shareable link
```

## Advanced Techniques

### Headless Mode

```bash
# Gemini one-shot command
gemini -p "Research ZFS performance and save to report.md"

# Claude with pipe
echo "Analyze this file" | claude

# Chain commands
gemini -p "Research topic" && claude -r
```

### Agent as Tool

```bash
# Claude agent using Gemini
> @gemini-research search for latest Docker security updates

# Agent runs:
gemini -p "search for latest Docker security updates"
```

### Obsidian Integration

```bash
# Navigate to vault
cd ~/Obsidian/MyVault

# Launch AI
gemini

# Work with notes
> Read my daily note and summarize tasks
> Create a new note about [topic] with backlinks
```

## Troubleshooting Commands

### Permission Issues

```bash
# Reinstall with sudo
sudo npm install -g @google/generative-ai-cli

# Fix permissions
sudo chown -R $USER /usr/local/lib/node_modules
```

### Command Not Found

```bash
# Reload shell
source ~/.bashrc
source ~/.zshrc

# Verify installation
which gemini
which claude
which opencode

# Check PATH
echo $PATH
```

### Context File Issues

```bash
# Verify file exists
ls *.md

# Check file contents
cat gemini.md

# Recreate if needed
> /init
```

### Clear Cache/Reset

```bash
# Claude Code
rm -rf ~/.config/claude-code

# Gemini CLI
rm -rf ~/.config/gemini-cli

# opencode
rm -rf ~/.config/opencode
```

## Common Workflows

### Research & Write

```bash
# Step 1: Research (Gemini)
gemini
> Research [topic] and compile findings

# Step 2: Write (Claude)
claude
> Read research.md and write comprehensive blog post

# Step 3: Review (Codex)
codex
> Review blog-post.md for accuracy and clarity
```

### Project Kickoff

```bash
# Create project
mkdir project-name
cd project-name

# Initialize
gemini
> /init
> Help me plan this project: [description]

# Track with git
git init
git add .
git commit -m "Project initialized"
```

### Daily Work Session

```bash
# Start
cd ~/current-project
claude

# Check status
> Where are we in the project?

# Work
> [Your tasks]

# End session
> @script-session-closer run
# Or manually:
git add .
git commit -m "Session: [summary]"
```

## Quick Tips

### Keyboard Shortcuts

```bash
Ctrl+C              # Interrupt AI / Exit
Ctrl+D              # Exit (alternative)
Tab                 # Toggle thinking (Claude)
Shift+Tab           # Toggle planning (Claude)
Ctrl+O              # Check agent status (Claude)
```

### Speed Tips

```bash
# Use dangerous mode (when safe)
claude --dangerously-skip-permissions

# Use headless for quick tasks
gemini -p "quick question"

# Deploy agents for parallel work
> @agent1 task A, @agent2 task B
```

### Organization Tips

```bash
# One directory per project
~/projects/project-a/
~/projects/project-b/

# Consistent context file naming
gemini.md, claude.md, agents.md

# Use git for everything
git commit regularly
```

## Emergency Commands

### Kill Stuck Process

```bash
# Find process ID
ps aux | grep gemini
ps aux | grep claude

# Kill it
kill -9 [PID]

# Or use Ctrl+C twice rapidly
```

### Reset Everything

```bash
# Remove config directories
rm -rf ~/.config/gemini-cli
rm -rf ~/.config/claude-code
rm -rf ~/.config/opencode

# Reinstall
npm install -g @google/generative-ai-cli
npm install -g @anthropic-ai/claude-code
curl -fsSL https://opencode.sh/install.sh | sh
```

## Official Documentation Links

```bash
# Gemini CLI
https://ai.google.dev/gemini-api/docs/cli

# Claude Code
https://docs.anthropic.com/claude/docs/claude-code

# opencode
https://github.com/stackblitz-labs/opencode

# Codex
https://platform.openai.com/docs/tools/codex
```

---

**Print this page for quick reference!**

[← Back to README](../README.md)

# docs/15-troubleshooting.md

# Troubleshooting Guide

## Installation Issues

### "Command not found" after installation

**Problem:** Installed tool but terminal doesn't recognize command

**Solutions:**

```bash
# 1. Reload shell configuration
source ~/.bashrc     # for bash
source ~/.zshrc      # for zsh

# 2. Close and reopen terminal

# 3. Check if actually installed
which gemini
which claude
which opencode

# 4. Verify PATH includes npm global packages
echo $PATH | grep npm
```

### "Permission denied" during installation

**Problem:** npm permission errors

**Solutions:**

```bash
# Option 1: Use sudo (quick fix)
sudo npm install -g @google/generative-ai-cli

# Option 2: Fix npm permissions (proper fix)
sudo chown -R $USER /usr/local/lib/node_modules
sudo chown -R $USER /usr/local/bin
```

### "Node.js not found"

**Problem:** npm commands fail, Node.js not installed

**Solution:**

1. Install Node.js from [nodejs.org](https://nodejs.org/)
2. Choose LTS (Long Term Support) version
3. Restart terminal after installation

## Authentication Issues

### Can't login to Gemini CLI

**Solutions:**

```bash
# 1. Ensure browser opens for OAuth
# Check if browser is set as default

# 2. Try incognito/private browser window
# Sometimes cached auth causes issues

# 3. Clear Gemini config and retry
rm -rf ~/.config/gemini-cli
gemini
```

### Claude Code authentication fails

**Solutions:**

```bash
# 1. Verify Claude Pro subscription is active
# Check at claude.ai

# 2. Clear auth cache
rm -rf ~/.config/claude-code/auth

# 3. Re-authenticate
claude auth login
```

### opencode provider authentication issues

**Solutions:**

```bash
# 1. Check auth status
opencode auth whoami

# 2. Re-login
opencode auth login

# 3. For Claude Pro: ensure correct provider selected
# Select "Anthropic" not "OpenAI"

# 4. Check API key validity (if using API keys)
```

## Context File Issues

### Context file not loading automatically

**Solutions:**

```bash
# 1. Verify correct filename (case-sensitive!)
ls gemini.md     # ✓ Correct
ls Gemini.md     # ✗ Wrong
ls GEMINI.md     # ✗ Wrong

# 2. Ensure you're in the right directory
pwd
# Should show your project directory

# 3. Recreate context file
> /init

# 4. Check file isn't empty
cat gemini.md
```

### Multiple context files out of sync

**Problem:** Using Claude + Gemini + Codex, context files differ

**Solution:**

```bash
# Use one AI to sync all files
claude
> Read claude.md and copy its content exactly to gemini.md and agents.md

# Verify they match
diff claude.md gemini.md
diff claude.md agents.md
```

### Context seems stale/outdated

**Solutions:**

```bash
# 1. Exit and restart session (forces reload)
exit
gemini  # or claude/codex

# 2. Manually update context file
nano gemini.md
# Make your changes
# Save and exit
# Restart session

# 3. Ask AI to update context
> Update gemini.md to reflect our latest progress
```

## Agent Issues (Claude Code)

### Can't create agent

**Solutions:**

```bash
# 1. Verify you're in Claude Code (not Gemini/Codex)
# Agents only work in Claude Code

# 2. Ensure Claude Pro subscription is active

# 3. Try creating via menu
> /agents
# Select "Create new agent"
```

### Agent not responding

**Solutions:**

```bash
# 1. Check agent syntax
> @agent-name do task    # ✓ Correct
> agent-name do task     # ✗ Wrong (missing @)

# 2. Verify agent exists
> /agents
# Check list of available agents

# 3. Check agent has appropriate tools enabled
> /agents
# Select "Edit agent"
# Verify tools are enabled
```

### "Agent not found" error

**Solutions:**

```bash
# 1. Check agent scope
# Project agents only available in that project directory

# 2. Verify agent name (case-sensitive)
> @homelab-guru    # ✓ Correct
> @Homelab-Guru    # ✗ Wrong

# 3. Recreate agent if necessary
> /agents
# Delete and recreate
```

## File Operation Issues

### AI can't read my files

**Solutions:**

```bash
# 1. Verify file permissions
ls -la yourfile.md

# 2. Check you're in correct directory
pwd
ls

# 3. Use absolute path if needed
> Read /full/path/to/file.md

# 4. Check file isn't binary
file yourfile.md
# Should show: "ASCII text" or "UTF-8 text"
```

### AI can't write files

**Solutions:**

```bash
# 1. Check directory permissions
ls -la

# 2. Verify disk space
df -h .

# 3. Try different filename
> Create test.md with content "hello"

# 4. Check if file exists and is read-only
ls -la existing-file.md
chmod 644 existing-file.md  # Make writable
```

## Performance Issues

### AI responses are very slow

**Solutions:**

```bash
# 1. Check internet connection
ping 8.8.8.8

# 2. Try different model (for opencode)
> /model grok-fast-1
# Faster model for quick tasks

# 3. Reduce context size
# Start new session if context window is full

# 4. Close unused terminal sessions
# Multiple AI sessions can slow things down
```

### Terminal freezes/hangs

**Solutions:**

```bash
# 1. Try Ctrl+C to interrupt
# Press once, wait 2 seconds

# 2. Force quit if needed
# Ctrl+C twice rapidly

# 3. Kill process from another terminal
ps aux | grep gemini
kill -9 [PID]

# 4. Close and reopen terminal
```

## Multi-Tool Issues

### AIs giving conflicting information

**Expected behavior!** Different models have different strengths.

**Strategy:**

- Claude: Best for deep work
- Gemini: Best for current info
- Codex: Best for analysis

Cross-check important decisions across multiple AIs.

### File conflicts (multiple AIs editing same file)

**Prevention:**

```bash
# Assign clear responsibilities
# Claude: sections/1.md
# Gemini: research/1.md
# Never overlap!
```

**Solution if it happens:**

```bash
# 1. Check file with git diff
git diff file.md

# 2. Review changes manually
cat file.md

# 3. Use version control to restore
git checkout file.md
```

## Platform-Specific Issues

### Windows / WSL Issues

**Problem:** Commands not working in PowerShell

**Solution:** Use WSL (Windows Subsystem for Linux)

```powershell
# Install WSL
wsl --install

# Launch Ubuntu
wsl

# Install tools in WSL, not PowerShell
```

### macOS Issues

**Problem:** "Developer tools not installed"

**Solution:**

```bash
xcode-select --install
# Wait for installation
# Retry npm install
```

### Linux Issues

**Problem:** npm permissions complex

**Solution:**

```bash
# Use nvm (Node Version Manager) instead
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install --lts
nvm use --lts

# Now install tools
npm install -g @google/generative-ai-cli
```

## Still Having Issues?

### Check Official Documentation

- [Gemini CLI Docs](https://ai.google.dev/gemini-api/docs/cli)
- [Claude Code Docs](https://docs.anthropic.com/claude/docs/claude-code)
- [opencode GitHub](https://github.com/stackblitz-labs/opencode)

### Community Support

- NetworkChuck Discord
- GitHub Issues for opencode
- Tool-specific forums

### Nuclear Option: Complete Reinstall

```bash
# 1. Remove all tools
npm uninstall -g @google/generative-ai-cli
npm uninstall -g @anthropic-ai/claude-code
rm -rf ~/.config/gemini-cli
rm -rf ~/.config/claude-code
rm -rf ~/.config/opencode

# 2. Reinstall from scratch
npm install -g @google/generative-ai-cli
npm install -g @anthropic-ai/claude-code
curl -fsSL https://opencode.sh/install.sh | sh

# 3. Reload shell
source ~/.bashrc
```

---

[← Back to README](../README.md)

# docs/16-faq.md

# Frequently Asked Questions

## Getting Started

### Which tool should I start with?

**Start with Gemini CLI** if you want free access. It's generous and perfect for learning the concepts.

**Upgrade to Claude Code** if you need agents and are serious about terminal AI workflows.

### Do I need all three tools?

No! Chuck uses all three because they have different strengths:

- **Gemini**: Research and web search
- **Claude**: Deep work and agents
- **Codex**: High-level analysis

Start with one, add others as needed.

### Is this just for developers?

**Absolutely not!** Chuck uses these tools for YouTube video scriptwriting. They work for:

- Writing and content creation
- Research and analysis
- Project planning
- Documentation
- Any text-based work

Coding is just ONE use case.

## Cost & Subscriptions

### How much does this cost?

- **Gemini CLI**: FREE (generous limits)
- **Claude Code**: $20/mo (Claude Pro required)
- **Codex**: $20/mo (ChatGPT Plus) or pay-per-use API
- **opencode**: FREE (Grok), or use existing subscriptions

### Can I use existing AI subscriptions?

**Yes!**

- Have Claude Pro? Use it with Claude Code
- Have ChatGPT Plus? Use it with Codex
- Have Claude Pro? Use it with opencode too!

### Which subscription is most worth it?

**Chuck's recommendation:** Claude Pro ($20/mo)

- Access to Claude Code (terminal)
- Access to Claude web
- Works with opencode
- Agents feature is game-changing

## Technical Questions

### What's a context file?

A markdown file (gemini.md, claude.md, agents.md) that tells the AI what your project is about. It loads automatically every session so you never re-explain your work.

### Why do I need different context files?

Each AI tool looks for its own:

- Gemini CLI → gemini.md
- Claude Code → claude.md
- Codex/opencode → agents.md

Keep them synced when using multiple tools!

### What's an agent?

(Claude Code feature) A separate AI instance with:

- Specialized instructions
- Fresh context window
- Custom tool access
- Independent from main conversation

Think: delegating tasks to specialized coworkers.

### Can AI access all my files?

Only files in the directory where you launch it.

**Safety tip:** Start AI tools in project directories, not your home folder!

## Workflow Questions

### How do I use multiple AI tools together?

1. Launch all tools in the same directory
2. Sync context files (claude.md = gemini.md = agents.md)
3. Each AI can read/write the same files
4. No copy/paste needed!

### How do I avoid losing my work?

Use git! Chuck commits his projects regularly:

```bash
git init
git add .
git commit -m "Session summary"
```

Everything is local files, perfect for version control.

### Can I access my Obsidian vault?

**Yes!** Just launch the AI in your vault directory:

```bash
cd ~/Obsidian/MyVault
gemini
```

AI can read all your notes (they're markdown files).

## Troubleshooting

### "Command not found"

```bash
# Reload shell
source ~/.bashrc

# Or close and reopen terminal
```

### "Permission denied"

```bash
# Use sudo
sudo npm install -g [package-name]
```

### Context file not loading

```bash
# Verify you're in right directory
pwd
ls gemini.md

# Recreate
> /init
```

## Comparison Questions

### Browser AI vs Terminal AI?

**Browser AI:**

- Lost context after scrolling
- Scattered across multiple chats
- Copy/paste nightmare
- Vendor lock-in

**Terminal AI:**

- Persistent context files
- One project folder
- Direct file access
- You own everything

### Which AI is "best"?

Depends on the task:

- **Claude**: Best for writing, deep work, agents
- **Gemini**: Best for web research, current info
- **ChatGPT**: Best for high-level analysis
- **opencode**: Best for flexibility, local models

Chuck uses all three for different strengths.

## Philosophy Questions

### Why does Chuck care about owning his context?

**Vendor lock-in avoidance.** Browser AI traps your work in their platform.

With terminal AI:

- Everything is local files
- Copy folder anywhere
- Switch AI tools anytime
- Full control

### What's the "It's just a folder" philosophy?

Your project = one folder containing:

- Context files
- Work products
- Research
- Everything

Portable, version-controlled, tool-agnostic. **You own it.**

## Need More Help?

→ [Troubleshooting Guide](15-troubleshooting.md)

→ [Command Cheat Sheet](14-cheat-sheet.md)

---

[← Back to README](../README.md)
