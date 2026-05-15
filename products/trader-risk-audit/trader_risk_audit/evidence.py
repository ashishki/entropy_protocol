from __future__ import annotations

import csv
import re
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

PILOT_CUSTOMER_LOG_FIELDS = (
    "prospect_source",
    "icp",
    "call_date",
    "export_provided",
    "rules_provided",
    "paid_amount",
    "objections",
    "report_delivered",
    "repeat_requested",
    "referral",
)
DEMO_SOURCES = frozenset({"public_sample_demo", "internal_demo", "demo_artifact"})
_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_HANDLE_PATTERN = re.compile(r"@[A-Za-z][A-Za-z0-9_]{4,}")
_LONG_NUMBER_PATTERN = re.compile(r"\b\d{6,}\b")


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

    def to_csv_row(self) -> dict[str, str]:
        _validate_safe_fields(asdict(self))
        return {
            "prospect_source": self.prospect_source,
            "icp": self.icp,
            "call_date": self.call_date,
            "export_provided": _yes_no(self.export_provided),
            "rules_provided": _yes_no(self.rules_provided),
            "paid_amount": self.paid_amount,
            "objections": self.objections,
            "report_delivered": _yes_no(self.report_delivered),
            "repeat_requested": _yes_no(self.repeat_requested),
            "referral": _yes_no(self.referral),
        }


@dataclass(frozen=True)
class ValidationGateSummary:
    qualified_prospects: int
    exports_and_rules: int
    paid_audits: int
    repeat_commitments: int
    referrals: int

    def format(self) -> str:
        return "\n".join(
            (
                "Validation Gate Summary",
                f"Qualified prospects: {self.qualified_prospects}/10",
                f"Exports and rules: {self.exports_and_rules}/5",
                f"Paid audits: {self.paid_audits}/3",
                f"Repeat commitments: {self.repeat_commitments}/2",
                f"Referrals: {self.referrals}",
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


def load_customer_log(path: str | Path) -> tuple[EvidenceRow, ...]:
    log_path = Path(path)
    if not log_path.exists():
        return ()
    with log_path.open(newline="", encoding="utf-8") as log_file:
        return tuple(_row_from_mapping(row) for row in csv.DictReader(log_file))


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
    )


def is_demo_evidence(row: EvidenceRow) -> bool:
    return row.prospect_source.strip().casefold() in DEMO_SOURCES


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
    )


def _validate_safe_fields(payload: dict[str, object]) -> None:
    for field, value in payload.items():
        text = str(value)
        lowered = text.casefold()
        if "\n" in text or "\r" in text:
            raise EvidenceValidationError(f"{field} must be a single line")
        if _EMAIL_PATTERN.search(text) or _HANDLE_PATTERN.search(text):
            raise EvidenceValidationError(f"{field} must not contain identifiers")
        if _LONG_NUMBER_PATTERN.search(text):
            raise EvidenceValidationError(f"{field} must not contain account numbers")
        if "timestamp,symbol" in lowered or "api_key" in lowered:
            raise EvidenceValidationError(f"{field} must be non-sensitive")


def _paid_amount(value: str) -> Decimal:
    try:
        return Decimal(str(value).strip() or "0")
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _bool(value: str) -> bool:
    return value.strip().casefold() in {"yes", "true", "1"}
