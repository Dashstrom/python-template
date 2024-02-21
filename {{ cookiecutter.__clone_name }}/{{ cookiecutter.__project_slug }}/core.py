"""Core module."""

from importlib.metadata import Distribution

_DISTRIBUTION = Distribution.from_name(
    "{{ cookiecutter.__project_slug }}",
)
_METADATA = _DISTRIBUTION.metadata

__author__ = _METADATA["Author"]
__license__ = _METADATA["License"]
__version__ = _METADATA["Version"]
__maintainer__ = _METADATA["Maintainer-email"]
__email__ = _METADATA["Maintainer"]
__summary__ = _METADATA["Summary"]


def hello(text: str) -> str:
    """Add hello text before the provided text.

    Args:
        text: Text to add after hello.

    Returns:
        A string with Hello + text.

    Examples:
        >>> hello("world")
        'Hello world'
        >>> hello(author).startswith('Hello')
        True
        >>> hello("")
        'Hello'
        >>> hello()
        Traceback (most recent call last):
        TypeError: hello() missing 1 required positional argument: 'text'
    """
    return f"Hello {text}".strip()
