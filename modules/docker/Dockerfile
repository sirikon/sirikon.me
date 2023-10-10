FROM debian:bookworm-slim AS base
WORKDIR /workdir

# # http://git.elenq.tech/guile-neocities/
# RUN apt-get update && \
#   apt-get install -y wget sudo
# RUN wget http://cdn.elenq.tech/guile-neocities-deb-pack.deb
# RUN apt-get install -y ./guile-neocities-deb-pack.deb
# ENV PATH="${PATH}:/gnu/store/wrckfh2jbd2l6pivmf1xpkcmhk6whpj0-guile-neocities-0.1/bin"

# Install Neocities official CLI until I figure out a way to make
# Ekaitz's guile-neocities package work here.
RUN apt-get update && \
  apt-get install -y ruby-full && \
  gem install neocities  
