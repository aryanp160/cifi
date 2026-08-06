import re
from typing import Optional
from cifi.models import (
    DiagnosticItem,
    FailureCategory,
    RuleMatchMetadata,
    RulePriority,
    ExplainabilityBlock,
    Language,
    Framework,
)
from cifi.rules.base import Rule
from cifi.intelligence.fingerprints import FingerprintGenerator


class CompilationErrorRule(Rule):
    rule_id = "R001"
    name = "Compilation or Syntax Error"
    description = "Source code contains syntax errors or failed compilation."
    category = FailureCategory.COMPILATION_ERROR
    priority = RulePriority.CRITICAL
    remediation = "Check syntax at reported file location and verify imports/types."

    REGEX = re.compile(
        r"(SyntaxError|TypeError|NameError|compilation failed|error\[E\d+\]|compile error)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        match = self.REGEX.search(text)
        if match:
            keyword = match.group(0)
            diag.suggested_remediation = self.remediation
            diag.confidence_score = 0.96
            diag.explainability = ExplainabilityBlock(
                rule_id=self.rule_id,
                matched_expression=keyword,
                stack_keyword=keyword,
                reason="Source file syntax parser encountered an unparseable token or type error.",
            )
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.96,
                priority=self.priority,
            )
        return None


class MissingDependencyRule(Rule):
    rule_id = "R002"
    name = "Missing Dependency"
    description = "Required package, module, or system dependency is missing."
    category = FailureCategory.MISSING_DEPENDENCY
    priority = RulePriority.HIGH
    remediation = "Install missing package or add to pyproject.toml / package.json."

    REGEX = re.compile(
        r"(ModuleNotFoundError|No module named|Cannot find module|package not found|Could not resolve dependency|ImportError)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        match = self.REGEX.search(text)
        if match:
            keyword = match.group(0)
            diag.suggested_remediation = self.remediation
            diag.confidence_score = 0.98
            diag.explainability = ExplainabilityBlock(
                rule_id=self.rule_id,
                matched_expression=keyword,
                stack_keyword=keyword,
                reason="Import statement referenced a module that is not installed in the execution environment or lockfile.",
            )
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.98,
                priority=self.priority,
            )
        return None


class AssertionFailureRule(Rule):
    rule_id = "R003"
    name = "Test Assertion Failure"
    description = "Automated test suite assertion or expectation failed."
    category = FailureCategory.ASSERTION_FAILURE
    priority = RulePriority.HIGH
    remediation = "Inspect test assertion expectations vs actual return values."

    REGEX = re.compile(
        r"(AssertionError|assert |Expected:|Jest Test Failure|Pytest Failure|Test failed)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        match = self.REGEX.search(text)
        if match:
            keyword = match.group(0)
            diag.suggested_remediation = self.remediation
            diag.confidence_score = 0.95
            diag.explainability = ExplainabilityBlock(
                rule_id=self.rule_id,
                matched_expression=keyword,
                stack_keyword=keyword,
                reason="Test framework evaluated an assertion condition that evaluated to False / mismatched expected output.",
            )
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.95,
                priority=self.priority,
            )
        return None


class MemoryExceededRule(Rule):
    rule_id = "R007"
    name = "Memory Exceeded / Out of Memory"
    description = "Process ran out of RAM / heap memory space."
    category = FailureCategory.MEMORY_EXCEEDED
    priority = RulePriority.CRITICAL
    remediation = "Increase memory limits on CI worker runner or optimize memory allocations."

    REGEX = re.compile(
        r"(Out of memory|MemoryError|OOMKilled|JavaScript heap out of memory|malloc failed|std::bad_alloc)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        match = self.REGEX.search(text)
        if match:
            keyword = match.group(0)
            diag.suggested_remediation = self.remediation
            diag.confidence_score = 0.98
            diag.explainability = ExplainabilityBlock(
                rule_id=self.rule_id,
                matched_expression=keyword,
                stack_keyword=keyword,
                reason="Process heap or RAM allocation exceeded host system or container memory limit.",
            )
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.98,
                priority=self.priority,
            )
        return None


class EnvironmentVariableRule(Rule):
    rule_id = "R010"
    name = "Missing Environment Variable"
    description = "Required environment variable or secret key is uninitialized or missing."
    category = FailureCategory.ENVIRONMENT_VARIABLE
    priority = RulePriority.HIGH
    remediation = "Set missing environment variable in CI secrets / .env configuration."

    REGEX = re.compile(
        r"(KeyError:\s*['\"][A-Z0-9_]+['\"]|missing required environment variable|Environment variable \w+ is not set)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        match = self.REGEX.search(text)
        if match:
            keyword = match.group(0)
            diag.suggested_remediation = self.remediation
            diag.confidence_score = 0.94
            diag.explainability = ExplainabilityBlock(
                rule_id=self.rule_id,
                matched_expression=keyword,
                stack_keyword=keyword,
                reason="Application attempted to access an environment key that is undefined in execution context.",
            )
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.94,
                priority=self.priority,
            )
        return None


class TimeoutRule(Rule):
    rule_id = "R004"
    name = "Execution Timeout"
    description = "Job, step, or test process timed out before completion."
    category = FailureCategory.TIMEOUT
    priority = RulePriority.MEDIUM
    remediation = "Increase job timeout in CI config or optimize slow blocking operations."

    REGEX = re.compile(
        r"(timed out|TimeoutError|Job cancelled after|SIGKILL|exceeded maximum time)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        match = self.REGEX.search(text)
        if match:
            keyword = match.group(0)
            diag.suggested_remediation = self.remediation
            diag.confidence_score = 0.90
            diag.explainability = ExplainabilityBlock(
                rule_id=self.rule_id,
                matched_expression=keyword,
                stack_keyword=keyword,
                reason="Execution elapsed time exceeded maximum allocated pipeline step limit.",
            )
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.90,
                priority=self.priority,
            )
        return None
