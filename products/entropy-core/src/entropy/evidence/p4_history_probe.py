"""P4 Binance archive history eligibility probe."""

from __future__ import annotations

import json
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Callable, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from entropy.evidence.crypto_universe import CryptoUniverseSnapshot
from entropy.evidence.source_selection import build_binance_monthly_klines_urls, validate_source_use

P4_HISTORY_PROBE_ID = "P4-BINANCE-HISTORY-PROBE-v1"
DEFAULT_REQUIRED_COMPLETED_WEEKS = 312
DEFAULT_REQUIRED_VALID_LABELED_WEEKS = 156
DEFAULT_WARMUP_WEEKS = 155

UrlExists = Callable[[str], bool]


@dataclass(frozen=True)
class P4HistoryMonthProbe:
    """Availability result for one monthly archive."""

    symbol: str
    year: int
    month: int
    url: str
    available: bool

    @property
    def month_key(self) -> str:
        return f"{self.year}-{self.month:02d}"


@dataclass(frozen=True)
class P4HistorySymbolProbe:
    """Eligibility result for one symbol."""

    symbol: str
    available_months: tuple[str, ...]
    missing_months: tuple[str, ...]
    earliest_available_month: str | None
    latest_available_month: str | None
    continuous_start_month: str | None
    continuous_end_month: str | None
    continuous_month_count: int
    estimated_completed_weeks: int
    estimated_valid_labeled_weeks: int
    eligible: bool
    reason_code: str


@dataclass(frozen=True)
class P4HistoryProbeResult:
    """Universe-level P4 history eligibility result."""

    probe_id: str
    universe_id: str
    universe_hash: str
    source_selection_id: str
    interval: str
    start_month: str
    end_month: str
    required_assets: int
    required_completed_weeks: int
    required_valid_labeled_weeks: int
    warmup_weeks: int
    rows: tuple[P4HistorySymbolProbe, ...]
    generated_at: datetime
    manifest_path: Path
    gate_claim_allowed: bool = False

    @property
    def eligible_assets(self) -> int:
        return sum(1 for row in self.rows if row.eligible)

    @property
    def universe_eligible(self) -> bool:
        return self.eligible_assets >= self.required_assets


def url_exists_head(url: str, *, timeout_seconds: int = 10) -> bool:
    """Return whether an approved public archive URL exists via HTTP HEAD."""
    request = Request(url, method="HEAD")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return 200 <= response.status < 300
    except HTTPError as exc:
        if exc.code == 404:
            return False
        raise
    except URLError:
        raise


