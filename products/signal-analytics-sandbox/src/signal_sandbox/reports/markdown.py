"""Deterministic Markdown report rendering."""

from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Sequence

from signal_sandbox.ledger.record import SignalRecord, compute_dedup_key
from signal_sandbox.outcomes.aggregate import SummaryRecord
from signal_sandbox.outcomes.matcher import (
    Outcome,
    OutcomeRecord,
    outcomes_parquet_bytes,
)
from signal_sandbox.prices.base import PriceSnapshot
from signal_sandbox.reports.disclaimers import CANONICAL_DISCLAIMER
from signal_sandbox.sources.manifest import SourceManifest


class ReportError(Exception):
    """Base exception for report rendering failures."""


class DisclaimerMissing(ReportError):
    """Raised when the canonical disclaimer is missing or duplicated."""


class PrototypeSnapshotNotAccepted(ReportError):
    """Raised when a prototype price snapshot is rendered without approval."""


def render_markdown_report(
    *,
    manifest: SourceManifest,
    ledger_records: Sequence[SignalRecord],
    snapshot: PriceSnapshot,
    outcomes: Sequence[OutcomeRecord],
    summary: SummaryRecord,
    ledger_sha256: str,
    accept_prototype_prices: bool = False,
) -> str:
    if snapshot.provider_status == "prototype" and not accept_prototype_prices:
        raise PrototypeSnapshotNotAccepted("prototype price snapshot not accepted")

    records_by_key = {compute_dedup_key(record): record for record in ledger_records}
    ordered_outcomes = sorted(
        outcomes,
        key=lambda row: (row.extracted_timestamp_utc.isoformat(), row.dedup_key),
    )
    evaluated = [outcome for outcome in ordered_outcomes if not _is_excluded(outcome)]
    excluded = [outcome for outcome in ordered_outcomes if _is_excluded(outcome)]
    report = "\n".join(
        [
            f"# Signal Analytics Report: {_escape(manifest.source_id)}",
            "",
            "## Disclaimer",
            "",
            CANONICAL_DISCLAIMER,
            "",
            "## Source",
            "",
            f"- Source URL: {_escape(manifest.source_url)}",
            f"- Source type: {manifest.source_type.value}",
            f"- Eligibility: {manifest.eligibility_verdict.value}",
            "",
            "## Provenance",
            "",
            f"- Provider: {snapshot.provider_id}",
            f"- Snapshot as_of_utc: {snapshot.as_of_utc.isoformat()}",
            f"- Snapshot SHA-256: {snapshot.sha256}",
            f"- Ledger SHA-256: {ledger_sha256}",
            f"- Outcomes SHA-256: {_sha256(outcomes_parquet_bytes(outcomes))}",
            f"- Summary SHA-256: {_sha256(summary.canonical_json_bytes())}",
            "",
            *_prototype_warning(snapshot),
            "## Historical Summary",
            "",
            f"- Total signals: {summary.total_signals}",
            f"- Evaluated signals: {summary.evaluated_signals}",
            f"- Historical wins: {summary.historical_wins}",
            f"- Historical losses: {summary.historical_losses}",
            f"- Historical timeouts: {summary.historical_timeouts}",
            f"- Historical win rate: {summary.historical_win_rate}",
            f"- Historical mean return pct: {summary.historical_mean_return_pct}",
            f"- Historical median return pct: {summary.historical_median_return_pct}",
            f"- Historical max drawdown pct: {summary.historical_max_drawdown_pct}",
            "",
            "## Per-Signal Outcomes",
            "",
            (
                "| dedup_key | outcome | return_pct | evidence_url | "
                "capture_timestamp_utc | text_sha256 |"
            ),
            "|---|---|---:|---|---|---|",
            *_outcome_rows(evaluated, records_by_key),
            "",
            "## Excluded Signals",
            "",
            *_excluded_counts(excluded),
            "",
            (
                "| dedup_key | exclusion_reason | evidence_url | "
                "capture_timestamp_utc | text_sha256 |"
            ),
            "|---|---|---|---|---|",
            *_excluded_rows(excluded, records_by_key),
            "",
        ]
    )
    validate_disclaimer(report)
    return report


def validate_disclaimer(report: str) -> None:
    if report.count(CANONICAL_DISCLAIMER) != 1:
        raise DisclaimerMissing("canonical disclaimer must appear exactly once")


def _is_excluded(outcome: OutcomeRecord) -> bool:
    return outcome.outcome.value.startswith("excluded_")


def _outcome_rows(
    outcomes: Sequence[OutcomeRecord],
    records_by_key: dict[str, SignalRecord],
) -> list[str]:
    return [
        _outcome_row(outcome, records_by_key[outcome.dedup_key]) for outcome in outcomes
    ]


def _outcome_row(outcome: OutcomeRecord, record: SignalRecord) -> str:
    return " | ".join(
        [
            f"| `{outcome.dedup_key}`",
            outcome.outcome.value,
            _decimal_text(outcome.return_pct),
            _escape(record.evidence_url),
            record.capture_timestamp_utc.isoformat(),
            f"`{record.text_sha256}` |",
        ]
    )


def _excluded_counts(outcomes: Sequence[OutcomeRecord]) -> list[str]:
    counts = Counter(outcome.outcome.value for outcome in outcomes)
    return [
        (
            f"- {Outcome.EXCLUDED_AMBIGUOUS.value}: "
            f"{counts[Outcome.EXCLUDED_AMBIGUOUS.value]}"
        ),
        (
            f"- {Outcome.EXCLUDED_NO_PRICE.value}: "
            f"{counts[Outcome.EXCLUDED_NO_PRICE.value]}"
        ),
    ]


def _excluded_rows(
    outcomes: Sequence[OutcomeRecord],
    records_by_key: dict[str, SignalRecord],
) -> list[str]:
    return [
        _excluded_row(outcome, records_by_key[outcome.dedup_key])
        for outcome in outcomes
    ]


def _excluded_row(outcome: OutcomeRecord, record: SignalRecord) -> str:
    return " | ".join(
        [
            f"| `{outcome.dedup_key}`",
            outcome.outcome.value,
            _escape(record.evidence_url),
            record.capture_timestamp_utc.isoformat(),
            f"`{record.text_sha256}` |",
        ]
    )


def _prototype_warning(snapshot: PriceSnapshot) -> list[str]:
    if snapshot.provider_status != "prototype":
        return []
    return [
        "## Prototype Price Source Warning",
        "",
        "This report used a prototype price snapshot accepted by the operator.",
        "",
    ]


def _decimal_text(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _escape(value: str) -> str:
    return value.replace("|", "\\|")
