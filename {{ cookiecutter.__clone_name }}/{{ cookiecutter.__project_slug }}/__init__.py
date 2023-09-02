"""Main module."""
{%- if 'none' != cookiecutter.cli %}
from .cli import entrypoint
{%- endif %}
from .core import hello
from .info import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __maintainer__,
    __project__,
    __version__,
)

__all__ = [
{%- if 'none' != cookiecutter.cli %}
    "entrypoint",
{%- endif %}
    "hello",
    "__author__",
    "__copyright__",
    "__description__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__project__",
    "__version__",
]
