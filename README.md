![Vibecoder Dashboard](docs/ScreenShot.jpeg)

# Claude Code Telegram Boss - Vibecoder Edition 😎

> **Cảnh báo:** Bot này không dành cho người nghiêm túc. Chỉ dành cho các "Vibecoder" hệ tư tưởng Code Đêm.

## 🤖 Nó là cái gì?

Đây là con hàng giúp bạn **điều khiển Claude Code CLI** từ xa qua Telegram.
Tưởng tượng bạn đang nằm ườn trên giường lướt điện thoại, nhưng sếp gọi bảo "fix bug gấp". Thay vì bật dậy mở laptop, bạn chỉ cần chat với con bot này.

Nó biến Telegram của bạn thành cái Terminal xịn xò, có sẵn "thư ký chân dài" Claude Code trực chiến 24/7.

## 🚀 Tính Năng Bá Đạo

*   **Chat như người thật**: Claude nhớ hết lịch sử chat, không như mấy con bot "cá vàng".
*   **Terminal bỏ túi**: `/ls`, `/cd` như hacker lỏ.
*   **Bảo mật tận răng**:
    *   Chỉ mình bạn (hoặc hội anh em được duyệt) mới chat được.
    *   Sandbox thư mục an toàn, không lo Claude táy máy xóa nhầm `System32`.
*   **Git Pro Vip**: Check branch, diff code ngay trên Telegram.
*   **Nút bấm tiện lợi**: UI/UX "cơm bưng nước rót", không cần gõ lệnh nhiều đau tay.

## 🛠 Cài Đặt Nhanh Gọn

### 1. Chuẩn bị đồ nghề
*   Python 3.10 trở lên (càng mới càng tốt).
*   Đã cài `claude` CLI và login (`npm i -g @anthropic-ai/claude-code`).
*   Một con bot Telegram (xin @BotFather).

### 2. Kéo code về
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss
```

### 3. Cài đặt & Cấu hình
```bash
# Cài dependencies
pip install poetry
poetry install

# Cấu hình biến môi trường
cp .env.example .env
nano .env
```
*Sửa file `.env` điền Token Bot và ID Telegram của bạn vào.*

### 4. Chạy thôi
```bash
# Chạy thẳng
./start_bot.sh

# Hoặc cài chạy ngầm vĩnh viễn (macOS)
cp com.vibecode.claude-bot.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.vibecode.claude-bot.plist
launchctl start com.vibecode.claude-bot
```

## 🎮 Cách Dùng Cho Pro

Gõ `/start` để bot chào đón bạn nồng nhiệt.

| Lệnh | Tác dụng |
| :--- | :--- |
| `/new` | Reset não cho Claude, bắt đầu phiên mới |
| `/ls` | Soi xem trong thư mục có gì |
| `/cd <tên>` | Chui vào thư mục (ví dụ `/cd du_an_trieu_do`) |
| `/projects` | Liệt kê các kèo thơm đang có |
| `/status` | Xem Claude còn sống không, hay hết tiền API |
| `/git` | Ra lệnh cho git |

**Mẹo nhỏ:**
*   Cứ chat tự nhiên: *"Ê Claude, viết cho tao cái script Python đào coin."*
*   Gửi file ảnh, file log lỗi vào chat, nó đọc được hết.

## ⚙️ Cấu Hình Bí Mật (.env)

*   `ALLOWED_USERS`: ID của bạn (lấy từ @userinfobot). Đừng để trống kẻo cả làng vào dùng chùa.
*   `APPROVED_DIRECTORY`: Thư mục gốc chứa code. Claude chỉ được phép loanh quanh trong này thôi.
*   `CLAUDE_ALLOWED_TOOLS`: Các quyền bạn cấp cho Claude (đọc, ghi file, chạy lệnh bash...).

---
*Made with ❤️ & ☕ by a Vibecoder*