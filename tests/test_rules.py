import pytest
from cifi.models import CIFailureReport, DiagnosticItem, Severity, FailureCategory, ConfidenceLevel
from cifi.rules import RuleEngine


def test_rule_engine_missing_dependency_explainability():
    diag = DiagnosticItem(
        summary="ModuleNotFoundError: No module named 'requests'",
        message="Traceback (most recent call last): ...",
    )
    report = CIFailureReport(diagnostics=[diag])

    engine = RuleEngine()
    processed = engine.process_report(report, log_text="ModuleNotFoundError: No module named 'requests'")

    assert processed.diagnostics[0].category == FailureCategory.MISSING_DEPENDENCY
    assert processed.diagnostics[0].rule_match is not None
    assert processed.diagnostics[0].rule_match.rule_id == "R002"
    assert processed.diagnostics[0].confidence_level == ConfidenceLevel.HIGH
    assert processed.diagnostics[0].fingerprint == "PYTHON-IMPORT-PIP-002"
    assert processed.diagnostics[0].explainability is not None
    assert "Import statement referenced" in processed.diagnostics[0].explainability.reason


def test_rule_engine_memory_exceeded_fingerprint():
    diag = DiagnosticItem(
        summary="FATAL ERROR: JavaScript heap out of memory",
        message="Allocation failed - JavaScript heap out of memory",
    )
    report = CIFailureReport(diagnostics=[diag])

    engine = RuleEngine()
    processed = engine.process_report(report, log_text="FAIL src/app.test.js\nheap out of memory")

    assert processed.diagnostics[0].category == FailureCategory.MEMORY_EXCEEDED
    assert processed.diagnostics[0].fingerprint == "SYS-MEMORY-OOM-001"
    assert processed.diagnostics[0].confidence_level == ConfidenceLevel.HIGH
