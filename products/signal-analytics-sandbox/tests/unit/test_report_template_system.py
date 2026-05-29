from __future__ import annotations

from datetime import UTC, datetime

from signal_sandbox.reports import (
    ReportTemplateData,
    ReportTemplateMetric,
    render_report_html_ready,
    render_report_markdown,
)
from signal_sandbox.reports.disclaimers import CANONICAL_DISCLAIMER


def test_report_template_renders_markdown_and_html_from_one_model() -> None:
    report = _report()

    markdown = render_report_markdown(report)
    html = render_report_html_ready(report)

    assert "# Three Channel V2 Report" in markdown
    assert "<h1>Three Channel V2 Report</h1>" in html
    assert "Metric coverage" in markdown
    assert "Metric coverage" in html
    assert "review coverage incomplete" in markdown
    assert "review coverage incomplete" in html
    assert CANONICAL_DISCLAIMER in markdown
    assert CANONICAL_DISCLAIMER in html


def test_report_template_html_escapes_user_visible_values() -> None:
    report = _report(
        title="Unsafe <script>",
        summary=["A | B", "x < y"],
        metric_label="Hit <rate>",
    )

    markdown = render_report_markdown(report)
    html = render_report_html_ready(report)

    assert "A \\| B" in markdown
    assert "Unsafe &lt;script&gt;" in html
    assert "x &lt; y" in html
    assert "Hit &lt;rate&gt;" in html
    assert "<script>" not in html


def _report(
    *,
    title: str = "Three Channel V2 Report",
    summary: list[str] | None = None,
    metric_label: str = "Metric coverage",
) -> ReportTemplateData:
    return ReportTemplateData(
        report_id="three-channel-v2",
        title=title,
        status="approve_internal_only",
        generated_at_utc=datetime(2026, 5, 19, tzinfo=UTC),
        summary=summary or ["Internal-only report data is stable."],
        metrics=[
            ReportTemplateMetric(
                metric_id="coverage",
                label=metric_label,
                value="170 evaluable claims",
                caveat="review coverage incomplete",
            )
        ],
        limitations=["External delivery remains blocked."],
    )
