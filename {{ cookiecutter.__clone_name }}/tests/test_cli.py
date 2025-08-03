"""Test for command line interface."""
{%- if "argparse" == cookiecutter.cli %}

import contextlib
import io
import os
import subprocess
import sys

import pytest

from {{ cookiecutter.__project_slug }} import entrypoint


def test_cli_version() -> None:
    """Test if the command line interface is installed correctly."""
    name = "{{ cookiecutter.__cli_name }}"
    env = os.environ.get("VIRTUAL_ENV", "")
    if env:
        if os.name == "nt":
            exe = f"{env}\\\\Scripts\\\\{name}.cmd"
            if not os.path.exists(exe):  # noqa: PTH110
                exe = f"{env}\\\\Scripts\\\\{name}.exe"
        else:
            exe = f"{env}/bin/{name}"
    else:
        exe = name
    out = subprocess.check_output((exe, "--version"), text=True, shell=False)
    assert "version" in out
    out = subprocess.check_output(
        (
            sys.executable,
            "-m",
            "{{ cookiecutter.__project_slug }}",
            "--version",
        ),
        text=True,
        shell=False,
    )
    assert "version" in out
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout), pytest.raises(SystemExit):
        entrypoint(("--version",))
    assert "version" in stdout.getvalue()


def test_import() -> None:
    """Test if module entrypoint has correct imports."""
    import {{ cookiecutter.__project_slug }}.__main__  # noqa: PLC0415, F401


def test_{{ cookiecutter.__project_slug }}_cli() -> None:
    """Test command {{ cookiecutter.__project_slug }}."""
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        entrypoint(("run", "random-path"))
    assert stdout.getvalue() == "False\n"
{%- elif "click" == cookiecutter.cli %}

import os
import subprocess
import sys
from functools import cache

from click.testing import CliRunner

from {{ cookiecutter.__project_slug }} import entrypoint


@cache
def is_click_legacy() -> bool:
    try:
        CliRunner(mix_stderr=False)  # type: ignore[call-arg,unused-ignore]
    except TypeError:
        return False
    return True


def test_cli_version() -> None:
    """Test if the command line interface is installed correctly."""
    name = "{{ cookiecutter.__cli_name }}"
    env = os.environ.get("VIRTUAL_ENV", "")
    if env:
        if os.name == "nt":
            exe = f"{env}\\\\Scripts\\\\{name}.cmd"
            if not os.path.exists(exe):  # noqa: PTH110
                exe = f"{env}\\\\Scripts\\\\{name}.exe"
        else:
            exe = f"{env}/bin/{name}"
    else:
        exe = name
    out = subprocess.check_output((exe, "--version"), text=True, shell=False)
    assert "version" in out
    out = subprocess.check_output(
        (
            sys.executable,
            "-m",
            "{{ cookiecutter.__project_slug }}",
            "--version",
        ),
        text=True,
        shell=False,
    )
    assert "version" in out
    # https://click.palletsprojects.com/en/stable/api/#click.testing.CliRunner
    if is_click_legacy():
        runner = CliRunner(mix_stderr=False)  # type: ignore[call-arg,unused-ignore]
    else:
        runner = CliRunner(catch_exceptions=False)  # type: ignore[call-arg,unused-ignore]
    result = runner.invoke(entrypoint, ["--version"])
    out = result.output
    assert "version" in out


def test_import() -> None:
    """Test if module entrypoint has correct imports."""
    import {{ cookiecutter.__project_slug }}.__main__  # noqa: PLC0415, F401


def test_{{ cookiecutter.__project_slug }}_cli() -> None:
    """Test command {{ cookiecutter.__project_slug }}."""
    runner = CliRunner()
    result = runner.invoke(entrypoint, ("run", "random-path"))
    assert result.output == "False\n"{% endif %}
