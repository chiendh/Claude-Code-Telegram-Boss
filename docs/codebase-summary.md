# Codebase Summary

This document provides a comprehensive overview of the `Claude-Code-Telegram-Boss` codebase, generated from the repository content.

## Project Overview

**Claude Code Telegram Boss** is a Telegram bot that provides a remote interface to Anthropic's Claude Code CLI. It allows authorized users to interact with Claude Code through Telegram messages, enabling remote coding, file management, and system operations.

### Key Features

- **Agentic Chat**: Full access to Claude Code capabilities (Read, Write, Bash, Git, etc.)
- **File Browser**: Interactive UI for browsing, reading, and managing files
- **Git Integration**: View status, logs, diffs, and manage repositories
- **Session Management**: Persistent sessions with context preservation
- **Security**: Directory sandboxing, user whitelisting, audit logging, and tool validation
- **Async Core**: Built on `python-telegram-bot` and `asyncio` for high performance

## Architecture

The project follows a modular architecture with clear separation of concerns:

```
src/
├── bot/                 # Telegram bot implementation
│   ├── handlers/        # Command and message handlers
│   ├── features/        # Feature implementations (file browser, etc.)
│   └── utils/           # Bot-specific utilities
├── claude/              # Claude Code integration
│   ├── sdk_integration.py # Python SDK integration
│   ├── integration.py   # CLI subprocess integration (fallback)
│   ├── session.py       # Session management
│   └── monitor.py       # Tool execution monitoring
├── config/              # Configuration management
│   ├── settings.py      # Pydantic settings
│   └── features.py      # Feature flags
├── security/            # Security components
│   ├── auth.py          # Authentication providers
│   ├── audit.py         # Audit logging
│   ├── validators.py    # Path and input validation
│   └── rate_limiter.py  # Rate limiting
├── storage/             # Data persistence
│   └── session_storage.py # SQLite session storage
└── utils/               # General utilities
```

## Core Components

### 1. Claude Integration (`src/claude/`)

- **`ClaudeIntegration`** (`facade.py`): The main entry point for bot handlers. It coordinates between session management, tool monitoring, and the execution backend (SDK or subprocess).
- **`ClaudeSDKManager`** (`sdk_integration.py`): Manages communication with the `claude-code-sdk`. Handles streaming responses, tool calls, and session state.
- **`ClaudeProcessManager`** (`integration.py`): Legacy fallback that manages Claude Code via subprocess when the SDK is unavailable or encounters errors.
- **`SessionManager`** (`session.py`): Handles user sessions, storage, retrieval, and expiration logic.

### 2. Bot Implementation (`src/bot/`)

- **`ClaudeCodeBot`** (`core.py`): The main bot class that initializes the application and registers handlers.
- **Handlers**:
  - `command.py`: Handles slash commands (`/start`, `/help`, `/ls`, `/cd`, etc.).
  - `message.py`: Processes text messages as prompts for Claude.
  - `callback.py`: Handles inline keyboard interactions.
- **`ResponseFormatter`** (`utils/formatting.py`): Formats Claude's output for Telegram, including syntax highlighting, markdown escaping, and message splitting.

### 3. Security (`src/security/`)

- **`SecurityValidator`**: Enforces directory sandboxing (`APPROVED_DIRECTORY`) to prevent path traversal attacks.
- **`AuditLogger`**: Records all sensitive actions (commands, file access, tool usage) for security auditing.
- **`RateLimiter`**: Prevents abuse by limiting request frequency and cost per user.
- **`AuthenticationManager`**: Manages user authentication (currently whitelist-based).

### 4. Configuration (`src/config/`)

- **`Settings`**: Uses Pydantic to load and validate environment variables from `.env`.
- **`FeatureFlags`**: Manages enablement of optional features like Git integration, file uploads, etc.

## Data Flow

1. **User Input**: A user sends a message or command via Telegram.
2. **Bot Handling**: The `ClaudeCodeBot` receives the update and routes it to the appropriate handler.
3. **Security Check**: The handler checks authentication, rate limits, and input validity.
4. **Context Loading**: The handler retrieves the user's current directory and active session ID.
5. **Claude Execution**:
   - The handler calls `ClaudeIntegration.run_command()`.
   - `ClaudeIntegration` retrieves/creates a session via `SessionManager`.
   - The command is executed via `ClaudeSDKManager` (or fallback).
   - Streaming updates are processed to show progress.
6. **Tool Execution**:
   - Claude determines if tools (Read, Write, Bash) are needed.
   - `ToolMonitor` validates tool usage against allowed policies.
   - Tools are executed, and results are fed back to Claude.
7. **Response Formatting**: The final response is formatted by `ResponseFormatter`.
8. **Delivery**: The formatted response is sent back to the user via Telegram.

## Recent Changes

- **Empty Content Handling**: Fixed empty messages by generating tool summaries (Write, Bash) when Claude returns tool-only responses.
- **Security hardening**: Added tool name sanitization (alphanumeric + underscore) in `_generate_tool_summary`.
- **Safe Markdown Truncation**: Implemented `_safe_truncate_markdown` in `src/bot/handlers/message.py` to prevent broken markdown entities in previews.
- **Documentation Updates**: Updated README structure and documentation organization.
- **Vietnamese Captions**: Added localized captions for better user experience.

## Technology Stack

- **Language**: Python 3.10+
- **Bot Framework**: `python-telegram-bot`
- **AI Integration**: `claude-code-sdk` (Anthropic)
- **Configuration**: `pydantic-settings`
- **Logging**: `structlog`
- **Database**: `aiosqlite` (Async SQLite)
- **Testing**: `pytest`, `pytest-asyncio`

## Development Guidelines

- **Code Style**: Follow PEP 8. Use `black` and `isort` for formatting.
- **Async First**: All I/O operations must be asynchronous.
- **Type Hinting**: Use Python type hints throughout the codebase.
- **Security**: Always validate user input and paths. Never trust external data.
- **Error Handling**: Use structured logging and user-friendly error messages.
