"""Message handlers for non-command inputs."""

import asyncio
from typing import Optional

import structlog
from telegram import Update
from telegram.ext import ContextTypes

from ...claude.exceptions import ClaudeToolValidationError
from ...config.settings import Settings
from ...security.audit import AuditLogger
from ...security.rate_limiter import RateLimiter
from ...security.validators import SecurityValidator

logger = structlog.get_logger()


def _get_tool_emoji(tool_name: str) -> str:
    """Get appropriate emoji for tool type."""
    tool_emojis = {
        "Read": "📖",
        "Write": "✍️",
        "Edit": "✏️",
        "Bash": "💻",
        "Glob": "🔍",
        "Grep": "🔎",
        "LS": "📂",
        "Task": "🎯",
        "MultiEdit": "📝",
        "NotebookEdit": "📓",
        "WebFetch": "🌐",
        "TodoWrite": "📋",
        "WebSearch": "🔎",
    }
    return tool_emojis.get(tool_name, "🔧")


def _safe_truncate_markdown(text: str, max_len: int, add_ellipsis: bool = True) -> str:
    """Truncate text safely without breaking markdown entities.

    Counts backticks, asterisks, underscores and closes unclosed ones.
    KISS approach - handles common cases, not nested/complex markdown.
    """
    if not text or len(text) <= max_len:
        return text

    truncated = text[:max_len]

    # Count markdown characters that need pairing
    backticks = truncated.count('`')
    # Asterisks (for bold/italic) - handle pairs of ** as single logical entity?
    # Telegram markdown is tricky. simple *bold* or *italic* (MarkdownV2 uses * for bold, _ for italic)
    # Actually Telegram MarkdownV2: *bold*, _italic_, __underline__, ~strikethrough~, ||spoiler||, `code`
    # We should count each type.

    # Simple count check for odd numbers
    if backticks % 2 != 0:
        truncated += '`'

    # Check for unclosed *
    if truncated.count('*') % 2 != 0:
        truncated += '*'

    # Check for unclosed _
    if truncated.count('_') % 2 != 0:
        truncated += '_'

    # Add ellipsis if requested
    if add_ellipsis:
        truncated += "..."

    return truncated


def _format_tool_params(tool_name: str, params: dict) -> str:
    """Format important parameters for tool preview."""
    if not params:
        return ""

    # Different formatting for different tools
    if tool_name == "Read":
        file_path = params.get("file_path", "")
        return f"`{file_path}`"

    elif tool_name in ["Write", "Edit"]:
        file_path = params.get("file_path", "")
        content_preview = params.get("content", params.get("new_string", ""))
        if content_preview:
            preview = _safe_truncate_markdown(content_preview, 50)
            return f"`{file_path}` ← {preview}"
        return f"`{file_path}`"

    elif tool_name == "Bash":
        command = params.get("command", "")
        # Escape internal backticks to prevent markdown conflicts
        command_safe = command.replace('`', "'")
        if len(command_safe) > 60:
            return f"`{command_safe[:60]}...`"
        return f"`{command_safe}`"

    elif tool_name in ["Glob", "Grep"]:
        pattern = params.get("pattern", "")
        path = params.get("path", "")
        if path:
            return f"Pattern: `{pattern}` in `{path}`"
        return f"Pattern: `{pattern}`"

    elif tool_name == "Task":
        prompt = params.get("prompt", "")
        subagent_type = params.get("subagent_type", "")
        if subagent_type:
            return f"{subagent_type}: {_safe_truncate_markdown(prompt, 40)}"
        return _safe_truncate_markdown(prompt, 50)

    # Default: show first few params
    preview_params = []
    for k, v in list(params.items())[:2]:
        if isinstance(v, str) and len(v) < 30:
            preview_params.append(f"{k}={v}")
    return ", ".join(preview_params) if preview_params else ""


