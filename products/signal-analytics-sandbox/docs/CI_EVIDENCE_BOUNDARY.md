# CI Evidence Boundary

The review-queue tests use
`tests/fixtures/review/synthetic_full_review_queue.json`. The fixture is a
small, deterministic schema and gate contract built only from invented values
under the reserved `example.invalid` domain.

The fixture contains no trader, pilot, customer, Telegram, provider, or other
user data. It is not pilot or user evidence, does not validate historical
full-corpus counts, and does not support adoption, production, quality, or
external-readiness claims.

Large `docs/pilot/*FULL_REVIEW_QUEUE.*` artifacts remain outside Git. A clean
checkout therefore cannot revalidate their historical aggregate claims. CI
instead verifies that:

- review-queue JSON is strictly validated;
- every required row field is present;
- external delivery remains blocked without complete review decisions;
- accepted decisions require reviewer and source evidence;
- static review rendering preserves source and normalized fields.

Any real full-review artifact must be validated separately in an
operator-controlled workspace. Its results may be promoted only as sanitized
aggregate evidence after an explicit privacy and provenance review. Until that
happens, external delivery remains blocked.
