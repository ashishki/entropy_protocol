# Entropy Protocol — Research Portfolio Monitor

**Version:** 1.0
**Last updated:** 2026-03-23
**Status:** Active — approved by Protocol Governor
**Purpose:** Define the Research Portfolio Monitor (RPM): its permitted signal classes, forbidden output types, presentation rules, attention signal layer, session comparison rules, derived metrics rules, and MVP specification.
**Authority:** This document is subordinate to `docs/core/PROTOCOL_SPEC.md` and `docs/core/CHARTER.md`. Where any conflict exists, the core protocol governs.

---

## Governing Principle

Every permitted signal must be expressible in exactly this form:

> *"The state of [X] is [Y]."*

If a signal requires the implicit suffix *"...therefore you should do Z"* to be meaningful — it is a decision output disguised as an observation. It is forbidden.

The RPM surfaces facts. The human supplies interpretation and all decisions.

---

## 1. Role and Constraints

The Research Portfolio Monitor is a read-only governance dashboard that displays the factual state of the research portfolio. It is part of the Governance Layer.

**The RPM is permitted to:**
- Display current factual state of the Trial Registry by hypothesis family
- Evaluate preregistered human-defined conditions against current data
- Display a manual point-in-time diff between the current state and a single named snapshot
- Flag proximity between a candidate hypothesis and existing registry entries, on manual trigger

**The RPM is prohibited from:**
- Writing to the Trial Registry or any protocol document
- Producing priority rankings, quality scores, or composite metrics
- Recommending actions of any kind
- Generating or evaluating hypotheses
- Influencing portfolio routing, sizing, risk escalation, or phase-gate decisions
- Generating attention conditions autonomously — all conditions are human-preregistered
- Retaining state between sessions (except a single named snapshot, per SC rules)

**The RPM does not produce admissible evidence.** Its outputs are dashboard observations. They cannot be cited in phase-gate evaluations, kill criterion assessments, or OOS evidence records.

---

## 2. Permitted Signal Classes

### Class A — State Signals

Report current factual status of the research portfolio at a point in time.

| Signal | Definition | Example output |
|---|---|---|
| **A-1: Family slot status** | Whether the 1-active-trial slot for each family is occupied or vacant | `Funding Signals — slot: FULL (Trial #047 active)` |
| **A-2: Total trial count by family** | Number of registered trials per family, cumulative lifetime | `Volatility Compression — 12 trials registered` |
| **A-3: Outcome triplet by family** | Count of pass / fail / inconclusive / pending outcomes per family | `Structure Levels — 2 pass / 6 fail / 1 inconclusive / 0 pending` |
| **A-4: Budget ceiling status** | Trials submitted this week vs. 3/week ceiling | `Week submissions: 2 of 3 allowed` |
| **A-5: Considered-and-declined log count** | Count of hypotheses surfaced but not submitted to Trial Registry | `Considered-and-declined log: 4 entries` |
| **A-6: Phase-gated family status** | Whether a family requires a phase that has not yet been entered | `Regime-Conditioned Signals — requires Phase 2 entry` |

---

### Class B — Pace Signals

Report rate of activity over defined time windows. Time windows are fixed constants defined in the configuration document, not dynamically computed.

| Signal | Definition | Example output |
|---|---|---|
| **B-1: Days since last submission per family** | Calendar days since the last Trial Registry entry in this family | `Liquidity/Flow Signals — last submission: 47 days ago` |
| **B-2: Days since last resolved result per family** | Calendar days since the last trial in this family reached a completed outcome | `Funding Signals — last resolved result: 23 days ago` |
| **B-3: Rolling submission rate** | Trial submissions in rolling 30-day window vs. budget ceiling | `Rolling 30-day submissions: 7 of 12 allowed` |
| **B-4: Average resolution time per family** | Mean days from submission to outcome per family, with mandatory basis count | `Volatility Compression — mean resolution: 34 days (6 resolved trials)` |

---

### Class C — Proximity Signals

Report similarity between a candidate hypothesis and existing registry entries.

**Constraint:** Proximity signals are computed only on explicit human trigger per session. They are never computed automatically on a schedule.

