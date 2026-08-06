import pytest
from cifi.models import (
    CIFailureReport,
    DiagnosticItem,
    FailureCategory,
    Severity,
    CodeLocation,
    ConfidenceLevel,
    Language,
    Framework,
    ExplainabilityBlock,
    RulePriority,
)


def test_code_location_creation():
    loc = CodeLocation(file_path="src/main.py", line_number=42, column_number=10, function_name="test_foo")
    assert loc.file_path == "src/main.py"
    assert loc.line_number == 42
    assert loc.column_number == 10
    assert loc.function_name == "test_foo"


def test_confidence_level_mapping():
    assert ConfidenceLevel.from_score(0.95) == ConfidenceLevel.HIGH
    assert ConfidenceLevel.from_score(0.85) == ConfidenceLevel.HIGH
    assert ConfidenceLevel.from_score(0.75) == ConfidenceLevel.MEDIUM
    assert ConfidenceLevel.from_score(0.50) == ConfidenceLevel.LOW


def test_explainability_and_fingerprint():
    exp = ExplainabilityBlock(
        rule_id="R002",
        matched_expression="ModuleNotFoundError",
        stack_keyword="pyjwt",
        reason="Detected import failure after dependency resolution.",
    )
    diag = DiagnosticItem(
        summary="Missing pyjwt package",
        fingerprint="PYTHON-IMPORT-UV-001",
        confidence_score=0.98,
        explainability=exp,
    )

    assert diag.fingerprint == "PYTHON-IMPORT-UV-001"
    assert diag.confidence_level == ConfidenceLevel.HIGH
    assert diag.explainability.rule_id == "R002"
    assert "dependency resolution" in diag.explainability.reason


def test_report_language_framework_defaults():
    report = CIFailureReport(
        log_source="build.log",
        detected_language=Language.PYTHON,
        detected_framework=Framework.UV,
    )
    assert report.detected_language == Language.PYTHON
    assert report.detected_framework == Framework.UV
