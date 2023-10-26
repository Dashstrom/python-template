"""Configuration for all tests."""

from typing import Any, Dict

import pytest

from {{ cookiecutter.__project_slug }} import METADATA


@pytest.fixture(autouse=True)
def _add_author(doctest_namespace: Dict[str, Any]) -> None:
    """Update doctest namespace."""
    doctest_namespace["author"] = METADATA["Author"]
