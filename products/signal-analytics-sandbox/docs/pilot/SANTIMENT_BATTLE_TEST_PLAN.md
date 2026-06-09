# Santiment Battle Test Plan

Date: 2026-06-09
Status: ready for operator-gated live run

## Purpose

Use Santiment as retrospective context for Telegram crypto candidates. The goal
is to learn whether channel posts appeared before, during, or after social,
sentiment, on-chain, exchange-flow, and price regime changes.

## Guardrails

- Santiment context is enrichment only.
- It must not auto-accept claims, mark wins/losses, or bypass provider,
  customer-policy, or human-review gates.
- Provider calls require `SIGNAL_SANDBOX_ENABLE_SANTIMENT=1`, a
  `SIGNAL_SANDBOX_SANTIMENT_API_KEY`, and CLI `--approve`.
- Every live run must persist JSON and Markdown artifacts with SHA-256 hashes.

## First Live Run

Inputs:

- 5 to 10 crypto `AutoValidationEvidenceBundle` artifacts from the current
  Telegram media candidates.
- Prefer BTC, ETH, SOL, TON, AVAX, ARB, SUI, or DOT rows because they have
  built-in Santiment slug mappings.

Command shape:

```bash
SIGNAL_SANDBOX_ENABLE_SANTIMENT=1 \
SIGNAL_SANDBOX_SANTIMENT_API_KEY=<operator-key> \
signal-sandbox santiment-context \
  --bundle docs/pilot/auto_validation/<candidate>.bundle.json \
  --output-dir docs/pilot/santiment \
  --approve
```

Expected artifacts:

- `docs/pilot/santiment/<candidate>.santiment_context.json`
- `docs/pilot/santiment/<candidate>.santiment_context.md`

Review questions:

- Did the post precede a social-volume or sentiment move?
- Did exchange inflow/outflow context support or contradict the post timing?
- Was price already moving before the post, or did movement follow it?
- Are patterns different across `bablos79`, `nemphiscrypts`, and
  `pifagortrade`?
- Which rows remain blocked because the asset has no Santiment slug or metric
  access under the operator account?

Pass criteria:

- At least 5 artifacts generated.
- Every artifact has a stable artifact SHA-256 and metric-series refs.
- No artifact changes auto-validation decision state by itself.
- A follow-up summary identifies channel-level retrospective hypotheses to test
  on a larger corpus.
