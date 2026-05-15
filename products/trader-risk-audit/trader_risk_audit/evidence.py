from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

PILOT_CUSTOMER_LOG_FIELDS = (
    "prospect_source",
    "icp",
    "call_date",
    "intake_method",
    "export_provided",
    "rules_provided",
    "paid_amount",
    "objections",
    "api_setup_objections",
    "report_delivered",
    "repeat_requested",
    "referral",
)
PREVIEW_EVENT_FIELDS = (
    "event_type",
    "timestamp",
    "intake_id",
    "source_type",
    "objection_tags",
)
HYPOTHESIS_FUNNEL_EVENT_FIELDS = (
    "event_type",
    "timestamp",
    "intake_id",
    "source_type",
    "evidence_source",
    "tags",
)
HYPOTHESIS_EXPORT_FIELDS = ("metric", "value")
DEMO_SOURCES = frozenset({"public_sample_demo", "internal_demo", "demo_artifact"})
INTAKE_METHODS = frozenset(
    {"csv_export", "bybit_read_only_api", "binance_read_only_api"}
)
MARKET_EVIDENCE_SOURCES = frozenset({"market", "customer", "paid_pilot"})
PREVIEW_EVENT_TYPES = frozenset(
    {
        "preview_generated",
        "preview_opened",
        "cta_shown",
        "cta_accepted",
        "cta_requested",
        "objection_recorded",
    }
)
PREVIEW_SOURCE_TYPES = INTAKE_METHODS | DEMO_SOURCES
HYPOTHESIS_FUNNEL_EVENT_TYPES = frozenset(
    {
        "prospect_qualified",
        "intake_started",
        "valid_export",
        "policy_built",
        "audit_run",
        "preview_generated",
        "cta_accepted",
        "paid_report",
        "repeat_commitment",
        "referral",
    }
)
HYPOTHESIS_FUNNEL_SOURCE_TYPES = PREVIEW_SOURCE_TYPES
HYPOTHESIS_EVIDENCE_SOURCES = MARKET_EVIDENCE_SOURCES | DEMO_SOURCES
EXCHANGE_INTAKE_METHODS = frozenset({"bybit_read_only_api", "binance_read_only_api"})
_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_HANDLE_PATTERN = re.compile(r"@[A-Za-z][A-Za-z0-9_]{4,}")
_LONG_NUMBER_PATTERN = re.compile(r"\b\d{6,}\b")
_ACCOUNT_ID_PATTERN = re.compile(r"\b(?:account|acct)[-_ ]?\d{4,}\b", re.I)
_PHONE_PATTERN = re.compile(r"(?:\+?\d[\s().-]*){10,}")


class EvidenceValidationError(ValueError):
    pass


@dataclass(frozen=True)
class EvidenceRow:
    prospect_source: str
    icp: str
    call_date: str
    export_provided: bool
    rules_provided: bool
    paid_amount: str
    objections: str
    report_delivered: bool
    repeat_requested: bool
    referral: bool
    intake_method: str = "csv_export"
    api_setup_objections: str = "none"

    def to_csv_row(self) -> dict[str, str]:
        _validate_safe_fields(asdict(self))
        intake_method = _validate_intake_method(self.intake_method)
        return {
            "prospect_source": self.prospect_source,
            "icp": self.icp,
            "call_date": self.call_date,
            "intake_method": intake_method,
            "export_provided": _yes_no(self.export_provided),
            "rules_provided": _yes_no(self.rules_provided),
            "paid_amount": self.paid_amount,
            "objections": self.objections,
            "api_setup_objections": self.api_setup_objections,
            "report_delivered": _yes_no(self.report_delivered),
            "repeat_requested": _yes_no(self.repeat_requested),
            "referral": _yes_no(self.referral),
        }


@dataclass(frozen=True)
class PreviewEvent:
    event_type: str
    timestamp: str
    intake_id: str
    source_type: str
    objection_tags: tuple[str, ...] = ()

    def to_csv_row(self) -> dict[str, str]:
        event_type = _validate_preview_event_type(self.event_type)
        source_type = _validate_preview_source_type(self.source_type)
        payload = {
            "event_type": event_type,
            "timestamp": self.timestamp,
            "intake_id": self.intake_id,
            "source_type": source_type,
            "objection_tags": ",".join(_safe_tag(tag) for tag in self.objection_tags),
        }
        _validate_safe_fields(payload)
        return payload


