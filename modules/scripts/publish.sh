#!/usr/bin/env bash
set -euo pipefail

root="$(dirname "$(realpath "${BASH_SOURCE[0]}")")/../../"
cd "$root"
python -m sirikon-neocities build
neocities push ./output
