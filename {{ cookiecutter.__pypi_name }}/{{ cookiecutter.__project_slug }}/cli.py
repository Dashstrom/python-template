"""Module for use module as a cli."""{% if cookiecutter.cli|lower == 'argparse' %}
import argparse
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
    parser.add_argument("--version", action="store_true")
    hello_subparser = parser.add_subparsers()
    hello_parser = hello_subparser.add_parser("hello")
    hello_parser.add_argument(
        "name",
        help="Name to greating",
        default=__author__
    )
    return parser


def cli(argv: Optional[Sequence[str]] = None) -> None:
    """Entrypoint for CLI."""
    parser = get_parser()
    args = parser.parse_args(argv)
    if args.version:  # type: ignore[misc]
        print(__version__)
    elif args.hello:
        print(hello(args.hello.name))


if __name__ == "__main__":
    cli(){% elif cookiecutter.cli|lower == 'click' %}
import click

from .core import hello
from .info import __author__, __copyright__, __description__, __version__


@click.group(name="{{ cookiecutter.__pypi_name }}", help=__description__, epilog=__copyright__)
@click.version_option(__version__)
def cli() -> None:
    """Console script."""


@cli.command("hello")
@click.argument("name", default=__author__)
def hello_command(name: str) -> None:
    """Run hello command."""
    click.echo(hello(name))


if __name__ == "__main__":
    cli(){% endif %}
