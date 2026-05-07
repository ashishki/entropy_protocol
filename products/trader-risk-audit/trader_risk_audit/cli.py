from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path

from trader_risk_audit import __version__
from trader_risk_audit.artifacts.manifest import build_audit_manifest, hash_file
from trader_risk_audit.evaluation.attribution import (
    attribute_pnl,
    ensure_reconciled,
    serialize_attribution,
)
from trader_risk_audit.evaluation.rules import (
    evaluate_loss_rules,
    evaluate_position_asset_rules,
)
from trader_risk_audit.evaluation.violations import serialize_violations
from trader_risk_audit.policy.review import build_review_packet
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.policy.validation import (
    PolicyReviewRequiredError,
    ensure_policy_ready_for_evaluation,
)
from trader_risk_audit.reporting.claim_guard import ensure_report_claims_valid
from trader_risk_audit.reporting.markdown import render_markdown_report
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.storage.retention import (
    delete_manifest_artifacts,
    format_retention_list,
)
from trader_risk_audit.trades.importers import normalize_csv, serialize_trade_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trader_risk_audit",
        description="Run local deterministic trader risk audit workflows.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"trader-risk-audit {__version__}",
    )

    subparsers = parser.add_subparsers(dest="command")

    audit = subparsers.add_parser("audit", help="Run an audit workflow.")
    audit.add_argument("--trades", required=True, help="Path to a trade export.")
    audit.add_argument("--policy", required=True, help="Path to a risk policy file.")
    audit.add_argument(
        "--output-dir",
        required=True,
        help="Directory for audit artifacts.",
    )
    audit.set_defaults(handler=_audit_command)

    manifest = subparsers.add_parser("manifest", help="Inspect audit manifests.")
    manifest.set_defaults(handler=_stub_command)

    retention = subparsers.add_parser("retention", help="Manage local audit retention.")
    retention_subparsers = retention.add_subparsers(dest="retention_command")
    retention_list = retention_subparsers.add_parser(
        "list",
        help="List local artifact groups by manifest.",
    )
    retention_list.add_argument("--manifest", action="append", required=True)
    retention_list.set_defaults(handler=_retention_list_command)
    retention_delete = retention_subparsers.add_parser(
        "delete",
        help="Delete local artifact files referenced by a manifest.",
    )
    retention_delete.add_argument("--manifest", required=True)
    retention_delete.add_argument("--dry-run", action="store_true")
    retention_delete.add_argument("--confirm-delete", action="store_true")
    retention_delete.set_defaults(handler=_retention_delete_command)

    return parser


def _stub_command(args: argparse.Namespace) -> int:
    print(f"{args.command} command is not implemented yet.")
    return 0


def _retention_list_command(args: argparse.Namespace) -> int:
    print(format_retention_list(tuple(args.manifest)), end="")
    return 0


def _retention_delete_command(args: argparse.Namespace) -> int:
    try:
        result = delete_manifest_artifacts(
            args.manifest,
            dry_run=args.dry_run,
            confirm_delete=args.confirm_delete,
        )
    except ValueError as error:
        print(str(error))
        return 2
    print("referenced paths:")
    for path in result.referenced_paths:
        print(path)
    if result.dry_run:
        return 0
    print("removed paths:")
    for path in result.removed_paths:
        print(path)
    print("missing paths:")
    for path in result.missing_paths:
        print(path)
    return 0


def _audit_command(args: argparse.Namespace) -> int:
    try:
        trades_path = Path(args.trades)
        policy_path = Path(args.policy)
        output_dir = Path(args.output_dir)

        trades = normalize_csv(trades_path)
        policy = load_policy(policy_path)
        ensure_policy_ready_for_evaluation(policy, build_review_packet(policy))

        position_asset_result = evaluate_position_asset_rules(trades, policy)
        loss_result = evaluate_loss_rules(trades, policy)
        violations = tuple(
            sorted(
                position_asset_result.violations + loss_result.violations,
                key=lambda item: (item.timestamp, item.rule_id, item.source_row_ids),
            )
        )
        warnings = tuple(
            sorted(
                position_asset_result.warnings + loss_result.warnings,
                key=lambda item: (item.rule_id, item.message_code),
            )
        )
        attribution = ensure_reconciled(attribute_pnl(trades, violations))
        report = render_markdown_report(
            build_report_model(
                trades=trades,
                policy=policy,
                violations=violations,
                warnings=warnings,
                attribution=attribution,
            )
        )
        ensure_report_claims_valid(report)

        output_dir.mkdir(parents=True, exist_ok=True)
        normalized_path = output_dir / "normalized_trades.json"
        violations_path = output_dir / "violations.json"
        attribution_path = output_dir / "attribution_summary.json"
        report_path = output_dir / "report.md"
        manifest_path = output_dir / "manifest.json"

        audit_id = _audit_id(trades_path, policy_path)
        normalized_path.write_text(serialize_trade_records(trades), encoding="utf-8")
        violations_path.write_text(
            serialize_violations(audit_id, violations),
            encoding="utf-8",
        )
        attribution_path.write_text(
            serialize_attribution(attribution),
            encoding="utf-8",
        )
        report_path.write_text(report, encoding="utf-8")

        manifest = build_audit_manifest(
            source_export=trades_path,
            policy_file=policy_path,
            normalized_trades=normalized_path,
            violations=violations_path,
            attribution_summary=attribution_path,
            report_markdown=report_path,
            command="trader-risk-audit audit",
            command_arguments=(
                "--trades",
                str(trades_path),
                "--policy",
                str(policy_path),
                "--output-dir",
                str(output_dir),
            ),
        )
        manifest_path.write_text(manifest.to_json(), encoding="utf-8")
        print(f"wrote audit manifest: {manifest_path}")
        return 0
    except PolicyReviewRequiredError as error:
        print(str(error))
        return 2
    except Exception as error:
        print(f"audit failed: {error}")
        return 1


def _audit_id(trades_path: Path, policy_path: Path) -> str:
    return f"audit_{hash_file(trades_path)[:8]}{hash_file(policy_path)[:8]}"


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))
