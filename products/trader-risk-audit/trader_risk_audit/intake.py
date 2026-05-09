from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO
from pathlib import Path

from trader_risk_audit.policy.profiles import CUSTOM_PROFILE, STARTER_PROFILES
from trader_risk_audit.trades.schema import TradeRecord, TradeValidationError

MAX_INTAKE_FILE_BYTES = 5 * 1024 * 1024
SUPPORTED_INTAKE_SUFFIXES = frozenset({".csv", ".yaml", ".yml", ".md", ".txt"})
SUPPORTED_TRADE_SUFFIXES = frozenset({".csv"})
POLICY_SUFFIXES = frozenset({".yaml", ".yml", ".md", ".txt"})
REQUIRED_TRADE_FIELDS = ("timestamp", "symbol", "side", "quantity", "price")
_COLUMN_ALIASES = {
    "timestamp": ("timestamp", "time", "executed_at", "executed at"),
    "symbol": ("symbol", "ticker", "instrument"),
    "side": ("side", "action"),
    "quantity": ("quantity", "qty", "size"),
    "price": ("price", "fill_price", "fill price", "execution_price"),
    "fees": ("fees", "fee", "commission"),
    "account_id": ("account_id", "account", "account id"),
}


@dataclass(frozen=True)
class IntakeFile:
    file_name: str
    content: bytes


@dataclass(frozen=True)
class IntakeValidationIssue:
    code: str
    message: str


@dataclass(frozen=True)
class IntakeValidationResult:
    status: str
    issues: tuple[IntakeValidationIssue, ...]

    @property
    def is_operator_ready(self) -> bool:
        return not self.issues and self.status == "operator_ready"

    def safe_feedback(self) -> str:
        if not self.issues:
            return "Intake files validated. Status: operator_ready."
        messages = "; ".join(issue.message for issue in self.issues)
        return f"Intake needs user fixes. Status: needs_user_fix. {messages}"


def validate_intake_files(
    files: tuple[IntakeFile, ...],
    *,
    selected_profile: str | None,
) -> IntakeValidationResult:
    issues: list[IntakeValidationIssue] = []
    normalized_profile = (selected_profile or "").strip().casefold()
    has_trade_csv = False
    has_policy_file = False

    if not normalized_profile:
        issues.append(
            IntakeValidationIssue(
                "missing_policy_profile",
                "select soft, medium, hard, or custom policy profile",
            )
        )
    elif normalized_profile not in (*STARTER_PROFILES, CUSTOM_PROFILE):
        issues.append(
            IntakeValidationIssue(
                "unsupported_policy_profile",
                "policy profile must be soft, medium, hard, or custom",
            )
        )

    for intake_file in files:
        suffix = Path(intake_file.file_name).suffix.casefold()
        if suffix not in SUPPORTED_INTAKE_SUFFIXES:
            issues.append(
                IntakeValidationIssue(
                    "unsupported_file_type",
                    f"{Path(intake_file.file_name).name}: unsupported file type",
                )
            )
            continue
        if len(intake_file.content) > MAX_INTAKE_FILE_BYTES:
            issues.append(
                IntakeValidationIssue(
                    "file_too_large",
                    f"{Path(intake_file.file_name).name}: file exceeds size limit",
                )
            )
            continue
        if suffix in POLICY_SUFFIXES:
            has_policy_file = True
        if suffix in SUPPORTED_TRADE_SUFFIXES:
            has_trade_csv = True
            issues.extend(_validate_trade_csv(intake_file))

    if not files:
        issues.append(IntakeValidationIssue("missing_files", "upload intake files"))
    if not has_trade_csv:
        issues.append(
            IntakeValidationIssue(
                "missing_trade_export",
                "upload a supported trade CSV export",
            )
        )
    if normalized_profile == CUSTOM_PROFILE and not has_policy_file:
        issues.append(
            IntakeValidationIssue(
                "missing_custom_policy",
                "custom profile requires written risk rules or policy file",
            )
        )

    return IntakeValidationResult(
        status="needs_user_fix" if issues else "operator_ready",
        issues=tuple(issues),
    )


def validate_uploaded_trade_file(
    file_name: str,
    content: bytes,
) -> IntakeValidationResult:
    return validate_intake_files(
        (IntakeFile(file_name=file_name, content=content),),
        selected_profile="soft",
    )


def _validate_trade_csv(intake_file: IntakeFile) -> tuple[IntakeValidationIssue, ...]:
    issues: list[IntakeValidationIssue] = []
    try:
        text = intake_file.content.decode("utf-8-sig")
    except UnicodeDecodeError:
        return (
            IntakeValidationIssue(
                "csv_decode_error",
                f"{Path(intake_file.file_name).name}: CSV must be UTF-8 text",
            ),
        )

    try:
        reader = csv.DictReader(StringIO(text))
        fieldnames = tuple(reader.fieldnames or ())
        column_map = _build_column_map(fieldnames)
        missing = tuple(
            field for field in REQUIRED_TRADE_FIELDS if field not in column_map
        )
        if missing:
            issues.append(
                IntakeValidationIssue(
                    "missing_trade_columns",
                    "missing canonical fields: " + ", ".join(missing),
                )
            )
            return tuple(issues)
        rows = list(reader)
    except csv.Error:
        return (
            IntakeValidationIssue(
                "csv_parse_error",
                f"{Path(intake_file.file_name).name}: CSV parse error",
            ),
        )

    if not rows:
        issues.append(
            IntakeValidationIssue(
                "empty_trade_export",
                f"{Path(intake_file.file_name).name}: trade CSV has no data rows",
            )
        )
        return tuple(issues)

    for row_number, row in enumerate(rows, start=2):
        try:
            TradeRecord.from_mapping(
                {
                    field: row[source_column]
                    for field, source_column in column_map.items()
                    if source_column in row
                }
                | {
                    "fees": row.get(column_map.get("fees", ""), "0"),
                    "source_file": Path(intake_file.file_name).name,
                    "source_row_number": row_number,
                }
            )
        except TradeValidationError as error:
            issues.append(
                IntakeValidationIssue(
                    "invalid_trade_row",
                    f"row {row_number}: invalid fields {', '.join(error.fields)}",
                )
            )
    return tuple(issues)


def _build_column_map(fieldnames: tuple[str, ...]) -> dict[str, str]:
    normalized_to_source = {_normalize_column(name): name for name in fieldnames}
    column_map: dict[str, str] = {}
    for canonical_field, aliases in _COLUMN_ALIASES.items():
        for alias in aliases:
            source_column = normalized_to_source.get(_normalize_column(alias))
            if source_column is not None:
                column_map[canonical_field] = source_column
                break
    return column_map


def _normalize_column(column: str) -> str:
    return column.strip().casefold().replace("-", "_").replace(" ", "_")
