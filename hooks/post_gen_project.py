"""Hook run after cookiecutter."""
import json
import os
import pathlib
import subprocess
import sys

PROJECT_DIRECTORY = pathlib.Path(os.path.curdir).resolve()


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
        " --update",
        "*",
        ".editorconfig",
        ".gitignore",
        ".github/",
        ".pre-commit-config.yaml",
    )
    run("git", "commit", "-m", "Initial commit")
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
    print("\n\nYou can activate venv with the following commands :")
    print("\n  cd {{ cookiecutter.__clone_name }}\n  poetry shell\n")


if __name__ == "__main__":
    main()
