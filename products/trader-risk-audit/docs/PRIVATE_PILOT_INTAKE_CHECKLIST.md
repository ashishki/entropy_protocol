# Private Pilot Intake Checklist

Status: active Phase 25 checklist
Date: 2026-05-15
Audience: operator only

This checklist prepares 1-3 operator-approved private or anonymized audit
inputs without committing raw private data. It is local-only preparation, not
SaaS onboarding, checkout, hosted upload, live exchange control, trading advice,
or automatic report delivery.

## Operator Approval Gate

Before any private input is processed, record operator approval outside git
using a local note or queue item with only:

- non-sensitive pilot label, for example `pilot_alpha_001`;
- intake method: `csv_export`, `bybit_read_only_api`, or
  `binance_read_only_api`;
- approved audit period;
- approved timezone and session window;
- approved risk-rules source;
- approval timestamp;
- deletion trigger date or event.

Do not record real names, handles, account ids, private paths, payment details,
or raw row excerpts in git.

## Allowed Files

Allowed in the operator-controlled local workspace outside git:

- one private or anonymized `.csv` trade export;
- `.xlsx` only as a candidate input for manual conversion/review, not direct
  committed evidence;
- written risk rules as a local text, Markdown, YAML, or template response;
- local intake request metadata containing only safe labels and audit settings;
- generated local artifacts under the operator workspace, subject to manual
  review before any delivery.

Allowed in git:

- safe aggregate run notes created later under `docs/private_pilot_runs/`;
- checklist completion status without private row values;
- non-sensitive blocker tags;
- report review status and delivery decision;
- hashes of safe summary artifacts only when they do not reveal private paths.

## Forbidden Data

Never commit or paste into docs, tests, fixtures, queue records, reports, or
run notes:

- raw private trade rows;
- broker account ids, exchange account ids, internal account ids, or balances;
- API keys, secrets, passwords, seed phrases, bearer tokens, signed URLs,
  request signatures, or session cookies;
- Telegram handles, emails, phone numbers, names, addresses, payment ids,
  invoices, receipts, or checkout metadata;
- private local paths, home directories, cloud-sync paths, screenshots with
  identifiers, or unapproved screenshots;
- broker statements, support chats, CRM notes, private journals, free-text
  trader notes, or documents outside the approved audit input;
- live order, withdrawal, transfer, leverage/margin mutation, or account-control
  credentials.

If any forbidden data is present, stop intake and request a redacted export or
operator-approved local handling outside git.

## Redaction Expectations

Before processing:

1. Replace real trader/account labels with a stable pilot label.
2. Remove columns that are not needed for deterministic audit rules when they
   contain private identifiers or notes.
3. Keep required canonical trade fields available locally:
   `timestamp`, `symbol`, `side`, `quantity`, `price`, `fees`, and safe
   account scope.
4. Preserve timezone, session, currency, and audit-period metadata.
5. Keep original private exports outside git and outside shared screenshots.
6. If redaction changes calculation fields, do not run the audit until the
   operator approves the transformed fixture as representative.

## Local Storage Rules

- Store private inputs outside the repository, under an operator-controlled
  workspace such as `../private-pilot-workspaces/<pilot_label>/`.
- Add no private input path to committed docs. Use safe labels only.
- Keep generated local artifacts in that same private workspace until manual
  review decides whether a safe summary can be committed.
- Do not sync private workspaces to public cloud folders unless the operator has
  explicitly approved that storage.
- Keep read-only exchange credentials, if used in a future approved flow, in
  approved local secret handling only. Do not store them in workspace files.

## Deletion Trigger

Set a deletion trigger before processing:

- default: delete private inputs and unreviewed generated artifacts 14 days
  after delivery decision;
- earlier deletion if the trader withdraws consent;
- immediate deletion if forbidden data is discovered in the wrong location;
- keep only safe aggregate run notes after deletion.

Use local retention tooling for generated audit artifacts when a manifest exists:

