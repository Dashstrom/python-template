.. role:: bash(code)
  :language: bash

***************
Python template
***************

A medium complexity template for create CLI or python package.

Tools used
##########

- `Black <https://black.readthedocs.io/en/stable/>`_
- `Cookiecutter <https://cookiecutter.readthedocs.io/en/stable/README.html>`_
- `Editorconfig <https://editorconfig.org/>`_
- `Git <https://git-scm.com/>`_
- `Github Actions <https://docs.github.com/en/actions>`_
- `Make <https://www.gnu.org/software/make/>`_
- `Mypy <https://mypy.readthedocs.io/en/stable/>`_
- `Pre-commit <https://pre-commit.com/>`_
- `Pytest <https://docs.pytest.org/en/7.3.x/>`_
- `Ruff <https://beta.ruff.rs/docs/rules/>`_
- `Setuptools <https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html>`_
- `Sphinx with read the docs theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/>`_
- `Tox <https://tox.wiki/en/latest/>`_
- `Twine <https://twine.readthedocs.io/en/stable/>`_
- `Virtualenv <https://virtualenv.pypa.io/en/latest/>`_

Prerequisite
############

You need to have :bash:`cookiecutter`, :bash:`make` and :bash:`git` installed system wide. :bash:`virtualenv` will be automatically installed system wide.

..  code-block:: bash

  sudo apt update -y && sudo apt upgrade -y
  sudo apt install build-essential git python3-pip
  pip install cookiecutter virtualenv


Installation
############

First you need to create your repository then process as follow :

..  code-block:: bash

  python3 -m cookiecutter https://github.com/Dashstrom/python-template.git
  cd YOUR_PROJECT && source venv/bin/activate

If you want use the template without cookiecutter and virtualenv installed system-wide you can process as follow :

..  code-block:: bash

  python3 -m venv venv
  venv/bin/pip install cookiecutter
  venv/bin/cookiecutter https://github.com/Dashstrom/python-template.git
  rm -rf venv
  cd YOUR_PROJECT && source venv/bin/activate
