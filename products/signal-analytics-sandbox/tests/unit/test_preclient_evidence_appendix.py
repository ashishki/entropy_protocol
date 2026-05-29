from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from signal_sandbox.reports import build_preclient_evidence_appendix

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APPENDIX_JSON = PROJECT_ROOT / "docs/pilot/preclient_EVIDENCE_APPENDIX.json"
APPENDIX_MD = PROJECT_ROOT / "docs/pilot/preclient_EVIDENCE_APPENDIX.md"


def test_preclient_evidence_appendix_has_required_row_contract() -> None:
    appendix = json.loads(APPENDIX_JSON.read_text(encoding="utf-8"))
    summary = appendix["summary"]
    rows = appendix["rows"]

    assert summary["status"] == "internal_traceability_appendix"
    assert summary["channels"] == ["bablos79", "nemphiscrypts", "pifagortrade"]
    assert summary["totals"]["rows"] == 301
    assert summary["totals"]["raw_media_rows"] == 0
    assert summary["totals"]["private_source_rows"] == 0
    assert summary["by_channel"] == {
        "bablos79": 198,
        "nemphiscrypts": 65,
        "pifagortrade": 38,
    }

    for row in rows:
        assert row["source_url"]
        assert row["evidence_kind"]
        assert row["artifact_refs"]
        assert row["checksum_or_text_hash"].startswith(
            ("media_sha256:", "text_sha256:", "row_sha256:")
        )
        assert row["review_status"]
        assert row["market_provider_status"]
        assert isinstance(row["blockers"], list)


def test_preclient_evidence_appendix_distinguishes_required_evidence_kinds() -> None:
    appendix = json.loads(APPENDIX_JSON.read_text(encoding="utf-8"))
    by_kind = appendix["summary"]["by_evidence_kind"]
    rows = appendix["rows"]

    assert by_kind["text_only_claim_metric_summary"] == 3
    assert by_kind["media_backed_claim"] == 5
    assert by_kind["media_post_factum"] == 4
    assert by_kind["context_only"] == 4
    assert by_kind["rejected_noise"] == 66
    assert by_kind["provider_gap"] == 3
    assert by_kind["media_processing_blocker"] == 47

    packet_rows = [
        row
        for row in rows
        if any(
            "preclient_MODEL_REVIEW_PACKET.json" in ref for ref in row["artifact_refs"]
        )
    ]
    assert len(packet_rows) == 9
    assert all(
        "arbiter=accept_internal_claim_candidate" in row["review_status"]
        for row in packet_rows
    )
    assert any(
        row["source_id"] == "bablos79"
        and row["post_id"] == 10450
        and row["market_provider_status"]
        == "rr_ready_internal_draft_market_recompute_required"
        for row in packet_rows
    )


def test_preclient_evidence_appendix_blocks_raw_media_and_private_access() -> None:
    appendix = json.loads(APPENDIX_JSON.read_text(encoding="utf-8"))
    report = APPENDIX_MD.read_text(encoding="utf-8")
    serialized = json.dumps(appendix, ensure_ascii=False)

    assert "no raw media bytes" in report
    assert "private/authenticated source access" in report
    assert "workspace/media" not in serialized
    assert '"local_path"' not in serialized
    assert '"bytes"' not in serialized
    for row in appendix["rows"]:
        assert row["raw_media_included"] is False
        assert row["private_source_required"] is False
        assert row["source_url"].startswith(("https://t.me/", "artifact://docs/pilot/"))
        assert not any(ref.startswith("workspace/") for ref in row["artifact_refs"])


def test_preclient_evidence_appendix_generator_reproduces_committed_summary() -> None:
    def read(path: str) -> dict[str, Any]:
        return json.loads((PROJECT_ROOT / path).read_text(encoding="utf-8"))

    committed = json.loads(APPENDIX_JSON.read_text(encoding="utf-8"))
    regenerated = build_preclient_evidence_appendix(
        model_review_packet=read("docs/pilot/preclient_MODEL_REVIEW_PACKET.json"),
        media_manifest=read("docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json"),
        processing_queue=read(
            "docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json"
        ),
        media_review_results=read("docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json"),
        metric_results=read("docs/pilot/three_channel_V1_METRIC_RESULTS.json"),
        generated_at_utc=committed["summary"]["generated_at_utc"],
    ).model_dump(mode="json")

    assert regenerated["summary"] == committed["summary"]
    assert regenerated["rows"] == committed["rows"]
