from __future__ import annotations

import pytest
from pydantic import ValidationError

from signal_sandbox.reports import (
    EvidenceAppendix,
    EvidenceAppendixMetricRow,
    render_evidence_appendix_markdown,
)


def test_evidence_appendix_links_every_metric_to_required_evidence() -> None:
    appendix = EvidenceAppendix(
        report_id="three-channel-v2",
        metric_rows=[
            EvidenceAppendixMetricRow(
                metric_id="hit-rate-bablos79",
                label="Hit rate",
                value="64.285714%",
                source_ref="bablos79:claim_001",
                provider="moex_iss",
                snapshot_id="moex-bablos79-v1",
                review_decision_id="review-bablos79-001",
                evidence_url="https://t.me/bablos79/10257",
            )
        ],
    )

    rendered = render_evidence_appendix_markdown(appendix)

    assert "# Evidence Appendix: three-channel-v2" in rendered
    assert "`hit-rate-bablos79`" in rendered
    assert "`bablos79:claim_001`" in rendered
    assert "moex_iss" in rendered
    assert "`moex-bablos79-v1`" in rendered
    assert "`review-bablos79-001`" in rendered
    assert "https://t.me/bablos79/10257" in rendered


def test_evidence_appendix_rejects_metric_rows_without_review_decision() -> None:
    with pytest.raises(ValidationError):
        EvidenceAppendixMetricRow(
            metric_id="hit-rate-bablos79",
            label="Hit rate",
            value="64.285714%",
            source_ref="bablos79:claim_001",
            provider="moex_iss",
            snapshot_id="moex-bablos79-v1",
            review_decision_id="",
            evidence_url="https://t.me/bablos79/10257",
        )
