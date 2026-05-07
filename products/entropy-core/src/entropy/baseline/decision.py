"""Phase 1J/K research decision and closure packets."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from entropy.baseline.report import Phase1IEvaluationReport

PHASE1J_RESEARCH_DECISION_ID = "PHASE1J-RESEARCH-DECISION-v1"
PHASE1K_RESEARCH_CLOSURE_PACKET_ID = "PHASE1K-ARCHIVE-ONLY-CLOSURE-PACKET-v1"


@dataclass(frozen=True)
class Phase1JResearchDecision:
    """No-capital research decision after the first report packet."""

    decision_id: str
    report_hash: str
    decision: str
    holdout_gate_opened: bool
    reason_code: str
    no_claim_labels: tuple[str, ...]
    production_label: bool = False
    capital_ready_label: bool = False
    phase_gate_evidence: bool = False


@dataclass(frozen=True)
class Phase1KClosurePacket:
    """Final archive-only closure packet for the D-K block."""

    packet_id: str
    decision_id: str
    report_hash: str
    closure_status: str
    deep_review_required_next: bool
    no_claim_labels: tuple[str, ...]
    holdout_executed: bool = False
    production_label: bool = False
    capital_ready_label: bool = False


def build_phase1j_research_decision(report: Phase1IEvaluationReport) -> Phase1JResearchDecision:
    """Decide the research state without opening holdout or production claims."""
    if (
        report.performance_conclusion
        or report.holdout_used
        or report.phase_gate_evidence
        or report.production_label
        or report.capital_ready_label
        or report.oos_label
    ):
        raise ValueError("Phase 1J decision requires a no-claim report")
    return Phase1JResearchDecision(
        decision_id=PHASE1J_RESEARCH_DECISION_ID,
        report_hash=report.report_hash,
        decision="archive_only_research_packet_complete_no_holdout_request",
        holdout_gate_opened=False,
        reason_code="NO_PERFORMANCE_CONCLUSION_FOR_HOLDOUT",
        no_claim_labels=(
            "research_decision_only",
            "holdout_not_opened",
            "not_production",
            "not_capital_ready",
        ),
    )


def build_phase1k_closure_packet(
    decision: Phase1JResearchDecision,
) -> Phase1KClosurePacket:
    """Close the archive-only D-K block without holdout execution."""
    if decision.holdout_gate_opened:
        raise ValueError("Phase 1K no-holdout closure requires holdout gate to remain closed")
    return Phase1KClosurePacket(
        packet_id=PHASE1K_RESEARCH_CLOSURE_PACKET_ID,
        decision_id=decision.decision_id,
        report_hash=decision.report_hash,
        closure_status="ARCHIVE_ONLY_DK_BLOCK_COMPLETE_DEEP_REVIEW_REQUIRED",
        deep_review_required_next=True,
        no_claim_labels=(
            "archive_only_closure",
            "holdout_not_executed",
            "deep_review_required",
            "not_production",
            "not_capital_ready",
        ),
    )


def phase1j_decision_hash(decision: Phase1JResearchDecision) -> str:
    """Hash a Phase 1J decision."""
    return _hash_payload(decision.__dict__)


def phase1k_closure_hash(packet: Phase1KClosurePacket) -> str:
    """Hash a Phase 1K closure packet."""
    return _hash_payload(packet.__dict__)


def _hash_payload(payload: object) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
