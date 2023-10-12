#!/usr/bin/env bash
set -euo pipefail

root="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../"
cd "$root"
rm -rf ./output
python -m sirikon-neocities build

# # Neocities official CLI
# neocities push ./output

# guile-neocities
cd "./output"
while IFS='\n' read -r line; do
  echo "Uploading ${line:1}"
  NEOCITIES_KEY="${NEOCITIES_API_KEY}" neocities upload "${line}" "${line:1}"
  echo ""
done <<< "$(find ./ -type f)"
