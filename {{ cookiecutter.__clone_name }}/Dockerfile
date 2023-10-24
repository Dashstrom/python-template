FROM python:3.8 as python-base

# Setup enrionnement variables
ENV \
    # https://docs.python.org/3/using/cmdline.html
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # https://pip.pypa.io/en/stable/
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # https://python-poetry.org/docs/configuration
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    # Add poetry to path
    PATH="$POETRY_HOME/bin"

# Install build stuff
RUN apt-get update && \
    apt-get install --yes --no-install-recommends build-essential

# Install poetry
RUN pip install pipx
RUN pipx install "poetry==$POETRY_VERSION"
RUN pipx ensurepath

# Install project dependencies
WORKDIR /app
COPY pyproject.toml .
RUN poetry install --no-dev --no-root --no-ansi

# Install project and basic tests on app
COPY . .
RUN poetry install --no-dev --no-interaction --no-ansi && \
    python -m {{ cookiecutter.__project_slug }} --version

# Run app
CMD ["python3", "-m", "{{ cookiecutter.__project_slug }}", "--log-file", "logs", "hello"]
