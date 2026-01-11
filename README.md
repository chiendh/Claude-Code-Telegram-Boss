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

# 🤖 Claude Code Telegram Boss - Vibecoder Edition 😎

> **Cảnh báo:** Bot này không dành cho người nghiêm túc. Chỉ dành cho các "Vibecoder" hệ tư tưởng Code Đêm.

**Điều khiển Claude Code CLI từ xa qua Telegram**

*Tưởng tượng bạn đang nằm ườn trên giường lướt điện thoại, nhưng sếp gọi bảo "fix bug gấp". 
Thay vì bật dậy mở laptop, bạn chỉ cần chat với con bot này.*

*Biến Telegram thành cái Terminal xịn xò, có sẵn "thư ký chân dài" Claude Code trực chiến 24/7.*

[Tính Năng](#-tính-năng-bá-đạo) •
[Cài Đặt](#-cài-đặt-nhanh-gọn) •
[Cách Dùng](#-cách-dùng-cho-pro) •
[Bảo Mật](#-bảo-mật-tận-răng) •
[Ủng Hộ](#-ủng-hộ-dự-án)

</div>

![Claude Code Telegram Boss](docs/ScreenShot.jpeg)

---

## 🚀 Tính Năng Bá Đạo

| Feature | Mô Tả |
|---------|-------|
| 🧠 **Chat như người thật** | Claude nhớ hết lịch sử chat, không như mấy con bot "cá vàng" |
| 📁 **Terminal bỏ túi** | `/ls`, `/cd` như hacker lỏ |
| 🔧 **Full Quyền Tool** | Read, Write, Edit, Bash, Glob, Grep... muốn gì có đó |
| 💬 **Nút bấm tiện lợi** | UI/UX "cơm bưng nước rót", không cần gõ lệnh nhiều đau tay |
| 📊 **Theo dõi Real-time** | Xem Claude đang làm gì, chạy tool nào |
| 🔐 **Bảo mật tận răng** | Sandbox thư mục an toàn, không lo Claude táy máy xóa nhầm `System32` |
| 📱 **Mobile-First** | Coding trên giường, trên toilet, trên xe buýt... đâu cũng được |

## 🛠 Cài Đặt Nhanh Gọn

### Chuẩn bị đồ nghề

- **Python 3.10+** (càng mới càng tốt)
- **Claude Code CLI** đã login:
  ```bash
  npm install -g @anthropic-ai/claude-code
  claude login
  ```
- **Telegram Bot Token** (xin @BotFather)

### Kéo code về và chạy

```bash
# Clone repo
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# Cài dependencies
pip install poetry
poetry install

# Cấu hình
cp .env.example .env
nano .env  # Sửa Token Bot và ID Telegram của bạn

# Chạy thôi
./start_bot.sh
```

### Chạy ngầm vĩnh viễn (macOS)

```bash
# Copy LaunchAgent
cp com.vibecode.claude-bot.plist ~/Library/LaunchAgents/

# Load và start
launchctl load ~/Library/LaunchAgents/com.vibecode.claude-bot.plist
launchctl start com.vibecode.claude-bot
```

## 🎮 Cách Dùng Cho Pro

Gõ `/start` để bot chào đón bạn nồng nhiệt.

| Lệnh | Tác dụng |
| :--- | :--- |
| `/new` | Reset não cho Claude, bắt đầu phiên mới |
| `/continue` | Nhắc Claude nhớ lại cuộc nói chuyện cũ |
| `/ls` | Soi xem trong thư mục có gì |
| `/cd <tên>` | Chui vào thư mục (ví dụ `/cd du_an_trieu_do`) |
| `/projects` | Liệt kê các kèo thơm đang có |
| `/status` | Xem Claude còn sống không, hay hết tiền API |
| `/git` | Ra lệnh cho git |

### Chat tự nhiên

Cứ chat như người thật:

```
Bạn: Ê Claude, viết cho tao cái script Python đào coin.
Claude: Đang viết cho anh đây...

Bạn: Thêm cái rate limiting vào đi
Claude: Done! Em đã thêm rate limiting bằng slowapi...
```

### Gửi file

- 📄 Gửi file code để review
- 🖼️ Gửi screenshot lỗi để Claude debug
- 📝 Gửi file log để phân tích

## ⚙️ Cấu Hình Bí Mật (.env)

### Bắt buộc

```env
TELEGRAM_BOT_TOKEN=token_từ_botfather
ALLOWED_USERS=["id_telegram_của_bạn"]  # Lấy từ @userinfobot
APPROVED_DIRECTORY=/đường/dẫn/thư/mục/code
```

### Tùy chọn

```env
# Mode tin tưởng tuyệt đối (chỉ dùng khi hiểu rõ rủi ro)
TRUST_CLAUDE_COMPLETELY=false
DISABLE_PATH_VALIDATION=false
DISABLE_DANGEROUS_PATTERN_CHECK=false

# Giới hạn request
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW_SECONDS=60

# Tool được phép
CLAUDE_ALLOWED_TOOLS=["Read", "Write", "Edit", "Bash", "Glob", "Grep", "LS"]
```

## 🔐 Bảo Mật Tận Răng

1. **Whitelist User** - Chỉ mình bạn (hoặc hội anh em được duyệt) mới chat được
2. **Sandbox Thư Mục** - Claude chỉ được loanh quanh trong thư mục approved
3. **Validate Tool** - Mỗi tool call đều được check trước khi chạy
4. **Rate Limiting** - Không lo bị spam hết tiền API
5. **Audit Log** - Ghi lại mọi hành động để review

### Trust Modes

| Mode | Mức Bảo Mật | Khi Nào Dùng |
|------|-------------|--------------|
| Default | 🔒 Tối đa | Production |
| `DISABLE_PATH_VALIDATION=true` | ⚠️ Trung bình | Dev với người tin tưởng |
| `TRUST_CLAUDE_COMPLETELY=true` | 🔓 Tối thiểu | Chỉ dùng cá nhân |

## 🏗️ Kiến Trúc

```
claude-code-telegram-boss/
├── src/
│   ├── bot/              # Telegram bot handlers
│   │   ├── handlers/     # Command & message handlers
│   │   ├── features/     # Optional features
│   │   └── utils/        # Formatting & utilities
│   ├── claude/           # Claude integration
│   ├── config/           # Configuration
│   └── security/         # Auth, rate limiting, validators
├── data/                 # SQLite database
└── docs/                 # Documentation
```

## 🤝 Contributing

Contributions are welcome! Feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/TinhNangMoi`)
3. Commit your changes (`git commit -m 'Thêm tính năng xịn'`)
4. Push to the branch (`git push origin feature/TinhNangMoi`)
5. Open a Pull Request

## 💖 Ủng Hộ Dự Án

Nếu thấy project này hữu ích, hãy ủng hộ để mình có động lực phát triển tiếp:

| Phương thức | Địa chỉ |
|-------------|---------|
| 💳 **PayPal** | `wikigamingmovies@gmail.com` |
| 💚 **USDT (TRC20)** | `TNGsaurWeFhaPPs1yxJ3AY15j1tDecX7ya` |
| 💛 **USDT (BEP20)** | `0x463695638788279F234386a77E0afA2Ee87b57F5` |
| 💜 **Solana (SOL)** | `HkgpzujF8uTBuYEYGSFMnmGzBYmEFyajzTiZacRtXzTr` |

## 📄 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 🙏 Credits

- [Anthropic](https://www.anthropic.com/) - Claude AI
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram library
- [RichardAtCT/claude-code-telegram](https://github.com/RichardAtCT/claude-code-telegram) - Inspiration

---

<div align="center">

**[⬆ Lên đầu trang](#-claude-code-telegram-boss---vibecoder-edition-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>