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


class PytestParser(BaseParser):
    """Parser for Pytest console output and tracebacks."""

    name = "pytest"

    # FAILED tests/test_foo.py::test_bar - AssertionError: msg
    FAILED_LINE_REGEX = re.compile(
        r"FAILED\s+(?P<file>[^\s:]+)::(?P<func>[^\s\-]+)(?:\s+-\s+(?P<err>.*))?"
    )
    # File "path/to/file.py", line 42, in func
    TRACEBACK_FILE_REGEX = re.compile(
        r'File\s+"(?P<file>[^"]+)",\s+line\s+(?P<line>\d+)(?:,\s+in\s+(?P<func>\w+))?'
    )

    def parse(self, log_content: str, source_name: str = "unknown") -> CIFailureReport:
        lines = log_content.splitlines()
        diagnostics: List[DiagnosticItem] = []

        for idx, line in enumerate(lines):
            match = self.FAILED_LINE_REGEX.search(line)
            if match:
                file_path = match.group("file")
                func_name = match.group("func")
                err_msg = match.group("err") or "Test failure"

                # Look backwards for specific traceback location
                loc_file = file_path
                loc_line = None
                for back_idx in range(idx - 1, max(-1, idx - 20), -1):
                    tb_match = self.TRACEBACK_FILE_REGEX.search(lines[back_idx])
                    if tb_match:
                        loc_file = tb_match.group("file")
                        loc_line = int(tb_match.group("line"))
                        break

                location = CodeLocation(
                    file_path=loc_file,
                    line_number=loc_line,
                    function_name=func_name,
                )
                context = self.extract_context(lines, idx, context_before=5, context_after=1)
                diag = DiagnosticItem(
                    category=FailureCategory.ASSERTION_FAILURE,
                    severity=Severity.ERROR,
                    summary=f"Pytest Failure: {func_name}",
                    message=f"{line}\n{err_msg}",
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
