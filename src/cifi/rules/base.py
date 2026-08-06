from abc import ABC, abstractmethod
from typing import Optional
from cifi.models import DiagnosticItem, FailureCategory, RuleMatchMetadata


class Rule(ABC):
    """Abstract base class for failure rule matchers."""

    rule_id: str
    name: str
    description: str
    category: FailureCategory

    @abstractmethod
    def evaluate(self, diag: DiagnosticItem) -> Optional[RuleMatchMetadata]:
        """Evaluate a diagnostic item and return RuleMatchMetadata if triggered."""
        pass
