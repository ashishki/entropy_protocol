"""Evidence appendix rendering for report metric rows."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class EvidenceAppendixMetricRow(BaseModel):
    model_config = ConfigDict(strict=True)

    metric_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    value: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    snapshot_id: str = Field(min_length=1)
    review_decision_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)


class EvidenceAppendix(BaseModel):
    model_config = ConfigDict(strict=True)

    report_id: str = Field(min_length=1)
    metric_rows: list[EvidenceAppendixMetricRow] = Field(min_length=1)


def render_evidence_appendix_markdown(appendix: EvidenceAppendix) -> str:
    lines = [
        f"# Evidence Appendix: {appendix.report_id}",
        "",
        (
            "| metric_id | label | value | source_ref | provider | snapshot_id | "
            "review_decision_id | evidence_url |"
        ),
        "|---|---|---:|---|---|---|---|---|",
        *_metric_rows(appendix.metric_rows),
        "",
    ]
    return "\n".join(lines)


def _metric_rows(rows: list[EvidenceAppendixMetricRow]) -> list[str]:
    return [
        " | ".join(
            [
                f"| `{_escape(row.metric_id)}`",
                _escape(row.label),
                _escape(row.value),
                f"`{_escape(row.source_ref)}`",
                _escape(row.provider),
                f"`{_escape(row.snapshot_id)}`",
                f"`{_escape(row.review_decision_id)}`",
                f"{_escape(row.evidence_url)} |",
            ]
        )
        for row in sorted(rows, key=lambda item: item.metric_id)
    ]


def _escape(value: str) -> str:
    return value.replace("|", "\\|")