| Signal | Definition | Example output |
|---|---|---|
| **C-1: Redundancy proximity score** | Semantic similarity score between candidate hypothesis text and existing registered hypotheses in the same family | `Candidate vs. Trial #031: similarity score 0.78` |
| **C-2: Near-duplicate flag** | Similarity score above the preregistered threshold triggers a neutral flag for human review | `FLAG: similarity ≥ 0.80 threshold met — human review required` |
| **C-3: Cross-family proximity** | Whether a candidate hypothesis shares structure with hypotheses in a different family | `Candidate resembles Trial #019 (Regime-Conditioned family) — human classification required` |

**Constraint on C-2:** The flag is triggered by a preregistered numeric threshold. It does not say "this hypothesis is redundant." It says "similarity exceeded threshold." The human determines whether the similarity constitutes true redundancy.

**Similarity algorithm:** Must be preregistered in the configuration document before first use. The algorithm version is logged alongside every proximity score produced. The algorithm does not change without a new configuration entry with a named human sponsor.

---

### Class D — Gap Signals

Report absence of activity. Gap signals draw attention to what has not happened, not to what should happen.

| Signal | Definition | Example output |
|---|---|---|
| **D-1: Families with no resolved result in N days** | Lists families where no trial has produced a completed outcome in the last N days (N is a preregistered constant) | `No resolved result in 60+ days: Structure Levels, Liquidity/Flow Signals` |
| **D-2: Families with zero lifetime trials** | Lists families that have never had a registered trial | `Zero lifetime trials: Liquidity/Flow Signals` |
| **D-3: Considered-and-declined log age** | Days since the considered-and-declined log was last reviewed by a named human sponsor | `Considered-and-declined log: last reviewed 14 days ago` |
| **D-4: Multiplicity budget headroom** | Remaining trial budget before Harvey-Liu shock-control trigger (10-trial growth in 30 days) | `M_total growth in rolling 30 days: 7 of 10 before shock-control pause` |

---

### Class ATT — Attention Signals

An attention signal fires when a preregistered human-defined condition is mechanically satisfied.

**Mechanism:**
1. The human defines a condition in the configuration document before any session in which it is active.
2. The system evaluates the condition against current registry data mechanically. No AI inference is applied.
3. When the condition is satisfied, the system displays a factual state report of the form: `"The state of [field] in [scope] is [value]."`
4. The system adds no interpretation, no suggested action, and no severity framing.

**Critical distinction:** The human authored the condition. The system executes it. The RPM does not generate conditions.

#### Preregistered Condition Schema

Each attention condition must be fully specified in the configuration document before it is active:

```
condition_id:     ATT-[NNN]
scope:            [family name] | [portfolio]
field:            [signal class and field — from permitted field list below]
operator:         greater_than | less_than | equal_to | not_equal_to
threshold:        [fixed scalar entered by human — not a formula or dynamic value]
display_text:     "The state of [field] in [scope] is [value]."
registered_by:    [named human sponsor]
registered_date:  [date]
change_log:       [record of any prior values and the human decision to change them]
```

**Constraints on the schema:**
- `threshold` must be a fixed scalar. Formulas, computed percentiles, and dynamic values are prohibited.
- `display_text` is preregistered verbatim. The system substitutes `[value]` with the current computed value only. Surrounding text is not altered.
- `operator` must be a simple binary comparator. Compound logic (`AND`, `OR`) is not permitted in a single condition. Multiple conditions for the same scope are separate entries.
- No condition may reference another condition's output as its input.

#### Permitted Condition Fields

Only fields from Classes A, B, C, and D may be used as condition fields:

| Field | Class | Example condition |
|---|---|---|
| `days_since_last_submission` | B-1 | greater_than 30 |
| `days_since_last_resolved_result` | B-2 | greater_than 60 |
| `active_slot_status` | A-1 | equal_to VACANT |
| `lifetime_trial_count` | A-2 | equal_to 0 |
| `weekly_submission_count` | A-4 | equal_to 3 |
| `m_total_growth_30d` | D-4 | greater_than 8 |
| `considered_declined_log_days_since_review` | D-3 | greater_than 14 |
| `proximity_score` | C-1 | greater_than 0.80 (manual trigger only) |
| `phase_gate_status` | A-6 | equal_to GATED |

