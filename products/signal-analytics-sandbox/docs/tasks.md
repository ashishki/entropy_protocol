# Signal Analytics Sandbox Tasks

Status: Separate validation sandbox task contract.

```yaml
Task: SAS-001
Owner: signal-sandbox
Phase: A
Type: validation
Depends-On: []
Objective: Validate whether public signal-source reports are technically and commercially worth pursuing.
Acceptance-Criteria:
  - id: AC1
    description: 3 public sources selected without private access or scraping controls.
    test: manual-evidence
  - id: AC2
    description: Manual signal ledger produced for at least one source.
    test: manual-evidence
  - id: AC3
    description: At least 5 target users review a sample report.
    test: manual-evidence
Files:
  - products/signal-analytics-sandbox/docs/PROJECT_BRIEF.md
Notes: This task must not modify Entropy Core.
```

```yaml
Task: SAS-002
Owner: legal-risk
Phase: A
Type: research
Depends-On:
  - SAS-001
Objective: Produce a terms/liability memo for Telegram/X public-source analytics.
Acceptance-Criteria:
  - id: AC1
    description: Memo states allowed sources, forbidden sources, and data-retention rules.
    test: doc-review
  - id: AC2
    description: Memo explicitly rejects private group scraping.
    test: doc-review
Files:
  - products/signal-analytics-sandbox/docs/legal_risk_memo.md
Notes: Engineering is blocked until this exists.
```

