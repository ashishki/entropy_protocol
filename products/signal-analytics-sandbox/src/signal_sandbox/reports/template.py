"""Shared report template data model and renderers."""

from __future__ import annotations

from datetime import datetime
from html import escape as html_escape

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.reports.disclaimers import CANONICAL_DISCLAIMER


class ReportTemplateMetric(BaseModel):
    model_config = ConfigDict(strict=True)

    metric_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    value: str = Field(min_length=1)
    caveat: str = Field(default="")


class ReportTemplateData(BaseModel):
    model_config = ConfigDict(strict=True)

    report_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: str = Field(min_length=1)
    generated_at_utc: datetime
    summary: list[str] = Field(default_factory=list)
    metrics: list[ReportTemplateMetric] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


def render_report_markdown(report: ReportTemplateData) -> str:
    lines = [
        f"# {report.title}",
        "",
        f"- Report ID: `{report.report_id}`",
        f"- Status: `{report.status}`",
        f"- Generated at UTC: `{report.generated_at_utc.isoformat()}`",
        "",
        "## Disclaimer",
        "",
        CANONICAL_DISCLAIMER,
        "",
        "## Summary",
        "",
        *_markdown_list(report.summary),
        "",
        "## Metrics",
        "",
        "| metric_id | label | value | caveat |",
        "|---|---|---:|---|",
        *_markdown_metric_rows(report.metrics),
        "",
        "## Limitations",
        "",
        *_markdown_list(report.limitations),
        "",
    ]
    return "\n".join(lines)


def render_report_html_ready(report: ReportTemplateData) -> str:
    summary_items = "".join(f"<li>{html_escape(item)}</li>" for item in report.summary)
    limitation_items = "".join(
        f"<li>{html_escape(item)}</li>" for item in report.limitations
    )
    metric_rows = "".join(_html_metric_row(metric) for metric in report.metrics)
    return "\n".join(
        [
            '<article class="report">',
            f"  <h1>{html_escape(report.title)}</h1>",
            "  <dl>",
            f"    <dt>Report ID</dt><dd>{html_escape(report.report_id)}</dd>",
            f"    <dt>Status</dt><dd>{html_escape(report.status)}</dd>",
            (
                "    <dt>Generated at UTC</dt><dd>"
                f"{html_escape(report.generated_at_utc.isoformat())}</dd>"
            ),
            "  </dl>",
            "  <section>",
            "    <h2>Disclaimer</h2>",
            f"    <p>{html_escape(CANONICAL_DISCLAIMER)}</p>",
            "  </section>",
            "  <section>",
            "    <h2>Summary</h2>",
            f"    <ul>{summary_items}</ul>",
            "  </section>",
            "  <section>",
            "    <h2>Metrics</h2>",
            (
                "    <table><thead><tr><th>metric_id</th><th>label</th>"
                "<th>value</th><th>caveat</th></tr></thead>"
                f"<tbody>{metric_rows}</tbody></table>"
            ),
            "  </section>",
            "  <section>",
            "    <h2>Limitations</h2>",
            f"    <ul>{limitation_items}</ul>",
            "  </section>",
            "</article>",
        ]
    )


def _markdown_list(items: list[str]) -> list[str]:
    if not items:
        return ["- none"]
    return [f"- {_escape_markdown_cell(item)}" for item in items]


def _markdown_metric_rows(metrics: list[ReportTemplateMetric]) -> list[str]:
    if not metrics:
        return ["| none | none | 0 | none |"]
    return [
        " | ".join(
            [
                f"| `{_escape_markdown_cell(metric.metric_id)}`",
                _escape_markdown_cell(metric.label),
                _escape_markdown_cell(metric.value),
                f"{_escape_markdown_cell(metric.caveat or 'none')} |",
            ]
        )
        for metric in metrics
    ]


def _html_metric_row(metric: ReportTemplateMetric) -> str:
    return (
        "<tr>"
        f"<td>{html_escape(metric.metric_id)}</td>"
        f"<td>{html_escape(metric.label)}</td>"
        f"<td>{html_escape(metric.value)}</td>"
        f"<td>{html_escape(metric.caveat or 'none')}</td>"
        "</tr>"
    )


def _escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")
