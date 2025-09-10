FROM python:3.12-bookworm as base


ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=2.1.2

RUN mkdir /app
WORKDIR /app

FROM base as builder
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install "poetry==$POETRY_VERSION" && \
    poetry config virtualenvs.in-project true && \
    poetry install --only main --no-root


FROM base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update && apt-get install -y gettext libgettextpo-dev
COPY --from=builder /app/.venv /app/.venv
WORKDIR /app
COPY src .
RUN ./.venv/bin/python manage.py collectstatic -c --noinput && \
    ./.venv/bin/python manage.py compilemessages
CMD [".venv/bin/daphne", "-b", "0.0.0.0", "s15.asgi:application"]
