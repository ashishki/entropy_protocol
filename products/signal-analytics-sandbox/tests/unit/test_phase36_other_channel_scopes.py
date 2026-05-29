from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_nemphiscrypts_phase36_scope_records_coverage_media_and_next_steps() -> None:
    scope = (
        PROJECT_ROOT / "docs/pilot/nemphiscrypts_PHASE36_CORPUS_COMPLETION_SCOPE.md"
    ).read_text(encoding="utf-8")

    for required in (
        "Public text rows | 514",
        "V1 evaluable claims | 49",
        "0 acquired audio refs",
        "not_audited_in_phase36_yet",
        "media linkage queue for `nemphiscrypts`",
    ):
        assert required in scope


def test_pifagortrade_phase36_scope_records_coverage_media_and_next_steps() -> None:
    scope = (
        PROJECT_ROOT / "docs/pilot/pifagortrade_PHASE36_CORPUS_COMPLETION_SCOPE.md"
    ).read_text(encoding="utf-8")

    for required in (
        "Public text rows | 492",
        "V1 evaluable claims | 107",
        "Explicit setup candidates | 43",
        "not_audited_in_phase36_yet",
        "media linkage queue for `pifagortrade`",
    ):
        assert required in scope


def test_other_channel_scopes_use_same_impact_and_truth_model() -> None:
    for relative_path in (
        "docs/pilot/nemphiscrypts_PHASE36_CORPUS_COMPLETION_SCOPE.md",
        "docs/pilot/pifagortrade_PHASE36_CORPUS_COMPLETION_SCOPE.md",
    ):
        scope = (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")
        for required in (
            "signal performance",
            "trend sense",
            "insight depth",
            "methodology",
            "risk management",
            "practical usefulness",
            "creativity/differentiation",
            "evidence confidence",
            "author-statement truth",
            "market-outcome truth",
            "product-conclusion truth",
            "Do not count provider gaps or unsupported proxies as losses",
        ):
            assert required in scope
