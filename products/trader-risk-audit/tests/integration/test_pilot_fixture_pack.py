from __future__ import annotations

import json
import re
from pathlib import Path

from trader_risk_audit.cli import main

PILOT_TRADES = Path("tests/fixtures/pilot/trades.csv")
PILOT_POLICY = Path("tests/fixtures/pilot/policy.yaml")
EXPECTED_VIOLATIONS = Path("tests/fixtures/expected/pilot_violations.json")
EXPECTED_ATTRIBUTION = Path("tests/fixtures/expected/pilot_attribution.json")
EXPECTED_REPORT = Path("tests/fixtures/expected/pilot_report.md")
EXPECTED_MANIFEST_HASHES = Path("tests/fixtures/expected/pilot_manifest_hashes.json")

FORBIDDEN_IDENTIFIER_PATTERNS = (
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"@[A-Za-z][A-Za-z0-9_]{4,}"),
    re.compile(r"\b\d{6,}\b"),
    re.compile(r"\b(?:john|jane|alice|bob|charlie|smith|doe)\b", re.I),
    re.compile(r"\b(?:account|acct)[-_ ]?\d{4,}\b", re.I),
)


def test_fixture_pack_contains_expected_artifacts() -> None:
    for path in (
        PILOT_TRADES,
        PILOT_POLICY,
        EXPECTED_VIOLATIONS,
        EXPECTED_ATTRIBUTION,
        EXPECTED_REPORT,
        EXPECTED_MANIFEST_HASHES,
    ):
        assert path.exists()

    manifest_hashes = json.loads(EXPECTED_MANIFEST_HASHES.read_text(encoding="utf-8"))
    assert set(manifest_hashes["artifacts"]) == {
        "source_export",
        "policy_file",
        "normalized_trades",
        "violations",
        "attribution_summary",
        "report_markdown",
        "delivery_packet",
    }
    assert manifest_hashes["content_hash"]


def test_end_to_end_fixture_outputs_match_expected_files(tmp_path: Path) -> None:
    output_dir = tmp_path / "pilot"

    result = main(
        [
            "audit",
            "--trades",
            str(PILOT_TRADES),
            "--policy",
            str(PILOT_POLICY),
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    assert (output_dir / "violations.json").read_text(
        encoding="utf-8"
    ) == EXPECTED_VIOLATIONS.read_text(encoding="utf-8").strip()
    assert (output_dir / "attribution_summary.json").read_text(
        encoding="utf-8"
    ) == EXPECTED_ATTRIBUTION.read_text(encoding="utf-8").strip()
    assert (output_dir / "report.md").read_text(
        encoding="utf-8"
    ) == EXPECTED_REPORT.read_text(encoding="utf-8")

    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    expected_hashes = json.loads(EXPECTED_MANIFEST_HASHES.read_text(encoding="utf-8"))
    artifact_hashes = {
        artifact["name"]: artifact["sha256"] for artifact in manifest["artifacts"]
    }
    assert manifest["content_hash"] == expected_hashes["content_hash"]
    assert artifact_hashes == expected_hashes["artifacts"]


def test_committed_fixtures_do_not_contain_customer_identifiers() -> None:
    fixture_paths = tuple(Path("tests/fixtures").rglob("*"))
    scanned_files = [path for path in fixture_paths if path.is_file()]

    for path in scanned_files:
        text = path.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_IDENTIFIER_PATTERNS:
            assert pattern.search(text) is None, f"{path} matched {pattern.pattern}"
