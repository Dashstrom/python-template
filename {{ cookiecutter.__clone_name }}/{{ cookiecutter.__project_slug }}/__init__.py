"""Main module."""
{% if 'none' != cookiecutter.cli %}
from .cli import entrypoint
{%- endif %}
from .core import DISTRIBUTION, METADATA, hello

__all__ = [
{%- if 'none' != cookiecutter.cli %}
    "entrypoint",
{%- endif %}
    "DISTRIBUTION",
    "METADATA",
    "hello",
]
