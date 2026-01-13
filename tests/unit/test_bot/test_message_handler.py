import pytest
from src.bot.handlers.message import _safe_truncate_markdown, _format_tool_params

class TestSafeTruncateMarkdown:
    """Tests for _safe_truncate_markdown function."""

    def test_basic_truncation(self):
        """Test simple text truncation."""
        text = "This is a long text that needs truncation"
        result = _safe_truncate_markdown(text, 10, add_ellipsis=False)
        assert result == "This is a "
        assert len(result) == 10

    def test_truncation_with_ellipsis(self):
        """Test truncation with ellipsis added."""
        text = "This is a long text"
        result = _safe_truncate_markdown(text, 10, add_ellipsis=True)
        assert result == "This is a ..."
        assert result.endswith("...")

    def test_no_truncation_needed(self):
        """Test when text is shorter than max length."""
        text = "Short text"
        result = _safe_truncate_markdown(text, 20)
        assert result == "Short text"

    def test_unclosed_backtick(self):
        """Test handling of unclosed backticks."""
        # Truncating right after opening backtick
        text = "Code: `print('hello')`"
        # "Code: `pri" -> 9 chars
        result = _safe_truncate_markdown(text, 9, add_ellipsis=False)
        assert result == "Code: `pr`"  # Should add closing backtick

    def test_closed_backticks(self):
        """Test when backticks are already balanced."""
        text = "`code` normal"
        result = _safe_truncate_markdown(text, 6, add_ellipsis=False)
        assert result == "`code`"

    def test_multiple_backticks(self):
        """Test with multiple backtick pairs."""
        text = "`a` `b` `c`"
        # "`a` `b` `" -> 9 chars (leaves last one open)
        result = _safe_truncate_markdown(text, 9, add_ellipsis=False)
        assert result == "`a` `b` ``"  # Should close the last one

    def test_asterisks_truncation(self):
        """Test safe truncation with asterisks."""
        text = "**Bold text**"
        # "**Bol" -> 5 chars. Should append "**" ? Or just "*" if it assumes pairs?
        # Simple markdown usually uses * or **.
        # If we just count *, "**" is 2 stars. 2 is even.
        # But if we cut at "**Bol", we have 2 stars. Even. So no close.
        # But wait, "**Bol" is not closed.
        # Markdown parsers usually require closing tags.
        # If I have "**Bol", it renders as "**Bol".
        # If I have "*Italic", it renders as "*Italic".
        # The goal is to avoid "Can't parse entities" error from Telegram.
        # Telegram MarkdownV2 is strict.
        # Unclosed * or _ or ` causes errors.

        # Test case: Unclosed bold
        text = "*Bold*"
        # "*Bo" -> 3 chars. 1 star. Odd. Should close with *.
        result = _safe_truncate_markdown(text, 3, add_ellipsis=False)
        assert result == "*Bo*"

    def test_underscore_truncation(self):
        """Test safe truncation with underscores."""
        text = "_Italic_"
        # "_It" -> 3 chars. 1 underscore. Odd. Should close.
        result = _safe_truncate_markdown(text, 3, add_ellipsis=False)
        assert result == "_It_"


    def test_vietnamese_characters(self):
        """Test with UTF-8 characters."""
        text = "Xin chào các bạn"
        result = _safe_truncate_markdown(text, 8, add_ellipsis=False)
        assert result == "Xin chào"

    def test_emoji_characters(self):
        """Test with emoji characters."""
        text = "Hello 👋 world 🌍"
        result = _safe_truncate_markdown(text, 8, add_ellipsis=False)
        # "Hello 👋" is 7 chars (space) + 1 char (wave)
        assert result.startswith("Hello")

class TestFormatToolParams:
    """Tests for _format_tool_params function."""

    def test_bash_backtick_escape(self):
        """Test escaping backticks in Bash commands."""
        params = {"command": "echo `date`"}
        result = _format_tool_params("Bash", params)
        assert "echo 'date'" in result
        assert "`" in result  # Outer backticks for markdown code block

    def test_write_preview_truncation(self):
        """Test content preview truncation in Write tool."""
        long_content = "x" * 100
        params = {"file_path": "test.txt", "content": long_content}
        result = _format_tool_params("Write", params)
        assert "..." in result
        assert len(result) < 100

    def test_task_truncation(self):
        """Test task prompt truncation."""
        long_prompt = "Do " + "very " * 20 + "important things"
        params = {"prompt": long_prompt}
        result = _format_tool_params("Task", params)
        assert "..." in result
        assert len(result) < len(long_prompt)
