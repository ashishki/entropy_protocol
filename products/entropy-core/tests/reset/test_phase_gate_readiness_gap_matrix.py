"""Phase-gate readiness gap matrix contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MATRIX = PROJECT_ROOT / "docs" / "readiness" / "PHASE_GATE_GAP_MATRIX.md"
EVIDENCE_INDEX = PROJECT_ROOT / "docs" / "EVIDENCE_INDEX.md"
REQUIRED_CONTROLS = {
    "replay",
    "reproducibility",
    "no-claim",
    "governance",
    "leakage",
    "holdout",
    "review",
}
BLOCKED_SURFACES = (
    "holdout",
    "OOS/performance",
    "live feed",
    "broker/exchange",
    "production",
    "capital-ready",
    "phase-gate approval",
)


def test_gap_matrix_lists_required_controls() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    rows = _matrix_rows(text)

    assert "Status: READINESS_ANALYSIS_ONLY" in text
    assert {row["Control"] for row in rows} == REQUIRED_CONTROLS
    for row in rows:
        assert row["Evidence status"] in {"complete", "partial", "blocked"}
        assert row["Current evidence"]
        assert row["Gap before phase-gate discussion"]
        assert row["Restricted approval state"].startswith("blocked:")


def test_gap_matrix_preserves_blocked_boundaries() -> None:
    text = MATRIX.read_text(encoding="utf-8")

    for surface in BLOCKED_SURFACES:
        assert f"{surface}: blocked" in text
    assert "does not approve a phase gate" in text
    assert "holdout read and unlock not approved" in text
    assert "OOS/performance approval not granted" in text
    assert "not sufficient" in text
    assert "open holdout access" in text


def test_evidence_index_records_gap_matrix() -> None:
    text = EVIDENCE_INDEX.read_text(encoding="utf-8")

    assert "T30 Archive Evidence Sufficiency Gap Matrix" in text
    assert "`docs/readiness/PHASE_GATE_GAP_MATRIX.md`" in text
    assert (
        "`tests/reset/test_phase_gate_readiness_gap_matrix.py::test_gap_matrix_lists_required_controls`"
        in text
    )
    assert (
        "`tests/reset/test_phase_gate_readiness_gap_matrix.py::test_gap_matrix_preserves_blocked_boundaries`"
        in text
    )


def _matrix_rows(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    header_index = lines.index(
        "| Control | Evidence status | Current evidence | Gap before phase-gate discussion | Restricted approval state |"
    )
    headers = _split_row(lines[header_index])
    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("|"):
            break
        rows.append(dict(zip(headers, _split_row(line), strict=True)))
    return rows


def _split_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]
