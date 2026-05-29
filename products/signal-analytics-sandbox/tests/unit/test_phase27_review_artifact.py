from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_phase27_review_archive_records_v1_closure_and_gate() -> None:
    review = (PROJECT_ROOT / "docs/archive/PHASE27_REVIEW.md").read_text(
        encoding="utf-8"
    )

    assert "Phase 27 completion: PASS" in review
    assert "Gate decision: `approve_internal_only`" in review
    assert "External/customer-facing delivery: not approved" in review
    assert "No P0/P1/P2 implementation findings were found" in review


def test_phase27_review_is_indexed() -> None:
    audit_index = (PROJECT_ROOT / "docs/audit/AUDIT_INDEX.md").read_text(
        encoding="utf-8"
    )

    schedule_row = (
        "| 27 | Phase 27 | 2026-05-19 | SAS-V1-001-SAS-V1-009 | No | 0 | 0 | 0 |"
    )

    assert schedule_row in audit_index
    assert "| 27 | `docs/archive/PHASE27_REVIEW.md` | Phase 27 | OK |" in audit_index
