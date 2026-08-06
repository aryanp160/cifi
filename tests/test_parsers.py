import pytest
from cifi.parser import get_parser, GitHubActionsParser, PytestParser, JestParser, CargoParser, GenericParser
from cifi.models import Severity, FailureCategory


def test_github_actions_parser():
    sample_log = (
        "Starting workflow...\n"
        "##[error]file=src/auth.py,line=25,col=4::ModuleNotFoundError: No module named 'jwt'\n"
        "##[warning]Deprecation notice\n"
    )
    parser = get_parser(sample_log)
    assert isinstance(parser, GitHubActionsParser)
    report = parser.parse(sample_log, source_name="gha.log")

    assert report.total_lines_parsed == 3
    assert len(report.diagnostics) == 2
    assert report.diagnostics[0].location.file_path == "src/auth.py"
    assert report.diagnostics[0].location.line_number == 25
    assert report.diagnostics[0].severity == Severity.ERROR
    assert report.diagnostics[1].severity == Severity.WARNING


def test_pytest_parser():
    sample_log = (
        "File \"tests/test_api.py\", line 15, in test_login\n"
        "FAILED tests/test_api.py::test_login - AssertionError: 404 != 200\n"
    )
    parser = get_parser(sample_log)
    assert isinstance(parser, PytestParser)
    report = parser.parse(sample_log, source_name="pytest.log")

    assert len(report.diagnostics) == 1
    diag = report.diagnostics[0]
    assert diag.location.file_path == "tests/test_api.py"
    assert diag.location.line_number == 15
    assert diag.location.function_name == "test_login"


def test_jest_parser():
    sample_log = (
        "FAIL src/components/Button.test.js\n"
        "  ● Button Component › renders correctly\n"
        "    at Object.<anonymous> (src/components/Button.test.js:12:5)\n"
    )
    parser = get_parser(sample_log)
    assert isinstance(parser, JestParser)
    report = parser.parse(sample_log, source_name="jest.log")

    assert len(report.diagnostics) == 1
    diag = report.diagnostics[0]
    assert diag.location.file_path == "src/components/Button.test.js"
    assert diag.location.line_number == 12


def test_cargo_parser():
    sample_log = (
        "error[E0425]: cannot find value `foo` in this scope\n"
        "  --> src/main.rs:18:5\n"
    )
    parser = get_parser(sample_log)
    assert isinstance(parser, CargoParser)
    report = parser.parse(sample_log, source_name="cargo.log")

    assert len(report.diagnostics) == 1
    diag = report.diagnostics[0]
    assert diag.category == FailureCategory.COMPILATION_ERROR
    assert diag.location.file_path == "src/main.rs"
    assert diag.location.line_number == 18


def test_generic_parser_fallback():
    sample_log = "2026-08-06 [ERROR] database connection failed: timeout at db.py:100\n"
    parser = get_parser(sample_log)
    assert isinstance(parser, GenericParser)
    report = parser.parse(sample_log, source_name="generic.log")

    assert len(report.diagnostics) == 1
    assert "database connection failed" in report.diagnostics[0].summary
