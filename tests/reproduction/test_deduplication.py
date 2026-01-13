import pytest
from unittest.mock import AsyncMock, Mock, patch, call
from telegram import Update, Message, Chat
from telegram.ext import ContextTypes

# Mock the module import to avoid dependencies on real infrastructure
import sys
from types import SimpleNamespace

# Create mocks for dependencies
mock_tool_tracker_cls = Mock()
mock_tool_tracker = Mock()
mock_tool_tracker_cls.return_value = mock_tool_tracker

# Mock imports
with patch.dict(sys.modules, {
    "structlog": Mock(get_logger=Mock(return_value=Mock())),
    "telegram": Mock(Update=Update, Message=Message, Chat=Chat),
    "telegram.ext": Mock(ContextTypes=ContextTypes),
    "..features.tool_execution_tracker": Mock(ToolExecutionTracker=mock_tool_tracker_cls),
    "..claude.exceptions": Mock(ClaudeToolValidationError=Exception),
    "..config.settings": Mock(),
    "..security.audit": Mock(),
    "..security.rate_limiter": Mock(),
    "..security.validators": Mock(),
    "..utils.formatting": Mock(),
}):
    # Import the function to test
    # We need to use relative imports matching the original file structure
    # But since we're running this as a standalone test script, we'll need to mock the imports differently
    # or just copy the relevant code parts for unit testing.

    # Let's import the file directly
    from src.bot.handlers.message import handle_text_message, _format_progress_update

@pytest.mark.asyncio
async def test_stream_handler_deduplication():
    """Test that stream_handler avoids sending duplicate updates."""

    # Setup mocks
    update = Mock(spec=Update)
    update.effective_user.id = 12345
    update.message = Mock(spec=Message)
    update.message.text = "test prompt"
    update.message.chat = Mock(spec=Chat)
    update.message.chat.send_action = AsyncMock()
    update.message.reply_text = AsyncMock()
    update.message.message_id = 100

    # Mock progress message
    progress_msg = Mock()
    progress_msg.edit_text = AsyncMock()
    progress_msg.delete = AsyncMock()
    update.message.reply_text.return_value = progress_msg

    # Setup context
    context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot_data = {
        "settings": Mock(approved_directory="/tmp"),
        "claude_integration": Mock(),
        "storage": Mock(),
        "audit_logger": Mock()
    }
    context.user_data = {}

    # Mock rate limiter check to allow request
    mock_rate_limiter = AsyncMock()
    mock_rate_limiter.check_rate_limit.return_value = (True, "")
    context.bot_data["rate_limiter"] = mock_rate_limiter

    # Mock Claude integration run_command to simulate streaming
    # We'll intercept the on_stream callback
    captured_stream_handler = None

    async def mock_run_command(*args, **kwargs):
        nonlocal captured_stream_handler
        captured_stream_handler = kwargs.get("on_stream")

        # Return a mock response
        return Mock(session_id="session_123", content="Response content")

    context.bot_data["claude_integration"].run_command = AsyncMock(side_effect=mock_run_command)

    # Mock _format_progress_update to return controlled values
    with patch("src.bot.handlers.message._format_progress_update", new_callable=AsyncMock) as mock_format:
        # Start the handler
        await handle_text_message(update, context)

        assert captured_stream_handler is not None

        # Test Case 1: First update should be sent
        mock_format.return_value = "Update 1"
        await captured_stream_handler(Mock())
        progress_msg.edit_text.assert_called_with("Update 1", parse_mode="Markdown")
        progress_msg.edit_text.reset_mock()

        # Test Case 2: Same update should NOT be sent (deduplication)
        mock_format.return_value = "Update 1"
        await captured_stream_handler(Mock())
        progress_msg.edit_text.assert_not_called()

        # Test Case 3: Different update should be sent
        mock_format.return_value = "Update 2"
        await captured_stream_handler(Mock())
        progress_msg.edit_text.assert_called_with("Update 2", parse_mode="Markdown")
        progress_msg.edit_text.reset_mock()

        # Test Case 4: Back to original update should be sent
        mock_format.return_value = "Update 1"
        await captured_stream_handler(Mock())
        progress_msg.edit_text.assert_called_with("Update 1", parse_mode="Markdown")

@pytest.mark.asyncio
async def test_stream_handler_error_handling():
    """Test that stream_handler handles errors gracefully."""

    # Setup mocks similar to above
    update = Mock(spec=Update)
    update.effective_user.id = 12345
    update.message = Mock(spec=Message)
    update.message.text = "test prompt"
    update.message.reply_text = AsyncMock()
    update.message.chat.send_action = AsyncMock()

    progress_msg = Mock()
    progress_msg.edit_text = AsyncMock()
    progress_msg.delete = AsyncMock()
    update.message.reply_text.return_value = progress_msg

    context = Mock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot_data = {
        "settings": Mock(approved_directory="/tmp"),
        "claude_integration": Mock(),
    }
    context.user_data = {}

    # Capture the stream handler
    captured_stream_handler = None

    async def mock_run_command(*args, **kwargs):
        nonlocal captured_stream_handler
        captured_stream_handler = kwargs.get("on_stream")
        return Mock(session_id="session_123", content="Response")

    context.bot_data["claude_integration"].run_command = AsyncMock(side_effect=mock_run_command)

    # Execute
    await handle_text_message(update, context)

    # Test error handling
    with patch("src.bot.handlers.message._format_progress_update", side_effect=Exception("Format error")):
        # Should not raise exception
        await captured_stream_handler(Mock())
        progress_msg.edit_text.assert_not_called()
