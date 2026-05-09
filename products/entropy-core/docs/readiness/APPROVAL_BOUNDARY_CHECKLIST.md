# Approval Boundary Checklist

Status: APPROVAL_CHECKLIST_NO_APPROVAL
Task: T32 Approval Boundary Checklist
Last updated: 2026-05-09

This checklist records explicit human approvals and evidence prerequisites that
would be required before holdout, phase-gate, or claim-surface work could be
considered. It does not grant approval and cannot be used as substitute evidence
for any restricted action.

## Boundary Checklist

| Boundary | Current status | Required approval | Required evidence before consideration |
|----------|----------------|-------------------|----------------------------------------|
| Research object registration | blocked unless explicit | Human registration approval | Preregistered candidate, hash bindings, readiness status, append-only registry path |
| Evaluation execution beyond scaffold/probe mode | blocked | Human evaluation approval | Registered object, dataset/code/policy/parameter hashes, leakage controls, no-claim review |
| Holdout unlock or read | blocked | Human holdout approval | Holdout access protocol, leakage proof, audit logging, explicit approval event |
| Phase-gate acceptance | blocked | Human phase-gate approval | Readiness packet, approval checklist, no-holdout dry run, phase review |
| Protocol boundary change | blocked | Human protocol approval | ADR or charter-level review, rollback plan, updated governance docs |
| New data-provider activation | blocked | Human provider approval | Provider contract, provenance controls, secrets plan, no-live claim boundary |
| Product workspace bridge into Core | blocked | Human bridge approval | Bridge contract, allowed primitives, forbidden calls, schema and gate evidence |
| Runtime/language escalation | blocked | Human runtime approval | Benchmark evidence, ADR, CI/toolchain plan, rollback plan |
| OOS/performance claim | blocked | Human claim approval plus gate evidence | Passing leakage and holdout gates, admissible evidence packet, explicit claim review |
| Live feed, broker/exchange, production, or capital-ready use | blocked | Human live/production approval plus future gate | Sandbox or dry-run protocol, risk controls, kill-switch/audit plan, explicit approval event |

## Not Approval Sources

The following artifacts are evidence or planning aids only and must not be treated as approval:

- roadmap phases
- planned future tasks
- readiness docs
- archive evidence packets
- reproducibility matrix rows
- no-claim sweep results
- review recommendations
- passing local tests
- generated packet scaffolds

## Current Blocked Status

- holdout read: blocked
- holdout unlock: blocked
- OOS/performance approval: blocked
- phase-gate approval: blocked
- live feed activation: blocked
- broker/exchange activation: blocked
- production label: blocked
- capital-ready label: blocked
- runtime/language escalation: blocked
- product bridge activation: blocked

## Prompt And Handoff Boundary

`docs/CODEX_PROMPT.md` and `PHASE_HANDOFF.md` must continue to state that real external side effects, holdout reads, live capital actions, live broker/exchange execution, and credentialed production deployment remain blocked.
