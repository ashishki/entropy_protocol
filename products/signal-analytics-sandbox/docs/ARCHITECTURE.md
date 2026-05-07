# Signal Analytics Sandbox Architecture

## Shape

Initial shape: manual feasibility study plus structured public-source ledger.

## Data Flow

1. Select public source.
2. Record observable signal messages and timestamps.
3. Normalize signal into structured record when possible.
4. Compare signal to market outcome using explicit assumptions.
5. Produce report with limitations and missing-data notes.

## Components

| Component | Purpose | Status |
|---|---|---|
| Source ledger | Timestamped public signal records | Proposed |
| Signal parser | Manual or rule-assisted extraction | Proposed |
| Outcome calculator | Entry/exit assumption evaluation | Proposed |
| Report generator | Channel/source report | Proposed |
| Terms risk memo | Legal/product constraints | Required before engineering |

## Boundaries

- Public sources only.
- No private group scraping.
- No source impersonation.
- No hidden paid API dependency before validation.
- No investment advice claims.

