# Santiment Battle Test Run

Date: 2026-06-09
Status: completed live provider run

## Summary

- Candidates: 6
- Metric series per candidate: [6]
- Features per candidate: [6]
- Blocked candidates: 0
- Guardrail: Santiment context is retrospective enrichment only and does not change auto-validation decisions.

## Rows

| candidate | source | asset | series | features | price context | social context | sentiment context | blockers |
|---|---|---:|---:|---:|---|---|---|---|
| santiment-battle-bablos79-10250 | bablos79 | BTC | 6 | 6 | down_price_context_after_post | up_social_context_after_post | down_social_context_after_post | none |
| santiment-battle-bablos79-10328 | bablos79 | TON | 6 | 6 | up_price_context_after_post | down_social_context_after_post | up_social_context_after_post | none |
| santiment-battle-nemphiscrypts-3966 | nemphiscrypts | BTC | 6 | 6 | up_price_context_after_post | down_social_context_after_post | down_social_context_after_post | none |
| santiment-battle-nemphiscrypts-4024 | nemphiscrypts | ETH | 6 | 6 | up_price_context_after_post | down_social_context_after_post | down_social_context_after_post | none |
| santiment-battle-pifagortrade-3214 | pifagortrade | BTC | 6 | 6 | down_price_context_after_post | down_social_context_after_post | up_social_context_after_post | none |
| santiment-battle-pifagortrade-3263 | pifagortrade | ETH | 6 | 6 | up_price_context_after_post | up_social_context_after_post | down_social_context_after_post | none |

## Artifacts

- `santiment-battle-bablos79-10250`: `docs/pilot/santiment/santiment-battle-bablos79-10250.santiment_context.json`, sha256 `e74ec443a6db764ca4bb5ac8c1e983bc305d0f13078596ce9fdb6f3c2322f57a`
- `santiment-battle-bablos79-10328`: `docs/pilot/santiment/santiment-battle-bablos79-10328.santiment_context.json`, sha256 `c6f4e2ed3d78bf6728657f4e645f27d67b19ebc6ec8563655f092d2108eb93dc`
- `santiment-battle-nemphiscrypts-3966`: `docs/pilot/santiment/santiment-battle-nemphiscrypts-3966.santiment_context.json`, sha256 `9e4e40db2df6ea7b8b9424f2a15dae6907eaf60c5479d1afe590983186bfc294`
- `santiment-battle-nemphiscrypts-4024`: `docs/pilot/santiment/santiment-battle-nemphiscrypts-4024.santiment_context.json`, sha256 `29ed7ad4f62d3ac7992137ec3417bac9498fa0c3323d427c7238c5eb01316d91`
- `santiment-battle-pifagortrade-3214`: `docs/pilot/santiment/santiment-battle-pifagortrade-3214.santiment_context.json`, sha256 `bca63336a62ab2819646ad6ebb77b6f8971a651e8333e2bd255aeb7b94debad2`
- `santiment-battle-pifagortrade-3263`: `docs/pilot/santiment/santiment-battle-pifagortrade-3263.santiment_context.json`, sha256 `94a5df884963d764b6a05b1073ea308747267d24382033a0c7b1388c3f5a2f11`
