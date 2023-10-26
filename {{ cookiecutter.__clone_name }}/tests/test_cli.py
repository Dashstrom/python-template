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
    import {{ cookiecutter.__project_slug }}.__main__  # NoQA: F401


def test_hello(caplog: pytest.LogCaptureFixture) -> None:
    """Test command hello."""
    name = "A super secret name"
    entrypoint(("hello", "--name", name))
    assert name in caplog.text
{%- elif "click" == cookiecutter.cli %}

import os
import subprocess
import sys

from click.testing import CliRunner

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
    runner = CliRunner()
    result = runner.invoke(entrypoint, ["--version"])
    out = result.output
    assert "version" in out


def test_import() -> None:
    """Test if module entrypoint has correct imports."""
    import {{ cookiecutter.__project_slug }}.__main__  # noqa: F401


def test_hello() -> None:
    """Test command hello."""
    name = "A super secret name"
    runner = CliRunner()
    result = runner.invoke(entrypoint, ["hello", "--name", name])
    assert name in result.output{% endif %}
