from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = PROJECT_ROOT / "docs/pilot/three_channel_V1_APPROVAL_MATRIX.md"


def test_three_channel_v1_approval_matrix_covers_all_channels() -> None:
    matrix = MATRIX_PATH.read_text(encoding="utf-8")

    for channel in ("bablos79", "nemphiscrypts", "pifagortrade"):
        assert f"`{channel}`" in matrix

    assert "Approved evaluator types" in matrix
    assert "Allowed claim types" in matrix
    assert "Default horizons" in matrix
    assert "Provider/proxy rules" in matrix
    assert "Exclusion statuses" in matrix


def test_three_channel_v1_approval_matrix_marks_v0_provider_classes() -> None:
    matrix = MATRIX_PATH.read_text(encoding="utf-8")

    for provider_class in (
        "Binance public daily klines",
        "MOEX ISS public daily share candles",
        "Futures-style proxies",
        "FX/currency proxies",
        "US ETF/fund proxies",
        "Commodity proxies",
        "Ambiguous/local aliases",
    ):
        assert provider_class in matrix

    assert "approved_internal_v1" in matrix
    assert "needs_operator_input" in matrix
    assert "rejected_until_mapped" in matrix


def test_three_channel_v1_approval_matrix_blocks_external_v0_use() -> None:
    matrix = MATRIX_PATH.read_text(encoding="utf-8")

    assert "V0 metrics are internal until V1 review and external gate pass" in matrix
    assert "This matrix does not approve external delivery" in matrix
    assert "No investment advice" not in matrix
    assert "Investment advice | rejected" in matrix
