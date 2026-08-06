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


class JestParser(BaseParser):
    """Parser for Jest and npm test console output."""

    name = "jest"

    FAIL_SUITE_REGEX = re.compile(r"FAIL\s+(?P<file>[^\s]+)")
    STACK_FRAME_REGEX = re.compile(r"at\s+.*?\((?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+)\)")

    def parse(self, log_content: str, source_name: str = "unknown") -> CIFailureReport:
        lines = log_content.splitlines()
        diagnostics: List[DiagnosticItem] = []

        for idx, line in enumerate(lines):
            match = self.FAIL_SUITE_REGEX.search(line)
            if match:
                file_path = match.group("file")

                # Scan forward for specific failed test description or stack trace line
                err_summary = f"Jest Test Failure in {file_path}"
                line_no = None
                col_no = None

                for fwd_idx in range(idx + 1, min(len(lines), idx + 25)):
                    fwd_line = lines[fwd_idx]
                    if fwd_line.strip().startswith("●"):
                        err_summary = fwd_line.strip().lstrip("●").strip()
                    sf_match = self.STACK_FRAME_REGEX.search(fwd_line)
                    if sf_match:
                        line_no = int(sf_match.group("line"))
                        col_no = int(sf_match.group("col"))
                        break

                location = CodeLocation(
                    file_path=file_path,
                    line_number=line_no,
                    column_number=col_no,
                )
                context = self.extract_context(lines, idx, context_before=1, context_after=8)
                diag = DiagnosticItem(
                    category=FailureCategory.ASSERTION_FAILURE,
                    severity=Severity.ERROR,
                    summary=err_summary,
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
