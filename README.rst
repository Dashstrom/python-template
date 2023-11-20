.. role:: bash(code)
  :language: bash

***************
Python template
***************

.. image:: https://github.com/Dashstrom/python-template/actions/workflows/tests.yml/badge.svg
  :target: https://github.com/Dashstrom/python-template/actions/workflows/tests.yml
  :alt: CI : Tests

Description
###########

A medium complexity template for create CLI or python package.

Tools used
##########

- `Black <https://black.readthedocs.io/en/stable/>`_ The uncompromising Python code formatter.
- `Cookiecutter <https://www.cookiecutter.io>`_ A cross-platform command-line utility that creates projects.
- `Doctest <https://docs.pytest.org/en/7.4.x/how-to/doctest.html>`_ Executes tests in docstrings
- `Editorconfig <https://editorconfig.org/>`_ Configuration file format for defining coding styles in shared projects.
- `Git <https://git-scm.com/>`_ Git is the most widely used version control system.
- `Github Actions <https://docs.github.com/en/actions>`_ Automate and execute your software development workflows right in your repository.
- `Mypy <https://mypy.readthedocs.io/en/stable/>`_ Optional static typing for Python.
- `Poetry <https://python-poetry.org/>`_ Python packaging and dependency management made easy.
- `Poe the Poet <https://poethepoet.natn.io/index.html>`_ A task runner that works well with poetry.
- `Pre-commit <https://pre-commit.com/>`_ A framework for managing and maintaining multi-language pre-commit hooks.
- `Pytest <https://docs.pytest.org/en/7.4.x/>`_ Framework making it easy to write small tests, yet scales to support complex functional testing.
- `Ruff <https://beta.ruff.rs/docs/rules/>`_ An extremely fast Python linter, written in Rust.
- `Sphinx with read the docs theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/>`_ Sphinx makes it easy to create intelligent and beautiful documentation.

Prerequisite
############

First of all you will need to install a version of `python <https://www.python.org/>`_ higher than 3.8.

You need to install `pix <https://pypa.github.io/pipx/installation/>`_, `cookiecutter <https://cookiecutter.readthedocs.io/en/1.7.3/installation.html>`_ and `poetry <https://python-poetry.org/docs/#installation>`_ with the following commands:

..  code-block:: bash

  pip install --user pipx
  pipx ensurepath
  pipx install cookiecutter poetry

You will also need to install `git <https://git-scm.com/>`_ following `the official guide <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_.


Installation
############

First you need to create your repository then process as follows:

..  code-block:: bash

  python -m cookiecutter --accept-hooks yes --keep-project-on-failure gh:Dashstrom/python-template
  cd YOUR_PROJECT
  poetry shell

Testing
#######

..  code-block:: bash

  python tests/test_template.py
