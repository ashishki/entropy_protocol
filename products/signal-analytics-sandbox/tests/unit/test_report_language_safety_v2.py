from __future__ import annotations

import json
from pathlib import Path

from signal_sandbox.reports import ReportSafetyCategory, check_report_language_safety

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = (
    PROJECT_ROOT / "docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md"
)
SAFETY_PATH = (
    PROJECT_ROOT / "docs/pilot/reports/three_channel_V1_REPORT_LANGUAGE_SAFETY.json"
)


def test_report_language_safety_passes_current_v1_report() -> None:
    report = REPORT_PATH.read_text(encoding="utf-8")
    result = check_report_language_safety(report)

    assert result.passed is True
    assert result.findings == []
    assert all(result.required_context_present.values())


def test_report_language_safety_blocks_advice_profit_and_ranking_language() -> None:
    unsafe_report = """
# Unsafe Report

Decision: approve_internal_only

## Limitations

https://t.me/example/1
This report is not approved for external/customer-facing delivery.
Audio, OCR, and chart claims remain excluded from customer-facing metrics.
You should buy BTC now because this is the best channel and will profit.
"""

    result = check_report_language_safety(unsafe_report)
    categories = {finding.category for finding in result.findings}

    assert result.passed is False
    assert ReportSafetyCategory.ADVICE in categories
    assert ReportSafetyCategory.FUTURE_PROFIT in categories
    assert ReportSafetyCategory.UNSUPPORTED_RANKING in categories


def test_report_language_safety_artifact_records_gate_and_media_context() -> None:
    report = REPORT_PATH.read_text(encoding="utf-8")
    artifact = json.loads(SAFETY_PATH.read_text(encoding="utf-8"))

    assert artifact["status"] == "pass"
    assert artifact["external_delivery_approved"] is False
    assert artifact["result"]["passed"] is True
    assert artifact["result"]["required_context_present"]["gate_status"] is True
    assert artifact["result"]["required_context_present"]["media_exclusion"] is True
    assert "Decision: approve_internal_only" in report
    assert "not approved for external/customer-facing delivery" in report
    assert "Audio, OCR, and chart claims remain excluded" in report
