from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

QUEUE_STATUSES = (
    "received",
    "needs_policy_mapping",
    "needs_user_clarification",
    "ready_to_run",
    "processing",
    "ready_for_review",
    "delivered",
    "rejected",
)


class PilotQueueError(ValueError):
    pass


@dataclass(frozen=True)
class PilotQueueRequest:
    audit_id: str
    status: str
    created_at: str
    file_references: dict[str, str]
    rejection_reason: str | None = None


class PilotQueue:
    def __init__(self, queue_file: str | Path) -> None:
        self._queue_file = Path(queue_file)

    def upsert_request(
        self,
        audit_id: str,
        *,
        status: str = "received",
        file_references: dict[str, str | Path] | None = None,
        created_at: datetime | None = None,
    ) -> PilotQueueRequest:
        _validate_status(status)
        requests = self._load()
        request = PilotQueueRequest(
            audit_id=_safe_single_line(audit_id, field="audit_id"),
            status=status,
            created_at=(created_at or datetime.now(UTC)).astimezone(UTC).isoformat(),
            file_references={
                _safe_single_line(label, field="file reference label"): _safe_file_ref(
                    value
                )
                for label, value in sorted((file_references or {}).items())
            },
        )
        requests[request.audit_id] = request
        self._save(requests)
        return request

    def list_requests(self) -> tuple[PilotQueueRequest, ...]:
        return tuple(
            sorted(
                self._load().values(),
                key=lambda item: (item.created_at, item.audit_id),
            )
        )

    def get_request(self, audit_id: str) -> PilotQueueRequest:
        requests = self._load()
        try:
            return requests[audit_id]
        except KeyError as exc:
            raise PilotQueueError(f"audit request not found: {audit_id}") from exc

    def set_status(self, audit_id: str, status: str) -> PilotQueueRequest:
        _validate_status(status)
        requests = self._load()
        request = self.get_request(audit_id)
        updated = PilotQueueRequest(
            audit_id=request.audit_id,
            status=status,
            created_at=request.created_at,
            file_references=request.file_references,
            rejection_reason=request.rejection_reason,
        )
        requests[audit_id] = updated
        self._save(requests)
        return updated

    def reject(self, audit_id: str, reason: str) -> PilotQueueRequest:
        requests = self._load()
        request = self.get_request(audit_id)
        updated = PilotQueueRequest(
            audit_id=request.audit_id,
            status="rejected",
            created_at=request.created_at,
            file_references=request.file_references,
            rejection_reason=_safe_reason(reason),
        )
        requests[audit_id] = updated
        self._save(requests)
        return updated

    def _load(self) -> dict[str, PilotQueueRequest]:
        if not self._queue_file.exists():
            return {}
        payload = json.loads(self._queue_file.read_text(encoding="utf-8"))
        return {
            audit_id: PilotQueueRequest(
                audit_id=audit_id,
                status=str(item["status"]),
                created_at=str(item["created_at"]),
                file_references={
                    str(label): str(value)
                    for label, value in item.get("file_references", {}).items()
                },
                rejection_reason=item.get("rejection_reason"),
            )
            for audit_id, item in payload.get("requests", {}).items()
        }

    def _save(self, requests: dict[str, PilotQueueRequest]) -> None:
        self._queue_file.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "requests": {
                audit_id: asdict(request)
                for audit_id, request in sorted(requests.items())
            }
        }
        self._queue_file.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )


def format_queue_list(requests: tuple[PilotQueueRequest, ...]) -> str:
    if not requests:
        return "No pilot requests.\n"
    lines = ["Audit ID | Status | Created At"]
    lines.extend(
        f"{request.audit_id} | {request.status} | {request.created_at}"
        for request in requests
    )
    return "\n".join(lines) + "\n"


def format_queue_request(request: PilotQueueRequest) -> str:
    lines = [
        f"Audit ID: {request.audit_id}",
        f"Status: {request.status}",
        f"Created At: {request.created_at}",
        "File References:",
    ]
    if request.file_references:
        lines.extend(
            f"- {label}: {value}"
            for label, value in sorted(request.file_references.items())
        )
    else:
        lines.append("- none")
    if request.rejection_reason:
        lines.append(f"Rejection Reason: {request.rejection_reason}")
    return "\n".join(lines) + "\n"


def _validate_status(status: str) -> None:
    if status not in QUEUE_STATUSES:
        raise PilotQueueError(f"unsupported queue status: {status}")


def _safe_file_ref(value: str | Path) -> str:
    text = _safe_single_line(str(value), field="file reference")
    if Path(text).is_absolute():
        return Path(text).name
    return text


def _safe_reason(reason: str) -> str:
    text = _safe_single_line(reason, field="rejection reason")
    forbidden_fragments = (
        "timestamp,symbol",
        "side,quantity,price",
        "\t",
        "api_key",
        "password",
        "bearer ",
    )
    lowered = text.casefold()
    if any(fragment in lowered for fragment in forbidden_fragments):
        raise PilotQueueError("rejection reason must be non-sensitive")
    return text


def _safe_single_line(value: str, *, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise PilotQueueError(f"{field} must not be blank")
    if "\n" in text or "\r" in text:
        raise PilotQueueError(f"{field} must be a single line")
    return text
