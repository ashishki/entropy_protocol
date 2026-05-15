from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.base import ExtractionStatus
from signal_sandbox.extraction.llm import (
    COST_CAP_ENV,
    ENABLE_LLM_ENV,
    CostCapExceeded,
    LLMCompletion,
    LLMExtractionAdapter,
    LLMNotApproved,
)
from signal_sandbox.ledger.io import LLMReviewRequired, read_ledger, write_ledger


@dataclass
class FixedClient:
    provider: str
    model: str
    completion: LLMCompletion
    calls: int = 0

    def complete(self, prompt: str) -> LLMCompletion:
        self.calls += 1
        assert "Evidence URL: https://t.me/bablos79/1" in prompt
        return self.completion


def post() -> CapturedPost:
    raw_text = "BTC long entry 100 target 110 stop 90"
    return CapturedPost(
        capture_id="cap-001",
        source_id="bablos79",
        evidence_url="https://t.me/bablos79/1",
        capture_timestamp_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )


def completion(*, cost_usd: Decimal = Decimal("0")) -> LLMCompletion:
    return LLMCompletion(
        content=json.dumps(
            {
                "asset_symbol": "BTC",
                "direction": "long",
                "entry": "100",
                "stop": "90",
                "target": "110",
                "confidence_flags": ["fixed_fixture"],
                "ambiguity_flags": [],
            },
            sort_keys=True,
        ),
        cost_usd=cost_usd,
    )


def env(*, cap: str = "1") -> dict[str, str]:
    return {ENABLE_LLM_ENV: "1", COST_CAP_ENV: cap}


def test_activation_requires_both_gates() -> None:
    client = FixedClient("ollama", "llama3.1", completion())

    with pytest.raises(LLMNotApproved):
        LLMExtractionAdapter(client, llm_approved=True, env={})

    with pytest.raises(LLMNotApproved):
        LLMExtractionAdapter(client, llm_approved=False, env=env())

    adapter = LLMExtractionAdapter(client, llm_approved=True, env=env())

    assert adapter.adapter_id == "llm/ollama/llama3.1"


def test_status_and_adapter_id() -> None:
    client = FixedClient("ollama", "llama3.1", completion())
    result = LLMExtractionAdapter(client, llm_approved=True, env=env()).extract(post())

    assert result.status == ExtractionStatus.DRAFT_PENDING_REVIEW
    assert result.record is not None
    adapter_id = result.record.extraction_metadata["adapter_id"]
    assert re.fullmatch(r"llm/(ollama|claude)/[A-Za-z0-9._-]+", adapter_id)
    assert adapter_id == "llm/ollama/llama3.1"
    assert result.record.evidence_url == post().evidence_url
    assert result.record.text_sha256 == post().text_sha256


def test_cost_cap_enforced() -> None:
    client = FixedClient(
        "claude",
        "claude-3-haiku",
        completion(cost_usd=Decimal("0.06")),
    )
    adapter = LLMExtractionAdapter(
        client,
        llm_approved=True,
        env=env(cap="0.05"),
    )

    first = adapter.extract(post())

    assert first.status == ExtractionStatus.DRAFT_PENDING_REVIEW
    assert client.calls == 1
    assert adapter.cumulative_cost_usd == Decimal("0.06")

    with pytest.raises(CostCapExceeded):
        adapter.extract(post())

    assert client.calls == 1


def test_zero_cap_disables_paid_provider() -> None:
    client = FixedClient(
        "claude",
        "claude-3-haiku",
        completion(cost_usd=Decimal("0.01")),
    )
    adapter = LLMExtractionAdapter(client, llm_approved=True, env=env(cap="0"))

    with pytest.raises(CostCapExceeded):
        adapter.extract(post())

    assert client.calls == 0


def test_no_direct_write_to_ledger(tmp_path: Path) -> None:
    client = FixedClient("ollama", "llama3.1", completion())
    result = LLMExtractionAdapter(client, llm_approved=True, env=env()).extract(post())
    assert result.record is not None

    with pytest.raises(LLMReviewRequired):
        write_ledger([result.record], tmp_path / "blocked.parquet")

    reviewed = result.record.model_copy(update={"reviewer_id": "operator-1"})
    path = tmp_path / "reviewed.parquet"
    write_ledger([reviewed], path)

    loaded = read_ledger(path)
    assert loaded[0].reviewer_id == "operator-1"
