# Conversation Outcome Scoring Rubric

Status: complete_for_operator_use
Date: 2026-05-19
Phase: 30

## Purpose

Use this rubric after each problem interview or report review to convert
conversation outcomes into aggregate evidence.

Do not use this to score people by name in git. Score outside git, then
summarize only aggregate counts.

## Scores

| Area | 0 | 1 | 2 |
|---|---|---|---|
| Pain recency | No past issue | Vague past issue | Specific recent issue |
| Workflow clarity | No workflow | Informal workflow | Repeatable review workflow |
| Report usefulness | Not useful | Some useful parts | Clear workflow use |
| Trust path | No trust path | Trust possible with changes | Trust possible with current limitations |
| Export willingness | Refuses export | Maybe later | Will prepare approved anonymized export |
| Pilot willingness | No next step | Wants more review | Accepts concrete manual pilot next step |

Total score:

- `10-12`: strong candidate for T116/export follow-up.
- `7-9`: continue concierge validation.
- `4-6`: weak signal, revisit ICP or offer.
- `0-3`: no-fit or disqualified.

## Decision Mapping

| Aggregate pattern | Decision |
|---|---|
| At least one `export_willing_yes` with approved anonymized export outside git | `return_to_t116` |
| 5+ interviews score 7+ but no export is ready | `continue_concierge_validation` |
| One ICP has 2x more 7+ scores than others | `narrow_icp` |
| Pain is high but report usefulness is under 2/5 or trust blockers dominate | `revise_offer` |
| Most interviews score under 4 and no concrete next step appears | `pause_or_pivot` |

## Interpretation Rules

- Compliments without past behavior score 0 for pain recency.
- Interest in signals, strategy, or live order control is a disqualifier, not a
  product opportunity for this scope.
- Export willingness matters more than demo praise.
- Paid willingness matters more than report aesthetics.
- Referrals and repeat commitments matter more than one-off curiosity.

