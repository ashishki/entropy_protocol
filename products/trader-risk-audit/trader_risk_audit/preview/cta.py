from __future__ import annotations

from dataclasses import dataclass

PAID_PILOT_PRICE_HYPOTHESIS = "$49-$149"
PAID_PILOT_TURNAROUND = "48-72 hours"


@dataclass(frozen=True)
class PaidPilotCta:
    eligible: bool
    title: str
    terms: tuple[str, ...]
    boundaries: tuple[str, ...]


def build_paid_pilot_cta(*, audit_status: str) -> PaidPilotCta:
    return PaidPilotCta(
        eligible=audit_status == "complete",
        title="Paid Pilot Review",
        terms=(
            "One manual reviewed audit report for one completed export period.",
            "Required inputs: real trade export, written risk rules, timezone, "
            "session window, account currency, and privacy confirmation.",
            f"Turnaround: {PAID_PILOT_TURNAROUND} after complete inputs and "
            "operator-approved mapping.",
            f"Pricing hypothesis: {PAID_PILOT_PRICE_HYPOTHESIS} for one manual "
            "audit report, confirmed manually before work starts.",
        ),
        boundaries=(
            "No SaaS account, checkout flow, payment processing, or hosted file "
            "storage is implemented here.",
            "No investment advice, live trading control, order blocking, broker "
            "control, or guaranteed improvement.",
        ),
    )


def render_paid_pilot_cta(cta: PaidPilotCta) -> str:
    if not cta.eligible:
        return ""
    lines = [
        "## Paid Pilot CTA",
        "",
        f"**{cta.title}**",
        "",
        "Package:",
        *[f"- {term}" for term in cta.terms],
        "",
        "Boundaries:",
        *[f"- {boundary}" for boundary in cta.boundaries],
        "",
    ]
    return "\n".join(lines)
