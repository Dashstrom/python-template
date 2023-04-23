"""Python scripts that run before your project is generated."""
import re
import sys


def fatal(text: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {text}", file=sys.stderr, flush=True)
    sys.exit(1)


def match(pattern: str, name: str, value: str) -> None:
    """Match field."""
    if not re.match(pattern, value) or 1 > len(value) or len(value) >= 256:
        fatal(f"{name} ({value}) doesn't match {pattern!r} !")


def check_names() -> None:
    """Check variables from cookiecutter."""
    match(
        r"^[ _a-zA-Z-][ _a-zA-Z0-9-]+$",
        "project_name",
        "{{ cookiecutter.project_name }}",
    )
    match(
        r"^[_a-zA-Z][_a-zA-Z0-9]+$",
        "project_slug",
        "{{ cookiecutter.__project_slug }}",
    )


def check_compatibilities() -> None:
    """Check compatibilities between variables."""
    if (
        "{{ cookiecutter.license }}" == "All Rights Reserved"
        and "{{ cookiecutter.pypi }}" == "yes"
    ):
        fatal("All Rights Reserved is not compatible with PyPI")
    if "dashstrom/template-python" in "{{ cookiecutter.__clone_url }}":
        fatal("You are trying to erase original project")


def main() -> None:
    """Main function."""
    check_names()
    check_compatibilities()


if __name__ == "__main__":
    main()
