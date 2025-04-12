ARG PYTHON_VERSION=3.13.3
FROM python:${PYTHON_VERSION}-slim-bookworm

# Poetry
RUN apt-get update && apt-get install -y curl
ARG POETRY_VERSION=2.1.2
ENV POETRY_VERSION="${POETRY_VERSION}"
ENV POETRY_HOME="/poetry"
ENV PATH="/poetry/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR /wd
COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./meta ./meta
RUN ./meta/install.sh
COPY ./src ./src
RUN ./meta/build.sh
RUN mv ./output /dist