@dataclass(frozen=True)
class HypothesisFunnelEvent:
    event_type: str
    timestamp: str
    intake_id: str
    source_type: str
    evidence_source: str = "market"
    tags: tuple[str, ...] = ()

    def to_csv_row(self) -> dict[str, str]:
        event_type = _validate_hypothesis_funnel_event_type(self.event_type)
        source_type = _validate_hypothesis_funnel_source_type(self.source_type)
        evidence_source = _validate_hypothesis_evidence_source(self.evidence_source)
        payload = {
            "event_type": event_type,
            "timestamp": self.timestamp,
            "intake_id": self.intake_id,
            "source_type": source_type,
            "evidence_source": evidence_source,
            "tags": ",".join(_safe_tag(tag) for tag in self.tags),
        }
        _validate_safe_fields(payload)
        return payload


@dataclass(frozen=True)
class HypothesisEvidenceDataset:
    legacy_rows: tuple[EvidenceRow, ...]
    funnel_events: tuple[HypothesisFunnelEvent, ...]


@dataclass(frozen=True)
class HypothesisDashboardSummary:
    qualified_prospects: int
    intake_started: int
    valid_exports: int
    policy_built: int
    audit_run: int
    preview_generated: int
    cta_accepted: int
    paid_reports: int
    repeat_commitments: int
    referrals: int
    demo_artifact_events: int
    objection_tags: tuple[tuple[str, int], ...]
    blocker_tags: tuple[tuple[str, int], ...]
    gate_status: str
    next_action: str

    def format(self) -> str:
        valid_export_ratio = _ratio(self.valid_exports, self.qualified_prospects)
        cta_accept_ratio = _ratio(self.cta_accepted, self.preview_generated)
        paid_report_ratio = _ratio(self.paid_reports, self.qualified_prospects)
        return "\n".join(
            (
                "Hypothesis Evidence Dashboard",
                f"Qualified prospects: {self.qualified_prospects}",
                f"Intake started: {self.intake_started}",
                f"Valid exports/rules: {self.valid_exports}",
                f"Policy built: {self.policy_built}",
                f"Audit run: {self.audit_run}",
                f"Preview generated: {self.preview_generated}",
                f"CTA accepted: {self.cta_accepted}",
                f"Paid reports: {self.paid_reports}",
                f"Repeat commitments: {self.repeat_commitments}",
                f"Referrals: {self.referrals}",
                f"Demo/artifact events: {self.demo_artifact_events}",
                f"Valid export ratio: {valid_export_ratio}",
                f"CTA accept ratio: {cta_accept_ratio}",
                f"Paid report ratio: {paid_report_ratio}",
                f"Gate status: {self.gate_status}",
                f"Objection tags: {_format_counts(self.objection_tags)}",
                f"Unsupported/blocker tags: {_format_counts(self.blocker_tags)}",
                f"Next action: {self.next_action}",
            )
        )


@dataclass(frozen=True)
class HypothesisGateDecision:
    status: str
    reasons: tuple[str, ...]
    next_action: str

    def format(self) -> str:
        return "\n".join(
            (
                "Hypothesis Gate Decision",
                f"Status: {self.status}",
                f"Reasons: {'; '.join(self.reasons) if self.reasons else 'none'}",
                f"Next action: {self.next_action}",
            )
        )


@dataclass(frozen=True)
class HypothesisEvidenceExport:
    csv_path: Path
    markdown_path: Path
    source_provenance: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ValidationGateSummary:
    qualified_prospects: int
    exports_and_rules: int
    paid_audits: int
    repeat_commitments: int
    referrals: int
    csv_pilots: int
    exchange_import_pilots: int

    def format(self) -> str:
        return "\n".join(
            (
                "Validation Gate Summary",
                f"Qualified prospects: {self.qualified_prospects}/10",
                f"Exports and rules: {self.exports_and_rules}/5",
                f"Paid audits: {self.paid_audits}/3",
                f"Repeat commitments: {self.repeat_commitments}/2",
                f"Referrals: {self.referrals}",
                f"CSV pilots: {self.csv_pilots}",
                f"Exchange import pilots: {self.exchange_import_pilots}",
            )
        )


