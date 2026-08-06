from typing import List, Optional
from cifi.models import CIFailureReport, Language, Framework
from cifi.rules.base import Rule
from cifi.rules.builtin import (
    CompilationErrorRule,
    MissingDependencyRule,
    AssertionFailureRule,
    MemoryExceededRule,
    EnvironmentVariableRule,
    TimeoutRule,
)
from cifi.intelligence.detectors import EnvironmentDetector
from cifi.intelligence.fingerprints import FingerprintGenerator


class RuleEngine:
    """Evaluates deterministic failure rules by RulePriority and generates Failure Fingerprints & Explainability blocks."""

    def __init__(self, rules: Optional[List[Rule]] = None):
        if rules is None:
            self.rules = [
                MemoryExceededRule(),
                CompilationErrorRule(),
                MissingDependencyRule(),
                AssertionFailureRule(),
                EnvironmentVariableRule(),
                TimeoutRule(),
            ]
        else:
            self.rules = rules

        # Sort rules by priority descending
        self.rules.sort(key=lambda r: getattr(r, "priority", 50), reverse=True)

    def process_report(self, report: CIFailureReport, log_text: str = "") -> CIFailureReport:
        """Run priority-sorted rules against diagnostics, attach fingerprints, and detect environment."""
        # Detect Ecosystem
        if log_text:
            lang, fw = EnvironmentDetector.detect(log_text)
            report.detected_language = lang
            report.detected_framework = fw

        for diag in report.diagnostics:
            for rule in self.rules:
                match = rule.evaluate(diag)
                if match:
                    diag.rule_match = match
                    diag.category = rule.category
                    diag.fingerprint = FingerprintGenerator.generate(
                        diag, report.detected_language, report.detected_framework
                    )
                    break
        return report
