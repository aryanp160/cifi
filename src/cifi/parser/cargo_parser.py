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


class CargoParser(BaseParser):
    """Parser for Rust Cargo build logs and compiler outputs."""

    name = "cargo"

    # error[E0425]: cannot find value `x` in this scope
    CARGO_ERROR_REGEX = re.compile(r"error\[(?P<code>E\d+)\]:\s*(?P<msg>.*)")
    #  --> src/main.rs:15:9
    CARGO_SPAN_REGEX = re.compile(r"\s*-->\s*(?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+)")

    def parse(self, log_content: str, source_name: str = "unknown") -> CIFailureReport:
        lines = log_content.splitlines()
        diagnostics: List[DiagnosticItem] = []

        for idx, line in enumerate(lines):
            match = self.CARGO_ERROR_REGEX.search(line)
            if match:
                err_code = match.group("code")
                msg = match.group("msg").strip()

                loc_file = None
                loc_line = None
                loc_col = None

                # Look forward for the arrow indicator line
                for fwd_idx in range(idx + 1, min(len(lines), idx + 5)):
                    span_match = self.CARGO_SPAN_REGEX.search(lines[fwd_idx])
                    if span_match:
                        loc_file = span_match.group("file")
                        loc_line = int(span_match.group("line"))
                        loc_col = int(span_match.group("col"))
                        break

                location = CodeLocation(
                    file_path=loc_file,
                    line_number=loc_line,
                    column_number=loc_col,
                )
                context = self.extract_context(lines, idx, context_before=1, context_after=5)
                diag = DiagnosticItem(
                    category=FailureCategory.COMPILATION_ERROR,
                    severity=Severity.ERROR,
                    summary=f"Rust [{err_code}]: {msg}",
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
