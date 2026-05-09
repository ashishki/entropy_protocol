from __future__ import annotations

from pathlib import Path

from signal_sandbox.profiles import (
    ChannelProfile,
    ChannelProfileRegistry,
    ProfileTerm,
    import_bablos79_profile,
)


def test_channel_profile_schema() -> None:
    term = ProfileTerm(
        term="#BTC",
        category="asset_alias",
        profile_state="accepted_for_draft",
        evidence_capture_ids=["capture-1"],
        evidence_excerpts=["#BTC example"],
        false_positive_risk="asset only",
        confidence=0.9,
    )
    profile = ChannelProfile(
        channel_id="example",
        source_urls=["https://t.me/example"],
        profile_version="example.v1",
        accepted_draft_terms=[term],
        needs_review_terms=[],
        excluded_terms=[],
        modality_flags={"text": True, "voice": False, "ocr": False},
        review_rules=["human review required"],
    )

    loaded = ChannelProfile.model_validate_json(profile.model_dump_json())

    assert loaded == profile
    assert loaded.accepted_draft_terms[0].term == "#BTC"
    assert loaded.modality_flags["text"] is True
    assert loaded.review_rules == ["human review required"]


def test_bablos79_profile_import_preserves_states() -> None:
    profile = import_bablos79_profile(
        Path("workspace/lexicons/bablos79_lexicon_draft.json")
    )

    assert profile.channel_id == "bablos79"
    assert profile.source_urls == ["https://t.me/bablos79"]
    assert profile.profile_version == "bablos79.phase10.v1"
    assert len(profile.accepted_draft_terms) == 17
    assert len(profile.needs_review_terms) == 9
    assert len(profile.excluded_terms) == 6
    assert {term.profile_state for term in profile.accepted_draft_terms} == {
        "accepted_for_draft"
    }
    assert {term.profile_state for term in profile.needs_review_terms} == {
        "needs_review"
    }
    assert {term.profile_state for term in profile.excluded_terms} == {"excluded"}


def test_unknown_channel_has_no_default_profile() -> None:
    registry = ChannelProfileRegistry(
        [import_bablos79_profile(Path("workspace/lexicons/bablos79_lexicon_draft.json"))]
    )

    assert registry.get("bablos79") is not None
    assert registry.get("unknown-channel") is None
