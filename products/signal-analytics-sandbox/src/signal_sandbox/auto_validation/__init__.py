"""Auto-validation evidence and validator contracts."""

from signal_sandbox.auto_validation.decision import (
    AutoValidationDecision,
    AutoValidationDecisionState,
    decide_auto_validation,
)
from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    ExtractedSetupFields,
    MarketWindowRef,
    ModelExtractionSpan,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.auto_validation.post_factum import (
    AUTO_REJECTED_FOR_PREDICTIVE_METRICS,
    POST_FACTUM_RISK,
    PostFactumCueEvidence,
    detect_post_factum_cues,
)
from signal_sandbox.auto_validation.provider_eligibility import (
    validate_provider_eligibility,
)
from signal_sandbox.auto_validation.results import (
    ValidationAuditLog,
    ValidationResult,
    ValidationStatus,
)
from signal_sandbox.auto_validation.setup_consistency import validate_setup_consistency
from signal_sandbox.auto_validation.timing import (
    FAILED_POST_FACTUM_OR_LATE,
    TimingOutcomeEvidence,
    TimingOutcomeKind,
    validate_pre_outcome_timing,
)

__all__ = [
    "AutoValidationEvidenceBundle",
    "AutoValidationDecision",
    "AutoValidationDecisionState",
    "EvidenceRef",
    "ExtractedSetupFields",
    "MarketWindowRef",
    "ModelExtractionSpan",
    "SourceClass",
    "TradeDirection",
    "AUTO_REJECTED_FOR_PREDICTIVE_METRICS",
    "POST_FACTUM_RISK",
    "PostFactumCueEvidence",
    "ValidationAuditLog",
    "ValidationResult",
    "ValidationStatus",
    "validate_provider_eligibility",
    "validate_setup_consistency",
    "FAILED_POST_FACTUM_OR_LATE",
    "TimingOutcomeEvidence",
    "TimingOutcomeKind",
    "detect_post_factum_cues",
    "decide_auto_validation",
    "validate_pre_outcome_timing",
]