@dataclass(frozen=True)
class PreviewEventSummary:
    total_events: int
    preview_generated: int
    cta_shown: int
    cta_accepted_market: int
    cta_requested_market: int
    objections: int

    def format(self) -> str:
        return "\n".join(
            (
                "Preview Event Summary",
                f"Total events: {self.total_events}",
                f"Preview generated: {self.preview_generated}",
                f"CTA shown: {self.cta_shown}",
                f"CTA accepted market: {self.cta_accepted_market}",
                f"CTA requested market: {self.cta_requested_market}",
                f"Objections: {self.objections}",
            )
        )


def append_customer_log_row(path: str | Path, row: EvidenceRow) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as log_file:
        writer = csv.DictWriter(log_file, fieldnames=PILOT_CUSTOMER_LOG_FIELDS)
        if not exists or log_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(row.to_csv_row())


def append_preview_event(path: str | Path, event: PreviewEvent) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as log_file:
        writer = csv.DictWriter(log_file, fieldnames=PREVIEW_EVENT_FIELDS)
        if not exists or log_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(event.to_csv_row())


def append_hypothesis_funnel_event(
    path: str | Path,
    event: HypothesisFunnelEvent,
) -> None:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    exists = log_path.exists()
    with log_path.open("a", newline="", encoding="utf-8") as log_file:
        writer = csv.DictWriter(log_file, fieldnames=HYPOTHESIS_FUNNEL_EVENT_FIELDS)
        if not exists or log_path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(event.to_csv_row())


def load_customer_log(path: str | Path) -> tuple[EvidenceRow, ...]:
    log_path = Path(path)
    if not log_path.exists():
        return ()
    with log_path.open(newline="", encoding="utf-8") as log_file:
        return tuple(_row_from_mapping(row) for row in csv.DictReader(log_file))


def load_preview_events(path: str | Path) -> tuple[PreviewEvent, ...]:
    log_path = Path(path)
    if not log_path.exists():
        return ()
    with log_path.open(newline="", encoding="utf-8") as log_file:
        return tuple(
            _preview_event_from_mapping(row) for row in csv.DictReader(log_file)
        )


def load_hypothesis_funnel_events(
    path: str | Path,
) -> tuple[HypothesisFunnelEvent, ...]:
    log_path = Path(path)
    if not log_path.exists():
        return ()
    with log_path.open(newline="", encoding="utf-8") as log_file:
        return tuple(
            _hypothesis_funnel_event_from_mapping(row)
            for row in csv.DictReader(log_file)
        )


def load_hypothesis_evidence(
    *,
    customer_log_path: str | Path | None = None,
    funnel_event_path: str | Path | None = None,
) -> HypothesisEvidenceDataset:
    return HypothesisEvidenceDataset(
        legacy_rows=load_customer_log(customer_log_path) if customer_log_path else (),
        funnel_events=(
            load_hypothesis_funnel_events(funnel_event_path)
            if funnel_event_path
            else ()
        ),
    )


def summarize_validation_gate(rows: tuple[EvidenceRow, ...]) -> ValidationGateSummary:
    market_rows = tuple(row for row in rows if not is_demo_evidence(row))
    return ValidationGateSummary(
        qualified_prospects=len(market_rows),
        exports_and_rules=sum(
            1 for row in market_rows if row.export_provided and row.rules_provided
        ),
        paid_audits=sum(
            1
            for row in market_rows
            if _paid_amount(row.paid_amount) > Decimal("0") and row.report_delivered
        ),
        repeat_commitments=sum(1 for row in market_rows if row.repeat_requested),
        referrals=sum(1 for row in market_rows if row.referral),
        csv_pilots=sum(
            1
            for row in market_rows
            if _validate_intake_method(row.intake_method) == "csv_export"
        ),
        exchange_import_pilots=sum(
            1
            for row in market_rows
            if _validate_intake_method(row.intake_method) in EXCHANGE_INTAKE_METHODS
        ),
    )


def summarize_preview_events(events: tuple[PreviewEvent, ...]) -> PreviewEventSummary:
    market_events = tuple(event for event in events if not is_demo_preview_event(event))
    return PreviewEventSummary(
        total_events=len(events),
        preview_generated=sum(
            1 for event in market_events if event.event_type == "preview_generated"
        ),
        cta_shown=sum(1 for event in market_events if event.event_type == "cta_shown"),
        cta_accepted_market=sum(
            1 for event in market_events if event.event_type == "cta_accepted"
        ),
        cta_requested_market=sum(
            1 for event in market_events if event.event_type == "cta_requested"
        ),
        objections=sum(
            1 for event in market_events if event.event_type == "objection_recorded"
        ),
    )


