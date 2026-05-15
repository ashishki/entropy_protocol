from __future__ import annotations

import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path

from signal_sandbox.cli import PLANNED_SUBCOMMANDS

SCRIPT_PATH = Path(sys.executable).with_name("signal-sandbox")


def run_cli(
    *args: str,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(SCRIPT_PATH), *args],
        capture_output=True,
        env=env,
        text=True,
        check=False,
    )


def test_help_lists_subcommands() -> None:
    result = run_cli("--help")

    assert result.returncode == 0
    for subcommand in PLANNED_SUBCOMMANDS:
        assert subcommand in result.stdout


def test_unimplemented_subcommands_exit_2() -> None:
    unimplemented = [command for command in PLANNED_SUBCOMMANDS if command != "status"]

    for command in unimplemented:
        result = run_cli(command)
        combined_output = result.stdout + result.stderr
        assert result.returncode == 2, command
        assert "not implemented" in combined_output


def test_status_exits_zero(tmp_path: Path) -> None:
    result = run_cli(
        "status",
        env={"SIGNAL_SANDBOX_WORKSPACE": str(tmp_path)},
    )

    assert result.returncode == 0
    assert "status: ok" in result.stdout
