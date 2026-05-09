from __future__ import annotations

import argparse
import csv
import json
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
from trader_risk_audit.evidence import (
    EvidenceRow,
    EvidenceValidationError,
    append_customer_log_row,
    load_customer_log,
    summarize_validation_gate,
)
from trader_risk_audit.exchange.bybit import normalize_bybit_executions
from trader_risk_audit.exchange.manifest import build_exchange_import_manifest
from trader_risk_audit.exchange.normalizer import normalize_exchange_records
from trader_risk_audit.exchange.snapshot import FetchedPage, build_raw_exchange_snapshot
from trader_risk_audit.pilot_queue import (
    PilotQueue,
    PilotQueueError,
    format_queue_list,
    format_queue_request,
)
from trader_risk_audit.policy.profiles import (
    PolicyProfileSelectionError,
    resolve_policy_profile,
)
from trader_risk_audit.policy.review import build_review_packet
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.policy.validation import (
    PolicyReviewRequiredError,
    ensure_policy_ready_for_evaluation,
)
from trader_risk_audit.reporting.claim_guard import ensure_report_claims_valid
from trader_risk_audit.reporting.delivery import render_delivery_packet
from trader_risk_audit.reporting.markdown import render_markdown_report
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.storage.retention import (
    delete_manifest_artifacts,
    format_retention_list,
)
from trader_risk_audit.trades.importers import normalize_csv, serialize_trade_records
from trader_risk_audit.trades.schema import TradeRecord
from trader_risk_audit.workspace import create_audit_workspace


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

    demo = subparsers.add_parser("demo", help="Show local demo artifacts.")
    demo_subparsers = demo.add_subparsers(dest="demo_command")
    public_sample = demo_subparsers.add_parser(
        "public-sample",
        help="Show the committed public sample demo summary.",
    )
    public_sample.set_defaults(handler=_public_sample_demo_command)

    exchange_import = subparsers.add_parser(
        "exchange-import",
        help="Run local fixture-backed exchange import workflows.",
    )
    exchange_import_subparsers = exchange_import.add_subparsers(
        dest="exchange_import_command"
    )
    exchange_fixture = exchange_import_subparsers.add_parser(
        "fixture",
        help="Import a sanitized local exchange fixture snapshot.",
    )
    exchange_fixture.add_argument("--snapshot", required=True)
    exchange_fixture.add_argument("--output-dir", required=True)
    exchange_fixture.set_defaults(handler=_exchange_import_fixture_command)

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

    queue = subparsers.add_parser("queue", help="Manage local pilot review queue.")
    queue_subparsers = queue.add_subparsers(dest="queue_command")
    queue_list = queue_subparsers.add_parser("list", help="List pilot requests.")
    queue_list.add_argument("--queue-file", required=True)
    queue_list.set_defaults(handler=_queue_list_command)
    queue_show = queue_subparsers.add_parser("show", help="Show one pilot request.")
    queue_show.add_argument("--queue-file", required=True)
    queue_show.add_argument("--audit-id", required=True)
    queue_show.set_defaults(handler=_queue_show_command)
    queue_status = queue_subparsers.add_parser("status", help="Set request status.")
    queue_status.add_argument("--queue-file", required=True)
    queue_status.add_argument("--audit-id", required=True)
    queue_status.add_argument("--status", required=True)
    queue_status.set_defaults(handler=_queue_status_command)
    queue_reject = queue_subparsers.add_parser("reject", help="Reject one request.")
    queue_reject.add_argument("--queue-file", required=True)
    queue_reject.add_argument("--audit-id", required=True)
    queue_reject.add_argument("--reason", required=True)
    queue_reject.set_defaults(handler=_queue_reject_command)

    operator = subparsers.add_parser("operator", help="Run local operator workflow.")
    operator_subparsers = operator.add_subparsers(dest="operator_command")
    operator_prepare = operator_subparsers.add_parser(
        "prepare",
        help="Prepare a local audit workspace from intake files.",
    )
    operator_prepare.add_argument("--queue-file", required=True)
    operator_prepare.add_argument("--workspace-root", required=True)
    operator_prepare.add_argument("--audit-id", required=True)
    operator_prepare.add_argument("--trades", required=True)
    operator_prepare.add_argument("--policy", required=True)
    operator_prepare.add_argument("--profile", required=True)
    operator_prepare.set_defaults(handler=_operator_prepare_command)
    operator_run = operator_subparsers.add_parser(
        "run",
        help="Run a ready local audit workspace.",
    )
    operator_run.add_argument("--queue-file", required=True)
    operator_run.add_argument("--workspace-root", required=True)
    operator_run.add_argument("--audit-id", required=True)
    operator_run.set_defaults(handler=_operator_run_command)

    evidence = subparsers.add_parser("evidence", help="Capture pilot evidence.")
    evidence_subparsers = evidence.add_subparsers(dest="evidence_command")
    evidence_append = evidence_subparsers.add_parser(
        "append",
        help="Append one non-sensitive pilot evidence row.",
    )
    evidence_append.add_argument("--log-file", required=True)
    for field in (
        "prospect-source",
        "icp",
        "call-date",
        "paid-amount",
        "objections",
    ):
        evidence_append.add_argument(f"--{field}", required=True)
    for field in (
        "export-provided",
        "rules-provided",
        "report-delivered",
        "repeat-requested",
        "referral",
    ):
        evidence_append.add_argument(f"--{field}", action="store_true")
    evidence_append.set_defaults(handler=_evidence_append_command)
    evidence_summary = evidence_subparsers.add_parser(
        "summary",
        help="Summarize current validation gate counts.",
    )
    evidence_summary.add_argument("--log-file", required=True)
    evidence_summary.set_defaults(handler=_evidence_summary_command)

    return parser


