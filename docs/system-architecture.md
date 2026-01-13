# System Architecture

## 1. High-Level Architecture

The **Claude Code Telegram Boss** operates as a bridge between the Telegram Messaging Platform and the local development environment (Claude Code/OS). It uses an asynchronous event-driven architecture to handle concurrent user requests efficiently.

```mermaid
graph TD
    User[User (Telegram)] <-->|HTTPS| TG[Telegram API]
    TG <-->|Webhook/Polling| Bot[Claude Code Bot]

    subgraph "Application Core"
        Bot -->|Dispatch| Router[Handler Router]
        Router -->|Validate| Middleware[Middleware Pipeline]
        Middleware -->|Process| Controller[Feature Controllers]
    end

    subgraph "Services"
        Controller -->|Auth/Audit| Security[Security Service]
        Controller -->|Query| DB[SQLite Storage]
        Controller -->|Execute| Claude[Claude Integration]
        Controller -->|Manage| System[OS / File System]
    end

    subgraph "External"
        Claude -->|API| Anthropic[Anthropic API]
        System -->|Shell| Git[Git / Bash Tools]
    end
```

## 2. Component Details

### 2.1 The Bot Engine (`src/bot`)
- Built on `python-telegram-bot`.
- **Polling/Webhook:** configurable listening mode.
- **Application Context:** Holds references to all singleton services (Storage, Auth, Claude Manager).

### 2.2 Middleware Pipeline
1. **Security:** Validates update structure and checks for global bans.
2. **Auth:** Authenticates `user_id`.
3. **RateLimit:** Checks token buckets.
4. **Context:** Injects dependencies into `context.bot_data`.

### 2.3 Claude Integration Layer (`src/claude`)
- **Strategy Pattern:** Supports two implementations:
  1. **CLI Wrapper:** Spawns `claude` subprocess, pipes `stdin`/ `stdout`, parses JSON stream.
  2. **SDK Native:** Uses `anthropic` Python SDK directly (Preferred).
- **Session Management:** Maintains conversation history `messages` list.
- **Tool Execution:** Intercepts tool calls from Claude, validates them via `SecurityValidator`, executes them (Read, Write, Bash), and feeds results back.
- **Response Handling:** Generates summaries for tool-only responses to prevent empty messages, ensuring user feedback even when Claude is silent.

### 2.4 Persistence Layer (`src/storage`)
- **SQLite:** Lightweight, serverless, file-based database.
- **Schema:**
  - `users`: User preferences and stats.
  - `sessions`: Active and archived conversation states.
  - `audit_logs`: Security and activity events.

## 3. Security Architecture

### 3.1 Trust Model
- **Zero Trust:** Even authenticated users are restricted.
- **Principle of Least Privilege:** Bot only accesses `APPROVED_DIRECTORY`.

### 3.2 Sandboxing
- **Path Validation:** All file operations run through a validator that ensures `path.resolve().is_relative_to(approved_root)`.
- **Command Whitelisting:** Only specific git and shell commands are allowed. Dangerous commands (`rm -rf /`, `mkfs`) are blocked by regex patterns in `Settings`.

### 3.3 Audit Trail
- Every "write" operation (File Edit, Shell Command) is logged with `timestamp`, `user_id`, `command`, and `risk_level`.

## 4. Scalability & Performance

- **AsyncIO:** The entire core is non-blocking.
- **Connection Pooling:** Database and HTTP connections are pooled.
- **Memory Management:** Large file reads are paginated. Claude outputs are streamed, not buffered in entirety.

## 5. Deployment View

- **Docker:** Can be containerized (Dockerfile provided).
- **Systemd:** Can run as a system service.
- **Requirements:**
  - Python 3.10+
  - Internet access (Telegram API, Anthropic API)
  - Write access to `data/` and `APPROVED_DIRECTORY`.
