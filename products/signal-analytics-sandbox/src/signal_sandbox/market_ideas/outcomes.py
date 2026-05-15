"""Deterministic MarketIdea outcome evaluation."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.assets import AssetRegistry, ResolutionStatus
from signal_sandbox.market_data.metrics import (
    Direction as MetricDirection,
)
from signal_sandbox.market_data.metrics import (
    HorizonMetric,
    evaluate_horizon_metrics,
)
from signal_sandbox.market_data.store import MarketDataSnapshot
from signal_sandbox.market_ideas.extractor import Direction, MarketIdeaDraft

METRIC_VERSION = "market-idea-outcomes-v1"


class IdeaOutcomeStatus(StrEnum):
    EVALUATED = "evaluated"
    UNRESOLVED_ASSET = "unresolved_asset"
    AMBIGUOUS_ASSET = "ambiguous_asset"
    NOT_APPLICABLE = "not_applicable"
    NO_SNAPSHOT = "no_snapshot"


class MarketIdeaOutcome(BaseModel):
    model_config = ConfigDict(strict=True)

    source_document_id: str = Field(min_length=1)
    market_idea_id: str = Field(min_length=1)
    asset_id: str = Field(min_length=1)
    snapshot_id: str = Field(min_length=1)
    metric_version: str = METRIC_VERSION
    status: IdeaOutcomeStatus
    asset_resolution_status: str = Field(min_length=1)
    horizon_metrics: list[HorizonMetric] = Field(default_factory=list)


def evaluate_market_idea_outcome(
    draft: MarketIdeaDraft,
    *,
    asset_registry: AssetRegistry,
    snapshots_by_asset: dict[str, MarketDataSnapshot],
) -> MarketIdeaOutcome:
    if not draft.asset_mentions:
        return _status_outcome(
            draft,
            asset_id="UNRESOLVED",
            snapshot_id="none",
            status=IdeaOutcomeStatus.UNRESOLVED_ASSET,
            asset_resolution_status=ResolutionStatus.UNRESOLVED.value,
        )

    resolutions = [
        asset_registry.resolve_alias(asset, evidence=draft.source_document_id)
        for asset in draft.asset_mentions
    ]
    exact_matches = [
        resolution.matches[0]
        for resolution in resolutions
        if resolution.status == ResolutionStatus.EXACT and len(resolution.matches) == 1
    ]
    if len(exact_matches) != 1 or any(
        resolution.status == ResolutionStatus.AMBIGUOUS for resolution in resolutions
    ):
        return _status_outcome(
            draft,
            asset_id="AMBIGUOUS" if exact_matches else "UNRESOLVED",
            snapshot_id="none",
            status=(
                IdeaOutcomeStatus.AMBIGUOUS_ASSET
                if exact_matches
                else IdeaOutcomeStatus.UNRESOLVED_ASSET
            ),
            asset_resolution_status=(
                ResolutionStatus.AMBIGUOUS.value
                if exact_matches
                else ResolutionStatus.UNRESOLVED.value
            ),
        )

    asset = exact_matches[0]
    snapshot = snapshots_by_asset.get(asset.canonical_id)
    if snapshot is None:
        return _status_outcome(
            draft,
            asset_id=asset.canonical_id,
            snapshot_id="none",
            status=IdeaOutcomeStatus.NO_SNAPSHOT,
            asset_resolution_status=ResolutionStatus.EXACT.value,
        )

    metrics = evaluate_horizon_metrics(
        snapshot,
        canonical_asset_id=asset.canonical_id,
        post_timestamp_utc=draft.source_timestamp_utc,
        direction=_metric_direction(draft.direction),
    )
    return MarketIdeaOutcome(
        source_document_id=draft.source_document_id,
        market_idea_id=draft.idea_id,
        asset_id=asset.canonical_id,
        snapshot_id=snapshot.metadata.snapshot_id,
        status=IdeaOutcomeStatus.EVALUATED,
        asset_resolution_status=ResolutionStatus.EXACT.value,
        horizon_metrics=metrics,
    )


def _status_outcome(
    draft: MarketIdeaDraft,
    *,
    asset_id: str,
    snapshot_id: str,
    status: IdeaOutcomeStatus,
    asset_resolution_status: str,
) -> MarketIdeaOutcome:
    return MarketIdeaOutcome(
        source_document_id=draft.source_document_id,
        market_idea_id=draft.idea_id,
        asset_id=asset_id,
        snapshot_id=snapshot_id,
        status=status,
        asset_resolution_status=asset_resolution_status,
    )


def _metric_direction(direction: Direction) -> MetricDirection:
    if direction == Direction.LONG:
        return MetricDirection.LONG
    if direction == Direction.SHORT:
        return MetricDirection.SHORT
    if direction == Direction.FLAT:
        return MetricDirection.FLAT
    if direction == Direction.MIXED:
        return MetricDirection.MIXED
    return MetricDirection.UNKNOWN
