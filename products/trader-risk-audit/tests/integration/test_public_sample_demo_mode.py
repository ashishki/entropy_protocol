from __future__ import annotations

from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.telegram_bot.handlers import (
    TelegramDemoSample,
    TelegramPilotHandlers,
)
from trader_risk_audit.telegram_bot.storage import TelegramAuditStorage


def test_public_sample_demo_mode_returns_demo_summary(capsys) -> None:
    result = main(["demo", "public-sample"])

    output = capsys.readouterr().out
    assert result == 0
    assert "Public Sample Demo" in output
    assert "demo_public_sample_001" in output
    assert "public/internal demo evidence" in output
    assert "Starter profile: hard" in output
    assert "demo/public_sample_001/output/report.md" in output
    assert "Trades reviewed: 4" in output
    assert "Violations recorded: 9" in output


def test_public_sample_demo_mode_labels_evidence_correctly(tmp_path: Path) -> None:
    handlers = TelegramPilotHandlers(
        TelegramAuditStorage(tmp_path / "telegram_workspaces"),
        demo_sample=TelegramDemoSample(
            audit_id="demo_public_sample_001",
            source_label=(
                "public/internal demo evidence, not paid pilot, PMF, "
                "or prospect evidence"
            ),
            report_path=Path("demo/public_sample_001/output/report.md"),
            delivery_packet_path=Path(
                "demo/public_sample_001/output/telegram_packet.txt"
            ),
            starter_profile="hard",
        ),
    )

    response = handlers.handle_command("/demo_sample")
    text = response.text.casefold()

    assert response.status == "ready_for_review"
    assert "public/internal demo evidence" in text
    assert "not paid pilot" in text
    assert "pmf" in text
    assert "prospect evidence" in text
    assert "proof that traders will pay" not in text


def test_public_sample_demo_mode_reuses_audit_artifacts(capsys) -> None:
    result = main(["demo", "public-sample"])
    output = capsys.readouterr().out

    assert result == 0
    expected_paths = (
        Path("demo/public_sample_001/output/report.md"),
        Path("demo/public_sample_001/output/telegram_packet.txt"),
        Path("demo/public_sample_001/output/manifest.json"),
    )
    for path in expected_paths:
        assert path.exists()

    assert "demo/public_sample_001/output/report.md" in output
    assert "demo/public_sample_001/output/telegram_packet.txt" in output
    assert "new report format" not in output.casefold()
