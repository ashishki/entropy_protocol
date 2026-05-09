from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

REDACTED_VALUE = "<redacted>"
APPROVED_READ_ONLY = "approved_read_only"
REJECTED_WRITE_SCOPE = "rejected_write_scope"
NEEDS_OPERATOR_REVIEW = "needs_operator_review"

_WRITE_PERMISSION_FRAGMENTS = (
    "accountmutation",
    "accounttransfer",
    "cancelorder",
    "leverage",
    "margin",
    "orderwrite",
    "placeorder",
    "submembertransfer",
    "tradewrite",
    "transfer",
    "withdraw",
)


@dataclass(frozen=True, repr=False)
class ExchangeCredentials:
    exchange: str
    api_key: str
    api_secret: str
    passphrase: str | None = None
    account_id: str | None = None

    def __post_init__(self) -> None:
        _require_non_blank(self.exchange, field="exchange")
        _require_non_blank(self.api_key, field="api_key")
        _require_non_blank(self.api_secret, field="api_secret")
        if self.passphrase is not None:
            _require_non_blank(self.passphrase, field="passphrase")
        if self.account_id is not None:
            _require_non_blank(self.account_id, field="account_id")

    def __repr__(self) -> str:
        metadata = self.to_safe_metadata()
        return f"ExchangeCredentials({json.dumps(metadata, sort_keys=True)})"

    def to_safe_metadata(self) -> dict[str, str]:
        metadata = {
            "exchange": self.exchange,
            "api_key": REDACTED_VALUE,
            "api_key_fingerprint": _fingerprint(self.api_key),
            "api_secret": REDACTED_VALUE,
        }
        if self.passphrase is not None:
            metadata["passphrase"] = REDACTED_VALUE
        if self.account_id is not None:
            metadata["account_id"] = REDACTED_VALUE
            metadata["account_id_fingerprint"] = _fingerprint(self.account_id)
        return metadata


@dataclass(frozen=True)
class PermissionReview:
    exchange: str
    status: str
    read_only: bool | None
    rejected_permissions: tuple[str, ...]
    reason: str

    def to_safe_metadata(self) -> dict[str, object]:
        return asdict(self)


def inspect_exchange_permissions(
    *,
    exchange: str,
    read_only: bool | int | str | None,
    permissions: Mapping[str, object] | None = None,
) -> PermissionReview:
    normalized_exchange = _require_non_blank(exchange, field="exchange")
    normalized_read_only = _normalize_read_only(read_only)
    rejected_permissions = _detect_write_permissions(permissions or {})

    if normalized_read_only is False:
        return PermissionReview(
            exchange=normalized_exchange,
            status=REJECTED_WRITE_SCOPE,
            read_only=False,
            rejected_permissions=rejected_permissions,
            reason="exchange reports the key is not read-only",
        )

    if rejected_permissions:
        return PermissionReview(
            exchange=normalized_exchange,
            status=REJECTED_WRITE_SCOPE,
            read_only=normalized_read_only,
            rejected_permissions=rejected_permissions,
            reason="exchange metadata contains write/control permissions",
        )

    if normalized_read_only is None:
        return PermissionReview(
            exchange=normalized_exchange,
            status=NEEDS_OPERATOR_REVIEW,
            read_only=None,
            rejected_permissions=(),
            reason="read-only permission could not be verified",
        )

    return PermissionReview(
        exchange=normalized_exchange,
        status=APPROVED_READ_ONLY,
        read_only=True,
        rejected_permissions=(),
        reason="exchange metadata verifies read-only access",
    )


def inspect_bybit_api_key_metadata(
    metadata: Mapping[str, Any],
) -> PermissionReview:
    result = metadata.get("result", metadata)
    if not isinstance(result, Mapping):
        return inspect_exchange_permissions(
            exchange="bybit",
            read_only=None,
            permissions=None,
        )
    permissions = result.get("permissions")
    return inspect_exchange_permissions(
        exchange="bybit",
        read_only=result.get("readOnly"),
        permissions=permissions if isinstance(permissions, Mapping) else None,
    )


def build_exchange_import_safe_metadata(
    *,
    credentials: ExchangeCredentials,
    permission_review: PermissionReview,
) -> dict[str, object]:
    return {
        "credentials": credentials.to_safe_metadata(),
        "permission_review": permission_review.to_safe_metadata(),
    }


def _normalize_read_only(value: bool | int | str | None) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value == 1:
            return True
        if value == 0:
            return False
        return None
    normalized = str(value).strip().casefold()
    if normalized in {"1", "true", "yes", "read_only", "readonly"}:
        return True
    if normalized in {"0", "false", "no", "read_write", "readwrite"}:
        return False
    return None


def _detect_write_permissions(permissions: Mapping[str, object]) -> tuple[str, ...]:
    detected: list[str] = []
    for group, values in sorted(permissions.items()):
        if _is_write_permission(group):
            detected.append(f"{group}:<enabled>")
        for value in _iter_permission_values(values):
            token = _permission_token(value)
            if _is_write_permission(token):
                detected.append(f"{group}:{value}")
    return tuple(detected)


def _iter_permission_values(values: object) -> tuple[str, ...]:
    if isinstance(values, str):
        return (values,)
    if isinstance(values, Mapping):
        nested_values: list[str] = []
        for nested_group, nested_value in values.items():
            nested_values.append(str(nested_group))
            nested_values.extend(_iter_permission_values(nested_value))
        return tuple(nested_values)
    try:
        iterator = iter(values)  # type: ignore[arg-type]
    except TypeError:
        return (str(values),)
    return tuple(str(item) for item in iterator)


def _is_write_permission(value: str) -> bool:
    token = _permission_token(value)
    return any(fragment in token for fragment in _WRITE_PERMISSION_FRAGMENTS)


def _permission_token(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def _fingerprint(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return f"sha256:{digest[:12]}"


def _require_non_blank(value: str, *, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} must not be blank")
    return text
