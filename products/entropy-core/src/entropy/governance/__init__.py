"""Governance package."""

from entropy.governance.approval import (
    HoldoutAccessDecision,
    HumanApprovalRecord,
    PhaseGateReport,
    ProviderActivationContract,
    ProviderActivationDecision,
    authorize_holdout_access,
    build_phase_gate_report,
    evaluate_provider_activation,
)
from entropy.governance.state_machine import (
    GovernanceStateMachine,
    P1Config,
    P1StateMachine,
    P3Config,
    P3StateMachine,
    event_types,
)
from entropy.governance.p4_labeler import (
    P4_METHOD_ID,
    P4_PARAM_HASH,
    P4_WEEKLY_RESAMPLE_VERSION,
    P4Label,
    WeeklyBar,
    build_p4_weekly_bars,
    label_p4_regimes,
)

__all__ = [
    "GovernanceStateMachine",
    "HoldoutAccessDecision",
    "HumanApprovalRecord",
    "P1Config",
    "P1StateMachine",
    "P3Config",
    "P3StateMachine",
    "P4Label",
    "P4_METHOD_ID",
    "P4_PARAM_HASH",
    "P4_WEEKLY_RESAMPLE_VERSION",
    "PhaseGateReport",
    "ProviderActivationContract",
    "ProviderActivationDecision",
    "WeeklyBar",
    "authorize_holdout_access",
    "build_phase_gate_report",
    "build_p4_weekly_bars",
    "event_types",
    "evaluate_provider_activation",
    "label_p4_regimes",
]
