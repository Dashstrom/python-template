"""Module for use module as a cli."""{% if cookiecutter.cli|lower == 'argparse' %}
import argparse
import sys
from typing import Optional, Sequence

from .core import hello
from .info import __author__, __copyright__, __description__, __version__


def get_parser() -> argparse.ArgumentParser:
    """Get configured parser."""
    parser = argparse.ArgumentParser(
        prog="{{ cookiecutter.__cli_name }}",
        description=__description__,
        epilog=__copyright__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s, version {__version__}",
    )
    hello_subparser = parser.add_subparsers(dest="command_hello")
    hello_parser = hello_subparser.add_parser("hello")
    hello_parser.add_argument(
        "--name",
        help="name to greating",
        default=__author__,
    )
    return parser


def entrypoint(argv: Optional[Sequence[str]] = None) -> None:
    """Entrypoint for CLI."""
    parser = get_parser()
    args = parser.parse_args(argv)
    if args.command_hello:
        print(hello(args.name))
    else:
        parser.error("No command specified")
    sys.exit(0){% elif cookiecutter.cli|lower == 'click' %}
import click

from .core import hello
from .info import __author__, __copyright__, __description__, __version__


@click.group(
    name="{{ cookiecutter.__pypi_name }}",
    help=__description__,
    epilog=__copyright__,
)
@click.version_option(__version__)
def entrypoint() -> None:
    """Console script."""


@entrypoint.command("hello")
@click.option("--name", default=__author__)
def hello_command(name: str) -> None:
    """Run hello command."""
    click.echo(hello(name)){% endif %}
