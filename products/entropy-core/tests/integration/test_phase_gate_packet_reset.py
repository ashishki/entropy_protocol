"""Reset-era phase-gate evidence packet tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from entropy.evidence import EvidenceCollectionError, build_phase_gate_evidence_packet

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_INDEX = PROJECT_ROOT / "docs" / "EVIDENCE_INDEX.md"


def test_phase_gate_packet_contains_required_sections() -> None:
    packet = build_phase_gate_evidence_packet(
        phase=3,
        phase_name="Evaluation Safety",
        phase_gate_id="phase-3-evaluation-safety",
        baseline="311 passed, 20 skipped",
        task_results={"T08": True, "T09": True, "T10": True, "T11": True},
        evidence_index_path=EVIDENCE_INDEX,
        project_root=PROJECT_ROOT,
    )
    markdown = packet.to_markdown()

    assert packet.phase_gate_status == "NOT_APPROVED"
    assert "## Required Human Approvals" in markdown
    assert "phase_gate:phase-3-evaluation-safety" in markdown
    assert "holdout_access:archive_holdout" in markdown
    assert "## Blocked Claim Surfaces" in markdown
    assert "OOS/performance approval: BLOCKED" in markdown
    assert "production approval: BLOCKED" in markdown
    assert "capital-ready approval: BLOCKED" in markdown
    assert "## Evidence Rows" in markdown
    assert "T07 Governance Approval Gate Audit" in markdown
    assert "T08 Data and Leakage Gate Verification" in markdown
    assert "T09 SimBroker and Cost Surface Regression" in markdown
    assert "T10 Attribution Stream Boundary Audit" in markdown
    assert "T11 Phase-Gate Evidence Packet" in markdown
    assert "Baseline: 311 passed, 20 skipped" in markdown


def test_phase_gate_packet_fails_missing_evidence(tmp_path: Path) -> None:
    evidence_index = tmp_path / "EVIDENCE_INDEX.md"
    evidence_index.write_text(
        "\n".join(
            [
                "# Evidence Index",
                "",
                "## Evidence Table",
                "",
                "| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |",
                "|------------------------|---------------|----------|---------------|---------------|------------|",
                "| T10 Attribution Stream Boundary Audit | Test result | `tests/unit/missing_attribution_reset.py::test_missing` | missing artifact | 2026-05-07 | Yes |",
                "",
                "## Pending Evidence",
                "",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(EvidenceCollectionError, match="Missing evidence artifact"):
        build_phase_gate_evidence_packet(
            phase=3,
            phase_name="Evaluation Safety",
            phase_gate_id="phase-3-evaluation-safety",
            baseline="311 passed, 20 skipped",
            task_results={"T10": True},
            evidence_index_path=evidence_index,
            project_root=PROJECT_ROOT,
            required_evidence_topics=("T10 Attribution Stream Boundary Audit",),
        )


def test_phase_gate_packet_blocks_unapproved_claim_labels() -> None:
    packet = build_phase_gate_evidence_packet(
        phase=3,
        phase_name="Evaluation Safety",
        phase_gate_id="phase-3-evaluation-safety",
        baseline="311 passed, 20 skipped",
        task_results={"T08": True, "T09": True, "T10": True, "T11": True},
        approval_records=(),
        evidence_index_path=EVIDENCE_INDEX,
        project_root=PROJECT_ROOT,
    )
    markdown = packet.to_markdown()

    assert packet.phase_gate_status == "NOT_APPROVED"
    assert packet.phase_gate_reason_code == "MISSING_HUMAN_PHASE_GATE_APPROVAL"
    assert {surface.status for surface in packet.blocked_claim_surfaces} == {"BLOCKED"}
    assert "OOS/performance approval: APPROVED" not in markdown
    assert "production approval: APPROVED" not in markdown
    assert "capital-ready approval: APPROVED" not in markdown
    assert "Phase gate approval: APPROVED" not in markdown
