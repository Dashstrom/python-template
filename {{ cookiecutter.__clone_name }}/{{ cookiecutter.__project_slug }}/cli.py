"""Module for command line interface."""
{%- if "argparse" == cookiecutter.cli %}

import argparse
import logging
import sys
from typing import NoReturn, Optional, Sequence

from .core import METADATA, hello

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
        description=METADATA["Summary"],
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s, version {METADATA['Version']}",
    )
    parser.add_argument(
        "--log-level",
        metavar="level",
        default="INFO",
        choices=LOG_LEVELS,
        help="minimum level of log messages, possible choices: %(choices)s",
    )
    parser.add_argument(
        "--log-file",
        metavar="file",
        help="log file to store DEBUG level messages",
    )
    hello_subparser = parser.add_subparsers(dest="command_hello")
    hello_parser = hello_subparser.add_parser("hello")
    hello_parser.add_argument(
        "--name",
        help="name to greeting",
    )
    return parser


def setup_logging(
    log_file: Optional[str] = None,
    log_level: Optional[str] = None,
) -> None:
    """Do setup logging to redirect to log_file at DEBUG level."""
    if log_level is None:
        log_level = "INFO"
    # Setup logging
    if log_file:
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)-8s - %(name)s - %(message)s",
            filename=log_file,
            filemode="w",
        )
        console = logging.StreamHandler()
        console.setLevel(log_level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)-8s - %(message)s",
        )
        console.setFormatter(formatter)
        logging.root.addHandler(console)
    else:
        logging.basicConfig(
            level=log_level,
            format="[%(asctime)s] %(levelname)-8s - %(message)s",
        )


def entrypoint(argv: Optional[Sequence[str]] = None) -> None:
    """Entrypoint for command line interface."""
    try:
        parser = get_parser()
        args = parser.parse_args(argv)
        setup_logging(args.log_file, args.log_level)
        if args.command_hello:
            logging.getLogger(__name__).info(hello(args.name))
        else:
            parser.error("No command specified")
    except Exception as err:  # NoQA: BLE001
        logger.critical("Unexpected error", stack_info=True, exc_info=err)
        logger.critical("Please, report this error.")
        sys.exit(1){% elif "click" == cookiecutter.cli %}

import logging
from typing import Optional

import click

from .core import METADATA, hello

LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]


@click.group(
    name="{{ cookiecutter.__cli_name }}",
    help=METADATA["Summary"],
)
@click.version_option(METADATA["Version"])
@click.option(
    "--log-level",
    metavar="level",
    type=click.Choice(LOG_LEVELS),
    default="INFO",
    show_default=True,
    help="Minimum level of log messages",
)
@click.option(
    "--log-file",
    help="Log file to store DEBUG level messages",
    metavar="file",
)
def entrypoint(log_level: str, log_file: Optional[str]) -> None:
    """Entrypoint for command line interface."""
    if log_file:
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)-8s - %(name)s - %(message)s",
            filename=log_file,
            filemode="w",
        )
        console = logging.StreamHandler()
        console.setLevel(log_level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)-8s - %(message)s",
        )
        console.setFormatter(formatter)
        logging.root.addHandler(console)
    else:
        logging.basicConfig(
            level=log_level,
            format="[%(asctime)s] %(levelname)-8s - %(message)s",
        )


@entrypoint.command("hello")
@click.option("--name", help="")
def cmd_hello(name: str) -> None:
    """Command for say hello."""
    click.echo(hello(name)){% endif %}
