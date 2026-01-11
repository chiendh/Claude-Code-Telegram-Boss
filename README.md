<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

[![GitHub Stars](https://img.shields.io/github/stars/0xAstroAlpha/Claude-Code-Telegram-Boss?style=flat-square&logo=github)](https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/0xAstroAlpha/Claude-Code-Telegram-Boss?style=flat-square&logo=github)](https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/0xAstroAlpha/Claude-Code-Telegram-Boss?style=flat-square&logo=github)](https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss/issues)
[![Contributors](https://img.shields.io/github/contributors/0xAstroAlpha/Claude-Code-Telegram-Boss?style=flat-square&logo=github)](https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss/graphs/contributors)

# 🤖 Claude Code Telegram Boss

**Control Claude Code CLI remotely via Telegram - Your AI coding assistant in your pocket**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Configuration](#️-configuration) • [Support](#-support--donations)

</div>

![Claude Code Telegram Boss Preview](docs/ScreenShot.jpeg)

---

## 📢 Recent Updates

- **🎯 Interactive Q&A**: Inline buttons for quick responses to Claude's questions
- **📊 Real-time Progress**: See tool execution status with detailed previews
- **🔐 Trust Mode**: Master switch to bypass all validation for personal use
- **🔧 Session Continuity**: Text replies continue existing sessions

---

## ✨ Features

### 🧠 Intelligent Sessions
- **Persistent Memory** - Claude remembers your entire conversation context
- **Session Continuity** - Text replies automatically continue active sessions
- **Multi-Project Support** - Switch between projects with `/cd` and `/projects`

### 📱 Mobile-First Design
- **Inline Keyboards** - Quick action buttons for common operations
- **Question Detection** - Automatic Yes/No buttons for Claude's questions
- **Progress Indicators** - Real-time status updates during tool execution
- **File Uploads** - Send code files directly for review

### 🔧 Full Claude Code Access
- **All Tools Available** - Read, Write, Edit, Bash, Glob, Grep, LS, Task
- **Git Integration** - Check branches, diffs, status directly in Telegram
- **Tool Previews** - See file paths and command previews during execution

### 🔐 Enterprise Security
- **User Whitelist** - Only authorized Telegram users can interact
- **Path Sandboxing** - Claude restricted to approved directories
- **Tool Validation** - Each tool call validated before execution
- **Rate Limiting** - Prevents abuse and controls API costs
- **Audit Logging** - All actions logged for review

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **Claude Code CLI** installed and authenticated
- **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss
```

---

### Step 2: Install Dependencies
```bash
pip install poetry
poetry install
```

---

### Step 3: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your settings:

| Setting | Example | Description |
|---------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | `123456:ABC...` | Token from @BotFather |
| `ALLOWED_USERS` | `["123456789"]` | Your Telegram user ID |
| `APPROVED_DIRECTORY` | `/path/to/projects` | Working directory for Claude |

> [!TIP]
> Get your Telegram user ID from [@userinfobot](https://t.me/userinfobot)

---

### Step 4: Start the Bot
```bash
./start_bot.sh
```

---

### Step 5: Persistent Service (macOS)
```bash
# Create LaunchAgent
cat > ~/Library/LaunchAgents/com.claudecode.telegram.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claudecode.telegram</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>-m</string>
        <string>poetry</string>
        <string>run</string>
        <string>claude-telegram-bot</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/Claude-Code-Telegram-Boss</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load and start
launchctl load ~/Library/LaunchAgents/com.claudecode.telegram.plist
```

---

## 📖 Usage

### Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot and show welcome |
| `/help` | Display available commands |
| `/new` | Start a fresh Claude session |
| `/continue` | Resume previous session |
| `/ls` | List files in current directory |
| `/cd <dir>` | Change working directory |
| `/pwd` | Show current directory |
| `/projects` | Browse available projects |
| `/status` | Check session status and usage |
| `/git` | Git integration menu |

### Natural Language Chat

Just chat naturally:

```
You: Create a Python FastAPI server with JWT authentication
Claude: I'll create that for you... [executes tools]

You: Add rate limiting to the /api endpoints  
Claude: Done! Added rate limiting using slowapi...
```

### File Uploads

Send any file to chat:
- 📄 **Code files** - Python, JavaScript, TypeScript, etc.
- 📝 **Text files** - Markdown, JSON, YAML
- 🖼️ **Images** - Screenshots for analysis

---

## ⚙️ Configuration

### Security Modes

| Mode | Setting | Security Level |
|------|---------|---------------|
| **Default** | All validation enabled | 🔒 Maximum |
| **Relaxed** | `DISABLE_PATH_VALIDATION=true` | ⚠️ Medium |
| **Trust** | `TRUST_CLAUDE_COMPLETELY=true` | 🔓 Minimal |

> [!CAUTION]  
> Only use Trust mode for personal use with full understanding of risks!

### All Environment Variables

```env
# Required
TELEGRAM_BOT_TOKEN=your_token
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/your/projects/path

# Security (optional)
TRUST_CLAUDE_COMPLETELY=false
DISABLE_PATH_VALIDATION=false
DISABLE_DANGEROUS_PATTERN_CHECK=false

# Rate Limiting (optional)
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60

# Claude Tools (optional)
CLAUDE_ALLOWED_TOOLS=["Read","Write","Edit","Bash","Glob","Grep","LS","Task"]
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot not responding | Check `TELEGRAM_BOT_TOKEN` is correct |
| "User not authorized" | Add your ID to `ALLOWED_USERS` |
| "Path outside approved" | Set `DISABLE_PATH_VALIDATION=true` or expand `APPROVED_DIRECTORY` |
| Tool validation failed | Enable `TRUST_CLAUDE_COMPLETELY=true` |
| Rate limit exceeded | Increase `RATE_LIMIT_REQUESTS` value |

---

## 💖 Support & Donations

If this project helps you, consider supporting development:

| Method | Address/Link |
|--------|--------------|
| 🇻🇳 **Vietnam** | Vietcombank: `0071001215286` (LE BA THANG) |
| 💳 **PayPal** | `wikigamingmovies@gmail.com` |
| 💚 **USDT (TRC20)** | `TNGsaurWeFhaPPs1yxJ3AY15j1tDecX7ya` |
| 💛 **USDT (BEP20)** | `0x463695638788279F234386a77E0afA2Ee87b57F5` |
| 💜 **Solana (SOL)** | `HkgpzujF8uTBuYEYGSFMnmGzBYmEFyajzTiZacRtXzTr` |

---

## 👨‍💻 Credits

- **[Anthropic](https://www.anthropic.com/)** - Claude AI
- **[python-telegram-bot](https://python-telegram-bot.org/)** - Telegram library
- **[RichardAtCT/claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram)** - Original inspiration

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**[⬆ Back to Top](#-claude-code-telegram-boss)**

Made with ❤️ by the Vibecoder community

</div>