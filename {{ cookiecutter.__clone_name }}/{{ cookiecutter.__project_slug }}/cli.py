"""Module for command line interface."""
{%- if "argparse" == cookiecutter.cli %}

import argparse
import logging
import pathlib
import sys
import warnings
from collections.abc import Sequence
from typing import NoReturn, TextIO

from .core import {{ cookiecutter.__project_slug }}
from .info import __issues__, __project__, __summary__, __version__

LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
DEFAULT_ATTRS = logging.LogRecord(
    "dummy",
    logging.CRITICAL,
    "dummy",
    42,
    None,
    None,
    None,
).__dict__.keys()
logger = logging.getLogger(__name__)


class ExtraFormatter(logging.Formatter):  # pragma: no cover
    """Class providing support for context logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format with extra information."""
        extras = set(record.__dict__.keys()) - DEFAULT_ATTRS
        fmt = self._fmt
        if fmt is not None:
            for attr in extras:
                fmt += f" {attr}=%({attr})r"
            self._style._fmt = fmt  # noqa: SLF001
        return super().format(record)


def showwarning(  # pragma: no cover
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    file: TextIO | None = None,  # noqa: ARG001
    line: str | None = None,  # noqa: ARG001
) -> None:
    """Show warning within the logger."""
    for module_name, module in sys.modules.items():  # noqa: B007
        module_path = getattr(module, "__file__", None)
        if module_path and pathlib.Path(module_path).samefile(filename):
            break
    else:
        module_name = pathlib.Path(filename).stem
    msg = f"{category.__name__}: {message}"
    logger = logging.getLogger(module_name)
    try:
        _, _, func, info = logger.findCaller()
    except ValueError:  # pragma: no cover
        func, info = "(unknown function)", None
    record = logger.makeRecord(
        logger.name,
        logging.WARNING,
        filename,
        lineno,
        msg,
        (),
        None,
        func,
        None,
        info,
    )
    logger.handle(record)


class HelpArgumentParser(argparse.ArgumentParser):
    """Parser for show usage on error."""

    def error(self, message: str) -> NoReturn:  # pragma: no cover
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
    run_parser = subparsers.add_parser(
        "run",
        parents=[parent_parser],
        help="Run {{ cookiecutter.__project_slug }}.",
    )
    run_parser.add_argument("path")
    return parser


def setup_logging(*, verbose: bool | None = None) -> None:
    """Do setup logging."""
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.WARNING,
        format="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
    )
    warnings.showwarning = showwarning
    for handler in logging.root.handlers:
        handler.setFormatter(ExtraFormatter(handler.formatter._fmt))  # type: ignore[union-attr]  # noqa: SLF001


def entrypoint(argv: Sequence[str] | None = None) -> None:
    """Entrypoint for command line interface."""
    try:
        parser = get_parser()
        args = parser.parse_args(argv)
        setup_logging(verbose=args.verbose)
        if args.action == "run":
            print({{ cookiecutter.__project_slug }}(args.path))  # noqa: T201
        else:  # pragma: no cover
            parser.error("No command specified")
    except Exception as err:  # NoQA: BLE001  # pragma: no cover
        logger.critical(
            "Unexpected error (%s, version %s)",
            __project__,
            __version__,
            exc_info=err,
        )
        logger.critical("Please, report this error to %s.", __issues__)
        sys.exit(1){% elif "click" == cookiecutter.cli %}

import logging
import pathlib
import sys
import warnings
from collections.abc import Callable
from functools import wraps
from typing import TextIO, TypeVar

import click
from typing_extensions import ParamSpec

from .core import {{ cookiecutter.__project_slug }}
from .info import __issues__, __project__, __summary__, __version__

logger = logging.getLogger(__name__)
LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
DEFAULT_ATTRS = logging.LogRecord(
    "dummy",
    logging.CRITICAL,
    "dummy",
    42,
    None,
    None,
    None,
).__dict__.keys()

P = ParamSpec("P")
T = TypeVar("T")


class ExtraFormatter(logging.Formatter):  # pragma: no cover
    """Class providing support for context logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format with extra information."""
        extras = set(record.__dict__.keys()) - DEFAULT_ATTRS
        fmt = self._fmt
        if fmt is not None:
            for attr in extras:
                fmt += f" {attr}=%({attr})r"
            self._style._fmt = fmt  # noqa: SLF001
        return super().format(record)


def showwarning(  # pragma: no cover
    message: Warning | str,
    category: type[Warning],
    filename: str,
    lineno: int,
    file: TextIO | None = None,  # noqa: ARG001
    line: str | None = None,  # noqa: ARG001
) -> None:
    """Show warning within the logger."""
    for module_name, module in sys.modules.items():  # noqa: B007
        module_path = getattr(module, "__file__", None)
        if module_path and pathlib.Path(module_path).samefile(filename):
            break
    else:
        module_name = pathlib.Path(filename).stem
    msg = f"{category.__name__}: {message}"
    logger = logging.getLogger(module_name)
    try:
        _, _, func, info = logger.findCaller()
    except ValueError:  # pragma: no cover
        func, info = "(unknown function)", None
    record = logger.makeRecord(
        logger.name,
        logging.WARNING,
        filename,
        lineno,
        msg,
        (),
        None,
        func,
        None,
        info,
    )
    logger.handle(record)


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
        warnings.showwarning = showwarning
        for handler in logging.root.handlers:
            handler.setFormatter(ExtraFormatter(handler.formatter._fmt))  # type: ignore[union-attr]  # noqa: SLF001
        try:
            return func(*args, **kwargs)
        except Exception as err:  # noqa: BLE001  # pragma: no cover
            logger.critical(
                "Unexpected error (%s, version %s)",
                __project__,
                __version__,
                exc_info=err,
            )
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


@entrypoint.command("run")
@click.argument("path")
@verbosity
def cmd_hello(path: str) -> None:
    """Command for say hello."""
    click.echo({{ cookiecutter.__project_slug }}(path)){% endif %}
