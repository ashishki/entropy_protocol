from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.claims import (
    ClaimDirection,
    ClaimOutcomeStatus,
    StructuredClaim,
    StructuredClaimType,
    evaluate_claim_outcome,
)
from signal_sandbox.market_data import make_operator_file_snapshot


def test_trade_setup_evaluates_target_stop_timeout_and_provenance() -> None:
    target_hit = evaluate_claim_outcome(
        _claim(StructuredClaimType.TRADE_SETUP, entry="100", stop="90", target="120"),
        _snapshot(),
        canonical_asset_id="CRYPTO:BTC",
    )
    stopped = evaluate_claim_outcome(
        _claim(
            StructuredClaimType.TRADE_SETUP,
            direction=ClaimDirection.SHORT,
            entry="100",
            stop="110",
            target="80",
        ),
        _snapshot(),
        canonical_asset_id="CRYPTO:BTC",
    )

    assert target_hit.status == ClaimOutcomeStatus.TARGET_HIT
    assert target_hit.return_pct == Decimal("20.000000")
    assert target_hit.risk_reward == Decimal("2.000000")
    assert target_hit.snapshot_id == "btc-v1-outcomes"
    assert stopped.status == ClaimOutcomeStatus.STOPPED
    assert stopped.return_pct == Decimal("-10.000000")


def test_directional_thesis_supports_fixed_horizon_without_levels() -> None:
    outcome = evaluate_claim_outcome(
        _claim(
            StructuredClaimType.DIRECTIONAL_THESIS,
            entry=None,
            stop=None,
            target=None,
        ),
        _snapshot(),
        canonical_asset_id="CRYPTO:BTC",
    )

    assert outcome.status == ClaimOutcomeStatus.EVALUATED
    assert outcome.entry_price is None
    assert outcome.return_pct == Decimal("50.000000")
    assert outcome.max_favorable_excursion_pct == Decimal("60.000000")


def test_trade_management_requires_original_setup_link() -> None:
    outcome = evaluate_claim_outcome(
        _claim(
            StructuredClaimType.TRADE_MANAGEMENT,
            entry=None,
            stop=None,
            target=None,
        ),
        _snapshot(),
        canonical_asset_id="CRYPTO:BTC",
    )

    assert outcome.status == ClaimOutcomeStatus.REQUIRES_ORIGINAL_SETUP_LINK
    assert outcome.exclusion_reason == "trade_management_requires_original_setup_link"


def _claim(
    claim_type: StructuredClaimType,
    *,
    direction: ClaimDirection = ClaimDirection.LONG,
    entry: str | None = "100",
    stop: str | None = "90",
    target: str | None = "120",
) -> StructuredClaim:
    text_sha = hashlib.sha256(
        f"{claim_type.value}-{direction.value}-{entry}-{stop}-{target}".encode()
    ).hexdigest()
    return StructuredClaim(
        claim_id=f"claim-{text_sha[:12]}",
        source_id="test",
        capture_id="capture-1",
        source_document_id="doc-1",
        evidence_url="https://t.me/test/1",
        text_sha256=text_sha,
        source_timestamp_utc=dt("2026-05-01T00:00:00+00:00"),
        claim_type=claim_type,
        assets=["BTC"],
        direction=direction,
        entry=Decimal(entry) if entry is not None else None,
        stop=Decimal(stop) if stop is not None else None,
        target=Decimal(target) if target is not None else None,
    )


def _snapshot():
    return make_operator_file_snapshot(
        snapshot_id="btc-v1-outcomes",
        canonical_asset_id="CRYPTO:BTC",
        provider_symbol="BTC/USDT",
        timeframe="1d",
        source_range_start_utc=dt("2026-05-01T00:00:00+00:00"),
        source_range_end_utc=dt("2026-05-10T00:00:00+00:00"),
        captured_at_utc=dt("2026-05-11T00:00:00+00:00"),
        rows=[
            row("2026-05-01T00:00:00+00:00", "100", "105", "95", "100"),
            row("2026-05-02T00:00:00+00:00", "100", "118", "96", "112"),
            row("2026-05-03T00:00:00+00:00", "112", "125", "109", "122"),
            row("2026-05-08T00:00:00+00:00", "122", "160", "120", "150"),
        ],
        license="operator_provided",
        provenance="unit test fixture",
    )


def row(timestamp: str, open_: str, high: str, low: str, close: str):
    return {
        "asset": "BTC",
        "timestamp_utc": timestamp,
        "open": open_,
        "high": high,
        "low": low,
        "close": close,
        "volume": "1",
    }


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value).astimezone(UTC)
