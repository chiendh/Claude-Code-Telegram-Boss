<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

# 🤖 Claude Code Telegram Boss - Vibecoder Edition 😎

> **Warnung:** Dieser Bot ist nicht für ernsthafte Leute. Nur für "Vibecoder" Nacht-Programmierer.

**Claude Code CLI fernsteuern via Telegram**

*Verwandeln Sie Telegram in ein leistungsstarkes Terminal mit Claude Code als Ihr 24/7 KI-Assistent.*

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

[Features](#-leistungsstarke-features) • [Installation](#-schnellinstallation) • [Docs](#-dokumentation) • [Sicherheit](#-robuste-sicherheit)

</div>

![Claude Code Telegram Boss](../ScreenShot.jpeg)

---

## 🚀 Leistungsstarke Features

| Feature | Beschreibung |
|---------|--------------|
| 🧠 **Agentischer Chat** | Volle Claude Code Funktionen: Read, Write, Bash, Git... |
| 📁 **Dateibrowser** | Dateien durchsuchen, Code ansehen, löschen mit Inline-Buttons |
| 📊 **Git Integration** | Status, Diff, Logs direkt in Telegram prüfen |
| 🔐 **Sicherheit Zuerst** | Verzeichnis-Sandbox, Whitelist, Audit-Logs, Rate-Limiting |
| ⚡ **Async Core** | Asynchrone Architektur für blitzschnelle Performance |

## 🛠 Schnellinstallation

### 1. Voraussetzungen
- **Python 3.10+**
- **Claude Code** (eingeloggt): `npm install -g @anthropic-ai/claude-code && claude login`
- **Telegram Bot Token** (von @BotFather)

### 2. Installation
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# Abhängigkeiten installieren
pip install poetry
poetry install

# Konfiguration
cp .env.example .env
# .env bearbeiten: Bot Token, erlaubte Benutzer, genehmigtes Verzeichnis hinzufügen
```

### 3. Ausführen
```bash
./start_bot.sh
```

## 📚 Dokumentation

Detaillierte Dokumentation ist im `docs/` Ordner verfügbar:

- [📝 Projektübersicht & PDR](../project-overview-pdr.md) - Projektübersicht und Anforderungen.
- [🏗️ Systemarchitektur](../system-architecture.md) - Details zur Systemarchitektur.
- [💻 Codebase-Zusammenfassung](../codebase-summary.md) - Code-Struktur für Entwickler.
- [📏 Code-Standards](../code-standards.md) - Codierungsstandards und Workflows.

## 🎮 Benutzerhandbuch

### Basisbefehle
| Befehl | Beschreibung |
| :--- | :--- |
| `/start` | Bot starten |
| `/new` | Neue Sitzung erstellen (Kontext zurücksetzen) |
| `/ls`, `/cd`, `/pwd` | Dateien mit Befehlen durchsuchen |
| `/browse` | Dateibrowser öffnen (UI) |
| `/git` | Git-Menü (Status, Log, Diff) |

### Beispiel
> **Sie:** "Behebe den Bug in der Datei `src/main.py`, Zeile 50 hat einen Import-Fehler."
>
> **Claude:** "Ok, lass mich die Datei prüfen..." (`Read` Tool ausführen) -> "Fehler gefunden, behebe..." (`Edit` Tool ausführen) -> "Fertig!"

## ⚙️ Konfiguration (.env)

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/path/to/your/project
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔐 Robuste Sicherheit

1. **Benutzer-Whitelist:** Nur autorisierte IDs können mit dem Bot interagieren.
2. **Verzeichnis-Sandbox:** Bot ist auf `APPROVED_DIRECTORY` beschränkt.
3. **Audit-Logs:** Alle sensiblen Aktionen werden protokolliert.
4. **Tool-Filter:** Blockiert gefährliche Befehle (`rm -rf`, `format`, etc.).

---

<div align="center">

**[⬆ Nach oben](#-claude-code-telegram-boss---vibecoder-edition-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>
