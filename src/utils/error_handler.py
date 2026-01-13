"""Error handling utilities for robust exception management."""

import asyncio
import functools
import logging
from typing import TypeVar, Callable, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Custom exception hierarchy
class BotError(Exception):
    """Base exception for bot-related errors."""
    pass

class ClaudeError(BotError):
    """Base exception for Claude integration errors."""
    pass

class TelegramHandlerError(BotError):
    """Exception for Telegram handler errors."""
    pass

class SubprocessCleanupError(ClaudeError):
    """Exception during subprocess cleanup."""
    pass

# Type variables for generic decorators
T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])

@dataclass
class RetryConfig:
    """Configuration for retry decorator."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    retry_exceptions: tuple = (Exception,)
    exclude_exceptions: tuple = (asyncio.CancelledError, KeyboardInterrupt)

def retry_async(config: Optional[RetryConfig] = None):
    """
    Retry decorator for async functions with exponential backoff.

    Args:
        config: RetryConfig instance or None for defaults

    Usage:
        @retry_async(RetryConfig(max_attempts=5))
        async def my_api_call():
            ...
    """
    if config is None:
        config = RetryConfig()

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            delay = config.initial_delay

            for attempt in range(config.max_attempts):
                try:
                    return await func(*args, **kwargs)
                except config.exclude_exceptions:
                    raise
                except config.retry_exceptions as e:
                    last_exception = e

                    if attempt == config.max_attempts - 1:
                        logger.error(
                            f"Final retry attempt failed for {func.__name__}",
                            extra={
                                "function": func.__name__,
                                "attempt": attempt + 1,
                                "max_attempts": config.max_attempts,
                                "error": str(e)
                            },
                            exc_info=True
                        )
                        raise

                    logger.warning(
                        f"Retry {attempt + 1}/{config.max_attempts} for {func.__name__}",
                        extra={
                            "function": func.__name__,
                            "attempt": attempt + 1,
                            "delay": delay,
                            "error": str(e)
                        }
                    )

                    await asyncio.sleep(delay)
                    delay = min(delay * config.exponential_base, config.max_delay)

            if last_exception:
                raise last_exception

        return wrapper
    return decorator

def log_exception(logger_instance: Optional[logging.Logger] = None):
    """
    Decorator to log exceptions with full traceback.

    Args:
        logger_instance: Custom logger or None to use module logger

    Usage:
        @log_exception()
        async def my_function():
            ...
    """
    _logger = logger_instance or logger

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                _logger.exception(
                    f"Exception in {func.__name__}",
                    extra={
                        "function": func.__name__,
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    }
                )
                raise

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                _logger.exception(
                    f"Exception in {func.__name__}",
                    extra={
                        "function": func.__name__,
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    }
                )
                raise

        # Return appropriate wrapper based on function type
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

async def safe_delete_message(message, logger_instance: Optional[logging.Logger] = None):
    """
    Safely delete a Telegram message with proper error handling.

    Args:
        message: Telegram message object
        logger_instance: Custom logger or None
    """
    _logger = logger_instance or logger
    try:
        await message.delete()
    except Exception as e:
        _logger.debug(
            f"Failed to delete message {message.message_id}",
            extra={
                "message_id": message.message_id,
                "error": str(e)
            }
        )

class ProcessCleanupManager:
    """Context manager for subprocess cleanup."""

    def __init__(self, process_tracker: dict, process_id: str, logger_instance: Optional[logging.Logger] = None):
        self.process_tracker = process_tracker
        self.process_id = process_id
        self.process = None
        self._logger = logger_instance or logger

    def set_process(self, process):
        """Register process for cleanup."""
        self.process = process
        self.process_tracker[self.process_id] = process

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure process cleanup on exit."""
        if self.process_id in self.process_tracker:
            del self.process_tracker[self.process_id]

        if self.process and self.process.returncode is None:
            try:
                self.process.terminate()
                try:
                    await asyncio.wait_for(self.process.wait(), timeout=5.0)
                except asyncio.TimeoutError:
                    self._logger.warning(f"Process {self.process_id} did not terminate, killing")
                    self.process.kill()
                    await self.process.wait()
            except Exception as e:
                self._logger.error(
                    f"Error cleaning up process {self.process_id}",
                    extra={"process_id": self.process_id, "error": str(e)},
                    exc_info=True
                )
