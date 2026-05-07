from __future__ import annotations

from trader_risk_audit.policy.review import PolicyReviewPacket
from trader_risk_audit.policy.schema import RiskPolicy


class PolicyReviewRequiredError(ValueError):
    def __init__(self, packet: PolicyReviewPacket) -> None:
        self.packet = packet
        rule_ids = ", ".join(item.rule_id for item in packet.unresolved_items)
        super().__init__(f"policy review required before evaluation: {rule_ids}")


def ensure_policy_ready_for_evaluation(
    policy: RiskPolicy,
    review_packet: PolicyReviewPacket,
) -> RiskPolicy:
    if review_packet.unresolved_items:
        raise PolicyReviewRequiredError(review_packet)
    return policy
