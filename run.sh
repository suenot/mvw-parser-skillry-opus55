#!/bin/sh
# Usage: ./run.sh [--limit N] [--no-media]. Data goes to $MVW_DATA or <workspace>/warehouse.
cd "$(dirname "$0")" && PYTHONPATH=../mvw-core exec python3 -m mvw_parser_skillry_opus55 "$@"
