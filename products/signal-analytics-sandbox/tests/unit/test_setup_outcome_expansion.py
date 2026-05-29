from __future__ import annotations

from decimal import Decimal

from signal_sandbox.claims import (
    ClaimDirection,
    ClaimOutcomeStatus,
    StructuredClaimType,
    evaluate_claim_outcome,
)
from signal_sandbox.market_data import make_operator_file_snapshot
from tests.unit.test_claim_outcomes_v1 import _claim, dt, row


def test_setup_target_and_stop_compute_r_multiple() -> None:
    target_hit = evaluate_claim_outcome(
        _claim(StructuredClaimType.TRADE_SETUP, entry="100", stop="90", target="120"),
        _snapshot_for_setup_expansion(),
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
        _snapshot_for_setup_expansion(),
        canonical_asset_id="CRYPTO:BTC",
    )

    assert target_hit.status == ClaimOutcomeStatus.TARGET_HIT
    assert target_hit.entry_price == Decimal("100")
    assert target_hit.exit_price == Decimal("120")
    assert target_hit.risk_reward == Decimal("2.000000")
    assert target_hit.r_multiple == Decimal("2.000000")

    assert stopped.status == ClaimOutcomeStatus.STOPPED
    assert stopped.exit_price == Decimal("110")
    assert stopped.r_multiple == Decimal("-1.000000")


def test_setup_timeout_computes_partial_r_multiple_from_timeout_close() -> None:
    outcome = evaluate_claim_outcome(
        _claim(StructuredClaimType.TRADE_SETUP, entry="100", stop="90", target="130"),
        _timeout_snapshot(),
        canonical_asset_id="CRYPTO:BTC",
        timeout_days=2,
    )

    assert outcome.status == ClaimOutcomeStatus.TIMEOUT
    assert outcome.exit_price == Decimal("108")
    assert outcome.return_pct == Decimal("8.000000")
    assert outcome.r_multiple == Decimal("0.800000")


def test_missing_or_invalid_setup_levels_remain_blockers() -> None:
    missing_stop = evaluate_claim_outcome(
        _claim(StructuredClaimType.TRADE_SETUP, entry="100", stop=None, target="120"),
        _snapshot_for_setup_expansion(),
        canonical_asset_id="CRYPTO:BTC",
    )
    invalid_risk = evaluate_claim_outcome(
        _claim(StructuredClaimType.TRADE_SETUP, entry="100", stop="100", target="120"),
        _snapshot_for_setup_expansion(),
        canonical_asset_id="CRYPTO:BTC",
    )

    assert missing_stop.status == ClaimOutcomeStatus.MISSING_REQUIRED_FIELDS
    assert missing_stop.exclusion_reason == "entry_stop_target_direction_required"
    assert missing_stop.r_multiple is None

    assert invalid_risk.status == ClaimOutcomeStatus.MISSING_REQUIRED_FIELDS
    assert invalid_risk.exclusion_reason == "valid_entry_stop_target_direction_required"
    assert invalid_risk.r_multiple is None


def _snapshot_for_setup_expansion():
    return make_operator_file_snapshot(
        snapshot_id="btc-setup-expansion",
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
        ],
        license="operator_provided",
        provenance="unit test fixture",
    )


def _timeout_snapshot():
    return make_operator_file_snapshot(
        snapshot_id="btc-setup-timeout",
        canonical_asset_id="CRYPTO:BTC",
        provider_symbol="BTC/USDT",
        timeframe="1d",
        source_range_start_utc=dt("2026-05-01T00:00:00+00:00"),
        source_range_end_utc=dt("2026-05-03T00:00:00+00:00"),
        captured_at_utc=dt("2026-05-04T00:00:00+00:00"),
        rows=[
            row("2026-05-01T00:00:00+00:00", "100", "103", "97", "100"),
            row("2026-05-03T00:00:00+00:00", "100", "110", "98", "108"),
        ],
        license="operator_provided",
        provenance="unit test fixture",
    )
