# Pokémon Crown & Chaos — Project Plan

## 1. Purpose and boundaries

This roadmap turns the concept into a polished, original 40+ hour GBA
monster-battling adventure while keeping each development task reviewable.
It is a planning baseline, not a promise to produce the whole game at once.

The project is a clean-room original implementation. It must not depend on a
commercial Pokémon ROM, disassembly, extracted data, proprietary assets,
encryption keys, or copyrighted music. Every dependency and asset must have its
origin and license recorded before release. “Pokémon-style” describes the genre
and hardware target; the shipped world, creatures, characters, text, visuals,
audio, and code must be original or properly licensed.

## 2. Selected technical approach

Use **Butano**, an open-source C++ engine for Game Boy Advance, with the
**devkitARM/devkitPro** toolchain. Build original game systems and content as a
standalone ROM rather than making a ROM hack.

Why this approach:

- It emits native `.gba` binaries and exposes GBA-friendly sprites, backgrounds,
  audio, input, save memory, and profiling abstractions.
- Modern C++ and data-generation tools are more maintainable for a multi-year,
  content-heavy project than writing all systems directly in assembly/C.
- A standalone build avoids redistributing or asking for a copyrighted base ROM.
- Engine examples support incremental vertical slices and hardware-budget checks.

Trade-offs: a party-battler, map/quest runtime, editors, AI, save migrations, and
all content still need to be authored. GBA memory, CPU, palette, tile, cartridge,
and audio limits must remain design constraints. Pin an audited Butano version;
do not vendor it until its license and update process are documented.

## 3. Production principles

1. **Vertical slices before volume.** Prove traversal, dialogue, battle, capture,
   progression, and save/load with temporary original assets before mass content.
2. **Data-driven content.** Maps, creatures, moves, trainers, items, dialogue,
   quests, and encounters should be validated source data, not scattered C++.
3. **Hardware-first budgets.** Track ROM, EWRAM/IWRAM, VRAM, object/palette,
   frame-time, and save-space budgets continuously on representative scenes.
4. **Original-by-default.** Keep an asset manifest containing author, source,
   license, modification notes, and attribution requirements.
5. **Deterministic builds.** Pin tools/dependencies and make clean builds possible
   in CI. Never commit built ROMs or save files.
6. **Testable milestones.** A milestone closes only after its exit criteria pass
   in emulator plus scheduled real-hardware checks where available.
7. **Respectful themes.** Fictional Catholic-inspired imagery should emphasize
   mercy, conscience, sacrifice, stewardship, hope, and human dignity; obtain
   sensitivity review and avoid presenting fictional doctrine as real teaching.

## 4. Phased roadmap

### Phase 0 — Foundation and preproduction

- Ratify the design pillars, audience, content rating, legal policy, naming
  process, source-control conventions, and decision log.
- Install and pin devkitARM and Butano; produce a reproducible minimal `.gba`.
- Add build, format, lint, asset validation, ROM-size reporting, emulator smoke
  testing, CI, and third-party notices.
- Define technical budgets, data schemas, stable IDs, content ownership, and the
  save-version/migration policy.
- Prototype the map/content workflow before committing to an editor.

**Exit:** a clean checkout produces an original input-responsive ROM; automated
checks run; dependency licenses and setup instructions are recorded.

### Phase 1 — Core technology prototypes

- Overworld: tiled maps, collision, camera, warps, NPC schedules, interactions,
  signs, triggers, cutscenes, menus, transitions, and debug teleport.
- Battle: turn loop, stats, elemental interactions, moves, status, switching,
  victory/defeat, experience, leveling, and deterministic seeded simulations.
- Collection: encounters, capture-equivalent recruitment, party/storage, bestiary,
  evolution, inventory, equipment/held-item equivalent, healing, and shops.
- Persistence: atomic saves, checksum, multiple safe slots if feasible, options,
  play time, story/quest flags, and corrupt-save recovery behavior.
- Audio/UI/accessibility prototypes and profiling overlays.

**Exit:** integrated “gray-box loop” supports explore → encounter → battle →
recruit → heal → save/reload without state loss and within provisional budgets.

### Phase 2 — Vertical slice

Create 45–90 polished minutes: opening, John selecting the Water starter, Candy
selecting the Fire starter, one settlement, one route, a small dungeon, quests,
trainers, a rival encounter, a villain tease, and a major battle. Use a small set
of release-quality original creatures, music, UI, effects, and dialogue.

**Exit:** external playtesters can finish without developer help; save continuity,
performance, difficulty, onboarding, and content pipeline are validated.

### Phase 3 — Full production: first act

- Lock the regional topology, critical path, progression gates, full narrative
  outline, character arcs, creature roster plan, and art/audio style guides.
- Build the opening hub, early routes/dungeons, first 2–3 major progression
  battles, initial villain operations, and early optional quest chains.
