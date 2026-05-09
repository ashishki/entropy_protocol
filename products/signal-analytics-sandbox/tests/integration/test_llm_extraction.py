from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.base import ExtractionStatus
from signal_sandbox.extraction.llm import (
    COST_CAP_ENV,
    ENABLE_LLM_ENV,
    LLMCompletion,
    LLMExtractionAdapter,
)


@dataclass
class FixtureLLMClient:
    provider: str = "ollama"
    model: str = "fixture-v1"

    def complete(self, prompt: str) -> LLMCompletion:
        assert "Raw text:" in prompt
        return LLMCompletion(
            content=json.dumps(
                {
                    "asset_symbol": "ETH",
                    "direction": "short",
                    "entry": "2500",
                    "stop": "2600",
                    "target": "2300",
                    "confidence_flags": ["fixture"],
                    "ambiguity_flags": [],
                },
                sort_keys=True,
            ),
            cost_usd=Decimal("0"),
        )


def test_fixed_mock_llm_client_extracts_without_live_api() -> None:
    raw_text = "ETH short entry 2500 target 2300 stop 2600"
    post = CapturedPost(
        capture_id="cap-eth-001",
        source_id="nemphiscrypts",
        evidence_url="https://t.me/nemphiscrypts/7",
        capture_timestamp_utc=datetime(2026, 5, 7, 12, tzinfo=UTC),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )

    result = LLMExtractionAdapter(
        FixtureLLMClient(),
        llm_approved=True,
        env={ENABLE_LLM_ENV: "1", COST_CAP_ENV: "1"},
    ).extract(post)

    assert result.status == ExtractionStatus.DRAFT_PENDING_REVIEW
    assert result.record is not None
    assert result.record.asset_symbol == "ETH"
    assert result.record.extraction_metadata["adapter_id"] == "llm/ollama/fixture-v1"
