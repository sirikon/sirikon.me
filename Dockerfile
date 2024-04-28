ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim-bookworm
RUN apt-get update && apt-get install -y curl
ARG POETRY_VERSION=1.8.2
ENV POETRY_VERSION="${POETRY_VERSION}"
ENV POETRY_HOME /poetry
ENV PATH="/poetry/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python -
WORKDIR /wd
COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./scripts ./scripts
RUN ./scripts/install.sh
COPY ./src ./src
RUN ./scripts/build.sh
RUN mv ./output /output
