from contextlib import suppress
import json
import pathlib
import re
from typing import Iterable, Match, Tuple
from urllib.request import urlopen

ROOT = pathlib.Path(__file__).parent.parent
RE_DEPENDENCIES = re.compile(
    r"(?P<p1>(?P<package>[a-zA-Z0-9_\-]+)\s*=\s*.*"
    r"version\s*=\s*\")(?P<version>[^\"]+)(?P<p2>\".*"
    r"optional\s*=\s*true.*)"
)
RE_PRE_COMMIT = re.compile(
    r"(?P<p1>repo\s*:\s*)(?P<repo>.+)(?P<p2>\s+rev\s*:\s*)(?P<rev>.+)"
)
PROJECT = ROOT / "{{ cookiecutter.__clone_name }}"
PYPROJECT = PROJECT / "pyproject.toml"
PRE_COMMIT = PROJECT / ".pre-commit-config.yaml"
MAX = {
    "sphinx": "7.1.2",
    "pre-commit": "3.5.0",
    "pytest-cov": "5.0.0",
    "poethepoet": "0.30.0",
    "commitizen": "3.31.0",
    "coverage": "7.6.1",
}


def latest(versions: Iterable[str]) -> Tuple[int, ...]:
    releases = []
    for version in versions:
        with suppress(ValueError):
            release = tuple(map(int, version.split(".")))
            releases.append(release)
    return ".".join(map(str, sorted(releases)[-1]))


def update_dependencies() -> None:
    def mapper(m: Match[str]) -> str:
        try:
            version = MAX[m["package"]]
        except KeyError:
            with urlopen(
                f"https://pypi.org/pypi/{m['package']}/json",
                timeout=10,
            ) as f:
                obj = json.loads(f.read())
            version = latest(obj["releases"])
        icon = "[+]" if m["version"] != version else "[=]"
        print(icon, m["package"], m["version"], "->", version)
        return m["p1"] + version + m["p2"]

    print("Update dependencies")
    config = RE_DEPENDENCIES.sub(mapper, PYPROJECT.read_text())
    PYPROJECT.write_text(config)


def update_pre_commit() -> None:
    def mapper(m: Match[str]) -> str:
        author, project = m["repo"].split("/")[-2:]
        with urlopen(
            f"https://api.github.com/repos/{author}/{project}/tags",
            timeout=10,
        ) as f:
            obj = json.loads(f.read())
        rev = f"v{latest([tag['name'].lstrip('v') for tag in obj])}"
        icon = "[+]" if m["rev"] != rev else "[=]"
        print(icon, m["repo"], m["rev"], "->", rev)
        return m["p1"] + m["repo"] + m["p2"] + rev

    print("Update pre-commit")
    config = RE_PRE_COMMIT.sub(mapper, PRE_COMMIT.read_text())
    PRE_COMMIT.write_text(config)


if __name__ == "__main__":
    update_dependencies()
    print()
    update_pre_commit()
