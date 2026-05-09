# Project Memory

## Trader Risk Audit

- Last completed: Read-only exchange import roadmap update at 2026-05-09 12:55:00 CEST
- Baseline: 142 pass / 0 skip
- Next task: T45 - Read-Only Exchange Import ADR
- Phase: Phase 11 planned - Read-Only Exchange Import Safety
- Review tier next: docs/scope review for ADR-002 before implementation
- Future phase planned: Phase 11 through Phase 15 define read-only Binance/Bybit import, fixture-backed import core, Bybit MVP, Binance MVP, and operator validation.
- Loop continuity: after phase deep review/archive/fixes, continue to the next planned phase unless stop-ship remains or a new ADR is required.
- Any blockers: none; CODE-1 P2 is closed. ADR-002 is proposed, but exchange network code must not start until T45-T47 close the safety boundary. `/tmp/orchestrator_checkpoint.md` is still owned by another user and cannot be overwritten from this session; repo-local `MEMORY.md` and `PHASE_HANDOFF.md` carry the checkpoint state.