- Establish encounter/battle telemetry and repeatable playtest reporting.

**Exit:** Act I is content-complete with no progression blockers.

### Phase 4 — Full production: middle acts

- Produce towns, routes, traversal upgrades, dungeons, gyms/major trials, rivals,
  villain escalation, secrets, and side quests in reviewable content batches.
- Add mid-game systems only when they deepen existing loops; avoid uncontrolled
  feature growth.
- Run balance simulations and milestone playthroughs after every content batch.

**Exit:** Acts II–III are complete, all core mechanics are locked, and the whole
critical path is playable with temporary content only where explicitly tracked.

### Phase 5 — Finale and content-complete alpha

- Implement the final city/dungeons, last major battles, villain resolution,
  championship sequence, ending, credits, and post-game unlock transition.
- Complete roster, moves, items, NPCs, dialogue, maps, quests, and cinematics.
- Freeze new features; triage bugs by severity and assign performance/memory work.

**Exit:** every planned main and optional activity is reachable; a start-to-credits
playthrough succeeds on a fresh save; no placeholder content remains untracked.

### Phase 6 — Post-game production

- Add the post-game story chapter, rematches, challenge facility, high-level
  exploration zone, superbosses, collection completion, and resolved quest arcs.
- Ensure rewards support continued play rather than merely raising completion
  counters.

**Exit:** post-game has a clear opening, several meaningful goals, and a capstone;
all content respects save/ROM/performance budgets.

### Phase 7 — Alpha, balance, accessibility, and polish

- Full regression passes for progression flags, warps, softlocks, battle edge
  cases, economy, encounters, text overflow, collision, saves, and idle behavior.
- Tune difficulty curves for main path and optional challenge; verify the Water
  and Fire starter arcs remain fair without erasing their identities.
- Polish feedback, animation, sound, UI consistency, tutorial pacing, navigation,
  text speed, control remapping where feasible, and photosensitivity concerns.
- Conduct narrative, cultural, theological-sensitivity, and copy-editing reviews.

**Exit:** zero known blockers/critical defects; performance budgets pass in stress
scenes; representative players finish without intervention.

### Phase 8 — Release candidate and 44VBA validation

- Produce a clean pinned-toolchain build and record hashes, compiler/engine
  versions, ROM/save sizes, and release notes.
- Test new game, save/reload, suspend/resume, audio, controls, major transitions,
  credits, post-game unlock, and long-session stability in the current supported
  44VBA release on representative browsers/devices.
- Cross-check in at least one accuracy-focused emulator and real GBA-compatible
  hardware/flash cartridge when legally and practically available.
- Test upgrades from every supported save version and confirm corrupted saves fail
  safely. Confirm no debug menus, licensed placeholders, secrets, or local paths.

**Exit:** signed release checklist, reproducible `.gba`, verified checksum, clean
license/attribution audit, backed-up source tag, and passed 44VBA test matrix.

### Phase 9 — Release and maintenance

- Publish source/releases according to the chosen license and distribution plan;
  provide controls, compatibility, known issues, accessibility notes, and credits.
- Triage defects, preserve reproducible builds, migrate saves cautiously, and keep
  release branches/tags. Post-release content requires its own scope and gates.

## 5. Quality gates and test strategy

- **Per change:** compile with warnings treated deliberately; format/lint; schema,
  stable-ID, bounds, referential-integrity, text-fit, asset-license, and unit tests.
- **Per content batch:** automated map reachability and warp checks; battle
  simulations; save/load round trips; scripted critical-path smoke tests.
- **Per milestone:** clean build, ROM/memory/frame-time report, exploratory testing,
  checklist playthrough, accessibility review, and backup/restore drill.
- **Release:** start-to-finish and post-game playthroughs, 44VBA browser/device
  matrix, emulator cross-check, real-hardware smoke test, and legal audit.

Bug severity: **blocker** (cannot build/finish/data loss), **critical** (softlock,
crash, severe exploit), **major** (system/content substantially broken), **minor**
(localized defect), **polish** (presentation). Alpha may not exit with known
blockers or criticals; release candidates require explicit sign-off for majors.

## 6. Scope and schedule controls

- Estimate content in playable minutes and production units, not only map counts.
- Maintain critical-path, optional, post-game, and stretch labels for every item.
- Keep at least 15% production capacity for integration, tooling, and bug fixing,
  then reserve a dedicated stabilization period after content lock.
- Cut in this order if budgets slip: cosmetic variants, redundant optional rooms,
  standalone minigames, then post-game breadth. Do not cut save safety, testing,
  onboarding, the narrative ending, or required accessibility work.
- Update `DEVELOPMENT_STATUS.md` when a gate is evidenced, not when work merely
  starts. Record detailed decisions under `docs/` as the project grows.
