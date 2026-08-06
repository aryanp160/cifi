import pytest
from cifi.models import CIFailureReport, DiagnosticItem, Severity, FailureCategory
from cifi.rules import RuleEngine, MissingDependencyRule, TimeoutRule


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


def test_rule_engine_timeout():
    diag = DiagnosticItem(
        summary="Job cancelled after 15 minutes due to timeout",
        message="Process SIGKILL sent",
    )
    report = CIFailureReport(diagnostics=[diag])

    engine = RuleEngine()
    processed = engine.process_report(report)

    assert processed.diagnostics[0].category == FailureCategory.TIMEOUT
    assert processed.diagnostics[0].rule_match.rule_id == "R004"
