import re
from cifi.models import DiagnosticItem, FailureCategory, Language, Framework


class FingerprintGenerator:
    """Generates human-readable, deterministic Failure Fingerprints (e.g. PYTHON-IMPORT-UV-001)."""

    @classmethod
    def generate(cls, diag: DiagnosticItem, language: Language, framework: Framework) -> str:
        lang_code = language.value.upper() if language != Language.GENERIC else "GENERIC"
        cat_code = diag.category.value.upper().replace("_", "-")

        # Specific Fingerprint Overrides
        msg = f"{diag.summary} {diag.message}".lower()

        if language == Language.PYTHON:
            if "uv" in msg or framework == Framework.UV:
                if diag.category == FailureCategory.MISSING_DEPENDENCY:
                    return "PYTHON-IMPORT-UV-001"
            elif "pytest" in msg or framework == Framework.PYTEST:
                if diag.category == FailureCategory.ASSERTION_FAILURE:
                    return "PYTEST-ASSERTION-001"
            if diag.category == FailureCategory.MISSING_DEPENDENCY:
                return "PYTHON-IMPORT-PIP-002"
        elif language == Language.NODE:
            if "jest" in msg or framework == Framework.JEST:
                if diag.category == FailureCategory.ASSERTION_FAILURE:
                    return "JEST-ASSERTION-001"
            if diag.category == FailureCategory.MISSING_DEPENDENCY:
                return "NODE-MODULE-MISSING-001"

        if diag.category == FailureCategory.MEMORY_EXCEEDED:
            return "SYS-MEMORY-OOM-001"
        elif diag.category == FailureCategory.NETWORK_ERROR:
            return "NET-CONNECTION-REFUSED-001"
        elif diag.category == FailureCategory.DATABASE_MIGRATION:
            return "DB-SCHEMA-MIGRATION-001"
        elif diag.category == FailureCategory.ENVIRONMENT_VARIABLE:
            return "ENV-SECRET-MISSING-001"
        elif diag.category == FailureCategory.DOCKER_ERROR:
            return "DOCKER-CONTAINER-EXIT-137"
        elif diag.category == FailureCategory.DISK_SPACE:
            return "SYS-DISK-ENOSPC-001"

        # Standard Fallback Fingerprint
        rule_id = diag.rule_match.rule_id if diag.rule_match else "R000"
        return f"{lang_code}-{cat_code}-{rule_id}"