def summarize_hypothesis_dashboard(
    dataset: HypothesisEvidenceDataset,
) -> HypothesisDashboardSummary:
    market_rows = tuple(row for row in dataset.legacy_rows if not is_demo_evidence(row))
    market_events = tuple(
        event for event in dataset.funnel_events if not is_demo_hypothesis_event(event)
    )
    demo_artifact_events = (
        len(dataset.legacy_rows)
        - len(market_rows)
        + len(dataset.funnel_events)
        - len(market_events)
    )
    counts = {event_type: 0 for event_type in HYPOTHESIS_FUNNEL_EVENT_TYPES}
    tag_counts: dict[str, int] = {}
    blocker_counts: dict[str, int] = {}
    for event in market_events:
        counts[event.event_type] += 1
        for tag in event.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
            if _is_blocker_tag(tag):
                blocker_counts[tag] = blocker_counts.get(tag, 0) + 1
    for row in market_rows:
        tag = _safe_tag(row.objections or "none")
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
        if _is_blocker_tag(tag):
            blocker_counts[tag] = blocker_counts.get(tag, 0) + 1
        api_tag = _safe_tag(row.api_setup_objections or "none")
        if api_tag != "none":
            tag_counts[api_tag] = tag_counts.get(api_tag, 0) + 1
            if _is_blocker_tag(api_tag):
                blocker_counts[api_tag] = blocker_counts.get(api_tag, 0) + 1

    qualified_prospects = len(market_rows) + counts["prospect_qualified"]
    valid_exports = (
        sum(1 for row in market_rows if row.export_provided and row.rules_provided)
        + counts["valid_export"]
    )
    paid_reports = (
        sum(
            1
            for row in market_rows
            if _paid_amount(row.paid_amount) > Decimal("0") and row.report_delivered
        )
        + counts["paid_report"]
    )
    repeat_commitments = (
        sum(1 for row in market_rows if row.repeat_requested)
        + counts["repeat_commitment"]
    )
    referrals = sum(1 for row in market_rows if row.referral) + counts["referral"]
    gate_status, next_action = _dashboard_gate_status(
        qualified_prospects=qualified_prospects,
        valid_exports=valid_exports,
        paid_reports=paid_reports,
        repeat_commitments=repeat_commitments,
        referrals=referrals,
    )
    return HypothesisDashboardSummary(
        qualified_prospects=qualified_prospects,
        intake_started=counts["intake_started"],
        valid_exports=valid_exports,
        policy_built=counts["policy_built"],
        audit_run=counts["audit_run"],
        preview_generated=counts["preview_generated"],
        cta_accepted=counts["cta_accepted"],
        paid_reports=paid_reports,
        repeat_commitments=repeat_commitments,
        referrals=referrals,
        demo_artifact_events=demo_artifact_events,
        objection_tags=_sorted_counts(tag_counts),
        blocker_tags=_sorted_counts(blocker_counts),
        gate_status=gate_status,
        next_action=next_action,
    )


def evaluate_hypothesis_gate(
    summary: HypothesisDashboardSummary,
) -> HypothesisGateDecision:
    missing: list[str] = []
    if summary.qualified_prospects < 10:
        missing.append(f"qualified prospects {summary.qualified_prospects}/10")
    if summary.valid_exports < 5:
        missing.append(f"valid exports/rules {summary.valid_exports}/5")
    if summary.paid_reports < 3:
        missing.append(f"paid reports {summary.paid_reports}/3")
    repeat_or_referral = summary.repeat_commitments + summary.referrals
    if repeat_or_referral < 2:
        missing.append(f"repeat/referral signals {repeat_or_referral}/2")

    blocker_total = sum(count for _, count in summary.blocker_tags)
    if blocker_total >= 5 and summary.paid_reports == 0:
        return HypothesisGateDecision(
            status="pivot",
            reasons=(
                f"blocking objections dominate with {blocker_total} blocker signals",
                "no paid reports recorded",
            ),
            next_action=(
                "pause feature work and rework offer, ICP, or intake before T93"
            ),
        )
    if not missing:
        return HypothesisGateDecision(
            status="proceed",
            reasons=("paid, repeat, and referral thresholds met with market evidence",),
            next_action="prepare T93 evidence decision review",
        )
    return HypothesisGateDecision(
        status="needs_more_evidence",
        reasons=tuple(missing),
        next_action=_next_action_for_missing(missing),
    )


