"""P4 scaled Binance archive collection planning."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import date
from typing import Sequence

from entropy.evidence.crypto_universe import CryptoUniverseSnapshot
from entropy.evidence.source_selection import build_binance_monthly_klines_urls, validate_source_use

P4_SCALE_PLAN_ID = "P4-BINANCE-SCALE-PLAN-v1"
P4_REVISED_SCALE_PLAN_ID = "P4-BINANCE-REVISED-SCALE-PLAN-v1"


@dataclass(frozen=True)
class P4DownloadItem:
    """One planned Binance monthly archive download."""

    sequence: int
    symbol: str
    interval: str
    year: int
    month: int
    url: str
    status: str = "PENDING"
    source_sha256: str | None = None
    dataset_hash: str | None = None


@dataclass(frozen=True)
class P4ScalePlan:
    """Deterministic scaled P4 collection plan."""

    plan_id: str
    universe_id: str
    universe_hash: str
    source_selection_id: str
    interval: str
    start_year: int
    start_month: int
    end_year: int
    end_month: int
    required_assets: int
    required_labeled_weeks: int
    download_items: tuple[P4DownloadItem, ...]
    artifact_root: str
    batch_size: int
    gate_claim_allowed: bool = False

    @property
    def plan_hash(self) -> str:
        payload = json.dumps(
            {
                "plan_id": self.plan_id,
                "universe_id": self.universe_id,
                "universe_hash": self.universe_hash,
                "source_selection_id": self.source_selection_id,
                "interval": self.interval,
                "start_year": self.start_year,
                "start_month": self.start_month,
                "end_year": self.end_year,
                "end_month": self.end_month,
                "required_assets": self.required_assets,
                "required_labeled_weeks": self.required_labeled_weeks,
                "download_items": [asdict(item) for item in self.download_items],
                "artifact_root": self.artifact_root,
                "batch_size": self.batch_size,
                "gate_claim_allowed": self.gate_claim_allowed,
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @property
    def asset_count(self) -> int:
        return len({item.symbol for item in self.download_items})

    @property
    def month_count(self) -> int:
        return len({(item.year, item.month) for item in self.download_items})

    @property
    def download_count(self) -> int:
        return len(self.download_items)


def build_p4_scale_plan(
    *,
    universe: CryptoUniverseSnapshot,
    plan_id: str = P4_SCALE_PLAN_ID,
    start_year: int = 2023,
    start_month: int = 1,
    end_year: int = 2025,
    end_month: int = 12,
    interval: str = "1d",
    required_assets: int = 15,
    required_labeled_weeks: int = 156,
    artifact_root: str = "artifacts/evidence/p4_binance_scale",
    batch_size: int = 20,
) -> P4ScalePlan:
    """Build a deterministic P4 scaled collection plan without downloading data."""
    validate_source_use(
        source_id="binance_public_archive",
        use_case="p4_label_coverage",
        domain="data.binance.vision",
    )
    if required_assets < 1:
        raise ValueError("required_assets must be positive")
    if required_labeled_weeks < 1:
        raise ValueError("required_labeled_weeks must be positive")
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    if not universe.assets:
        raise ValueError("universe must contain at least one asset")
    if not plan_id.strip():
        raise ValueError("plan_id must not be blank")

    items: list[P4DownloadItem] = []
    sequence = 1
    for asset in universe.assets:
        urls = build_binance_monthly_klines_urls(
            symbol=asset.binance_symbol,
            interval=interval,
            start_year=start_year,
            start_month=start_month,
            end_year=end_year,
            end_month=end_month,
        )
        for url in urls:
            year, month = _parse_year_month_from_url(url)
            items.append(
                P4DownloadItem(
                    sequence=sequence,
                    symbol=asset.binance_symbol,
                    interval=interval,
                    year=year,
                    month=month,
                    url=url,
                )
            )
            sequence += 1
    return P4ScalePlan(
        plan_id=plan_id,
        universe_id=universe.universe_id,
        universe_hash=universe.universe_hash,
        source_selection_id=universe.source_selection_id,
        interval=interval,
        start_year=start_year,
        start_month=start_month,
        end_year=end_year,
        end_month=end_month,
        required_assets=required_assets,
        required_labeled_weeks=required_labeled_weeks,
        download_items=tuple(items),
        artifact_root=artifact_root,
        batch_size=batch_size,
    )


def render_p4_scale_plan(plan: P4ScalePlan) -> str:
    """Render a deterministic Markdown scale plan."""
    lines = [
        "# P4 Coverage Scale Plan",
        "",
        f"Plan ID: `{plan.plan_id}`",
        f"Plan hash: `{plan.plan_hash}`",
        f"Universe ID: `{plan.universe_id}`",
        f"Universe hash: `{plan.universe_hash}`",
        f"Source selection ID: `{plan.source_selection_id}`",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Asset count | {plan.asset_count} |",
        f"| Month count | {plan.month_count} |",
        f"| Planned downloads | {plan.download_count} |",
        f"| Interval | {plan.interval} |",
        f"| Window | {plan.start_year}-{plan.start_month:02d} to {plan.end_year}-{plan.end_month:02d} |",
        f"| Required passing assets | {plan.required_assets} |",
        f"| Required labeled weeks | {plan.required_labeled_weeks} |",
        f"| Batch size | {plan.batch_size} |",
        f"| Gate claim allowed | {str(plan.gate_claim_allowed).lower()} |",
        "",
        "## Resume Policy",
        "",
        "- Download items are immutable and ordered by `sequence`.",
        "- Each completed item must record `source_sha256` before conversion.",
        "- Each converted symbol dataset must record `dataset_hash` before P4 generation.",
        "- Failed or missing monthly archives remain `PENDING` or `FAILED`; do not delete rows.",
        "- Run collection in batches no larger than the configured batch size.",
        "",
        "## Acceptance Checks Before Gate Packet",
        "",
        "- All planned downloads must be terminal: `DONE`, documented `MISSING_SOURCE`, or `FAILED`.",
        "- At least 15 assets must have >=156 valid post-warmup P4 labeled weeks.",
        "- Every passing asset must have source hashes, dataset hash, label artifact, and coverage row.",
        "- Gate claim remains false until a reviewed P4 coverage packet is produced.",
        "",
        "| Sequence | Symbol | Month | Status | URL |",
        "|----------|--------|-------|--------|-----|",
    ]
    for item in plan.download_items:
        lines.append(
            "| "
            f"{item.sequence} | "
            f"{item.symbol} | "
            f"{item.year}-{item.month:02d} | "
            f"{item.status} | "
            f"{item.url} |"
        )
    lines.append("")
    return "\n".join(lines)


def plan_manifest_payload(plan: P4ScalePlan) -> dict[str, object]:
    """Return a JSON-serializable scale-plan manifest."""
    return {
        "plan_id": plan.plan_id,
        "plan_hash": plan.plan_hash,
        "universe_id": plan.universe_id,
        "universe_hash": plan.universe_hash,
        "source_selection_id": plan.source_selection_id,
        "interval": plan.interval,
        "start": f"{plan.start_year}-{plan.start_month:02d}",
        "end": f"{plan.end_year}-{plan.end_month:02d}",
        "required_assets": plan.required_assets,
        "required_labeled_weeks": plan.required_labeled_weeks,
        "artifact_root": plan.artifact_root,
        "batch_size": plan.batch_size,
        "gate_claim_allowed": plan.gate_claim_allowed,
        "download_count": plan.download_count,
        "download_items": [asdict(item) for item in plan.download_items],
    }


def _parse_year_month_from_url(url: str) -> tuple[int, int]:
    file_name = url.rsplit("/", 1)[-1]
    stem = file_name.removesuffix(".zip")
    year = int(stem.rsplit("-", 2)[-2])
    month = int(stem.rsplit("-", 1)[-1])
    if date(year, month, 1).year != year:
        raise ValueError("invalid year/month in URL")
    return year, month


def first_batch(plan: P4ScalePlan) -> tuple[P4DownloadItem, ...]:
    """Return the first resumable batch."""
    return batch_items(plan, batch_index=1)


def batch_items(plan: P4ScalePlan, *, batch_index: int) -> tuple[P4DownloadItem, ...]:
    """Return one resumable batch by one-based batch index."""
    if batch_index < 1:
        raise ValueError("batch_index must be positive")
    start_index = (batch_index - 1) * plan.batch_size
    end_index = start_index + plan.batch_size
    return plan.download_items[start_index:end_index]


def pending_count(items: Sequence[P4DownloadItem]) -> int:
    """Count pending download items."""
    return sum(1 for item in items if item.status == "PENDING")
