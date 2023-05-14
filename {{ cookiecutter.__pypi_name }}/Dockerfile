FROM python:3.11

WORKDIR /app

# Install dependencies
RUN python3 -m pip install --no-cache-dir toml>=0.10.2
COPY pyproject.toml pyproject.toml
RUN python3 -m pip `python3 -c "import toml;print(' '.join(toml.loads(open('pyproject.toml', 'r', encoding='utf-8').read()).get('project', {}).get('dependencies', [])))"`

# Install and build app
COPY . .
RUN python3 -m pip install --no-cache-dir .

# Run app
CMD python -u -m {{ cookiecutter.__pypi_name }}
