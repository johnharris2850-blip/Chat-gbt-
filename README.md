# Pokémon Crown & Chaos

A custom Pokémon adventure project.

## Main Adventure

- Player: John
- John's starter: Water type
- Candy's starter: Fire type
- Target: 40+ hour story-driven adventure
- Platform target: Game Boy Advance / 44VBA

## Development

Crown & Chaos will be developed in stages, including:

- Main story and side quests
- Original region and locations
- John and Candy's adventure
- Pokémon encounters and trainers
- Gyms and major battles
- Villains and rivals
- Catholic-inspired themes and symbolism
- Post-game content
- Balancing, bug fixing and final testing

## Current Status

Development started September 2026.

## Development Foundation

The project will be an **original clean-room game built with the open-source
[Butano](https://github.com/GValiente/butano) C++ engine and devkitARM**, rather
than a patch or modification of a commercial ROM. This keeps the source,
characters, maps, writing, art, audio, and data under this project's control and
gives the team a reproducible path to a `.gba` build.

> **Legal and creative boundary:** do not commit commercial ROMs, extracted
> Nintendo/Pokémon assets or data, proprietary fonts or music, encryption keys,
> or unlicensed third-party material. Placeholder and final content must be
> original or have a clearly documented compatible license.

### Repository map

- `src/` and `include/` — future C++ game implementation and headers
- `graphics/`, `audio/`, and `dmg_audio/` — source assets for Butano's converters
- `data/` — authored game data such as maps, encounters, dialogue, and quests
- `tools/` — validation and content-pipeline utilities
- `tests/` — host-side automated tests and test fixtures
- `docs/` — focused technical and production documentation
- [`PROJECT_PLAN.md`](PROJECT_PLAN.md) — delivery roadmap and quality gates
- [`GAME_DESIGN.md`](GAME_DESIGN.md) — creative vision and content targets
- [`DEVELOPMENT_STATUS.md`](DEVELOPMENT_STATUS.md) — milestone checklist

No engine or SDK is vendored. Dependencies remain external and version-pinned;
see the current milestone evidence and recommended next task in
`DEVELOPMENT_STATUS.md`.

### Bootstrap build

The first playable vertical slice contains an original fantasy title and six-page
intro, John's furnished bedroom and house, the village of Crownhaven, and the Old
Road finale. John and four distinct NPCs have original pixel sprites; movement,
collision, interaction dialogue, an objective flag, screen shake, a START menu,
and versioned world-state saving are all implemented. Toolchain installation and build commands are documented in
[`docs/BUILDING.md`](docs/BUILDING.md). The expected local build output is
`crown_and_chaos.gba`; build products remain intentionally untracked.
All placeholder BMP and WAV inputs are also generated locally from tracked source
code and JSON at build time, avoiding binary files in pull-request diffs.

Quick repository-only checks, which do not require the GBA SDK:

```sh
python3 tools/check_project.py
python3 tools/generate_placeholder_assets.py --check
```
