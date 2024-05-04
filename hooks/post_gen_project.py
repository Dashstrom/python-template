"""Hook run after cookiecutter."""

import json
import os
import pathlib
import shutil
import subprocess
import sys

PROJECT_DIRECTORY = pathlib.Path(os.path.curdir).resolve()
DISABLE_VSCODE = os.environ.get("DISABLE_VSCODE", "no").lower() in ("yes", "y", "1")


def escape(value: str) -> bytes:
    """Minimal but unsafe escaping of string."""
    return json.dumps(value.strip(), ensure_ascii=False).encode("utf-8")


def remove_file(filepath: str) -> None:
    """Remove a file from project."""
    (PROJECT_DIRECTORY / filepath).unlink()


def fatal(text: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {text}", file=sys.stderr, flush=True)
    sys.exit(1)


def run(*args: str) -> None:
    """Run command on computer."""
    print("[RUN]", " ".join(args))
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError:
        fatal("Command failed, exiting")


def autoformat() -> None:
    """Format project."""
    try:
        subprocess.check_call(["poetry", "run", "poe", "pre-commit"])
        print("[FORMAT] formatting done !")
    except subprocess.CalledProcessError:
        print(
            "[FORMAT] This error is expected : "
            "it occurs when `poe pre-commit` run for the first time. "
            "You can ignore it."
        )


def open_vscode() -> None:
    """Open Visual Studio Code."""
    try:
        path = shutil.which("code")
        if path is not None:
            print(f"[RUN] {path} {PROJECT_DIRECTORY}")
            subprocess.check_call([path, str(PROJECT_DIRECTORY)])
        else:
            print("[WARNING] Cannot found Visual Studio Code.")
    except subprocess.CalledProcessError:
        print("[WARNING] Visual Studio Code could not run.")


def main() -> None:
    """Main function for the hook."""
    if "none" == "{{ cookiecutter.cli }}":  # type: ignore
        project = "{{ cookiecutter.__project_slug }}"
        remove_file(os.path.join(project, "cli.py"))
        remove_file(os.path.join(project, "__main__.py"))
        remove_file(os.path.join("tests", "test_cli.py"))
    if "{{ cookiecutter.docker }}" != "True":  # type: ignore
        remove_file("Dockerfile")
        remove_file("docker-compose.yml")
        remove_file(".dockerignore")
    run("git", "init")
    run(
        "git",
        "add",
        "*",
        ".editorconfig",
        ".gitignore",
        ".github/",
        ".pre-commit-config.yaml",
    )
    run("git", "commit", "-m", "[feat] Initial commit")
    run("git", "branch", "-M", "main")
    run(
        "git",
        "remote",
        "add",
        "origin",
        {{cookiecutter.__clone_url | tojson()}},
    )
    run("poetry", "install", "--all-extras", "--no-interaction")
    run("poetry", "run", "poe", "setup")
    autoformat()
    if "{{ cookiecutter.push }}" == "True":  # type: ignore
        run("git", "push", "-uf", "origin", "main")
    if DISABLE_VSCODE:
        print("\n\nYou can activate venv with the following commands :")
        print("\n  cd {{ cookiecutter.__clone_name }}\n  poetry shell\n")
    else:
        open_vscode()


if __name__ == "__main__":
    main()
