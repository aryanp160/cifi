import re
from typing import Optional
from cifi.models import DiagnosticItem, FailureCategory, RuleMatchMetadata
from cifi.rules.base import Rule


class CompilationErrorRule(Rule):
    rule_id = "R001"
    name = "Compilation or Syntax Error"
    description = "Source code contains syntax errors or failed compilation."
    category = FailureCategory.COMPILATION_ERROR
    remediation = "Check syntax at reported file location and verify imports/types."

    REGEX = re.compile(
        r"(SyntaxError|TypeError|NameError|compilation failed|error\[E\d+\]|compile error)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
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
    remediation = "Install missing package or add to pyproject.toml / package.json / Cargo.toml."

    REGEX = re.compile(
        r"(ModuleNotFoundError|No module named|Cannot find module|package not found|Could not resolve dependency|ImportError)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
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
    remediation = "Inspect test assertion expectations vs actual return values."

    REGEX = re.compile(
        r"(AssertionError|assert |Expected:|Jest Test Failure|Pytest Failure|Test failed)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
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
    remediation = "Increase job timeout in CI config or optimize slow blocking operations."

    REGEX = re.compile(
        r"(timed out|TimeoutError|Job cancelled after|SIGKILL|exceeded maximum time)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
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
    remediation = "Verify file read/write permissions or update secret access tokens."

    REGEX = re.compile(
        r"(PermissionDenied|EACCES|Access is denied|Unauthorized|403 Forbidden|Authentication failed)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
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
    remediation = "Verify path exists or add build step to generate required file."

    REGEX = re.compile(
        r"(FileNotFoundError|ENOENT|No such file or directory|file not found)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.95,
            )
        return None


class MemoryExceededRule(Rule):
    rule_id = "R007"
    name = "Memory Exceeded / Out of Memory"
    description = "Process ran out of RAM / heap memory space."
    category = FailureCategory.MEMORY_EXCEEDED
    remediation = "Increase memory limits on CI worker runner or optimize memory allocations."

    REGEX = re.compile(
        r"(Out of memory|MemoryError|OOMKilled|JavaScript heap out of memory|malloc failed|std::bad_alloc)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.96,
            )
        return None


class NetworkConnectionRule(Rule):
    rule_id = "R008"
    name = "Network Connection Failure"
    description = "Remote server unreachable, socket connection refused, or DNS lookup failed."
    category = FailureCategory.NETWORK_ERROR
    remediation = "Verify network connectivity, proxy settings, or remote host availability."

    REGEX = re.compile(
        r"(ECONNREFUSED|Connection refused|Could not resolve host|DNS resolution failed|socket.gaierror|ETIMEDOUT)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.94,
            )
        return None


class DatabaseMigrationRule(Rule):
    rule_id = "R009"
    name = "Database Schema / Migration Issue"
    description = "Missing database table, unapplied migrations, or column schema drift."
    category = FailureCategory.DATABASE_MIGRATION
    remediation = "Run database migration scripts (e.g. alembic upgrade head / prisma db push) before tests."

    REGEX = re.compile(
        r"(MigrationError|PendingMigrationConnection|relation \".*?\" does not exist|Table '.*?' doesn't exist|alembic.util.exc.CommandError)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.95,
            )
        return None


class EnvironmentVariableRule(Rule):
    rule_id = "R010"
    name = "Missing Environment Variable"
    description = "Required environment variable or secret key is uninitialized or missing."
    category = FailureCategory.ENVIRONMENT_VARIABLE
    remediation = "Set missing environment variable in CI secrets / .env configuration."

    REGEX = re.compile(
        r"(KeyError:\s*['\"][A-Z0-9_]+['\"]|missing required environment variable|Environment variable \w+ is not set)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.93,
            )
        return None


class TypeMismatchRule(Rule):
    rule_id = "R011"
    name = "Type Mismatch Error"
    description = "Operation or function received an incompatible object type."
    category = FailureCategory.TYPE_MISMATCH
    remediation = "Check type annotations, function signature parameters, and type conversions."

    REGEX = re.compile(
        r"(TypeError:|ClassCastException|cannot convert|type mismatch|is not assignable)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.92,
            )
        return None


class LockTimeoutRule(Rule):
    rule_id = "R012"
    name = "Lock or Resource Deadlock"
    description = "Process failed to acquire file lock or database row lock in time."
    category = FailureCategory.LOCK_TIMEOUT
    remediation = "Clear stale lock files or ensure concurrent job processes release database/file locks."

    REGEX = re.compile(
        r"(LockTimeout|DeadlockDetected|could not obtain lock|database is locked|FileLockException)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.91,
            )
        return None


class DockerContainerRule(Rule):
    rule_id = "R013"
    name = "Docker Container Failure"
    description = "Docker daemon error, container exit code 137, or Dockerfile build syntax error."
    category = FailureCategory.DOCKER_ERROR
    remediation = "Check Dockerfile build syntax, container memory limits (exit 137), or image repository credentials."

    REGEX = re.compile(
        r"(container exit code 137|ImagePullBackOff|docker: Error response from daemon|Dockerfile:\d+)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.95,
            )
        return None


class DiskSpaceRule(Rule):
    rule_id = "R014"
    name = "Disk Space Exhausted"
    description = "File system partition or disk quota has run out of free space."
    category = FailureCategory.DISK_SPACE
    remediation = "Clean temporary build artifacts or expand disk storage allocation on CI runner."

    REGEX = re.compile(
        r"(ENOSPC|No space left on device|disk quota exceeded)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.98,
            )
        return None


class DependencyConflictRule(Rule):
    rule_id = "R015"
    name = "Dependency Version Conflict"
    description = "Package manager found conflicting dependency version requirements."
    category = FailureCategory.DEPENDENCY_CONFLICT
    remediation = "Resolve package version pin constraints in lockfile or lock compatible package versions."

    REGEX = re.compile(
        r"(VersionConflict|Could not solve dependencies|Peer dependency unmet|conflict: \w+ requires \w+)",
        re.IGNORECASE,
    )

    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        text = f"{diag.summary} {diag.message}"
        if self.REGEX.search(text):
            diag.suggested_remediation = self.remediation
            return RuleMatchMetadata(
                rule_id=self.rule_id,
                rule_name=self.name,
                description=self.description,
                confidence=0.94,
            )
        return None
