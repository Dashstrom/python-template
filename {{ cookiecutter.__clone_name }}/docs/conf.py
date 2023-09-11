"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

from {{ cookiecutter.__project_slug }} import info

sys.path.insert(0, os.path.abspath(".."))

project = info.__project__
copyright = info.__copyright__.replace("Copyright", "").strip()
author = info.__author__
version = info.__version__
release = info.__version__

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
# If no docstring, inherit from base class
autodoc_inherit_docstrings = True
# Remove 'view source code' from top of page (for html, not python)
html_show_sourcelink = False
# Enable 'expensive' imports for sphinx_autodoc_typehints
set_type_checking_flag = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["resources"]
