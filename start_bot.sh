#!/bin/bash
cd "$(dirname "$0")"
export PATH="/usr/local/bin:$PATH"  # Ensure basic paths are present
# Run using the python/poetry environment we set up
/usr/bin/env python3 -m poetry run claude-telegram-bot
