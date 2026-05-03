"""CLI entry point for Entropy Protocol."""

import typer

from entropy import __version__

app = typer.Typer(
    help="Entropy Protocol command-line interface.",
    no_args_is_help=True,
    rich_markup_mode=None,
)


@app.callback()
def callback() -> None:
    """Operate Entropy Protocol from the command line."""


@app.command()
def version() -> None:
    """Print the installed package version."""
    typer.echo(__version__)


def main() -> None:
    """Run the CLI application."""
    app()
