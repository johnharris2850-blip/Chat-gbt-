#!/usr/bin/env bash
set -euo pipefail

readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly OUTPUT="${TMPDIR:-/tmp}/crown_save_layout_test"

python3 -m unittest discover -s "${ROOT}/tests" -v
g++ -std=c++17 -Wall -Wextra -Wpedantic -Werror -I"${ROOT}/include" \
    "${ROOT}/tests/save_layout_test.cpp" -o "${OUTPUT}"
"${OUTPUT}"
echo "host tests passed"
