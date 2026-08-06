import pytest
from cifi.pipeline import LogIntelligencePipeline
from cifi.models import FailureCategory


def test_pipeline_execution():
    raw_log = "##[error]file=src/api.py,line=10::ModuleNotFoundError: No module named 'flask'\n"
    pipeline = LogIntelligencePipeline()
    report = pipeline.run(raw_log, source_name="gha_pipeline.log")

    assert report.log_source == "gha_pipeline.log"
    assert report.parser_type == "github_actions"
    assert report.execution_time_ms is not None
    assert report.execution_time_ms >= 0.0
    assert len(report.diagnostics) == 1
    assert report.diagnostics[0].category == FailureCategory.MISSING_DEPENDENCY
    assert report.diagnosed_count == 1
