from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_external_gate_rerun_records_internal_only_decision_and_blockers() -> None:
    gate = (
        PROJECT_ROOT / "docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md"
    ).read_text(encoding="utf-8")

    assert "Rerun: SAS-NEXT-004" in gate
    assert "Decision: approve_internal_only" in gate
    assert "not approved for external/customer-facing delivery" in gate
    assert (
        "Full review queue rows still need durable operator closure decisions" in gate
    )
    assert (
        "False-negative drafts are not scoreable customer-facing win/loss rows" in gate
    )


def test_external_gate_cites_required_phase_28_evidence_dimensions() -> None:
    gate = (
        PROJECT_ROOT / "docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md"
    ).read_text(encoding="utf-8")

    for required in (
        "Review coverage | partial",
        "Provider coverage | partial",
        "Multimodal posture | blocked",
        "RR/setup coverage | blocked",
        "Report wording safety | pass",
        "three_channel_FULL_REVIEW_QUEUE.json",
        "three_channel_FALSE_NEGATIVE_PASS.json",
        "three_channel_V1_REPORT_LANGUAGE_SAFETY.json",
    ):
        assert required in gate
