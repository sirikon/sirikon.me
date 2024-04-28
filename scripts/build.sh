#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH="$(pwd)/src/python"
export PYTHONPATH

poetry run python -m sirikon_me build
