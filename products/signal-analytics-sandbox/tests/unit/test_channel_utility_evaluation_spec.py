from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_channel_utility_spec_requires_multimodal_normalization() -> None:
    spec = (PROJECT_ROOT / "docs/specs/CHANNEL_UTILITY_EVALUATION.md").read_text(
        encoding="utf-8"
    )

    assert "text, audio transcript, or image/OCR evidence" in spec
    assert "All modalities converge into the same normalized claim surface" in spec
    assert "SourceDocument" in spec
    assert "MarketIdea" in spec


def test_channel_utility_spec_uses_open_api_window_validation() -> None:
    spec = (PROJECT_ROOT / "docs/specs/CHANNEL_UTILITY_EVALUATION.md").read_text(
        encoding="utf-8"
    )

    assert "avoid maintaining a huge local market database" in spec
    assert "Fetch OHLCV windows on demand" in spec
    assert "exchange-public" in spec
    assert "operator_file" in spec
    assert "Deterministic metrics" in spec


def test_channel_utility_spec_keeps_claims_operator_gated() -> None:
    spec = (PROJECT_ROOT / "docs/specs/CHANNEL_UTILITY_EVALUATION.md").read_text(
        encoding="utf-8"
    )

    assert "Approval gate" in spec
    assert "No overclaim" in spec
    assert "Counterexamples" in spec
    assert "will make money in the future" in spec
