# {{ cookiecutter.project_name }}

[![CI : Docs]({{ cookiecutter.__repository }}/actions/workflows/docs.yml/badge.svg)]({{ cookiecutter.__repository }}/actions/workflows/docs.yml)
[![CI : Lint]({{ cookiecutter.__repository }}/actions/workflows/lint.yml/badge.svg)]({{ cookiecutter.__repository }}/actions/workflows/lint.yml)
[![CI : Tests]({{ cookiecutter.__repository }}/actions/workflows/tests.yml/badge.svg)]({{ cookiecutter.__repository }}/actions/workflows/tests.yml)
{% if cookiecutter.license != "Proprietary" %}
[![PyPI : {{ cookiecutter.__pypi_name }}](https://img.shields.io/pypi/v/{{ cookiecutter.__pypi_name }}.svg)]({{ cookiecutter.__pypi_url }})
[![Python : versions](https://img.shields.io/pypi/pyversions/{{ cookiecutter.__pypi_name }}.svg)]({{ cookiecutter.__pypi_url }})
{% endif %}
{% if cookiecutter.__discord %}
[![Discord](https://img.shields.io/badge/Discord-{{ cookiecutter.project_name.replace(" ", "%20") }}-5865F2?style=flat&logo=discord&logoColor=white)]({{ cookiecutter.discord }})
{% endif %}
[![License : {{ cookiecutter.license }}](https://img.shields.io/badge/license-{{ cookiecutter.license.replace(" ", "%20") }}-green.svg)]({{ cookiecutter.__repository }}/blob/main/LICENSE)

{{ cookiecutter.__description }}{% if cookiecutter.license != "Proprietary" %}

Documentation
#############

Documentation is available on {{ cookiecutter.__documentation }}{% endif %}

## Installation

```bash
# Using pip
pip install {{ cookiecutter.__pypi_name }}
# Using uv (install in your project dependencies)
uv add {{ cookiecutter.__pypi_name }}
# Using pipx (install as a tool in a venv)
pipx install {{ cookiecutter.__pypi_name }}
# Using uv (install as a tool in a venv)
uv tool install {{ cookiecutter.__pypi_name }}
```

## Usage

```bash
{{ cookiecutter.__cli_name }} --version
{{ cookiecutter.__cli_name }} --help
{{ cookiecutter.__cli_name }} run ./README.md
```

## Development

### Contributing

Contributions are very welcome. Tests can be run with `poe check`, please
ensure the coverage at least stays the same before you submit a pull request.

### Prerequisite

First, You need to install [git](https://git-scm.com) following [the official guide](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and configure it. Finally, run these commands for setup install the project with dev dependencies.

```bash
git clone {{ cookiecutter.__clone_url }}
cd {{ cookiecutter.__clone_name }}
uv sync --all-extras --python 3.10
uv run poe setup
```

### Poe

Poe is available for help you to run tasks: `uv run poe {task}` or `poe task` within the venv.

```text
test                  Run test suite.
lint                  Run linters: ruff checker and ruff formatter and mypy.
format                Run linters in fix mode.
check                 Run all checks: lint, test and docs.
check-tag             Check if the current tag match the version.
cov                   Run coverage for generate report and html.
open-cov              Open html coverage report in webbrowser.
doc                   Build documentation.
open-doc              Open documentation in webbrowser.
setup                 Setup pre-commit.
pre-commit            Run pre-commit.
clean                 Clean cache files.
```

### How to add dependency

```bash
uv add 'PACKAGE'
```

### Ignore illegitimate warnings

To ignore illegitimate warnings you can add :

- **# noqa: ERROR_CODE** on the same line for ruff.
- **# type: ignore[ERROR_CODE]** on the same line for mypy.
- **# pragma: no cover** on the same line to ignore line for coverage.
- **# doctest: +SKIP** on the same line for doctest.

## Uninstall

```bash
pip uninstall {{ cookiecutter.__pypi_name }}
```

## License

This work is licensed under [{{ cookiecutter.license }}]({{ cookiecutter.__repository }}/blob/main/LICENSE).
