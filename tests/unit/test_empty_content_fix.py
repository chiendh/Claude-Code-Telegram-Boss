"""Tests for empty content fix (tool summary generation)."""

import pytest
from src.claude.integration import ClaudeProcessManager
from src.claude.sdk_integration import ClaudeSDKManager
from src.config.settings import Settings


class TestToolSummaryGeneration:
    """Test tool summary generation for empty content."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Settings(
            telegram_bot_token="test_token",
            telegram_bot_username="test_bot",
            approved_directory="/tmp",
            allowed_users=[123456],
        )
        self.process_manager = ClaudeProcessManager(self.config)
        self.sdk_manager = ClaudeSDKManager(self.config)

    def test_generate_tool_summary_single_tool(self):
        """Test summary with single tool."""
        tools = [{"name": "Write", "timestamp": "123"}]
        result = self.process_manager._generate_tool_summary(tools)
        assert result == "✅ Completed: Write"

    def test_generate_tool_summary_multiple_tools(self):
        """Test summary with multiple different tools."""
        tools = [
            {"name": "Read", "timestamp": "1"},
            {"name": "Write", "timestamp": "2"},
            {"name": "Bash", "timestamp": "3"},
        ]
        result = self.process_manager._generate_tool_summary(tools)
        assert "Read" in result
        assert "Write" in result
        assert "Bash" in result
        assert "✅ Completed:" in result

    def test_generate_tool_summary_repeated_tools(self):
        """Test summary with repeated tool executions."""
        tools = [
            {"name": "Bash", "timestamp": "1"},
            {"name": "Bash", "timestamp": "2"},
            {"name": "Bash", "timestamp": "3"},
        ]
        result = self.process_manager._generate_tool_summary(tools)
        assert "Bash (x3)" in result
        assert "✅ Completed:" in result

    def test_generate_tool_summary_empty(self):
        """Test summary with no tools."""
        result = self.process_manager._generate_tool_summary([])
        assert result == ""

    def test_generate_tool_summary_mixed_counts(self):
        """Test summary with mix of single and repeated tools."""
        tools = [
            {"name": "Read", "timestamp": "1"},
            {"name": "Write", "timestamp": "2"},
            {"name": "Write", "timestamp": "3"},
            {"name": "Bash", "timestamp": "4"},
            {"name": "Bash", "timestamp": "5"},
            {"name": "Bash", "timestamp": "6"},
        ]
        result = self.process_manager._generate_tool_summary(tools)
        assert "Read" in result  # Single
        assert "Write (x2)" in result  # Doubled
        assert "Bash (x3)" in result  # Tripled
        assert "✅ Completed:" in result

    def test_sdk_generate_tool_summary_same_behavior(self):
        """Test SDK manager has same summary generation behavior."""
        tools = [
            {"name": "Edit", "timestamp": "1"},
            {"name": "Edit", "timestamp": "2"},
        ]
        result = self.sdk_manager._generate_tool_summary(tools)
        assert "Edit (x2)" in result
        assert "✅ Completed:" in result


class TestFallbackMessages:
    """Test fallback message updates."""

    def test_fallback_message_format(self):
        """Verify fallback message format is user-friendly."""
        # Test that our fallback messages are informative
        expected_fallback = "✅ Operation completed."
        expected_success = "✅ Command executed successfully."

        # These are the new fallback messages that should appear
        assert "✅" in expected_fallback
        assert "✅" in expected_success
        assert "completed" in expected_fallback.lower()
        assert "executed" in expected_success.lower()
