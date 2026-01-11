"""Diff visualization and rendering utilities.

Provides formatted diff output for code changes, git diffs, and file comparisons.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

import structlog

logger = structlog.get_logger()


@dataclass
class DiffLine:
    """Represents a single line in a diff."""

    type: str  # 'added', 'removed', 'context', 'header'
    content: str
    line_num_old: Optional[int] = None
    line_num_new: Optional[int] = None


class DiffRenderer:
    """Render diffs in human-readable format for Telegram."""

    def __init__(self, max_context_lines: int = 3):
        """Initialize diff renderer.

        Args:
            max_context_lines: Maximum context lines to show around changes
        """
        self.max_context_lines = max_context_lines

    def parse_unified_diff(self, diff_text: str) -> List[DiffLine]:
        """Parse unified diff format into structured lines.

        Args:
            diff_text: Unified diff output (from git diff, etc.)

        Returns:
            List of DiffLine objects
        """
        lines = []
        old_line = 0
        new_line = 0

        for line in diff_text.split("\n"):
            if not line:
                continue

            # File headers
            if line.startswith("diff --git"):
                lines.append(DiffLine(type="header", content=line))
            elif line.startswith("index ") or line.startswith("---") or line.startswith("+++"):
                lines.append(DiffLine(type="header", content=line))

            # Hunk headers (@@ -1,5 +1,6 @@)
            elif line.startswith("@@"):
                match = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
                if match:
                    old_line = int(match.group(1))
                    new_line = int(match.group(2))
                lines.append(DiffLine(type="header", content=line))

            # Added lines
            elif line.startswith("+"):
                lines.append(
                    DiffLine(
                        type="added",
                        content=line[1:],  # Remove + prefix
                        line_num_new=new_line,
                    )
                )
                new_line += 1

            # Removed lines
            elif line.startswith("-"):
                lines.append(
                    DiffLine(
                        type="removed",
                        content=line[1:],  # Remove - prefix
                        line_num_old=old_line,
                    )
                )
                old_line += 1

            # Context lines
            elif line.startswith(" "):
                lines.append(
                    DiffLine(
                        type="context",
                        content=line[1:],
                        line_num_old=old_line,
                        line_num_new=new_line,
                    )
                )
                old_line += 1
                new_line += 1

            # Other lines
            else:
                lines.append(DiffLine(type="context", content=line))

        return lines

    def render_telegram(
        self, diff_lines: List[DiffLine], collapse_context: bool = True
    ) -> str:
        """Render diff for Telegram with Markdown formatting.

        Args:
            diff_lines: Parsed diff lines
            collapse_context: Whether to collapse unchanged context

        Returns:
            Formatted diff string
        """
        output = []
        context_buffer = []
        in_changes = False

        for i, line in enumerate(diff_lines):
            if line.type == "header":
                # File/hunk headers
                if line.content.startswith("diff --git"):
                    # Extract file name
                    match = re.search(r"a/(.*?) b/", line.content)
                    if match:
                        output.append(f"\n📄 **{match.group(1)}**")
                elif line.content.startswith("@@"):
                    # Hunk header
                    output.append(f"\n`{line.content}`")

            elif line.type in ["added", "removed"]:
                # Flush context buffer when entering changes
                if not in_changes and context_buffer:
                    if collapse_context and len(context_buffer) > self.max_context_lines * 2:
                        # Show first few and last few context lines
                        for ctx in context_buffer[: self.max_context_lines]:
                            output.append(f"  {ctx}")
                        output.append(f"  ... ({len(context_buffer) - self.max_context_lines * 2} lines)")
                        for ctx in context_buffer[-self.max_context_lines :]:
                            output.append(f"  {ctx}")
                    else:
                        for ctx in context_buffer:
                            output.append(f"  {ctx}")
                    context_buffer = []

                in_changes = True

                # Format changed lines
                if line.type == "added":
                    output.append(f"➕ {line.content}")
                else:  # removed
                    output.append(f"➖ {line.content}")

            elif line.type == "context":
                if in_changes:
                    # Context within changes - show immediately
                    output.append(f"  {line.content}")
                else:
                    # Buffer context lines
                    context_buffer.append(line.content)

        return "\n".join(output)

    def create_side_by_side_text(
        self, old_content: str, new_content: str, max_width: int = 35
    ) -> str:
        """Create text-based side-by-side diff (limited width for Telegram).

        Args:
            old_content: Old version of text
            new_content: New version of text
            max_width: Maximum width per side

        Returns:
            Formatted side-by-side diff
        """
        old_lines = old_content.split("\n")
        new_lines = new_content.split("\n")

        output = ["```"]
        output.append(f"{'Old':^{max_width}} | {'New':^{max_width}}")
        output.append("-" * max_width + "-+-" + "-" * max_width)

        max_lines = max(len(old_lines), len(new_lines))
        for i in range(max_lines):
            old_line = old_lines[i] if i < len(old_lines) else ""
            new_line = new_lines[i] if i < len(new_lines) else ""

            # Truncate long lines
            if len(old_line) > max_width:
                old_line = old_line[: max_width - 3] + "..."
            if len(new_line) > max_width:
                new_line = new_line[: max_width - 3] + "..."

            # Pad to width
            old_line = old_line.ljust(max_width)
            new_line = new_line.ljust(max_width)

            output.append(f"{old_line} | {new_line}")

        output.append("```")
        return "\n".join(output)

    def format_file_diff(
        self, file_path: str, old_content: str, new_content: str
    ) -> str:
        """Format a complete file diff.

        Args:
            file_path: Path to the file
            old_content: Original content
            new_content: Modified content

        Returns:
            Formatted diff
        """
        import difflib

        # Generate unified diff
        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
            lineterm="",
        )

        diff_text = "".join(diff)

        if not diff_text:
            return f"📄 **{file_path}**\n\n_No changes detected_"

        # Parse and render
        diff_lines = self.parse_unified_diff(diff_text)
        rendered = self.render_telegram(diff_lines)

        return rendered

    def summarize_changes(self, diff_lines: List[DiffLine]) -> dict:
        """Summarize diff statistics.

        Args:
            diff_lines: Parsed diff lines

        Returns:
            Dictionary with stats (additions, deletions, files_changed)
        """
        stats = {"additions": 0, "deletions": 0, "files_changed": 0, "files": []}

        current_file = None
        for line in diff_lines:
            if line.type == "header" and line.content.startswith("diff --git"):
                match = re.search(r"a/(.*?) b/", line.content)
                if match:
                    current_file = match.group(1)
                    stats["files_changed"] += 1
                    stats["files"].append(current_file)

            elif line.type == "added":
                stats["additions"] += 1
            elif line.type == "removed":
                stats["deletions"] += 1

        return stats


def format_diff_summary(stats: dict) -> str:
    """Format diff summary for Telegram.

    Args:
        stats: Statistics from summarize_changes()

    Returns:
        Formatted summary string
    """
    files = stats["files_changed"]
    additions = stats["additions"]
    deletions = stats["deletions"]

    summary = f"📊 **Diff Summary**\n\n"
    summary += f"📁 Files changed: {files}\n"
    summary += f"➕ Additions: {additions}\n"
    summary += f"➖ Deletions: {deletions}\n"
    summary += f"📈 Net change: {additions - deletions:+d} lines\n"

    if stats.get("files"):
        summary += f"\n**Files:**\n"
        for file in stats["files"][:10]:  # Limit to 10 files
            summary += f"• `{file}`\n"
        if len(stats["files"]) > 10:
            summary += f"• ... and {len(stats['files']) - 10} more\n"

    return summary


def truncate_diff(diff_text: str, max_lines: int = 50) -> Tuple[str, bool]:
    """Truncate diff if too long for Telegram.

    Args:
        diff_text: Full diff text
        max_lines: Maximum lines to include

    Returns:
        Tuple of (truncated_diff, was_truncated)
    """
    lines = diff_text.split("\n")

    if len(lines) <= max_lines:
        return diff_text, False

    truncated = "\n".join(lines[:max_lines])
    truncated += f"\n\n... ({len(lines) - max_lines} more lines truncated)"

    return truncated, True
