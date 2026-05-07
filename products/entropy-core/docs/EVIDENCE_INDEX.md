# Evidence Index - Entropy Core

Version: 1.0
Last updated: 2026-05-07

This file indexes proof artifacts. It is not authority by itself.

## Evidence Table

| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |
|------------------------|---------------|----------|---------------|---------------|------------|

No reset evidence rows are recorded yet. T01 records the first reset baseline. T08 and T10 must add heavy-task evidence rows when implemented.

## Pending Evidence

| Topic | Expected artifact | Owning task |
|-------|-------------------|-------------|
| Reset baseline | pytest/ruff/format/pyright command results in `docs/CODEX_PROMPT.md` | T01-T03 |
| Leakage/holdout proof | `tests/unit/test_data_leakage_reset.py::test_leakage_failure_blocks_oos_label` | T08 |
| Attribution stream proof | `tests/unit/test_attribution_reset.py::test_net_sharpe_excludes_stream_d` | T10 |
| Phase-gate packet proof | `tests/integration/test_phase_gate_packet_reset.py::test_phase_gate_packet_contains_required_sections` | T11 |
| Product bridge proof | `tests/integration/test_trader_risk_bridge_contract.py::test_bridge_rejects_live_and_claim_surfaces` | T12 |

## Retrieval Rules

- Add rows only after the referenced artifact exists.
- Prefer executable tests, review reports, fixtures, and generated packets over summary prose.
- Legacy summaries are context, not proof.
