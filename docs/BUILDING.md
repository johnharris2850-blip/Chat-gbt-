# Building Crown & Chaos

## Pinned dependencies

| Dependency | Pin | Purpose |
| --- | --- | --- |
| Butano | tag `18.1.0` | GBA engine and asset pipeline |
| devkitARM | release `r65` | ARM cross-compiler/toolchain |
| Python | 3.10 or newer | deterministic project checks/assets |

The pins are the supported Task 2 baseline, not an instruction to silently use
the newest release. Upgrade them in a dedicated commit after a clean build and
emulator regression. Butano is fetched outside version control into `external/`;
the SDK and generated ROM are not committed.

## Install prerequisites

Install devkitPro's `gba-dev` group using the official instructions for the host
operating system. Confirm that `DEVKITPRO` and `DEVKITARM` are exported and that
`arm-none-eabi-g++` is on `PATH`. A compatible shell, Git, GNU Make, and Python
3.10+ are also required.

The exact supported devkitARM release is `r65`. Package managers can move past an
old release; if the official repository no longer offers it, use devkitPro's
documented archive/container mechanism rather than an unofficial compiler build.
Record any approved pin change in this file and `DEVELOPMENT_STATUS.md`.

## Bootstrap and build

From the repository root:

```sh
python3 tools/generate_placeholder_assets.py --check
python3 tools/check_project.py
tools/bootstrap_butano.sh
tools/check_toolchain.sh
make -f make/host.mk assets
make -j1
```

To use an existing checkout of the pinned engine:

```sh
BUTANO=/absolute/path/to/butano-repository/butano tools/check_toolchain.sh
make -j1 BUTANO=/absolute/path/to/butano-repository/butano
```

The upstream repository contains the engine in its `butano/` subdirectory; the
repository root itself is not the SDK include path and does not contain
`butano.mak`. The standard root project configuration assigns this SDK path to
Butano's required `LIBBUTANO` variable before including
`$(LIBBUTANO)/butano.mak`; Butano then uses its canonical absolute form to locate
the adjacent `butano_dka.mak`.

The expected output is `crown_and_chaos.gba` in the repository root. Build output
and ROMs are ignored by Git. The root `Makefile` follows Butano's standard project
layout because Butano reinvokes that same absolute Makefile from the `build/`
directory while compiling and linking. Generate assets before invoking the
default build. Run `make -f make/host.mk clean` before a reproducibility build.
`make -f make/host.mk assets` runs the deterministic generator before the default Butano build,
creating the ignored `graphics/*.bmp` and `audio/*.wav` inputs from the tracked
Python and JSON sources. CI performs these two steps explicitly. These generated
binaries must never be committed. `make -f make/host.mk clean`
removes them along with the ROM and object output; `make -f make/host.mk verify` runs all host
checks without requiring generated binaries to be present.

Every push and pull request also runs `.github/workflows/checks.yml`. Its GBA job
uses the pinned `devkitpro/devkitarm:20241104` container, fetches Butano 18.1.0,
builds the ROM, records its SHA-256 checksum, and uploads both files as the
`crown-and-chaos-gba-<commit>` artifact. On GitHub, open the commit's **Actions**
run, select **Artifacts**, and download that artifact. A workflow artifact is a
test build, not a commercial-ROM patch and does not require any base ROM.
The workflow explicitly exports `/opt/devkitpro/devkitARM/bin` through
`GITHUB_PATH` and verifies `arm-none-eabi-g++` before running the same strict
toolchain check used by local builds.
The dependency repository is checked out by `actions/checkout` directly under
the workspace at `external/butano`; its build entry point is
`external/butano/butano/butano.mak`. After checkout, the verification step logs the incoming
`BUTANO`, `GITHUB_WORKSPACE`, physical working directory, and resolved dependency
path. It canonicalizes the engine's
`${GITHUB_WORKSPACE}/external/butano/butano` subdirectory with `realpath`, exports
that exact container path through `GITHUB_ENV`, and only then
performs the location, Git metadata, pinned-tag commit, and `butano.mak` checks
used by compilation. Because `actions/checkout` creates the nested checkout on
the runner before the devkitPro container consumes it, the workflow marks only
this canonical dependency path as a Git safe directory. Version verification
compares `HEAD` directly with the peeled `refs/tags/18.1.0` commit instead of
depending on the display text returned by `git describe`.

## Emulator smoke test

1. Serve or transfer `crown_and_chaos.gba` to the current 44VBA installation on
   the target iPhone; do not distribute it with unrelated ROM material.
2. Confirm the Crown & Chaos title and **PRESS START** appear.
3. Press START and confirm John appears in Pilgrim's Rest.
4. Walk in four directions; confirm animation, collision, and camera follow.
5. Enter and leave John's home through its door.
6. Face Elder Mara and press A; advance both dialogue pages and hear the cue.
7. Find the old garden secret and confirm its visual marker and message.
8. Open/close the START menu, then close the emulator normally and reload; confirm
   John's location, direction, map, NPC interaction, and secret state persist.
9. Repeat in an independent GBA emulator and record emulator/browser/device
   versions in the status document or test report.

The interaction cue is a project-generated 0.1-second waveform. The save service
writes a versioned, checksummed 32-byte SRAM record at boot, transitions,
discoveries, NPC interaction, and START-menu opening.

## Reproducibility record

For a release or milestone build, retain the output of:

```sh
git rev-parse HEAD
git -C external/butano describe --tags --exact-match
arm-none-eabi-g++ --version
sha256sum crown_and_chaos.gba
stat -c '%n %s bytes' crown_and_chaos.gba
```

Do not commit the ROM. Attach its checksum and test matrix to the relevant release
record instead.
