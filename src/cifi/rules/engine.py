from typing import List, Optional
from cifi.models import CIFailureReport
from cifi.rules.base import Rule
from cifi.rules.builtin import (
    CompilationErrorRule,
    MissingDependencyRule,
    AssertionFailureRule,
    TimeoutRule,
    PermissionRule,
    FileNotFoundErrorRule,
    MemoryExceededRule,
    NetworkConnectionRule,
    DatabaseMigrationRule,
    EnvironmentVariableRule,
    TypeMismatchRule,
    LockTimeoutRule,
    DockerContainerRule,
    DiskSpaceRule,
    DependencyConflictRule,
)


class RuleEngine:
    """Evaluates 15 registered deterministic failure rules against a CIFailureReport and annotates findings."""

    def __init__(self, rules: Optional[List[Rule]] = None):
        if rules is None:
            self.rules = [
                MissingDependencyRule(),
                CompilationErrorRule(),
                AssertionFailureRule(),
                TimeoutRule(),
                PermissionRule(),
                FileNotFoundErrorRule(),
                MemoryExceededRule(),
                NetworkConnectionRule(),
                DatabaseMigrationRule(),
                EnvironmentVariableRule(),
                TypeMismatchRule(),
                LockTimeoutRule(),
                DockerContainerRule(),
                DiskSpaceRule(),
                DependencyConflictRule(),
            ]
        else:
            self.rules = rules

    def process_report(self, report: CIFailureReport) -> CIFailureReport:
        """Run all registered rules against report diagnostics and update categories/metadata/remediations."""
        for diag in report.diagnostics:
            for rule in self.rules:
                match = rule.evaluate(diag)
                if match:
                    diag.rule_match = match
                    diag.category = rule.category
                    break
        return report
