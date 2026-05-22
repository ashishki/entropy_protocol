from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_buyer_feedback_log_records_required_demo_fields() -> None:
    log = (PROJECT_ROOT / "docs/pilot/BUYER_FEEDBACK_LOG.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "`buyer_role`",
        "`main_objection`",
        "`requested_output`",
        "`willingness_to_pay`",
        "`next_action`",
        "| demo_id | demo_date | buyer_role | buyer_segment |",
    ):
        assert required in log


def test_buyer_feedback_log_tracks_wtp_and_next_action_rules() -> None:
    log = (PROJECT_ROOT / "docs/pilot/BUYER_FEEDBACK_LOG.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "## Willingness-To-Pay Scale",
        "`yes_paid_pilot`",
        "`yes_if_scope_adjusted`",
        "`unclear`",
        "`no`",
        "Every `yes_paid_pilot` or `yes_if_scope_adjusted` record needs an owner",
        "Do not count compliments as validation.",
        "Real demos recorded: 0",
    ):
        assert required in log
