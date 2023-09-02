"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# pylint: skip-file
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

sys.path.insert(0, os.path.abspath("../src"))  # build docs without dependancy

import {{ cookiecutter.__project_slug }}.info

project = {{ cookiecutter.__project_slug }}.info.__project__
copyright = {{ cookiecutter.__project_slug }}.info.__copyright__.replace("Copyright ", "")
author = {{ cookiecutter.__project_slug }}.info.__author__
release = {{ cookiecutter.__project_slug }}.info.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "**tests**"]
todo_include_todos = False
html_favicon = "resources/favicon.ico"
autodoc_inherit_docstrings = True  # If no docstring, inherit from base class

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["resources"]
