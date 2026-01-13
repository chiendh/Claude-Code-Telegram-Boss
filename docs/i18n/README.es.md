<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

# 🤖 Claude Code Telegram Boss - Edición Vibecoder 😎

> **Advertencia:** Este bot no es para gente seria. Solo para "Vibecoders" programadores nocturnos.

**Controla Claude Code CLI remotamente vía Telegram**

*Transforma Telegram en un Terminal potente con Claude Code como tu asistente IA 24/7.*

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

[Características](#-características-poderosas) • [Instalación](#-instalación-rápida) • [Docs](#-documentación) • [Seguridad](#-seguridad-robusta)

</div>

![Claude Code Telegram Boss](../ScreenShot.jpeg)

---

## 🚀 Características Poderosas

| Característica | Descripción |
|----------------|-------------|
| 🧠 **Chat Agéntico** | Todas las capacidades de Claude Code: Read, Write, Bash, Git... |
| 📁 **Explorador de Archivos** | Navega archivos, ve código, elimina con botones inline |
| 📊 **Integración Git** | Verifica estado, diff, logs directamente en Telegram |
| 🔐 **Seguridad Primero** | Sandbox de directorio, lista blanca, logs de auditoría, límite de tasa |
| ⚡ **Núcleo Asíncrono** | Arquitectura asíncrona para rendimiento ultrarrápido |

## 🛠 Instalación Rápida

### 1. Requisitos Previos
- **Python 3.10+**
- **Claude Code** (conectado): `npm install -g @anthropic-ai/claude-code && claude login`
- **Telegram Bot Token** (desde @BotFather)

### 2. Instalación
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# Instalar dependencias
pip install poetry
poetry install

# Configuración
cp .env.example .env
# Editar .env: agregar Bot Token, usuarios permitidos, directorio aprobado
```

### 3. Ejecutar
```bash
./start_bot.sh
```

## 📚 Documentación

La documentación detallada está disponible en la carpeta `docs/`:

- [📝 Resumen del Proyecto y PDR](../project-overview-pdr.md) - Resumen del proyecto y requisitos.
- [🏗️ Arquitectura del Sistema](../system-architecture.md) - Detalles de arquitectura del sistema.
- [💻 Resumen del Código](../codebase-summary.md) - Estructura del código para desarrolladores.
- [📏 Estándares de Código](../code-standards.md) - Estándares de codificación y flujos de trabajo.

## 🎮 Guía de Usuario

### Comandos Básicos
| Comando | Descripción |
| :--- | :--- |
| `/start` | Iniciar el bot |
| `/new` | Crear nueva sesión (reiniciar contexto) |
| `/ls`, `/cd`, `/pwd` | Navegar archivos con comandos |
| `/browse` | Abrir explorador de archivos (UI) |
| `/git` | Menú Git (Estado, Log, Diff) |

### Ejemplo
> **Tú:** "Arregla el bug en el archivo `src/main.py`, la línea 50 tiene error de import."
>
> **Claude:** "Ok, déjame revisar ese archivo..." (Ejecuta herramienta `Read`) -> "Error encontrado, arreglando..." (Ejecuta herramienta `Edit`) -> "¡Listo!"

## ⚙️ Configuración (.env)

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/path/to/your/project
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔐 Seguridad Robusta

1. **Lista Blanca de Usuarios:** Solo IDs autorizados pueden interactuar con el bot.
2. **Sandbox de Directorio:** El bot está restringido a `APPROVED_DIRECTORY`.
3. **Logs de Auditoría:** Todas las acciones sensibles se registran.
4. **Filtros de Herramientas:** Bloquea comandos peligrosos (`rm -rf`, `format`, etc.).

---

<div align="center">

**[⬆ Volver arriba](#-claude-code-telegram-boss---edición-vibecoder-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>
