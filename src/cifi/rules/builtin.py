import re
from typing import Optional
from cifi.models import DiagnosticItem, FailureCategory, RuleMatchMetadata
from cifi.rules.base import Rule


class CompilationErrorRule(Rule):
    rule_id = "R001"
    name = "Compilation or Syntax Error"
    description = "Source code contains syntax errors or failed compilation."
    category = FailureCategory.COMPILATION_ERROR

    REGEX = re.compile(
        r"(SyntaxError|TypeError|NameError|compilation failed|error\[E\d+\]|compile error)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.95,
            )
        return None


class MissingDependencyRule(Rule):
    rule_id = "R002"
    name = "Missing Dependency"
    description = "Required package, module, or system dependency is missing."
    category = FailureCategory.MISSING_DEPENDENCY

    REGEX = re.compile(
        r"(ModuleNotFoundError|No module named|Cannot find module|package not found|Could not resolve dependency|ImportError)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.98,
            )
        return None


class AssertionFailureRule(Rule):
    rule_id = "R003"
    name = "Test Assertion Failure"
    description = "Automated test suite assertion or expectation failed."
    category = FailureCategory.ASSERTION_FAILURE

    REGEX = re.compile(
        r"(AssertionError|assert |Expected:|Jest Test Failure|Pytest Failure|Test failed)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.95,
            )
        return None


class TimeoutRule(Rule):
    rule_id = "R004"
    name = "Execution Timeout"
    description = "Job, step, or test process timed out before completion."
    category = FailureCategory.TIMEOUT

    REGEX = re.compile(
        r"(timed out|TimeoutError|Job cancelled after|SIGKILL|exceeded maximum time)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.90,
            )
        return None


class PermissionRule(Rule):
    rule_id = "R005"
    name = "Permission or Authentication Denied"
    description = "File system permission, API access token, or credentials issue."
    category = FailureCategory.PERMISSION_DENIED

    REGEX = re.compile(
        r"(PermissionDenied|EACCES|Access is denied|Unauthorized|403 Forbidden|Authentication failed)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.92,
            )
        return None


class FileNotFoundErrorRule(Rule):
    rule_id = "R006"
    name = "File Not Found"
    description = "Target file or directory path does not exist."
    category = FailureCategory.FILE_NOT_FOUND

    REGEX = re.compile(
        r"(FileNotFoundError|ENOENT|No such file or directory|file not found)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.95,
            )
        return None
