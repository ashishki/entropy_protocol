from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

PAID_UNLOCK_STATUSES = (
    "preview_only",
    "paid_requested",
    "operator_reviewed",
    "delivered",
)
_ALLOWED_TRANSITIONS = {
    "preview_only": frozenset({"paid_requested"}),
    "paid_requested": frozenset({"operator_reviewed"}),
    "operator_reviewed": frozenset({"delivered"}),
    "delivered": frozenset(),
}
_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_HANDLE_PATTERN = re.compile(r"@[A-Za-z][A-Za-z0-9_]{4,}")
_LONG_NUMBER_PATTERN = re.compile(r"\b\d{6,}\b")


class PaidUnlockError(ValueError):
    pass


@dataclass(frozen=True)
class PaidUnlockState:
    audit_id: str
    status: str
    manual_payment_evidence: str = "none"
    operator_reviewed: bool = False
    claim_safe: bool = False
    delivered_ref: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def create_preview_unlock_state(audit_id: str) -> PaidUnlockState:
    return PaidUnlockState(
        audit_id=_safe_label(audit_id, field="audit_id"),
        status="preview_only",
    )


def transition_paid_unlock_state(
    state: PaidUnlockState,
    next_status: str,
    *,
    manual_payment_evidence: str | None = None,
    claim_safe: bool | None = None,
    delivered_ref: str | None = None,
) -> PaidUnlockState:
    normalized_next = _validate_status(next_status)
    if normalized_next not in _ALLOWED_TRANSITIONS[state.status]:
        raise PaidUnlockError(
            f"cannot transition paid unlock from {state.status} to {normalized_next}"
        )
    if normalized_next == "paid_requested":
        evidence = _safe_label(
            manual_payment_evidence or "manual_intent_recorded",
            field="manual_payment_evidence",
        )
        return PaidUnlockState(
            audit_id=state.audit_id,
            status=normalized_next,
            manual_payment_evidence=evidence,
        )
    if normalized_next == "operator_reviewed":
        return PaidUnlockState(
            audit_id=state.audit_id,
            status=normalized_next,
            manual_payment_evidence=state.manual_payment_evidence,
            operator_reviewed=True,
            claim_safe=bool(claim_safe),
        )
    if normalized_next == "delivered":
        if not state.operator_reviewed or not state.claim_safe:
            raise PaidUnlockError("delivery requires operator review and claim safety")
        return PaidUnlockState(
            audit_id=state.audit_id,
            status=normalized_next,
            manual_payment_evidence=state.manual_payment_evidence,
            operator_reviewed=True,
            claim_safe=True,
            delivered_ref=_safe_ref(delivered_ref or "delivery_packet"),
        )
    raise PaidUnlockError("unsupported paid unlock transition")


def load_paid_unlock_state(path: str | Path) -> PaidUnlockState:
    state_path = Path(path)
    if not state_path.exists():
        return create_preview_unlock_state(audit_id=state_path.stem)
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise PaidUnlockError("paid unlock state must contain a JSON object")
    return PaidUnlockState(
        audit_id=_safe_label(payload.get("audit_id"), field="audit_id"),
        status=_validate_status(str(payload.get("status", ""))),
        manual_payment_evidence=_safe_label(
            payload.get("manual_payment_evidence", "none"),
            field="manual_payment_evidence",
        ),
        operator_reviewed=bool(payload.get("operator_reviewed", False)),
        claim_safe=bool(payload.get("claim_safe", False)),
        delivered_ref=(
            _safe_ref(str(payload["delivered_ref"]))
            if payload.get("delivered_ref")
            else None
        ),
    )


def write_paid_unlock_state(state: PaidUnlockState, path: str | Path) -> Path:
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(state.to_json(), encoding="utf-8")
    return state_path


def _validate_status(value: str) -> str:
    status = value.strip().casefold()
    if status not in PAID_UNLOCK_STATUSES:
        raise PaidUnlockError("unsupported paid unlock status")
    return status


def _safe_label(value: object, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PaidUnlockError(f"{field} is required")
    normalized = value.strip()
    lowered = normalized.casefold()
    if "\n" in normalized or "\r" in normalized:
        raise PaidUnlockError(f"{field} must be single-line")
    if _EMAIL_PATTERN.search(normalized) or _HANDLE_PATTERN.search(normalized):
        raise PaidUnlockError(f"{field} must not contain identifiers")
    if _LONG_NUMBER_PATTERN.search(normalized):
        raise PaidUnlockError(f"{field} must not contain payment identifiers")
    forbidden = ("payment_id", "transaction", "stripe", "checkout", "api_key")
    if any(word in lowered for word in forbidden):
        raise PaidUnlockError(f"{field} must be privacy-safe")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-"
    if len(normalized) > 128 or any(
        character not in allowed for character in normalized
    ):
        raise PaidUnlockError(f"{field} must be a safe label")
    return normalized


def _safe_ref(value: str) -> str:
    ref = value.strip().replace("\\", "/")
    if not ref or ref.startswith("/") or ".." in Path(ref).parts:
        raise PaidUnlockError("delivered ref must be safe")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/-"
    if len(ref) > 160 or any(character not in allowed for character in ref):
        raise PaidUnlockError("delivered ref must be safe")
    return ref
