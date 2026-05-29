# CODEX_PROMPT.md - Signal Analytics Sandbox

Version: 3.05
Date: 2026-05-23
Phase: 38
Compact restart state only. Detailed history lives in
`docs/IMPLEMENTATION_JOURNAL.md`, `docs/archive/`, and `docs/tasks.md`.

## Current State

- Phase: 38 (Client-Readiness Evidence Acceptance)
- Baseline: 362 pass / 0 skip
- Ruff: `ruff check src/ tests/ scripts/` passes
- Format: `ruff format --check src/ tests/ scripts/` passes
- Pyright: `.venv/bin/pyright` passes
- Latest completed: `SAS-PRECLIENT-010 Phase 37 Deep Review And Client-Readiness Decision`
- Phase 37 decision: `continue_internal_hardening`
- Engineering Phase 1 (T01+) may begin.
- | SAS-001: Paid Pilot Demand Validation | acknowledged |
- | SAS-002: Public-Source Legal/Terms Memo | acknowledged |
- External gate: `approve_internal_only`
- External delivery: not approved
- Current priority: operator acceptance, accepted-row recompute, and redacted
  demo readiness before buyer outreach.

## Next Task

Active route: Phase 38 client-readiness evidence acceptance.

- Two-month source window `2026-03-22..2026-05-22`: 526 text rows,
  37 normalized claims, 28 7d evaluable, 19 confirmed, 9 contradicted.
- Multimodal pass: 570 public posts, 295 media refs, 70 voice transcripts,
  185 image/OCR drafts, 40 video/manual blockers, 1 internal RR-ready draft.
- Media reviewer pass: `gpt-4.1-mini` reviewed 255 drafts; `gpt-4.1`
  arbitrated 35 high-signal rows and accepted 9 internal candidates.
- Phase 37 produced contract, model packet, 301-row appendix, dashboard cards,
  internal reports, paid-style demo, candidate outcomes, static dashboard,
  safety gate, and deep review.
- Phase 37 review says the package is a valid internal diligence baseline, not
  a client-valid product. Buyer conversations remain blocked.
- Next task: `SAS-CLIENTREADY-001` operator media acceptance ledger.

Read first: `docs/tasks.md` Phase 38,
`docs/archive/PHASE37_PRECLIENT_REVIEW.md`,
`docs/pilot/preclient_MODEL_REVIEW_PACKET.md`,
`docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md`.

Supporting cross-product cognition vault on this VPS:
`/srv/codex-entropy/repos/product-3/engineering-cognition-vault/10-projects/entropy-protocol.md`.
Product-local docs remain authoritative.

## Canonical Artifacts

- Phase 37 review: `docs/archive/PHASE37_PRECLIENT_REVIEW.md`
- Pre-client contract: `docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md`
- Pre-client model packet: `docs/pilot/preclient_MODEL_REVIEW_PACKET.md`
- Pre-client evidence appendix: `docs/pilot/preclient_EVIDENCE_APPENDIX.md`
- Pre-client dashboard cards: `docs/pilot/preclient_FREE_DASHBOARD_CARDS.md`
- Pre-client candidate outcomes: `docs/pilot/preclient_CANDIDATE_OUTCOMES.md`
- Pre-client dashboard: `docs/pilot/preclient_dashboard/index.html`
- Pre-client safety gate: `docs/pilot/preclient_ARTIFACT_SAFETY_GATE.md`
- Pre-client reports: `docs/pilot/reports/preclient/`
- Two-month multimodal run: `docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md`
- Media reviewer run: `docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md`

## Key Product Facts

- V1 evaluable claims: `bablos79` 14, `nemphiscrypts` 49, `pifagortrade` 107.
- Safety gate covers 14 artifacts, 0 forbidden phrase findings, 0 showable now.
- Model packet has 9 internal candidates and 0 customer-facing rows.
- Candidate outcomes: 4 insufficient fields, 4 post-factum-only, 1 provider gap,
  1 internal RR recompute, 0 market outcomes recomputed.
- Main blockers: 0 operator-accepted media claims, 0 dashboard-safe RR rows,
  0 market-outcome recomputed candidates.

Supporting cross-product cognition vault on this VPS:
`/srv/codex-entropy/repos/product-3/engineering-cognition-vault/10-projects/entropy-protocol.md`.
Product-local docs remain authoritative.

## Active Guardrails

- Public/operator-authorized sources only.
- No private scraping, access-control bypass, advice, future-profit claims,
  unsupported ranking, marketplace framing, payment flow, or private-source
  promise.
- Unsupported providers/proxies are exclusions, not wins/losses.
- Unreviewed transcript/OCR/chart claims stay out of customer-facing metrics.
- Every buyer-facing artifact requires an explicit gate.
