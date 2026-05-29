from __future__ import annotations

from signal_sandbox.reports import (
    ALLOWED_CONTEXT_PHRASES,
    WordingCategory,
    find_forbidden_wording,
    is_customer_safe_wording,
)


def test_customer_safe_wording_blocks_forbidden_report_phrases() -> None:
    findings = find_forbidden_wording(
        "This is the best channel. You should buy now. "
        "It will profit, subscribe now, and has a proven edge."
    )
    categories = {finding.category for finding in findings}

    assert WordingCategory.LEADERBOARD in categories
    assert WordingCategory.ADVICE in categories
    assert WordingCategory.FUTURE_PROFIT in categories
    assert WordingCategory.MARKETPLACE in categories
    assert WordingCategory.OVERCLAIM in categories


def test_customer_safe_wording_allows_bounded_internal_context() -> None:
    safe_text = (
        "This is historical research only, not financial advice, and internal "
        "only. Unsupported rows are exclusions."
    )

    assert is_customer_safe_wording(safe_text)
    assert "historical research only" in ALLOWED_CONTEXT_PHRASES
    assert "unsupported rows are exclusions" in ALLOWED_CONTEXT_PHRASES
