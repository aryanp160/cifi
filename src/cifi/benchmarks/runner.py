import os
import json
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from cifi.pipeline import LogIntelligencePipeline


class BenchmarkCaseResult(BaseModel):
    case_id: str
    category_folder: str
    filename: str
    passed: bool
    actual_category: str = "unknown"
    actual_fingerprint: str = "UNKNOWN-000"
    actual_confidence: str = "LOW"
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None


class BenchmarkReport(BaseModel):
    version: str = "0.2.1"
    total_cases: int = 0
    passed_cases: int = 0
    accuracy_rate: float = 0.0
    avg_runtime_ms: float = 0.0
    regression_count: int = 0
    results: List[BenchmarkCaseResult] = Field(default_factory=list)
    category_summaries: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class BenchmarkRunner:
    """Automated benchmark framework and regression suite runner."""

    def __init__(self, benchmarks_dir: Optional[str] = None):
        if benchmarks_dir is None:
            self.benchmarks_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "benchmarks",
            )
        else:
            self.benchmarks_dir = benchmarks_dir

        self.manifest_path = os.path.join(self.benchmarks_dir, "manifest.json")

    def run(self) -> BenchmarkReport:
        """Run entire benchmark corpus against manifest.json expectations."""
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"Benchmark manifest not found at {self.manifest_path}")

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        cases = manifest.get("cases", [])
        pipeline = LogIntelligencePipeline()

        results: List[BenchmarkCaseResult] = []
        total_time = 0.0
        passed_count = 0
        regressions = 0

        cat_stats: Dict[str, Dict[str, Any]] = {}

        for case in cases:
            case_id = case["id"]
            cat_folder = case["category_folder"]
            filename = case["filename"]
            exp_cat = case["expected_category"]
            exp_fp = case["expected_fingerprint"]
            exp_conf = case.get("expected_confidence", "HIGH")

            log_path = os.path.join(self.benchmarks_dir, cat_folder, filename)
            if not os.path.exists(log_path):
                # Fallback check in root benchmarks_dir
                log_path = os.path.join(self.benchmarks_dir, filename)

            if not os.path.exists(log_path):
                results.append(
                    BenchmarkCaseResult(
                        case_id=case_id,
                        category_folder=cat_folder,
                        filename=filename,
                        passed=False,
                        error_message=f"Benchmark log file missing at {log_path}",
                    )
                )
                regressions += 1
                continue

            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            report = pipeline.run(content, source_name=filename)
            total_time += (report.execution_time_ms or 0.0)

            act_cat = "unknown"
            act_fp = "UNKNOWN-000"
            act_conf = "LOW"

            if report.diagnostics:
                d = report.diagnostics[0]
                act_cat = d.category.value
                act_fp = d.fingerprint or "GENERIC-001"
                act_conf = d.confidence_level.value

            passed = (act_cat == exp_cat) and (act_fp == exp_fp)
            if passed:
                passed_count += 1
            else:
                regressions += 1

            # Update category statistics
            if cat_folder not in cat_stats:
                cat_stats[cat_folder] = {"total": 0, "passed": 0, "time_ms": 0.0}
            cat_stats[cat_folder]["total"] += 1
            if passed:
                cat_stats[cat_folder]["passed"] += 1
            cat_stats[cat_folder]["time_ms"] += (report.execution_time_ms or 0.0)

            results.append(
                BenchmarkCaseResult(
                    case_id=case_id,
                    category_folder=cat_folder,
                    filename=filename,
                    passed=passed,
                    actual_category=act_cat,
                    actual_fingerprint=act_fp,
                    actual_confidence=act_conf,
                    execution_time_ms=report.execution_time_ms or 0.0,
                    error_message=None if passed else f"Expected {exp_cat}/{exp_fp}, got {act_cat}/{act_fp}",
                )
            )

        total_cases = len(cases)
        accuracy_rate = round((passed_count / total_cases * 100), 2) if total_cases > 0 else 0.0
        avg_runtime = round((total_time / total_cases), 2) if total_cases > 0 else 0.0

        for cat, stat in cat_stats.items():
            tot = stat["total"]
            stat["accuracy"] = round((stat["passed"] / tot * 100), 2) if tot > 0 else 0.0
            stat["avg_ms"] = round((stat["time_ms"] / tot), 2) if tot > 0 else 0.0

        return BenchmarkReport(
            version="0.2.1",
            total_cases=total_cases,
            passed_cases=passed_count,
            accuracy_rate=accuracy_rate,
            avg_runtime_ms=avg_runtime,
            regression_count=regressions,
            results=results,
            category_summaries=cat_stats,
        )
