.. role:: bash(code)
   :language: bash

{{cookiecutter.project_name}}
{% for i in range(cookiecutter.project_name|length) %}={% endfor %}

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

Install
*******

You can install :bash:`{{ cookiecutter.__pypi_name }}` via `pip <https://pypi.org/project/pip/>`_ from `PyPI <https://pypi.org/project>`_

..  code-block:: bash

    pip install {{ cookiecutter.__pypi_name }}

Usage
*****

DShow version of {{cookiecutter.__pypi_name}}.

..  code-block:: bash
    {{ cookiecutter.__pypi_name }}

Developpement
*************

Contributing
------------
Contributions are very welcome. Tests can be run with tox, please ensure
the coverage at least stays the same before you submit a pull request.

Installation
------------

..  code-block:: bash

    sudo apt update -y && sudo apt upgrade -y
    sudo apt install mypy python3.8-venv
    git clone {{cookiecutter.__clone_url}}
    cd {{cookiecutter.__pypi_name}}
    make setup

Makefile
--------

A Makefile is available for help you to run commands.

..  code-block:: text

    help         show actual message
    venv         create virtual environment
    clean        remove all build, test, coverage and Python artifacts
    lint         check style with pre-commit
    test         run tests, lint and docs build
    coverage     check code coverage quickly with the default Python
    docs         generate Sphinx HTML documentation
    release      package and upload a release
    dist         builds source and wheel package
    install      install the package to the active Python's site-packages
{% if cookiecutter.docker == true %}
Docker
******

How to install docker and docker-compose
----------------------------------------

On rasbian run these command before install docker :

..  code-block:: bash

    sudo apt install --reinstall raspberrypi-bootloader raspberrypi-kernel
    sudo reboot

Install docker from script

..  code-block:: bash

    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker "${USER}"
    pip3 install docker-compose

Some usefull commands
---------------------

..  code-block:: bash

    docker compose up -d --build
    docker compose logs -f
    docker compose exec bot bash
    docker compose stop
    docker compose down --volumes --rmi 'all'

Update
------

..  code-block:: bash

    git pull
    docker compose up -d --build

Backups
-------

Export backups

..  code-block:: bash

    docker compose stop
    docker run --rm -v "easterobot_database:/database" -v "easterobot_logs:/logs" -v "$PWD":/backup ubuntu tar czvf /backup/backup.tar.gz -C / database logs
    docker compose up -d

Import backups

..  code-block:: bash

    docker compose stop
    docker run --rm -v "easterobot_database:/database" -v "easterobot_logs:/logs" -v "$PWD":/backup ubuntu bash -c "cd / && rm -rf /{database,logs}/* && tar xvfP /backup/backup.tar.gz"
    docker compose up -d{% endif %}
License
*******

This work is licensed under `{{ cookiecutter.license }} <{{ cookiecutter.__source }}/blob/main/LICENSE>`_.