async def _format_progress_update(update_obj, tracker=None) -> Optional[str]:
    """Format progress updates with enhanced context and visual indicators."""
    # Tool execution started - show which tools are being called
    if update_obj.type == "assistant" and update_obj.tool_calls:
        tool_names = update_obj.get_tool_names()
        if tool_names:
            # Format tool calls with parameters preview
            tool_list = []
            for i, tool_call in enumerate(update_obj.tool_calls):
                tool_name = tool_call.get("name", "Unknown")
                tool_id = tool_call.get("id", "")
                tool_input = tool_call.get("input", {})

                # Track tool start if tracker available
                if tracker and tool_id:
                    session_id = (
                        update_obj.session_context.get("session_id")
                        if update_obj.session_context
                        else "unknown"
                    )
                    tracker.start_tool(tool_name, tool_id, tool_input, session_id)

                # Get emoji for tool type
                tool_emoji = _get_tool_emoji(tool_name)

                # Preview important parameters
                param_preview = _format_tool_params(tool_name, tool_input)

                if param_preview:
                    tool_list.append(f"{tool_emoji} **{tool_name}**\n  ↳ {param_preview}")
                else:
                    tool_list.append(f"{tool_emoji} **{tool_name}**")

            return f"🔧 **Executing tools:**\n\n" + "\n".join(tool_list)

    if update_obj.type == "tool_result":
        # Show tool completion status
        tool_id = update_obj.metadata.get("tool_use_id") if update_obj.metadata else None
        tool_name = "Tool"

        # Try to get tool name from tracker
        if tracker and tool_id:
            execution = tracker.get_execution(tool_id)
            if execution:
                tool_name = execution.tool_name

                # Mark as completed or failed
                if update_obj.is_error():
                    tracker.fail_tool(tool_id, update_obj.get_error_message() or "Unknown error")
                else:
                    tracker.complete_tool(tool_id, update_obj.content)
            else:
                # Fallback to metadata
                tool_name = update_obj.metadata.get("tool_name", "Tool")
        else:
            # Fallback to metadata
            if update_obj.metadata:
                tool_name = update_obj.metadata.get("tool_name", "Tool")

        # Get emoji
        tool_emoji = _get_tool_emoji(tool_name)

        if update_obj.is_error():
            return f"❌ **{tool_emoji} {tool_name} failed**\n\n_{update_obj.get_error_message()}_"
        else:
            execution_time = ""
            if update_obj.metadata and update_obj.metadata.get("execution_time_ms"):
                time_ms = update_obj.metadata["execution_time_ms"]
                execution_time = f" ({time_ms}ms)"
            return f"✅ **{tool_emoji} {tool_name} completed**{execution_time}"

    elif update_obj.type == "progress":
        # Handle progress updates
        progress_text = f"🔄 **{update_obj.content or 'Working...'}**"

        percentage = update_obj.get_progress_percentage()
        if percentage is not None:
            # Create a simple progress bar
            filled = int(percentage / 10)  # 0-10 scale
            bar = "█" * filled + "░" * (10 - filled)
            progress_text += f"\n\n`{bar}` {percentage}%"

        if update_obj.progress:
            step = update_obj.progress.get("step")
            total_steps = update_obj.progress.get("total_steps")
            if step and total_steps:
                progress_text += f"\n\nStep {step} of {total_steps}"

        return progress_text

    elif update_obj.type == "error":
        # Handle error messages
        return f"❌ **Error**\n\n_{update_obj.get_error_message()}_"

    elif update_obj.type == "assistant" and update_obj.tool_calls:
        # Show when tools are being called
        tool_names = update_obj.get_tool_names()
        if tool_names:
            tools_text = ", ".join(tool_names)
            return f"🔧 **Using tools:** {tools_text}"

    elif update_obj.type == "assistant" and update_obj.content:
        # Regular content updates with preview
        content_preview = _safe_truncate_markdown(update_obj.content, 150)
        # Don't wrap in underscores - can conflict with content's markdown
        return f"🤖 **Claude is working...**\n\n{content_preview}"

    elif update_obj.type == "system":
        # System initialization or other system messages
        if update_obj.metadata and update_obj.metadata.get("subtype") == "init":
            tools_count = len(update_obj.metadata.get("tools", []))
            model = update_obj.metadata.get("model", "Claude")
            return f"🚀 **Starting {model}** with {tools_count} tools available"

    return None


