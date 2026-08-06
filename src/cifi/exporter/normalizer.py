import re
from cifi.models import CIFailureReport


class OutputNormalizer:
    """Normalizes raw diagnostic text, strips ANSI escape sequences, and cleans log noise."""

    ANSI_ESCAPE_REGEX = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    @classmethod
    def strip_ansi(cls, text: str) -> str:
        """Remove ANSI color codes and terminal formatting characters."""
        return cls.ANSI_ESCAPE_REGEX.sub("", text)

    def normalize(self, report: CIFailureReport) -> CIFailureReport:
        """Clean and normalize all diagnostics in the failure report."""
        for diag in report.diagnostics:
            diag.summary = self.strip_ansi(diag.summary).strip()
            diag.message = self.strip_ansi(diag.message).strip()
            if diag.context and diag.context.raw_lines:
                diag.context.raw_lines = [self.strip_ansi(line) for line in diag.context.raw_lines]
        return report
