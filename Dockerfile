FROM python:3.10-slim

# https://docs.python.org/3/using/cmdline.html#envvar
# https://pip.pypa.io/en/stable/user_guide/#environment-variables
# https://python-poetry.org/docs/configuration/
ENV PYTHONFAULTHANDLER=1 \ 
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.12 \
    POETRY_VIRTUALENVS_CREATE=0\
    PYTHONPATH="${PYTHONPATH}:/code/src"

RUN apt-get update && apt-get install -y curl git && pip install --upgrade pip "poetry==${POETRY_VERSION}"

WORKDIR /code

# Install Python dependencies.
COPY pyproject.toml ./


RUN poetry install

# Only now copy the code into the container. Everything before this will be cached
# even with code changes.
COPY . .
RUN poetry install


RUN useradd -m yelloow_user && chown -R yelloow_user /code

USER yelloow_user

ENTRYPOINT ["/bin/sh", "on_startup.sh"]
