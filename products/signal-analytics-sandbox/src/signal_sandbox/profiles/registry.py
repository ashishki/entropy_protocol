"""Versioned channel profile registry."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class ProfileTerm(BaseModel):
    model_config = ConfigDict(strict=True)

    term: str = Field(min_length=1)
    category: str = Field(min_length=1)
    profile_state: str = Field(pattern="^(accepted_for_draft|needs_review|excluded)$")
    evidence_capture_ids: list[str] = Field(default_factory=list)
    evidence_excerpts: list[str] = Field(default_factory=list)
    false_positive_risk: str = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)


class ChannelProfile(BaseModel):
    model_config = ConfigDict(strict=True)

    channel_id: str = Field(min_length=1)
    source_urls: list[str] = Field(default_factory=list)
    profile_version: str = Field(min_length=1)
    accepted_draft_terms: list[ProfileTerm] = Field(default_factory=list)
    needs_review_terms: list[ProfileTerm] = Field(default_factory=list)
    excluded_terms: list[ProfileTerm] = Field(default_factory=list)
    modality_flags: dict[str, bool] = Field(default_factory=dict)
    review_rules: list[str] = Field(default_factory=list)


class ChannelProfileRegistry:
    def __init__(self, profiles: list[ChannelProfile] | None = None):
        self._profiles = {
            profile.channel_id: profile for profile in profiles or []
        }

    def get(self, channel_id: str) -> ChannelProfile | None:
        return self._profiles.get(channel_id)

    def add(self, profile: ChannelProfile) -> None:
        self._profiles[profile.channel_id] = profile


def import_bablos79_profile(path: Path) -> ChannelProfile:
    payload = json.loads(path.read_text(encoding="utf-8"))
    terms = [ProfileTerm.model_validate(item) for item in payload["candidates"]]
    return ChannelProfile(
        channel_id="bablos79",
        source_urls=["https://t.me/bablos79"],
        profile_version="bablos79.phase10.v1",
        accepted_draft_terms=[
            term for term in terms if term.profile_state == "accepted_for_draft"
        ],
        needs_review_terms=[
            term for term in terms if term.profile_state == "needs_review"
        ],
        excluded_terms=[term for term in terms if term.profile_state == "excluded"],
        modality_flags={
            "text": True,
            "voice": False,
            "ocr": False,
            "image": False,
        },
        review_rules=[
            "accepted_for_draft terms are draft hints only",
            "needs_review terms cannot become automatic parser truth",
            "excluded terms cannot produce positive signal candidates",
            "asset aliases do not imply direction, entry, stop, target, or approval",
        ],
    )
