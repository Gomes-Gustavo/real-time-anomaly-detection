# --- Stage 1: Builder ---
# In this stage, we install all python dependencies in a clean virtual environment.
FROM python:3.10-slim as builder

# Set the working directory inside the image
WORKDIR /app

# Install Poetry, the dependency manager
RUN pip install poetry

# Configure Poetry to create the virtual environment inside the project directory
RUN poetry config virtualenvs.in-project true

# Copy only the dependency definition files to leverage Docker's layer caching
COPY pyproject.toml poetry.lock ./

# Install only the PRODUCTION dependencies.
RUN poetry install --without dev --no-root


# --- Stage 2: Final Image ---
# We start from a clean slim image again to keep the final image size small.
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the virtual environment with the pre-installed dependencies from the builder stage
COPY --from=builder /app/.venv ./.venv

# Activate the virtual environment by adding its bin directory to the system's PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy our application source code and the trained model
COPY src/ ./src
COPY models/ ./models

# Expose port 80, the standard port for HTTP traffic, to the container's network
EXPOSE 80

# The command to start our application when a container is run from this image.
# --host 0.0.0.0 makes the API accessible from outside the container.
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "80"]