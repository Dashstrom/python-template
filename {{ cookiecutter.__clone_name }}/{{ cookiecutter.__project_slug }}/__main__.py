"""Entrypoint with `python -m {{ cookiecutter.__project_slug }}`."""

from .cli import entrypoint

if __name__ == "__main__":
    entrypoint()  # pragma: no cover
