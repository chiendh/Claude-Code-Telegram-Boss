<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

# 🤖 Claude Code Telegram Boss - Édition Vibecoder 😎

> **Attention :** Ce bot n'est pas pour les personnes sérieuses. Réservé aux codeurs nocturnes "Vibecoder".

**Contrôlez Claude Code CLI à distance via Telegram**

*Transformez Telegram en un Terminal puissant avec Claude Code comme assistant IA 24/7.*

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

[Fonctionnalités](#-fonctionnalités-puissantes) • [Installation](#-installation-rapide) • [Docs](#-documentation) • [Sécurité](#-sécurité-renforcée)

</div>

![Claude Code Telegram Boss](../ScreenShot.jpeg)

---

## 🚀 Fonctionnalités Puissantes

| Fonctionnalité | Description |
|----------------|-------------|
| 🧠 **Chat Agentique** | Toutes les capacités de Claude Code : Read, Write, Bash, Git... |
| 📁 **Explorateur de Fichiers** | Parcourir les fichiers, voir le code, supprimer avec des boutons inline |
| 📊 **Intégration Git** | Vérifier le statut, diff, logs directement dans Telegram |
| 🔐 **Sécurité d'Abord** | Sandbox de répertoire, liste blanche, logs d'audit, limitation de débit |
| ⚡ **Cœur Asynchrone** | Architecture asynchrone pour des performances ultra-rapides |

## 🛠 Installation Rapide

### 1. Prérequis
- **Python 3.10+**
- **Claude Code** (connecté) : `npm install -g @anthropic-ai/claude-code && claude login`
- **Telegram Bot Token** (depuis @BotFather)

### 2. Installation
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# Installer les dépendances
pip install poetry
poetry install

# Configuration
cp .env.example .env
# Modifier .env : ajouter Bot Token, utilisateurs autorisés, répertoire approuvé
```

### 3. Lancer
```bash
./start_bot.sh
```

## 📚 Documentation

La documentation détaillée est disponible dans le dossier `docs/` :

- [📝 Aperçu du Projet et PDR](../project-overview-pdr.md) - Vue d'ensemble et exigences du projet.
- [🏗️ Architecture Système](../system-architecture.md) - Détails de l'architecture système.
- [💻 Résumé du Code](../codebase-summary.md) - Structure du code pour les développeurs.
- [📏 Standards de Code](../code-standards.md) - Standards de codage et workflows.

## 🎮 Guide Utilisateur

### Commandes de Base
| Commande | Description |
| :--- | :--- |
| `/start` | Démarrer le bot |
| `/new` | Créer nouvelle session (réinitialiser le contexte) |
| `/ls`, `/cd`, `/pwd` | Parcourir les fichiers avec des commandes |
| `/browse` | Ouvrir l'explorateur de fichiers (UI) |
| `/git` | Menu Git (Status, Log, Diff) |

### Exemple
> **Vous :** "Corrige le bug dans le fichier `src/main.py`, ligne 50 a une erreur d'import."
>
> **Claude :** "D'accord, je vérifie ce fichier..." (Exécute l'outil `Read`) -> "Erreur trouvée, correction..." (Exécute l'outil `Edit`) -> "Terminé !"

## ⚙️ Configuration (.env)

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/path/to/your/project
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔐 Sécurité Renforcée

1. **Liste Blanche d'Utilisateurs :** Seuls les IDs autorisés peuvent interagir avec le bot.
2. **Sandbox de Répertoire :** Le bot est limité à `APPROVED_DIRECTORY`.
3. **Logs d'Audit :** Toutes les actions sensibles sont enregistrées.
4. **Filtres d'Outils :** Bloque les commandes dangereuses (`rm -rf`, `format`, etc.).

---

<div align="center">

**[⬆ Retour en haut](#-claude-code-telegram-boss---édition-vibecoder-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>
