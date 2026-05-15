"""Private or restricted source URL patterns.

This module is a defense-in-depth URL check. Source-level eligibility remains
the primary public-source gate in `SourceManifest`.
"""

from __future__ import annotations

import re

PRIVATE_SOURCE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"https?://t\.me/\+", re.IGNORECASE),
    re.compile(r"https?://t\.me/joinchat/", re.IGNORECASE),
    re.compile(r"https?://(?:www\.)?discord\.gg/", re.IGNORECASE),
    re.compile(r"[?&](?:auth|token|invite)=", re.IGNORECASE),
    re.compile(r"/(?:login|signin|paywall|members-only)(?:/|$)", re.IGNORECASE),
)


def is_private_source_url(url: str) -> bool:
    return any(pattern.search(url) for pattern in PRIVATE_SOURCE_PATTERNS)
