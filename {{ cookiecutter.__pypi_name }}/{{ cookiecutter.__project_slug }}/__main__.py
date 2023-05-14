"""Main entrypoint for package."""
import sys

from .cli import entrypoint

if __name__ == "__main__":
    sys.modules["__main__"] = entrypoint  # type: ignore[assignment]  # pragma: no cover  # noqa: E501
    entrypoint()  # pylint: disable=no-value-for-parameter,missing-kwoa  # pragma: no cover  # noqa: E501
