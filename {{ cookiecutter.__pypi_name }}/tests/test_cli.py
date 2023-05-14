"""Base module for testing command line interface."""{% if cookiecutter.cli|lower == 'argparse' %}
import contextlib
import io
import subprocess
import sys

import pytest

from {{ cookiecutter.__project_slug }} import __version__, entrypoint


def test_cli() -> None:
    """Basic test for command line interface."""
    out = subprocess.check_output(
        [
            "{{ cookiecutter.__cli_name }}",
            "--version"
        ],
        text=True,
        shell=False,
    )
    assert __version__ in out.strip()
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "{{ cookiecutter.__project_slug }}",
            "--version",
        ],
        text=True,
        shell=False,
    )
    assert __version__ in out.strip()
    stdout = io.StringIO()
    stderr = io.StringIO()
    with (
        contextlib.redirect_stderr(stderr),
        contextlib.redirect_stdout(stdout),
        pytest.raises(SystemExit),
    ):
        entrypoint(["--version"])
    out = stdout.getvalue() + stderr.getvalue()
    assert __version__ in out.strip()


def test_import() -> None:
    """Test if module entrypoint has correct imports."""
    import {{ cookiecutter.__project_slug }}.__main__  # noqa: F401


def test_hello(capsys: pytest.CaptureFixture[str]) -> None:
    """Test command hello."""
    name = "uizuifruzbfbwsf"
    with pytest.raises(SystemExit):
        entrypoint(("hello", "--name", name))
    captured = capsys.readouterr()
    assert name in captured.out{% elif cookiecutter.cli|lower == 'click' %}
import subprocess
import sys

import click.testing

from {{ cookiecutter.__project_slug }} import __version__, entrypoint


def test_cli() -> None:
    """Basic test for command line interface."""
    ver = f"version {__version__}"
    out = subprocess.check_output(
        [
            "{{ cookiecutter.__cli_name }}",
            "--version"
        ],
        text=True,
        shell=False,
    )
    assert ver in out
    out = subprocess.check_output(
        [
            sys.executable,
            "-m",
            "{{ cookiecutter.__project_slug }}",
            "--version",
        ],
        text=True,
        shell=False,
    )
    assert ver in out
    runner = click.testing.CliRunner()
    result = runner.invoke(entrypoint, ["--version"])
    out = result.output
    assert ver in out


def test_import() -> None:
    """Test if module entrypoint has correct imports."""
    import {{ cookiecutter.__project_slug }}.__main__  # noqa: F401


def test_hello() -> None:
    """Test command hello."""
    name = "uizuifruzbfbwsf"
    runner = click.testing.CliRunner()
    result = runner.invoke(entrypoint, ["hello", "--name", name])
    assert name in result.output{% endif %}
