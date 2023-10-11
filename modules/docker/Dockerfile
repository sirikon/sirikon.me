FROM python:3.12-slim-bookworm AS base
WORKDIR /build

# # http://git.elenq.tech/guile-neocities/
# RUN apt-get update && \
#   apt-get install -y wget sudo
# RUN wget http://cdn.elenq.tech/guile-neocities-deb-pack.deb
# RUN apt-get install -y ./guile-neocities-deb-pack.deb
# ENV PATH="${PATH}:/gnu/store/khwpa6z35f4cs0bc2zbfwjxs0ihm74gn-guile-neocities-0.1/bin"

# Install Neocities official CLI until I figure out a way to make
# Ekaitz's guile-neocities package work here.
RUN apt-get update && \
  apt-get install -y ruby-full && \
  gem install neocities  

COPY ./modules/generator/requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /workspace
ENV PYTHONPATH="/workspace/modules/generator"
