import pytest
from cifi.models import (
    CIFailureReport,
    DiagnosticItem,
    FailureCategory,
    Severity,
    CodeLocation,
    LogContext,
    RuleMatchMetadata,
)


def test_code_location_creation():
    loc = CodeLocation(file_path="src/main.py", line_number=42, column_number=10, function_name="test_foo")
    assert loc.file_path == "src/main.py"
    assert loc.line_number == 42
    assert loc.column_number == 10
    assert loc.function_name == "test_foo"


def test_diagnostic_item_defaults():
    item = DiagnosticItem(summary="Test failure")
    assert item.category == FailureCategory.UNKNOWN_FAILURE
    assert item.severity == Severity.ERROR
    assert item.summary == "Test failure"
    assert item.location is None


def test_report_failure_counts():
    err_diag = DiagnosticItem(
        category=FailureCategory.ASSERTION_FAILURE,
        severity=Severity.ERROR,
        summary="Assertion Error",
    )
    warn_diag = DiagnosticItem(
        category=FailureCategory.UNKNOWN_FAILURE,
        severity=Severity.WARNING,
        summary="Deprecation warning",
    )
    report = CIFailureReport(
        log_source="ci_run.log",
        total_lines_parsed=100,
        diagnostics=[err_diag, warn_diag],
    )

    assert report.has_failures is True
    assert report.failure_count == 1
    assert report.warning_count == 1
