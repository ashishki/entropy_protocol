from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from decimal import Decimal

import pytest

from signal_sandbox.ledger.record import Direction, SignalRecord, compute_dedup_key
from signal_sandbox.outcomes.aggregate import aggregate_outcomes
from signal_sandbox.outcomes.matcher import Outcome, OutcomeRecord
from signal_sandbox.outcomes.rule_registry import (
    EXCLUDED_AMBIGUOUS_RULE_ID,
    LONG_TARGET_STOP_RULE_ID,
)
from signal_sandbox.prices.base import make_price_snapshot
from signal_sandbox.reports.disclaimers import CANONICAL_DISCLAIMER
from signal_sandbox.reports.markdown import (
    DisclaimerMissing,
    PrototypeSnapshotNotAccepted,
    render_markdown_report,
    validate_disclaimer,
)
from signal_sandbox.sources.manifest import (
    EligibilityVerdict,
    SourceManifest,
    SourceType,
)

TEXT_SHA = "c" * 64
LEDGER_SHA = "d" * 64


def fixture_records() -> list[SignalRecord]:
    return [
        make_signal("target", Direction.LONG, minute=0),
        make_signal("ambiguous", Direction.UNKNOWN, minute=1),
    ]


def make_signal(capture_id: str, direction: Direction, *, minute: int) -> SignalRecord:
    return SignalRecord(
        source_id="pilot",
        capture_id=capture_id,
        evidence_url=f"https://t.me/example/{minute}",
        text_sha256=TEXT_SHA,
        capture_timestamp_utc=datetime(2026, 5, 7, 9, minute, tzinfo=UTC),
        extracted_timestamp_utc=datetime(2026, 5, 7, 10, minute, tzinfo=UTC),
        asset_symbol="BTC",
        direction=direction,
        entry=Decimal("100"),
        stop=Decimal("90"),
        target=Decimal("110"),
    )


def fixture_manifest() -> SourceManifest:
    return SourceManifest(
        source_id="pilot",
        source_url="https://t.me/example",
        source_type=SourceType.TELEGRAM_PUBLIC,
        capture_method="operator_file",
        tos_reference="docs/legal_risk_memo.md",
        eligibility_verdict=EligibilityVerdict.APPROVED,
    )


def fixture_snapshot(provider_status: str = "operator_supplied"):
    snapshot = make_price_snapshot(
        provider_id="operator-file",
        provider_status="operator_supplied",
        as_of_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
        range_start_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        range_end_utc=datetime(2026, 5, 7, 11, tzinfo=UTC),
        assets=["BTC"],
        rows=[
            {
                "asset": "BTC",
                "timestamp_utc": datetime(2026, 5, 7, 10, tzinfo=UTC),
                "open": "100",
                "high": "111",
                "low": "95",
                "close": "110",
                "volume": "10",
            }
        ],
    )
    return snapshot.model_copy(update={"provider_status": provider_status})


def fixture_outcomes(records: list[SignalRecord]) -> list[OutcomeRecord]:
    target, ambiguous = records
    return [
        OutcomeRecord(
            dedup_key=compute_dedup_key(target),
            source_id=target.source_id,
            asset_symbol=target.asset_symbol,
            extracted_timestamp_utc=target.extracted_timestamp_utc,
            outcome=Outcome.TARGET_HIT,
            return_pct=Decimal("10.000000"),
            outcome_rule_id=LONG_TARGET_STOP_RULE_ID,
            snapshot_sha256=fixture_snapshot().sha256,
        ),
        OutcomeRecord(
            dedup_key=compute_dedup_key(ambiguous),
            source_id=ambiguous.source_id,
            asset_symbol=ambiguous.asset_symbol,
            extracted_timestamp_utc=ambiguous.extracted_timestamp_utc,
            outcome=Outcome.EXCLUDED_AMBIGUOUS,
            outcome_rule_id=EXCLUDED_AMBIGUOUS_RULE_ID,
            snapshot_sha256=fixture_snapshot().sha256,
        ),
    ]


def render(provider_status: str = "operator_supplied", *, accept: bool = False) -> str:
    records = fixture_records()
    outcomes = fixture_outcomes(records)
    return render_markdown_report(
        manifest=fixture_manifest(),
        ledger_records=records,
        snapshot=fixture_snapshot(provider_status),
        outcomes=outcomes,
        summary=aggregate_outcomes(outcomes),
        ledger_sha256=LEDGER_SHA,
        accept_prototype_prices=accept,
    )


def test_byte_identical_re_run() -> None:
    first = render()
    second = render()

    assert first == second
    assert (
        hashlib.sha256(first.encode("utf-8")).hexdigest()
        == hashlib.sha256(second.encode("utf-8")).hexdigest()
    )


def test_disclaimer_present_and_canonical() -> None:
    report = render()

    assert report.count(CANONICAL_DISCLAIMER) == 1
    with pytest.raises(DisclaimerMissing):
        validate_disclaimer("## Disclaimer\n\nnot canonical")


def test_provenance_complete() -> None:
    snapshot = fixture_snapshot()
    report = render()

    assert report.count(snapshot.provider_id) == 1
    assert report.count(snapshot.as_of_utc.isoformat()) == 1
    assert report.count(snapshot.sha256) == 1
    assert report.count(LEDGER_SHA) == 1


def test_per_signal_evidence_present() -> None:
    report = render()

    for record in fixture_records():
        assert record.evidence_url in report
        assert record.capture_timestamp_utc.isoformat() in report
        assert record.text_sha256 in report


def test_prototype_snapshot_gated() -> None:
    with pytest.raises(PrototypeSnapshotNotAccepted):
        render("prototype")

    assert "Prototype Price Source Warning" in render("prototype", accept=True)


def test_excluded_signals_separated() -> None:
    report = render()
    evaluated_section = report.split("## Per-Signal Outcomes", maxsplit=1)[1].split(
        "## Excluded Signals", maxsplit=1
    )[0]
    excluded_section = report.split("## Excluded Signals", maxsplit=1)[1]

    assert "excluded_ambiguous: 1" in excluded_section
    assert "ambiguous" not in evaluated_section
    assert "excluded_ambiguous" in excluded_section
