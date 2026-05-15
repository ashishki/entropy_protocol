from __future__ import annotations

from pathlib import Path

GUIDES = (
    Path("docs/EXCHANGE_IMPORT_GUIDE_RU.md"),
    Path("docs/EXCHANGE_IMPORT_GUIDE_EN.md"),
)


def test_exchange_guidance_avoids_persisted_secrets() -> None:
    text = _guide_text()

    assert "environment variables" in text
    assert "env vars" in text
    assert "local prompt" in text
    assert "read -r -s" in text
    assert "committing API keys or secrets to files" in text
    assert "metadata.json" in text
    assert ".env" in text
    assert "fixtures" in text


def test_exchange_guidance_covers_failure_states() -> None:
    text = _guide_text()

    for failure_state in (
        "non-read-only key",
        "missing symbol/category",
        "time range too wide",
        "rate limit",
        "permission unverifiable",
    ):
        assert failure_state in text

    assert "needs_operator_review" in text


def test_exchange_guidance_keeps_csv_fallback() -> None:
    text = _guide_text()

    assert "CSV upload remains the fallback path" in text
    assert "csv_export" in text
    assert "does not want to create an API key" in text
    assert "not exchange endorsement" in text


def _guide_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in GUIDES)
