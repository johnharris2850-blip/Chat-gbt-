# Pokémon Crown & Chaos — Development Status

Last updated: 2026-09-21

This is the canonical milestone checklist. Check an item only when its stated
output exists and has been reviewed or tested. Link future issue/commit evidence
beside completed items. Detailed scope lives in `PROJECT_PLAN.md`; creative targets
live in `GAME_DESIGN.md`.

## Milestone 0 — Project foundation

- [x] Preserve initial README project information.
- [x] Record clean-room legal/asset boundary.
- [x] Select Butano + devkitARM standalone-ROM approach.
- [x] Add high-level production roadmap.
- [x] Add high-level game design and 40+ hour content envelope.
- [x] Add repository directories and contribution-safe ignore/editor settings.
- [ ] Choose project code/content license and add `LICENSE`.
- [ ] Add asset provenance/license manifest format.

## Milestone 1 — Reproducible toolchain bootstrap

- [x] Pin documented devkitARM r65 and Butano 18.1.0 versions.
- [x] Add setup instructions for supported host environments.
- [x] Add a minimal original Butano program in `src/` and `include/`.
- [x] Add the Butano-compatible build entry point without vendoring the engine.
- [x] Show an original title screen/diagnostic scene and respond to input.
- [ ] Produce a clean `.gba` from a fresh checkout.
- [ ] Record ROM size and dependency licenses.
- [x] Add automated repository/content checks and a pinned-container GBA build job
      that uploads the ROM and SHA-256 file as a GitHub Actions artifact.
- [ ] Smoke-test the output in 44VBA and one independent emulator.

### Task 2 implementation and verification record

Implemented on 2026-09-21:

- Butano-compatible `Makefile`, pinned dependency bootstrap/check scripts, and
  deterministic project-original placeholder graphics.
- Crown & Chaos title/START screen, explicit title → field-test state transition,
  D-pad-controlled marker, and A-button save probe.
- Central input snapshot, game-state boundary, audio-service seam, and 32-byte
  versioned/checksummed SRAM data record with invalid-data reset behavior.
- Dependency-free source/link/JSON/prohibited-file checks and generated-asset
  reproducibility checks, both enabled in CI.

Checks passed in this environment:

- `python3 tools/check_project.py`
- `python3 tools/generate_placeholder_assets.py --check`
- `python3 -m py_compile tools/check_project.py tools/generate_placeholder_assets.py`
- `bash -n tools/bootstrap_butano.sh tools/check_toolchain.sh`
- `git diff --check`

Blocked by the execution environment, not marked complete:

- devkitARM is not installed and `DEVKITPRO`/`DEVKITARM` are unset.
- GitHub dependency download returned HTTP 403, so pinned Butano could not be
  fetched here.
- Consequently no `.gba` was produced, its size/license record could not be
  captured, and no 44VBA or independent-emulator smoke test was possible.

### Task 3 implementation and verification record

Implemented on 2026-09-21:

- Replaced the diagnostic field screen with the original **Pilgrim's Rest**
  gray-box starter area and **John's Home** interior.
- Added John as a four-direction player with three-frame directional placeholder
  walking, foot-based tile collision, and a bounded scrolling camera.
- Added original generated grass, paths, water, boundary foliage, building,
  interior floor, furniture, player, NPC, secret, dialogue-panel, and sound assets.
- Added door transitions into and out of John's Home.
- Added Elder Mara, facing-based A interaction, a fixed-screen dialogue box, two
  dialogue pages, and an original generated interaction cue.
- Added the hidden old-garden crown stone, discovery message, persistent gold
  marker, and START menu showing John, current area, and secret status.
- Upgraded the 32-byte SRAM schema to version 2; it restores map, pixel position,
  facing, secret discovery, and Elder Mara interaction state. Invalid/older records
  reset safely under the existing checksum/version policy.
- Added authored JSON for maps/dialogue, deterministic world/header/asset
  generation, and host tests for map dimensions, collision reachability, safe
  transitions, NPC access, dialogue pages, line bounds, and allowed characters.
- Enabled a GitHub Actions build using pinned image
  `devkitpro/devkitarm:20241104` and Butano 18.1.0. A successful run uploads
  `crown_and_chaos.gba` plus its SHA-256 file in artifact
  `crown-and-chaos-gba-<commit>`.

Tested locally:

- Repository policy, JSON, local-link, required-source, and prohibited ROM/patch/
  save-file checks.
- Deterministic generation checks for every original PNG, world collision header,
  and interaction WAV.
- Python unit tests for map data, collision/reachability, transitions, NPC access,
  and dialogue data.
- Python and shell syntax checks, save-layout host compile assertion, and Git
  whitespace checks.

Compilation status and ROM availability:

- Local GBA compilation remains blocked: this container has no devkitARM, and its
  network proxy rejects GitHub/devkitPro dependency hosts with HTTP 403.
- No local `crown_and_chaos.gba` was produced, so runtime behavior and 44VBA have
  not been falsely marked as verified.
- To obtain the ROM, push the commit to GitHub, open **Actions → Project checks →
  the successful run → Artifacts**, and download `crown-and-chaos-gba-<commit>`.
  It contains `crown_and_chaos.gba` and `crown_and_chaos.gba.sha256`. If that build
  exposes an engine/API mismatch, its log is the remaining blocker to fix before
  emulator validation.

### Pull-request binary compatibility fix

Completed on 2026-09-21:

- Removed every generated PNG and WAV from Git tracking without removing its
  generator, metadata, source data, or runtime reference.
- Split the build into a text-only root wrapper and `make/Butano.mk`; every normal
  `make` now regenerates all original binary inputs before Butano evaluates its
  asset graph.
- Added ignore rules and a repository policy check that rejects any generated
  `graphics/*.png` or `audio/*.wav` accidentally added to Git.
