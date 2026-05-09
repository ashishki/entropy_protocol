from datetime import UTC, datetime, timedelta
from pathlib import Path

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.draft_export import (
    export_draft_rows,
    load_profile,
    render_draft_markdown,
    write_draft_markdown,
)


def test_export_rows_are_deterministic_and_complete() -> None:
    posts = [
        _post("cap-2", "#MAGN entry 100 stop 95 target 110 buy", minutes=2),
        _post("cap-1", "стрим без сигнала", minutes=1),
    ]
    source_timestamps = {
        "cap-2": "2026-05-05T10:00:00Z",
        "cap-1": "2026-05-05T09:00:00Z",
    }

    rows = export_draft_rows(posts, _profile(), source_timestamps=source_timestamps)

    assert [row.capture_id for row in rows] == ["cap-1", "cap-2"]
    complete = rows[1]
    assert complete.suggested_status == "review_candidate"
    assert complete.candidate_fields["asset_candidates"] == ["MAGN"]
    assert complete.missing_fields == []
    assert complete.reason_codes == ["asset_alias_detected", "direction_long_term"]
    assert complete.evidence_url == "https://t.me/bablos79/cap-2"
    assert complete.text_sha256 == compute_text_sha256(posts[0].raw_text)


def test_export_is_draft_only_and_does_not_write_ledger(tmp_path: Path) -> None:
    rows = export_draft_rows([_post("cap-1", "#MAGN buy")], _profile())
    export_path = tmp_path / "docs" / "EXTRACTION_DRAFTS_BABLOS79.md"
    export_path.parent.mkdir()

    write_draft_markdown(export_path, rows)

    assert rows[0].reviewer_id == "pending"
    assert "`pending`" in export_path.read_text(encoding="utf-8")
    assert not (tmp_path / "ledger").exists()


def test_load_profile_reads_json_profile(tmp_path: Path) -> None:
    profile_path = tmp_path / "profile.json"
    profile_path.write_text('{"candidates": []}\n', encoding="utf-8")

    assert load_profile(profile_path) == {"candidates": []}


def test_rendered_markdown_contains_required_columns() -> None:
    rows = export_draft_rows([_post("cap-1", "#MAGN buy")], _profile())

    rendered = render_draft_markdown(rows)

    for column in (
        "suggested_status",
        "missing_fields",
        "reason_codes",
        "confidence",
        "evidence_url",
        "text_sha256",
    ):
        assert column in rendered


def _post(capture_id: str, raw_text: str, *, minutes: int = 0) -> CapturedPost:
    return CapturedPost(
        capture_id=capture_id,
        source_id="bablos79",
        evidence_url=f"https://t.me/bablos79/{capture_id}",
        capture_timestamp_utc=datetime(2026, 5, 7, 18, 51, tzinfo=UTC)
        + timedelta(minutes=minutes),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )


def _profile() -> dict[str, object]:
    return {
        "candidates": [
            {
                "term": "#MAGN",
                "category": "asset_alias",
                "profile_state": "accepted_for_draft",
            },
            {
                "term": "buy",
                "category": "direction_long",
                "profile_state": "accepted_for_draft",
            },
        ]
    }
