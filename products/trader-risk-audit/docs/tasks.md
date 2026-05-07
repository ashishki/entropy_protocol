# Trader Risk Audit Tasks

Status: Primary commercial MVP task contract.

```yaml
Task: TRA-001
Owner: validation-gtm
Phase: A
Type: validation
Depends-On: []
Objective: Prove that traders will share exports, written rules, and pay for an audit.
Acceptance-Criteria:
  - id: AC1
    description: 20 qualified conversations completed.
    test: manual-evidence
  - id: AC2
    description: 5 real trade exports collected.
    test: manual-evidence
  - id: AC3
    description: 3 paid audit reports sold from 10 qualified prospects.
    test: manual-evidence
Files:
  - products/trader-risk-audit/docs/PROJECT_BRIEF.md
Notes: No product engineering before this gate.
```

```yaml
Task: TRA-002
Owner: product-ux
Phase: B
Type: documentation
Depends-On:
  - TRA-001
Objective: Create the manual audit report template.
Acceptance-Criteria:
  - id: AC1
    description: Template includes rule summary, violations, P&L impact, and next-review checklist.
    test: doc-review
  - id: AC2
    description: Template avoids OOS, performance, investment advice, and live-control claims.
    test: doc-review
Files:
  - products/trader-risk-audit/docs/report_template.md
Notes: Keep report understandable to a trader in under five minutes.
```

```yaml
Task: TRA-003
Owner: data-import
Phase: C
Type: design
Depends-On:
  - TRA-001
Objective: Define canonical trade import schema from real pilot exports.
Acceptance-Criteria:
  - id: AC1
    description: Schema covers timestamp, symbol, side, quantity, price, fees, account, and source.
    test: doc-review
  - id: AC2
    description: Missing/ambiguous fields have explicit validation errors.
    test: doc-review
Files:
  - products/trader-risk-audit/docs/import_schema.md
Notes: Do not design live broker integration.
```

```yaml
Task: TRA-004
Owner: rule-engine
Phase: C
Type: design
Depends-On:
  - TRA-001
Objective: Define deterministic risk policy and violation record contracts.
Acceptance-Criteria:
  - id: AC1
    description: Each MVP rule has inputs, evaluation logic, and violation output fields.
    test: doc-review
  - id: AC2
    description: Rule evaluation is deterministic and does not use AI.
    test: doc-review
Files:
  - products/trader-risk-audit/docs/risk_policy_spec.md
Notes: Future implementation may move shared contracts into Entropy Core.
```

```yaml
Task: TRA-005
Owner: reporting
Phase: D
Type: implementation
Depends-On:
  - TRA-002
  - TRA-003
  - TRA-004
Objective: Implement the minimum report-generation path only after paid validation.
Acceptance-Criteria:
  - id: AC1
    description: Report can be generated from normalized trades and a risk policy.
    test: tests-required
  - id: AC2
    description: Report includes no unsupported performance or live-control claims.
    test: tests-required
Files:
  - products/trader-risk-audit/
Notes: Implementation task requires a separate root coding task if shared entropy modules are touched.
```

