.. role:: bash(code)
  :language: bash

{% for i in range(cookiecutter.project_name|length) %}*{% endfor %}
{{ cookiecutter.project_name }}
{% for i in range(cookiecutter.project_name|length) %}*{% endfor %}

.. image:: {{ cookiecutter.__repository }}/actions/workflows/docs.yml/badge.svg
  :target: {{ cookiecutter.__repository }}/actions/workflows/docs.yml
  :alt: CI : Docs

.. image:: {{ cookiecutter.__repository }}/actions/workflows/lint.yml/badge.svg
  :target: {{ cookiecutter.__repository }}/actions/workflows/lint.yml
  :alt: CI : Lint

.. image:: {{ cookiecutter.__repository }}/actions/workflows/tests.yml/badge.svg
  :target: {{ cookiecutter.__repository }}/actions/workflows/tests.yml
  :alt: CI : Tests{% if cookiecutter.license != "Proprietary" %}

.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.__pypi_name }}.svg
  :target: {{ cookiecutter.__pypi_url }}
  :alt: PyPI : {{ cookiecutter.__pypi_name }}

.. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.__pypi_name }}.svg
  :target: {{ cookiecutter.__pypi_url }}
  :alt: Python : versions{% endif %}{% if cookiecutter.discord|lower not in ("no", "null", "false", "n", "non", "f", "0", "none", "undefined") %}

.. image:: https://img.shields.io/badge/Discord-{{ cookiecutter.project_name.replace(" ", "%20") }}-5865F2?style=flat&logo=discord&logoColor=white
  :target: {{ cookiecutter.discord }}
  :alt: Discord{% endif %}

.. image:: https://img.shields.io/badge/license-{{ cookiecutter.license.replace(" ", "%20") }}-green.svg
  :target: {{ cookiecutter.__repository }}/blob/main/LICENSE
  :alt: License : {{ cookiecutter.license }}

Description
###########

{{cookiecutter.project_short_description}}

Installation
############

You can install :bash:`{{ cookiecutter.__pypi_name }}` via `pip <https://pypi.org/project/pip/>`_
from `PyPI <https://pypi.org/project>`_

..  code-block:: bash

  pip install {{ cookiecutter.__pypi_name }}

Usage
#####

..  code-block:: bash

  {{ cookiecutter.__cli_name }} --version
  {{ cookiecutter.__cli_name }} --help

Development
###########

Contributing
************

Contributions are very welcome. Tests can be run with :bash:`poe check`, please
ensure the coverage at least stays the same before you submit a pull request.

Setup
*****

You need to install `Poetry <https://python-poetry.org/docs/#installation>`_
and `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_
for work with this project.

..  code-block:: bash

  git clone {{ cookiecutter.__clone_url }}
  cd {{ cookiecutter.__clone_name }}
  poetry install --all-extras
  poetry run poe setup
  poetry shell

Poe
********

Poe is available for help you to run tasks.

..  code-block:: text

  test           Run test suite.
  lint           Run linters : ruff linter, ruff formatter and mypy.
  format         Run linters in fix mode.
  check          Run all checks : lint, test and docs.
  cov            Run coverage for generate report and html.
  open-cov       Open html coverage report in webbrowser.
  docs           Build documentation.
  open-docs      Open documentation in webbrowser.
  setup          Setup pre-commit.
  pre-commit     Run pre-commit.
  clean          Clean cache files

Skip commit verification
************************

If the linting is not successful, you can't commit.
For forcing the commit you can use the next command :

..  code-block:: bash

  git commit --no-verify -m 'MESSAGE'

Commit with commitizen
**********************

To respect commit conventions, this repository uses
`Commitizen <https://github.com/commitizen-tools/commitizen?tab=readme-ov-file>`_.

..  code-block:: bash

  cz commit

How to add dependency
*********************

..  code-block:: bash

  poetry add 'PACKAGE'

Ignore illegitimate warnings
****************************

To ignore illegitimate warnings you can add :

- **# noqa: ERROR_CODE** on the same line for ruff.
- **# type: ignore[ERROR_CODE]** on the same line for mypy.
- **# pragma: no cover** on the same line to ignore line for coverage.
- **# doctest: +SKIP** on the same line for doctest.

Uninstall
#########

..  code-block:: bash

  pip uninstall {{ cookiecutter.__pypi_name }}
{%- if cookiecutter.license != "Proprietary" %}

License
#######

This work is licensed under `{{ cookiecutter.license }} <{{ cookiecutter.__repository }}/-/raw/main/LICENSE>`_.{%- endif %}
