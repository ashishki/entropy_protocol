# Repository CI and product routing

Status reviewed: 2026-07-13

## Why routing is explicit

Entropy Protocol is a source-history monorepo, not one product or shared
runtime. A green check for one workspace does not validate another workspace,
and a product-specific change must not be hidden inside a root portfolio or CI
edit. GitHub discovers workflow files only under root `.github/workflows/`;
nested `.github/workflows/` files inside product directories are local
templates, not active GitHub Actions checks for this repository.

## Owning surfaces and gates

| Surface | Owning path | Active root workflow | Local gate from owning path | Bounded public intake |
| --- | --- | --- | --- | --- |
| Repository orchestration | `README.md`, `docs/`, root `.github/` | The affected workflow below | `python tools/verify_repository_surface.py` from root | Root workflow trigger, dependency, action, or routing defects only |
| Entropy Core | `products/entropy-core/` | `.github/workflows/ci.yml` | Ruff, Pyright, and `python -m pytest tests/ -q --tb=short` | Not currently offered; use the local gate for a scoped pull request |
| Signal Analytics Sandbox | `products/signal-analytics-sandbox/` | `.github/workflows/signal-analytics-sandbox-ci.yml` | Ruff, Pyright, and `python -m pytest tests/ -q --tb=short` | Not currently offered; use the local gate for a scoped pull request |
| Trader Risk Audit | `products/trader-risk-audit/` | `.github/workflows/trader-risk-audit-ci.yml` | Ruff and `python -m pytest tests -q --tb=short` | Not currently offered; use the local gate for a scoped pull request |

Every root-CI issue must name the exact commit, active root workflow, owning
path, clean-checkout reproduction, and synthetic/local boundary. For a run that
exists, include its URL and exact job/step. For a discovery or path-trigger
failure where no run exists, include the event, ref, changed-path comparison,
expected workflow, and the Actions-page check showing no matching run. A
root-CI change may adjust orchestration needed to execute the product's own
gate; it must not silently change product rules, thresholds, datasets, or
claims.

Product-behavior issue intake is not currently offered: the root chooser has no
product form and blank issues remain disabled. A proposed product fix must stay
within one owning path, reproduce against its documented local gate, and arrive
as an explicitly scoped pull request. This is a routing statement, not an
invitation to publish private inputs or vulnerability details.

## Out of scope for public intake

- generic features, product-roadmap requests, shared-platform abstractions, or
  a monorepo-wide release;
- live trading, order execution/blocking, exchange mutation, investment advice,
  strategy or performance claims;
- private Telegram sources, private trades, customer/operator data, credentials,
  tokens, production endpoints, or local absolute paths;
- treating synthetic fixtures, public-source rehearsals, tests, or Markdown as
  users, adoption, commercial validation, production operation, or regulatory
  evidence;
- moving code between products without an explicit dependency, history,
  licensing, and evidence review.

This repository has no root open-source license. Public visibility and issue
intake do not grant a general right to copy, modify, redistribute, or combine
the product workspaces. Any future license decision is product-specific and
requires a separate dependency and source-material review.

## Security and private material

Do not post a suspected vulnerability, secret, private export, exploit detail,
or personal data in an issue. Follow `SECURITY.md`. If public material was
included accidentally, stop publication and rotate/revoke any exposed
credential; deleting a later commit does not retract already fetched copies.

## Root-CI defect acceptance

The root form is accepted only when the failure is reproducible at the reported
revision and belongs to workflow discovery, trigger/path routing, dependency
installation, action/runtime setup, or execution of an existing product gate.
The absence of a run is valid evidence for a discovery or trigger defect when
the event, ref, changed paths, expected workflow, and no-run check are supplied.
The smallest fix must preserve the owning product's local command. Product
behavior changes need a separate, explicitly scoped product review.
