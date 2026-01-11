"""Tool execution tracking for real-time visibility.

This module tracks tool calls and their results to provide better
user feedback during Claude Code execution.
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger()


@dataclass
class ToolExecution:
    """Track a single tool execution."""

    tool_name: str
    tool_id: str
    parameters: Dict[str, Any]
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Any] = None
    error: Optional[str] = None

    @property
    def duration_ms(self) -> Optional[int]:
        """Get execution duration in milliseconds."""
        if self.end_time:
            return int((self.end_time - self.start_time) * 1000)
        return None

    def mark_running(self) -> None:
        """Mark tool as currently running."""
        self.status = "running"

    def mark_completed(self, result: Any = None) -> None:
        """Mark tool as completed successfully."""
        self.status = "completed"
        self.result = result
        self.end_time = time.time()

    def mark_failed(self, error: str) -> None:
        """Mark tool as failed."""
        self.status = "failed"
        self.error = error
        self.end_time = time.time()


class ToolExecutionTracker:
    """Track tool executions across sessions."""

    def __init__(self):
        """Initialize tracker."""
        self.executions: Dict[str, ToolExecution] = {}
        self.session_tools: Dict[str, List[str]] = {}  # session_id -> tool_ids

    def start_tool(
        self, tool_name: str, tool_id: str, parameters: Dict[str, Any], session_id: str
    ) -> ToolExecution:
        """Start tracking a tool execution."""
        execution = ToolExecution(
            tool_name=tool_name, tool_id=tool_id, parameters=parameters
        )
        execution.mark_running()

        self.executions[tool_id] = execution

        # Track per session
        if session_id not in self.session_tools:
            self.session_tools[session_id] = []
        self.session_tools[session_id].append(tool_id)

        logger.info(
            "Started tracking tool execution",
            tool_name=tool_name,
            tool_id=tool_id,
            session_id=session_id,
        )

        return execution

    def complete_tool(self, tool_id: str, result: Any = None) -> Optional[ToolExecution]:
        """Mark tool as completed."""
        if tool_id in self.executions:
            execution = self.executions[tool_id]
            execution.mark_completed(result)

            logger.info(
                "Tool execution completed",
                tool_name=execution.tool_name,
                tool_id=tool_id,
                duration_ms=execution.duration_ms,
            )

            return execution

        logger.warning("Tool completion for unknown tool_id", tool_id=tool_id)
        return None

    def fail_tool(self, tool_id: str, error: str) -> Optional[ToolExecution]:
        """Mark tool as failed."""
        if tool_id in self.executions:
            execution = self.executions[tool_id]
            execution.mark_failed(error)

            logger.warning(
                "Tool execution failed",
                tool_name=execution.tool_name,
                tool_id=tool_id,
                error=error,
                duration_ms=execution.duration_ms,
            )

            return execution

        logger.warning("Tool failure for unknown tool_id", tool_id=tool_id)
        return None

    def get_execution(self, tool_id: str) -> Optional[ToolExecution]:
        """Get execution by tool ID."""
        return self.executions.get(tool_id)

    def get_session_tools(self, session_id: str) -> List[ToolExecution]:
        """Get all tool executions for a session."""
        tool_ids = self.session_tools.get(session_id, [])
        return [self.executions[tid] for tid in tool_ids if tid in self.executions]

    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for session tool usage."""
        tools = self.get_session_tools(session_id)

        stats = {
            "total_tools": len(tools),
            "completed": len([t for t in tools if t.status == "completed"]),
            "failed": len([t for t in tools if t.status == "failed"]),
            "running": len([t for t in tools if t.status == "running"]),
            "tool_breakdown": {},
        }

        # Tool type breakdown
        for tool in tools:
            if tool.tool_name not in stats["tool_breakdown"]:
                stats["tool_breakdown"][tool.tool_name] = 0
            stats["tool_breakdown"][tool.tool_name] += 1

        return stats

    def clear_session(self, session_id: str) -> None:
        """Clear tracking data for a session."""
        if session_id in self.session_tools:
            tool_ids = self.session_tools[session_id]

            # Remove executions
            for tool_id in tool_ids:
                if tool_id in self.executions:
                    del self.executions[tool_id]

            # Remove session tracking
            del self.session_tools[session_id]

            logger.info(
                "Cleared tool tracking for session",
                session_id=session_id,
                tools_removed=len(tool_ids),
            )
