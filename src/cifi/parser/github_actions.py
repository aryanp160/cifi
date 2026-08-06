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


class GitHubActionsParser(BaseParser):
    """Parser for GitHub Actions log streams and annotation workflows."""

    name = "github_actions"

    # Regex for GHA workflow commands: ##[error]file=app.py,line=10,col=5::Message or ##[warning]Message
    GHA_ANNOTATION_REGEX = re.compile(
        r"##\[(?P<level>error|warning)\](?:file=(?P<file>[^,]+))?(?:,line=(?P<line>\d+))?(?:,col=(?P<col>\d+))?(?:::|:|\s+)?(?P<message>.*)",
        re.IGNORECASE,
    )

    def parse(self, log_content: str, source_name: str = "unknown") -> CIFailureReport:
        lines = log_content.splitlines()
        diagnostics: List[DiagnosticItem] = []

        for idx, line in enumerate(lines):
            match = self.GHA_ANNOTATION_REGEX.search(line)
            if match:
                level = match.group("level").lower()
                sev = Severity.ERROR if level == "error" else Severity.WARNING
                file_path = match.group("file")
                line_no = int(match.group("line")) if match.group("line") else None
                col_no = int(match.group("col")) if match.group("col") else None
                message = match.group("message").strip()

                location = None
                if file_path or line_no:
                    location = CodeLocation(
                        file_path=file_path,
                        line_number=line_no,
                        column_number=col_no,
                    )

                context = self.extract_context(lines, idx)
                diag = DiagnosticItem(
                    category=FailureCategory.UNKNOWN_FAILURE,
                    severity=sev,
                    summary=message or f"GitHub Actions {level}",
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
