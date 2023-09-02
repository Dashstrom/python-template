FROM python:3.8

WORKDIR /app

# Install build stuff
RUN apt-get update && \
    apt-get install --yes --no-install-recommends gcc g++ libffi-dev

# Install dependencies
COPY pyproject.toml .
ENV PIP_INDEX_URL $PIP_INDEX_URL
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir 'setuptools==67.8.0' 'pip>=21.3' 'toml>=0.10.2' && \
    python3 -c 'import toml;print("\n".join(toml.loads(open("pyproject.toml", "r", encoding="utf-8").read()).get("project", {}).get("dependencies", [])))' > requirements-generated.txt && \
    pip install --no-cache-dir -r requirements-generated.txt && \
    rm -f requirements-generated.txt
ENV PYTHON_SETUPTOOLS_VERSION 67.8.0

# Install and basic tests on app
COPY . .
RUN python3 -m pip install --no-cache-dir . && \
    python -u -m {{ cookiecutter.__project_slug }} --version && \
    python -u -m {{ cookiecutter.__project_slug }} --help

# Run app
CMD ["python3", "-u", "-m", "{{ cookiecutter.__project_slug }}", "--log-file", "logs", "hello"]