def export_hypothesis_evidence(
    *,
    output_dir: str | Path,
    customer_log_path: str | Path | None = None,
    funnel_event_path: str | Path | None = None,
) -> HypothesisEvidenceExport:
    dataset = load_hypothesis_evidence(
        customer_log_path=customer_log_path,
        funnel_event_path=funnel_event_path,
    )
    summary = summarize_hypothesis_dashboard(dataset)
    decision = evaluate_hypothesis_gate(summary)
    provenance = _source_provenance(
        customer_log_path=customer_log_path,
        funnel_event_path=funnel_event_path,
    )
    rows = _hypothesis_export_rows(summary, decision, provenance)
    report = _render_hypothesis_export_markdown(summary, decision, provenance)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    csv_path = output_path / "hypothesis_evidence_summary.csv"
    markdown_path = output_path / "hypothesis_evidence_summary.md"
    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=HYPOTHESIS_EXPORT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    markdown_path.write_text(report, encoding="utf-8")
    ensure_evidence_export_safe(csv_path.read_text(encoding="utf-8"))
    ensure_evidence_export_safe(report)
    return HypothesisEvidenceExport(
        csv_path=csv_path,
        markdown_path=markdown_path,
        source_provenance=provenance,
    )


def ensure_evidence_export_safe(text: str) -> None:
    for index, line in enumerate(text.splitlines(), start=1):
        _validate_safe_fields({f"evidence_export_line_{index}": line})
    if _PHONE_PATTERN.search(text):
        raise EvidenceValidationError("evidence_export must not contain phone numbers")


def is_demo_evidence(row: EvidenceRow) -> bool:
    return row.prospect_source.strip().casefold() in DEMO_SOURCES


def is_demo_preview_event(event: PreviewEvent) -> bool:
    return event.source_type.strip().casefold() in DEMO_SOURCES


def is_demo_hypothesis_event(event: HypothesisFunnelEvent) -> bool:
    return (
        event.source_type.strip().casefold() in DEMO_SOURCES
        or event.evidence_source.strip().casefold() in DEMO_SOURCES
    )


def _row_from_mapping(row: dict[str, str]) -> EvidenceRow:
    return EvidenceRow(
        prospect_source=row["prospect_source"],
        icp=row["icp"],
        call_date=row["call_date"],
        export_provided=_bool(row["export_provided"]),
        rules_provided=_bool(row["rules_provided"]),
        paid_amount=row["paid_amount"],
        objections=row["objections"],
        report_delivered=_bool(row["report_delivered"]),
        repeat_requested=_bool(row["repeat_requested"]),
        referral=_bool(row["referral"]),
        intake_method=_validate_intake_method(row.get("intake_method", "csv_export")),
        api_setup_objections=row.get("api_setup_objections", "none"),
    )


def _preview_event_from_mapping(row: dict[str, str]) -> PreviewEvent:
    tags = tuple(
        _safe_tag(tag)
        for tag in row.get("objection_tags", "").split(",")
        if tag.strip()
    )
    return PreviewEvent(
        event_type=_validate_preview_event_type(row["event_type"]),
        timestamp=row["timestamp"],
        intake_id=row["intake_id"],
        source_type=_validate_preview_source_type(row["source_type"]),
        objection_tags=tags,
    )


def _hypothesis_funnel_event_from_mapping(
    row: dict[str, str],
) -> HypothesisFunnelEvent:
    tags = tuple(
        _safe_tag(tag) for tag in row.get("tags", "").split(",") if tag.strip()
    )
    return HypothesisFunnelEvent(
        event_type=_validate_hypothesis_funnel_event_type(row["event_type"]),
        timestamp=row["timestamp"],
        intake_id=row["intake_id"],
        source_type=_validate_hypothesis_funnel_source_type(row["source_type"]),
        evidence_source=_validate_hypothesis_evidence_source(
            row.get("evidence_source", "market")
        ),
        tags=tags,
    )


