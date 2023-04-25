"""Base module for testing command line interface."""{% if cookiecutter.cli|lower == 'argparse' %}
import contextlib
import io
import subprocess
import sys

from {{ cookiecutter.__project_slug }} import cli, __version__


def test_cli() -> None:
    """Basic test for command line interface."""
    out = subprocess.check_output(
        ["{{ cookiecutter.__pypi_name }}", "--version"],
        text=True,
        shell=False,
    )
    assert out.strip() == __version__
    out = subprocess.check_output(
        [sys.executable, "-m", "{{ cookiecutter.__pypi_name }}", "--version"],
        text=True,
        shell=False,
    )
    assert out.strip() == __version__
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(stdout):
        cli(["--version"])
    out = stdout.getvalue() + stderr.getvalue()
    assert out.strip() == __version__{% elif cookiecutter.cli|lower == 'click' %}
import subprocess
import sys

import click.testing

from {{ cookiecutter.__project_slug }} import __version__, cli


def test_cli() -> None:
    """Basic test for command line interface."""
    ver = f"version {__version__}"
    out = subprocess.check_output(
        ["{{ cookiecutter.__pypi_name }}", "--version"],
        text=True,
        shell=False,
    )
    assert ver in out
    out = subprocess.check_output(
        [sys.executable, "-m", "{{ cookiecutter.__pypi_name }}", "--version"],
        text=True,
        shell=False,
    )
    assert ver in out
    runner = click.testing.CliRunner()
    result = runner.invoke(cli, ["--version"])
    out = result.output
    assert ver in out{% endif %}