def run_p4_history_probe(
    *,
    universe: CryptoUniverseSnapshot,
    output_dir: Path | str,
    generated_at: datetime,
    start_year: int = 2020,
    start_month: int = 1,
    end_year: int = 2025,
    end_month: int = 12,
    interval: str = "1d",
    required_assets: int = 15,
    required_completed_weeks: int = DEFAULT_REQUIRED_COMPLETED_WEEKS,
    required_valid_labeled_weeks: int = DEFAULT_REQUIRED_VALID_LABELED_WEEKS,
    warmup_weeks: int = DEFAULT_WARMUP_WEEKS,
    url_exists: UrlExists = url_exists_head,
    max_workers: int = 16,
) -> P4HistoryProbeResult:
    """Probe Binance monthly archive availability without downloading archives."""
    validate_source_use(
        source_id="binance_public_archive",
        use_case="p4_label_coverage",
        domain="data.binance.vision",
    )
    _require_utc(generated_at, "generated_at")
    if required_assets < 1:
        raise ValueError("required_assets must be positive")
    if required_completed_weeks < 1:
        raise ValueError("required_completed_weeks must be positive")
    if required_valid_labeled_weeks < 1:
        raise ValueError("required_valid_labeled_weeks must be positive")
    if warmup_weeks < 0:
        raise ValueError("warmup_weeks must be non-negative")
    if max_workers < 1:
        raise ValueError("max_workers must be positive")

    month_keys = _month_keys(start_year, start_month, end_year, end_month)
    month_probes = _probe_months(
        universe=universe,
        start_year=start_year,
        start_month=start_month,
        end_year=end_year,
        end_month=end_month,
        interval=interval,
        url_exists=url_exists,
        max_workers=max_workers,
    )
    rows = tuple(
        _summarize_symbol(
            symbol=asset.binance_symbol,
            month_keys=month_keys,
            probes=month_probes[asset.binance_symbol],
            required_completed_weeks=required_completed_weeks,
            required_valid_labeled_weeks=required_valid_labeled_weeks,
            warmup_weeks=warmup_weeks,
        )
        for asset in universe.assets
    )
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    manifest_path = root / "P4_HISTORY_ELIGIBILITY_PROBE_MANIFEST.json"
    result = P4HistoryProbeResult(
        probe_id=P4_HISTORY_PROBE_ID,
        universe_id=universe.universe_id,
        universe_hash=universe.universe_hash,
        source_selection_id=universe.source_selection_id,
        interval=interval,
        start_month=month_keys[0],
        end_month=month_keys[-1],
        required_assets=required_assets,
        required_completed_weeks=required_completed_weeks,
        required_valid_labeled_weeks=required_valid_labeled_weeks,
        warmup_weeks=warmup_weeks,
        rows=rows,
        generated_at=generated_at,
        manifest_path=manifest_path,
    )
    manifest_path.write_text(
        json.dumps(history_probe_manifest_payload(result), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def history_probe_manifest_payload(result: P4HistoryProbeResult) -> dict[str, object]:
    """Return a JSON-serializable history-probe manifest."""
    return {
        "probe_id": result.probe_id,
        "universe_id": result.universe_id,
        "universe_hash": result.universe_hash,
        "source_selection_id": result.source_selection_id,
        "interval": result.interval,
        "start_month": result.start_month,
        "end_month": result.end_month,
        "required_assets": result.required_assets,
        "required_completed_weeks": result.required_completed_weeks,
        "required_valid_labeled_weeks": result.required_valid_labeled_weeks,
        "warmup_weeks": result.warmup_weeks,
        "eligible_assets": result.eligible_assets,
        "universe_eligible": result.universe_eligible,
        "gate_claim_allowed": result.gate_claim_allowed,
        "generated_at": result.generated_at.isoformat(),
        "rows": [asdict(row) for row in result.rows],
        "boundary": "eligibility_probe_not_phase_gate_evidence",
    }


def render_p4_history_probe_summary(result: P4HistoryProbeResult) -> str:
    """Render a deterministic Markdown history-probe summary."""
    lines = [
        "# P4 Extended History Eligibility Probe",
        "",
        f"Probe ID: `{result.probe_id}`",
        f"Universe ID: `{result.universe_id}`",
        f"Universe hash: `{result.universe_hash}`",
        f"Source selection ID: `{result.source_selection_id}`",
        f"Interval: `{result.interval}`",
        f"Window probed: `{result.start_month}` through `{result.end_month}`",
        f"Required assets: {result.required_assets}",
        f"Required completed weeks: {result.required_completed_weeks}",
        f"Required valid labeled weeks: {result.required_valid_labeled_weeks}",
        f"Warmup weeks: {result.warmup_weeks}",
        f"Eligible assets: {result.eligible_assets}/{result.required_assets}",
        f"Universe eligible: `{_bool(result.universe_eligible)}`",
        f"Gate claim allowed: `{_bool(result.gate_claim_allowed)}`",
        "",
        "| Symbol | Eligible | Continuous Window | Months | Est. Weeks | Est. Valid Labels | Missing Months | Reason |",
        "|--------|----------|-------------------|--------|------------|-------------------|----------------|--------|",
    ]
    for row in result.rows:
        continuous_window = (
            ""
            if row.continuous_start_month is None
            else f"{row.continuous_start_month}..{row.continuous_end_month}"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    row.symbol,
                    _bool(row.eligible),
                    continuous_window,
                    str(row.continuous_month_count),
                    str(row.estimated_completed_weeks),
                    str(row.estimated_valid_labeled_weeks),
                    ", ".join(row.missing_months),
                    row.reason_code,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Boundary: this is source-history eligibility evidence only. It does not "
            "close P4 coverage, approve Phase 0, start Phase 1, or make performance claims.",
            "",
        ]
    )
    return "\n".join(lines)


def _probe_months(
    *,
    universe: CryptoUniverseSnapshot,
    start_year: int,
    start_month: int,
    end_year: int,
    end_month: int,
    interval: str,
    url_exists: UrlExists,
    max_workers: int,
) -> dict[str, tuple[P4HistoryMonthProbe, ...]]:
    tasks: dict[Future[bool], tuple[str, int, int, str]] = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
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
                future = executor.submit(url_exists, url)
                tasks[future] = (asset.binance_symbol, year, month, url)

        by_symbol: dict[str, list[P4HistoryMonthProbe]] = {
            asset.binance_symbol: [] for asset in universe.assets
        }
        for future in as_completed(tasks):
            symbol, year, month, url = tasks[future]
            by_symbol[symbol].append(
                P4HistoryMonthProbe(
                    symbol=symbol,
                    year=year,
                    month=month,
                    url=url,
                    available=future.result(),
                )
            )
    return {
        symbol: tuple(sorted(probes, key=lambda probe: (probe.year, probe.month)))
        for symbol, probes in by_symbol.items()
    }


def _summarize_symbol(
    *,
    symbol: str,
    month_keys: Sequence[str],
    probes: Sequence[P4HistoryMonthProbe],
    required_completed_weeks: int,
    required_valid_labeled_weeks: int,
    warmup_weeks: int,
) -> P4HistorySymbolProbe:
    available_months = tuple(probe.month_key for probe in probes if probe.available)
    missing_months = tuple(probe.month_key for probe in probes if not probe.available)
    available_set = set(available_months)
    suffix = _continuous_suffix(month_keys, available_set)
    completed_weeks = _estimate_completed_weeks(suffix[0], suffix[-1]) if suffix else 0
    valid_labeled_weeks = max(0, completed_weeks - warmup_weeks)
    eligible = (
        completed_weeks >= required_completed_weeks
        and valid_labeled_weeks >= required_valid_labeled_weeks
    )
    reason_code = "pass" if eligible else "insufficient_continuous_history"
    return P4HistorySymbolProbe(
        symbol=symbol,
        available_months=available_months,
        missing_months=missing_months,
        earliest_available_month=available_months[0] if available_months else None,
        latest_available_month=available_months[-1] if available_months else None,
        continuous_start_month=suffix[0] if suffix else None,
        continuous_end_month=suffix[-1] if suffix else None,
        continuous_month_count=len(suffix),
        estimated_completed_weeks=completed_weeks,
        estimated_valid_labeled_weeks=valid_labeled_weeks,
        eligible=eligible,
        reason_code=reason_code,
    )


def _month_keys(
    start_year: int, start_month: int, end_year: int, end_month: int
) -> tuple[str, ...]:
    urls = build_binance_monthly_klines_urls(
        symbol="BTCUSDT",
        interval="1d",
        start_year=start_year,
        start_month=start_month,
        end_year=end_year,
        end_month=end_month,
    )
    return tuple(f"{year}-{month:02d}" for year, month in map(_parse_year_month_from_url, urls))


def _continuous_suffix(month_keys: Sequence[str], available_months: set[str]) -> tuple[str, ...]:
    suffix: list[str] = []
    for month_key in reversed(month_keys):
        if month_key not in available_months:
            break
        suffix.append(month_key)
    return tuple(reversed(suffix))


def _estimate_completed_weeks(start_month: str, end_month: str) -> int:
    start = _month_start(start_month)
    end_exclusive = _month_after(end_month)
    return (end_exclusive - start).days // 7


def _month_start(month_key: str) -> date:
    year, month = _parse_month_key(month_key)
    return date(year, month, 1)


def _month_after(month_key: str) -> date:
    year, month = _parse_month_key(month_key)
    if month == 12:
        return date(year + 1, 1, 1)
    return date(year, month + 1, 1)


def _parse_month_key(month_key: str) -> tuple[int, int]:
    year_text, month_text = month_key.split("-", 1)
    return int(year_text), int(month_text)


def _parse_year_month_from_url(url: str) -> tuple[int, int]:
    file_name = url.rsplit("/", 1)[-1]
    stem = file_name.removesuffix(".zip")
    return int(stem.rsplit("-", 2)[-2]), int(stem.rsplit("-", 1)[-1])


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _require_utc(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() != UTC.utcoffset(value):
        raise ValueError(f"{name} must be timezone-aware UTC")
