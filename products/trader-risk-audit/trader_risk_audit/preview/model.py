from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from trader_risk_audit.audit_session.artifact_bundle import (
    load_artifact_bundle_index,
)
from trader_risk_audit.preview.cta import build_paid_pilot_cta, render_paid_pilot_cta
from trader_risk_audit.reporting.claim_guard import (
    REQUIRED_DISCLAIMER,
    ensure_report_claims_valid,
)

PREVIEW_FILE_NAME = "preview.md"


class PreviewError(ValueError):
    pass


@dataclass(frozen=True)
class PreviewRuleCategory:
    rule_type: str
    count: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class PreviewModel:
    bundle_id: str
    audit_status: str
    source_coverage: dict[str, str | int]
    violation_count: int
    top_rule_categories: tuple[PreviewRuleCategory, ...]
    unsupported_fields: tuple[str, ...]
    next_action: str

    def to_dict(self) -> dict[str, object]:
        return {
            "audit_status": self.audit_status,
            "bundle_id": self.bundle_id,
            "next_action": self.next_action,
            "source_coverage": dict(self.source_coverage),
            "top_rule_categories": [
                category.to_dict() for category in self.top_rule_categories
            ],
            "unsupported_fields": list(self.unsupported_fields),
            "violation_count": self.violation_count,
        }


def build_preview_model(bundle_path: str | Path) -> PreviewModel:
    bundle_file = Path(bundle_path)
    bundle = load_artifact_bundle_index(bundle_file)
    root = bundle_file.parent
    artifact_refs = {artifact.name: artifact.ref for artifact in bundle.artifacts}
    normalized_trades = _load_json_list(
        root / _required_ref(artifact_refs, "normalized_trades")
    )
    violations = _load_json_list(root / _required_ref(artifact_refs, "violations"))
    rule_counts = Counter(
        _safe_label(violation.get("rule_type"), "unknown_rule")
        for violation in violations
        if isinstance(violation, dict)
    )
    top_rule_categories = tuple(
        PreviewRuleCategory(rule_type=rule_type, count=count)
        for rule_type, count in sorted(
            rule_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )[:5]
    )
    unsupported_fields = tuple(
        sorted(
            {
                _safe_label(register.name, "manual_review_required")
                for register in bundle.limitation_registers
            }
        )
    )
    return PreviewModel(
        bundle_id=_safe_label(bundle.bundle_id, "unknown"),
        audit_status=_safe_label(bundle.status, "unknown"),
        source_coverage={
            "policy_ref": _safe_label(
                bundle.input_refs.get("policy"),
                "policy_file",
            ),
            "source_export_ref": _safe_label(
                bundle.input_refs.get("source_export"),
                "source_export",
            ),
            "trade_count": len(normalized_trades),
        },
        violation_count=len(violations),
        top_rule_categories=top_rule_categories,
        unsupported_fields=unsupported_fields,
        next_action=(
            "Request an operator-reviewed full report to inspect source-row "
            "evidence, limitations, and deterministic artifacts."
        ),
    )


def render_preview_markdown(model: PreviewModel) -> str:
    lines = [
        "# Audit Preview",
        "",
        f"Bundle: `{model.bundle_id}`",
        f"Status: `{model.audit_status}`",
        "",
        "## Source Coverage",
        "",
        f"- Source export: `{model.source_coverage['source_export_ref']}`",
        f"- Policy: `{model.source_coverage['policy_ref']}`",
        f"- Normalized trade count: {model.source_coverage['trade_count']}",
        f"- Violation count: {model.violation_count}",
        "",
        "## Top Rule Categories",
        "",
    ]
    if model.top_rule_categories:
        lines.extend(
            f"- `{category.rule_type}`: {category.count}"
            for category in model.top_rule_categories
        )
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Limitations",
            "",
        ]
    )
    if model.unsupported_fields:
        lines.extend(
            f"- `{field}` requires review" for field in model.unsupported_fields
        )
    else:
        lines.append("- No limitation register attached to this preview.")
    lines.extend(
        [
            "",
            "## Next Action",
            "",
            model.next_action,
            "",
        ]
    )
    cta_text = render_paid_pilot_cta(
        build_paid_pilot_cta(audit_status=model.audit_status)
    )
    if cta_text:
        lines.append(cta_text)
    lines.extend([REQUIRED_DISCLAIMER, ""])
    preview_text = "\n".join(lines)
    ensure_report_claims_valid(preview_text)
    return preview_text


def write_preview_markdown(model: PreviewModel, output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    preview_path = output_path / PREVIEW_FILE_NAME
    preview_path.write_text(render_preview_markdown(model), encoding="utf-8")
    return preview_path


def _required_ref(artifact_refs: dict[str, str], name: str) -> str:
    ref = artifact_refs.get(name)
    if not ref:
        raise PreviewError(f"preview requires bundle artifact: {name}")
    ref_path = Path(ref)
    if ref_path.is_absolute() or ".." in ref_path.parts:
        raise PreviewError(f"unsafe bundle artifact ref: {name}")
    return ref


def _load_json_list(path: Path) -> list[Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise PreviewError("preview artifact must contain a JSON list")
    return payload


def _safe_label(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        normalized = value.strip()
        allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-"
        if len(normalized) <= 128 and all(
            character in allowed for character in normalized
        ):
            return normalized
    return fallback
