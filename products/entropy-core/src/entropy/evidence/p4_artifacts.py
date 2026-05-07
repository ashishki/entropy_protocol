"""P4 label-vintage artifact generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Mapping, Sequence

from entropy.governance.p4_labeler import CalendarProfile, P4Label, label_p4_regimes
from entropy.models.market import OHLCVBar

DEFAULT_REQUIRED_P4_LABELED_WEEKS = 156
DEFAULT_REQUIRED_P4_ASSETS = 15


@dataclass(frozen=True)
class P4ArtifactInput:
    """Approved local input dataset for one symbol's P4 artifact generation."""

    symbol: str
    bars: Sequence[OHLCVBar]
    calendar_profile: CalendarProfile
    dataset_hash: str


@dataclass(frozen=True)
class P4SymbolCoverage:
    """Coverage summary for one symbol's generated P4 labels."""

    symbol: str
    calendar_profile: CalendarProfile | str
    dataset_hash: str
    input_daily_bars: int
    generated_labels: int
    valid_labeled_weeks: int
    first_week_close_ts: datetime | None
    last_week_close_ts: datetime | None
    artifact_path: Path | None
    passes_required_coverage: bool
    reason_code: str


@dataclass(frozen=True)
class P4CoverageSummary:
    """Aggregate P4 coverage result."""

    rows: tuple[P4SymbolCoverage, ...]
    passing_assets: int
    required_assets: int
    required_labeled_weeks: int
    gate_evidence_complete: bool
    summary_path: Path


def generate_p4_label_artifacts(
    *,
    datasets: Mapping[str, P4ArtifactInput],
    target_universe: Sequence[str],
    output_dir: Path | str,
    label_generation_ts: datetime,
    required_assets: int = DEFAULT_REQUIRED_P4_ASSETS,
    required_labeled_weeks: int = DEFAULT_REQUIRED_P4_LABELED_WEEKS,
) -> P4CoverageSummary:
    """Write deterministic P4 label artifacts and a coverage summary."""
    _require_utc(label_generation_ts, "label_generation_ts")
    if required_assets < 1:
        raise ValueError("required_assets must be positive")
    if required_labeled_weeks < 1:
        raise ValueError("required_labeled_weeks must be positive")

    universe = _normalize_universe(target_universe)
    root = Path(output_dir)
    labels_dir = root / "labels"
    labels_dir.mkdir(parents=True, exist_ok=True)

    rows: list[P4SymbolCoverage] = []
    for symbol in universe:
        dataset = datasets.get(symbol)
        if dataset is None:
            rows.append(_missing_symbol_row(symbol))
            continue
        if dataset.symbol != symbol:
            raise ValueError("dataset symbol must match target_universe symbol")

        labels = label_p4_regimes(
            symbol=symbol,
            bars=dataset.bars,
            calendar_profile=dataset.calendar_profile,
            dataset_hash=dataset.dataset_hash,
            label_generation_ts=label_generation_ts,
        )
        artifact_path = labels_dir / f"{_safe_symbol(symbol)}_p4_labels.jsonl"
        _write_label_jsonl(artifact_path, labels)
        valid_labeled_weeks = sum(1 for label in labels if label.p4_state != "UNLABELED")
        passes = valid_labeled_weeks >= required_labeled_weeks
        rows.append(
            P4SymbolCoverage(
                symbol=symbol,
                calendar_profile=dataset.calendar_profile,
                dataset_hash=dataset.dataset_hash,
                input_daily_bars=len(dataset.bars),
                generated_labels=len(labels),
                valid_labeled_weeks=valid_labeled_weeks,
                first_week_close_ts=labels[0].week_close_ts if labels else None,
                last_week_close_ts=labels[-1].week_close_ts if labels else None,
                artifact_path=artifact_path,
                passes_required_coverage=passes,
                reason_code="pass" if passes else "insufficient_labeled_weeks",
            )
        )

    passing_assets = sum(1 for row in rows if row.passes_required_coverage)
    summary_path = root / "P4_COVERAGE_SUMMARY.md"
    summary = P4CoverageSummary(
        rows=tuple(rows),
        passing_assets=passing_assets,
        required_assets=required_assets,
        required_labeled_weeks=required_labeled_weeks,
        gate_evidence_complete=passing_assets >= required_assets,
        summary_path=summary_path,
    )
    summary_path.write_text(render_p4_coverage_summary(summary), encoding="utf-8")
    return summary


def render_p4_coverage_summary(summary: P4CoverageSummary) -> str:
    """Render deterministic Markdown coverage summary."""
    lines = [
        "# P4 Label Coverage Summary",
        "",
        "Status: IMPLEMENTATION_EVIDENCE_ONLY",
        f"Gate evidence complete: {_bool(summary.gate_evidence_complete)}",
        f"Passing assets: {summary.passing_assets}/{summary.required_assets}",
        f"Required labeled weeks per passing asset: {summary.required_labeled_weeks}",
        "",
        "| Symbol | Calendar | Dataset Hash | Daily Bars | Labels | Valid Labeled Weeks | Pass | Reason | Artifact |",
        "|--------|----------|--------------|------------|--------|---------------------|------|--------|----------|",
    ]
    for row in summary.rows:
        artifact = "" if row.artifact_path is None else row.artifact_path.as_posix()
        lines.append(
            "| "
            + " | ".join(
                [
                    row.symbol,
                    str(row.calendar_profile),
                    row.dataset_hash,
                    str(row.input_daily_bars),
                    str(row.generated_labels),
                    str(row.valid_labeled_weeks),
                    _bool(row.passes_required_coverage),
                    row.reason_code,
                    artifact,
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _write_label_jsonl(path: Path, labels: Sequence[P4Label]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for label in labels:
            handle.write(json.dumps(_label_payload(label), sort_keys=True) + "\n")


def _label_payload(label: P4Label) -> dict[str, str]:
    return {
        "symbol": label.symbol,
        "calendar_profile": label.calendar_profile,
        "week_close_ts": label.week_close_ts.isoformat(),
        "p4_state": label.p4_state,
        "p4_version": label.p4_version,
        "p4_param_hash": label.p4_param_hash,
        "label_generation_ts": label.label_generation_ts.isoformat(),
        "dataset_hash": label.dataset_hash,
        "p4_weekly_resample_version": label.p4_weekly_resample_version,
    }


def _normalize_universe(target_universe: Sequence[str]) -> tuple[str, ...]:
    if not target_universe:
        raise ValueError("target_universe must not be empty")
    symbols: list[str] = []
    seen: set[str] = set()
    for symbol in target_universe:
        normalized = symbol.strip()
        if not normalized:
            raise ValueError("target_universe symbols must not be blank")
        if normalized in seen:
            raise ValueError("target_universe symbols must be unique")
        seen.add(normalized)
        symbols.append(normalized)
    return tuple(symbols)


def _missing_symbol_row(symbol: str) -> P4SymbolCoverage:
    return P4SymbolCoverage(
        symbol=symbol,
        calendar_profile="missing",
        dataset_hash="missing",
        input_daily_bars=0,
        generated_labels=0,
        valid_labeled_weeks=0,
        first_week_close_ts=None,
        last_week_close_ts=None,
        artifact_path=None,
        passes_required_coverage=False,
        reason_code="missing_dataset",
    )


def _safe_symbol(symbol: str) -> str:
    return "".join(
        character if character.isalnum() or character in ("-", "_") else "_" for character in symbol
    )


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _require_utc(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() != timedelta(0):
        raise ValueError(f"{name} must be timezone-aware UTC")
