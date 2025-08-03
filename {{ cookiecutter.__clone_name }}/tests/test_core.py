"""Test core module."""

from {{ cookiecutter.__project_slug }} import {{ cookiecutter.__project_slug }}


def test_{{ cookiecutter.__project_slug }}() -> None:
    """Test the {{ cookiecutter.__project_slug }} function."""
    assert not {{ cookiecutter.__project_slug }}("README.rst")
    assert {{ cookiecutter.__project_slug }}("README.md")
