# Phase 28 Error Register

Status: T122 manual review
Date: 2026-05-19

## Summary

| Severity | Count | Demo block? |
|---|---:|---|
| P0 | 0 | Yes if any appear |
| P1 | 0 | Yes if any appear |
| P2 | 2 | No, but caveats must stay visible |

No unresolved P0 or P1 findings block the account-scoped real-open-data
rehearsal pack. P2 findings are source-shape and wording limitations that must
remain visible in reviewed reports, dashboards, and gate updates.

## Findings

| ID | Severity | Case | Area | Finding | Demo status | Disposition |
|---|---|---|---|---|---|---|
| PH28-P2-001 | P2 | `real_open_dex_contract_sequence_001` | source shape | Contract-recipient filtered swaps are more scoped than pair-level flow, but still do not prove one trader account ledger, customer identity, or private-report readiness. | Development rehearsal only | Accepted limitation; preserved in reviewed report and review note. |
| PH28-P2-002 | P2 | `real_open_dex_contract_sequence_001` | fees and P&L | Fees are unsupported by the pair event and P&L attribution is a rehearsal calculation on transformed rows, not verified realized trader P&L. | Development rehearsal only | Accepted limitation; preserved in reviewed report and review note. |

## Gate Impact

This register does not change `docs/PAID_PILOT_READY_GATE.md` to ready.
T116 remains blocked until one operator-approved private/anonymized report is
run and manually reviewed outside git.
