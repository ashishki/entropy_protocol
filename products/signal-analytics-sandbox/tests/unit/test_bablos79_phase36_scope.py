from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_phase36_scope_records_current_bablos_limitations() -> None:
    scope = (
        PROJECT_ROOT / "docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md"
    ).read_text(encoding="utf-8")

    for required in (
        "60",
        "about 9 days",
        "2",
        "0 source-linked image/OCR artifacts",
        "14 reviewable non-blocker rows",
        "0 deterministic deep-ledger outcome-ready rows",
    ):
        assert required in scope


def test_phase36_scope_lists_recovery_tasks() -> None:
    scope = (
        PROJECT_ROOT / "docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md"
    ).read_text(encoding="utf-8")

    for task_id in (
        "SAS-BABLOS-001",
        "SAS-BABLOS-002",
        "SAS-BABLOS-003",
        "SAS-BABLOS-004",
        "SAS-BABLOS-005",
        "SAS-BABLOS-006",
        "SAS-BABLOS-007",
        "SAS-BABLOS-008",
    ):
        assert task_id in scope


def test_phase36_scope_preserves_media_guardrails() -> None:
    scope = (
        PROJECT_ROOT / "docs/pilot/bablos79_PHASE36_CORPUS_COMPLETION_SCOPE.md"
    ).read_text(encoding="utf-8")
    recapture_plan = (
        PROJECT_ROOT / "docs/pilot/bablos79_PHASE36_TEXT_RECAPTURE_PLAN.md"
    ).read_text(encoding="utf-8")

    for required in (
        "OCR/vision output is draft evidence until human/operator accepted",
        "Audio transcripts are internal-only until human/operator accepted",
        "No private Telegram scraping",
    ):
        assert required in scope

    for required in (
        "public Telegram `/s/bablos79` pages",
        "treating missing rows as wins, losses, weak evidence, or strong evidence",
        "No outcome metrics should be recomputed until the recapture output and media",
    ):
        assert required in recapture_plan
