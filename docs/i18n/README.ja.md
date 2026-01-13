<div align="center">

![Claude Code](https://img.shields.io/badge/Claude-Code-0075FF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-❤️-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/0xAstroAlpha)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-☕-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/astroalpha)

# 🤖 Claude Code Telegram Boss - Vibecoder エディション 😎

> **警告：** このボットは真面目な人向けではありません。「Vibecoder」の夜型コーダー専用です。

**Telegram経由でClaude Code CLIをリモート制御**

*TelegramをパワフルなTerminalに変換し、Claude Codeを24時間365日のAIアシスタントに。*

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

[機能](#-強力な機能) • [インストール](#-クイックインストール) • [ドキュメント](#-ドキュメント) • [セキュリティ](#-堅牢なセキュリティ)

</div>

![Claude Code Telegram Boss](../ScreenShot.jpeg)

---

## 🚀 強力な機能

| 機能 | 説明 |
|------|------|
| 🧠 **エージェントチャット** | 完全なClaude Code機能：Read、Write、Bash、Git... |
| 📁 **ファイルブラウザ** | インラインボタンでファイルを閲覧、コードを表示、ファイルを削除 |
| 📊 **Git統合** | Telegram内で直接ステータス、差分、ログを確認 |
| 🔐 **セキュリティ優先** | ディレクトリサンドボックス、ユーザーホワイトリスト、監査ログ、レート制限 |
| ⚡ **非同期コア** | 超高速パフォーマンスの非同期アーキテクチャ |

## 🛠 クイックインストール

### 1. 前提条件
- **Python 3.10+**
- **Claude Code**（ログイン済み）：`npm install -g @anthropic-ai/claude-code && claude login`
- **Telegram Bot Token**（@BotFatherから取得）

### 2. インストール
```bash
git clone https://github.com/0xAstroAlpha/Claude-Code-Telegram-Boss.git
cd Claude-Code-Telegram-Boss

# 依存関係のインストール
pip install poetry
poetry install

# 設定
cp .env.example .env
# .envを編集：Bot Token、許可されたユーザー、承認されたディレクトリを追加
```

### 3. 実行
```bash
./start_bot.sh
```

## 📚 ドキュメント

詳細なドキュメントは `docs/` フォルダにあります：

- [📝 プロジェクト概要とPDR](../project-overview-pdr.md) - プロジェクト概要と要件。
- [🏗️ システムアーキテクチャ](../system-architecture.md) - システムアーキテクチャの詳細。
- [💻 コードベースサマリー](../codebase-summary.md) - 開発者向けコード構造。
- [📏 コード標準](../code-standards.md) - コーディング標準とワークフロー。

## 🎮 ユーザーガイド

### 基本コマンド
| コマンド | 説明 |
| :--- | :--- |
| `/start` | ボットを起動 |
| `/new` | 新しいセッションを作成（コンテキストをリセット） |
| `/ls`, `/cd`, `/pwd` | コマンドでファイルを閲覧 |
| `/browse` | ファイルブラウザを開く（UI） |
| `/git` | Gitメニュー（ステータス、ログ、差分） |

### 例
> **あなた：** "ファイル `src/main.py` のバグを修正して、50行目にインポートエラーがあります。"
>
> **Claude：** "了解しました、そのファイルをチェックします..." (`Read`ツールを実行) -> "エラーを発見しました、修正中..." (`Edit`ツールを実行) -> "完了！"

## ⚙️ 設定（.env）

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
ALLOWED_USERS=["your_telegram_id"]
APPROVED_DIRECTORY=/path/to/your/project
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

## 🔐 堅牢なセキュリティ

1. **ユーザーホワイトリスト：** 認可されたIDのみがボットと対話可能。
2. **ディレクトリサンドボックス：** ボットは `APPROVED_DIRECTORY` に制限されます。
3. **監査ログ：** すべての機密操作が記録されます。
4. **ツールフィルター：** 危険なコマンド（`rm -rf`、`format`など）をブロック。

---

<div align="center">

**[⬆ トップに戻る](#-claude-code-telegram-boss---vibecoder-エディション-)**

*Made with ❤️ & ☕ by a Vibecoder*

</div>
