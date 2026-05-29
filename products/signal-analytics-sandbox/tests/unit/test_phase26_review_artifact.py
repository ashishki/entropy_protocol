from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_phase26_review_archive_records_required_boundaries() -> None:
    review = (PROJECT_ROOT / "docs/archive/PHASE26_REVIEW.md").read_text(
        encoding="utf-8"
    )

    assert "Phase 26 completion: PASS" in review
    assert "External/customer-facing delivery: still blocked" in review
    assert "Public-source boundary | PASS" in review
    assert "Market-data posture | PASS" in review
    assert "No P0/P1/P2 implementation findings were found" in review


def test_phase26_review_is_indexed() -> None:
    audit_index = (PROJECT_ROOT / "docs/audit/AUDIT_INDEX.md").read_text(
        encoding="utf-8"
    )

    schedule_row = (
        "| 26 | Phase 26 | 2026-05-19 | SAS-ER-000-SAS-ER-006 | No | 0 | 0 | 0 |"
    )

    assert schedule_row in audit_index
    assert "| 26 | `docs/archive/PHASE26_REVIEW.md` | Phase 26 | OK |" in audit_index
