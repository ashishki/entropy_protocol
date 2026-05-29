from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_three_channel_v1_report_contains_metrics_examples_and_limits() -> None:
    report = (
        PROJECT_ROOT / "docs/pilot/reports/three_channel_V1_CHANNEL_UTILITY_REPORT.md"
    ).read_text(encoding="utf-8")

    for required in (
        "V1 Metric Summary",
        "Confirmed Examples",
        "Contradicted Examples",
        "What Changed From V0",
        "Limitations",
        "not investment advice",
        "not a promise of future performance",
    ):
        assert required in report


def test_three_channel_v1_external_gate_blocks_external_delivery() -> None:
    gate = (
        PROJECT_ROOT / "docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md"
    ).read_text(encoding="utf-8")

    assert "Decision: approve_internal_only" in gate
    assert "not approved for external/customer-facing delivery" in gate
    assert "No advice/future-profit claims | pass" in gate
    assert "Multimodal posture | blocked" in gate
    assert "Paid external delivery" in gate
