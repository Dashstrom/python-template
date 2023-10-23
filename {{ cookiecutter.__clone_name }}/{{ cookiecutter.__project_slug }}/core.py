"""Core module."""
from importlib.metadata import Distribution

DISTRIBUTION = Distribution.from_name(
    "{{ cookiecutter.__project_slug }}",
)
METADATA = DISTRIBUTION.metadata


def hello(text: str) -> str:
    """Add hello text before the provided text."""
    return f"Hello {text}".strip()
