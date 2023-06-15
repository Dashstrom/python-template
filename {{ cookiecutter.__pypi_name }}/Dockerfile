FROM python:3.8

WORKDIR /app

# Install build stuff
RUN apt-get update && \
    apt-get install --yes --no-install-recommends gcc g++ libffi-dev

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools>=62.0.0 pip>=21.3 && \
    pip install --no-cache-dir toml>=0.10.2
COPY pyproject.toml .
RUN python3 -c 'import toml;print("\n".join(toml.loads(open("pyproject.toml", "r", encoding="utf-8").read()).get("project", {}).get("dependencies", [])))' > requirements-generated.txt
RUN pip install --no-cache-dir -r requirements-generated.txt
RUN rm -f requirements-generated.txt

# Install and build app
COPY . .
RUN python3 -m pip install --no-cache-dir .

# Run app
CMD python -u -m {{ cookiecutter.__pypi_name }}
