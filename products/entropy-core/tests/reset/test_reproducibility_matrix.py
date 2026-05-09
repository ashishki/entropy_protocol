"""Reproducibility matrix contract tests."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MATRIX = PROJECT_ROOT / "docs" / "research" / "REPRODUCIBILITY_MATRIX.md"
EVIDENCE_INDEX = PROJECT_ROOT / "docs" / "EVIDENCE_INDEX.md"
REQUIRED_HASH_COLUMNS = (
    "candidate_packet_hash",
    "dataset_hash",
    "code_hash",
    "policy_hash",
    "parameter_hash",
    "evidence_artifact_hash",
    "replay_json_hash",
)
REQUIRED_PACKETS = {
    "first": "FRC-001-VC-BREAKOUT-CONTINUATION",
    "second": "SRC-001-STRUCTURE-RETEST-BOUNCE",
}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def test_reproducibility_matrix_lists_required_hashes() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    rows = _matrix_rows(text)

    assert "Status: ARCHIVE_ONLY_HASH_BOOKKEEPING" in text
    assert len(rows) == 2
    assert {row["Packet"] for row in rows} == set(REQUIRED_PACKETS)
    for row in rows:
        assert row["Candidate id"] == REQUIRED_PACKETS[row["Packet"]]
        for column in REQUIRED_HASH_COLUMNS:
            assert HASH_RE.match(row[column])
        assert "CANDIDATE_PACKET.md" in row["Source artifacts"]
        assert "DATASET_MANIFEST.md" in row["Source artifacts"]
        assert "RESEARCH_EVIDENCE_PACKET.md" in row["Source artifacts"]
    assert "rank hypotheses" in text
    assert "No OOS/performance" in text


def test_reproducibility_matrix_rejects_missing_hashes() -> None:
    valid_rows = _matrix_rows(MATRIX.read_text(encoding="utf-8"))

    _validate_matrix_rows(valid_rows)
    with pytest.raises(AssertionError, match="required hash"):
        _validate_matrix_rows(
            [{key: value for key, value in valid_rows[0].items() if key != "code_hash"}]
        )
    with pytest.raises(AssertionError, match="unresolved"):
        _validate_matrix_rows([{**valid_rows[0], "dataset_hash": "PENDING_T27_DATASET_HASH"}])
    with pytest.raises(AssertionError, match="duplicate packet"):
        _validate_matrix_rows([valid_rows[0], {**valid_rows[1], "Packet": valid_rows[0]["Packet"]}])
    with pytest.raises(AssertionError, match="duplicate candidate"):
        _validate_matrix_rows(
            [valid_rows[0], {**valid_rows[1], "Candidate id": valid_rows[0]["Candidate id"]}]
        )


def test_evidence_index_records_reproducibility_matrix() -> None:
    text = EVIDENCE_INDEX.read_text(encoding="utf-8")

    assert "T27 Evidence Hash Reproducibility Matrix" in text
    assert "`docs/research/REPRODUCIBILITY_MATRIX.md`" in text
    assert (
        "`tests/reset/test_reproducibility_matrix.py::test_reproducibility_matrix_lists_required_hashes`"
        in text
    )
    assert (
        "`tests/reset/test_reproducibility_matrix.py::test_reproducibility_matrix_rejects_missing_hashes`"
        in text
    )


def _matrix_rows(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    header_index = lines.index(
        "| Packet | Candidate id | candidate_packet_hash | dataset_hash | code_hash | policy_hash | parameter_hash | evidence_artifact_hash | replay_json_hash | Source artifacts |"
    )
    headers = _split_row(lines[header_index])
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        values = _split_row(line)
        rows.append(dict(zip(headers, values, strict=True)))
    _validate_matrix_rows(rows)
    return rows


def _split_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def _validate_matrix_rows(rows: list[dict[str, str]]) -> None:
    packets = [row.get("Packet", "") for row in rows]
    candidates = [row.get("Candidate id", "") for row in rows]
    assert len(packets) == len(set(packets)), "duplicate packet row"
    assert len(candidates) == len(set(candidates)), "duplicate candidate row"
    for row in rows:
        for column in REQUIRED_HASH_COLUMNS:
            assert column in row, f"missing required hash column: {column}"
            value = row[column]
            assert not value.startswith("PENDING_"), f"unresolved required hash: {column}"
            assert HASH_RE.match(value), f"invalid required hash: {column}"
