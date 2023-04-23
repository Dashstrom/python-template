"""Module for use module as a cli."""

import argparse
from typing import Optional, Sequence

from .core import hello
from .info import __author__, __copyright__, __description__, __version__


def cli(argv: Optional[Sequence[str]] = None) -> None:
    """Entrypoint for CLI."""
    parser = argparse.ArgumentParser(
        prog="{{ cookiecutter.__cli_name }}",
        description=__description__,
        epilog=__copyright__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args(argv)
    if args.version:  # type: ignore[misc]
        print(__version__)
    else:
        hello(__author__)


if __name__ == "__main__":
    cli()