def _stub_command(args: argparse.Namespace) -> int:
    print(f"{args.command} command is not implemented yet.")
    return 0


def _retention_list_command(args: argparse.Namespace) -> int:
    print(format_retention_list(tuple(args.manifest)), end="")
    return 0


def _public_sample_demo_command(args: argparse.Namespace) -> int:
    del args
    paths = _public_sample_paths()
    missing = [label for label, path in paths.items() if not path.exists()]
    if missing:
        print(f"public sample demo is incomplete: {', '.join(missing)}")
        return 2

    packet_lines = paths["delivery_packet"].read_text(encoding="utf-8").splitlines()
    summary_lines = tuple(line for line in packet_lines if line and ":" in line)[:3]
    lines = [
        "Public Sample Demo",
        "Audit ID: demo_public_sample_001",
        (
            "Source label: public/internal demo evidence, not paid pilot, PMF, "
            "or prospect evidence"
        ),
        "Starter profile: hard",
        f"Report: {paths['report']}",
        f"Delivery packet: {paths['delivery_packet']}",
        "Summary:",
        *summary_lines,
    ]
    print("\n".join(lines))
    return 0


def _exchange_import_fixture_command(args: argparse.Namespace) -> int:
    try:
        snapshot_path = Path(args.snapshot)
        output_dir = Path(args.output_dir)
        fixture = _load_exchange_fixture(snapshot_path)
        records = tuple(fixture["records"])
        exchange = str(fixture["exchange"])
        market = _fixture_market(exchange, records)
        symbols = _fixture_symbols(records)
        start_time, end_time = _fixture_time_range(records)
        endpoint_label = f"{exchange}.{fixture['endpoint_family']}"
        raw_snapshot = build_raw_exchange_snapshot(
            exchange=exchange,
            market=market,
            symbols=symbols,
            start_time=start_time,
            end_time=end_time,
            fetched_pages=(
                FetchedPage(
                    endpoint_label=endpoint_label,
                    page_number=1,
                    record_count=len(records),
                ),
            ),
            source_endpoint_labels=(endpoint_label,),
            raw_records=records,
        )
        normalized = _normalize_fixture_exchange_records(
            exchange=exchange,
            market=market,
            records=records,
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        raw_snapshot_output = output_dir / "raw_snapshot.json"
        normalized_output = output_dir / "normalized_trades.csv"
        manifest_output = output_dir / "import_manifest.json"
        raw_snapshot_output.write_text(raw_snapshot.to_json(), encoding="utf-8")
        _write_normalized_exchange_trades(normalized_output, normalized)
        manifest = build_exchange_import_manifest(
            raw_snapshot=raw_snapshot_output,
            normalized_trades=normalized_output,
            exchange=exchange,
            market=market,
            symbols=symbols,
            start_time=start_time,
            end_time=end_time,
        )
        manifest_output.write_text(manifest.to_json(), encoding="utf-8")
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"exchange fixture import failed: {error}")
        return 2

    print(f"wrote exchange import manifest: {manifest_output}")
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


def _queue_list_command(args: argparse.Namespace) -> int:
    print(format_queue_list(PilotQueue(args.queue_file).list_requests()), end="")
    return 0


def _queue_show_command(args: argparse.Namespace) -> int:
    try:
        request = PilotQueue(args.queue_file).get_request(args.audit_id)
    except PilotQueueError as error:
        print(str(error))
        return 2
    print(format_queue_request(request), end="")
    return 0


