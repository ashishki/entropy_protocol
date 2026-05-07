"""Resumable P4 Binance archive batch collection."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Sequence
from urllib.request import urlopen

from entropy.evidence.p4_scale_plan import P4DownloadItem, P4ScalePlan, first_batch
from entropy.evidence.source_selection import validate_source_use

P4_BATCH_COLLECTION_ID = "P4-BINANCE-BATCH-COLLECT-v1"

FetchBytes = Callable[[str], bytes]


@dataclass(frozen=True)
class P4BatchItemResult:
    """Result for one batch download item."""

    sequence: int
    symbol: str
    year: int
    month: int
    url: str
    status: str
    path: str | None
    source_sha256: str | None
    byte_count: int
    error: str | None = None


@dataclass(frozen=True)
class P4BatchCollectionResult:
    """Manifest-level result for a P4 batch collection."""

    collection_id: str
    plan_id: str
    plan_hash: str
    batch_index: int
    requested_items: int
    done_count: int
    failed_count: int
    output_dir: Path
    manifest_path: Path
    items: tuple[P4BatchItemResult, ...]
    gate_claim_allowed: bool = False


def fetch_url_bytes(url: str, *, timeout_seconds: int = 30) -> bytes:
    """Fetch URL bytes from an approved public source."""
    with urlopen(url, timeout=timeout_seconds) as response:
        return response.read()


def collect_first_p4_batch(
    *,
    plan: P4ScalePlan,
    output_dir: Path | str,
    fetch_bytes: FetchBytes = fetch_url_bytes,
    batch_index: int = 1,
) -> P4BatchCollectionResult:
    """Download the first planned P4 batch and write a deterministic manifest."""
    return collect_p4_batch(
        plan=plan,
        items=first_batch(plan),
        output_dir=output_dir,
        fetch_bytes=fetch_bytes,
        batch_index=batch_index,
    )


def collect_p4_batch(
    *,
    plan: P4ScalePlan,
    items: Sequence[P4DownloadItem],
    output_dir: Path | str,
    fetch_bytes: FetchBytes = fetch_url_bytes,
    batch_index: int = 1,
) -> P4BatchCollectionResult:
    """Download planned P4 archive items and write a resumable batch manifest."""
    validate_source_use(
        source_id="binance_public_archive",
        use_case="p4_label_coverage",
        domain="data.binance.vision",
    )
    if batch_index < 1:
        raise ValueError("batch_index must be positive")
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    item_results: list[P4BatchItemResult] = []
    for item in items:
        item_path = (
            root / item.symbol / f"{item.symbol}-{item.interval}-{item.year}-{item.month:02d}.zip"
        )
        try:
            payload = fetch_bytes(item.url)
            item_path.parent.mkdir(parents=True, exist_ok=True)
            item_path.write_bytes(payload)
            source_sha256 = hashlib.sha256(payload).hexdigest()
            item_results.append(
                P4BatchItemResult(
                    sequence=item.sequence,
                    symbol=item.symbol,
                    year=item.year,
                    month=item.month,
                    url=item.url,
                    status="DONE",
                    path=item_path.as_posix(),
                    source_sha256=source_sha256,
                    byte_count=len(payload),
                )
            )
        except Exception as exc:  # noqa: BLE001 - manifest must record any fetch failure.
            item_results.append(
                P4BatchItemResult(
                    sequence=item.sequence,
                    symbol=item.symbol,
                    year=item.year,
                    month=item.month,
                    url=item.url,
                    status="FAILED",
                    path=None,
                    source_sha256=None,
                    byte_count=0,
                    error=str(exc),
                )
            )
    manifest_path = root / f"P4_BATCH_{batch_index:03d}_MANIFEST.json"
    result = P4BatchCollectionResult(
        collection_id=P4_BATCH_COLLECTION_ID,
        plan_id=plan.plan_id,
        plan_hash=plan.plan_hash,
        batch_index=batch_index,
        requested_items=len(item_results),
        done_count=sum(1 for item in item_results if item.status == "DONE"),
        failed_count=sum(1 for item in item_results if item.status == "FAILED"),
        output_dir=root,
        manifest_path=manifest_path,
        items=tuple(item_results),
    )
    manifest_path.write_text(
        json.dumps(batch_manifest_payload(result), sort_keys=True, indent=2) + "\n"
    )
    return result


def batch_manifest_payload(result: P4BatchCollectionResult) -> dict[str, object]:
    """Return a JSON-serializable batch manifest."""
    return {
        "collection_id": result.collection_id,
        "plan_id": result.plan_id,
        "plan_hash": result.plan_hash,
        "batch_index": result.batch_index,
        "requested_items": result.requested_items,
        "done_count": result.done_count,
        "failed_count": result.failed_count,
        "output_dir": result.output_dir.as_posix(),
        "gate_claim_allowed": result.gate_claim_allowed,
        "items": [asdict(item) for item in result.items],
    }


def render_p4_batch_summary(result: P4BatchCollectionResult) -> str:
    """Render a deterministic Markdown batch summary."""
    lines = [
        "# P4 Batch Collection Summary",
        "",
        f"Collection ID: `{result.collection_id}`",
        f"Plan ID: `{result.plan_id}`",
        f"Plan hash: `{result.plan_hash}`",
        f"Batch index: {result.batch_index}",
        f"Requested items: {result.requested_items}",
        f"Done: {result.done_count}",
        f"Failed: {result.failed_count}",
        f"Gate claim allowed: `{str(result.gate_claim_allowed).lower()}`",
        "",
        "| Sequence | Symbol | Month | Status | Bytes | SHA-256 |",
        "|----------|--------|-------|--------|-------|---------|",
    ]
    for item in result.items:
        lines.append(
            "| "
            f"{item.sequence} | "
            f"{item.symbol} | "
            f"{item.year}-{item.month:02d} | "
            f"{item.status} | "
            f"{item.byte_count} | "
            f"{item.source_sha256 or ''} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this is controlled batch collection only. It does not close P4 "
            "coverage, approve Phase 0, start Phase 1, or make performance claims.",
            "",
        ]
    )
    return "\n".join(lines)
