#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="$(pwd)/src"
exec ./.venv/bin/python -m sirikon_me.freeze
