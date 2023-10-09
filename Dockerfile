FROM debian:bookworm-slim
WORKDIR /workdir
RUN apt-get update && apt-get install -y wget

# @Ekaitz lol
# http://git.elenq.tech/guile-neocities/
RUN wget http://cdn.elenq.tech/guile-neocities-deb-pack.deb
RUN apt-get install -y ./guile-neocities-deb-pack.deb
ENV PATH="${PATH}:/gnu/store/fis13hgjw3pszbqgvps9xjm7vm9d1rcf-guile-neocities-0.1/bin"
