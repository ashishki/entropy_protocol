"""Reset-phase package skeleton contract tests."""

from __future__ import annotations

import subprocess
import sys
from importlib import metadata

import entropy


def test_entropy_package_import_surface() -> None:
    """Importing entropy exposes a usable package version."""
    package_version = getattr(entropy, "__version__", "")
    metadata_version = metadata.version("entropy-protocol")

    assert isinstance(package_version, str)
    assert package_version
    assert package_version == metadata_version


def test_entropy_cli_help_runs() -> None:
    """The CLI help exposes the local operator command surface."""
    result = subprocess.run(
        [sys.executable, "-m", "entropy", "--help"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Entropy Protocol command-line interface." in result.stdout
    assert "health" in result.stdout
    assert "version" in result.stdout
