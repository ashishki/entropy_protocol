"""Approval boundary checklist contract tests."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHECKLIST = PROJECT_ROOT / "docs" / "readiness" / "APPROVAL_BOUNDARY_CHECKLIST.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"
REQUIRED_BOUNDARIES = {
    "Research object registration",
    "Evaluation execution beyond scaffold/probe mode",
    "Holdout unlock or read",
    "Phase-gate acceptance",
    "Protocol boundary change",
    "New data-provider activation",
    "Product workspace bridge into Core",
    "Runtime/language escalation",
    "OOS/performance claim",
    "Live feed, broker/exchange, production, or capital-ready use",
}
NOT_APPROVAL_SOURCES = (
    "roadmap phases",
    "planned future tasks",
    "readiness docs",
    "archive evidence packets",
    "reproducibility matrix rows",
    "no-claim sweep results",
    "review recommendations",
    "passing local tests",
    "generated packet scaffolds",
)
BLOCKED_BOUNDARIES = (
    "holdout read: blocked",
    "holdout unlock: blocked",
    "OOS/performance approval: blocked",
    "phase-gate approval: blocked",
    "live feed activation: blocked",
    "broker/exchange activation: blocked",
    "production label: blocked",
    "capital-ready label: blocked",
    "runtime/language escalation: blocked",
    "product bridge activation: blocked",
)


def test_checklist_lists_required_boundaries() -> None:
    text = CHECKLIST.read_text(encoding="utf-8")
    rows = _checklist_rows(text)

    assert "Status: APPROVAL_CHECKLIST_NO_APPROVAL" in text
    assert {row["Boundary"] for row in rows} == REQUIRED_BOUNDARIES
    for row in rows:
        assert row["Current status"].startswith("blocked")
        assert row["Required approval"].startswith("Human")
        assert row["Required evidence before consideration"]
    for boundary in BLOCKED_BOUNDARIES:
        assert boundary in text


def test_checklist_rejects_implicit_approval_sources() -> None:
    text = CHECKLIST.read_text(encoding="utf-8")

    assert "must not be treated as approval" in text
    for source in NOT_APPROVAL_SOURCES:
        assert f"- {source}" in text
    assert "does not grant approval" in text
    assert "substitute evidence" in text


def test_prompt_and_handoff_match_boundary_checklist() -> None:
    checklist = CHECKLIST.read_text(encoding="utf-8").lower()
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()
    combined = f"{prompt}\n{handoff}"

    for boundary in (
        "real external side effects",
        "holdout reads",
        "live capital actions",
        "live broker/exchange execution",
        "credentialed production deployment",
    ):
        assert boundary in checklist
        assert boundary in combined
    assert "current active task is t49 live-feed observability packet" in prompt
    assert "active task: t49 live-feed observability packet" in handoff
    assert "t40 holdout approval request packet scaffold completed" in prompt
    assert "t41 holdout approval evidence intake contract completed" in prompt
    assert "t39 holdout access protocol review completed" in prompt
    assert "t38 holdout leakage guard protocol fixture completed" in prompt
    assert "t37 holdout access audit logging contract completed" in prompt
    assert "t36 holdout approval event schema contract completed" in prompt
    assert "t35 holdout access protocol deny-by-default contract completed" in prompt
    assert "phase 10 complete through t45" in prompt
    assert "phase 11 is local-only live-feed dry-run readiness" in prompt
    assert "phase 9 complete through t39" in prompt
    assert "holdout read/unlock still blocked" in handoff


def _checklist_rows(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    header_index = lines.index(
        "| Boundary | Current status | Required approval | Required evidence before consideration |"
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
