#!/usr/bin/env bash
set -euo pipefail

readonly EXPECTED_BUTANO_VERSION="18.1.0"
readonly EXPECTED_DEVKITARM_RELEASE="65"
readonly ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readonly BUTANO_PATH="${BUTANO:-${ROOT}/external/butano/butano}"
readonly BUTANO_REPOSITORY="$(cd "${BUTANO_PATH}/.." 2>/dev/null && pwd -P || true)"

[[ -n "${DEVKITPRO:-}" ]] || { echo 'DEVKITPRO is not set' >&2; exit 1; }
[[ -n "${DEVKITARM:-}" ]] || { echo 'DEVKITARM is not set' >&2; exit 1; }
command -v arm-none-eabi-g++ >/dev/null || { echo 'arm-none-eabi-g++ is not on PATH' >&2; exit 1; }
[[ -f "${BUTANO_PATH}/butano.mak" ]] || { echo "Butano not found: ${BUTANO_PATH}" >&2; exit 1; }

[[ -n "${BUTANO_REPOSITORY}" && -e "${BUTANO_REPOSITORY}/.git" ]] || {
    echo "Butano Git checkout not found: ${BUTANO_REPOSITORY:-unknown}" >&2
    exit 1
}
checked_out_commit="$(git -C "${BUTANO_REPOSITORY}" rev-parse HEAD 2>/dev/null || true)"
pinned_commit="$(git -C "${BUTANO_REPOSITORY}" rev-parse "refs/tags/${EXPECTED_BUTANO_VERSION}^{commit}" 2>/dev/null || true)"
[[ -n "${checked_out_commit}" && "${checked_out_commit}" == "${pinned_commit}" ]] || {
    echo "Expected Butano ${EXPECTED_BUTANO_VERSION}; checkout is not at the pinned tag" >&2
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
