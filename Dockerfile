FROM python:3.11-slim-buster as builder

ARG DEBIAN_FRONTEND=noninteractive

RUN pip install poetry==1.8.5

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

FROM python:3.11-slim-buster as final

RUN apt-get update && apt-get install --no-install-recommends -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PYTHONPATH=/app/
ENV PYTHON_PACKAGES_DIR=/usr/local/lib/python3.11/site-packages
ENV PYTHON_BINARIES_DIR=/usr/local/bin

COPY --from=builder $PYTHON_PACKAGES_DIR $PYTHON_PACKAGES_DIR
COPY --from=builder $PYTHON_BINARIES_DIR $PYTHON_BINARIES_DIR
COPY application-local.yaml poetry.lock pyproject.toml README.md ./
COPY food_review_api ./food_review_api
RUN poetry install --only main

COPY run.sh ./
ENTRYPOINT [ "/app/run.sh" ]
