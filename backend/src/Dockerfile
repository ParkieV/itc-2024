FROM python:3.12.5 AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

FROM base AS base_with_req

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml .

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH" && \
    poetry lock --no-cache && \
    poetry install --no-cache && \
    poetry cache clear pypi --all && \
    poetry cache clear virtualenvs --all && \
    find / -type f -name '*.py[cod]' -delete && \
    find / -type f -name '*.whl' -delete

FROM base_with_req

WORKDIR /src

COPY backend/ .

CMD ["python", "-m", "src.main"]
