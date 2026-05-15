"""Versioned append-only rule extraction templates."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class RuleTemplate:
    template_id: str
    pattern: str
    pattern_sha256: str


BINANCE_SPOT_V1_PATTERN = (
    r"(?P<asset>[A-Z]{2,12})\s+"
    r"(?P<direction>long|short)\s+"
    r"entry\s+(?P<entry>[0-9]+(?:\.[0-9]+)?)\s+"
    r"target\s+(?P<target>[0-9]+(?:\.[0-9]+)?)\s+"
    r"stop\s+(?P<stop>[0-9]+(?:\.[0-9]+)?)"
)

TEMPLATES: dict[str, RuleTemplate] = {
    "binance_spot_v1": RuleTemplate(
        template_id="binance_spot_v1",
        pattern=BINANCE_SPOT_V1_PATTERN,
        pattern_sha256="8de9f14c2eb6b9c0d73e64c3cbb001e9d30383ae33127c70110ff07aad896130",
    )
}


def template_sha256(pattern: str) -> str:
    return hashlib.sha256(pattern.encode("utf-8")).hexdigest()
