#!/usr/bin/env bash
set -euo pipefail

readonly EXPECTED_BUTANO_VERSION="18.1.0"
readonly EXPECTED_DEVKITARM_RELEASE="65"
readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly BUTANO_PATH="${BUTANO:-${ROOT}/external/butano}"

[[ -n "${DEVKITPRO:-}" ]] || { echo 'DEVKITPRO is not set' >&2; exit 1; }
[[ -n "${DEVKITARM:-}" ]] || { echo 'DEVKITARM is not set' >&2; exit 1; }
command -v arm-none-eabi-g++ >/dev/null || { echo 'arm-none-eabi-g++ is not on PATH' >&2; exit 1; }
[[ -f "${BUTANO_PATH}/butano.mak" ]] || { echo "Butano not found: ${BUTANO_PATH}" >&2; exit 1; }

butano_version="$(git -C "${BUTANO_PATH}" describe --tags --exact-match 2>/dev/null || true)"
[[ "${butano_version#v}" == "${EXPECTED_BUTANO_VERSION}" ]] || {
    echo "Expected Butano ${EXPECTED_BUTANO_VERSION}; found '${butano_version:-unknown}'" >&2
    exit 1
}

version_file="${DEVKITARM}/.version"
if [[ -f "${version_file}" ]]; then
    installed_release="$(tr -cd '0-9' < "${version_file}")"
    [[ "${installed_release}" == "${EXPECTED_DEVKITARM_RELEASE}" ]] || {
        echo "Expected devkitARM r${EXPECTED_DEVKITARM_RELEASE}; found $(cat "${version_file}")" >&2
        exit 1
    }
else
    echo "Warning: ${version_file} is unavailable; devkitARM release cannot be verified." >&2
fi

echo "Butano ${EXPECTED_BUTANO_VERSION} and devkitARM r${EXPECTED_DEVKITARM_RELEASE} verified"
