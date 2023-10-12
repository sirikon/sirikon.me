FROM python:3.12-slim-bookworm AS base
WORKDIR /build
COPY ./modules/generator/requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /workspace
ENV PYTHONPATH="/workspace/modules/generator"

FROM base AS publish-with-guile-neocities
ENV NEOCITIES_CLI_FLAVOR=guile
# http://git.elenq.tech/guile-neocities/
RUN apt-get update && \
  apt-get install -y wget sudo
RUN wget http://cdn.elenq.tech/guile-neocities-deb-pack.deb
RUN apt-get install -y ./guile-neocities-deb-pack.deb
ENV PATH="${PATH}:/gnu/store/mhy5xdqngrb6bi8xaw6d0k28inzjnsdr-guile-neocities-0.1/bin"

FROM base AS publish-with-official-neocities
ENV NEOCITIES_CLI_FLAVOR=official
# Install Neocities official CLI
RUN apt-get update && \
  apt-get install -y ruby-full && \
  gem install neocities  
