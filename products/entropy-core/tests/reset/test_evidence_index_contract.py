"""Reset evidence and journal contract tests."""

from __future__ import annotations

import ast
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_INDEX = PROJECT_ROOT / "docs" / "EVIDENCE_INDEX.md"
IMPLEMENTATION_JOURNAL = PROJECT_ROOT / "docs" / "IMPLEMENTATION_JOURNAL.md"
LEGACY_SUMMARY = PROJECT_ROOT / "docs" / "legacy" / "CORE_LEGACY_SUMMARY.md"
TASKS = PROJECT_ROOT / "docs" / "tasks.md"


def test_evidence_index_rows_point_to_existing_artifacts() -> None:
    """Every non-pending evidence row references existing files or tests."""
    rows = _markdown_rows_between(
        EVIDENCE_INDEX.read_text(), "## Evidence Table", "## Pending Evidence"
    )

    assert rows
    for row in rows:
        cells = _split_markdown_row(row)
        assert len(cells) == 6
        for location in _backtick_values(cells[2]):
            file_path, _, test_name = location.partition("::")
            artifact_path = PROJECT_ROOT / file_path
            assert artifact_path.exists(), location
            if test_name:
                assert _python_file_defines_test(artifact_path, test_name), location


def test_journal_has_reset_entry() -> None:
    """The journal keeps an append-only reset entry with scope and next task."""
    journal_text = IMPLEMENTATION_JOURNAL.read_text()
    reset_entry = _journal_entry(journal_text, "2026-05-07 - RESET - Governance Reset Bootstrap")

    assert "- Scope:" in reset_entry
    assert "docs/" in reset_entry
    assert "pyproject.toml" in reset_entry
    assert "- Follow-ups:" in reset_entry
    assert "T01" in reset_entry


def test_legacy_archive_pointers_are_scoped() -> None:
    """Legacy archive references stay in the summary or task Context-Refs only."""
    legacy_summary = LEGACY_SUMMARY.read_text()
    tasks_text = TASKS.read_text()

    assert "docs/legacy/old-workflow/2026-05-07/" in legacy_summary
    assert "docs/legacy/old-workflow/2026-05-07/" not in tasks_text
    for match in re.finditer(r"docs/legacy/[^\s`]+", tasks_text):
        assert _line_is_inside_context_refs(tasks_text, match.start())


def _markdown_rows_between(markdown_text: str, start_heading: str, end_heading: str) -> list[str]:
    start = markdown_text.index(start_heading)
    end = markdown_text.index(end_heading, start)
    rows: list[str] = []
    for line in markdown_text[start:end].splitlines():
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= {"-"}:
            continue
        if "Topic / Finding / Task" in line:
            continue
        rows.append(line)
    return rows


def _split_markdown_row(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def _backtick_values(cell: str) -> list[str]:
    return re.findall(r"`([^`]+)`", cell)


def _python_file_defines_test(path: Path, test_name: str) -> bool:
    tree = ast.parse(path.read_text(), filename=str(path))
    return any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == test_name
        for node in ast.walk(tree)
    )


def _journal_entry(journal_text: str, heading: str) -> str:
    entry_start = journal_text.index(f"### {heading}")
    next_entry = journal_text.find("\n### ", entry_start + 1)
    return journal_text[entry_start:] if next_entry == -1 else journal_text[entry_start:next_entry]


def _line_is_inside_context_refs(text: str, offset: int) -> bool:
    line_start = text.rfind("\n", 0, offset) + 1
    preceding_text = text[:line_start]
    nearest_task = preceding_text.rfind("\n## T")
    nearest_context_refs = preceding_text.rfind("\nContext-Refs:")
    nearest_notes = preceding_text.rfind("\nNotes:")
    nearest_acceptance = preceding_text.rfind("\nAcceptance-Criteria:")

    return (
        nearest_context_refs > nearest_task
        and nearest_context_refs > nearest_acceptance
        and nearest_notes < nearest_context_refs
    )
