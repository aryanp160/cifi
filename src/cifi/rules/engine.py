from typing import List
from cifi.models import CIFailureReport
from cifi.rules.base import Rule
from cifi.rules.builtin import (
    CompilationErrorRule,
    MissingDependencyRule,
    AssertionFailureRule,
    TimeoutRule,
    PermissionRule,
    FileNotFoundErrorRule,
)


class RuleEngine:
    """Evaluates registered failure rules against a CIFailureReport and annotates findings."""

    def __init__(self, rules: List[Rule] = None):
        if rules is None:
            self.rules = [
                MissingDependencyRule(),
                CompilationErrorRule(),
                AssertionFailureRule(),
                TimeoutRule(),
                PermissionRule(),
                FileNotFoundErrorRule(),
            ]
        else:
            self.rules = rules

    def process_report(self, report: CIFailureReport) -> CIFailureReport:
        """Run all registered rules against report diagnostics and update categories/metadata."""
        for diag in report.diagnostics:
            for rule in self.rules:
                match = rule.evaluate(diag)
                if match:
                    diag.rule_match = match
                    diag.category = rule.category
                    break
        return report
