"""Reset closure review contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESET_REVIEW = PROJECT_ROOT / "docs" / "audit" / "RESET_REVIEW.md"
AUDIT_INDEX = PROJECT_ROOT / "docs" / "audit" / "AUDIT_INDEX.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"


def test_reset_review_contains_required_sections() -> None:
    text = RESET_REVIEW.read_text(encoding="utf-8")

    for heading in (
        "## Completed Reset Tasks",
        "## Evidence",
        "## Open Findings",
        "## Next Recommendation",
    ):
        assert heading in text
    assert "T01" in text
    assert "T14" in text
    assert "328 passed, 20 skipped" in text
    assert "No open findings" in text
    assert "awaits human decision" in text


def test_audit_index_records_reset_review() -> None:
    text = AUDIT_INDEX.read_text(encoding="utf-8")

    assert "RESET-CLOSURE" in text
    assert "`docs/audit/RESET_REVIEW.md`" in text
    assert "| RESET-CLOSURE |" in text


def test_codex_prompt_records_reset_closure_state() -> None:
    text = CODEX_PROMPT.read_text(encoding="utf-8")

    assert (
        "Reset implementation awaits human decision after T14" in text
        or "## Next Task\n\nT" in text
        or "Human decision required after T19" in text
    )
    assert "T14 Reset Strategy Closure Review completed" in text
