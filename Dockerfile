################################
# PYTHON-BASE
################################
FROM python:3.11.6-slim-bookworm as python-base

# Sets up all our shared environment variables
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.7.0 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


################################
# BUILDER-BASE
# Used to build deps + create our virtual environment
################################
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# Install poetry - respects $POETRY_VERSION & $POETRY_HOME
# The --mount will mount the buildx cache directory to where
# Poetry and Pip store their cache so that they can re-use it
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY pyproject.toml pyproject.toml

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry install --without dev


################################
# DEVELOPMENT
# Image used during development / testing
################################
FROM python-base as development
ENV FASTAPI_ENV=development

# will become mountpoint of our code
ENV DIR="/src"
RUN mkdir ${DIR} && chown -fR ${USER}:${USER} ${DIR}

WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN --mount=type=cache,target=/root/.cache \
    poetry install --with=dev

WORKDIR /src
# Copy the project files
COPY --chown=${USER} app app
COPY --chown=${USER} migrations migrations
COPY --chown=${USER} scripts scripts
COPY --chown=${USER} tests tests
COPY --chown=${USER} alembic.ini alembic.ini
