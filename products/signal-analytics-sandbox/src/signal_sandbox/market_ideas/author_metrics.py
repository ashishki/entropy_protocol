"""Aggregate MarketIdea outcomes into author/channel metrics."""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.assets import AssetRegistry
from signal_sandbox.market_data.metrics import HorizonStatus
from signal_sandbox.market_ideas.extractor import Direction, IdeaType, MarketIdeaDraft
from signal_sandbox.market_ideas.outcomes import IdeaOutcomeStatus, MarketIdeaOutcome


class AuthorMetrics(BaseModel):
    model_config = ConfigDict(strict=True)

    counts_by_idea_type: dict[str, int] = Field(default_factory=dict)
    counts_by_asset_type: dict[str, int] = Field(default_factory=dict)
    counts_by_horizon_status: dict[str, int] = Field(default_factory=dict)
    counts_by_review_status: dict[str, int] = Field(default_factory=dict)
    directional_hit_rate: Decimal | None = None
    directional_evaluable_count: int = 0
    null_content_count: int = 0
    null_content_rate: Decimal = Decimal("0")


def aggregate_author_metrics(
    drafts: list[MarketIdeaDraft],
    outcomes: list[MarketIdeaOutcome],
    *,
    asset_registry: AssetRegistry,
) -> AuthorMetrics:
    outcomes_by_idea_id = {outcome.market_idea_id: outcome for outcome in outcomes}
    metrics = AuthorMetrics()

    for draft in drafts:
        _increment(metrics.counts_by_idea_type, draft.idea_type.value)
        _increment(metrics.counts_by_review_status, draft.approval_state.value)
        if draft.idea_type == IdeaType.NON_MARKET:
            metrics.null_content_count += 1

        outcome = outcomes_by_idea_id.get(draft.idea_id)
        if outcome is None:
            continue
        asset = asset_registry.get(outcome.asset_id)
        if asset is not None:
            _increment(metrics.counts_by_asset_type, asset.instrument_type.value)
        _count_horizon_statuses(metrics, outcome)

    hits, evaluable = _directional_hits(drafts, outcomes_by_idea_id)
    metrics.directional_evaluable_count = evaluable
    metrics.directional_hit_rate = (
        _ratio(hits, evaluable) if evaluable > 0 else None
    )
    metrics.null_content_rate = _ratio(metrics.null_content_count, len(drafts))
    return metrics


def _count_horizon_statuses(
    metrics: AuthorMetrics,
    outcome: MarketIdeaOutcome,
) -> None:
    if not outcome.horizon_metrics:
        _increment(metrics.counts_by_horizon_status, outcome.status.value)
        return
    for horizon_metric in outcome.horizon_metrics:
        _increment(metrics.counts_by_horizon_status, horizon_metric.status.value)


def _directional_hits(
    drafts: list[MarketIdeaDraft],
    outcomes_by_idea_id: dict[str, MarketIdeaOutcome],
) -> tuple[int, int]:
    hits = 0
    evaluable = 0
    for draft in drafts:
        if draft.direction not in {Direction.LONG, Direction.SHORT}:
            continue
        outcome = outcomes_by_idea_id.get(draft.idea_id)
        if outcome is None or outcome.status != IdeaOutcomeStatus.EVALUATED:
            continue
        first_evaluated = next(
            (
                metric
                for metric in outcome.horizon_metrics
                if metric.status == HorizonStatus.EVALUATED
                and metric.return_pct is not None
            ),
            None,
        )
        if first_evaluated is None or first_evaluated.return_pct is None:
            continue
        evaluable += 1
        if draft.direction == Direction.LONG and first_evaluated.return_pct > 0:
            hits += 1
        if draft.direction == Direction.SHORT and first_evaluated.return_pct < 0:
            hits += 1
    return hits, evaluable


def _increment(counts: dict[str, int], key: str) -> None:
    counts[key] = counts.get(key, 0) + 1


def _ratio(numerator: int, denominator: int) -> Decimal:
    if denominator == 0:
        return Decimal("0.000000")
    return (Decimal(numerator) / Decimal(denominator)).quantize(
        Decimal("0.000001"),
        rounding=ROUND_HALF_EVEN,
    )
