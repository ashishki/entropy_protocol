"""Unit tests for P4 batch collection manifests."""

from __future__ import annotations

from entropy.evidence.crypto_universe import get_default_phase0_crypto_universe
from entropy.evidence.p4_batch_collection import (
    P4_BATCH_COLLECTION_ID,
    collect_first_p4_batch,
    render_p4_batch_summary,
)
from entropy.evidence.p4_scale_plan import build_p4_scale_plan


def test_collect_first_p4_batch_writes_hash_manifest(tmp_path) -> None:
    plan = build_p4_scale_plan(universe=get_default_phase0_crypto_universe(), batch_size=2)

    result = collect_first_p4_batch(
        plan=plan,
        output_dir=tmp_path,
        fetch_bytes=lambda url: f"payload:{url}".encode("utf-8"),
    )
    rendered = render_p4_batch_summary(result)

    assert result.collection_id == P4_BATCH_COLLECTION_ID
    assert result.requested_items == 2
    assert result.done_count == 2
    assert result.failed_count == 0
    assert result.gate_claim_allowed is False
    assert result.manifest_path.exists()
    assert result.items[0].source_sha256 is not None
    assert (tmp_path / "BTCUSDT" / "BTCUSDT-1d-2023-01.zip").exists()
    assert "Gate claim allowed: `false`" in rendered


def test_collect_first_p4_batch_records_failures(tmp_path) -> None:
    plan = build_p4_scale_plan(universe=get_default_phase0_crypto_universe(), batch_size=1)

    def fail_fetch(_url: str) -> bytes:
        raise RuntimeError("network unavailable")

    result = collect_first_p4_batch(plan=plan, output_dir=tmp_path, fetch_bytes=fail_fetch)

    assert result.requested_items == 1
    assert result.done_count == 0
    assert result.failed_count == 1
    assert result.items[0].status == "FAILED"
    assert result.items[0].error == "network unavailable"
