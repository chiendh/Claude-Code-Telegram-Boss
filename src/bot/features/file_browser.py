"""Interactive file browser with inline keyboards.

Provides a UI for browsing files and directories via Telegram inline buttons.
"""

import datetime
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

import structlog
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logger = structlog.get_logger()


@dataclass
class FileNode:
    """Represents a file or directory node."""

    name: str
    path: Path
    is_dir: bool
    size: Optional[int] = None
    modified_time: Optional[float] = None

    @property
    def emoji(self) -> str:
        """Get appropriate emoji for file type."""
        if self.is_dir:
            return "📁"

        # File type emojis
        ext = self.path.suffix.lower()
        emoji_map = {
            ".py": "🐍",
            ".js": "📜",
            ".ts": "📘",
            ".tsx": "⚛️",
            ".jsx": "⚛️",
            ".java": "☕",
            ".go": "🔷",
            ".rs": "🦀",
            ".c": "©️",
            ".cpp": "➕",
            ".h": "📋",
            ".md": "📝",
            ".txt": "📄",
            ".json": "📊",
            ".yaml": "⚙️",
            ".yml": "⚙️",
            ".toml": "⚙️",
            ".xml": "📰",
            ".html": "🌐",
            ".css": "🎨",
            ".sh": "💻",
            ".bash": "💻",
            ".sql": "🗄️",
            ".db": "💾",
            ".lock": "🔒",
            ".env": "🔐",
            ".git": "🔀",
            ".gitignore": "🚫",
            ".dockerfile": "🐳",
            ".png": "🖼️",
            ".jpg": "🖼️",
            ".jpeg": "🖼️",
            ".gif": "🎞️",
            ".svg": "🎨",
            ".pdf": "📕",
            ".zip": "📦",
            ".tar": "📦",
            ".gz": "📦",
        }
        return emoji_map.get(ext, "📄")

    @property
    def display_name(self) -> str:
        """Get display name with emoji."""
        suffix = "/" if self.is_dir else ""
        return f"{self.emoji} {self.name}{suffix}"

    @property
    def size_str(self) -> str:
        """Get human-readable size."""
        if self.size is None or self.is_dir:
            return ""

        if self.size < 1024:
            return f"{self.size}B"
        elif self.size < 1024 * 1024:
            return f"{self.size / 1024:.1f}KB"
        elif self.size < 1024 * 1024 * 1024:
            return f"{self.size / (1024 * 1024):.1f}MB"
        else:
            return f"{self.size / (1024 * 1024 * 1024):.1f}GB"


