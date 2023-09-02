.. role:: bash(code)
  :language: bash

***************
Python template
***************

A medium complexity template for create CLI or python package.

Tools used
##########

- `Black <https://black.readthedocs.io/en/stable/>`_ Formatter
- `Cookiecutter <https://www.cookiecutter.io>`_ Template framework
- `Editorconfig <https://editorconfig.org/>`_ Common configuration for editor
- `Git <https://git-scm.com/>`_ Version controller
- `Github Actions <https://docs.github.com/en/actions>`_ CI/CD
- `Make <https://www.gnu.org/software/make/>`_ Tool for run commands
- `Mypy <https://mypy.readthedocs.io/en/stable/>`_ Linter for types and annotations
- `Pre-commit <https://pre-commit.com/>`_ Tool for create hooks when committing
- `Pytest <https://docs.pytest.org/en/7.3.x/>`_ Tests runner
- `Ruff <https://beta.ruff.rs/docs/rules/>`_ Formatter and linter embedding flake8, pylint, bandit, pycodestyle and pep8
- `Setuptools <https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html>`_ Tool for packaging
- `Sphinx with read the docs theme <https://sphinx-rtd-theme.readthedocs.io/en/stable/>`_ Docs generator
- `Tox <https://tox.wiki/en/latest/>`_ Virtual env manager for tests
- `Twine <https://twine.readthedocs.io/en/stable/>`_ Command line interface for upload to PyPI
- `Virtualenv <https://virtualenv.pypa.io/en/latest/>`_ Tool for isolate project

Prerequisite
############

You need to have :bash:`cookiecutter`, :bash:`make` and :bash:`git` installed system-wide. :bash:`virtualenv` will be automatically installed system-wide.

..  code-block:: bash

  sudo apt update -y && sudo apt upgrade -y
  sudo apt install build-essential git python3-pip
  pip install -U cookiecutter

Installation
############

First you need to create your repository then process as follows :

..  code-block:: bash

  python3 -m cookiecutter --accept-hooks yes --keep-project-on-failure gh:Dashstrom/python-template
  cd YOUR_PROJECT && source venv/bin/activate

If you want to use the template without cookiecutter installed system-wide you can process as follows (this will steal install virtualenv system-wide) :

..  code-block:: bash

  python3 -m venv venv
  venv/bin/pip install -U cookiecutter
  venv/bin/cookiecutter --accept-hooks yes --keep-project-on-failure gh:Dashstrom/python-template
  rm -rf venv
  cd YOUR_PROJECT && source venv/bin/activate

Testing
#######

..  code-block:: bash

  python3 tests/test_template.py

Troubleshooting
###############

Ruff : FBT001 Boolean positional arg in function definition
***********************************************************

..  code-block:: python

  def foo_bad(a: int, b: bool = False, c: int = 5) -> bool:
      return a % c is b

  def foo_good(a: int, c: int = 5, *, b: bool = False) -> bool:
      return a % c is b

  foo_bad(1, True)
  foo_good(1, True)  # Doesn't work, b is now keyword only
  foo_good(1, b=True)

Mypy : Unexpected keyword argument "foo" for "Bar" [call-arg]
**************************************************************************************

..  code-block:: python

  # Bad
  Bar(foo=True)  # foo exist in 3.10 but not in 3.8, mypy raise an error

  # Good
  import sys

  if sys.version_info > (3, 8):
      Bar(foo=True)
  else:
      Bar()

Common mistake in lazy initialization
*************************************

..  code-block:: python

  from typing import Optional

  class B:
      def get(self) -> int:
          return 5

  class BadA:
      def __init__(self) -> None:
          self.b: Optional[B] = None

      def init(self) -> None:
          self.b = B()

      def foo(self) -> int:
          # mypy : Item "None" of "Optional[B]" has no attribute "get" [union-attr]
          return self.b.get()

  class GoodA:
      def __init__(self) -> None:
          self._b: Optional[B] = None

      def init(self) -> None:
          self._b = B()

      @property
      def b(self) -> B:
          if self._b is None:
              err_msg = "Not initialized"
              raise ValueError(err_msg)
          return self._b

      def foo(self) -> int:
          return self.b.get()


  class C:
      b: B

      def foo_bad(self) -> B:
          # mypy : Member "b" has type "B" which does not implement bool or len so it could always be true in boolean context [truthy-bool]
          # Will raise AttributeError
          if not self.b:
              self.b = B()
          return self.b

      def foo_bad_also(self) -> B:
          # Will raise AttributeError
          if self.b is None:
              self.b = B()
          return self.b

      def foo_good(self) -> B:
          if hasattr(self, "b"):
              self.b = B()
          return self.b