def _format_error_message(error_str: str) -> str:
    """Format error messages for user-friendly display."""
    if "usage limit reached" in error_str.lower():
        # Usage limit error - already user-friendly from integration.py
        return error_str
    elif "tool not allowed" in error_str.lower():
        # Tool validation error - already handled in facade.py
        return error_str
    elif "no conversation found" in error_str.lower():
        return (
            f"🔄 **Session Not Found**\n\n"
            f"The Claude session could not be found or has expired.\n\n"
            f"**What you can do:**\n"
            f"• Use `/new` to start a fresh session\n"
            f"• Try your request again\n"
            f"• Use `/status` to check your current session"
        )
    elif "rate limit" in error_str.lower():
        return (
            f"⏱️ **Rate Limit Reached**\n\n"
            f"Too many requests in a short time period.\n\n"
            f"**What you can do:**\n"
            f"• Wait a moment before trying again\n"
            f"• Use simpler requests\n"
            f"• Check your current usage with `/status`"
        )
    elif "timeout" in error_str.lower():
        return (
            f"⏰ **Request Timeout**\n\n"
            f"Your request took too long to process and timed out.\n\n"
            f"**What you can do:**\n"
            f"• Try breaking down your request into smaller parts\n"
            f"• Use simpler commands\n"
            f"• Try again in a moment"
        )
    else:
        # Generic error handling
        return (
            f"❌ **Claude Code Error**\n\n"
            f"Failed to process your request: {error_str}\n\n"
            f"Please try again or contact the administrator if the problem persists."
        )


