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
    acceptance_rate,
)

EVAL_SET = [
    {
        "source_id": "bablos79",
        "capture_id": "eval-001",
        "evidence_url": "https://t.me/bablos79/101",
        "raw_text": "BTC long entry 100 target 110 stop 90",
        "expected": {
            "asset_symbol": "BTC",
            "direction": "long",
            "entry": "100",
            "stop": "90",
            "target": "110",
        },
    },
    {
        "source_id": "nemphiscrypts",
        "capture_id": "eval-002",
        "evidence_url": "https://t.me/nemphiscrypts/202",
        "raw_text": "ETH short entry 2500 target 2300 stop 2600",
        "expected": {
            "asset_symbol": "ETH",
            "direction": "short",
            "entry": "2500",
            "stop": "2600",
            "target": "2300",
        },
    },
    {
        "source_id": "pifagortrade",
        "capture_id": "eval-003",
        "evidence_url": "https://t.me/pifagortrade/303",
        "raw_text": "SOL long entry 150 target 180 stop 140",
        "expected": {
            "asset_symbol": "SOL",
            "direction": "long",
            "entry": "150",
            "stop": "140",
            "target": "180",
        },
    },
]


@dataclass
class FixtureEvalClient:
    provider: str = "ollama"
    model: str = "eval-fixture-v1"

    def complete(self, prompt: str) -> LLMCompletion:
        raw_text = prompt.rsplit("Raw text:\n", maxsplit=1)[1]
        for item in EVAL_SET:
            if item["raw_text"] == raw_text:
                expected = item["expected"]
                break
        else:
            raise AssertionError(f"unexpected eval prompt: {raw_text}")

        return LLMCompletion(
            content=json.dumps(
                {
                    **expected,
                    "confidence_flags": ["eval_fixture"],
                    "ambiguity_flags": [],
                },
                sort_keys=True,
            ),
            cost_usd=Decimal("0"),
        )


def test_acceptance_rate_baseline() -> None:
    adapter = LLMExtractionAdapter(
        FixtureEvalClient(),
        llm_approved=True,
        env={ENABLE_LLM_ENV: "1", COST_CAP_ENV: "1"},
    )

    approvals = []
    for item in EVAL_SET:
        raw_text = str(item["raw_text"])
        post = CapturedPost(
            capture_id=str(item["capture_id"]),
            source_id=str(item["source_id"]),
            evidence_url=str(item["evidence_url"]),
            capture_timestamp_utc=datetime(2026, 5, 7, 13, tzinfo=UTC),
            raw_text=raw_text,
            text_sha256=compute_text_sha256(raw_text),
        )
        result = adapter.extract(post)
        assert result.status == ExtractionStatus.DRAFT_PENDING_REVIEW
        assert result.record is not None

        expected = item["expected"]
        approvals.append(
            result.record.asset_symbol == expected["asset_symbol"]
            and result.record.direction.value == expected["direction"]
            and str(result.record.entry) == expected["entry"]
            and str(result.record.stop) == expected["stop"]
            and str(result.record.target) == expected["target"]
        )

    assert acceptance_rate(approvals) == Decimal("1")
