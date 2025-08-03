"""Test for template."""

import argparse
import json
import os
from pathlib import Path
from shlex import quote
import shutil
import subprocess
import sys
import tempfile
from time import sleep

HERE = Path(__file__).parent
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
    "license": "LGPL-2.1-or-later",
    "push": False,
    "docker": False,
    "line": "79",
    "fail": False,
}
CONFIGS = [
    {
        "project_short_description": "A little simple test",
    },
    {
        "project_short_description": 'A"; import sys;sys.exit(1)',
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
    {"license": "LicenseRef-Proprietary"},
    {"line": "119"},
    {"docker": True},
    {"line": 120},
    {"cli": "click", "line": 120},
    {"discord": "blabla"},
]


def error(text: str) -> None:
    """Print error and exit."""
    print(f"ERROR: {text}", file=sys.stderr, flush=True)
    raise OSError("Invalid return")


def wait_if_a_tty() -> None:
    """Check if the current terminal is a tty."""
    if sys.stdin.isatty():
        input("Press enter for clean up")


def fatal(text: str) -> None:
    """Print error and exit."""
    try:
        error(text)
    except OSError:
        wait_if_a_tty()
        sys.exit(1)


def run(*cmd: str, cwd: Path | str | None = None) -> None:
    """Run test command."""
    print(f"[TEST RUN] {' '.join(quote(arg) for arg in cmd)} in {cwd}")
    try:
        subprocess.check_call(
            cmd,
            shell=False,
            stdout=sys.stderr,
            stderr=sys.stderr,
            cwd=str(cwd),
            env={**os.environ.copy(), "DISABLE_VSCODE": "1"},
        )
    except subprocess.CalledProcessError:
        error("Exit code is not zero")


def test_config(*, indexes: list[int] | None = None) -> None:
    """Test for configs."""
    shutil.rmtree(CACHE, ignore_errors=True)
    CACHE.mkdir(exist_ok=True, parents=True)
    for index, partial_config in enumerate(CONFIGS, start=1):
        if indexes is not None and index not in indexes:
            continue
        repr_config = json.dumps(partial_config, indent=2)
        config = DEFAULT_CONFIG.copy()
        config.update(partial_config)  # type: ignore[call-overload]
        should_fail = config.get("fail", False)
        with tempfile.TemporaryDirectory(prefix="python-template-", dir=CACHE) as tmp:
            try:
                print(
                    f"\n\nWorking on {index}/{len(CONFIGS)} at {tmp} "
                    f"with config: \n{repr_config}\n\n"
                )
                if sys.stdout.isatty():
                    sleep(3)
                run(
                    "uvx",
                    "cookiecutter",
                    "-v",
                    "--keep-project-on-failure",
                    "--no-input",
                    str(TEMPLATE_PATH),
                    *[f"{key}={value}" for key, value in config.items()],
                    cwd=tmp,
                )
                project_url: str = config["project_url"]  # type: ignore[assignment]
                clone_name: str = project_url.split("/")[-1]
                project = Path(tmp) / clone_name
                run("uv", "sync", cwd=project)
                run("uv", "run", "poe", "check", cwd=project)
                run("uv", "run", "poe", "cov", cwd=project)
                if should_fail:
                    fatal("Test should fail")
            except KeyboardInterrupt:
                print("Interrupted !")
                break
            except (OSError, SystemExit, subprocess.CalledProcessError):
                if not should_fail:
                    print("An unexpected error occurred:", file=sys.stderr, flush=True)
                    raise
            if sys.stdout.isatty():
                sleep(3)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=int)
    args = parser.parse_args()
    index = args.index
    indexes = None if index is None else [index]
    print(f"[ENV] indexes={indexes}")
    try:
        test_config(indexes=indexes)
    finally:
        shutil.rmtree(CACHE, ignore_errors=True)


if __name__ == "__main__":
    main()
