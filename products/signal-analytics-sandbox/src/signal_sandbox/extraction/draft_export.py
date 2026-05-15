"""Draft export helpers for review-only extraction suggestions."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from signal_sandbox.capture.loader import CapturedPost
from signal_sandbox.extraction.draft_parser import parse_draft


@dataclass(frozen=True)
class DraftExportRow:
    capture_id: str
    source_timestamp_utc: str | None
    suggested_status: str
    candidate_fields: dict[str, object]
    missing_fields: list[str]
    reason_codes: list[str]
    confidence: float
    evidence_url: str
    text_sha256: str
    reviewer_id: str = "pending"


def load_profile(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def export_draft_rows(
    posts: Sequence[CapturedPost],
    profile: Mapping[str, Any],
    *,
    source_timestamps: Mapping[str, str] | None = None,
) -> list[DraftExportRow]:
    timestamps = source_timestamps or {}
    rows: list[DraftExportRow] = []
    sorted_posts = sorted(
        posts,
        key=lambda item: (item.capture_timestamp_utc, item.capture_id),
    )
    for post in sorted_posts:
        draft = parse_draft(post, profile)
        rows.append(
            DraftExportRow(
                capture_id=draft.capture_id,
                source_timestamp_utc=timestamps.get(draft.capture_id),
                suggested_status=draft.suggested_status,
                candidate_fields=draft.candidate_fields,
                missing_fields=draft.missing_required_fields,
                reason_codes=draft.reason_codes,
                confidence=draft.confidence,
                evidence_url=draft.evidence_url,
                text_sha256=draft.text_sha256,
            )
        )
    return sorted(
        rows,
        key=lambda row: (row.source_timestamp_utc or "", row.capture_id),
    )


def render_draft_markdown(rows: Sequence[DraftExportRow]) -> str:
    lines = [
        "# bablos79 Extraction Drafts - Review Pending",
        "",
        "Status: draft-only, unapproved export",
        "",
        "These rows are parser suggestions for human review. They are not approved "
        "ledger records and must not be used for performance metrics or "
        "customer-facing claims until reviewed.",
        "",
        "| capture_id | source_timestamp_utc | suggested_status | assets | "
        "direction | entry | stop | target | missing_fields | reason_codes | "
        "confidence | reviewer_id | evidence_url | text_sha256 |",
        "|------------|----------------------|------------------|--------|"
        "-----------|-------|------|--------|----------------|--------------|"
        "------------|-------------|--------------|-------------|",
    ]
    for row in rows:
        fields = row.candidate_fields
        lines.append(
            "| "
            f"`{row.capture_id}` | "
            f"{_cell(row.source_timestamp_utc)} | "
            f"`{row.suggested_status}` | "
            f"{_cell(fields.get('asset_candidates'))} | "
            f"{_cell(fields.get('direction_candidate'))} | "
            f"{_cell(fields.get('entry_candidate'))} | "
            f"{_cell(fields.get('stop_candidate'))} | "
            f"{_cell(fields.get('target_candidate'))} | "
            f"{_cell(row.missing_fields)} | "
            f"{_cell(row.reason_codes)} | "
            f"{row.confidence:.2f} | "
            f"`{row.reviewer_id}` | "
            f"{row.evidence_url} | "
            f"`{row.text_sha256}` |"
        )
    return "\n".join(lines) + "\n"


def write_draft_markdown(path: Path, rows: Sequence[DraftExportRow]) -> None:
    path.write_text(render_draft_markdown(rows), encoding="utf-8")


def _cell(value: object) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "-"
    return str(value).replace("|", "\\|").replace("\n", "<br>")
