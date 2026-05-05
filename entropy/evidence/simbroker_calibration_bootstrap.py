"""No-budget SimBroker calibration quote bootstrap tooling."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable, Literal, Sequence
from urllib.request import Request, urlopen

from entropy.evidence.source_selection import validate_source_use
from entropy.simbroker.calibration import NO_GATE_CLAIM

SIMBROKER_CALIBRATION_BOOTSTRAP_ID = "SB-CAL-BOOTSTRAP-v1"

FetchJson = Callable[[str], dict[str, Any]]


@dataclass(frozen=True)
class CalibrationQuoteTarget:
    """One approved public quote lookup target."""

    symbol: str
    source_id: Literal["coinbase_exchange_public_api", "kraken_public_api"]
    source_symbol: str
    url: str
    domain: str


@dataclass(frozen=True)
class CalibrationQuoteSnapshot:
    """One raw public quote snapshot candidate."""

    symbol: str
    source_id: str
    source_symbol: str
    domain: str
    url: str
    status: str
    quote_ts: str | None
    bid: str | None
    ask: str | None
    raw_path: str | None
    raw_sha256: str | None
    error: str | None = None


@dataclass(frozen=True)
class CalibrationQuoteBootstrapResult:
    """Manifest-level bootstrap result."""

    bootstrap_id: str
    evidence_claim: str
    quote_target_count: int
    done_count: int
    failed_count: int
    output_dir: Path
    manifest_path: Path
    summary_path: Path
    snapshots: tuple[CalibrationQuoteSnapshot, ...]
    gate_claim_allowed: bool = False
    calibration_rows_created: bool = False
    manual_verification_complete: bool = False


DEFAULT_QUOTE_TARGETS: tuple[CalibrationQuoteTarget, ...] = (
    CalibrationQuoteTarget(
        symbol="BTC-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="BTC-USD",
        url="https://api.exchange.coinbase.com/products/BTC-USD/ticker",
        domain="api.exchange.coinbase.com",
    ),
    CalibrationQuoteTarget(
        symbol="ETH-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="ETH-USD",
        url="https://api.exchange.coinbase.com/products/ETH-USD/ticker",
        domain="api.exchange.coinbase.com",
    ),
    CalibrationQuoteTarget(
        symbol="LTC-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="LTC-USD",
        url="https://api.exchange.coinbase.com/products/LTC-USD/ticker",
        domain="api.exchange.coinbase.com",
    ),
    CalibrationQuoteTarget(
        symbol="BCH-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="BCH-USD",
        url="https://api.exchange.coinbase.com/products/BCH-USD/ticker",
        domain="api.exchange.coinbase.com",
    ),
    CalibrationQuoteTarget(
        symbol="XLM-USD",
        source_id="coinbase_exchange_public_api",
        source_symbol="XLM-USD",
        url="https://api.exchange.coinbase.com/products/XLM-USD/ticker",
        domain="api.exchange.coinbase.com",
    ),
    CalibrationQuoteTarget(
        symbol="BTC-USD",
        source_id="kraken_public_api",
        source_symbol="XBTUSD",
        url="https://api.kraken.com/0/public/Ticker?pair=XBTUSD",
        domain="api.kraken.com",
    ),
    CalibrationQuoteTarget(
        symbol="ETH-USD",
        source_id="kraken_public_api",
        source_symbol="ETHUSD",
        url="https://api.kraken.com/0/public/Ticker?pair=ETHUSD",
        domain="api.kraken.com",
    ),
    CalibrationQuoteTarget(
        symbol="LTC-USD",
        source_id="kraken_public_api",
        source_symbol="LTCUSD",
        url="https://api.kraken.com/0/public/Ticker?pair=LTCUSD",
        domain="api.kraken.com",
    ),
    CalibrationQuoteTarget(
        symbol="BCH-USD",
        source_id="kraken_public_api",
        source_symbol="BCHUSD",
        url="https://api.kraken.com/0/public/Ticker?pair=BCHUSD",
        domain="api.kraken.com",
    ),
    CalibrationQuoteTarget(
        symbol="XLM-USD",
        source_id="kraken_public_api",
        source_symbol="XLMUSD",
        url="https://api.kraken.com/0/public/Ticker?pair=XLMUSD",
        domain="api.kraken.com",
    ),
)


def fetch_json_url(url: str, *, timeout_seconds: int = 30) -> dict[str, Any]:
    """Fetch JSON from an approved public source."""
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "entropy-protocol-phase0-evidence-bootstrap/1.0",
        },
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = response.read()
    parsed = json.loads(payload.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("expected JSON object")
    return parsed


def collect_calibration_quote_bootstrap(
    *,
    output_dir: Path | str,
    targets: Sequence[CalibrationQuoteTarget] = DEFAULT_QUOTE_TARGETS,
    fetch_json: FetchJson = fetch_json_url,
    fetched_at: datetime | None = None,
) -> CalibrationQuoteBootstrapResult:
    """Collect raw approved public quote snapshots for future manual review."""
    if not targets:
        raise ValueError("targets must not be empty")
    root = Path(output_dir)
    raw_dir = root / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    fetch_ts = fetched_at or datetime.now(UTC)
    if fetch_ts.tzinfo is None or fetch_ts.utcoffset() is None:
        raise ValueError("fetched_at must be timezone-aware")
    snapshots: list[CalibrationQuoteSnapshot] = []
    for index, target in enumerate(targets, start=1):
        validate_source_use(
            source_id=target.source_id,
            use_case="simbroker_calibration",
            domain=target.domain,
        )
        try:
            raw = fetch_json(target.url)
            raw_bytes = _canonical_json_bytes(raw)
            raw_hash = hashlib.sha256(raw_bytes).hexdigest()
            raw_path = raw_dir / f"{index:03d}_{target.source_id}_{target.source_symbol}.json"
            raw_path.write_bytes(raw_bytes)
            bid, ask, quote_ts = _parse_quote(target, raw, fetch_ts)
            snapshots.append(
                CalibrationQuoteSnapshot(
                    symbol=target.symbol,
                    source_id=target.source_id,
                    source_symbol=target.source_symbol,
                    domain=target.domain,
                    url=target.url,
                    status="DONE",
                    quote_ts=quote_ts.isoformat(),
                    bid=str(bid),
                    ask=str(ask),
                    raw_path=raw_path.as_posix(),
                    raw_sha256=raw_hash,
                )
            )
        except Exception as exc:  # noqa: BLE001 - evidence manifests must capture fetch failures.
            snapshots.append(
                CalibrationQuoteSnapshot(
                    symbol=target.symbol,
                    source_id=target.source_id,
                    source_symbol=target.source_symbol,
                    domain=target.domain,
                    url=target.url,
                    status="FAILED",
                    quote_ts=None,
                    bid=None,
                    ask=None,
                    raw_path=None,
                    raw_sha256=None,
                    error=str(exc),
                )
            )
    result = CalibrationQuoteBootstrapResult(
        bootstrap_id=SIMBROKER_CALIBRATION_BOOTSTRAP_ID,
        evidence_claim=NO_GATE_CLAIM,
        quote_target_count=len(targets),
        done_count=sum(1 for snapshot in snapshots if snapshot.status == "DONE"),
        failed_count=sum(1 for snapshot in snapshots if snapshot.status == "FAILED"),
        output_dir=root,
        manifest_path=root / "SIMBROKER_CALIBRATION_BOOTSTRAP_MANIFEST.json",
        summary_path=root / "SIMBROKER_CALIBRATION_BOOTSTRAP_SUMMARY.md",
        snapshots=tuple(snapshots),
    )
    _write_manifest(result)
    result.summary_path.write_text(
        render_calibration_quote_bootstrap_summary(result), encoding="utf-8"
    )
    return result


def render_calibration_quote_bootstrap_summary(result: CalibrationQuoteBootstrapResult) -> str:
    """Render a deterministic Markdown summary for the quote bootstrap."""
    lines = [
        "# SimBroker Calibration Quote Bootstrap",
        "",
        f"Bootstrap ID: `{result.bootstrap_id}`",
        f"Evidence claim: `{result.evidence_claim}`",
        f"Gate claim allowed: `{str(result.gate_claim_allowed).lower()}`",
        f"Calibration rows created: `{str(result.calibration_rows_created).lower()}`",
        f"Manual verification complete: `{str(result.manual_verification_complete).lower()}`",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Quote targets | {result.quote_target_count} |",
        f"| Done | {result.done_count} |",
        f"| Failed | {result.failed_count} |",
        "",
        "| Symbol | Source | Status | Bid | Ask | Raw SHA-256 |",
        "|---|---|---|---:|---:|---|",
    ]
    for snapshot in result.snapshots:
        lines.append(
            "| "
            f"{snapshot.symbol} | "
            f"{snapshot.source_id}:{snapshot.source_symbol} | "
            f"{snapshot.status} | "
            f"{snapshot.bid or ''} | "
            f"{snapshot.ask or ''} | "
            f"{snapshot.raw_sha256 or ''} |"
        )
    lines.extend(
        [
            "",
            "Boundary: this bootstrap records raw public quote snapshots only. It does "
            "not create manually verified calibration rows, approve Phase 0, activate a "
            "broker/provider, trade, or make OOS/performance claims.",
        ]
    )
    return "\n".join(lines)


def _write_manifest(result: CalibrationQuoteBootstrapResult) -> None:
    result.output_dir.mkdir(parents=True, exist_ok=True)
    payload = asdict(result)
    payload["output_dir"] = result.output_dir.as_posix()
    payload["manifest_path"] = result.manifest_path.as_posix()
    payload["summary_path"] = result.summary_path.as_posix()
    result.manifest_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _parse_quote(
    target: CalibrationQuoteTarget,
    raw: dict[str, Any],
    fetched_at: datetime,
) -> tuple[Decimal, Decimal, datetime]:
    if target.source_id == "coinbase_exchange_public_api":
        bid = Decimal(str(raw["bid"]))
        ask = Decimal(str(raw["ask"]))
        quote_ts = datetime.fromisoformat(str(raw["time"]).replace("Z", "+00:00"))
    elif target.source_id == "kraken_public_api":
        errors = raw.get("error", [])
        if errors:
            raise ValueError(f"kraken error: {errors}")
        result = raw["result"]
        pair_payload = next(iter(result.values()))
        bid = Decimal(str(pair_payload["b"][0]))
        ask = Decimal(str(pair_payload["a"][0]))
        quote_ts = fetched_at
    else:  # pragma: no cover - Literal type and source validation prevent this branch.
        raise ValueError(f"unsupported source: {target.source_id}")
    if bid <= 0 or ask <= 0:
        raise ValueError("bid/ask must be positive")
    if ask < bid:
        raise ValueError("ask must be greater than or equal to bid")
    if quote_ts.tzinfo is None or quote_ts.utcoffset() is None:
        raise ValueError("quote timestamp must be timezone-aware")
    return bid, ask, quote_ts.astimezone(UTC)


def _canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
