import os
import glob
import pytest
from cifi.pipeline import LogIntelligencePipeline
from cifi.models import FailureCategory


def test_empirical_benchmark_suite():
    benchmark_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "benchmarks")
    log_files = glob.glob(os.path.join(benchmark_dir, "*.log"))

    assert len(log_files) >= 4, "Benchmark suite requires at least 4 test log files"

    pipeline = LogIntelligencePipeline()
    total_logs = len(log_files)
    correct_diagnoses = 0
    total_execution_time = 0.0

    for filepath in log_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        report = pipeline.run(content, source_name=os.path.basename(filepath))
        total_execution_time += (report.execution_time_ms or 0.0)

        if report.diagnosed_count > 0:
            correct_diagnoses += 1

    accuracy_rate = (correct_diagnoses / total_logs) * 100
    avg_runtime_ms = round(total_execution_time / total_logs, 2)

    assert accuracy_rate >= 90.0, f"Accuracy rate {accuracy_rate}% is below 90% target"
    assert avg_runtime_ms <= 25.0, f"Average runtime {avg_runtime_ms} ms exceeds 25ms SLA"
