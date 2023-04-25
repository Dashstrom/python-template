"""Main package."""{% if cookiecutter.cli|lower != 'none' %}
from .cli import cli{% endif %}
from .core import hello
from .info import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __maintainer__,
    __version__,
)

__all__ = [
    "cli",
    "hello",
    "__author__",
    "__copyright__",
    "__description__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__version__",
]
