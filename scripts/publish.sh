#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH="$(pwd)/src/python"
export PYTHONPATH

poetry run python -m sirikon-blog build

cd "./output"
while IFS= read -r line; do
  echo "Uploading ${line:1}"
  NEOCITIES_KEY="${NEOCITIES_API_KEY}" neocities upload "${line}" "${line:1}"
  echo ""
done <<<"$(find ./ -type f)"
