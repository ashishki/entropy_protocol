"""Append-only outcome rule registry.

Registry version: 1.0.0

Numerical outcome metrics use Decimal arithmetic and banker's rounding to six
decimal places before any Parquet float conversion.
"""

from __future__ import annotations

from dataclasses import dataclass

RULE_REGISTRY_VERSION = "1.0.0"

LONG_TARGET_STOP_RULE_ID = "outcome.long_target_stop.v1"
EXCLUDED_AMBIGUOUS_RULE_ID = "outcome.excluded_ambiguous.v1"
EXCLUDED_NO_PRICE_RULE_ID = "outcome.excluded_no_price.v1"


@dataclass(frozen=True)
class OutcomeRule:
    rule_id: str
    description: str


RULES: dict[str, OutcomeRule] = {
    LONG_TARGET_STOP_RULE_ID: OutcomeRule(
        rule_id=LONG_TARGET_STOP_RULE_ID,
        description=(
            "For evaluable directional signals, walk forward through OHLCV rows "
            "from extracted_timestamp_utc. For long signals, target wins when "
            "high reaches target before low reaches stop; otherwise stop wins. "
            "No hit before range end produces timeout_no_hit."
        ),
    ),
    EXCLUDED_AMBIGUOUS_RULE_ID: OutcomeRule(
        rule_id=EXCLUDED_AMBIGUOUS_RULE_ID,
        description=(
            "Signals with flat/unknown direction, missing numeric levels, or any "
            "ambiguity flag are excluded from win/loss outcomes."
        ),
    ),
    EXCLUDED_NO_PRICE_RULE_ID: OutcomeRule(
        rule_id=EXCLUDED_NO_PRICE_RULE_ID,
        description=(
            "Signals whose asset is absent from the price snapshot, or has no "
            "forward OHLCV rows, are excluded from win/loss outcomes."
        ),
    ),
}
