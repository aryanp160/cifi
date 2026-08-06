import pytest
from click.testing import CliRunner
from cifi.cli.main import cli


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0a2" in result.output


def test_cli_rules():
    runner = CliRunner()
    result = runner.invoke(cli, ["rules"])
    assert result.exit_code == 0
    assert "R001" in result.output
    assert "Missing Dependency" in result.output


def test_cli_parse_file(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("##[error]file=app.py,line=5::ModuleNotFoundError: No module named 'foo'\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["parse", str(log_file)])
    assert result.exit_code == 0
    assert "ModuleNotFoundError" in result.output
    assert "missing_dependency" in result.output


def test_cli_parse_json(tmp_path):
    log_file = tmp_path / "pytest.log"
    log_file.write_text("FAILED tests/test_foo.py::test_bar - AssertionError: msg\n")

    runner = CliRunner()
    result = runner.invoke(cli, ["parse", str(log_file), "--json"])
    assert result.exit_code == 0
    assert '"parser_type": "pytest"' in result.output
    assert '"assertion_failure"' in result.output
