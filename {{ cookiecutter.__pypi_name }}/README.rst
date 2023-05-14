.. role:: bash(code)
   :language: bash

{% for i in range(cookiecutter.project_name|length) %}*{% endfor %}
{{cookiecutter.project_name}}
{% for i in range(cookiecutter.project_name|length) %}*{% endfor %}

.. image:: {{ cookiecutter.__source }}/actions/workflows/docs.yml/badge.svg
  :target: {{ cookiecutter.__source }}/actions/workflows/docs.yml
  :alt: CI : Docs
.. image:: {{ cookiecutter.__source }}/actions/workflows/lint.yml/badge.svg
  :target: {{ cookiecutter.__source }}/actions/workflows/lint.yml
  :alt: CI : Lint
.. image:: {{ cookiecutter.__source }}/actions/workflows/tests.yml/badge.svg
  :target: {{ cookiecutter.__source }}/actions/workflows/tests.yml
  :alt: CI : Tests{% if cookiecutter.pypi %}
.. image:: https://img.shields.io/pypi/v/{{ cookiecutter.__pypi_name }}.svg
  :target: {{ cookiecutter.__pypi_url }}
  :alt: PyPI : {{ cookiecutter.__pypi_name }}
.. image:: https://img.shields.io/pypi/pyversions/{{ cookiecutter.__pypi_name }}.svg
  :target: {{ cookiecutter.__pypi_url }}
  :alt: Python : versions{% endif %}{% if cookiecutter.discord != 'no' %}
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

  {{ cookiecutter.__pypi_name }}  --version
  {{ cookiecutter.__pypi_name }}  --help

Developpement
#############

Contributing
************

Contributions are very welcome. Tests can be run with :bash:`make tests-all`,
please ensure the coverage at least stays the same before you submit a pull request.

Setup
*****

..  code-block:: bash

  sudo apt update -y && sudo apt upgrade -y
  git clone {{cookiecutter.__clone_url}} && cd {{cookiecutter.__pypi_name}}
  make setup

Makefile
********

A Makefile is available for help you to run commands.

.. code-block:: text

  clean        Remove all build, test, coverage, venv and Python artifacts.
  cov          Check code coverage.
  dist         Builds source and wheel package.
  docs         Generate Sphinx HTML documentation.
  format       Format style with pre-commit, ruff, black and mypy.
  help         Show current message.
  install      Install the package to the active Python's site-packages.
  lint         Check style with tox, ruff, black and mypy.
  open-docs    Open documentation.
  open-cov     Open coverage report.
  recreate     Clean project and recrete venv.
  release      Package and upload a release.
  setup        Create virtual environment and install pre-commit.
  tests        Run unit and functional tests.
  tests-all    Run all tests in parallel (docs, lint and tests).

{% if cookiecutter.docker == true %}
Docker
######

How to install docker and docker-compose
****************************************

On rasbian run these command before install docker :

.. code-block:: bash

  sudo apt install --reinstall raspberrypi-bootloader raspberrypi-kernel
  sudo reboot

Install docker from script

.. code-block:: bash

  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  sudo usermod -aG docker "${USER}"
  pip3 install docker-compose

Some usefull commands
*********************

.. code-block:: bash

  docker compose up -d --build
  docker compose logs -f
  docker compose exec bot bash
  docker compose stop
  docker compose down --volumes --rmi 'all'

Update
******

.. code-block:: bash

  git pull
  docker compose up -d --build

Backups
*******

Export backups

.. code-block:: bash

  docker compose stop
  docker run --rm -v "easterobot_database:/database" -v "easterobot_logs:/logs" -v "$PWD":/backup ubuntu tar czvf /backup/backup.tar.gz -C / database logs
  docker compose up -d

Import backups

.. code-block:: bash

  docker compose stop
  docker run --rm -v "easterobot_database:/database" -v "easterobot_logs:/logs" -v "$PWD":/backup ubuntu bash -c "cd / && rm -rf /{database,logs}/* && tar xvfP /backup/backup.tar.gz"
  docker compose up -d{%- endif %}{%- if 'none' != cookiecutter.cli %}
Troubleshooting
###############

Your scripts in not on your path
********************************

You can't directly run :bash:`{{ cookiecutter.__cli_name }}`. Add your path to your library as below.

.. code-block:: bash

  echo 'export PATH="$PATH:$HOME/.local/bin' >> ~/.bashrc
  source ~/.bashrc

or use :bash:`{{ cookiecutter.__project_slug }}` as module

.. code-block:: bash

  python3 -m {{ cookiecutter.__project_slug }} --version
{%- endif %}

Uninstall
*********

.. code-block:: bash

  python3 -m pip uninstall {{ cookiecutter.__project_slug }}

License
*******

This work is licensed under `{{ cookiecutter.license }} <{{ cookiecutter.__source }}/blob/main/LICENSE>`_.
