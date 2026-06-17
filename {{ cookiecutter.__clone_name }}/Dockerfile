FROM python:3.14-slim-bookworm

# Metadata for clarity and documentation
LABEL maintainer={{ cookiecutter.email | tojson() }}
LABEL description="Docker image for {{ cookiecutter.__project_slug }}"

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    # compilations
    build-essential \
    # UV
    curl ca-certificates \
    # Clean-up
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/0.8.7/install.sh /uv-installer.sh

# Run the installer then remove it
RUN env UV_INSTALL_DIR="/bin" sh /uv-installer.sh && rm /uv-installer.sh

# Add non-root user
RUN useradd --create-home --shell /sbin/nologin {{ cookiecutter.__project_slug }}

# Disable development dependencies
ENV UV_NO_DEV=1

# Create directory
RUN mkdir -p /data /app && chown {{ cookiecutter.__project_slug }}:{{ cookiecutter.__project_slug }} /data /app

# Use non-root user for security
USER {{ cookiecutter.__project_slug }}

# Change the working directory to the `src` directory
WORKDIR /app

# Copy only project definition files (improves caching)
COPY --chown={{ cookiecutter.__project_slug }}:{{ cookiecutter.__project_slug }} pyproject.toml /app

# Install dependencies
RUN uv sync --no-install-project --no-cache

# Copy the project into the image
COPY --chown={{ cookiecutter.__project_slug }}:{{ cookiecutter.__project_slug }} . .

# Fix permissions
RUN chmod +x /app/entrypoint.sh

# Sync the project
RUN uv sync --frozen --no-cache

# Default command (use exec form for signal handling)
CMD ["uv", "run", "--frozen", "--no-cache", "run"]
