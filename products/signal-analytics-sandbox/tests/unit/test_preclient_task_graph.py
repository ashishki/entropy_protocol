from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_preclient_phase_lists_reliable_artifact_contract() -> None:
    tasks = (PROJECT_ROOT / "docs/tasks.md").read_text(encoding="utf-8")
    plan = (PROJECT_ROOT / "docs/AI_DEVELOPMENT_PLAN_RU.md").read_text(encoding="utf-8")

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
    assert "Phase 37 - Pre-Client Artifact Hardening" in plan


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
