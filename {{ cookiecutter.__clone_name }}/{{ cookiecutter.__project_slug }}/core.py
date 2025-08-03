"""Core module of {{ cookiecutter.__project_slug }}."""

import logging
from pathlib import Path

# Each file must have a different logger
logger = logging.getLogger(__name__)


def {{ cookiecutter.__project_slug }}(path: str | Path) -> bool:
    """{{ cookiecutter.__description }}.

    Args:
        path: Path to the artifacts

    Returns:
        A boolean if the file exists.

    Examples:
        >>> {{ cookiecutter.__project_slug }}("README.rst")
        False
        >>> {{ cookiecutter.__project_slug }}("README.md")
        True
        >>> {{ cookiecutter.__project_slug }}()
        Traceback (most recent call last):
        TypeError: {{ cookiecutter.__project_slug }}() missing 1 required positional argument: 'path'
    """
    # TODO(you): Put your code here
    logger.debug("Process path: %s", path)
    return Path(path).exists()
