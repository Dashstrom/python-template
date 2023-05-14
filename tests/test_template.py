"""Test for template."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
from time import sleep
from typing import Optional, Union

HERE = pathlib.Path(__file__).parent
TEMPLATE_PATH = HERE.parent
CACHE = TEMPLATE_PATH / ".cache" / "tests"
DEFAULT_CONFIG = {
    "full_name": "Dashstrom",
    "email": "dashstrom.pro@gmail.com",
    "github_username": "Dashstrom",
    "project_name": None,
    "project_short_description": "Hola project",
    "discord": "no",
    "version": "0.0.1",
    "cli": "click",
    "license": "GNU GPL v3.0",
    "pypi": True,
    "git": True,
    "push": False,
    "docker": False,
}

CONFIGS = [
    {"project_name": "aaa-aaa", "cli": "none"},
    {
        "project_name": "aaa-aaa",
        "project_short_description": '"; import sys;sys.exit(1)',
    },
    {"project_name": "aaa"},
    {"project_name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    {"project_name": "aaa-aaa", "cli": "argparse"},
    {"project_name": "aaa-aaa"},
    {"project_name": "zzz-zzz"},
    {"project_name": "aaa-aaa", "pypi": False},
    {"project_name": "aaa-aaa", "git": False},
    {"project_name": "aaa-aaa", "setup": False},
    {"project_name": "aaa-aaa", "license": "MIT"},
    {
        "project_name": "aaa-aaa",
        "license": "All Rights Reserved",
        "pypi": False,
    },
]


def fatal(text: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {text}", file=sys.stderr, flush=True)
    input("Error ...")
    sys.exit(1)


def run(*cmd: str, cwd: Optional[Union[pathlib.Path, str]] = None) -> None:
    """Run test command"""
    print(f"[TEST RUN] {' '.join(cmd)} in {cwd}")
    try:
        subprocess.check_call(
            cmd, shell=False, stdout=sys.stdout, cwd=str(cwd)
        )
    except subprocess.CalledProcessError:
        fatal("Exit code is not zero")


def test_config() -> None:
    """Test for configs."""
    shutil.rmtree(CACHE, ignore_errors=True)
    CACHE.mkdir(exist_ok=True, parents=True)
    for config in CONFIGS:
        repr_config = json.dumps(config, indent=2)
        config = {**DEFAULT_CONFIG, **config}  # type: ignore[call-overload]
        with tempfile.TemporaryDirectory(
            prefix="template-python-", dir=CACHE
        ) as tmp:
            try:
                print(f"\n\nWorking at {tmp} with config: \n{repr_config}\n\n")
                sleep(3)
                run(
                    "cookiecutter",
                    "-v",
                    "--no-input",
                    str(TEMPLATE_PATH),
                    *[f"{key}={value}" for key, value in config.items()],
                    cwd=tmp,
                )
                pypi_name: str = (
                    config["project_name"]  # type: ignore[union-attr]
                    .lower()
                    .replace(" ", "-")
                    .replace("-", "-")
                )
                project = pathlib.Path(tmp) / pypi_name

                run("make", "tests-all", cwd=project)
                run("make", "format", cwd=project)
                run("make", "cov", cwd=project)
            except KeyboardInterrupt:
                print("Interrupted !")
            finally:
                sleep(3)


if __name__ == "__main__":
    test_config()
