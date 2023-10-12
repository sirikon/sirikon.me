#!/usr/bin/env bash
set -euo pipefail

root="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../"
cd "$root"
rm -rf ./output
python -m sirikon-neocities build

if [ "${NEOCITIES_CLI_FLAVOR}" == "guile" ]; then
  cd "./output"
  while IFS= read -r line; do
    echo "Uploading ${line:1}"
    NEOCITIES_KEY="${NEOCITIES_API_KEY}" neocities upload "${line}" "${line:1}"
    echo ""
  done <<<"$(find ./ -type f)"
elif [ "${NEOCITIES_CLI_FLAVOR}" == "official" ]; then
  neocities push ./output
else
  echo "Unknown flavor Neocities CLI flavor ${NEOCITIES_CLI_FLAVOR}"
fi
