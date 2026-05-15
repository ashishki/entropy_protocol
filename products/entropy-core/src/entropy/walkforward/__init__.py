"""Walk-forward package."""

from entropy.walkforward.embargo import (
    PURGE_EMBARGO_METHOD_ID,
    PurgeEmbargoResult,
    PurgeEmbargoSpec,
    derive_embargo_bars,
)
from entropy.walkforward.leakage import (
    CheckStatus,
    FeatureAudit,
    LeakageCheckResult,
    LeakageReport,
    OOSLabel,
    OOSLabelBlockedError,
    OptimizationAudit,
    RegimeLabelAudit,
    UniverseSelectionAudit,
    create_oos_label,
    run_checklist,
)
from entropy.walkforward.runner import (
    IncompleteRunRecordError,
    LeakageBlockError,
    WalkForwardRunnerError,
    WalkForwardStrategy,
    run_walk_forward,
)
from entropy.walkforward.splitter import LeakageError, SplitResult, split
from entropy.walkforward.temporal_shuffle import (
    TEMPORAL_SHUFFLE_METHOD_ID,
    TemporalShuffleAuditResult,
    reverse_oos_window,
    run_temporal_shuffle_audit,
)

__all__ = [
    "CheckStatus",
    "FeatureAudit",
    "IncompleteRunRecordError",
    "LeakageBlockError",
    "LeakageError",
    "LeakageCheckResult",
    "LeakageReport",
    "OOSLabel",
    "OOSLabelBlockedError",
    "OptimizationAudit",
    "PURGE_EMBARGO_METHOD_ID",
    "PurgeEmbargoResult",
    "PurgeEmbargoSpec",
    "RegimeLabelAudit",
    "SplitResult",
    "TEMPORAL_SHUFFLE_METHOD_ID",
    "TemporalShuffleAuditResult",
    "UniverseSelectionAudit",
    "WalkForwardRunnerError",
    "WalkForwardStrategy",
    "create_oos_label",
    "derive_embargo_bars",
    "reverse_oos_window",
    "run_checklist",
    "run_temporal_shuffle_audit",
    "run_walk_forward",
    "split",
]
