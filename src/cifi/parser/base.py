from abc import ABC, abstractmethod
from typing import List
from cifi.models import CIFailureReport, LogContext


class BaseParser(ABC):
    """Abstract base class for all log parser implementations."""

    name: str = "base"

    @abstractmethod
    def parse(self, log_content: str, source_name: str = "unknown") -> CIFailureReport:
        """Parse log content string into a normalized CIFailureReport."""
        pass

    def extract_context(
        self,
        lines: List[str],
        target_idx: int,
        context_before: int = 3,
        context_after: int = 3,
    ) -> LogContext:
        """Extract a window of context lines around a specific line index."""
        start = max(0, target_idx - context_before)
        end = min(len(lines), target_idx + context_after + 1)
        return LogContext(
            raw_lines=lines[start:end],
            line_start_index=start,
            line_end_index=end - 1,
        )
