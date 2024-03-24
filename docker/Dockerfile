ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-bookworm
RUN apt-get update && apt-get install -y wget sudo
RUN wget http://cdn.elenq.tech/guile-neocities-deb-pack.deb
RUN apt-get install -y ./guile-neocities-deb-pack.deb
ENV PATH="${PATH}:/gnu/store/mhy5xdqngrb6bi8xaw6d0k28inzjnsdr-guile-neocities-0.1/bin"
ARG POETRY_VERSION
ENV POETRY_VERSION="${POETRY_VERSION}"
ENV POETRY_HOME /poetry
ENV PATH="/poetry/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python -
WORKDIR /wd
