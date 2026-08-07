import pytest
from cifi.benchmarks import BenchmarkRunner, BenchmarkReport


def test_benchmark_zero_regression_barrier():
    """Strict automated regression test barrier.

    Enforces zero regressions, 100% accuracy, and microsecond SLA across all 5 CI categories.
    """
    runner = BenchmarkRunner()
    report = runner.run()

    assert isinstance(report, BenchmarkReport)
    assert report.total_cases == 5, f"Expected 5 benchmark corpus cases, found {report.total_cases}"
    assert report.regression_count == 0, f"REGRESSION DETECTED: {report.regression_count} cases failed expectation"
    assert report.accuracy_rate == 100.0, f"Accuracy rate {report.accuracy_rate}% is below 100.0% SLA"
    assert report.avg_runtime_ms <= 5.0, f"Average runtime {report.avg_runtime_ms} ms exceeds 5.0ms SLA"
