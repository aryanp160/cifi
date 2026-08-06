import re
from typing import Tuple
from cifi.models import Language, Framework


class EnvironmentDetector:
    """Detects primary language ecosystem (Python/Node) and test/tooling framework from raw log text."""

    PYTHON_KEYWORDS = re.compile(
        r"(\.py[:\s]|Traceback \(most recent call last\):|ModuleNotFoundError|ImportError|pytest|pyproject\.toml|uv\.lock|requirements\.txt|pip|poetry)",
        re.IGNORECASE,
    )
    NODE_KEYWORDS = re.compile(
        r"(\.(?:js|ts|jsx|tsx)[:\s]|npm ERR!|node_modules|FAIL src/|Jest|yarn\.lock|pnpm-lock\.yaml|package\.json)",
        re.IGNORECASE,
    )

    @classmethod
    def detect(cls, log_content: str) -> Tuple[Language, Framework]:
        """Detect language ecosystem and framework from raw log text."""
        py_matches = len(cls.PYTHON_KEYWORDS.findall(log_content))
        node_matches = len(cls.NODE_KEYWORDS.findall(log_content))

        language = Language.GENERIC
        if py_matches > node_matches and py_matches > 0:
            language = Language.PYTHON
        elif node_matches > py_matches and node_matches > 0:
            language = Language.NODE

        framework = Framework.GENERIC
        if language == Language.PYTHON:
            if "uv" in log_content or "uv.lock" in log_content:
                framework = Framework.UV
            elif "poetry" in log_content or "poetry.lock" in log_content:
                framework = Framework.POETRY
            elif "pytest" in log_content or "FAILED " in log_content:
                framework = Framework.PYTEST
            elif "pip" in log_content or "requirements.txt" in log_content:
                framework = Framework.PIP
        elif language == Language.NODE:
            if "Jest" in log_content or "FAIL " in log_content:
                framework = Framework.JEST
            elif "npm" in log_content or "package.json" in log_content:
                framework = Framework.NPM

        return language, framework
