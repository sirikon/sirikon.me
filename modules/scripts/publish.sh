#!/usr/bin/env bash
set -euo pipefail

root="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../"
docker compose \
  -f "${root}/docker-compose.yml" \
  -f "${root}/modules/docker/docker-compose.yml" \
  run --build sirikon-neocities ls -lah /
