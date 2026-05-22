"""Report rendering package."""

from signal_sandbox.reports.author_market import (
    AuthorMarketReport,
    EvidenceExample,
    IdeaTaxonomyRow,
    MarketSnapshotProvenance,
    MissingReportProvenance,
    OutcomeCategory,
    OutcomeMetricRow,
    SourceDocumentProvenance,
    render_author_market_report,
)
from signal_sandbox.reports.evidence_appendix import (
    EvidenceAppendix,
    EvidenceAppendixMetricRow,
    render_evidence_appendix_markdown,
)
from signal_sandbox.reports.safety import (
    ReportSafetyCategory,
    ReportSafetyFinding,
    ReportSafetyResult,
    check_report_language_safety,
)
from signal_sandbox.reports.template import (
    ReportTemplateData,
    ReportTemplateMetric,
    render_report_html_ready,
    render_report_markdown,
)
from signal_sandbox.reports.wording import (
    ALLOWED_CONTEXT_PHRASES,
    FORBIDDEN_WORDING_RULES,
    WordingCategory,
    WordingFinding,
    WordingRule,
    find_forbidden_wording,
    is_customer_safe_wording,
)

__all__ = [
    "AuthorMarketReport",
    "ALLOWED_CONTEXT_PHRASES",
    "EvidenceAppendix",
    "EvidenceAppendixMetricRow",
    "EvidenceExample",
    "FORBIDDEN_WORDING_RULES",
    "IdeaTaxonomyRow",
    "MarketSnapshotProvenance",
    "MissingReportProvenance",
    "OutcomeCategory",
    "OutcomeMetricRow",
    "ReportSafetyCategory",
    "ReportSafetyFinding",
    "ReportSafetyResult",
    "ReportTemplateData",
    "ReportTemplateMetric",
    "SourceDocumentProvenance",
    "WordingCategory",
    "WordingFinding",
    "WordingRule",
    "check_report_language_safety",
    "find_forbidden_wording",
    "is_customer_safe_wording",
    "render_author_market_report",
    "render_evidence_appendix_markdown",
    "render_report_html_ready",
    "render_report_markdown",
]