def _queue_status_command(args: argparse.Namespace) -> int:
    try:
        request = PilotQueue(args.queue_file).set_status(args.audit_id, args.status)
    except PilotQueueError as error:
        print(str(error))
        return 2
    print(format_queue_request(request), end="")
    return 0


def _queue_reject_command(args: argparse.Namespace) -> int:
    try:
        request = PilotQueue(args.queue_file).reject(args.audit_id, args.reason)
    except PilotQueueError as error:
        print(str(error))
        return 2
    print(format_queue_request(request), end="")
    return 0


def _operator_prepare_command(args: argparse.Namespace) -> int:
    try:
        trades_path = Path(args.trades)
        policy_path = Path(args.policy)
        selection = resolve_policy_profile(
            args.profile,
            custom_policy_path=policy_path if args.profile == "custom" else None,
        )
        workspace = create_audit_workspace(
            args.workspace_root,
            args.audit_id,
            status="ready_to_run",
            file_references={
                "trades_export": f"input/{trades_path.name}",
                "policy_file": f"input/{policy_path.name}",
            },
            policy_profile=selection,
        )
        workspace_trades = workspace.input_dir / trades_path.name
        workspace_policy = workspace.input_dir / policy_path.name
        workspace_trades.write_bytes(trades_path.read_bytes())
        workspace_policy.write_bytes(policy_path.read_bytes())
        request = PilotQueue(args.queue_file).upsert_request(
            args.audit_id,
            status="ready_to_run",
            file_references={
                "workspace": str(workspace.root),
                "trades_export": f"input/{workspace_trades.name}",
                "policy_file": f"input/{workspace_policy.name}",
                "selected_policy_profile": selection.selected_profile,
            },
        )
    except (OSError, PilotQueueError, PolicyProfileSelectionError, ValueError) as error:
        print(str(error))
        return 2

    print(_format_operator_prepare(workspace.root, request, selection.selected_profile))
    return 0


def _operator_run_command(args: argparse.Namespace) -> int:
    try:
        queue = PilotQueue(args.queue_file)
        request = queue.get_request(args.audit_id)
        if request.status != "ready_to_run":
            raise PilotQueueError("operator run requires ready_to_run status")
        workspace_root = Path(args.workspace_root) / args.audit_id
        trades_path = workspace_root / request.file_references["trades_export"]
        policy_path = workspace_root / request.file_references["policy_file"]
        output_dir = workspace_root / "output"

        audit_args = argparse.Namespace(
            trades=str(trades_path),
            policy=str(policy_path),
            output_dir=str(output_dir),
        )
        result = _audit_command(audit_args)
        if result != 0:
            return result

        report_path = output_dir / "report.md"
        packet_path = output_dir / "telegram_packet.txt"
        manifest_path = output_dir / "manifest.json"
        updated = queue.upsert_request(
            args.audit_id,
            status="ready_for_review",
            file_references={
                **request.file_references,
                "report_markdown": f"output/{report_path.name}",
                "delivery_packet": f"output/{packet_path.name}",
                "manifest": f"output/{manifest_path.name}",
            },
        )
    except (KeyError, OSError, PilotQueueError, ValueError) as error:
        print(str(error))
        return 2

    print(_format_operator_run(updated))
    return 0


def _evidence_append_command(args: argparse.Namespace) -> int:
    try:
        append_customer_log_row(
            args.log_file,
            EvidenceRow(
                prospect_source=args.prospect_source,
                icp=args.icp,
                call_date=args.call_date,
                export_provided=args.export_provided,
                rules_provided=args.rules_provided,
                paid_amount=args.paid_amount,
                objections=args.objections,
                report_delivered=args.report_delivered,
                repeat_requested=args.repeat_requested,
                referral=args.referral,
            ),
        )
    except (OSError, EvidenceValidationError) as error:
        print(str(error))
        return 2
    print("Evidence row appended.")
    return 0


