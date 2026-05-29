from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_phase37_preclient_review_records_internal_hardening_decision() -> None:
    review = _read("docs/archive/PHASE37_PRECLIENT_REVIEW.md")

    assert "Phase 37 completion: PASS" in review
    assert "Decision: `continue_internal_hardening`" in review
    assert "Client/buyer conversations: not approved" in review
    assert "No P0/P1/P2 implementation findings were found" in review
    for blocker in (
        "`0 operator_accepted_media_claims`",
        "`0 dashboard_safe_rr_rows`",
        "`0 market_outcome_recomputed_candidates`",
    ):
        assert blocker in review


def test_phase37_preclient_review_checks_required_boundaries() -> None:
    review = _read("docs/archive/PHASE37_PRECLIENT_REVIEW.md")

    for required in (
        "Artifact traceability | PASS_WITH_LIMITS",
        "Report fairness | PASS_WITH_LIMITS",
        "Dashboard safety | PASS",
        "Model/human boundary | PASS",
        "Outcome correctness | PASS_WITH_BLOCKERS",
        "Buyer-promise clarity | PASS",
        "Start Phase 38: Client-readiness evidence acceptance.",
    ):
        assert required in review


def test_phase37_preclient_review_is_indexed_and_routes_phase38() -> None:
    audit_index = _read("docs/audit/AUDIT_INDEX.md")
    tasks = _read("docs/tasks.md")
    prompt = _read("docs/CODEX_PROMPT.md")

    schedule_row = (
        "| 28 | Phase 37 | 2026-05-23 | "
        "SAS-PRECLIENT-001-SAS-PRECLIENT-010 | No | 0 | 0 | 0 |"
    )

    assert schedule_row in audit_index
    assert (
        "| 28 | `docs/archive/PHASE37_PRECLIENT_REVIEW.md` | Phase 37 | OK |"
        in audit_index
    )
    assert "## Phase 38 — Client-Readiness Evidence Acceptance" in tasks
    assert "SAS-CLIENTREADY-001: Operator Media Acceptance Ledger" in tasks
    assert "Phase 37 decision: `continue_internal_hardening`" in prompt
