from __future__ import annotations

from trader_risk_audit.intake import build_intake_report


def test_intake_report_status_sections() -> None:
    runnable = build_intake_report(
        session_payload=_session(),
        profile_payload=_profile(timestamp_timezone="timezone_aware"),
    )
    needs_user_fix = build_intake_report(
        session_payload=_session(),
        profile_payload=_profile(missing_required_fields=["price"]),
    )
    needs_operator_review = build_intake_report(
        session_payload=_session(),
        profile_payload=_profile(duplicate_row_id_risk=True),
    )
    rejected = build_intake_report(
        session_payload=_session(status="blocked_needs_fix"),
        profile_payload=_profile(),
    )

    assert runnable.status == "runnable"
    assert "Proceed to structured rule builder" in runnable.next_action
    assert needs_user_fix.status == "needs-user-fix"
    assert needs_user_fix.reasons == ("missing required fields: price",)
    assert "Ask the prospect for a corrected CSV export" in needs_user_fix.markdown
    assert needs_operator_review.status == "needs-operator-review"
    assert "duplicate or blank row id values need review" in (
        needs_operator_review.markdown
    )
    assert rejected.status == "rejected"
    assert "Stop intake" in rejected.next_action


def test_intake_report_lists_unsupported_checks() -> None:
    report = build_intake_report(
        session_payload=_session(),
        profile_payload=_profile(
            fee_available=False,
            leverage_available=False,
            pnl_available=False,
            account_balance_available=False,
        ),
    )
    covered = build_intake_report(
        session_payload=_session(),
        profile_payload=_profile(
            fee_available=True,
            leverage_available=True,
            pnl_available=True,
            account_balance_available=True,
        ),
    )

    assert report.unsupported_checks == (
        "fees",
        "P&L",
        "drawdown",
        "leverage",
        "account balance",
    )
    assert "- fees" in report.markdown
    assert "- drawdown" in report.markdown
    assert covered.unsupported_checks == ()
    assert "## Unsupported Checks\n- none" in covered.markdown


def test_intake_report_redacts_sensitive_metadata() -> None:
    report = build_intake_report(
        session_payload=_session(source_type="csv_export")
        | {"prospect_label": "@real_trader_handle"},
        profile_payload=_profile(
            canonical_field_map={
                "timestamp": "timestamp",
                "symbol": "telegram_handle",
                "side": "side",
                "quantity": "quantity",
                "price": "price",
            },
            unsupported_columns=["api_key_note"],
        ),
    )

    assert "@real_trader_handle" not in report.markdown
    assert "telegram_handle" not in report.markdown
    assert "api_key_note" not in report.markdown
    assert "redacted" in report.markdown


def _session(
    *,
    status: str = "ready_for_schema_profile",
    source_type: str = "csv_export",
) -> dict[str, object]:
    return {
        "session_id": "intake_demo_001",
        "prospect_label": "pilot_export_001",
        "source_type": source_type,
        "status": status,
    }


def _profile(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "source_file": "export.csv",
        "canonical_field_map": {
            "timestamp": "timestamp",
            "symbol": "symbol",
            "side": "side",
            "quantity": "quantity",
            "price": "price",
        },
        "missing_required_fields": [],
        "duplicate_row_id_risk": False,
        "timestamp_timezone": "timezone_aware",
        "fee_available": True,
        "leverage_available": True,
        "pnl_available": True,
        "account_balance_available": True,
        "unsupported_columns": [],
    }
    payload.update(overrides)
    return payload
