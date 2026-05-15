from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from signal_sandbox.artifact_pipeline import (
    build_capture_pack,
    build_outcome_prep_pack,
    build_review_closure_pack,
    build_source_report_input,
)
from signal_sandbox.capture.loader import compute_text_sha256


def test_capture_pack_joins_validated_pseudo_labels(tmp_path: Path) -> None:
    _write_capture(tmp_path, "cap-1", "#BTC шорт от уровня")
    label_path = tmp_path / "labels.jsonl"
    label_path.write_text(
        json.dumps(
            {
                "capture_id": "cap-1",
                "candidate_fields": {
                    "asset_candidates": ["BTC"],
                    "direction_candidate": "short",
                    "entry_candidate": None,
                    "stop_candidate": None,
                    "target_candidate": None,
                },
                "confidence": 0.64,
                "evidence_spans": [
                    {"field": "asset_candidates", "text": "#BTC"},
                    {"field": "direction_candidate", "text": "шорт"},
                ],
                "missing_fields": ["entry", "stop", "target"],
                "source_timestamp_utc": "2026-05-01T10:00:00Z",
                "suggested_status": "insufficient_fields",
                "uncertainty_reason": "levels missing",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    pack = build_capture_pack(
        workspace=tmp_path,
        source_id="bablos79",
        pseudo_label_path=label_path,
        generated_at_utc=datetime(2026, 5, 12, tzinfo=UTC),
    )

    assert len(pack.rows) == 1
    row = pack.rows[0]
    assert row.source_timestamp_utc == datetime(2026, 5, 1, 10, tzinfo=UTC)
    assert row.pseudo_label_status == "insufficient_fields"
    assert row.candidate_assets == ["BTC"]
    assert row.direction_candidate == "short"
    assert pack.summary_counts() == {"insufficient_fields": 1}


def test_capture_pack_rejects_unsupported_label_span(tmp_path: Path) -> None:
    _write_capture(tmp_path, "cap-1", "#BTC шорт от уровня")
    label_path = tmp_path / "labels.jsonl"
    label_path.write_text(
        json.dumps(
            {
                "capture_id": "cap-1",
                "candidate_fields": {"asset_candidates": ["ETH"]},
                "evidence_spans": [{"field": "asset_candidates", "text": "#ETH"}],
                "suggested_status": "needs_review",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="absent from raw text"):
        build_capture_pack(
            workspace=tmp_path,
            source_id="bablos79",
            pseudo_label_path=label_path,
        )


def test_capture_pack_writes_operator_inspectable_artifacts(tmp_path: Path) -> None:
    _write_capture(tmp_path, "cap-1", "stream only")
    pack = build_capture_pack(
        workspace=tmp_path,
        source_id="bablos79",
        generated_at_utc=datetime(2026, 5, 12, tzinfo=UTC),
    )

    pack.write_markdown(tmp_path / "out" / "pack.md")
    pack.write_json(tmp_path / "out" / "pack.json")

    markdown = (tmp_path / "out" / "pack.md").read_text(encoding="utf-8")
    payload = json.loads((tmp_path / "out" / "pack.json").read_text(encoding="utf-8"))
    assert "Captured rows: 1" in markdown
    assert "Approved ledger rows created: 0" in markdown
    assert payload["rows"][0]["capture_id"] == "cap-1"
    assert not (tmp_path / "ledgers").exists()
    assert not (tmp_path / "reports").exists()


def test_review_closure_separates_report_input_statuses(tmp_path: Path) -> None:
    _write_capture(tmp_path, "cap-1", "#BTC шорт")
    _write_capture(tmp_path, "cap-2", "stream only")
    label_path = tmp_path / "labels.jsonl"
    labels = [
        {
            "capture_id": "cap-1",
            "candidate_fields": {
                "asset_candidates": ["BTC"],
                "direction_candidate": "short",
            },
            "evidence_spans": [
                {"field": "asset_candidates", "text": "#BTC"},
                {"field": "direction_candidate", "text": "шорт"},
            ],
            "missing_fields": ["entry", "stop", "target"],
            "suggested_status": "insufficient_fields",
        },
        {
            "capture_id": "cap-2",
            "candidate_fields": {"direction_candidate": "unknown"},
            "evidence_spans": [],
            "missing_fields": [],
            "suggested_status": "not_a_signal",
        },
    ]
    label_path.write_text(
        "\n".join(json.dumps(label, sort_keys=True) for label in labels) + "\n",
        encoding="utf-8",
    )
    capture_pack = build_capture_pack(
        workspace=tmp_path,
        source_id="bablos79",
        pseudo_label_path=label_path,
        generated_at_utc=datetime(2026, 5, 12, tzinfo=UTC),
    )

    closure = build_review_closure_pack(
        capture_pack,
        generated_at_utc=datetime(2026, 5, 12, tzinfo=UTC),
    )

    statuses = {row.capture_id: row.final_review_status for row in closure.rows}
    assert statuses == {
        "cap-1": "insufficient_evidence",
        "cap-2": "rejected_not_market_related",
    }
    assert closure.eligible_count() == 0


def test_outcome_prep_avoids_market_fetch_for_unresolved_rows(
    tmp_path: Path,
) -> None:
    _write_capture(tmp_path, "cap-1", "#BTC шорт")
    label_path = tmp_path / "labels.jsonl"
    label_path.write_text(
        json.dumps(
            {
                "capture_id": "cap-1",
                "candidate_fields": {
                    "asset_candidates": ["BTC"],
                    "direction_candidate": "short",
                },
                "evidence_spans": [
                    {"field": "asset_candidates", "text": "#BTC"},
                    {"field": "direction_candidate", "text": "шорт"},
                ],
                "missing_fields": ["entry", "stop", "target"],
                "suggested_status": "insufficient_fields",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    capture_pack = build_capture_pack(
        workspace=tmp_path,
        source_id="bablos79",
        pseudo_label_path=label_path,
    )
    review_pack = build_review_closure_pack(capture_pack)

    outcome_pack = build_outcome_prep_pack(review_pack)

    assert outcome_pack.market_data_fetch_count() == 0
    assert outcome_pack.rows[0].outcome_status == "unresolved_insufficient_evidence"
    assert outcome_pack.rows[0].market_data_action == "do_not_fetch"


def test_source_report_summarizes_negative_artifact_without_claims(
    tmp_path: Path,
) -> None:
    _write_capture(tmp_path, "cap-1", "stream only")
    label_path = tmp_path / "labels.jsonl"
    label_path.write_text(
        json.dumps(
            {
                "capture_id": "cap-1",
                "candidate_fields": {"direction_candidate": "unknown"},
                "evidence_spans": [],
                "missing_fields": [],
                "suggested_status": "not_a_signal",
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    capture_pack = build_capture_pack(
        workspace=tmp_path,
        source_id="bablos79",
        pseudo_label_path=label_path,
        generated_at_utc=datetime(2026, 5, 12, tzinfo=UTC),
    )
    review_pack = build_review_closure_pack(capture_pack)
    outcome_pack = build_outcome_prep_pack(review_pack)

    report = build_source_report_input(
        capture_pack=capture_pack,
        review_pack=review_pack,
        outcome_pack=outcome_pack,
        generated_at_utc=datetime(2026, 5, 12, tzinfo=UTC),
    )
    report.write_markdown(tmp_path / "report.md")

    rendered = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "not financial advice" in rendered
    assert "Customer-report eligible rows: 0" in rendered
    assert "Deterministic outcome metrics computed: 0" in rendered
    assert "expected return" not in rendered.casefold()


def _write_capture(tmp_path: Path, capture_id: str, raw_text: str) -> None:
    capture_dir = tmp_path / "captures" / "bablos79"
    capture_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "capture_id": capture_id,
        "capture_timestamp_utc": "2026-05-07T18:51:32Z",
        "evidence_url": f"https://t.me/bablos79/{capture_id}",
        "raw_text": raw_text,
        "source_id": "bablos79",
        "text_sha256": compute_text_sha256(raw_text),
    }
    (capture_dir / f"{capture_id}.json").write_text(
        json.dumps(payload, sort_keys=True),
        encoding="utf-8",
    )
