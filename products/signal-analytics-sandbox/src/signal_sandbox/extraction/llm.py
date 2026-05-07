"""Gated LLM extraction adapter."""

from __future__ import annotations

import json
import os
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol

from signal_sandbox.capture.loader import CapturedPost
from signal_sandbox.extraction.base import (
    ExtractionAdapter,
    ExtractionResult,
    ExtractionStatus,
)
from signal_sandbox.ledger.record import Direction, SignalRecord

ENABLE_LLM_ENV = "SIGNAL_SANDBOX_ENABLE_LLM"
COST_CAP_ENV = "SIGNAL_SANDBOX_COST_CAP_USD"
SUPPORTED_PROVIDERS = {"ollama", "claude"}
MODEL_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class LLMExtractionError(Exception):
    """Base exception for LLM extraction failures."""


class LLMNotApproved(LLMExtractionError):
    """Raised when the double approval gate is not satisfied."""


class CostCapExceeded(LLMExtractionError):
    """Raised before invoking a paid model when the run is out of budget."""


@dataclass(frozen=True)
class LLMCompletion:
    content: str
    cost_usd: Decimal = Decimal("0")


class LLMClient(Protocol):
    provider: str
    model: str

    def complete(self, prompt: str) -> LLMCompletion:
        """Return a JSON extraction completion for the prompt."""
        ...


class LLMExtractionAdapter(ExtractionAdapter):
    def __init__(
        self,
        client: LLMClient,
        *,
        llm_approved: bool,
        env: Mapping[str, str] | None = None,
    ) -> None:
        self.client = client
        self.env = os.environ if env is None else env
        if self.env.get(ENABLE_LLM_ENV) != "1" or not llm_approved:
            raise LLMNotApproved("LLM extraction requires env gate and run approval")
        self.adapter_id = _adapter_id(client.provider, client.model)
        self.cost_cap_usd = _cost_cap(self.env)
        self.cumulative_cost_usd = Decimal("0")

    def extract(self, post: CapturedPost) -> ExtractionResult:
        self._ensure_cost_cap_allows_call()
        completion = self.client.complete(_prompt(post))
        self.cumulative_cost_usd += completion.cost_usd
        record = _record_from_completion(
            post=post,
            completion=completion,
            adapter_id=self.adapter_id,
        )
        return ExtractionResult(
            status=ExtractionStatus.DRAFT_PENDING_REVIEW,
            post=post,
            record=record,
        )

    def _ensure_cost_cap_allows_call(self) -> None:
        if self.client.provider != "claude":
            return
        if self.cost_cap_usd <= Decimal("0"):
            raise CostCapExceeded("paid LLM provider disabled by zero cost cap")
        if self.cumulative_cost_usd >= self.cost_cap_usd:
            raise CostCapExceeded("LLM cost cap exceeded")


def acceptance_rate(approved_without_modification: Sequence[bool]) -> Decimal:
    if not approved_without_modification:
        return Decimal("0")
    approved = sum(1 for value in approved_without_modification if value)
    return Decimal(approved) / Decimal(len(approved_without_modification))


def _adapter_id(provider: str, model: str) -> str:
    if provider not in SUPPORTED_PROVIDERS:
        raise ValueError(f"unsupported LLM provider: {provider}")
    if not MODEL_RE.fullmatch(model):
        raise ValueError(f"invalid LLM model id: {model}")
    return f"llm/{provider}/{model}"


def _cost_cap(env: Mapping[str, str]) -> Decimal:
    raw_value = env.get(COST_CAP_ENV, "0")
    try:
        return Decimal(raw_value)
    except Exception as exc:
        raise ValueError(f"{COST_CAP_ENV} must be a decimal string") from exc


def _prompt(post: CapturedPost) -> str:
    return (
        "Extract one trading signal as strict JSON with keys asset_symbol, "
        "direction, entry, stop, target, confidence_flags, ambiguity_flags. "
        f"Evidence URL: {post.evidence_url}\n"
        f"Raw text:\n{post.raw_text}"
    )


def _record_from_completion(
    *,
    post: CapturedPost,
    completion: LLMCompletion,
    adapter_id: str,
) -> SignalRecord:
    payload = json.loads(completion.content)
    metadata = {
        "adapter_id": adapter_id,
        "cost_usd": str(completion.cost_usd),
    }
    return SignalRecord(
        source_id=post.source_id,
        capture_id=post.capture_id,
        evidence_url=post.evidence_url,
        text_sha256=post.text_sha256,
        capture_timestamp_utc=post.capture_timestamp_utc,
        extracted_timestamp_utc=payload.get(
            "extracted_timestamp_utc",
            post.capture_timestamp_utc,
        ),
        asset_symbol=str(payload["asset_symbol"]),
        direction=Direction(str(payload["direction"]).lower()),
        entry=_decimal_or_none(payload.get("entry")),
        stop=_decimal_or_none(payload.get("stop")),
        target=_decimal_or_none(payload.get("target")),
        confidence_flags=_string_list(payload.get("confidence_flags", [])),
        ambiguity_flags=_string_list(payload.get("ambiguity_flags", [])),
        extraction_metadata=metadata,
    )


def _decimal_or_none(value: object) -> Decimal | None:
    if value is None or value == "":
        return None
    return Decimal(str(value))


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        raise ValueError("expected list")
    return [str(item) for item in value]