```bash
.venv/bin/python -m trader_risk_audit.cli retention list --manifest <private_manifest_json>
.venv/bin/python -m trader_risk_audit.cli retention delete --manifest <private_manifest_json> --dry-run
.venv/bin/python -m trader_risk_audit.cli retention delete --manifest <private_manifest_json> --confirm-delete
```

Do not paste the private manifest path into committed docs.

## Command Mapping

Run commands only against files in the private local workspace. The examples use
placeholders; do not replace them with real private paths in git.

1. Create safe intake session metadata:

```bash
.venv/bin/python -m trader_risk_audit.cli intake create \
  --output-dir <private_workspace>/intake \
  --prospect-label <safe_pilot_label> \
  --source-type csv_export \
  --source-file <private_workspace>/input/export.csv \
  --risk-rules-file <private_workspace>/input/rules.md \
  --source-timezone UTC \
  --display-timezone Europe/Berlin \
  --session-start 00:00 \
  --session-end 23:59 \
  --currency USD
```

2. Profile the CSV schema safely:

```bash
.venv/bin/python -m trader_risk_audit.cli intake profile \
  --session <private_workspace>/intake/intake_session.json \
  --csv <private_workspace>/input/export.csv \
  --output-dir <private_workspace>/intake
```

3. Render the intake report:

```bash
.venv/bin/python -m trader_risk_audit.cli intake report \
  --session <private_workspace>/intake/intake_session.json \
  --profile <private_workspace>/intake/schema_profile.json \
  --output-dir <private_workspace>/intake
```

4. Build or flow the policy only after operator approval:

```bash
.venv/bin/python -m trader_risk_audit.cli policy flow \
  --schema-profile <private_workspace>/intake/schema_profile.json \
  --account-id <safe_account_scope> \
  --source-timezone UTC \
  --session-start 00:00 \
  --session-end 23:59 \
  --output-dir <private_workspace>/policy
```

or:

```bash
.venv/bin/python -m trader_risk_audit.cli policy build \
  --session <private_workspace>/intake/intake_session.json \
  --profile <private_workspace>/intake/schema_profile.json \
  --account-id <safe_account_scope> \
  --output-dir <private_workspace>/policy
```

5. Run the local audit session:

```bash
.venv/bin/python -m trader_risk_audit.cli audit-session run \
  --session <private_workspace>/intake/intake_session.json \
  --policy <private_workspace>/policy/policy.yaml \
  --input-dir <private_workspace>/input \
  --output-dir <private_workspace>/run \
  --policy-status approved
```

6. Bundle artifacts for local review:

```bash
.venv/bin/python -m trader_risk_audit.cli audit-session bundle \
  --run-dir <private_workspace>/run \
  --output <private_workspace>/run/bundle_index.json
```

7. Use direct `audit` only for an already approved local CSV/policy pair:

```bash
.venv/bin/python -m trader_risk_audit.cli audit \
  --trades <private_workspace>/input/export.csv \
  --policy <private_workspace>/policy/policy.yaml \
  --output-dir <private_workspace>/run
```

## Stop Conditions

Stop before audit execution if:

- source provenance or consent is unclear;
- required canonical fields are missing and cannot be safely mapped;
- written risk rules are ambiguous and lack operator approval;
- private identifiers are needed to explain the report;
- the user asks for advice, order blocking, live control, or guaranteed
  performance;
- read-only API permissions cannot be verified;
- deletion trigger is not recorded.

## Checklist Signoff

| Check | Status | Notes |
|---|---|---|
| Operator approval recorded outside git | pending | safe label only |
| Allowed file set confirmed | pending | no private path in git |
| Forbidden data scan completed | pending | no rows or identifiers committed |
| Redaction approved | pending | calculation fields preserved |
| Local storage location approved | pending | outside repo |
| Deletion trigger set | pending | date or event |
| Intake/session command selected | pending | existing CLI only |
| Policy mapping approval ready | pending | no unresolved ambiguity |
| Report review checklist next | pending | use T111 artifact |
