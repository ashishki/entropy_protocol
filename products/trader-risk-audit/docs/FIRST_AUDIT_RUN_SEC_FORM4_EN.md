# First Audit Run - SEC Form 4 Open Source

Status: T65 artifact run complete
Date: 2026-05-12
Input fixture: `demo/open_source_sec_form4_001/trades.csv`
Policy: `demo/open_source_sec_form4_001/policy.yaml`
Output directory: `demo/open_source_sec_form4_001/output/`

## Command

```bash
.venv/bin/python -m trader_risk_audit audit \
  --trades demo/open_source_sec_form4_001/trades.csv \
  --policy demo/open_source_sec_form4_001/policy.yaml \
  --output-dir demo/open_source_sec_form4_001/output
```

Result:

```text
wrote audit manifest: demo/open_source_sec_form4_001/output/manifest.json
```

## Artifact Pack

| Artifact | Path | SHA-256 |
|---|---|---|
| source export | `demo/open_source_sec_form4_001/trades.csv` | `7ced77044c53e39bcdb03a8a708826a75dae1a152db4c5fab31c55f03dcdfe4e` |
| policy file | `demo/open_source_sec_form4_001/policy.yaml` | `236ee1f0375f1cbe19b0edfb913b126b84fc4b6a1a8e272b2eda84cb464c705e` |
| normalized trades | `demo/open_source_sec_form4_001/output/normalized_trades.json` | `648df0bac83a16a0229515b7a26d10e93dc3c1e89ead9631db26b8bfdabff856` |
| violations | `demo/open_source_sec_form4_001/output/violations.json` | `c123323724d99fed7896019f73c8f68049ec2680af4db156ca2e649eb2759582` |
| attribution summary | `demo/open_source_sec_form4_001/output/attribution_summary.json` | `b797673281937accdd0349e18e155dc4acce9eab824bea196fcf0740659c74e8` |
| Markdown report | `demo/open_source_sec_form4_001/output/report.md` | `02aeb77e66c59869b72e56a6d89f6b348e2002a713728c2854fa8ee55cd1d524` |
| delivery packet | `demo/open_source_sec_form4_001/output/telegram_packet.txt` | `9eda7aeb28ab2d1f435bdc0622f6dcb58f5c4114e7f30c62aa6aa1430fbc0070` |

Manifest content hash:

```text
9cfdd76e5904f3e512f6c04a9321706b7071e712b3868841c8817e93469907e8
```

## Determinism Check

Rerun command:

```bash
.venv/bin/python -m trader_risk_audit audit \
  --trades demo/open_source_sec_form4_001/trades.csv \
  --policy demo/open_source_sec_form4_001/policy.yaml \
  --output-dir /tmp/trader-risk-audit-sec/open_source_sec_form4_rerun
```

Primary and rerun manifest content hashes matched:

```text
9cfdd76e5904f3e512f6c04a9321706b7071e712b3868841c8817e93469907e8
```

## Report Review

Generated report:

- includes executive summary;
- includes repeated patterns;
- includes traceable violation table with SEC-derived source row ids;
- includes P&L attribution section with zero P&L because the source lacks
  account-level realized P&L;
- includes unsupported leverage limitation;
- includes no-advice/no-live-control disclaimer.

## Critical Limitations For T66/T67

The report is mechanically complete but must be polished before external use:

- `max_position_size` is a transaction-notional proxy in this fixture, not a
  true open-position exposure rule.
- `SVRE` is a validation watchlist symbol, not a real customer restriction or
  investment view.
- P&L, daily loss, and drawdown are not meaningful for this source and must not
  be presented as customer/account performance.
- The generic report currently shows zero P&L attribution; T67 should make the
  open-source limitation visible in first-screen report text.
- External delivery remains blocked until T66 manual calculation validation and
  T67 claim-safety review complete.