async def handle_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle regular text messages as Claude prompts."""
    user_id = update.effective_user.id
    message_text = update.message.text
    settings: Settings = context.bot_data["settings"]

    # Get services
    rate_limiter: Optional[RateLimiter] = context.bot_data.get("rate_limiter")
    audit_logger: Optional[AuditLogger] = context.bot_data.get("audit_logger")

    # Check if this is a reply to a pending question
    pending_question = context.user_data.get("pending_question")
    awaiting_custom = context.user_data.get("awaiting_custom_answer", False)
    
    if pending_question or awaiting_custom:
        # Clear the pending state
        context.user_data["pending_question"] = None
        context.user_data["awaiting_custom_answer"] = False
        
        logger.info(
            "Processing reply to pending question",
            user_id=user_id,
            message=message_text[:50],
            had_pending=bool(pending_question),
            was_awaiting=awaiting_custom
        )
        
        # Prepend context to indicate this is an answer
        message_text = f"Trả lời cho câu hỏi: {message_text}"

    logger.info(
        "Processing text message", user_id=user_id, message_length=len(message_text)
    )

    try:
        # Check rate limit with estimated cost for text processing
        estimated_cost = _estimate_text_processing_cost(message_text)

        if rate_limiter:
            allowed, limit_message = await rate_limiter.check_rate_limit(
                user_id, estimated_cost
            )
            if not allowed:
                await update.message.reply_text(f"⏱️ {limit_message}")
                return

        # Send typing indicator
        await update.message.chat.send_action("typing")

        # Create progress message
        progress_msg = await update.message.reply_text(
            "🤔 Processing your request...",
            reply_to_message_id=update.message.message_id,
        )

        # Get Claude integration and storage from context
        claude_integration = context.bot_data.get("claude_integration")
        storage = context.bot_data.get("storage")

        if not claude_integration:
            await update.message.reply_text(
                "❌ **Claude integration not available**\n\n"
                "The Claude Code integration is not properly configured. "
                "Please contact the administrator.",
                parse_mode="Markdown",
            )
            return

        # Get current directory
        current_dir = context.user_data.get(
            "current_directory", settings.approved_directory
        )

        # Get existing session ID
        session_id = context.user_data.get("claude_session_id")

        # Initialize tool tracker for this request
        from ..features.tool_execution_tracker import ToolExecutionTracker

        tool_tracker = ToolExecutionTracker()

        # Track last progress text to avoid duplicate edits
        last_progress_text = None

        # Enhanced stream updates handler with progress tracking
        async def stream_handler(update_obj):
            nonlocal last_progress_text
            try:
                progress_text = await _format_progress_update(update_obj, tracker=tool_tracker)
                if progress_text and progress_text != last_progress_text:
                    await progress_msg.edit_text(progress_text, parse_mode="Markdown")
                    last_progress_text = progress_text
            except Exception as e:
                logger.warning("Failed to update progress message", error=str(e))

        # Run Claude command
        try:
            claude_response = await claude_integration.run_command(
                prompt=message_text,
                working_directory=current_dir,
                user_id=user_id,
                session_id=session_id,
                on_stream=stream_handler,
            )

            # Update session ID
            context.user_data["claude_session_id"] = claude_response.session_id

            # Check if Claude changed the working directory and update our tracking
            _update_working_directory_from_claude_response(
                claude_response, context, settings, user_id
            )

            # Log interaction to storage
            if storage:
                try:
                    await storage.save_claude_interaction(
                        user_id=user_id,
                        session_id=claude_response.session_id,
                        prompt=message_text,
                        response=claude_response,
                        ip_address=None,  # Telegram doesn't provide IP
                    )
                except Exception as e:
                    logger.warning("Failed to log interaction to storage", error=str(e))

            # Format response
            from ..utils.formatting import ResponseFormatter, parse_claude_question, format_question_with_options

            formatter = ResponseFormatter(settings)
            
            # Check if Claude is asking a question with options
            question_data = parse_claude_question(claude_response.content)
            if question_data:
                # Store question data for callback handler
                context.user_data["pending_question"] = question_data
                
                # Clear pending custom answer flag
                context.user_data["awaiting_custom_answer"] = False
                
                # Format as question with inline buttons
                question_message = format_question_with_options(question_data)
                formatted_messages = [question_message]
                
                logger.info(
                    "Detected Claude question with options",
                    user_id=user_id,
                    question=question_data.get('question', '')[:50],
                    num_options=len(question_data.get('options', []))
                )
            else:
                formatted_messages = formatter.format_claude_response(
                    claude_response.content
                )

        except ClaudeToolValidationError as e:
            # Tool validation error with detailed instructions
            logger.error(
                "Tool validation error",
                error=str(e),
                user_id=user_id,
                blocked_tools=e.blocked_tools,
            )
            # Error message already formatted, create FormattedMessage
            from ..utils.formatting import FormattedMessage

            formatted_messages = [FormattedMessage(str(e), parse_mode="Markdown")]
        except Exception as e:
            logger.error("Claude integration failed", error=str(e), user_id=user_id)
            # Format error and create FormattedMessage
            from ..utils.formatting import FormattedMessage

            formatted_messages = [
                FormattedMessage(_format_error_message(str(e)), parse_mode="Markdown")
            ]

        # Delete progress message
        await progress_msg.delete()

        # Send formatted responses (may be multiple messages)
        for i, message in enumerate(formatted_messages):
            try:
                await update.message.reply_text(
                    message.text,
                    parse_mode=message.parse_mode,
                    reply_markup=message.reply_markup,
                    reply_to_message_id=update.message.message_id if i == 0 else None,
                )

                # Delay between messages to avoid Telegram rate limits
                if i < len(formatted_messages) - 1:
                    await asyncio.sleep(1.5)

            except Exception as e:
                logger.error(
                    "Failed to send response message", error=str(e), message_index=i
                )
                # Try to send error message
                await update.message.reply_text(
                    "❌ Failed to send response. Please try again.",
                    reply_to_message_id=update.message.message_id if i == 0 else None,
                )

        # Update session info
        context.user_data["last_message"] = update.message.text

        # Add conversation enhancements if available
        features = context.bot_data.get("features")
        conversation_enhancer = (
            features.get_conversation_enhancer() if features else None
        )

        if conversation_enhancer and claude_response:
            try:
                # Update conversation context with full response object
                conversation_enhancer.update_context(user_id, claude_response)
                conversation_context = conversation_enhancer.get_or_create_context(user_id)

                # Check if we should show follow-up suggestions
                if conversation_enhancer.should_show_suggestions(claude_response):
                    # Generate follow-up suggestions
                    suggestions = conversation_enhancer.generate_follow_up_suggestions(
                        claude_response,
                        conversation_context,
                    )

                    if suggestions:
                        # Create keyboard with suggestions
                        suggestion_keyboard = (
                            conversation_enhancer.create_follow_up_keyboard(suggestions)
                        )

                        # Send follow-up suggestions
                        await update.message.reply_text(
                            "💡 **What would you like to do next?**",
                            parse_mode="Markdown",
                            reply_markup=suggestion_keyboard,
                        )

            except Exception as e:
                logger.warning(
                    "Conversation enhancement failed", error=str(e), user_id=user_id
                )

        # Log successful message processing
        if audit_logger:
            await audit_logger.log_command(
                user_id=user_id,
                command="text_message",
                args=[update.message.text[:100]],  # First 100 chars
                success=True,
            )

        logger.info("Text message processed successfully", user_id=user_id)

    except Exception as e:
        # Clean up progress message if it exists
        try:
            await progress_msg.delete()
        except Exception as delete_err:
            logger.debug(
                "Failed to delete progress message",
                extra={"error": str(delete_err), "message_id": getattr(progress_msg, 'message_id', None)}
            )

        error_msg = f"❌ **Error processing message**\n\n{str(e)}"
        await update.message.reply_text(error_msg, parse_mode="Markdown")

        # Log failed processing
        if audit_logger:
            await audit_logger.log_command(
                user_id=user_id,
                command="text_message",
                args=[update.message.text[:100]],
                success=False,
            )

        logger.exception(
            "Error processing text message",
            extra={"user_id": user_id, "error_type": type(e).__name__}
        )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle file uploads."""
    user_id = update.effective_user.id
    document = update.message.document
    settings: Settings = context.bot_data["settings"]

    # Get services
    security_validator: Optional[SecurityValidator] = context.bot_data.get(
        "security_validator"
    )
    audit_logger: Optional[AuditLogger] = context.bot_data.get("audit_logger")
    rate_limiter: Optional[RateLimiter] = context.bot_data.get("rate_limiter")

    logger.info(
        "Processing document upload",
        user_id=user_id,
        filename=document.file_name,
        file_size=document.file_size,
    )

    try:
        # Validate filename using security validator
        if security_validator:
            valid, error = security_validator.validate_filename(document.file_name)
            if not valid:
                await update.message.reply_text(
                    f"❌ **File Upload Rejected**\n\n{error}"
                )

                # Log security violation
                if audit_logger:
                    await audit_logger.log_security_violation(
                        user_id=user_id,
                        violation_type="invalid_file_upload",
                        details=f"Filename: {document.file_name}, Error: {error}",
                        severity="medium",
                    )
                return

        # Check file size limits
        max_size = 10 * 1024 * 1024  # 10MB
        if document.file_size > max_size:
            await update.message.reply_text(
                f"❌ **File Too Large**\n\n"
                f"Maximum file size: {max_size // 1024 // 1024}MB\n"
                f"Your file: {document.file_size / 1024 / 1024:.1f}MB"
            )
            return

        # Check rate limit for file processing
        file_cost = _estimate_file_processing_cost(document.file_size)
        if rate_limiter:
            allowed, limit_message = await rate_limiter.check_rate_limit(
                user_id, file_cost
            )
            if not allowed:
                await update.message.reply_text(f"⏱️ {limit_message}")
                return

        # Send processing indicator
        await update.message.chat.send_action("upload_document")

        progress_msg = await update.message.reply_text(
            f"📄 Processing file: `{document.file_name}`...", parse_mode="Markdown"
        )

        # Check if enhanced file handler is available
        features = context.bot_data.get("features")
        file_handler = features.get_file_handler() if features else None

        if file_handler:
            # Use enhanced file handler
            try:
                processed_file = await file_handler.handle_document_upload(
                    document,
                    user_id,
                    update.message.caption or "Please review this file:",
                )
                prompt = processed_file.prompt

                # Update progress message with file type info
                await progress_msg.edit_text(
                    f"📄 Processing {processed_file.type} file: `{document.file_name}`...",
                    parse_mode="Markdown",
                )

            except Exception as e:
                logger.warning(
                    "Enhanced file handler failed, falling back to basic handler",
                    error=str(e),
                )
                file_handler = None  # Fall back to basic handling

        if not file_handler:
            # Fall back to basic file handling
            file = await document.get_file()
            file_bytes = await file.download_as_bytearray()

            # Try to decode as text
            try:
                content = file_bytes.decode("utf-8")

                # Check content length
                max_content_length = 50000  # 50KB of text
                if len(content) > max_content_length:
                    content = (
                        content[:max_content_length]
                        + "\n... (file truncated for processing)"
                    )

                # Create prompt with file content
                caption = update.message.caption or "Please review this file:"
                prompt = f"{caption}\n\n**File:** `{document.file_name}`\n\n```\n{content}\n```"

            except UnicodeDecodeError:
                await progress_msg.edit_text(
                    "❌ **File Format Not Supported**\n\n"
                    "File must be text-based and UTF-8 encoded.\n\n"
                    "**Supported formats:**\n"
                    "• Source code files (.py, .js, .ts, etc.)\n"
                    "• Text files (.txt, .md)\n"
                    "• Configuration files (.json, .yaml, .toml)\n"
                    "• Documentation files"
                )
                return

        # Delete progress message
        await progress_msg.delete()

        # Create a new progress message for Claude processing
        claude_progress_msg = await update.message.reply_text(
            "🤖 Processing file with Claude...", parse_mode="Markdown"
        )

        # Get Claude integration from context
        claude_integration = context.bot_data.get("claude_integration")

        if not claude_integration:
            await claude_progress_msg.edit_text(
                "❌ **Claude integration not available**\n\n"
                "The Claude Code integration is not properly configured.",
                parse_mode="Markdown",
            )
            return

        # Get current directory and session
        current_dir = context.user_data.get(
            "current_directory", settings.approved_directory
        )
        session_id = context.user_data.get("claude_session_id")

        # Process with Claude
        try:
            claude_response = await claude_integration.run_command(
                prompt=prompt,
                working_directory=current_dir,
                user_id=user_id,
                session_id=session_id,
            )

            # Update session ID
            context.user_data["claude_session_id"] = claude_response.session_id

            # Check if Claude changed the working directory and update our tracking
            _update_working_directory_from_claude_response(
                claude_response, context, settings, user_id
            )

            # Format and send response
            from ..utils.formatting import ResponseFormatter

            formatter = ResponseFormatter(settings)
            formatted_messages = formatter.format_claude_response(
                claude_response.content
            )

            # Delete progress message
            await claude_progress_msg.delete()

            # Send responses
            for i, message in enumerate(formatted_messages):
                await update.message.reply_text(
                    message.text,
                    parse_mode=message.parse_mode,
                    reply_markup=message.reply_markup,
                    reply_to_message_id=(update.message.message_id if i == 0 else None),
                )

                if i < len(formatted_messages) - 1:
                    await asyncio.sleep(1.5)

        except Exception as e:
            await claude_progress_msg.edit_text(
                _format_error_message(str(e)), parse_mode="Markdown"
            )
            logger.error("Claude file processing failed", error=str(e), user_id=user_id)

        # Log successful file processing
        if audit_logger:
            await audit_logger.log_file_access(
                user_id=user_id,
                file_path=document.file_name,
                action="upload_processed",
                success=True,
                file_size=document.file_size,
            )

    except Exception as e:
        try:
            await progress_msg.delete()
        except Exception as delete_err:
            logger.debug(
                "Failed to delete progress message",
                extra={"error": str(delete_err), "message_id": getattr(progress_msg, 'message_id', None)}
            )

        logger.exception(
            "Error processing file upload",
            extra={"user_id": user_id, "error_type": type(e).__name__, "filename": document.file_name}
        )

        error_msg = f"❌ **Error processing file**\n\n{str(e)}"
        await update.message.reply_text(error_msg, parse_mode="Markdown")

        # Log failed file processing
        if audit_logger:
            await audit_logger.log_file_access(
                user_id=user_id,
                file_path=document.file_name,
                action="upload_failed",
                success=False,
                file_size=document.file_size,
            )

        logger.error("Error processing document", error=str(e), user_id=user_id)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo uploads."""
    user_id = update.effective_user.id
    settings: Settings = context.bot_data["settings"]

    # Check if enhanced image handler is available
    features = context.bot_data.get("features")
    image_handler = features.get_image_handler() if features else None

    if image_handler:
        try:
            # Send processing indicator
            progress_msg = await update.message.reply_text(
                "📸 Processing image...", parse_mode="Markdown"
            )

            # Get the largest photo size
            photo = update.message.photo[-1]

            # Process image with enhanced handler
            processed_image = await image_handler.process_image(
                photo, update.message.caption
            )

            # Delete progress message
            await progress_msg.delete()

            # Create Claude progress message
            claude_progress_msg = await update.message.reply_text(
                "🤖 Analyzing image with Claude...", parse_mode="Markdown"
            )

            # Get Claude integration
            claude_integration = context.bot_data.get("claude_integration")

            if not claude_integration:
                await claude_progress_msg.edit_text(
                    "❌ **Claude integration not available**\n\n"
                    "The Claude Code integration is not properly configured.",
                    parse_mode="Markdown",
                )
                return

            # Get current directory and session
            current_dir = context.user_data.get(
                "current_directory", settings.approved_directory
            )
            session_id = context.user_data.get("claude_session_id")

            # Process with Claude
            try:
                claude_response = await claude_integration.run_command(
                    prompt=processed_image.prompt,
                    working_directory=current_dir,
                    user_id=user_id,
                    session_id=session_id,
                )

                # Update session ID
                context.user_data["claude_session_id"] = claude_response.session_id

                # Format and send response
                from ..utils.formatting import ResponseFormatter

                formatter = ResponseFormatter(settings)
                formatted_messages = formatter.format_claude_response(
                    claude_response.content
                )

                # Delete progress message
                await claude_progress_msg.delete()

                # Send responses
                for i, message in enumerate(formatted_messages):
                    await update.message.reply_text(
                        message.text,
                        parse_mode=message.parse_mode,
                        reply_markup=message.reply_markup,
                        reply_to_message_id=(
                            update.message.message_id if i == 0 else None
                        ),
                    )

                    if i < len(formatted_messages) - 1:
                        await asyncio.sleep(1.5)

            except Exception as e:
                await claude_progress_msg.edit_text(
                    _format_error_message(str(e)), parse_mode="Markdown"
                )
                logger.error(
                    "Claude image processing failed", error=str(e), user_id=user_id
                )

        except Exception as e:
            logger.error("Image processing failed", error=str(e), user_id=user_id)
            await update.message.reply_text(
                f"❌ **Error processing image**\n\n{str(e)}", parse_mode="Markdown"
            )
    else:
        # Fall back to unsupported message
        await update.message.reply_text(
            "📸 **Photo Upload**\n\n"
            "Photo processing is not yet supported.\n\n"
            "**Currently supported:**\n"
            "• Text files (.py, .js, .md, etc.)\n"
            "• Configuration files\n"
            "• Documentation files\n\n"
            "**Coming soon:**\n"
            "• Image analysis\n"
            "• Screenshot processing\n"
            "• Diagram interpretation"
        )


def _estimate_text_processing_cost(text: str) -> float:
    """Estimate cost for processing text message."""
    # Base cost
    base_cost = 0.001

    # Additional cost based on length
    length_cost = len(text) * 0.00001

    # Additional cost for complex requests
    complex_keywords = [
        "analyze",
        "generate",
        "create",
        "build",
        "implement",
        "refactor",
        "optimize",
        "debug",
        "explain",
        "document",
    ]

    text_lower = text.lower()
    complexity_multiplier = 1.0

    for keyword in complex_keywords:
        if keyword in text_lower:
            complexity_multiplier += 0.5

    return (base_cost + length_cost) * min(complexity_multiplier, 3.0)


def _estimate_file_processing_cost(file_size: int) -> float:
    """Estimate cost for processing uploaded file."""
    # Base cost for file handling
    base_cost = 0.005

    # Additional cost based on file size (per KB)
    size_cost = (file_size / 1024) * 0.0001

    return base_cost + size_cost


async def _generate_placeholder_response(
    message_text: str, context: ContextTypes.DEFAULT_TYPE
) -> dict:
    """Generate placeholder response until Claude integration is implemented."""
    settings: Settings = context.bot_data["settings"]
    current_dir = getattr(
        context.user_data, "current_directory", settings.approved_directory
    )
    relative_path = current_dir.relative_to(settings.approved_directory)

    # Analyze the message for intent
    message_lower = message_text.lower()

    if any(
        word in message_lower for word in ["list", "show", "see", "directory", "files"]
    ):
        response_text = (
            f"🤖 **Claude Code Response** _(Placeholder)_\n\n"
            f"I understand you want to see files. Try using the `/ls` command to list files "
            f"in your current directory (`{relative_path}/`).\n\n"
            f"**Available commands:**\n"
            f"• `/ls` - List files\n"
            f"• `/cd <dir>` - Change directory\n"
            f"• `/projects` - Show projects\n\n"
            f"_Note: Full Claude Code integration will be available in the next phase._"
        )

    elif any(word in message_lower for word in ["create", "generate", "make", "build"]):
        response_text = (
            f"🤖 **Claude Code Response** _(Placeholder)_\n\n"
            f"I understand you want to create something! Once the Claude Code integration "
            f"is complete, I'll be able to:\n\n"
            f"• Generate code files\n"
            f"• Create project structures\n"
            f"• Write documentation\n"
            f"• Build complete applications\n\n"
            f"**Current directory:** `{relative_path}/`\n\n"
            f"_Full functionality coming soon!_"
        )

    elif any(word in message_lower for word in ["help", "how", "what", "explain"]):
        response_text = (
            f"🤖 **Claude Code Response** _(Placeholder)_\n\n"
            f"I'm here to help! Try using `/help` for available commands.\n\n"
            f"**What I can do now:**\n"
            f"• Navigate directories (`/cd`, `/ls`, `/pwd`)\n"
            f"• Show projects (`/projects`)\n"
            f"• Manage sessions (`/new`, `/status`)\n\n"
            f"**Coming soon:**\n"
            f"• Full Claude Code integration\n"
            f"• Code generation and editing\n"
            f"• File operations\n"
            f"• Advanced programming assistance"
        )

    else:
        response_text = (
            f"🤖 **Claude Code Response** _(Placeholder)_\n\n"
            f"I received your message: \"{message_text[:100]}{'...' if len(message_text) > 100 else ''}\"\n\n"
            f"**Current Status:**\n"
            f"• Directory: `{relative_path}/`\n"
            f"• Bot core: ✅ Active\n"
            f"• Claude integration: 🔄 Coming soon\n\n"
            f"Once Claude Code integration is complete, I'll be able to process your "
            f"requests fully and help with coding tasks!\n\n"
            f"For now, try the available commands like `/ls`, `/cd`, and `/help`."
        )

    return {"text": response_text, "parse_mode": "Markdown"}


def _update_working_directory_from_claude_response(
    claude_response, context, settings, user_id
):
    """Update the working directory based on Claude's response content."""
    import re
    from pathlib import Path

    # Look for directory changes in Claude's response
    # This searches for common patterns that indicate directory changes
    patterns = [
        r"(?:^|\n).*?cd\s+([^\s\n]+)",  # cd command
        r"(?:^|\n).*?Changed directory to:?\s*([^\s\n]+)",  # explicit directory change
        r"(?:^|\n).*?Current directory:?\s*([^\s\n]+)",  # current directory indication
        r"(?:^|\n).*?Working directory:?\s*([^\s\n]+)",  # working directory indication
    ]

    content = claude_response.content.lower()
    current_dir = context.user_data.get(
        "current_directory", settings.approved_directory
    )

    for pattern in patterns:
        matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            try:
                # Clean up the path
                new_path = match.strip().strip("\"'`")

                # Handle relative paths
                if new_path.startswith("./") or new_path.startswith("../"):
                    new_path = (current_dir / new_path).resolve()
                elif not new_path.startswith("/"):
                    # Relative path without ./
                    new_path = (current_dir / new_path).resolve()
                else:
                    # Absolute path
                    new_path = Path(new_path).resolve()

                # Validate that the new path is within the approved directory
                if (
                    new_path.is_relative_to(settings.approved_directory)
                    and new_path.exists()
                ):
                    context.user_data["current_directory"] = new_path
                    logger.info(
                        "Updated working directory from Claude response",
                        old_dir=str(current_dir),
                        new_dir=str(new_path),
                        user_id=user_id,
                    )
                    return  # Take the first valid match

            except (ValueError, OSError) as e:
                # Invalid path, skip this match
                logger.debug(
                    "Invalid path in Claude response", path=match, error=str(e)
                )
                continue
