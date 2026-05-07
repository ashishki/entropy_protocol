"""Local Ollama client for opt-in LLM extraction."""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable
from decimal import Decimal

from signal_sandbox.extraction.llm import LLMCompletion

HTTPPost = Callable[[str, bytes], bytes]


class OllamaClient:
    provider = "ollama"

    def __init__(
        self,
        model: str,
        *,
        endpoint: str = "http://localhost:11434/api/generate",
        http_post: HTTPPost | None = None,
    ) -> None:
        self.model = model
        self.endpoint = endpoint
        self._http_post = _urllib_post if http_post is None else http_post

    def complete(self, prompt: str) -> LLMCompletion:
        request_payload = json.dumps(
            {"model": self.model, "prompt": prompt, "stream": False},
            sort_keys=True,
        ).encode("utf-8")
        response_payload = json.loads(self._http_post(self.endpoint, request_payload))
        return LLMCompletion(
            content=str(response_payload["response"]),
            cost_usd=Decimal("0"),
        )


def _urllib_post(endpoint: str, payload: bytes) -> bytes:
    request = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()
