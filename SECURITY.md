# Security policy

Entropy Protocol is a local research monorepo, not a hosted service. Reports are
accepted only for the current `master` revision and the documented local
product/CI boundaries. There is no production deployment, stable monorepo
release, security SLA, or authorization to test systems or data you do not own.

Do not open a public issue for a suspected vulnerability or exposed private
material. Email `verter25@gmail.com` with subject `entropy_protocol security
report`. Name the exact commit, owning product path, prerequisites, impact, and
minimal synthetic reproduction. Keep the first message minimal; do not attach
credentials, private trades, Telegram exports, customer/operator data, or an
exploit against third-party infrastructure. A safer detail-transfer path can be
agreed before sending sensitive material.

GitHub private vulnerability reporting is not assumed to be enabled. Use a
GitHub private advisory form only if the repository Security page visibly
offers **Report a vulnerability**. Reports will be triaged against the explicit
boundaries in `docs/CONTRIBUTION_ROUTING.md`, but this maintainer-run research
repository cannot promise a response or remediation deadline.

If a credential is exposed, revoke or rotate it at the provider. Removing a
file or rewriting Git history does not make an exposed value safe again.
