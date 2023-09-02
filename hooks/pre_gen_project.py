# -*- coding: utf-8 -*-
"""Hook run before cookiecutter."""
import re
import sys

# Came from https://github.com/pypa/packaging/blob/23.1/src/packaging/version.py#L113
VERSION_PATTERN = r"""
    ^
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
    $
"""


def match(pattern: str, name: str, value: str) -> None:
    """Match non empty string."""
    if not re.match(pattern, value, re.VERBOSE | re.IGNORECASE):
        print(f"ERROR: {name} ({value!r}) is not a valid string.")
        sys.exit(1)


def main() -> None:
    """Main function for this hook."""
    print(f"[ENV] sys.executable={sys.executable}")
    print(f"[ENV] sys.version={sys.version}")
    match(
        r"^[-a-zA-Z_ ][-a-zA-Z0-9_ ]{,255}$",
        "project_name",
        {{cookiecutter.project_name | tojson()}},
    )
    match(
        r"^[_a-zA-Z][_a-zA-Z0-9]{,255}$",
        "project_slug",
        {{cookiecutter.__project_slug | tojson()}},
    )
    match(
        r"^[a-zA-Z][-a-zA-Z0-9]{,255}$",
        "pip_name",
        {{cookiecutter.__pypi_name | tojson()}},
    )
    match(
        r"^[-a-zA-Z_][-a-zA-Z0-9_]{,255}$",
        "cli_name",
        {{cookiecutter.__cli_name | tojson()}},
    )
    match(VERSION_PATTERN, "version", "{{ cookiecutter.version }}")
    clone_url = "{{ cookiecutter.project_url.strip()|lower }}"
    if "Dashstrom/python-template" in clone_url:
        print("ERROR: Invalid clone url")
        sys.exit(1)
    cli_name = "{{ cookiecutter.__cli_name|lower }}"
    if cli_name in ("test", "echo", "ls", "cat"):
        print("ERROR: Invalid project name")
        sys.exit(1)


if __name__ == "__main__":
    main()
