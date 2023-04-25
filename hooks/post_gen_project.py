"""Python scripts that run after your project is generated."""
import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).parent.resolve()
PROJECT = REPO / "{{ cookiecutter.__pypi_name }}"

REMOVED_IF_FALSE = {
    "{{ cookiecutter.docker }}": [
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
    ],
    "{{ cookiecutter.cli }}": [
        "{{ cookiecutter.__project_slug }}/cli.py",
        "{{ cookiecutter.__project_slug }}/__main__.py",
        "tests/test_cli.py",
    ],
}


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


def remove_paths() -> None:
    """Remove paths."""
    for pred, paths in REMOVED_IF_FALSE.items():
        for path in paths:
            if pred.lower().strip() in (
                "no",
                "false",
                "n",
                "non",
                "0",
                "none",
                "",
            ):
                abspath = pathlib.Path(path).resolve()
                abspath.unlink()


def git() -> None:
    """Instansiate Git repository."""
    if "{{ cookiecutter.git }}" == "True":
        run("git", "init")
        run("git", "add", "*")
        run("git", "commit", "-m", "Initial commit")
        run("git", "branch", "-M", "main")
        run("git", "remote", "add", "origin", "{{ cookiecutter.__clone_url }}")
        # run("git", "push", "-u", "origin", "main")


def setup() -> None:
    """Setup virtual environnement and pre-commit."""
    if "{{ cookiecutter.setup }}" == "True":
        run("make", "setup")


def main() -> None:
    """Main function."""
    remove_paths()
    git()
    setup()


if __name__ == "__main__":
    main()
