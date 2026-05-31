from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GATE_JSON = PROJECT_ROOT / "docs/pilot/clientready_DISCOVERY_GATE.json"
GATE_MD = PROJECT_ROOT / "docs/pilot/clientready_DISCOVERY_GATE.md"
CODEX_PROMPT = PROJECT_ROOT / "docs/CODEX_PROMPT.md"


def _gate() -> dict:
    return json.loads(GATE_JSON.read_text(encoding="utf-8"))


def test_clientready_discovery_gate_records_decision_and_blockers() -> None:
    gate = _gate()
    summary = gate["summary"]
    report = GATE_MD.read_text(encoding="utf-8")

    assert summary["status"] == "clientready_discovery_gate"
    assert summary["gate_decision"] == "continue_internal_hardening"
    assert summary["ready_for_discovery"] is False
    assert summary["state_may_move_to_client_discovery"] is False
    assert gate["explicit_blockers"] == [
        "redacted_demo_showable_now_false",
        "0_operator_accepted_media_claims",
        "0_recomputed_market_outcomes",
        "0_buyer_demo_safe_rows",
        "dashboard_safe_rr_rows_absent",
    ]
    assert "Gate decision: `continue_internal_hardening`" in report
    assert "Ready for discovery: `false`" in report


def test_clientready_discovery_success_criteria_are_discovery_only() -> None:
    gate = _gate()
    criteria = gate["discovery_only_success_criteria"]
    combined = (
        json.dumps(criteria, ensure_ascii=False)
        + "\n"
        + GATE_MD.read_text(encoding="utf-8")
    ).lower()

    assert len(criteria) == 4
    assert {criterion["current_status"] for criterion in criteria} == {"not_met"}
    assert gate["forbidden_next_steps"] == [
        "pricing",
        "paid_delivery",
        "private_partnerships",
        "public_launch",
    ]
    for forbidden in gate["forbidden_next_steps"]:
        assert forbidden.replace("_", " ") not in combined


def test_clientready_discovery_gate_does_not_move_state_without_ready_gate() -> None:
    gate = _gate()
    policy = gate["state_update_policy"]
    prompt = CODEX_PROMPT.read_text(encoding="utf-8")

    assert policy["if_gate_decision"] == "ready_for_discovery"
    assert policy["then_state_route"] == "client_discovery"
    assert policy["current_state_route"] == "continue_internal_hardening"
    assert policy["state_updated_to_client_discovery"] is False
    assert "External gate: `approve_internal_only`" in prompt
    assert "External delivery: not approved" in prompt
