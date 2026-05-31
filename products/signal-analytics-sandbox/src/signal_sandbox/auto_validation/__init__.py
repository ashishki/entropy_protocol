"""Auto-validation evidence and validator contracts."""

from signal_sandbox.auto_validation.audit_export import (
    ValidationAuditExport,
    export_validation_audit_with_receipt,
    load_signal_auto_validation_receipt,
)
from signal_sandbox.auto_validation.core_receipt import (
    SignalAutoValidationProofReceipt,
    SignalProofEvidenceRef,
    build_signal_auto_validation_receipt,
)
from signal_sandbox.auto_validation.customer_policy import (
    CustomerPolicyInput,
    evaluate_customer_policy,
)
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
    "AUTO_REJECTED_FOR_PREDICTIVE_METRICS",
    "FAILED_POST_FACTUM_OR_LATE",
    "POST_FACTUM_RISK",
    "AutoValidationDecision",
    "AutoValidationDecisionState",
    "AutoValidationEvidenceBundle",
    "CustomerPolicyInput",
    "EvidenceRef",
    "ExtractedSetupFields",
    "MarketWindowRef",
    "ModelExtractionSpan",
    "PostFactumCueEvidence",
    "SignalAutoValidationProofReceipt",
    "SignalProofEvidenceRef",
    "SourceClass",
    "TimingOutcomeEvidence",
    "TimingOutcomeKind",
    "TradeDirection",
    "ValidationAuditExport",
    "ValidationAuditLog",
    "ValidationResult",
    "ValidationStatus",
    "build_signal_auto_validation_receipt",
    "decide_auto_validation",
    "detect_post_factum_cues",
    "evaluate_customer_policy",
    "export_validation_audit_with_receipt",
    "load_signal_auto_validation_receipt",
    "validate_pre_outcome_timing",
    "validate_provider_eligibility",
    "validate_setup_consistency",
]
