"""Anthropic Claude client shell for opt-in LLM extraction."""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable
from decimal import Decimal

from signal_sandbox.extraction.llm import LLMCompletion

HTTPPost = Callable[[str, bytes, dict[str, str]], bytes]


class ClaudeClient:
    provider = "claude"

    def __init__(
        self,
        model: str,
        *,
        api_key: str,
        endpoint: str = "https://api.anthropic.com/v1/messages",
        http_post: HTTPPost | None = None,
        cost_per_call_usd: Decimal = Decimal("0"),
    ) -> None:
        self.model = model
        self.api_key = api_key
        self.endpoint = endpoint
        self._http_post = _urllib_post if http_post is None else http_post
        self.cost_per_call_usd = cost_per_call_usd

    def complete(self, prompt: str) -> LLMCompletion:
        request_payload = json.dumps(
            {
                "model": self.model,
                "max_tokens": 512,
                "messages": [{"role": "user", "content": prompt}],
            },
            sort_keys=True,
        ).encode("utf-8")
        response_payload = json.loads(
            self._http_post(
                self.endpoint,
                request_payload,
                {
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                    "x-api-key": self.api_key,
                },
            )
        )
        content = response_payload["content"][0]["text"]
        return LLMCompletion(
            content=str(content),
            cost_usd=self.cost_per_call_usd,
        )


def _urllib_post(endpoint: str, payload: bytes, headers: dict[str, str]) -> bytes:
    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers=headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()
