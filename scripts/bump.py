"""Script for bump version."""

from contextlib import suppress
from functools import cache
import json
from operator import eq, ge, gt, le, ne, lt
import pathlib
import re
from typing import Match
from urllib.request import Request, urlopen

# Cache
MAX: dict[str, str] = {}

# Operators used
OPERATORS = {">=": ge, "==": eq, "<=": le, "!=": ne, ">": gt, "<": lt}

# Regex
RE_DEPENDENCIES = re.compile(
    r"(?P<package>[a-zA-Z0-9\-\_\[\]]+)==(?P<version>[0-9\.]+)"
)
RE_PYTHON_VERSION = re.compile(
    r"python_version\s*=\s*(?P<version>[\"']?[0-9\.]+[\"']?)"
)
RE_VERSION = re.compile(
    rf"(?P<op>{'|'.join(re.escape(k) for k in OPERATORS)})\s*(?P<version>[\d\.]+)"
)

# Paths
ROOT = pathlib.Path(__file__).parent.parent
PROJECT = ROOT / "{{ cookiecutter.__clone_name }}"
PROJECT_PYPROJECT = PROJECT / "pyproject.toml"


@cache
def get_pyproject_version() -> str:
    match = RE_PYTHON_VERSION.search(PROJECT_PYPROJECT.read_text("utf-8"))
    if match is None:
        err = "Python version cannot be resolved from pyproject.toml"
        raise ValueError(err)
    return match["version"].strip('"')


def parse_stable_version(version: str) -> tuple[int, ...]:
    """Parse stable version like 'X.Y.Z'."""
    return tuple(map(int, version.split(".")))


def match_requires(
    requires_python: str | None,
    python_version: str,
) -> bool:
    """Check if a requirement match a version."""
    parsed_python_version = parse_stable_version(python_version)
    # Check require_python is None
    if isinstance(requires_python, str):
        # Iterate over all constrains
        for req in requires_python.split(","):
            # Parse the contraint (and ignore it overwise)
            if m := RE_VERSION.search(req):
                # Resolve and parse values
                op = OPERATORS[m.group("op").strip()]
                value = parse_stable_version(m.group("version").strip())
                # Compare value
                if not op(parsed_python_version, value):
                    return False
    return True


@cache
def get_highest_version(package: str, python_version: str) -> str:
    """Get the highest compatible version for a package."""

    # Get all information on the package from pypi
    req = Request(url=f"https://pypi.org/pypi/{package}/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "Github: Dashstrom/python-template/scripts/bump.py")
    with urlopen(req, timeout=1) as resp:
        content = json.load(resp)

    # Order stable versions
    versions = []
    none_versions = []
    for release in reversed(content["releases"]):
        with suppress(ValueError):
            constraints = tuple(
                {
                    file["requires_python"]
                    for file in content["releases"][release]
                    if file["requires_python"]
                }
            )
            if not constraints:
                none_versions.append(parse_stable_version(release))
            elif all(
                match_requires(constrain, python_version) for constrain in constraints
            ):
                versions.append(parse_stable_version(release))
    versions.sort()
    none_versions.sort()

    if versions:
        return ".".join(map(str, versions[-1]))
    if none_versions:
        return ".".join(map(str, none_versions[-1]))

    # If no version found, raise a warning
    err = f"No match for package {package} with version {python_version}"
    raise ValueError(err)


def update_dependencies(path: pathlib.Path) -> None:
    python_version = get_pyproject_version()

    def mapper(m: Match[str]) -> str:
        # Print a waiting line
        print("[.]", m["package"], m["version"], "->", "...", end="\r")
        name = m["package"].split("[")[0]
        if name in MAX:
            version = MAX[name]
        else:
            # Resolve the highest version working with the python version
            version = get_highest_version(name, python_version)
        # print the information about the modification
        icon = "[+]" if m["version"] != version else "[=]"
        print(icon, m["package"], m["version"], "->", version)
        return f'{m["package"]}=={version}'

    print(f"Update {path}")
    config = RE_DEPENDENCIES.sub(mapper, path.read_text())
    path.write_text(config)


def update_all() -> None:
    python_version = get_pyproject_version()
    print(f"Python version: {python_version}")
    update_dependencies(PROJECT_PYPROJECT)


if __name__ == "__main__":
    update_all()
