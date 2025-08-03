"""Update template on your project."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
from time import sleep
import json
import tomli
import tempfile
import shutil

TEMPLATE = str(Path(__file__).resolve().parent.parent)
RE_TITLE = re.compile(r"\*\*\*\**\n(.+)\n\*\*\*\**|^# (.+)")
RE_PATH = re.compile(r"Virtualenv\n.*Path:\s*([^\n]+)\n.*Base", re.DOTALL)
RE_VERSION = re.compile(r"__version__\s*=\s*([^\n]+)\n")
RE_DEPENDENCIES = re.compile(
    r"(?P<package>[a-zA-Z0-9\-\_\[\]]+)(?:(?P<op>>=|==|<=|!=|>|<)v?(?P<version>[0-9\.]+))?"
)
DELETE = ["Makefile", "MANIFEST.in", ".editorconfig"]


def get_poetry_env(repository: Path) -> Path | None:
    try:
        info = subprocess.check_output(
            ["poetry", "env", "info"],
            cwd=repository,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return None
    match = RE_PATH.search(info)
    if match is None:
        return None
    path = Path(match.group(1))
    if not path.exists():
        return None
    return path


def delete_poetry_env(repository: Path) -> None:
    path = get_poetry_env(repository)
    if path is not None:
        shutil.rmtree(path)


def get_git_changes(repository: Path) -> list[tuple[str, ...]]:
    git_output = subprocess.check_output(
        ["git", "status", "--porcelain"],
        cwd=repository,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    return [
        tuple(line.strip().split(" ", maxsplit=1))
        for line in git_output.strip().splitlines()
    ]


def has_uncommitted_git_changes(repository: Path) -> bool:
    return len(get_git_changes(repository)) > 0


def undo_git_change(repository: Path, file: str) -> None:
    subprocess.check_output(
        ["git", "checkout", "HEAD", file],
        cwd=repository,
        stderr=subprocess.DEVNULL,
        text=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument(
        "--template", default=TEMPLATE, help="Path or url to the template."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not update the project.",
        default=False,
    )
    args = parser.parse_args()
    template = args.template
    if not (
        template.startswith("https://")
        or template.startswith("http://")
        or template.startswith("git@")
    ):
        template = str(Path(template).resolve())
    path = Path(args.project)
    dry_run = args.dry_run

    print("Check for uncommitted changes ...")
    if dry_run:
        try:
            if has_uncommitted_git_changes(path):
                print(f"Uncommitted change detected in {path}", file=sys.stderr)
                return
        except subprocess.CalledProcessError:
            print(f"No .git found in in {path}", file=sys.stderr)
            return

    print("Resolving initial configuration of the project ...")
    pyproject = tomli.loads((path / "pyproject.toml").read_text())

    config = {"push": False}

    # Resolve project_name
    readme_rst_path = path / "README.rst"
    if readme_rst_path.exists():
        readme = (path / "README.rst").read_text()
        config["project_name"] = RE_TITLE.search(readme).group(1)
    else:
        readme = (path / "README.md").read_text()
        config["project_name"] = RE_TITLE.search(readme).group(2)

    # Resolve line
    config["line"] = pyproject["tool"]["ruff"]["line-length"]

    # Resolve license
    license_path = path / "LICENSE"
    if not license_path.exists():
        config["license"] = "LicenseRef-Proprietary"
    else:
        license = license_path.read_text()
        if "GNU GENERAL PUBLIC LICENSE" in license:
            config["license"] = "GPL-3.0-or-later"
        elif "GNU LESSER GENERAL PUBLIC LICENSE" in license:
            config["license"] = "LGPL-2.1-or-later"
        elif "MIT License" in license:
            config["license"] = "MIT"
        else:
            config["license"] = "LicenseRef-Proprietary"

    # Using poetry
    dependencies = {}
    if "poetry" in pyproject["tool"]:
        print("Using [tool.poetry]")
        poetry = pyproject["tool"]["poetry"]
        dependencies = set(poetry["dependencies"])
        config.update(
            {
                "project_short_description": poetry["description"],
                "project_url": poetry["homepage"],
                "version": poetry["version"],
                "cli": (
                    "click"
                    if "click" in dependencies
                    else ("argparse" if "scripts" in poetry else "none")
                ),
            }
        )

    # Using setuptools
    elif "project" in pyproject:
        print("Using [project]")
        project = pyproject["project"]
        dependencies_with_versions = set(project.get("dependencies", []))
        groups = pyproject.get("dependency-groups", {})
        dependencies_with_versions |= set(groups.get("dev", []))
        dependencies_with_versions |= {
            dep
            for deps in project.get("optional-dependencies", {}).values()
            for dep in deps
        }

        # Parse dependencies
        dependencies = set()
        for dependency in dependencies_with_versions:
            match = RE_DEPENDENCIES.fullmatch(dependency)
            if match:
                dependencies.add(match["package"])

        # Add version
        if "version" in project:
            config["version"] = project["version"]

        # Other configuration
        config.update(
            {
                "project_short_description": project["description"],
                "project_url": project["urls"]["Source"],
                "cli": (
                    "click"
                    if any(dep.startswith("click") for dep in project["dependencies"])
                    else ("argparse" if "scripts" in project else "none")
                ),
            }
        )

    # Unknown packager
    else:
        print("Unknown packager", file=sys.stderr)
        return

    # doc field
    if "mkdocs" in dependencies or "sphinx" in dependencies:
        config["doc"] = "mkdocs"

    # test field
    config["test"] = "pytest" if "pytest" in dependencies else "none"

    # linter field
    config["linter"] = (
        "ruff" if "ruff" in dependencies or "black" in dependencies else "none"
    )

    # typer field
    config["typer"] = "mypy" if "mypy" in dependencies else "none"

    # hooks field
    config["hooks"] = "pre-commit" if "pre-commit" in dependencies else "none"

    # ci field
    ci = path / ".gitlab-ci.yml"
    if ci.exists():
        ci_content = ci.read_text("utf-8")
        if "\ntest:" in ci_content:
            config["ci"] = "GitLab CI/CD with Windows support"
        elif "test-windows" not in ci_content:
            config["ci"] = "GitLab CI/CD"
        else:  # By default add windows support
            config["ci"] = "GitLab CI/CD with Windows support"
    else:
        config["ci"] = "none"

    # Fallback for resolve version
    if "version" not in config:
        for module in (path / "src").iterdir():
            for candidate in ("info.py", "core.py"):
                metadata_path = module / candidate
                if metadata_path.is_file():
                    metadata = metadata_path.read_text()
                    version_match = RE_VERSION.search(metadata)
                    if version_match:
                        config["version"] = json.loads(version_match[1])

    # Safe sleep
    print("Using cookiecutter config:", json.dumps(config, indent=2))
    if dry_run:
        return None
    sleep(5)

    # Create the new template
    with tempfile.TemporaryDirectory() as tmp:
        print("Recreate the project using resolved configuration ...")
        cmd = [
            "cookiecutter",
            "-v",
            "--no-input",
            template,
            *[f"{key}={value}" for key, value in config.items()],
        ]
        try:
            subprocess.check_call(
                cmd,
                shell=False,
                cwd=str(tmp),
                env={**os.environ, "PYTHON_TEMPLATE_FAST": "y"},
            )
        except subprocess.CalledProcessError as err:
            print(f"An error occurred, exit code: {err.returncode}")
            return
        name = next(iter(name for name in os.listdir(tmp)))
        print("Merge .git directory to the project ...")
        tmp_project = Path(tmp) / name
        shutil.rmtree(tmp_project / ".git", ignore_errors=True)
        shutil.copytree(path / ".git", tmp_project / ".git")
        delete_poetry_env(path)
        shutil.rmtree(path)
        shutil.move(tmp_project, path)
        print("Undo deletions ...")
        for change, file in get_git_changes(path):
            if change == "D" and file not in DELETE:
                print(f"Undo {file}")
                undo_git_change(path, file)
        print("All done, you need to undo change you don't want in your project !")
        print("Don't forget to reinstall all your dependency with:")
        print("uv sync --all-extras; uv run poe setup-pre-commit; uv run poe format")


if __name__ == "__main__":
    main()