def _evidence_summary_command(args: argparse.Namespace) -> int:
    try:
        summary = summarize_validation_gate(load_customer_log(args.log_file))
    except (OSError, KeyError, EvidenceValidationError) as error:
        print(str(error))
        return 2
    print(summary.format())
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
        report_model = build_report_model(
            trades=trades,
            policy=policy,
            violations=violations,
            warnings=warnings,
            attribution=attribution,
        )
        report = render_markdown_report(report_model)
        ensure_report_claims_valid(report)

        output_dir.mkdir(parents=True, exist_ok=True)
        normalized_path = output_dir / "normalized_trades.json"
        violations_path = output_dir / "violations.json"
        attribution_path = output_dir / "attribution_summary.json"
        report_path = output_dir / "report.md"
        delivery_packet_path = output_dir / "telegram_packet.txt"
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
        delivery_packet_path.write_text(
            render_delivery_packet(
                model=report_model,
                report_text=report,
                report_path=report_path.name,
            ),
            encoding="utf-8",
        )

        manifest = build_audit_manifest(
            source_export=trades_path,
            policy_file=policy_path,
            normalized_trades=normalized_path,
            violations=violations_path,
            attribution_summary=attribution_path,
            report_markdown=report_path,
            delivery_packet=delivery_packet_path,
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


def _format_operator_prepare(
    workspace_root: Path,
    request,
    selected_profile: str,
) -> str:
    lines = [
        f"Audit ID: {request.audit_id}",
        f"Status: {request.status}",
        f"Workspace: {workspace_root}",
        f"Selected policy profile: {selected_profile}",
        "Input Files:",
        f"- trades_export: {request.file_references['trades_export']}",
        f"- policy_file: {request.file_references['policy_file']}",
        "Next action: operator run",
    ]
    return "\n".join(lines)


def _format_operator_run(request) -> str:
    lines = [
        f"Audit ID: {request.audit_id}",
        f"Status: {request.status}",
        "Output References:",
        f"- report_markdown: {request.file_references['report_markdown']}",
        f"- delivery_packet: {request.file_references['delivery_packet']}",
        f"- manifest: {request.file_references['manifest']}",
    ]
    return "\n".join(lines)


def _public_sample_paths() -> dict[str, Path]:
    root = Path("demo/public_sample_001")
    return {
        "source": root / "source.md",
        "report": root / "output" / "report.md",
        "delivery_packet": root / "output" / "telegram_packet.txt",
        "manifest": root / "output" / "manifest.json",
    }


def _load_exchange_fixture(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as fixture_file:
        payload = json.load(fixture_file)
    if not isinstance(payload, dict):
        raise ValueError("fixture snapshot must contain a JSON object")
    records = payload.get("records")
    if not isinstance(records, list) or not all(
        isinstance(record, dict) for record in records
    ):
        raise ValueError("fixture snapshot must contain a records list")
    if not records:
        raise ValueError("fixture snapshot records must not be empty")
    for field in ("exchange", "endpoint_family"):
        if not str(payload.get(field, "")).strip():
            raise ValueError(f"fixture snapshot missing required field: {field}")
    return payload


def _fixture_market(exchange: str, records: Sequence[object]) -> str:
    if exchange == "binance":
        return "spot"
    first = records[0]
    if isinstance(first, dict):
        category = str(first.get("category", "")).strip()
        if category:
            return category
    return "unknown"


def _fixture_symbols(records: Sequence[object]) -> tuple[str, ...]:
    symbols = sorted(
        {
            str(record.get("symbol", "")).strip()
            for record in records
            if isinstance(record, dict) and str(record.get("symbol", "")).strip()
        }
    )
    if not symbols:
        raise ValueError("fixture snapshot records must include symbols")
    return tuple(symbols)


def _fixture_time_range(records: Sequence[object]) -> tuple[str, str]:
    timestamps = sorted(
        {
            timestamp
            for record in records
            if isinstance(record, dict)
            for timestamp in (_record_timestamp(record),)
            if timestamp
        }
    )
    if not timestamps:
        raise ValueError("fixture snapshot records must include timestamps")
    return timestamps[0], timestamps[-1]


def _record_timestamp(record: dict[object, object]) -> str | None:
    for field in ("timestamp", "time", "exec_time", "executed_at"):
        value = record.get(field)
        if value not in (None, ""):
            return str(value)
    return None


def _write_normalized_exchange_trades(
    path: Path,
    records: Sequence[TradeRecord],
) -> None:
    fieldnames = (
        "row_id",
        "timestamp",
        "symbol",
        "side",
        "quantity",
        "price",
        "fees",
        "account_id",
    )
    with path.open("w", encoding="utf-8", newline="") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {
                    "account_id": record.account_id,
                    "fees": format(record.fees.normalize(), "f"),
                    "price": format(record.price.normalize(), "f"),
                    "quantity": format(record.quantity.normalize(), "f"),
                    "row_id": record.row_id,
                    "side": record.side,
                    "symbol": record.symbol,
                    "timestamp": record.timestamp.isoformat(),
                }
            )


def _normalize_fixture_exchange_records(
    *,
    exchange: str,
    market: str,
    records: Sequence[dict[str, object]],
) -> tuple[TradeRecord, ...]:
    if exchange == "bybit":
        return normalize_bybit_executions(records, category=market).trades
    return normalize_exchange_records(
        exchange=exchange,
        market=market,
        records=records,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 0
    return int(handler(args))