#### Forbidden Condition Fields

The following may not be used as ATT condition fields:
- Any composite score or derived ratio
- Any comparison between two families (`family_X.field > family_Y.field`)
- Any field referencing session-comparison deltas
- Any trend-derived value (moving average, rate of change, direction)
- Any AI-generated assessment

#### ATT Display Rules

**Dedicated section.** Attention signals appear in a separate section. They are never inline with the family status table.

**Fixed ordering.** Alphabetical by scope, then alphabetical by field. Never ordered by urgency, importance, or any computed quality.

**All conditions shown.** Both satisfied (`[MET]`) and unsatisfied conditions are displayed. Showing only triggered conditions creates a filtered view that implies the untriggered conditions are less relevant.

**No visual weight differentiation.** A triggered condition uses the neutral marker `[MET]`. It does not use color, bold, or enlarged text to imply urgency.

**No explanatory text.** The system does not add "this may indicate X" or "consider reviewing Y." The state fact is the complete output.

#### ATT Display Format

```
ATTENTION CONDITIONS
────────────────────────────────────────────────────────────────────────────────
ID        Scope                  Field                        Threshold   Current     State
────────────────────────────────────────────────────────────────────────────────
ATT-001   Funding Signals        days_since_last_submission   > 30        47          [MET]
ATT-002   Liquidity/Flow         lifetime_trial_count         = 0         0           [MET]
ATT-003   Structure Levels       days_since_last_submission   > 30        12          —
ATT-004   [portfolio]            m_total_growth_30d           > 8         7           —
ATT-005   [portfolio]            weekly_submission_count      = 3         2           —
```

#### What an Attention Signal Is Not

| Prohibited formulation | Why prohibited | Permitted substitute |
|---|---|---|
| "Funding Signals needs attention" | Implies action | "The state of days_since_last_submission in Funding Signals is 47." |
| "Consider reviewing Structure Levels" | Prescribes action | Show condition row with current value and `—` status |
| "Inactive families flagged" | Labels a category | Show all conditions with current values |
| "High priority: Liquidity/Flow Signals" | Ranking | "ATT-002: lifetime_trial_count = 0, condition met" |
| "Warning: budget nearly exhausted" | Qualitative severity | Show current value and threshold as numerics |

---

### Class DM — Derived Metrics

Derived metrics are mechanical transformations of raw registry data that show all inputs necessary for interpretation.

A derived metric is permitted when:
1. Both numerator and denominator are visible (no collapsed percentages)
2. No benchmark is embedded
3. No cross-family comparison is implied
4. The computation formula is stated in the configuration document

#### Permitted Derived Metrics

**DM-1: Resolution ratio as X of Y**

Format: `"[N] of [M] trials resolved as [outcome]"`

The denominator is always visible. Percentages are prohibited.

```
Permitted:   "Funding Signals: 3 of 11 trials resolved as pass"
Forbidden:   "Funding Signals: 27% pass rate"
```

**DM-2: Mean resolution time with mandatory basis count**

Format: `"Mean days from submission to resolved outcome: [N] days (based on [M] resolved trials)"`

The basis count is mandatory. A mean without a basis count is not a permitted display.

```
Permitted:   "Volatility Compression: mean resolution 34 days (based on 7 resolved trials)"
Forbidden:   "Volatility Compression: average resolution time 34 days"
```

**DM-3: Outcome triplet (formally defined)**

Format: `"[pass] pass / [fail] fail / [inconclusive] inconclusive / [pending] pending"`

This is the standard outcome display used in the family status table. All four counts are always shown together.

**DM-4: Budget headroom as remaining capacity**

Format: `"[N] submissions remaining this week"` or `"[N] submissions remaining before shock-control pause"`

```
Permitted:   "1 submission remaining this week"
Forbidden:   "Budget nearly exhausted — 1 remaining"
```

**DM-5: Consecutive outcome count**

Format: `"Consecutive [outcome] outcomes: [N]"`

