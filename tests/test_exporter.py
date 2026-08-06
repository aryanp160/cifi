import json
import os
import pytest
from cifi.models import CIFailureReport, DiagnosticItem, Severity, FailureCategory, CodeLocation
from cifi.exporter import OutputNormalizer, JSONExporter


def test_strip_ansi():
    raw_text = "\x1b[31m[ERROR]\x1b[0m ModuleNotFoundError: No module named 'requests'"
    cleaned = OutputNormalizer.strip_ansi(raw_text)
    assert cleaned == "[ERROR] ModuleNotFoundError: No module named 'requests'"


def test_json_exporter_to_dict():
    diag = DiagnosticItem(
        summary="\x1b[31mSyntax Error\x1b[0m",
        message="invalid syntax at main.py:10",
        category=FailureCategory.COMPILATION_ERROR,
        location=CodeLocation(file_path="main.py", line_number=10),
    )
    report = CIFailureReport(log_source="build.log", diagnostics=[diag])

    exporter = JSONExporter()
    data = exporter.to_dict(report)

    assert data["log_source"] == "build.log"
    assert data["diagnostics"][0]["summary"] == "Syntax Error"
    assert data["diagnostics"][0]["location"]["file_path"] == "main.py"


def test_json_exporter_file(tmp_path):
    diag = DiagnosticItem(summary="Assertion Error")
    report = CIFailureReport(diagnostics=[diag])

    out_file = str(tmp_path / "report.json")
    exporter = JSONExporter()
    exporter.export_file(report, out_file)

    assert os.path.exists(out_file)
    with open(out_file, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert content["diagnostics"][0]["summary"] == "Assertion Error"


def test_ai_prompt_format():
    diag = DiagnosticItem(
        summary="Import Error",
        message="ImportError: missing mod",
        severity=Severity.ERROR,
        location=CodeLocation(file_path="src/app.py", line_number=5),
    )
    report = CIFailureReport(log_source="run.log", diagnostics=[diag])

    exporter = JSONExporter()
    ai_text = exporter.export_ai_prompt_format(report)

    assert "=== CI FAILURE DIAGNOSTIC REPORT ===" in ai_text
    assert "Location: src/app.py:5" in ai_text
