from __future__ import annotations

import csv
import re
from pathlib import Path

EVIDENCE_LOG = Path("docs/PILOT_EVIDENCE_LOG_RU.md")
CUSTOMER_LOG = Path("templates/pilot_customer_log.csv")

REQUIRED_FIELDS = (
    "prospect_source",
    "icp",
    "call_date",
    "export_provided",
    "rules_provided",
    "paid_amount",
    "objections",
    "report_delivered",
    "repeat_requested",
    "referral",
)


def test_evidence_log_documents_required_business_fields() -> None:
    text = EVIDENCE_LOG.read_text(encoding="utf-8").casefold()

    for field in REQUIRED_FIELDS:
        assert field in text
    assert "qualified prospect" in text
    assert "manual audit" in text
    assert "non-sensitive objections" in text


def test_customer_log_template_contains_required_columns_only() -> None:
    rows = list(csv.reader(CUSTOMER_LOG.read_text(encoding="utf-8").splitlines()))

    assert rows == [list(REQUIRED_FIELDS)]
    text = CUSTOMER_LOG.read_text(encoding="utf-8")
    forbidden_patterns = (
        re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
        re.compile(r"@[A-Za-z][A-Za-z0-9_]{4,}"),
        re.compile(r"\b(?:account|acct)[-_ ]?\d{4,}\b", re.I),
        re.compile(r"\b\d{6,}\b"),
    )
    for pattern in forbidden_patterns:
        assert pattern.search(text) is None


def test_evidence_log_records_advancement_gate() -> None:
    text = " ".join(EVIDENCE_LOG.read_text(encoding="utf-8").casefold().split())

    required_gate_phrases = (
        "3 paid audit reports",
        "10 qualified prospects",
        "within 14 days",
        "2 repeat audit commitments",
        "within 30 days",
    )
    for phrase in required_gate_phrases:
        assert phrase in text
