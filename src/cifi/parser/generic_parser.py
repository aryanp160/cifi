import re
from typing import List
from cifi.models import (
    CIFailureReport,
    DiagnosticItem,
    Severity,
    CodeLocation,
    FailureCategory,
)
from cifi.parser.base import BaseParser


class GenericParser(BaseParser):
    """Fallback parser using heuristics to identify common error signatures."""

    name = "generic"

    # Match standard error markers: ERROR, FATAL, Exception, Traceback
    ERROR_KEYWORD_REGEX = re.compile(
        r"(?:\[ERROR\]|\[FATAL\]|ERROR:|FATAL:|Traceback \(most recent call last\):|([A-Za-z0-9_]+Error):)\s*(?P<msg>.*)",
        re.IGNORECASE,
    )

    # Match file paths like path/to/file.ext:123
    FILE_LINE_REGEX = re.compile(r"(?P<file>[a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+):(?P<line>\d+)")

    def parse(self, log_content: str, source_name: str = "unknown") -> CIFailureReport:
        lines = log_content.splitlines()
        diagnostics: List[DiagnosticItem] = []

        for idx, line in enumerate(lines):
            match = self.ERROR_KEYWORD_REGEX.search(line)
            if match:
                msg = match.group("msg").strip() if match.group("msg") else line.strip()
                loc_match = self.FILE_LINE_REGEX.search(line)
                location = None
                if loc_match:
                    location = CodeLocation(
                        file_path=loc_match.group("file"),
                        line_number=int(loc_match.group("line")),
                    )

                context = self.extract_context(lines, idx)
                diag = DiagnosticItem(
                    category=FailureCategory.UNKNOWN_FAILURE,
                    severity=Severity.ERROR,
                    summary=msg[:120] if msg else "Error detected in log",
                    message=line,
                    location=location,
                    context=context,
                )
                diagnostics.append(diag)

        return CIFailureReport(
            log_source=source_name,
            parser_type=self.name,
            total_lines_parsed=len(lines),
            diagnostics=diagnostics,
        )
