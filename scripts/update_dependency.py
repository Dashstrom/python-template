import pathlib
import re
import subprocess
from typing import Match


ROOT = pathlib.Path(__file__).parent.parent
RE = re.compile(
    r"(?P<p1>(?P<package>[a-zA-Z0-9_\-]+)\s*=\s*.*"
    r"version\s*=\s*\")(?P<version>[^\"]+)(?P<p2>\".*"
    r"optional\s*=\s*true.*)"
)
PYPROJECT = ROOT / "{{ cookiecutter.__clone_name }}" / "pyproject.toml"
MAX = {"sphinx": "7.1.2"}


def update_dependency() -> None:
    def mapper(m: Match[str]) -> str:
        result = subprocess.check_output(
            (
                "pip",
                "index",
                "versions",
                m["package"],
            ),
            stderr=subprocess.PIPE,
        )
        try:
            version = MAX[m["package"]]
        except KeyError:
            version = (
                result.split(b"\n")[0].strip().split(b" ")[1][1:-1].decode()
            )
        print(m["package"], m["version"], "=>", version)
        return m["p1"] + version + m["p2"]

    config = RE.sub(mapper, PYPROJECT.read_text())
    PYPROJECT.write_text(config)


if __name__ == "__main__":
    update_dependency()
