<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

# 🤖 Claude Code Telegram Boss - Vibecoder Edition 😎

> **Cảnh báo:** Bot này không dành cho người nghiêm túc. Chỉ dành cho các "Vibecoder" hệ tư tưởng Code Đêm.

**Điều khiển Claude Code CLI từ xa qua Telegram**

*Biến Telegram thành cái Terminal xịn xò, có sẵn "thư ký chân dài" Claude Code trực chiến 24/7.*

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

[Tính Năng](#-tính-năng-bá-đạo) • [Cài Đặt](#-cài-đặt-nhanh-gọn) • [Docs](#-documentation) • [Bảo Mật](#-bảo-mật-tận-răng)

</div>

![Claude Code Telegram Boss](../ScreenShot.jpeg)

---

## 🚀 Tính Năng Bá Đạo

| Feature | Mô Tả |
|---------|-------|
| 🧠 **Chat Agentic** | Claude Code đầy đủ sức mạnh: Read, Write, Bash, Git... |
| 📁 **File Browser** | Duyệt file, xem code, xóa file bằng nút bấm Inline |
| 📊 **Git Integration** | Check status, diff, log ngay trong Telegram |
| 🔐 **Security First** | Sandbox thư mục, Whitelist User, Audit Log, Rate Limit |
| ⚡ **Async Core** | Kiến trúc bất đồng bộ, nhanh như người yêu cũ trở mặt |

## 🛠 Cài Đặt Nhanh Gọn

### 1. Chuẩn bị
- **Python 3.10+**
- **Claude Code** (đã login): `npm install -g @anthropic-ai/claude-code && claude login`
- **Telegram Bot Token** (từ @BotFather)

### 2. Cài đặt
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# Cài dependencies
pip install poetry
poetry install

# Cấu hình
cp .env.example .env
# Sửa .env: điền Token Bot, Allowed Users, Approved Directory
```

### 3. Chạy
```bash
./start_bot.sh
```

## 📚 Documentation

Tài liệu chi tiết nằm trong thư mục `docs/`:

- [📝 Project Overview & PDR](../project-overview-pdr.md) - Tổng quan dự án và yêu cầu.
- [🏗️ System Architecture](../system-architecture.md) - Kiến trúc hệ thống.
- [💻 Codebase Summary](../codebase-summary.md) - Cấu trúc code cho developers.
- [📏 Code Standards](../code-standards.md) - Chuẩn code và quy trình.

## 🎮 Hướng Dẫn Sử Dụng

### Lệnh Cơ Bản
| Lệnh | Tác dụng |
| :--- | :--- |
| `/start` | Khởi động bot |
| `/new` | Tạo session mới (reset context) |
| `/ls`, `/cd`, `/pwd` | Duyệt file bằng lệnh |
| `/browse` | Mở giao diện duyệt file (UI) |
| `/git` | Menu Git (Status, Log, Diff) |

### Ví dụ
> **Bạn:** "Fix bug ở file `src/main.py`, dòng 50 đang bị lỗi import."
>
> **Claude:** "Ok, để em check file đó..." (Chạy tool `Read`) -> "Đã thấy lỗi, đang sửa..." (Chạy tool `Edit`) -> "Done!"

## ⚙️ Cấu Hình (.env)

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/path/to/your/project
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔐 Bảo Mật Tận Răng

1. **Whitelist User:** Chỉ ID được cấp phép mới chat được.
2. **Directory Sandbox:** Bot bị nhốt trong `APPROVED_DIRECTORY`.
3. **Audit Log:** Mọi hành động nhạy cảm đều được ghi lại.
4. **Tool Filters:** Chặn các lệnh nguy hiểm (`rm -rf`, `format`, v.v.).

---

<div align="center">

**[⬆ Lên đầu trang](#-claude-code-telegram-boss---vibecoder-edition-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>
