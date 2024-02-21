"""Main module."""
{% if 'none' != cookiecutter.cli %}
from .cli import entrypoint
{%- endif %}
from .core import (
    __author__,
    __email__,
    __license__,
    __maintainer__,
    __summary__,
    __version__,
    hello,
)

__all__ = [
{%- if 'none' != cookiecutter.cli %}
    "entrypoint",
{%- endif %}
    "__author__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__summary__",
    "__version__",
    "hello",
]
