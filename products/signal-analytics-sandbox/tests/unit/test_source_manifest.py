from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from signal_sandbox.sources.manifest import (
    SourceManifest,
    SourceNotApproved,
    load_source,
    save_source_manifest,
)


def make_manifest(**overrides: Any) -> SourceManifest:
    data: dict[str, Any] = {
        "source_id": "bablos79",
        "source_url": "https://t.me/bablos79",
        "source_type": "telegram_public",
        "capture_method": "operator_supplied",
        "tos_reference": "docs/legal_risk_memo.md",
        "eligibility_verdict": "approved",
        "operator_notes": "initial pilot source",
    }
    data.update(overrides)
    return SourceManifest.model_validate(data)


def test_source_type_allowlist() -> None:
    assert make_manifest(source_type="telegram_public").source_type == "telegram_public"
    assert make_manifest(source_type="x_public").source_type == "x_public"
    assert make_manifest(source_type="website_public").source_type == "website_public"

    with pytest.raises(ValueError):
        make_manifest(source_type="private_telegram")


def test_eligibility_required() -> None:
    with pytest.raises(ValidationError):
        make_manifest(eligibility_verdict=None)

    with pytest.raises(ValidationError):
        SourceManifest.model_validate(
            {
                "source_id": "missing-verdict",
                "source_url": "https://example.com/source",
                "source_type": "website_public",
                "capture_method": "operator_supplied",
                "tos_reference": "docs/legal_risk_memo.md",
            }
        )

    with pytest.raises(ValueError):
        make_manifest(eligibility_verdict="unknown")


def test_blocked_source_rejected(tmp_path: Path) -> None:
    blocked = make_manifest(source_id="blocked", eligibility_verdict="blocked")
    save_source_manifest(blocked, tmp_path)

    with pytest.raises(SourceNotApproved):
        load_source(tmp_path, "blocked")


def test_round_trip_byte_identical(tmp_path: Path) -> None:
    manifest = make_manifest()
    path = save_source_manifest(manifest, tmp_path)

    loaded = load_source(tmp_path, "bablos79")
    redumped = loaded.model_dump_json(by_alias=False, sort_keys=True)

    assert path.read_text(encoding="utf-8") == redumped