def _validate_safe_fields(payload: dict[str, object]) -> None:
    for field, value in payload.items():
        text = str(value)
        lowered = text.casefold()
        if "\n" in text or "\r" in text:
            raise EvidenceValidationError(f"{field} must be a single line")
        if _EMAIL_PATTERN.search(text) or _HANDLE_PATTERN.search(text):
            raise EvidenceValidationError(f"{field} must not contain identifiers")
        if _LONG_NUMBER_PATTERN.search(text) or _ACCOUNT_ID_PATTERN.search(text):
            raise EvidenceValidationError(f"{field} must not contain account numbers")
        if (
            "timestamp,symbol" in lowered
            or "api_key" in lowered
            or "api_secret" in lowered
            or "password" in lowered
            or "secret key" in lowered
            or "seed phrase" in lowered
            or "private key" in lowered
            or "raw_trade" in lowered
            or "raw trade" in lowered
            or "source_row" in lowered
            or "payment_id" in lowered
            or "transaction_id" in lowered
            or "stripe" in lowered
            or "checkout" in lowered
        ):
            raise EvidenceValidationError(f"{field} must be non-sensitive")


def _validate_intake_method(value: str) -> str:
    intake_method = value.strip().casefold()
    if intake_method not in INTAKE_METHODS:
        supported = ", ".join(sorted(INTAKE_METHODS))
        raise EvidenceValidationError(f"intake_method must be one of: {supported}")
    return intake_method


def _validate_preview_event_type(value: str) -> str:
    event_type = value.strip().casefold()
    if event_type not in PREVIEW_EVENT_TYPES:
        supported = ", ".join(sorted(PREVIEW_EVENT_TYPES))
        raise EvidenceValidationError(f"event_type must be one of: {supported}")
    return event_type


def _validate_preview_source_type(value: str) -> str:
    source_type = value.strip().casefold()
    if source_type not in PREVIEW_SOURCE_TYPES:
        supported = ", ".join(sorted(PREVIEW_SOURCE_TYPES))
        raise EvidenceValidationError(f"source_type must be one of: {supported}")
    return source_type


def _validate_hypothesis_funnel_event_type(value: str) -> str:
    event_type = value.strip().casefold()
    if event_type not in HYPOTHESIS_FUNNEL_EVENT_TYPES:
        supported = ", ".join(sorted(HYPOTHESIS_FUNNEL_EVENT_TYPES))
        raise EvidenceValidationError(f"event_type must be one of: {supported}")
    return event_type


def _validate_hypothesis_funnel_source_type(value: str) -> str:
    source_type = value.strip().casefold()
    if source_type not in HYPOTHESIS_FUNNEL_SOURCE_TYPES:
        supported = ", ".join(sorted(HYPOTHESIS_FUNNEL_SOURCE_TYPES))
        raise EvidenceValidationError(f"source_type must be one of: {supported}")
    return source_type


def _validate_hypothesis_evidence_source(value: str) -> str:
    evidence_source = value.strip().casefold()
    if evidence_source not in HYPOTHESIS_EVIDENCE_SOURCES:
        supported = ", ".join(sorted(HYPOTHESIS_EVIDENCE_SOURCES))
        raise EvidenceValidationError(f"evidence_source must be one of: {supported}")
    return evidence_source


def _safe_tag(value: str) -> str:
    tag = value.strip().casefold().replace(" ", "_")
    if not tag:
        raise EvidenceValidationError("objection tag must not be empty")
    if len(tag) > 40 or not all(
        character.isalnum() or character in {"_", "-"} for character in tag
    ):
        raise EvidenceValidationError("objection tag must be safe")
    _validate_safe_fields({"objection_tag": tag})
    return tag


def _is_blocker_tag(tag: str) -> bool:
    return any(
        marker in tag
        for marker in (
            "unsupported",
            "missing",
            "blocker",
            "cannot",
            "no_export",
            "api_setup",
            "wants_live",
        )
    )