- Kept GitHub Actions artifact generation intact: CI now invokes the same root
  build wrapper and still uploads `crown_and_chaos.gba` plus its checksum.
- Verified checks from a clean, binary-free tree and verified that `make assets`
  deterministically restores all required build inputs. Local ROM compilation is
  still limited only by the previously recorded unavailable toolchain/network.

### GitHub Actions toolchain-path fix

Completed on 2026-09-21 after the first `gba-build` attempt:

- The pinned devkitPro container contained devkitARM under
  `/opt/devkitpro/devkitARM`, but its compiler directory was not present on the
  GitHub Actions step `PATH`.
- The job now declares `DEVKITPRO` and `DEVKITARM`, verifies the compiler exists at
  `${DEVKITARM}/bin/arm-none-eabi-g++`, publishes that directory through
  `GITHUB_PATH`, prints the compiler version, and confirms command lookup before
  running the unchanged toolchain validator and ROM build.
- This fixes the reported `arm-none-eabi-g++ is not on PATH` failure without
  weakening or bypassing `tools/check_toolchain.sh`.

## Milestone 2 — Data and engine skeleton

- [ ] Document architecture, ownership, memory/frame/save budgets, and stable IDs.
- [ ] Define validated schemas for creatures, moves, items, dialogue, maps, NPCs,
      trainers, encounters, quests, and progression flags.
- [ ] Add host-side validators and representative test fixtures.
- [ ] Implement scene/state stack, input mapping, debug overlay, and error handling.
- [ ] Establish asset pipeline and provenance checks.

## Milestone 3 — Gray-box core loop

- [x] Render the prototype maps with collision, camera, NPC interaction, one
      building transition, and a persistent discovery trigger.
- [x] Implement the first multipage dialogue box and persistent interaction flags.
- [ ] Implement party, creature, move, item, encounter, and inventory models.
- [ ] Implement deterministic battle loop, basic AI, experience, and recruitment.
- [ ] Implement menu, healing, storage, shop, and bestiary skeletons.
- [x] Implement versioned checksum save/load and invalid-data reset behavior.
- [ ] Pass explore → battle → recruit → heal → save/reload integration test.

## Milestone 4 — Vertical slice

- [ ] Finalize the slice brief and content budget.
- [ ] Implement John and Candy with Water/Fire starter setup.
- [ ] Complete one settlement, route, small dungeon, optional secret, and quests.
- [ ] Complete first rival/set-piece and major progression battle.
- [ ] Add representative final-quality original art, UI, audio, and writing.
- [ ] Conduct external playtests and resolve blockers/critical defects.
- [ ] Confirm performance, memory, ROM, save, and content-pipeline budgets.

## Milestone 5 — World and Act I

- [ ] Lock region topology, critical path, eight-trial structure, and narrative
      outline while retaining controlled change procedures.
- [ ] Lock roster plan and visual/audio/writing guides.
- [ ] Complete prologue and first 2–3 progression trials.
- [ ] Complete early optional chains and initial villain/rival arcs.
- [ ] Pass Act I regression and balance review.

## Milestone 6 — Acts II and III

- [ ] Complete middle towns, routes, dungeons, traversal upgrades, and trials.
- [ ] Complete mid-game character, rival, villain, and optional quest arcs.
- [ ] Complete late-game regions and trials.
- [ ] Lock core mechanics; reject or defer nonessential new systems.
- [ ] Pass each content-batch reachability, battle, save, and performance suite.

## Milestone 7 — Finale and content-complete alpha

- [ ] Complete Crown Seat approach, championship sequence, finale, ending, credits,
      and post-game transition.
- [ ] Complete all planned roster, maps, encounters, trainers, items, and dialogue.
- [ ] Complete all committed side quests and secrets.
- [ ] Finish a fresh-save start-to-credits playthrough.
- [ ] Remove or explicitly track every placeholder; enter feature freeze.

## Milestone 8 — Post-game

- [ ] Complete post-game narrative chapter and remote exploration zone.
- [ ] Complete rematches, challenge facility, superbosses, and collection support.
- [ ] Complete character and settlement epilogues.
- [ ] Finish start-to-post-game playthrough and balance pass.

## Milestone 9 — Stabilization and release candidate

- [ ] Resolve all blocker and critical defects.
- [ ] Complete progression, collision/warp, battle, economy, text, save, and idle
      regression suites.
- [ ] Complete accessibility, copy, narrative, cultural, and sensitivity reviews.
- [ ] Meet measured ROM, RAM, VRAM, frame-time, and save-space budgets.
- [ ] Audit licenses, attributions, debug features, and asset provenance.
- [ ] Verify supported save migrations and corrupt-save recovery.

## Milestone 10 — 44VBA validation and release

- [ ] Freeze and hash a reproducible release candidate `.gba`.
- [ ] Pass 44VBA controls, audio, save/load, suspend/resume, long-session, finale,
      credits, and post-game tests across the supported browser/device matrix.
- [ ] Cross-check an accuracy-focused emulator.
- [ ] Smoke-test real compatible hardware when available.
- [ ] Publish compatibility notes, controls, credits, known issues, and source tag.
- [ ] Establish patch, regression, and save-compatibility maintenance process.

## Recommended next task

**Task 4: First core RPG loop.** Begin by resolving any GitHub Actions compilation
errors and completing the Task 3 smoke matrix in 44VBA plus an independent
emulator. Once the overworld foundation is confirmed, add the opening starter
selection with John receiving the Water-type starter, introduce Candy and her
Fire-type starter, define validated creature/move/party data, and implement one
small deterministic basic battle prototype with commands, HP, victory/defeat, and
return to the overworld. Keep the roster, battle effects, and story scene narrowly
scoped; do not begin full campaign content production.
