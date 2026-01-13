<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

# 🤖 Claude Code Telegram Boss - Vibecoder 에디션 😎

> **경고:** 이 봇은 진지한 사람들을 위한 것이 아닙니다. "Vibecoder" 야행성 코더 전용입니다.

**Telegram을 통해 Claude Code CLI를 원격 제어**

*Telegram을 강력한 터미널로 변환하고 Claude Code를 24/7 AI 어시스턴트로 활용하세요.*

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

[기능](#-강력한-기능) • [설치](#-빠른-설치) • [문서](#-문서) • [보안](#-견고한-보안)

</div>

![Claude Code Telegram Boss](../ScreenShot.jpeg)

---

## 🚀 강력한 기능

| 기능 | 설명 |
|------|------|
| 🧠 **에이전트 채팅** | 전체 Claude Code 기능: Read, Write, Bash, Git... |
| 📁 **파일 브라우저** | 인라인 버튼으로 파일 탐색, 코드 보기, 파일 삭제 |
| 📊 **Git 통합** | Telegram에서 직접 상태, 차이점, 로그 확인 |
| 🔐 **보안 우선** | 디렉토리 샌드박스, 사용자 화이트리스트, 감사 로그, 속도 제한 |
| ⚡ **비동기 코어** | 초고속 성능의 비동기 아키텍처 |

## 🛠 빠른 설치

### 1. 사전 요구사항
- **Python 3.10+**
- **Claude Code** (로그인 완료): `npm install -g @anthropic-ai/claude-code && claude login`
- **Telegram Bot Token** (@BotFather에서 받기)

### 2. 설치
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# 의존성 설치
pip install poetry
poetry install

# 구성
cp .env.example .env
# .env 편집: Bot Token, 허용된 사용자, 승인된 디렉토리 추가
```

### 3. 실행
```bash
./start_bot.sh
```

## 📚 문서

자세한 문서는 `docs/` 폴더에 있습니다:

- [📝 프로젝트 개요 및 PDR](../project-overview-pdr.md) - 프로젝트 개요 및 요구사항.
- [🏗️ 시스템 아키텍처](../system-architecture.md) - 시스템 아키텍처 세부정보.
- [💻 코드베이스 요약](../codebase-summary.md) - 개발자를 위한 코드 구조.
- [📏 코드 표준](../code-standards.md) - 코딩 표준 및 워크플로우.

## 🎮 사용자 가이드

### 기본 명령어
| 명령어 | 설명 |
| :--- | :--- |
| `/start` | 봇 시작 |
| `/new` | 새 세션 생성 (컨텍스트 리셋) |
| `/ls`, `/cd`, `/pwd` | 명령어로 파일 탐색 |
| `/browse` | 파일 브라우저 열기 (UI) |
| `/git` | Git 메뉴 (상태, 로그, 차이점) |

### 예시
> **당신:** "파일 `src/main.py`의 버그를 수정해 주세요. 50번째 줄에 import 오류가 있습니다."
>
> **Claude:** "알겠습니다. 해당 파일을 확인하겠습니다..." (`Read` 도구 실행) -> "오류를 찾았습니다. 수정 중..." (`Edit` 도구 실행) -> "완료!"

## ⚙️ 구성 (.env)

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/path/to/your/project
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔐 견고한 보안

1. **사용자 화이트리스트:** 승인된 ID만 봇과 상호작용 가능.
2. **디렉토리 샌드박스:** 봇은 `APPROVED_DIRECTORY`로 제한됩니다.
3. **감사 로그:** 모든 민감한 작업이 기록됩니다.
4. **도구 필터:** 위험한 명령어 차단 (`rm -rf`, `format` 등).

---

<div align="center">

**[⬆ 맨 위로](#-claude-code-telegram-boss---vibecoder-에디션-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>