A mechanical count of sequential outcomes of the same type. Must be displayed as a raw integer only. No language implying the streak is meaningful.

```
Permitted:   "Structure Levels: consecutive fail outcomes: 4"
Forbidden:   "Structure Levels: concerning failure streak of 4"
```

**DM-6: Days per trial (mean submission interval)**

Format: `"Average [N] days between submissions (based on [M] submission intervals)"`

The basis count is mandatory.

#### Forbidden Derived Metrics

**DM-F1: Any percentage without visible denominator.** Percentages collapse the denominator. Forbidden in all forms.

**DM-F2: Cross-family ratios.** Any metric that compares one family against another on qualitative grounds.

**DM-F3: Composite metrics.** Any formula aggregating multiple fields into a single quality or priority score.

**DM-F4: Efficiency or productivity ratios.** Any metric relating outcomes to inputs in a way that implies a ratio is "good" or "bad" — passes per trial, cost per positive result, research yield.

---

### Class SC — Session Comparison

A manual point-in-time diff between the current state and a single named, human-saved snapshot.

#### Governing Rules

**SC-1: Manual trigger only.** The comparison view is never displayed by default. The researcher explicitly invokes it each session.

**SC-2: One snapshot retained.** Exactly one snapshot is stored. Saving a new snapshot overwrites the prior one. There is no snapshot history. This prevents time-series construction from accumulated diffs.

**SC-3: Snapshot is always human-named and timestamped.** The saved snapshot must display the date and time it was taken at all times when the comparison is shown.

**SC-4: Delta format — raw signed integer only.**

```
Permitted:   "days_since_last_submission: was 12 (snapshot 2026-02-15) / now 47 / delta +35"
Forbidden:   "days_since_last_submission: increased ↑"
Forbidden:   "days_since_last_submission: worsened"
Forbidden:   "days_since_last_submission: +291% change"
```

Both the prior value and the current value are always shown. The delta is a signed integer. No arrows, no directional language, no percentage change.

**SC-5: Applies to Classes A and B only.** Session comparison is not applied to Class C (proximity scores) or Class D (gap signals). These are state signals that do not benefit from point-in-time comparison without trend inference.

**SC-6: No comparison between two non-current snapshots.** The comparison is always: current state vs. one named snapshot. Comparing snapshot A to snapshot B is not permitted.

**SC-7: No RPM-generated inference from the delta.** The system displays the numbers. It does not add any text about what the delta means.

#### SC Display Format

```
SNAPSHOT COMPARISON   [manual — invoked by researcher]
Reference snapshot: 2026-02-15 14:32 UTC   [saved by: researcher name]

Family                  Field                         Snapshot    Current    Delta
─────────────────────────────────────────────────────────────────────────────────
Funding Signals         days_since_last_submission    12          47         +35
Funding Signals         lifetime_trial_count          9           11         +2
Structure Levels        days_since_last_submission    8           12         +4
Structure Levels        lifetime_trial_count          7           9          +2
[portfolio]             weekly_submission_count       1           2          +1
[portfolio]             m_total_growth_30d            3           7          +4
```

No other content in this section. No interpretation. No totals. No highlighted rows.

---

## 3. Forbidden Signal Classes

The following output types are permanently prohibited. These are definitional exclusions: if a signal belongs to any of these classes, it is not an attention signal and cannot be part of the RPM.

| Class | Description | Examples |
|---|---|---|
| **F-1 — Value signals** | Any assessment of future informational yield, research potential, or expected utility | "Expected informational value: High"; "High learning potential" |
| **F-2 — Priority signals** | Any ranking, ordering, or weighting of research directions by computed quality | "Top priority: Funding Signals"; "Research priority ranking: 1. X, 2. Y" |
| **F-3 — Action signals** | Any output prescribing, suggesting, or implying a course of action | "Recommend: defer"; "Consider pausing"; "Should be rejected" |
| **F-4 — Composite scores** | Any aggregation of multiple metrics into a single quality or priority number | "Research health score: 72/100"; "Portfolio quality index: 0.65" |
| **F-5 — Comparative quality signals** | Any signal framing one family or hypothesis as better or worse than another | "Funding Signals outperforming Volatility Compression" |
| **F-6 — Trend inference** | Any signal requiring directional change to interpret — moving averages, rate-of-change, "improving/declining" labels | Trend arrows; "activity is rising"; moving average overlays |
| **F-7 — Denominator-collapsed ratios** | Percentages without visible denominator; efficiency ratios without basis counts | "27% success rate"; "efficiency rating: B+" |

