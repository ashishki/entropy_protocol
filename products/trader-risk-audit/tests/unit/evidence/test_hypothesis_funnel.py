from __future__ import annotations

from pathlib import Path

import pytest

from trader_risk_audit.evidence import (
    EvidenceRow,
    EvidenceValidationError,
    HypothesisFunnelEvent,
    append_customer_log_row,
    append_hypothesis_funnel_event,
    is_demo_hypothesis_event,
    load_hypothesis_evidence,
)


def test_funnel_schema_rejects_sensitive_fields(tmp_path: Path) -> None:
    log = tmp_path / "hypothesis_funnel_events.csv"
    event = HypothesisFunnelEvent(
        event_type="paid_report",
        timestamp="2026-05-15T10:00:00Z",
        intake_id="intake_market_001",
        source_type="csv_export",
        tags=("paid_report", "manual_reviewed"),
    )

    append_hypothesis_funnel_event(log, event)

    assert load_hypothesis_evidence(funnel_event_path=log).funnel_events == (event,)
    for unsafe_event in (
        HypothesisFunnelEvent(
            event_type="valid_export",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="trader@example.com",
            source_type="csv_export",
        ),
        HypothesisFunnelEvent(
            event_type="valid_export",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="intake_ok",
            source_type="csv_export",
            tags=("timestamp,symbol,side,qty",),
        ),
        HypothesisFunnelEvent(
            event_type="policy_built",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="intake_ok",
            source_type="csv_export",
            tags=("api_key",),
        ),
        HypothesisFunnelEvent(
            event_type="paid_report",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="intake_ok",
            source_type="csv_export",
            tags=("payment_id",),
        ),
        HypothesisFunnelEvent(
            event_type="prospect_qualified",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="acct_123456",
            source_type="csv_export",
        ),
    ):
        with pytest.raises(EvidenceValidationError):
            unsafe_event.to_csv_row()


def test_funnel_loader_preserves_legacy_rows(tmp_path: Path) -> None:
    customer_log = tmp_path / "pilot_customer_log.csv"
    funnel_log = tmp_path / "hypothesis_funnel_events.csv"
    legacy_row = EvidenceRow(
        prospect_source="warm_network",
        icp="prop/funded trader",
        call_date="2026-05-15",
        export_provided=True,
        rules_provided=True,
        paid_amount="99",
        objections="privacy",
        report_delivered=True,
        repeat_requested=True,
        referral=False,
    )
    funnel_event = HypothesisFunnelEvent(
        event_type="cta_accepted",
        timestamp="2026-05-15T11:00:00Z",
        intake_id="intake_market_002",
        source_type="csv_export",
    )

    append_customer_log_row(customer_log, legacy_row)
    append_hypothesis_funnel_event(funnel_log, funnel_event)

    dataset = load_hypothesis_evidence(
        customer_log_path=customer_log,
        funnel_event_path=funnel_log,
    )

    assert dataset.legacy_rows == (legacy_row,)
    assert dataset.funnel_events == (funnel_event,)


def test_demo_funnel_events_are_marked_vanity() -> None:
    event = HypothesisFunnelEvent(
        event_type="preview_generated",
        timestamp="2026-05-15T12:00:00Z",
        intake_id="demo_preview",
        source_type="public_sample_demo",
        evidence_source="demo_artifact",
    )

    assert is_demo_hypothesis_event(event)
