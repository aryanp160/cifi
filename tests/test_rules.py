import pytest
from cifi.models import CIFailureReport, DiagnosticItem, Severity, FailureCategory
from cifi.rules import RuleEngine


def test_rule_engine_missing_dependency():
    diag = DiagnosticItem(
        summary="ModuleNotFoundError: No module named 'requests'",
        message="Traceback (most recent call last): ...",
    )
    report = CIFailureReport(diagnostics=[diag])

    engine = RuleEngine()
    processed = engine.process_report(report)

    assert processed.diagnostics[0].category == FailureCategory.MISSING_DEPENDENCY
    assert processed.diagnostics[0].rule_match is not None
    assert processed.diagnostics[0].rule_match.rule_id == "R002"
    assert "Missing Dependency" in processed.diagnostics[0].rule_match.rule_name
    assert processed.diagnostics[0].suggested_remediation is not None


def test_rule_engine_memory_exceeded():
    diag = DiagnosticItem(
        summary="FATAL ERROR: JavaScript heap out of memory",
        message="Allocation failed - JavaScript heap out of memory",
    )
    report = CIFailureReport(diagnostics=[diag])

    engine = RuleEngine()
    processed = engine.process_report(report)

    assert processed.diagnostics[0].category == FailureCategory.MEMORY_EXCEEDED
    assert processed.diagnostics[0].rule_match.rule_id == "R007"
    assert "memory limits" in processed.diagnostics[0].suggested_remediation.lower()


def test_rule_engine_docker_error():
    diag = DiagnosticItem(
        summary="Task failed: container exit code 137",
        message="docker daemon error: container exit code 137",
    )
    report = CIFailureReport(diagnostics=[diag])

    engine = RuleEngine()
    processed = engine.process_report(report)

    assert processed.diagnostics[0].category == FailureCategory.DOCKER_ERROR
    assert processed.diagnostics[0].rule_match.rule_id == "R013"
