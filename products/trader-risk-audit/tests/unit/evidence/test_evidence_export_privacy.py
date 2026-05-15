from __future__ import annotations

from pathlib import Path

import pytest

from trader_risk_audit.evidence import (
    EvidenceValidationError,
    HypothesisFunnelEvent,
    append_hypothesis_funnel_event,
    ensure_evidence_export_safe,
    export_hypothesis_evidence,
)


def test_evidence_export_rejects_sensitive_fields() -> None:
    unsafe_values = (
        "contact trader@example.com",
        "telegram @traderhandle",
        "phone +1 415 555 1212",
        "payment_id pi_test_abc",
        "transaction_id tx_abc",
        "api_key abc",
        "timestamp,symbol,side,qty",
    )

    for value in unsafe_values:
        with pytest.raises(EvidenceValidationError):
            ensure_evidence_export_safe(value)


def test_evidence_export_includes_provenance(tmp_path: Path) -> None:
    funnel_log = tmp_path / "hypothesis_funnel_events.csv"
    append_hypothesis_funnel_event(
        funnel_log,
        HypothesisFunnelEvent(
            event_type="paid_report",
            timestamp="2026-05-15T10:00:00Z",
            intake_id="intake_market_001",
            source_type="csv_export",
        ),
    )

    export = export_hypothesis_evidence(
        output_dir=tmp_path / "export",
        funnel_event_path=funnel_log,
    )
    markdown = export.markdown_path.read_text(encoding="utf-8")
    csv_text = export.csv_path.read_text(encoding="utf-8")

    assert ("funnel_event_log_name", "hypothesis_funnel_events_csv") in (
        export.source_provenance
    )
    assert "funnel_event_log_sha256" in markdown
    assert "funnel_event_log_sha256" in csv_text
    assert "hypothesis_funnel_events_csv" in markdown
    assert str(tmp_path) not in markdown
