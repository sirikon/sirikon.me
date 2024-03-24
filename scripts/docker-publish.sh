#!/usr/bin/env bash
set -euo pipefail

PYTHON_VERSION="$(grep python <.tool-versions | cut -d ' ' -f 2)"
TAG="sirikon-blog-devenv:$(date -u '+%Y%m%d_%H%M%S')"
docker build \
  --build-arg PYTHON_VERSION="${PYTHON_VERSION}" \
  --file docker/Dockerfile \
  --tag "${TAG}" \
  .

docker run \
  -t -v ./:/wd \
  -e NEOCITIES_API_KEY="${NEOCITIES_API_KEY}" \
  "${TAG}" \
  bash -c '/wd/scripts/install.sh && /wd/scripts/publish.sh'
