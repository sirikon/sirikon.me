#!/usr/bin/env bash
set -euo pipefail

PYTHONPATH="$(pwd)/src"
export PYTHONPATH
exec ./.venv/bin/python -m sirikon_me.freeze
