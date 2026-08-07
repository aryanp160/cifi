import pytest
from cifi.benchmarks import BenchmarkRunner, BenchmarkReport


def test_benchmark_runner_execution():
    runner = BenchmarkRunner()
    report = runner.run()

    assert isinstance(report, BenchmarkReport)
    assert report.total_cases == 5
    assert report.passed_cases == 5
    assert report.accuracy_rate == 100.0
    assert report.regression_count == 0
    assert report.avg_runtime_ms <= 10.0
