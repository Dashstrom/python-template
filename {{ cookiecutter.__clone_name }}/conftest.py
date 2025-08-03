"""Configuration for all tests."""

from pathlib import Path
from typing import Any

import pytest

from {{ cookiecutter.__project_slug }} import __author__


@pytest.fixture
def resources_path() -> Path:
    """Fixture for create a path to test resources."""
    return Path(__file__).parent / "tests" / "resources"


@pytest.fixture(autouse=True)
def _populate_doctest(doctest_namespace: dict[str, Any]) -> None:
    """Update doctest namespace."""
    doctest_namespace["author"] = __author__
