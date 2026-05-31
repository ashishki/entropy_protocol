"""Auto-validation evidence and validator contracts."""

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    ExtractedSetupFields,
    MarketWindowRef,
    ModelExtractionSpan,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.auto_validation.results import (
    ValidationAuditLog,
    ValidationResult,
    ValidationStatus,
)

__all__ = [
    "AutoValidationEvidenceBundle",
    "EvidenceRef",
    "ExtractedSetupFields",
    "MarketWindowRef",
    "ModelExtractionSpan",
    "SourceClass",
    "TradeDirection",
    "ValidationAuditLog",
    "ValidationResult",
    "ValidationStatus",
]