---

## 4. Presentation Rules

Bias can be introduced through presentation even when individual signals are factual. The following rules govern how all permitted signals are displayed.

**P-1: Fixed neutral ordering.** All families displayed in fixed alphabetical order. Never reordered by any computed metric.

**P-2: All families always visible.** All five hypothesis families shown at all times, regardless of activity state. No hiding, collapsing, or graying out.

**P-3: No implied good/bad color coding.** Color or visual weight may encode only structural states: slot full vs. vacant, phase-eligible vs. gated, ATT condition met vs. not met. Color may not encode high/low activity, many/few failures, or long/short gaps.

**P-4: Raw numbers, not derived proportions.** The RPM displays raw counts. Percentages of success, failure rates, and efficiency ratios are prohibited (see also F-7). Exception: DM-class signals define their own format explicitly.

**P-5: Preregistered display thresholds.** Any threshold used to trigger a visual flag (bold text, `[MET]` marker) must be defined in the configuration document before first use, recorded with a change log, and changed only through a documented human decision.

**P-6: No trend indicators.** No directional arrows, trend lines, or change-from-last-period indicators. The RPM displays the current state only.

**P-7: Timestamp on every display.** Every dashboard view must display the exact timestamp at which data was last refreshed.

**P-8: No persistent state between sessions.** Each session queries the Trial Registry fresh. No accumulating research journal, no session-to-session comparison accumulation, no trend tracking. Exception: one named snapshot for SC-class comparison (per SC rules).

---

## 5. Considered-and-Declined Log

The considered-and-declined log prevents shadow multiplicity inflation. Hypotheses surfaced and reviewed but not submitted to the Trial Registry represent real search effort. Without a log, this effort is invisible to Harvey-Liu accounting.

**What qualifies:** Any hypothesis that was explicitly reviewed and decided against, not merely an idea not yet considered.

**Required fields per entry:**
- date
- family assignment
- one-line description
- reason not submitted
- named human sponsor who made the decision

**The RPM displays:** Count of entries (A-5) and days since last human review (D-3). The RPM does not evaluate or summarize the entries.

**Authority:** The log is human-maintained. The RPM reads it; it does not write to it.

---

## 6. MVP Specification

The MVP addresses the two genuine gaps established in the Governor ruling:
1. No cross-family evidence review mechanism
2. No explicit redundancy detection

### MVP Scope

| Component | Signals | Notes |
|---|---|---|
| Family Status Table | A-1, A-2, A-3 (DM-3), A-6 | Alphabetical, always complete |
| Derived Metrics Panel | DM-1, DM-2, DM-5, DM-6 | Basis count mandatory for DM-2 and DM-6 |
| Budget Meter | A-4, B-3, D-4, DM-4 | Weekly and 30-day views |
| Activity Gap View | B-1, B-2, D-1, D-2 | No computed quality framing |
| Attention Conditions Panel | ATT class | All conditions shown; `[MET]` marker only |
| Redundancy Checker | C-1, C-2, C-3 | Manual trigger only |
| Considered-and-Declined Log | A-5, D-3 | Count and review age only |
| Snapshot Comparison | SC class | Manual trigger; one snapshot; signed integer delta |

### MVP Display Layout

