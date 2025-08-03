"""Init module of {{ cookiecutter.__project_slug }}."""
{% if 'none' != cookiecutter.cli %}
from .cli import entrypoint
{%- endif %}
from .core import (
    {{ cookiecutter.__project_slug }},
)
from .info import (
    __author__,
    __copyright__,
    __email__,
    __issues__,
    __license__,
    __maintainer__,
    __maintainer_email__,
    __project__,
    __summary__,
    __version__,
)

__all__ = [
    "__author__",
    "__copyright__",
    "__email__",
    "__issues__",
    "__license__",
    "__maintainer__",
    "__maintainer_email__",
    "__project__",
    "__summary__",
    "__version__",
    "{{ cookiecutter.__project_slug }}",
{%- if 'none' != cookiecutter.cli %}
    "entrypoint",
{%- endif %}
]
