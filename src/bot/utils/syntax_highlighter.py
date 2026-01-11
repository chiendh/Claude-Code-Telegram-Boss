"""Syntax highlighting utilities for code formatting.

Provides syntax highlighting for code snippets in Telegram messages
using Pygments library.
"""

import re
from io import BytesIO
from typing import Optional, Tuple

import structlog

logger = structlog.get_logger()

# Language detection patterns
LANGUAGE_PATTERNS = {
    "python": [r"^import\s", r"^from\s.*import", r"^def\s", r"^class\s", r"print\("],
    "javascript": [r"^const\s", r"^let\s", r"^var\s", r"^function\s", r"console\.log"],
    "typescript": [r"^interface\s", r"^type\s", r":\s*\w+\s*=", r"<\w+>"],
    "java": [r"^public class", r"^private\s", r"System\.out\.println"],
    "go": [r"^package\s", r"^func\s", r"fmt\.Print"],
    "rust": [r"^fn\s", r"^pub\s", r"println!"],
    "c": [r"^#include", r"printf\("],
    "cpp": [r"^#include", r"std::"],
    "ruby": [r"^def\s", r"^class\s", r"puts\s"],
    "php": [r"^<\?php", r"\$\w+\s*="],
    "bash": [r"^#!/bin/bash", r"^\w+\s*=", r"\$\{"],
    "yaml": [r"^\w+:", r"^-\s"],
    "json": [r"^{", r"^\[", r"\":\s*[{\[]"],
    "sql": [r"^SELECT", r"^INSERT", r"^UPDATE", r"^CREATE"],
    "html": [r"^<!DOCTYPE", r"^<html", r"<\/\w+>"],
    "css": [r"{\s*$", r":\s*.*;"],
    "markdown": [r"^#{1,6}\s", r"^\*\*", r"^\-\s", r"^\d+\."],
}


def detect_language(code: str) -> Optional[str]:
    """Detect programming language from code content."""
    if not code:
        return None

    code_lower = code.lower()
    lines = code.split("\n")

    # Check first few lines for patterns
    check_lines = "\n".join(lines[:10])

    for lang, patterns in LANGUAGE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, check_lines, re.MULTILINE | re.IGNORECASE):
                logger.debug("Detected language", language=lang, pattern=pattern)
                return lang

    # Fallback heuristics
    if "{" in code and "}" in code:
        if "function" in code_lower or "const" in code_lower:
            return "javascript"
        if "class" in code_lower and ("public" in code_lower or "private" in code_lower):
            return "java"

    return None


def extract_code_blocks(text: str) -> list[Tuple[str, Optional[str], str]]:
    """Extract code blocks from markdown text.

    Returns list of tuples: (full_match, language, code)
    """
    # Match both ``` and ` code blocks
    pattern = r"```(\w+)?\n(.*?)```|`([^`]+)`"
    matches = []

    for match in re.finditer(pattern, text, re.DOTALL):
        if match.group(1) is not None:  # Triple backtick with language
            lang = match.group(1)
            code = match.group(2)
            matches.append((match.group(0), lang, code.strip()))
        elif match.group(2) is not None:  # Triple backtick without language
            code = match.group(2)
            detected_lang = detect_language(code)
            matches.append((match.group(0), detected_lang, code.strip()))
        elif match.group(3) is not None:  # Single backtick
            code = match.group(3)
            # Don't highlight inline code (too short)
            if len(code) < 50:
                continue
            detected_lang = detect_language(code)
            matches.append((match.group(0), detected_lang, code.strip()))

    return matches


def should_highlight(code: str, language: Optional[str]) -> bool:
    """Determine if code should be syntax highlighted."""
    # Don't highlight if too short
    if len(code) < 20:
        return False

    # Don't highlight if no language detected
    if not language:
        return False

    # Don't highlight plain text or markdown
    if language in ["text", "markdown", "md"]:
        return False

    # Don't highlight if code is already too long for Telegram
    if len(code) > 4000:
        return False

    return True


def format_code_with_language(code: str, language: str) -> str:
    """Format code with language tag for better Telegram rendering."""
    # Use Telegram's MarkdownV2 code block format
    # This provides basic syntax highlighting in Telegram
    return f"```{language}\n{code}\n```"


def truncate_code(code: str, max_length: int = 3000) -> str:
    """Truncate code if too long."""
    if len(code) <= max_length:
        return code

    # Truncate and add marker
    truncated = code[:max_length]
    return truncated + "\n\n... (truncated)"


# Try to import Pygments for advanced highlighting (optional)
try:
    from pygments import highlight
    from pygments.formatters import TerminalFormatter, Terminal256Formatter
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.util import ClassNotFound

    PYGMENTS_AVAILABLE = True
    logger.info("Pygments available for advanced syntax highlighting")

except ImportError:
    PYGMENTS_AVAILABLE = False
    logger.info("Pygments not available, using basic highlighting")


def highlight_code_pygments(code: str, language: Optional[str] = None) -> str:
    """Highlight code using Pygments (if available).

    Returns ANSI-colored code or original code if Pygments unavailable.
    """
    if not PYGMENTS_AVAILABLE:
        return code

    try:
        # Get lexer
        if language:
            try:
                lexer = get_lexer_by_name(language)
            except ClassNotFound:
                lexer = guess_lexer(code)
        else:
            lexer = guess_lexer(code)

        # Use Terminal256Formatter for better colors
        formatter = Terminal256Formatter(style="monokai")

        # Highlight
        highlighted = highlight(code, lexer, formatter)
        return highlighted

    except Exception as e:
        logger.warning("Failed to highlight with Pygments", error=str(e))
        return code


def enhance_code_formatting(text: str, use_pygments: bool = False) -> str:
    """Enhance code formatting in text.

    Args:
        text: Text potentially containing code blocks
        use_pygments: Whether to use Pygments for highlighting (requires conversion)

    Returns:
        Text with enhanced code formatting
    """
    # Extract code blocks
    code_blocks = extract_code_blocks(text)

    if not code_blocks:
        return text

    # Replace each code block with enhanced version
    result = text
    for full_match, language, code in code_blocks:
        if should_highlight(code, language):
            # Truncate if needed
            processed_code = truncate_code(code)

            if use_pygments and PYGMENTS_AVAILABLE:
                # Use Pygments highlighting
                highlighted = highlight_code_pygments(processed_code, language)
                enhanced = f"```\n{highlighted}\n```"
            else:
                # Use basic Telegram formatting
                enhanced = format_code_with_language(processed_code, language or "")

            result = result.replace(full_match, enhanced, 1)

    return result