```
RESEARCH PORTFOLIO MONITOR
Refreshed: [timestamp]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAMILY STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Family                    Slot     Pass  Fail  Incon.  Pending  Last submission
────────────────────────────────────────────────────────────────────────────────
Funding Signals           FULL     3     7     1       0        47 days ago
Liquidity/Flow Signals    VACANT   0     0     0       0        never
Regime-Conditioned        GATED*   1     2     1       0        34 days ago
Structure Levels          VACANT   2     6     1       0        12 days ago
Volatility Compression    FULL     2     4     1       0        3 days ago

* GATED: requires Phase 2 entry

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DERIVED METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Family                    Pass of total          Mean resolution           Consec. fails  Avg days/submission
────────────────────────────────────────────────────────────────────────────────────────────────────────────
Funding Signals           3 of 11 resolved       29 days (9 resolved)      2              18 days (10 intervals)
Liquidity/Flow Signals    — (0 trials)           —                         —              —
Regime-Conditioned        1 of 4 resolved        41 days (4 resolved)      1              34 days (3 intervals)
Structure Levels          2 of 9 resolved        37 days (8 resolved)      4              14 days (8 intervals)
Volatility Compression    2 of 7 resolved        34 days (6 resolved)      0              10 days (6 intervals)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUDGET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This week:          2 of 3 allowed / 1 remaining
Rolling 30 days:    7 of 12 allowed / 5 remaining
M_total growth:     7 of 10 before shock-control pause / 3 remaining

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATTENTION CONDITIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID        Scope                  Field                        Threshold   Current     State
────────────────────────────────────────────────────────────────────────────────────────
ATT-001   Funding Signals        days_since_last_submission   > 30        47          [MET]
ATT-002   Liquidity/Flow         lifetime_trial_count         = 0         0           [MET]
ATT-003   Structure Levels       days_since_last_submission   > 30        12          —
ATT-004   [portfolio]            m_total_growth_30d           > 8         7           —
ATT-005   [portfolio]            weekly_submission_count      = 3         2           —

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONSIDERED-AND-DECLINED LOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Entries: 4   Last reviewed: 14 days ago   [sponsor: —]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REDUNDANCY CHECKER        [manual trigger only]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Enter candidate hypothesis text]
Threshold for FLAG: 0.80   Algorithm: TF-IDF cosine v1.0   [preregistered 2026-03-23]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SNAPSHOT COMPARISON       [manual trigger only]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[No snapshot saved]   [Save current state as snapshot]
```

---

## 7. Configuration Document Requirements

Before first use, a configuration document must exist recording:

| Item | Content |
|---|---|
| Attention conditions | All ATT-NNN entries with full schema fields |
| Proximity threshold | Numeric value for C-2 flag |
| Proximity algorithm | Algorithm name and version string |
| Gap threshold | Value used for D-1 staleness display (default: 60 days) |
| DM basis count rule | Confirmation that basis count is mandatory for DM-2 and DM-6 |
| Session comparison constraint | Confirmation that one-snapshot constraint is enforced |
| Change log | All modifications to any threshold or algorithm, with date and named human sponsor |

No threshold or algorithm parameter may be changed without a new entry in the change log with a named human sponsor.

---

## 8. Prerequisites for Integration

The following prerequisites must be satisfied before any implementation begins:

**Prerequisite 1 — Considered-and-declined log specification**
A written definition of what qualifies as "considered and declined," required fields for each entry, who is authorized to add entries, and the review cadence requirement.

**Prerequisite 2 — Preregistered display thresholds document**
A configuration document recording the similarity threshold for C-2, the gap threshold for D-1, and the text similarity algorithm identifier.

**Prerequisite 3 — This governance document**
This document must be reviewed and acknowledged by a named human sponsor before implementation begins.

---

## 9. Cross-References

- `docs/core/PROTOCOL_SPEC.md` Section E (Research Governance Interfaces) — RPM listed as governance component
- `docs/core/GLOSSARY.md` — definitions: Attention Signal (ATT), Derived Metric (DM), Session Comparison (SC), Research Portfolio Monitor (RPM)
- `docs/governance/research_firewall.md` — Research Firewall (RPM is downstream of firewall; firewall governs admissibility; RPM displays state)
- `docs/governance/hypothesis_families.md` — Hypothesis Families (ATT conditions reference family names; family definitions are authoritative here)
- `docs/governance/experiment_readiness_gate.md` — Experiment Readiness Gate (RPM displays trial counts; gate governs admissibility)
- `docs/architecture/system_architecture.md` Section 5 — Governance Layer (RPM listed as component)