class FileBrowser:
    """Interactive file browser for Telegram."""

    def __init__(self, approved_directory: Path, items_per_page: int = 8):
        """Initialize file browser.

        Args:
            approved_directory: Root directory for browsing
            items_per_page: Number of items to show per page
        """
        self.approved_directory = approved_directory
        self.items_per_page = items_per_page

    def list_directory(
        self, directory: Path, page: int = 0, show_hidden: bool = False
    ) -> Tuple[List[FileNode], int]:
        """List files and directories.

        Args:
            directory: Directory to list
            page: Page number (0-indexed)
            show_hidden: Whether to show hidden files

        Returns:
            Tuple of (file_nodes, total_pages)
        """
        if not directory.exists() or not directory.is_dir():
            logger.warning("Directory does not exist", directory=str(directory))
            return [], 0

        try:
            # Get all entries
            entries = []
            for entry in directory.iterdir():
                # Skip hidden files unless requested
                if not show_hidden and entry.name.startswith("."):
                    continue

                # Get file info
                is_dir = entry.is_dir()
                size = None
                modified_time = None

                if not is_dir:
                    try:
                        stat = entry.stat()
                        size = stat.st_size
                        modified_time = stat.st_mtime
                    except Exception as e:
                        logger.warning("Failed to stat file", file=str(entry), error=str(e))

                node = FileNode(
                    name=entry.name,
                    path=entry,
                    is_dir=is_dir,
                    size=size,
                    modified_time=modified_time,
                )
                entries.append(node)

            # Sort: directories first, then files, alphabetically
            entries.sort(key=lambda x: (not x.is_dir, x.name.lower()))

            # Paginate
            total_pages = (len(entries) + self.items_per_page - 1) // self.items_per_page
            start_idx = page * self.items_per_page
            end_idx = start_idx + self.items_per_page
            page_entries = entries[start_idx:end_idx]

            return page_entries, total_pages

        except PermissionError:
            logger.error("Permission denied", directory=str(directory))
            return [], 0
        except Exception as e:
            logger.error("Failed to list directory", directory=str(directory), error=str(e))
            return [], 0

    def create_keyboard(
        self,
        current_dir: Path,
        page: int = 0,
        show_hidden: bool = False,
    ) -> InlineKeyboardMarkup:
        """Create inline keyboard for file browser.

        Args:
            current_dir: Current directory being browsed
            page: Current page number
            show_hidden: Whether to show hidden files

        Returns:
            InlineKeyboardMarkup for Telegram
        """
        entries, total_pages = self.list_directory(current_dir, page, show_hidden)

        keyboard = []

        # Add parent directory button if not at root
        if current_dir != self.approved_directory:
            parent = current_dir.parent
            keyboard.append([
                InlineKeyboardButton(
                    "⬆️ ..", callback_data=f"browse:{parent}:0:{'1' if show_hidden else '0'}"
                )
            ])

        # Add file/directory buttons
        for entry in entries:
            if entry.is_dir:
                # Directory: navigate into it
                callback_data = f"browse:{entry.path}:0:{'1' if show_hidden else '0'}"
                button_text = entry.display_name
            else:
                # File: show file actions
                callback_data = f"file_actions:{entry.path}"
                size_info = f" ({entry.size_str})" if entry.size_str else ""
                button_text = f"{entry.display_name}{size_info}"

            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

        # Navigation buttons
        nav_buttons = []

        # Previous page
        if page > 0:
            nav_buttons.append(
                InlineKeyboardButton(
                    "◀️ Prev",
                    callback_data=f"browse:{current_dir}:{page-1}:{'1' if show_hidden else '0'}",
                )
            )

        # Page indicator
        if total_pages > 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    f"📄 {page + 1}/{total_pages}",
                    callback_data="noop",
                )
            )

        # Next page
        if page < total_pages - 1:
            nav_buttons.append(
                InlineKeyboardButton(
                    "Next ▶️",
                    callback_data=f"browse:{current_dir}:{page+1}:{'1' if show_hidden else '0'}",
                )
            )

        if nav_buttons:
            keyboard.append(nav_buttons)

        # Action buttons row
        action_buttons = []

        # Toggle hidden files
        hidden_text = "🙈 Hide Hidden" if show_hidden else "👁️ Show Hidden"
        action_buttons.append(
            InlineKeyboardButton(
                hidden_text,
                callback_data=f"browse:{current_dir}:{page}:{'0' if show_hidden else '1'}",
            )
        )

        # Refresh
        action_buttons.append(
            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data=f"browse:{current_dir}:{page}:{'1' if show_hidden else '0'}",
            )
        )

        keyboard.append(action_buttons)

        # Close button
        keyboard.append([InlineKeyboardButton("❌ Close", callback_data="close")])

        return InlineKeyboardMarkup(keyboard)

    def create_file_actions_keyboard(self, file_path: Path) -> InlineKeyboardMarkup:
        """Create keyboard with file actions.

        Args:
            file_path: Path to the file

        Returns:
            InlineKeyboardMarkup with file action buttons
        """
        keyboard = []

        # Read file
        keyboard.append([
            InlineKeyboardButton("📖 Read", callback_data=f"file_read:{file_path}")
        ])

        # Edit file
        keyboard.append([
            InlineKeyboardButton("✏️ Edit", callback_data=f"file_edit:{file_path}")
        ])

        # Delete file (with confirmation)
        keyboard.append([
            InlineKeyboardButton("🗑️ Delete", callback_data=f"file_delete_confirm:{file_path}")
        ])

        # Copy path to clipboard
        keyboard.append([
            InlineKeyboardButton("📋 Copy Path", callback_data=f"file_copy_path:{file_path}")
        ])

        # Back to browser
        parent_dir = file_path.parent
        keyboard.append([
            InlineKeyboardButton(
                "⬅️ Back", callback_data=f"browse:{parent_dir}:0:0"
            )
        ])

        return InlineKeyboardMarkup(keyboard)

    def format_directory_message(self, current_dir: Path, page: int = 0) -> str:
        """Format message text for directory listing.

        Args:
            current_dir: Current directory
            page: Current page number

        Returns:
            Formatted message text
        """
        # Get relative path from approved directory
        try:
            relative_path = current_dir.relative_to(self.approved_directory)
            path_display = f"/{relative_path}" if str(relative_path) != "." else "/"
        except ValueError:
            # Not relative to approved directory (shouldn't happen)
            path_display = str(current_dir)

        # Count items
        try:
            total_items = len(list(current_dir.iterdir()))
            dirs = len([e for e in current_dir.iterdir() if e.is_dir()])
            files = total_items - dirs
        except Exception:
            total_items = dirs = files = 0

        message = (
            f"📂 **File Browser**\n\n"
            f"**Current Directory:**\n`{path_display}`\n\n"
            f"**Contents:** {total_items} items ({dirs} dirs, {files} files)\n\n"
            f"_Select a file or directory:_"
        )

        return message

    def format_file_info_message(self, file_path: Path) -> str:
        """Format message with file information.

        Args:
            file_path: Path to the file

        Returns:
            Formatted message with file details
        """
        try:
            stat = file_path.stat()

            # Size
            size = stat.st_size
            if size < 1024:
                size_str = f"{size} bytes"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} KB"
            elif size < 1024 * 1024 * 1024:
                size_str = f"{size / (1024 * 1024):.2f} MB"
            else:
                size_str = f"{size / (1024 * 1024 * 1024):.2f} GB"

            # Modified time
            import datetime

            mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
            mtime_str = mtime.strftime("%Y-%m-%d %H:%M:%S")

            # Get file type emoji
            node = FileNode(name=file_path.name, path=file_path, is_dir=False, size=size)

            message = (
                f"{node.emoji} **File Info**\n\n"
                f"**Name:** `{file_path.name}`\n"
                f"**Size:** {size_str}\n"
                f"**Modified:** {mtime_str}\n"
                f"**Type:** {file_path.suffix or 'No extension'}\n\n"
                f"**Path:**\n`{file_path}`\n\n"
                f"_What would you like to do?_"
            )

            return message

        except Exception as e:
            logger.error("Failed to get file info", file=str(file_path), error=str(e))
            return f"📄 **{file_path.name}**\n\nUnable to retrieve file information."
