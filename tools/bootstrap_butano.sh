#!/usr/bin/env bash
set -euo pipefail

readonly BUTANO_VERSION="18.1.0"
readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly DESTINATION="${BUTANO_REPOSITORY:-${ROOT}/external/butano}"

if [[ -e "${DESTINATION}" ]]; then
    echo "Refusing to replace existing path: ${DESTINATION}" >&2
    exit 1
fi

git clone --branch "${BUTANO_VERSION}" --depth 1 \
    https://github.com/GValiente/butano.git "${DESTINATION}"
echo "Installed Butano ${BUTANO_VERSION} at ${DESTINATION}"
echo "Set BUTANO=${DESTINATION}/butano when building Crown & Chaos"
