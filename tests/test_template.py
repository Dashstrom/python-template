"""Test for template."""
import argparse
import json
import pathlib
from shlex import quote
import shutil
import subprocess
import sys
import tempfile
import os
from time import sleep
from typing import List, Optional, Union

HERE = pathlib.Path(__file__).parent
TEMPLATE_PATH = HERE.parent.resolve()
CACHE = TEMPLATE_PATH / ".cache" / "tests"
DEFAULT_CONFIG = {
    "full_name": "Dashstrom",
    "email": "dashstrom.pro@gmail.com",
    "github_username": "Dashstrom",
    "project_name": "aaa-aaa",
    "project_short_description": "iozerjfiezifbzef",
    "project_url": "https://github/Dashstrom/aaa-aaa",
    "version": "0.0.1",
    "cli": "argparse",
    "license": "LGPL2.1+",
    "push": False,
    "strict_lint": False,
    "docker": False,
    "line": 79,
    "fail": False,
}
USE_FORMATER = os.environ.get("USE_FORMATER", "True").lower() not in (
    "false",
    "",
    "off",
    "0",
)
CONFIGS = [
    {
        "project_short_description": '"; import sys;sys.exit(1)',
    },
    {"cli": "click"},
    {
        "project_short_description": "a b c èé" * 20,
    },
    {
        "project_name": '"; import sys;sys.exit(1)',
        "fail": True,
    },
    {"project_name": "aaa"},
    {"project_name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    {"project_name": "zzz-zzz"},
    {"cli": "none"},
    {"license": "MIT"},
    {"license": "All Rights Reserved"},
    {"strict_lint": True},
    {"docker": True},
    {"line": 120},
    {"cli": "click", "line": 120},
    {"discord": "blabla"},
]


def error(text: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {text}", file=sys.stderr, flush=True)
    raise OSError("Invalid return")


def fatal(text: str) -> None:
    """Print error and exit."""
    try:
        error(text)
    except OSError:
        if sys.stdin.isatty():
            input("Press enter for clean up")
        sys.exit(1)


def run(*cmd: str, cwd: Optional[Union[pathlib.Path, str]] = None) -> None:
    """Run test command"""
    print(f"[TEST RUN] {' '.join(quote(arg) for arg in cmd)} in {cwd}")
    try:
        subprocess.check_call(
            cmd,
            shell=False,
            stdout=sys.stderr,
            stderr=sys.stderr,
            cwd=str(cwd),
        )
    except subprocess.CalledProcessError:
        error("Exit code is not zero")


def test_config(*, indexes: Optional[List[int]] = None) -> None:
    """Test for configs."""
    shutil.rmtree(CACHE, ignore_errors=True)
    CACHE.mkdir(exist_ok=True, parents=True)
    if indexes is None:
        configs = CONFIGS
    else:
        configs = [config for i, config in enumerate(CONFIGS) if i in indexes]

    for config in configs:
        repr_config = json.dumps(config, indent=2)
        config = {**DEFAULT_CONFIG, **config}  # type: ignore[call-overload]
        should_fail = config.pop("fail", False)
        with tempfile.TemporaryDirectory(
            prefix="python-template-", dir=CACHE
        ) as tmp:
            try:
                print(f"\n\nWorking at {tmp} with config: \n{repr_config}\n\n")
                if sys.stdout.isatty():
                    sleep(3)
                run(
                    "cookiecutter",
                    "-v",
                    "--no-input",
                    str(TEMPLATE_PATH),
                    *[f"{key}={value}" for key, value in config.items()],
                    cwd=tmp,
                )
                project_url: str = config["project_url"]  # type: ignore[assignment]
                clone_name: str = project_url.split("/")[-1]
                project = pathlib.Path(tmp) / clone_name

                run("make", "tests-all", cwd=project)
                if USE_FORMATER:
                    run("make", "format", cwd=project)
                run("make", "cov", cwd=project)
                if should_fail:
                    fatal("Test should fail")
            except KeyboardInterrupt:
                print("Interrupted !")
                break
            except OSError:
                if not should_fail:
                    fatal("Error ...\n")
                    raise
            if sys.stdout.isatty():
                sleep(3)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int)
    args = parser.parse_args()
    index = args.index
    indexes = None if index is None else [index]
    print(f"[ENV] USE_FORMATER={USE_FORMATER}")
    print(f"[ENV] indexes={indexes}")
    test_config(indexes=indexes)


if __name__ == "__main__":
    main()
