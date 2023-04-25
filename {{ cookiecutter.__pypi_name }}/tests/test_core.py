"""Test module for test core module."""
from {{ cookiecutter.__project_slug }} import hello


def test_hello() -> None:
    """Test basic."""
    assert hello("Dashstrom") == "Hello Dashstrom"
    assert hello("") == "Hello"
