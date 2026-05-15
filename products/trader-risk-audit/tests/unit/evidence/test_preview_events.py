from __future__ import annotations

import pytest

from trader_risk_audit.evidence import (
    EvidenceValidationError,
    PreviewEvent,
    is_demo_preview_event,
    summarize_preview_events,
)


def test_preview_event_schema_is_safe() -> None:
    event = PreviewEvent(
        event_type="cta_accepted",
        timestamp="2026-05-15T10:00:00Z",
        intake_id="intake_abcd1234",
        source_type="csv_export",
        objection_tags=("price", "privacy"),
    )

    assert event.to_csv_row() == {
        "event_type": "cta_accepted",
        "timestamp": "2026-05-15T10:00:00Z",
        "intake_id": "intake_abcd1234",
        "source_type": "csv_export",
        "objection_tags": "price,privacy",
    }
    with pytest.raises(EvidenceValidationError):
        PreviewEvent(
            event_type="cta_accepted",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="user@example.com",
            source_type="csv_export",
        ).to_csv_row()
    with pytest.raises(EvidenceValidationError):
        PreviewEvent(
            event_type="objection_recorded",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="intake_ok",
            source_type="csv_export",
            objection_tags=("timestamp,symbol,side",),
        ).to_csv_row()


def test_preview_events_do_not_count_demo_as_paid() -> None:
    events = (
        PreviewEvent(
            event_type="cta_accepted",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="intake_market",
            source_type="csv_export",
        ),
        PreviewEvent(
            event_type="cta_accepted",
            timestamp="2026-05-15T10:01:00Z",
            intake_id="intake_demo",
            source_type="public_sample_demo",
        ),
    )

    summary = summarize_preview_events(events)
    assert summary.cta_accepted_market == 1
    assert is_demo_preview_event(events[1])
