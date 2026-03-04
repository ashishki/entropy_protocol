# Entropy Protocol — Documentation

**Last updated:** 2026-03-04
**Status:** Active

---

## What Is This Project

Entropy Protocol is a **systematic capital allocation and research governance architecture**.

It is NOT a trading bot, signal generator, or alpha discovery tool.

It provides:
- Walk-forward evaluation infrastructure with strict IS/OOS separation
- Trial registry and multiplicity control
- SimBroker cost and slippage modeling
- Regime governance and portfolio allocation logic
- Structured risk escalation rules

Current classification: **Research Lab** (Era 0–2).
Conditional destination: **Capital Allocation Framework** (Era 3+, after Phase 1 exit criteria met).

---

## Document Map

### Core Documents (start here)

| Document | Purpose | Audience |
|---|---|---|
| [`CHARTER.md`](./CHARTER.md) | Project intent, non-negotiables, phase roadmap | All |
| [`PROTOCOL_SPEC.md`](./PROTOCOL_SPEC.md) | Engineering specification: rules, thresholds, exit criteria | Developers, AI models |
| [`GLOSSARY.md`](./GLOSSARY.md) | Terms, formulas, abbreviations | AI models, new team members |

### Architecture and Process

| Document | Purpose | Audience |
|---|---|---|
| [`EVOLUTION.md`](./EVOLUTION.md) | Design decision history: why constraints exist (v1→v5) | Architects, AI models |
| [`AI_ENGINEERING_FRAMEWORK.md`](./AI_ENGINEERING_FRAMEWORK.md) | How AI-assisted development works in this project | Developers, AI models |

### Audience-Specific Briefs

| Document | Purpose | Audience |
|---|---|---|
| [`audience/ARCHITECT_BRIEF.md`](./audience/ARCHITECT_BRIEF.md) | System architecture stress-test brief | Senior architects |
| [`audience/TRADER_BRIEF.md`](./audience/TRADER_BRIEF.md) | Framework explanation for practitioners contributing hypotheses | External contributors |

### Archive

[`archive/`](./archive/) contains historical design reasoning documents (v1–v4 reviews, literature research). These are preserved for reference and explain the origins of current constraints. They are NOT active specifications.

See [`archive/README.md`](./archive/README.md) for index.

---

## Reading Order

**For a new developer or AI model context-loading:**
1. This README (orientation)
2. `GLOSSARY.md` (terminology)
3. `PROTOCOL_SPEC.md` Section B (frozen non-negotiables)
4. `PROTOCOL_SPEC.md` Section C–D (phase structure and exit criteria)
5. `CHARTER.md` Section D (regime signal governance)
6. `AI_ENGINEERING_FRAMEWORK.md` (development workflow)

**For a senior architect joining the team:**
1. This README
2. `audience/ARCHITECT_BRIEF.md`
3. `CHARTER.md` (full)
4. `EVOLUTION.md` (design history)

**For an external practitioner:**
1. `audience/TRADER_BRIEF.md`

---

## Document Governance

**Frozen documents:** `CHARTER.md` Section B (Non-Negotiables), all kill criteria, all phase exit criteria thresholds. These require a written justification document and explicit version increment. Inline edits are not permitted.

**Evolvable documents:** `PROTOCOL_SPEC.md` implementation sections, `AI_ENGINEERING_FRAMEWORK.md`, audience briefs. These can be updated as the system evolves.

**Archived documents:** historical reasoning in `archive/`. Never modified after archiving. Referenced by date and version label.

**Version naming convention:**
- Core documents use `UPPERCASE_NAME.md` with no version in the filename. Version is tracked in the document header and git log.
- Audience documents: same convention.
- Archive: original filenames preserved.

---

## Current Phase

**Phase 0 (active):** Evaluation engine + SimBroker construction.
**Parallel:** Hypothesis Acceleration Track (paper-only).

No signal receives an OOS evaluation label until Phase 0 exit criteria are met. See `PROTOCOL_SPEC.md` Phase 0 for criteria.

---

## Active Review Questions (Near-Term Resolution)

The following items are currently under active review and targeted for near-term specification closure (Cycle 1 remediation set):

1. **P4 algorithm formalization (A-01 / F-4):** complete reproducible regime-labeling specification (inputs, thresholds/model, calibration, versioning).
2. **P3 trigger determinism (A-02):** lock population/interval definition and deterministic 35–50% reduction rule.
3. **RDL operational boundary unification (B-02 / F-23):** resolve `"Phase 2+"` vs `"after Phase 2 exit"` language across spec/governance docs.
4. **Harvey-Liu canonical variant and trial aggregation (B-01 / F-1, F-24):** define formula and cross-namespace counting (`Main`, `AT`, `RDL-*`).
5. **RBE governance object (B-03 / F-26):** define authority, required artifact, and storage for "charter-level review".
6. **RBE interaction controls (B-04 / F-31):** specify kill-window continuity and enforce RDL->RBE non-interaction.
7. **Net Sharpe stream composition consistency (E-01 / F-22):** normalize all references to `(a+b+c)` and remove `(a+c)` drift.
8. **K3 deterministic definition (C-02, E-02 / F-29):** lock `N_eff` estimator and temporal trigger wording.
9. **GE-2 vs GE-3 zero-weight boundary (B-05 / F-32):** close trial-count suppression loophole.

Tracking sources:
- `docs/audit/REVIEW_REPORT.md` (Cycle 1 findings F-22..F-32)
- `docs/audit/QUESTION_POOL.md` (Q-ID A-01..F-03)