def _sorted_counts(counts: dict[str, int]) -> tuple[tuple[str, int], ...]:
    return tuple(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def _format_counts(counts: tuple[tuple[str, int], ...]) -> str:
    if not counts:
        return "none"
    return ", ".join(f"{tag}={count}" for tag, count in counts)


def _ratio(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "0/0 (0%)"
    percent = round((numerator / denominator) * 100)
    return f"{numerator}/{denominator} ({percent}%)"


def _dashboard_gate_status(
    *,
    qualified_prospects: int,
    valid_exports: int,
    paid_reports: int,
    repeat_commitments: int,
    referrals: int,
) -> tuple[str, str]:
    repeat_or_referral = repeat_commitments + referrals
    if (
        qualified_prospects >= 10
        and valid_exports >= 5
        and paid_reports >= 3
        and repeat_or_referral >= 2
    ):
        return "ready_for_decision", "prepare T93 evidence decision review"
    if qualified_prospects < 10:
        return "needs_more_evidence", "qualify more market prospects"
    if valid_exports < 5:
        return "needs_more_evidence", "collect valid exports and written rules"
    if paid_reports < 3:
        return "needs_more_evidence", "convert previews into paid manual reports"
    return "needs_more_evidence", "secure repeat commitments or referrals"


def _next_action_for_missing(missing: list[str]) -> str:
    joined = " ".join(missing)
    if "qualified prospects" in joined:
        return "qualify more market prospects"
    if "valid exports/rules" in joined:
        return "collect valid exports and written rules"
    if "paid reports" in joined:
        return "convert previews into paid manual reports"
    return "secure repeat commitments or referrals"


def _hypothesis_export_rows(
    summary: HypothesisDashboardSummary,
    decision: HypothesisGateDecision,
    provenance: tuple[tuple[str, str], ...],
) -> tuple[dict[str, str], ...]:
    rows = [
        ("qualified_prospects", str(summary.qualified_prospects)),
        ("intake_started", str(summary.intake_started)),
        ("valid_exports_rules", str(summary.valid_exports)),
        ("policy_built", str(summary.policy_built)),
        ("audit_run", str(summary.audit_run)),
        ("preview_generated", str(summary.preview_generated)),
        ("cta_accepted", str(summary.cta_accepted)),
        ("paid_reports", str(summary.paid_reports)),
        ("repeat_commitments", str(summary.repeat_commitments)),
        ("referrals", str(summary.referrals)),
        ("demo_artifact_events", str(summary.demo_artifact_events)),
        ("gate_verdict", decision.status),
        ("gate_reasons", " | ".join(decision.reasons)),
        ("next_action", decision.next_action),
        ("objection_tags", _format_counts(summary.objection_tags)),
        ("unsupported_blocker_tags", _format_counts(summary.blocker_tags)),
        *provenance,
    ]
    return tuple({"metric": metric, "value": value} for metric, value in rows)


def _render_hypothesis_export_markdown(
    summary: HypothesisDashboardSummary,
    decision: HypothesisGateDecision,
    provenance: tuple[tuple[str, str], ...],
) -> str:
    provenance_lines = "\n".join(
        f"- `{metric}`: `{value}`" for metric, value in provenance
    )
    return "\n".join(
        (
            "# Hypothesis Evidence Summary",
            "",
            "## Dashboard",
            "",
            summary.format(),
            "",
            "## Gate Decision",
            "",
            decision.format(),
            "",
            "## Provenance",
            "",
            provenance_lines,
            "",
        )
    )


def _source_provenance(
    *,
    customer_log_path: str | Path | None,
    funnel_event_path: str | Path | None,
) -> tuple[tuple[str, str], ...]:
    return (
        ("customer_log_name", _safe_source_name(customer_log_path)),
        ("customer_log_sha256", _safe_file_sha256(customer_log_path)),
        ("funnel_event_log_name", _safe_source_name(funnel_event_path)),
        ("funnel_event_log_sha256", _safe_file_sha256(funnel_event_path)),
    )


def _safe_source_name(path: str | Path | None) -> str:
    if path is None:
        return "not_provided"
    return _safe_tag(Path(path).name.replace(".", "_"))


def _safe_file_sha256(path: str | Path | None) -> str:
    if path is None:
        return "not_provided"
    source_path = Path(path)
    if not source_path.exists():
        return "not_found"
    digest = hashlib.sha256()
    with source_path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _paid_amount(value: str) -> Decimal:
    try:
        return Decimal(str(value).strip() or "0")
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _bool(value: str) -> bool:
    return value.strip().casefold() in {"yes", "true", "1"}
