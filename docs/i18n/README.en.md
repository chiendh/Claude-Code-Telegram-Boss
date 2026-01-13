<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

# 🤖 Claude Code Telegram Boss - Vibecoder Edition 😎

> **Warning:** This bot is not for serious people. Only for "Vibecoder" night-owl coders.

**Remote Control Claude Code CLI via Telegram**

*Transform Telegram into a powerful Terminal with Claude Code as your 24/7 AI assistant.*

---

### 🌍 Languages / Ngôn ngữ / 言語 / 语言

[![English](https://img.shields.io/badge/English-0075FF?style=flat-square)](README.en.md)
[![Vietnamese](https://img.shields.io/badge/Tiếng_Việt-FF0000?style=flat-square)](README.vi.md)
[![Chinese](https://img.shields.io/badge/简体中文-FF0000?style=flat-square)](README.zh.md)
[![Japanese](https://img.shields.io/badge/日本語-FF0000?style=flat-square)](README.ja.md)
[![Korean](https://img.shields.io/badge/한국어-FF0000?style=flat-square)](README.ko.md)
[![French](https://img.shields.io/badge/Français-FF0000?style=flat-square)](README.fr.md)
[![Spanish](https://img.shields.io/badge/Español-FF0000?style=flat-square)](README.es.md)
[![German](https://img.shields.io/badge/Deutsch-FF0000?style=flat-square)](README.de.md)

---

[Features](#-powerful-features) • [Installation](#-quick-installation) • [Docs](#-documentation) • [Security](#-rock-solid-security)

</div>

![Claude Code Telegram Boss](../ScreenShot.jpeg)

---

## 🚀 Powerful Features

| Feature | Description |
|---------|-------------|
| 🧠 **Agentic Chat** | Full Claude Code capabilities: Read, Write, Bash, Git... |
| 📁 **File Browser** | Browse files, view code, delete files with inline buttons |
| 📊 **Git Integration** | Check status, diff, log directly in Telegram |
| 🔐 **Security First** | Directory sandbox, user whitelist, audit logs, rate limiting |
| ⚡ **Async Core** | Asynchronous architecture for blazing-fast performance |

## 🛠 Quick Installation

### 1. Prerequisites
- **Python 3.10+**
- **Claude Code** (logged in): `npm install -g @anthropic-ai/claude-code && claude login`
- **Telegram Bot Token** (from @BotFather)

### 2. Installation
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# Install dependencies
pip install poetry
poetry install

# Configuration
cp .env.example .env
# Edit .env: add Bot Token, Allowed Users, Approved Directory
```

### 3. Run
```bash
./start_bot.sh
```

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:

- [📝 Project Overview & PDR](../project-overview-pdr.md) - Project overview and requirements.
- [🏗️ System Architecture](../system-architecture.md) - System architecture details.
- [💻 Codebase Summary](../codebase-summary.md) - Code structure for developers.
- [📏 Code Standards](../code-standards.md) - Coding standards and workflows.

## 🎮 User Guide

### Basic Commands
| Command | Description |
| :--- | :--- |
| `/start` | Start the bot |
| `/new` | Create new session (reset context) |
| `/ls`, `/cd`, `/pwd` | Browse files with commands |
| `/browse` | Open file browser (UI) |
| `/git` | Git menu (Status, Log, Diff) |

### Example
> **You:** "Fix bug in file `src/main.py`, line 50 has import error."
>
> **Claude:** "Ok, let me check that file..." (Runs `Read` tool) -> "Found the error, fixing..." (Runs `Edit` tool) -> "Done!"

## ⚙️ Configuration (.env)

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/path/to/your/project
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔐 Rock-Solid Security

1. **User Whitelist:** Only authorized IDs can interact with the bot.
2. **Directory Sandbox:** Bot is restricted to `APPROVED_DIRECTORY`.
3. **Audit Log:** All sensitive actions are logged.
4. **Tool Filters:** Blocks dangerous commands (`rm -rf`, `format`, etc.).

---

<div align="center">

**[⬆ Back to top](#-claude-code-telegram-boss---vibecoder-edition-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>
