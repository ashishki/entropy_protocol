from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = PROJECT_ROOT / "docs/pilot/reports/preclient"
CHANNELS = ("bablos79", "nemphiscrypts", "pifagortrade")


def test_preclient_channel_reports_exist_for_all_channels() -> None:
    for channel in CHANNELS:
        path = REPORT_DIR / f"{channel}_DEEP_REPORT_V0.md"
        assert path.exists(), path
        report = path.read_text(encoding="utf-8")
        assert f"# {channel} Internal Deep Report V0" in report


def test_preclient_channel_reports_stay_internal_only_with_required_citations() -> None:
    for channel in CHANNELS:
        report = (REPORT_DIR / f"{channel}_DEEP_REPORT_V0.md").read_text(
            encoding="utf-8"
        )

        assert "Status: `internal_only_deep_report_v0`" in report
        assert "Allowed audience: `internal_only`" in report
        assert "Decision: `internal_only`" in report
        assert "docs/pilot/preclient_EVIDENCE_APPENDIX.md" in report
        assert "human/operator review" in report
        assert "external gate" in report


def test_preclient_channel_reports_use_same_deep_report_outline() -> None:
    required_sections = (
        "## Executive Summary",
        "## Source And Period",
        "## Source Style",
        "## Measurable Claims",
        "## Media Findings",
        "## Setup And RR Findings",
        "## Model-Reviewed Candidates",
        "## Confirmed Example",
        "## Contradicted Example",
        "## Strengths",
        "## Weaknesses",
        "## Limitations",
        "## Report Decision",
    )

    for channel in CHANNELS:
        report = (REPORT_DIR / f"{channel}_DEEP_REPORT_V0.md").read_text(
            encoding="utf-8"
        )
        for section in required_sections:
            assert section in report


def test_preclient_channel_reports_support_strengths_and_weaknesses_with_refs() -> None:
    for channel in CHANNELS:
        report = (REPORT_DIR / f"{channel}_DEEP_REPORT_V0.md").read_text(
            encoding="utf-8"
        )
        strengths = report.split("## Strengths", maxsplit=1)[1].split(
            "## Weaknesses", maxsplit=1
        )[0]
        weaknesses = report.split("## Weaknesses", maxsplit=1)[1].split(
            "## Limitations", maxsplit=1
        )[0]

        assert strengths.count("Evidence:") >= 3
        assert weaknesses.count("Evidence:") >= 3
        assert "docs/pilot/preclient_FREE_DASHBOARD_CARDS.json" in strengths
        assert "docs/pilot/preclient_EVIDENCE_APPENDIX.md" in weaknesses
