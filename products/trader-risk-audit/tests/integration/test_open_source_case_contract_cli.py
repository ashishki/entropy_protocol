from __future__ import annotations

from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.validation.open_source_case import (
    validate_open_source_case_pack,
)

ROOT = Path(__file__).resolve().parents[2]
SEC_PACK = ROOT / "demo" / "open_source_sec_form4_001"


def test_sec_form4_pack_passes_contract(capsys) -> None:
    result = validate_open_source_case_pack(SEC_PACK)

    assert result.ok, result.issues
    assert main(["case-bank", "validate", "--case-dir", str(SEC_PACK)]) == 0
    output = capsys.readouterr().out
    assert "case pack validation: passed" in output
    assert "open_source_sec_form4_001" in output
