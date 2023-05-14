"""Main package."""{% if cookiecutter.cli|lower != 'none' %}
from .cli import entrypoint{% endif %}
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
    "entrypoint",
    "hello",
    "__author__",
    "__copyright__",
    "__description__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__version__",
]
