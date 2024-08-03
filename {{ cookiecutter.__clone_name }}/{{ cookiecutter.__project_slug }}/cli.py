"""Module for command line interface."""
{%- if "argparse" == cookiecutter.cli %}

import argparse
import logging
import sys
from typing import NoReturn, Optional, Sequence

from .core import hello
from .info import __issues__, __summary__, __version__

LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
logger = logging.getLogger(__name__)


class HelpArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        """Handle error from argparse.ArgumentParser."""
        self.print_help(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n")


def get_parser() -> argparse.ArgumentParser:
    """Prepare ArgumentParser."""
    parser = HelpArgumentParser(
        prog="{{ cookiecutter.__cli_name }}",
        description=__summary__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s, version {__version__}",
    )

    # Add subparsers
    subparsers = parser.add_subparsers(
        help="desired action to perform",
        dest="action",
        required=True,
    )

    # Add parent parser with common arguments
    parent_parser = HelpArgumentParser(add_help=False)
    parent_parser.add_argument(
        "-v",
        "--verbose",
        help="verbose mode, enable INFO and DEBUG messages.",
        action="store_true",
        required=False,
    )

    # Parser of hello command
    hello_parser = subparsers.add_parser(
        "hello",
        parents=[parent_parser],
        help="greet the user.",
    )
    hello_parser.add_argument("--name", help="name to greeting")
    return parser


def setup_logging(verbose: Optional[bool] = None) -> None:
    """Do setup logging."""
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    )


def entrypoint(argv: Optional[Sequence[str]] = None) -> None:
    """Entrypoint for command line interface."""
    try:
        parser = get_parser()
        args = parser.parse_args(argv)
        setup_logging(args.verbose)
        if args.action == "hello":
            print(hello(args.name))  # noqa: T201
        else:
            parser.error("No command specified")
    except Exception as err:  # NoQA: BLE001
        logger.critical("Unexpected error", exc_info=err)
        logger.critical("Please, report this error to %s.", __issues__)
        sys.exit(1){% elif "click" == cookiecutter.cli %}

import logging
import sys
from functools import wraps
from typing import Callable, TypeVar

import click
from typing_extensions import ParamSpec

from .core import hello
from .info import __issues__, __summary__, __version__

logger = logging.getLogger(__name__)
LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
P = ParamSpec("P")
T = TypeVar("T")


def verbosity(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator for logging."""
    func = click.option(
        "-v",
        "--verbose",
        help="verbose mode, enable INFO and DEBUG messages.",
        is_flag=True,
    )(func)

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        verbose = kwargs.pop("verbose", False)
        logging.basicConfig(
            level=logging.DEBUG if verbose else logging.WARNING,
            format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        )
        try:
            return func(*args, **kwargs)
        except Exception as err:  # noqa: BLE001
            logger.critical("Unexpected error", exc_info=err)
            logger.critical("Please, report this error to %s.", __issues__)
            sys.exit(1)

    return wrapper


@click.group(
    name="{{ cookiecutter.__cli_name }}",
    help=__summary__,
)
@click.version_option(__version__)
def entrypoint() -> None:
    """Entrypoint for command line interface."""


@entrypoint.command("hello")
@click.option("--name", help="")
@verbosity
def cmd_hello(name: str) -> None:
    """Command for say hello."""
    click.echo(hello(name)){% endif %}
