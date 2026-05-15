"""Build artifact-first report input packs from public captures."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.capture.loader import CapturedPost, load_captures
from signal_sandbox.extraction.draft_validation import validate_pseudo_label

CAPTURE_METHOD_PUBLIC_TELEGRAM_HTML = "public_telegram_s_html"
MEDIA_STATUS_TEXT_ONLY = "text_only_no_media_artifacts"
CANONICAL_HISTORICAL_ONLY_DISCLAIMER = (
    "This report is historical research only. It is not financial advice, "
    "investment advice, trading advice, or a recommendation to buy, sell, or "
    "hold any asset."
)


class CapturePackRow(BaseModel):
    model_config = ConfigDict(strict=True)

    capture_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_label: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    capture_timestamp_utc: datetime
    source_timestamp_utc: datetime | None = None
    text_sha256: str = Field(min_length=64, max_length=64)
    raw_text_path: str = Field(min_length=1)
    capture_method: str = Field(min_length=1)
    media_status: str = Field(min_length=1)
    pseudo_label_status: str = Field(min_length=1)
    candidate_assets: list[str] = Field(default_factory=list)
    direction_candidate: str = Field(default="unknown", min_length=1)
    missing_fields: list[str] = Field(default_factory=list)
    confidence: float | None = None
    uncertainty_reason: str = ""

    @field_validator("capture_timestamp_utc", "source_timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")


class CapturePack(BaseModel):
    model_config = ConfigDict(strict=True)

    source_id: str = Field(min_length=1)
    generated_at_utc: datetime
    rows: list[CapturePackRow]

    @field_validator("generated_at_utc", mode="before")
    @classmethod
    def _coerce_generated_at(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("generated_at_utc must be a datetime or ISO-8601 string")

    def summary_counts(self) -> dict[str, int]:
        counts: Counter[str] = Counter(row.pseudo_label_status for row in self.rows)
        return dict(sorted(counts.items()))

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.model_dump_json(indent=2, by_alias=False),
            encoding="utf-8",
        )

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_capture_pack_markdown(self), encoding="utf-8")


class ReviewClosureRow(BaseModel):
    model_config = ConfigDict(strict=True)

    capture_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    source_timestamp_utc: datetime | None = None
    input_status: str = Field(min_length=1)
    final_review_status: str = Field(min_length=1)
    customer_report_eligible: bool
    reviewer_action: str = Field(min_length=1)
    candidate_assets: list[str] = Field(default_factory=list)
    direction_candidate: str = Field(min_length=1)
    missing_fields: list[str] = Field(default_factory=list)
    limitation_reason: str = ""

    @field_validator("source_timestamp_utc", mode="before")
    @classmethod
    def _coerce_source_timestamp(cls, value: object) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")


class ReviewClosurePack(BaseModel):
    model_config = ConfigDict(strict=True)

    source_id: str = Field(min_length=1)
    generated_at_utc: datetime
    rows: list[ReviewClosureRow]

    @field_validator("generated_at_utc", mode="before")
    @classmethod
    def _coerce_generated_at(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("generated_at_utc must be a datetime or ISO-8601 string")

    def summary_counts(self) -> dict[str, int]:
        counts: Counter[str] = Counter(row.final_review_status for row in self.rows)
        return dict(sorted(counts.items()))

    def eligible_count(self) -> int:
        return sum(1 for row in self.rows if row.customer_report_eligible)

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.model_dump_json(indent=2, by_alias=False),
            encoding="utf-8",
        )

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_review_closure_markdown(self), encoding="utf-8")


class OutcomePrepRow(BaseModel):
    model_config = ConfigDict(strict=True)

    capture_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    source_timestamp_utc: datetime | None = None
    outcome_status: str = Field(min_length=1)
    asset_status: str = Field(min_length=1)
    direction_status: str = Field(min_length=1)
    market_data_action: str = Field(min_length=1)
    reason: str = Field(min_length=1)

    @field_validator("source_timestamp_utc", mode="before")
    @classmethod
    def _coerce_source_timestamp(cls, value: object) -> datetime | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")


class OutcomePrepPack(BaseModel):
    model_config = ConfigDict(strict=True)

    source_id: str = Field(min_length=1)
    generated_at_utc: datetime
    rows: list[OutcomePrepRow]

    @field_validator("generated_at_utc", mode="before")
    @classmethod
    def _coerce_generated_at(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("generated_at_utc must be a datetime or ISO-8601 string")

    def summary_counts(self) -> dict[str, int]:
        counts: Counter[str] = Counter(row.outcome_status for row in self.rows)
        return dict(sorted(counts.items()))

    def market_data_fetch_count(self) -> int:
        return sum(1 for row in self.rows if row.market_data_action == "fetch_snapshot")

    def write_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            self.model_dump_json(indent=2, by_alias=False),
            encoding="utf-8",
        )

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_outcome_prep_markdown(self), encoding="utf-8")


class SourceReportInput(BaseModel):
    model_config = ConfigDict(strict=True)

    capture_pack: CapturePack
    review_pack: ReviewClosurePack
    outcome_pack: OutcomePrepPack
    generated_at_utc: datetime

    @field_validator("generated_at_utc", mode="before")
    @classmethod
    def _coerce_generated_at(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("generated_at_utc must be a datetime or ISO-8601 string")

    def write_markdown(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_source_report(self), encoding="utf-8")


def build_capture_pack(
    *,
    workspace: Path,
    source_id: str,
    pseudo_label_path: Path | None = None,
    generated_at_utc: datetime | None = None,
    capture_method: str = CAPTURE_METHOD_PUBLIC_TELEGRAM_HTML,
) -> CapturePack:
    """Load captures and optional pseudo-labels into an inspectable report pack."""

    posts = load_captures(workspace, source_id)
    pseudo_labels = _load_pseudo_labels(pseudo_label_path) if pseudo_label_path else {}
    rows = [
        _row_from_post(
            post,
            workspace=workspace,
            label=pseudo_labels.get(post.capture_id),
            capture_method=capture_method,
        )
        for post in posts
    ]
    _reject_orphan_labels(pseudo_labels, {post.capture_id for post in posts})
    return CapturePack(
        source_id=source_id,
        generated_at_utc=generated_at_utc or datetime.now(UTC),
        rows=rows,
    )


def load_capture_pack(path: Path) -> CapturePack:
    return CapturePack.model_validate_json(path.read_bytes())


def load_review_closure_pack(path: Path) -> ReviewClosurePack:
    return ReviewClosurePack.model_validate_json(path.read_bytes())


def load_outcome_prep_pack(path: Path) -> OutcomePrepPack:
    return OutcomePrepPack.model_validate_json(path.read_bytes())


def build_source_report_input(
    *,
    capture_pack: CapturePack,
    review_pack: ReviewClosurePack,
    outcome_pack: OutcomePrepPack,
    generated_at_utc: datetime | None = None,
) -> SourceReportInput:
    _assert_same_source(capture_pack.source_id, review_pack.source_id)
    _assert_same_source(capture_pack.source_id, outcome_pack.source_id)
    return SourceReportInput(
        capture_pack=capture_pack,
        review_pack=review_pack,
        outcome_pack=outcome_pack,
        generated_at_utc=generated_at_utc or datetime.now(UTC),
    )


def build_review_closure_pack(
    capture_pack: CapturePack,
    *,
    generated_at_utc: datetime | None = None,
) -> ReviewClosurePack:
    rows = [_review_row_from_capture_row(row) for row in capture_pack.rows]
    return ReviewClosurePack(
        source_id=capture_pack.source_id,
        generated_at_utc=generated_at_utc or datetime.now(UTC),
        rows=rows,
    )


def build_outcome_prep_pack(
    review_pack: ReviewClosurePack,
    *,
    generated_at_utc: datetime | None = None,
) -> OutcomePrepPack:
    return OutcomePrepPack(
        source_id=review_pack.source_id,
        generated_at_utc=generated_at_utc or datetime.now(UTC),
        rows=[_outcome_row_from_review_row(row) for row in review_pack.rows],
    )


def render_source_report(report: SourceReportInput) -> str:
    capture_counts = report.capture_pack.summary_counts()
    review_counts = report.review_pack.summary_counts()
    outcome_counts = report.outcome_pack.summary_counts()
    source_id = report.capture_pack.source_id
    lines = [
        f"# Signal Source Report V1 - {source_id}",
        "",
        f"Generated: `{report.generated_at_utc.isoformat()}`",
        "Status: internal artifact-first report draft",
        "",
        "## Disclaimer",
        "",
        CANONICAL_HISTORICAL_ONLY_DISCLAIMER,
        "",
        "## Executive Summary",
        "",
        (
            f"The `{source_id}` text-only capture window contains "
            f"{len(report.capture_pack.rows)} public Telegram text captures. "
            "The validated pseudo-label pass found no complete customer-report-"
            "eligible trade setup rows in this batch."
        ),
        "",
        "Primary finding: this source/window is currently useful as a negative "
        "or limitation artifact, not as a performance-metric report.",
        "",
        "## Source And Period",
        "",
        f"- Source ID: `{source_id}`",
        "- Source URL: `https://t.me/bablos79`",
        (
            "- Source timestamp range: "
            f"`{_format_ts(_first_timestamp(report.capture_pack.rows))}` through "
            f"`{_format_ts(_last_timestamp(report.capture_pack.rows))}`"
        ),
        "- Capture method: `public_telegram_s_html`",
        "- Media scope: text-only; no media/transcript/OCR evidence used",
        "",
        "## Corpus Coverage",
        "",
        f"- Captured text rows: {len(report.capture_pack.rows)}",
        _count_line(capture_counts, "not_a_signal"),
        _count_line(capture_counts, "insufficient_fields"),
        _count_line(capture_counts, "needs_review"),
        "",
        "## Review Queue Result",
        "",
        f"- Customer-report eligible rows: {report.review_pack.eligible_count()}",
        _count_line(review_counts, "rejected_not_market_related"),
        _count_line(review_counts, "insufficient_evidence"),
        _count_line(review_counts, "ambiguous_needs_operator_review"),
        "",
        "## Outcome Readiness",
        "",
        (
            "- Market-data fetches required now: "
            f"{report.outcome_pack.market_data_fetch_count()}"
        ),
        "- Deterministic outcome metrics computed: 0",
        _count_line(outcome_counts, "not_applicable_not_market_related"),
        _count_line(outcome_counts, "unresolved_insufficient_evidence"),
        _count_line(outcome_counts, "unresolved_operator_review_required"),
        "",
        "## Strongest Findings",
        "",
        "- The current public text window does not support defensible historical "
        "performance metrics under the validated pseudo-label result.",
        "- Most rows are classified as not market-related for report metrics.",
        "- The rows that mention assets or trade-management language still miss "
        "fields required for deterministic outcomes.",
        "",
        "## Evidence Appendix",
        "",
        "- Capture pack: `docs/pilot/bablos79_CAPTURE_PACK.md`",
        "- Review queue closure: `docs/pilot/bablos79_REVIEW_QUEUE_CLOSED.md`",
        "- Outcome prep register: `docs/pilot/bablos79_OUTCOME_PREP.md`",
        "",
        "## Limitations",
        "",
        "- No complete trade setup rows were approved for metrics in this batch.",
        "- No media evidence was used.",
        "- No private, paywalled, or login-walled source was used.",
        "- This draft is ready for operator evaluation, not external delivery.",
        "",
    ]
    return "\n".join(lines)


def render_capture_pack_markdown(pack: CapturePack) -> str:
    counts = pack.summary_counts()
    first_source_ts = _format_ts(_first_timestamp(pack.rows))
    last_source_ts = _format_ts(_last_timestamp(pack.rows))
    lines = [
        f"# Capture Pack - {pack.source_id}",
        "",
        f"Generated: `{pack.generated_at_utc.isoformat()}`",
        "Status: internal artifact-first report input",
        "",
        "## Summary",
        "",
        f"- Source ID: `{pack.source_id}`",
        f"- Captured rows: {len(pack.rows)}",
        f"- Source timestamp range: `{first_source_ts}` through `{last_source_ts}`",
        f"- Capture method: `{pack.rows[0].capture_method if pack.rows else 'none'}`",
        f"- Media status: `{MEDIA_STATUS_TEXT_ONLY}`",
        "- Approved ledger rows created: 0",
        "- Customer-facing claims created: 0",
        "",
        "## Pseudo-Label Status Counts",
        "",
    ]
    if counts:
        for status, count in counts.items():
            lines.append(f"- `{status}`: {count}")
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            (
                "| capture_id | source_ref | source_timestamp | label_status | "
                "assets | direction | missing_fields | confidence | media_status |"
            ),
            "|---|---|---|---|---|---|---|---:|---|",
        ]
    )
    for row in pack.rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.capture_id}`",
                    f"[source]({row.evidence_url})",
                    f"`{_format_ts(row.source_timestamp_utc)}`",
                    f"`{row.pseudo_label_status}`",
                    ", ".join(row.candidate_assets) or "-",
                    row.direction_candidate,
                    ", ".join(row.missing_fields) or "-",
                    f"{row.confidence:.2f}" if row.confidence is not None else "-",
                    row.media_status,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            (
                "- This pack is text-only; no local media, transcript, or OCR "
                "artifacts are attached."
            ),
            (
                "- Pseudo-label rows are validated against raw capture text but "
                "still require final operator evaluation."
            ),
            (
                "- Rows with missing entry, stop, target, direction, or asset "
                "fields must not be used for deterministic outcome metrics."
            ),
            (
                "- This pack does not create approved ledgers, reports, outcomes, "
                "or investment advice."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def render_outcome_prep_markdown(pack: OutcomePrepPack) -> str:
    counts = pack.summary_counts()
    lines = [
        f"# Outcome Prep Register - {pack.source_id}",
        "",
        f"Generated: `{pack.generated_at_utc.isoformat()}`",
        "Status: internal outcome-prep register",
        "",
        "## Summary",
        "",
        f"- Source ID: `{pack.source_id}`",
        f"- Rows assessed: {len(pack.rows)}",
        f"- Market-data fetches required now: {pack.market_data_fetch_count()}",
        "- Outcome metrics computed: 0",
        "- Customer-facing claims created: 0",
        "",
        "## Outcome Status Counts",
        "",
    ]
    for status, count in counts.items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            (
                "| capture_id | source_ref | source_timestamp | outcome_status | "
                "asset_status | direction_status | market_data_action | reason |"
            ),
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in pack.rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.capture_id}`",
                    f"[source]({row.evidence_url})",
                    f"`{_format_ts(row.source_timestamp_utc)}`",
                    f"`{row.outcome_status}`",
                    row.asset_status,
                    row.direction_status,
                    row.market_data_action,
                    row.reason,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            (
                "Market data is requested only for rows that are report-eligible "
                "and have complete measurable fields. Current unresolved rows are "
                "limitations, not failed trades."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def render_review_closure_markdown(pack: ReviewClosurePack) -> str:
    counts = pack.summary_counts()
    lines = [
        f"# Review Queue Closure - {pack.source_id}",
        "",
        f"Generated: `{pack.generated_at_utc.isoformat()}`",
        "Status: internal report-input review pack",
        "",
        "## Summary",
        "",
        f"- Source ID: `{pack.source_id}`",
        f"- Rows reviewed: {len(pack.rows)}",
        f"- Customer-report eligible rows: {pack.eligible_count()}",
        "- Approved ledger rows created: 0",
        "- Customer-facing claims created: 0",
        "",
        "## Final Review Status Counts",
        "",
    ]
    for status, count in counts.items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            (
                "| capture_id | source_ref | source_timestamp | final_review_status | "
                "eligible | assets | direction | missing_fields | reviewer_action |"
            ),
            "|---|---|---|---|---:|---|---|---|---|",
        ]
    )
    for row in pack.rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row.capture_id}`",
                    f"[source]({row.evidence_url})",
                    f"`{_format_ts(row.source_timestamp_utc)}`",
                    f"`{row.final_review_status}`",
                    "yes" if row.customer_report_eligible else "no",
                    ", ".join(row.candidate_assets) or "-",
                    row.direction_candidate,
                    ", ".join(row.missing_fields) or "-",
                    row.reviewer_action,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            (
                "This artifact closes the machine-prepared review queue for the "
                "current text-only batch. It does not approve ledger rows, compute "
                "outcomes, create report claims, or use media evidence."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def _outcome_row_from_review_row(row: ReviewClosureRow) -> OutcomePrepRow:
    if row.customer_report_eligible:
        return OutcomePrepRow(
            capture_id=row.capture_id,
            source_id=row.source_id,
            evidence_url=row.evidence_url,
            source_timestamp_utc=row.source_timestamp_utc,
            outcome_status="needs_market_snapshot",
            asset_status="candidate_present",
            direction_status="candidate_present",
            market_data_action="fetch_snapshot",
            reason="row is eligible and needs deterministic market data",
        )
    if row.final_review_status == "rejected_not_market_related":
        return OutcomePrepRow(
            capture_id=row.capture_id,
            source_id=row.source_id,
            evidence_url=row.evidence_url,
            source_timestamp_utc=row.source_timestamp_utc,
            outcome_status="not_applicable_not_market_related",
            asset_status="not_required",
            direction_status="not_required",
            market_data_action="do_not_fetch",
            reason="row excluded from report metrics as not market-related",
        )
    if row.final_review_status == "ambiguous_needs_operator_review":
        return OutcomePrepRow(
            capture_id=row.capture_id,
            source_id=row.source_id,
            evidence_url=row.evidence_url,
            source_timestamp_utc=row.source_timestamp_utc,
            outcome_status="unresolved_operator_review_required",
            asset_status=_field_status(row.candidate_assets),
            direction_status=_direction_status(row.direction_candidate),
            market_data_action="do_not_fetch",
            reason="operator review required before outcome preparation",
        )
    return OutcomePrepRow(
        capture_id=row.capture_id,
        source_id=row.source_id,
        evidence_url=row.evidence_url,
        source_timestamp_utc=row.source_timestamp_utc,
        outcome_status="unresolved_insufficient_evidence",
        asset_status=_field_status(row.candidate_assets),
        direction_status=_direction_status(row.direction_candidate),
        market_data_action="do_not_fetch",
        reason="missing fields block deterministic outcome metrics",
    )


def _row_from_post(
    post: CapturedPost,
    *,
    workspace: Path,
    label: Mapping[str, Any] | None,
    capture_method: str,
) -> CapturePackRow:
    if label is not None:
        validate_pseudo_label(post, label)
    candidate_fields = _mapping(label.get("candidate_fields")) if label else {}
    return CapturePackRow(
        capture_id=post.capture_id,
        source_id=post.source_id,
        source_label=post.source_id,
        evidence_url=post.evidence_url,
        capture_timestamp_utc=post.capture_timestamp_utc,
        source_timestamp_utc=label.get("source_timestamp_utc") if label else None,
        text_sha256=post.text_sha256,
        raw_text_path=str(
            workspace / "captures" / post.source_id / f"{post.capture_id}.json"
        ),
        capture_method=capture_method,
        media_status=MEDIA_STATUS_TEXT_ONLY,
        pseudo_label_status=(
            str(label.get("suggested_status")) if label else "unlabeled"
        ),
        candidate_assets=_string_list(candidate_fields.get("asset_candidates")),
        direction_candidate=str(candidate_fields.get("direction_candidate", "unknown")),
        missing_fields=_string_list(label.get("missing_fields")) if label else [],
        confidence=(
            float(label["confidence"]) if label and "confidence" in label else None
        ),
        uncertainty_reason=str(label.get("uncertainty_reason", "")) if label else "",
    )


def _field_status(values: list[str]) -> str:
    return "candidate_present" if values else "missing"


def _direction_status(direction: str) -> str:
    return "candidate_present" if direction in {"long", "short"} else "missing"


def _review_row_from_capture_row(row: CapturePackRow) -> ReviewClosureRow:
    final_status, eligible, action, reason = _review_decision(row)
    return ReviewClosureRow(
        capture_id=row.capture_id,
        source_id=row.source_id,
        evidence_url=row.evidence_url,
        source_timestamp_utc=row.source_timestamp_utc,
        input_status=row.pseudo_label_status,
        final_review_status=final_status,
        customer_report_eligible=eligible,
        reviewer_action=action,
        candidate_assets=row.candidate_assets,
        direction_candidate=row.direction_candidate,
        missing_fields=row.missing_fields,
        limitation_reason=reason,
    )


def _review_decision(row: CapturePackRow) -> tuple[str, bool, str, str]:
    if row.pseudo_label_status == "not_a_signal":
        return (
            "rejected_not_market_related",
            False,
            "exclude_from_report_metrics",
            "pseudo-label classified row as not a market signal",
        )
    if row.pseudo_label_status == "insufficient_fields":
        return (
            "insufficient_evidence",
            False,
            "record_as_limitation_or_context",
            "required evaluable fields are missing",
        )
    if row.pseudo_label_status == "needs_review":
        return (
            "ambiguous_needs_operator_review",
            False,
            "operator_decide_before_report",
            "pseudo-label marks row as ambiguous or context-dependent",
        )
    if row.pseudo_label_status == "review_candidate" and not row.missing_fields:
        return (
            "candidate_pending_operator_final_evaluation",
            True,
            "operator_verify_for_report_input",
            "complete draft candidate requires final operator evaluation",
        )
    return (
        "unresolved",
        False,
        "inspect_before_report",
        "status is not mapped to a closed report-input category",
    )


def _load_pseudo_labels(path: Path) -> dict[str, Mapping[str, Any]]:
    labels: dict[str, Mapping[str, Any]] = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, Mapping):
            raise ValueError(f"pseudo-label line {line_number} must be a JSON object")
        capture_id = payload.get("capture_id")
        if not isinstance(capture_id, str) or not capture_id:
            raise ValueError(f"pseudo-label line {line_number} missing capture_id")
        if capture_id in labels:
            raise ValueError(f"duplicate pseudo-label for {capture_id}")
        labels[capture_id] = payload
    return labels


def _reject_orphan_labels(
    labels: Mapping[str, Mapping[str, Any]],
    capture_ids: set[str],
) -> None:
    orphaned = sorted(set(labels) - capture_ids)
    if orphaned:
        raise ValueError(f"pseudo-labels without captures: {', '.join(orphaned)}")


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _first_timestamp(rows: list[CapturePackRow]) -> datetime | None:
    timestamps = [row.source_timestamp_utc for row in rows if row.source_timestamp_utc]
    return min(timestamps) if timestamps else None


def _last_timestamp(rows: list[CapturePackRow]) -> datetime | None:
    timestamps = [row.source_timestamp_utc for row in rows if row.source_timestamp_utc]
    return max(timestamps) if timestamps else None


def _format_ts(value: datetime | None) -> str:
    return value.isoformat() if value is not None else "unknown"


def _assert_same_source(left: str, right: str) -> None:
    if left != right:
        raise ValueError(f"source mismatch: {left} != {right}")


def _count_line(counts: Mapping[str, int], status: str) -> str:
    return f"- `{status}`: {counts.get(status, 0)}"
