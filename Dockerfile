############
# Virtualenv
############
FROM python:3.11-alpine3.18 AS builder
# .build-deps build-base libffi-dev git rust cargo openssl-dev
RUN apk add --update --no-cache --virtual .build-deps build-base libffi-dev
RUN python -m venv --copies /opt/venv

ENV PATH="/opt/venv/bin:$PATH" \
    POETRY_VERSION=1.7.0

COPY poetry.lock pyproject.toml /tmp/

RUN pip install --upgrade pip \
  && pip install --no-cache-dir "poetry==$POETRY_VERSION"
RUN cd /tmp  \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi \
  && rm -fr /tmp/poetry.lock /tmp/pyproject.toml

#########
# Runtime
#########
FROM python:3.11-alpine as runtime

RUN #apk add --no-cache binutils

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY . .

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "-m", "app"]
