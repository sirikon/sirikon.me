#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH="$(pwd)/src/python"
export PYTHONPATH

function main() {
  trap cleanup EXIT
  log "Starting server on http://127.0.0.1:8000"
  poetry run python -m sirikon_me watch &
  poetry run python -m http.server --directory output 8000 &
  wait -n
}

function cleanup() {
  log "Cleaning up"
  jobs -l
  for job_pid in $(jobs -p); do
    log "Killing ${job_pid}"
    kill -9 "$job_pid" || true
  done
}

function log() {
  printf "### [start.sh] %s\n" "$@"
}

main "$@"
