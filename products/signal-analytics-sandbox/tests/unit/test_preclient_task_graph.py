from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = PROJECT_ROOT / "docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md"


def test_preclient_phase_lists_reliable_artifact_contract() -> None:
    tasks = (PROJECT_ROOT / "docs/tasks.md").read_text(encoding="utf-8")
    plan = (PROJECT_ROOT / "docs/AI_DEVELOPMENT_PLAN_RU.md").read_text(encoding="utf-8")
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    assert "## Phase 37 — Pre-Client Artifact Hardening" in tasks
    assert "SAS-PRECLIENT-001: Product Artifact Contract And Reliability Bar" in tasks
    assert "docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md" in tasks
    for status in (
        "draft",
        "model_reviewed",
        "operator_reviewed",
        "market_validated",
        "dashboard_safe",
        "paid_report_safe",
        "blocked",
    ):
        assert status in tasks
        assert status in contract
    assert "Phase 37 - Pre-Client Artifact Hardening" in plan
    assert "Required Artifact Inventory" in contract
    assert "Allowed audience" in contract


def test_preclient_phase_covers_all_before_client_artifacts() -> None:
    tasks = (PROJECT_ROOT / "docs/tasks.md").read_text(encoding="utf-8")

    for task_id in (
        "SAS-PRECLIENT-001",
        "SAS-PRECLIENT-002",
        "SAS-PRECLIENT-003",
        "SAS-PRECLIENT-004",
        "SAS-PRECLIENT-005",
        "SAS-PRECLIENT-006",
        "SAS-PRECLIENT-007",
        "SAS-PRECLIENT-008",
        "SAS-PRECLIENT-009",
        "SAS-PRECLIENT-010",
    ):
        assert task_id in tasks

    for artifact in (
        "preclient_MODEL_REVIEW_PACKET",
        "preclient_EVIDENCE_APPENDIX",
        "preclient_FREE_DASHBOARD_CARDS",
        "PAID_STYLE_DEMO_REPORT",
        "preclient_CANDIDATE_OUTCOMES",
        "preclient_dashboard/index.html",
        "preclient_ARTIFACT_SAFETY_GATE",
        "PHASE37_PRECLIENT_REVIEW",
    ):
        assert artifact in tasks


def test_preclient_phase_preserves_customer_safety_gates() -> None:
    tasks = (PROJECT_ROOT / "docs/tasks.md").read_text(encoding="utf-8")
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    for required in (
        "pre-client",
        "model reviewers do not replace human/operator acceptance",
        "no-advice",
        "future-profit",
        "private-channel analysis",
        "start outreach",
        "customer-facing",
    ):
        assert required in tasks

    for required in (
        "A model reviewer",
        "cannot directly promote",
        "Transcript/OCR/chart claims remain",
        "Gate 5 - Wording Safety",
        "buy/sell/hold recommendations",
        "future-profit language",
        "best/worst channel ranking",
        "private-source access promises",
        "ready for discovery",
    ):
        assert required in contract


def test_preclient_artifact_contract_covers_dashboard_and_paid_report_boundaries() -> (
    None
):
    contract = CONTRACT_PATH.read_text(encoding="utf-8")

    for section in (
        "Free Dashboard Card Contract",
        "Paid Deep Report Contract",
        "Pre-Client Done Criteria",
        "Explicit Non-Goals",
    ):
        assert section in contract

    for required in (
        "source_id",
        "what_it_is",
        "setup_rr_status",
        "media_coverage_summary",
        "evidence_confidence",
        "gate_status",
        "full evidence appendix",
        "post-factum vs forward-looking distinction",
        "proceed_to_client_discovery",
        "continue_internal_hardening",
        "pivot_scope",
    ):
        assert required in contract
