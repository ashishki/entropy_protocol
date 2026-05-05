"""Formation-only input adapter for the Phase 1B baseline surface."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import polars as pl

from entropy.baseline.features import (
    Phase1BFeatureContract,
    phase1b_feature_contract_hash,
    validate_phase1b_feature_columns,
)
from entropy.baseline.long_only import Phase1BBaselineSurface
from entropy.evidence.phase1a_registration import PHASE1A_FORMATION_LABEL

PHASE1B_FORMATION_INPUT_ADAPTER_ID = "PHASE1B-FORMATION-INPUT-ADAPTER-v1"


@dataclass(frozen=True)
class Phase1BFormationInputFrame:
    """Prepared formation-only input frame and audit metadata."""

    adapter_id: str
    split_label: str
    row_count: int
    symbol_count: int
    dataset_hashes: tuple[str, ...]
    input_hash: str
    schema_hash: str
    feature_contract_hash: str
    frame: pl.DataFrame
    evaluation_allowed: bool = False
    gate_claim_allowed: bool = False


def prepare_phase1b_formation_input(
    surface: Phase1BBaselineSurface,
    rows: pl.DataFrame,
    *,
    split_label: str = PHASE1A_FORMATION_LABEL,
    feature_contract: Phase1BFeatureContract | None = None,
) -> Phase1BFormationInputFrame:
    """Prepare formation-only OHLCV rows without computing alpha or metrics."""
    if split_label != PHASE1A_FORMATION_LABEL:
        raise ValueError("Phase 1B formation adapter only accepts formation split rows")
    if split_label not in surface.allowed_split_labels:
        raise ValueError("Phase 1B surface does not allow the requested split label")
    contract = feature_contract or Phase1BFeatureContract()
    decision = validate_phase1b_feature_columns(rows.columns, contract)
    if not decision.allowed:
        raise ValueError(f"Phase 1B formation input rejected: {decision.reason_code}")
    _validate_ohlcv_values(rows)

    selected = rows.select(list(contract.required_input_columns)).sort(["symbol", "timestamp_utc"])
    dataset_hashes = tuple(selected.get_column("dataset_hash").unique().sort().to_list())
    return Phase1BFormationInputFrame(
        adapter_id=PHASE1B_FORMATION_INPUT_ADAPTER_ID,
        split_label=split_label,
        row_count=selected.height,
        symbol_count=selected.get_column("symbol").n_unique(),
        dataset_hashes=dataset_hashes,
        input_hash=_hash_dataframe(selected),
        schema_hash=_hash_schema(selected),
        feature_contract_hash=phase1b_feature_contract_hash(contract),
        frame=selected,
    )


def _validate_ohlcv_values(rows: pl.DataFrame) -> None:
    if rows.height == 0:
        raise ValueError("Phase 1B formation input requires at least one row")
    invalid = rows.filter(
        (pl.col("close") <= 0)
        | (pl.col("open") <= 0)
        | (pl.col("high") < pl.max_horizontal("open", "close"))
        | (pl.col("low") > pl.min_horizontal("open", "close"))
        | (pl.col("low") <= 0)
        | (pl.col("volume") < 0)
    )
    if invalid.height > 0:
        raise ValueError("Phase 1B formation input failed OHLCV sanity checks")


def _hash_schema(frame: pl.DataFrame) -> str:
    payload = [(name, str(dtype)) for name, dtype in frame.schema.items()]
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _hash_dataframe(frame: pl.DataFrame) -> str:
    payload = frame.to_dicts()
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
