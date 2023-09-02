.. role:: bash(code)
  :language: bash

{% for i in range(cookiecutter.project_name|length) %}*{% endfor %}
{{ cookiecutter.project_name }}
{% for i in range(cookiecutter.project_name|length) %}*{% endfor %}

.. image:: {{ cookiecutter.__source }}/actions/workflows/docs.yml/badge.svg
  :target: {{ cookiecutter.__source }}/actions/workflows/docs.yml
  :alt: CI : Docs
.. image:: {{ cookiecutter.__source }}/actions/workflows/lint.yml/badge.svg
  :target: {{ cookiecutter.__source }}/actions/workflows/lint.yml
  :alt: CI : Lint
.. image:: {{ cookiecutter.__source }}/actions/workflows/tests.yml/badge.svg
  :target: {{ cookiecutter.__source }}/actions/workflows/tests.yml
  :alt: CI : Tests{% if if 'not open' not in cookiecutter.license|lower %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.__pypi_name }}.svg
  :target: {{ cookiecutter.__pypi_url }}
  :alt: PyPI : {{ cookiecutter.__pypi_name }}
.. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.__pypi_name }}.svg
  :target: {{ cookiecutter.__pypi_url }}
  :alt: Python : versions{% endif %}{% if cookiecutter.discord|lower != 'no' %}
.. image:: https://img.shields.io/badge/Discord-cookiecutter-5865F2?style=flat&logo=discord&logoColor=white
  :target: {{ cookiecutter.discord }}
  :alt: Discord{% endif %}
.. image:: https://img.shields.io/badge/license-{{ cookiecutter.license.replace(" ", "%20") }}-green.svg
  :target: {{ cookiecutter.__source }}/blob/main/LICENSE
  :alt: License : {{ cookiecutter.license }}

{{cookiecutter.project_short_description}}

Installation
############

You can install :bash:`{{ cookiecutter.__pypi_name }}` via `pip <https://pypi.org/project/pip/>`_ from `PyPI <https://pypi.org/project>`_

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

Contributions are very welcome. Tests can be run with :bash:`make tests-all`, please ensure
the coverage at least stays the same before you submit a pull request.

Setup
*****

..  code-block:: bash

  sudo apt update -y && sudo apt upgrade -y && sudo apt-get install python3-pip
  git clone {{ cookiecutter.__clone_url }} && cd {{ cookiecutter.__clone_name }}
  make setup

Makefile
********

A Makefile is available for help you to run commands.

..  code-block:: text

  clean          Remove all build, test, coverage, venv and Python artifacts.
  cov            Check code coverage.
  dist           Builds source and wheel package.{%- if "True" == cookiecutter.docker %}
  docker-logs    Check and follow docker logs.
  docker-up      Run docker as daemon and rebuild image.
  docker-stop    Stop all containers.
  docker-purge   Remove and drop every image, container and network.
  docker-restore Restore logs backup.
  docker-backup  Make backups of logs.
  docker-shell   Get a shell in the running container.{%- endif %}
  docs           Generate Sphinx HTML documentation.
  format         Format style with pre-commit, ruff, black and mypy.
  help           Show current message.
  install        Install the package to the active Python's site-packages.
  lint           Check style with tox, ruff, black and mypy.
  open-docs      Open documentation.
  open-cov       Open coverage report.
  release        Package and upload a release.
  setup          Create virtual environment and install pre-commit.
  tests          Run unit and functional tests.
  tests-all      Run all tests in parallel (docs, lint and tests).
  uninstall      Install the package to the active Python's site-packages.
{%- if cookiecutter.strict_lint %}

Commit
******

If the linting is not successful, you can't commit. For forcing the commit you can use the next command :

..  code-block:: bash

  git commit --no-verify -m "MESSAGE"
{%- endif %}{%- if 'none' != cookiecutter.cli %}

How to add dependency
*********************

Your must add the requirement in :

- **pre-commit-config.yaml** line 28
- **pyproject.toml** line 19

After that you need to exit your virtualenv with :bash:`deactivate`
and close your editor if it uses dependencies for autocompletion.

Once this is done, recreate virtualenv with :bash:`make setup`.

Ignore illegitimate warnings
****************************

To ignore illegitimate warnings you can add :

- **# NoQA: ERROR_CODE** on the same line for ruff.
- **# type: ignore[ERROR_CODE]** on the same line for mypy.
- **# fmt: off** et **# fmt: on** before and after for black.
- **# pragma: no cover** on the same line to ignore line for coverage.

Troubleshooting
###############

Your scripts in not on your path
********************************

You can't directly run :bash:`{{ cookiecutter.__cli_name }}`. Add your path to your library as below.

..  code-block:: bash

  echo 'export PATH="$PATH:$HOME/.local/bin' >> ~/.bashrc
  source ~/.bashrc

or use :bash:`{{ cookiecutter.__project_slug }}` as module

..  code-block:: bash

  python3 -m {{ cookiecutter.__project_slug }} --help
{%- endif %}

Uninstall
#########

..  code-block:: bash

  pip uninstall {{ cookiecutter.__pip_name }}
{%- if 'not open' not in cookiecutter.license|lower %}

License
#######

This work is licensed under `{{ cookiecutter.license }} <{{ cookiecutter.__source }}/-/raw/main/LICENSE>`_.{%- endif %}
