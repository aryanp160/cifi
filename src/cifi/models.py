from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class FailureCategory(str, Enum):
    COMPILATION_ERROR = "compilation_error"
    ASSERTION_FAILURE = "assertion_failure"
    MISSING_DEPENDENCY = "missing_dependency"
    TIMEOUT = "timeout"
    PERMISSION_DENIED = "permission_denied"
    FILE_NOT_FOUND = "file_not_found"
    SYNTAX_ERROR = "syntax_error"
    MEMORY_EXCEEDED = "memory_exceeded"
    NETWORK_ERROR = "network_error"
    DATABASE_MIGRATION = "database_migration"
    ENVIRONMENT_VARIABLE = "environment_variable"
    TYPE_MISMATCH = "type_mismatch"
    LOCK_TIMEOUT = "lock_timeout"
    DOCKER_ERROR = "docker_error"
    DISK_SPACE = "disk_space"
    DEPENDENCY_CONFLICT = "dependency_conflict"
    UNKNOWN_FAILURE = "unknown_failure"


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class CodeLocation(BaseModel):
    file_path: Optional[str] = Field(None, description="Path to the source file where failure occurred")
    line_number: Optional[int] = Field(None, description="Line number of the failure")
    column_number: Optional[int] = Field(None, description="Column number if available")
    function_name: Optional[str] = Field(None, description="Name of the function or test case")


class LogContext(BaseModel):
    raw_lines: List[str] = Field(default_factory=list, description="Raw log lines surrounding the error")
    line_start_index: int = Field(0, description="0-indexed line number where context starts")
    line_end_index: int = Field(0, description="0-indexed line number where context ends")


class RuleMatchMetadata(BaseModel):
    rule_id: str = Field(..., description="Unique ID of the triggered rule")
    rule_name: str = Field(..., description="Human readable rule name")
    description: str = Field("", description="Rule description / root cause hint")
    confidence: float = Field(1.0, ge=0.0, le=1.0, description="Confidence score of the match")


class DiagnosticItem(BaseModel):
    category: FailureCategory = Field(FailureCategory.UNKNOWN_FAILURE, description="Categorized type of failure")
    severity: Severity = Field(Severity.ERROR, description="Diagnostic severity level")
    summary: str = Field(..., description="Short single-line description of the error")
    message: str = Field("", description="Detailed error message or stack trace string")
    location: Optional[CodeLocation] = Field(None, description="Extracted code location")
    context: Optional[LogContext] = Field(None, description="Log line context block")
    rule_match: Optional[RuleMatchMetadata] = Field(None, description="Matched rule metadata")
    suggested_remediation: Optional[str] = Field(None, description="Actionable deterministic remediation hint")


class CIFailureReport(BaseModel):
    log_source: str = Field("unknown", description="Source filename, pipeline name, or stream identifier")
    parser_type: str = Field("generic", description="Parser engine used (e.g. github_actions, pytest, cargo)")
    total_lines_parsed: int = Field(0, ge=0, description="Total number of lines ingested")
    diagnostics: List[DiagnosticItem] = Field(default_factory=list, description="Extracted diagnostic findings")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary custom execution metadata")
    execution_time_ms: Optional[float] = Field(None, description="Pipeline execution duration in milliseconds")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Report generation timestamp")

    @property
    def has_failures(self) -> bool:
        return any(d.severity == Severity.ERROR for d in self.diagnostics)

    @property
    def failure_count(self) -> int:
        return sum(1 for d in self.diagnostics if d.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for d in self.diagnostics if d.severity == Severity.WARNING)

    @property
    def diagnosed_count(self) -> int:
        return sum(1 for d in self.diagnostics if d.category != FailureCategory.UNKNOWN_FAILURE)
