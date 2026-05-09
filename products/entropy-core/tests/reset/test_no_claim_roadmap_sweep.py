"""No-claim roadmap and archive surface regression sweep."""

from __future__ import annotations

import re
from pathlib import Path

from entropy.evidence import replay_archive_research_packets

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TASKS = PROJECT_ROOT / "docs" / "tasks.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"
ACTIVE_DOCS = (
    TASKS,
    CODEX_PROMPT,
    PHASE_HANDOFF,
    PROJECT_ROOT / "docs" / "research" / "first-packet" / "CANDIDATE_PACKET.md",
    PROJECT_ROOT / "docs" / "research" / "first-packet" / "DATASET_MANIFEST.md",
    PROJECT_ROOT / "docs" / "research" / "first-packet" / "RESEARCH_EVIDENCE_PACKET.md",
    PROJECT_ROOT / "docs" / "research" / "second-packet" / "CANDIDATE_PACKET.md",
    PROJECT_ROOT / "docs" / "research" / "second-packet" / "DATASET_MANIFEST.md",
    PROJECT_ROOT / "docs" / "research" / "second-packet" / "RESEARCH_EVIDENCE_PACKET.md",
    PROJECT_ROOT / "docs" / "research" / "REPRODUCIBILITY_MATRIX.md",
    PROJECT_ROOT / "docs" / "audit" / "ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md",
    PROJECT_ROOT / "docs" / "bridges" / "hypothesis-backtest.md",
)
DISALLOWED_APPROVAL_PATTERNS = (
    re.compile(r"\bholdout_unlock:\s*True\b"),
    re.compile(r"\boos_performance_approval:\s*True\b"),
    re.compile(r"\bphase_gate_approval:\s*True\b"),
    re.compile(r"\bproduction_approval:\s*True\b"),
    re.compile(r"\bcapital_ready_approval:\s*True\b"),
    re.compile(r"\blive_feed_approval:\s*True\b"),
    re.compile(r"\bbroker_exchange_approval:\s*True\b"),
    re.compile(r"\bStatus:\s*(?:APPROVED|PRODUCTION_READY|CAPITAL_READY)\b"),
)


def test_active_docs_do_not_open_restricted_surfaces() -> None:
    for path in ACTIVE_DOCS:
        text = path.read_text(encoding="utf-8")
        for pattern in DISALLOWED_APPROVAL_PATTERNS:
            assert pattern.search(text) is None, (
                f"{path} opens restricted surface: {pattern.pattern}"
            )

    for result in replay_archive_research_packets(project_root=PROJECT_ROOT):
        packet = result.packet
        assert packet.holdout_unlock is False
        assert packet.oos_performance_approval is False
        assert packet.phase_gate_approval is False
        assert packet.production_approval is False
        assert packet.capital_ready_approval is False
        assert packet.live_feed_approval is False
        assert packet.broker_exchange_approval is False
        for pattern in DISALLOWED_APPROVAL_PATTERNS:
            assert pattern.search(packet.to_markdown()) is None


def test_future_phases_are_not_approvals() -> None:
    tasks = TASKS.read_text(encoding="utf-8")
    prompt = CODEX_PROMPT.read_text(encoding="utf-8").lower()
    handoff = PHASE_HANDOFF.read_text(encoding="utf-8").lower()

    for phase_number in range(8, 14):
        assert f"| {phase_number} |" in tasks
    assert "future phases are planned until roadmap evaluation promotes or rewrites them" in tasks
    assert "phase 8 is complete through t34" in prompt
    assert "phase 9 complete through t39" in prompt
    assert "phase 10 complete through t45" in prompt
    assert "phase 11 is local-only live-feed dry-run readiness" in prompt
    assert "roadmap phases 12 through 13 remain planned direction" in prompt
    assert "phase: 11" in prompt
    assert "phase: 11 live-feed dry run readiness" in handoff
    assert "protocol-only holdout access design" in handoff
    assert "active task: t46 live-feed boundary contract" in handoff
    assert "t40 holdout approval request packet scaffold completed" in prompt
    assert "t41 holdout approval evidence intake contract completed" in prompt
    assert "t35 holdout access protocol deny-by-default contract completed" in prompt
    assert "t36 holdout approval event schema contract completed" in prompt
    assert "t37 holdout access audit logging contract completed" in prompt
    assert "t38 holdout leakage guard protocol fixture completed" in prompt
    assert "t39 holdout access protocol review completed" in prompt


def test_prompt_and_handoff_preserve_boundaries() -> None:
    combined = f"{CODEX_PROMPT.read_text(encoding='utf-8')}\n{PHASE_HANDOFF.read_text(encoding='utf-8')}".lower()

    for boundary in (
        "no holdout",
        "live capital",
        "broker/exchange",
        "production",
        "capital-ready",
        "phase-gate",
        "oos/performance",
        "credentialed production deployment",
    ):
        assert boundary in combined
    assert "remain blocked" in combined
    assert "not approved" in combined
