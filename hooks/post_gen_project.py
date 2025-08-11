"""Hook run after cookiecutter."""  # noqa: INP001

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

cookiecutter: Any = object()
tojson: Any = object()

PROJECT_DIRECTORY = Path(os.path.curdir).resolve()
DISABLE_VSCODE = os.environ.get("DISABLE_VSCODE", "no").lower() in ("yes", "y", "1")
PYTHON_TEMPLATE_FAST = os.environ.get("PYTHON_TEMPLATE_FAST", "n").lower() in (
    "yes",
    "y",
    "1",
)


def escape(value: str) -> bytes:
    """Minimal but unsafe escaping of string."""
    return json.dumps(value.strip(), ensure_ascii=False).encode("utf-8")


def fatal(text: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {text}", file=sys.stderr, flush=True)  # noqa: T201
    sys.exit(1)


def remove_file(filepath: str | Path) -> None:
    """Remove a file from project."""
    (PROJECT_DIRECTORY / filepath).unlink()


def run(*args: str) -> None:
    """Run command on computer."""
    print("[RUN]", " ".join(args))  # noqa: T201
    try:
        subprocess.check_call(args)  # noqa: S603
    except subprocess.CalledProcessError:
        fatal("Command failed, exiting")


def autoformat() -> None:
    """Format project."""
    args = ["uv", "run", "poe", "pre-commit"]
    print("[RUN]", " ".join(args))  # noqa: T201
    try:
        subprocess.check_call(args)  # noqa: S603
        print("[FORMAT] formatting done !")  # noqa: T201
    except subprocess.CalledProcessError:
        print(  # noqa: T201
            "[FORMAT] This error is expected : "
            "it occurs when `poe pre-commit` run for the first time. "
            "You can ignore it.",
        )
        git_add()
    try:
        args = ["uv", "run", "poe", "format"]
        print("[RUN]", " ".join(args))  # noqa: T201
        subprocess.check_call(args)  # noqa: S603
    except subprocess.CalledProcessError:
        print(  # noqa: T201
            "[FORMAT] This error is expected : "
            "it occurs when `poe format` run for the first time."
            "You can ignore it.",
        )
        git_add()


def git_add() -> None:
    """Add all files to git."""
    run(
        "git",
        "add",
        "*",
        ".gitignore",
        ".github/",
        ".pre-commit-config.yaml",
    )


def run_tests() -> None:
    """Run all test."""
    run("uv", "run", "poe", "check")
    print("[TEST] All tests are successful")  # noqa: T201


def open_vscode() -> None:
    """Open Visual Studio Code."""
    try:
        path = shutil.which("code")
        if path is not None:
            print(f"[RUN] {path} {PROJECT_DIRECTORY}")  # noqa: T201
            subprocess.check_call([path, str(PROJECT_DIRECTORY)])  # noqa: S603
        else:
            print("[WARNING] Cannot found Visual Studio Code.")  # noqa: T201
    except subprocess.CalledProcessError:
        print("[WARNING] Visual Studio Code could not run.")  # noqa: T201


def main() -> None:
    """Run after project initialisation."""
    if "none" == "{{ cookiecutter.cli }}":  # noqa: PLR0133
        project = "{{ cookiecutter.__project_slug }}"
        remove_file(Path(project) / "cli.py")
        remove_file(Path(project) / "__main__.py")
        remove_file("tests/test_cli.py")
    if "{{ cookiecutter.docker }}" != "True":  # noqa: PLR0133
        remove_file("Dockerfile")
        remove_file("docker-compose.yml")
        remove_file(".dockerignore")
    if not PYTHON_TEMPLATE_FAST:
        run("git", "init")
        run("uv", "sync")
        run("uv", "run", "poe", "setup")
        git_add()
        autoformat()
        run("git", "commit", "-m", "feat: Initial commit")
        run("git", "branch", "-M", "main")
        run(
            "git",
            "remote",
            "add",
            "origin",
            {{cookiecutter.__clone_url | tojson()}},  # noqa: SLF001
        )
        run_tests()
        if "{{ cookiecutter.push }}" == "True":  # noqa: PLR0133
            run("git", "push", "-uf", "origin", "main")
        if DISABLE_VSCODE:
            print(
                "\n\nYou can activate venv with the following commands :"
            )  # noqa: T201
            print("\n  cd {{ cookiecutter.__clone_name }}\n\n")  # noqa: T201
        else:
            open_vscode()


if __name__ == "__main__":
    main()
