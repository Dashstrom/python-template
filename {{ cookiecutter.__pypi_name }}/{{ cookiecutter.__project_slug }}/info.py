"""Module for package information."""

# fmt: off
__project__ = {{cookiecutter.project_name | tojson()}}
__author__ = {{cookiecutter.full_name | tojson()}}
__maintainer__ = {{cookiecutter.full_name | tojson()}}
__description__ = {{cookiecutter.project_short_description | tojson()}}
__email__ = {{cookiecutter.email | tojson()}}
__version__ = {{cookiecutter.version | tojson()}}
__copyright__ = {{cookiecutter.copyright | tojson()}}
__license__ = {{cookiecutter.license | tojson()}}
# fmt: on
