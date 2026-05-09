"""Command-line interface for Signal Analytics Sandbox."""

from __future__ import annotations

import click

from signal_sandbox.config import get_workspace

PLANNED_SUBCOMMANDS = (
    "init-workspace",
    "add-source",
    "extract",
    "review",
    "snapshot",
    "match",
    "report",
    "status",
)


def _not_implemented() -> None:
    click.echo("not implemented", err=True)
    raise click.exceptions.Exit(2)


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def main() -> None:
    """Audit public signal sources with deterministic local workflows."""


@main.command("init-workspace", help="Initialize a local operator workspace.")
def init_workspace() -> None:
    _not_implemented()


@main.command("add-source", help="Add a public source manifest.")
def add_source() -> None:
    _not_implemented()


@main.command("extract", help="Extract signal drafts from captured posts.")
def extract() -> None:
    _not_implemented()


@main.command("review", help="Review extraction drafts before ledger approval.")
def review() -> None:
    _not_implemented()


@main.command("snapshot", help="Create or load a price-data snapshot.")
def snapshot() -> None:
    _not_implemented()


@main.command("match", help="Match approved signals against a price snapshot.")
def match() -> None:
    _not_implemented()


@main.command("report", help="Render a Markdown audit report.")
def report() -> None:
    _not_implemented()


@main.command("status", help="Show local configuration status.")
def status() -> None:
    click.echo(f"status: ok\nworkspace: {get_workspace()}")


if __name__ == "__main__":
    main()
