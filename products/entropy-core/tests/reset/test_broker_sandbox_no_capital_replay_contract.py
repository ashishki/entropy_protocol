"""Reset tests for local broker sandbox no-capital replay packets."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTRACT = PROJECT_ROOT / "docs" / "protocols" / "BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT.md"
RESULT = PROJECT_ROOT / "docs" / "protocols" / "BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT.md"
CODEX_PROMPT = PROJECT_ROOT / "docs" / "CODEX_PROMPT.md"
PHASE_HANDOFF = PROJECT_ROOT / "PHASE_HANDOFF.md"


def test_replay_contract_binds_local_approval_and_inputs() -> None:
    text = CONTRACT.read_text()

    assert "BROKER_SANDBOX_NO_CAPITAL_REPLAY_CONTRACT_LOCAL_ONLY" in text
    assert "LOCAL_BROKER_SANDBOX_REPLAY_APPROVAL_EVENT.md" in text
    assert "required approval scope: local_broker_sandbox_no_capital_replay" in text
    assert "scenario model: `SandboxReplayScenario`" in text
    assert "execution primitive: `run_no_capital_sandbox_replay`" in text


def test_replay_contract_rejects_restricted_scope_and_claims() -> None:
    text = CONTRACT.read_text()

    for fragment in (
        "production_capital_validation",
        "broker_exchange_execution",
        "live_order_placement",
        "holdout_oos_evaluation",
        "product hypothesis confirmation: not_claimed",
        "OOS/performance conclusion: not_claimed",
    ):
        assert fragment in text


def test_replay_result_records_deterministic_local_evidence_delta() -> None:
    text = RESULT.read_text()

    assert "BROKER_SANDBOX_NO_CAPITAL_REPLAY_RESULT_LOCAL_ONLY" in text
    assert "replay_hash: 9b3681de22bf73160baadb022cc4b8af289b144449ca421ffa0f6457910c4c7e" in text
    assert "scenario_count: 2" in text
    assert "deterministic replay: true" in text
    assert "product_hypothesis_delta: local_evidence_strengthened_not_confirmed" in text
    assert "product hypothesis confirmation status: not_confirmed" in text


def test_state_docs_record_replay_result_and_artifact_support_override() -> None:
    prompt = CODEX_PROMPT.read_text()
    handoff = PHASE_HANDOFF.read_text()

    assert "Phase: 31" in prompt
    assert "Name: V2 Internal Kernel Review" in prompt
    assert "Active task: none - human gate required for next bounded Core V2 phase" in handoff
    assert "T66-T68 remain pending but deferred" in prompt
    assert "T63 Local Broker Sandbox Replay Approval Event completed" in prompt
    assert "T64 Broker Sandbox No-Capital Replay Primitive completed" in prompt
    assert "T65 Broker Sandbox Replay Evidence Packet completed" in prompt
