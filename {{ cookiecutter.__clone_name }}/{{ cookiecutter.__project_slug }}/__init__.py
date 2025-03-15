"""Main module."""
{% if 'none' != cookiecutter.cli %}
from .cli import entrypoint
{%- endif %}
from .core import hello
from .info import (
    __author__,
    __email__,
    __license__,
    __maintainer__,
    __summary__,
    __version__,
)

__all__ = [
    "__author__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__summary__",
    "__version__",
{%- if 'none' != cookiecutter.cli %}
    "entrypoint",
{%- endif %}
    "hello",
]
