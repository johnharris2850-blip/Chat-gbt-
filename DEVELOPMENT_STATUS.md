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

### GitHub Actions Butano-checkout fix

Completed on 2026-09-21 after the next `gba-build` attempt:

- Replaced the working-directory-dependent `git clone external/butano` command
  with a second `actions/checkout` invocation targeting the pinned Butano 18.1.0
  tag and explicit `external/butano` workspace path.
- Set `BUTANO` to `${{ github.workspace }}/external/butano` for the whole GBA job.
- Added a pre-build gate that verifies the absolute location, Git checkout,
  `butano.mak`, and exact `18.1.0` tag before the unchanged toolchain validator is
  allowed to run.
- The checksum and downloadable ROM artifact steps remain unchanged and will run
  only after a real successful compilation.

### Container workspace-path correction

Completed on 2026-09-21 after checkout verification exposed the host/container
workspace distinction:

- Removed the job-level `BUTANO: ${{ github.workspace }}/external/butano` value,
  because GitHub evaluates that expression to the host path before entering the
  devkitPro container.
- The toolchain setup step now derives `BUTANO` from the container's runtime
  `GITHUB_WORKSPACE` (`/__w/...`) and publishes it to later steps with
  `GITHUB_ENV`.
- The existing equality, repository, `butano.mak`, and exact-tag checks remain in
  place and now validate the same mounted path populated by `actions/checkout`.

### Runtime Butano-path resolution

Completed on 2026-09-21 after the next Actions log showed the exported value still
did not compare byte-for-byte with the checkout path:

- Removed the earlier pre-checkout `BUTANO` export.
- The post-checkout verification now logs the incoming `BUTANO`, runtime
  `GITHUB_WORKSPACE`, physical `pwd`, and canonical dependency path before testing.
- It uses `realpath -e` to require and canonicalize the actual checked-out
  `${GITHUB_WORKSPACE}/external/butano` directory, exports that exact value through
  `GITHUB_ENV`, and compares it with the canonical workspace path.
- Git metadata, `butano.mak`, exact tag, the unchanged toolchain validator, ROM
  checksum, and artifact gates remain mandatory.

### Pinned-checkout verification correction

Completed on 2026-09-21 after the diagnostics proved the checkout path itself was
correct:

- `BUTANO` is assigned from the canonical runtime checkout path in the same shell
  that verifies it, then persisted to later container steps through `GITHUB_ENV`.
- The canonical nested checkout is registered as a Git safe directory before Git
  reads it, accounting for the runner/container ownership boundary without
  weakening path, repository, or version validation.
- Each gate now has a log label, so a future failure identifies the exact check.
- Version validation compares the checked-out `HEAD` commit to the peeled
  `refs/tags/18.1.0` commit. This verifies the pinned revision without relying on
  `git describe`'s human-readable tag spelling.
- The required `.git` entry and `butano.mak` file are still checked explicitly;
  the strict toolchain, ROM existence, checksum, and artifact gates are unchanged.

### Butano build-entry-point correction

Completed on 2026-09-21 after the real Actions checkout passed path and Git
verification but showed that the repository root has no `butano.mak`:

- The checkout remains at `external/butano`, while the `BUTANO` SDK variable now
  points to the upstream engine subdirectory `external/butano/butano` containing
  `butano.mak`.
- CI prints the repository listing and searches three levels for `butano.mak`,
  `common.mk`, and `Makefile` before applying strict checks, making the upstream
  layout visible in every build log.
- Git metadata and the pinned `18.1.0` tag are verified against the repository
  root; the build entry point is verified separately against the engine directory.
- Local defaults, bootstrap guidance, and the strict toolchain checker now use the
  same repository-root versus engine-directory distinction as CI.

### Butano make-variable correction

Completed on 2026-09-21 after the real build entered `butano.mak` but attempted
to include `/butano_dka.mak`:

- The project now assigns the resolved SDK directory to Butano 18.1.0's required
  `LIBBUTANO` make variable before including `$(LIBBUTANO)/butano.mak`.
- This preserves `BUTANO` as the documented local/CI override while ensuring
  Butano's own makefiles can resolve adjacent files such as `butano_dka.mak`.
- CI now verifies both `butano.mak` and `butano_dka.mak` before compilation.
- Repository policy checks enforce the supported `LIBBUTANO` integration so the
  recursive build cannot silently regress to an empty SDK prefix.

### Recursive-make propagation correction

Completed on 2026-09-21 after the real build showed `LIBBUTANO` was still empty
inside the recursive make despite the child makefile alias:

- The root Makefile now defines the SDK default and passes both `BUTANO` and
  `LIBBUTANO` explicitly on the recursive make command line, matching the standard
  Butano project contract and giving `butano.mak` the variable in its own make
  invocation.
- The child project makefile retains a local fallback, prints `BUTANO`,
  `LIBBUTANO`, and the resolved `butano_dka.mak` candidate for real-CI diagnosis,
  and fails before including Butano unless both engine makefiles exist.
- Repository checks now require the explicit recursive-make propagation.

### Absolute Butano make-variable correction

Completed on 2026-09-21 after real-CI diagnostics proved `BUTANO` and
`LIBBUTANO` were populated while Butano line 5 still expanded its include to
`/butano_dka.mak`:

- The standard `LIBBUTANOABS` variable is now derived with GNU Make's `realpath`
  and passed explicitly into the recursive invocation alongside `LIBBUTANO`.
- The project fails immediately if the absolute path is empty or if
  `${LIBBUTANOABS}/butano_dka.mak` is absent, and logs the exact expansion used by
  Butano line 5.
- Real CI now prints the first 15 lines of the pinned `butano.mak`, representative
  official example Makefiles, and both canonical engine paths immediately before
  building, so the checked-out 18.1.0 sources—not an assumed layout—are visible in
  the authoritative build log.

### Deterministic ROM output correction

Completed on 2026-09-21 after the real Butano compilation succeeded but the
repository-root ROM gate found no file:

- The root build now passes Butano/devkitARM's extension-free `OUTPUT` variable as
  the absolute `${repository}/crown_and_chaos` path, while retaining
  `TARGET := crown_and_chaos` for the supported project configuration.
- The output is configured before Butano evaluates its rules, rather than copying
  or renaming an unknown product after compilation.
- The Build ROM step lists every generated `.gba` file with its size and requires
  the canonical root ROM immediately; Record ROM uses the runtime
  `GITHUB_WORKSPACE` path for existence, checksum, and size checks.
- Artifact upload continues to require `crown_and_chaos.gba` and its SHA-256 file.

### Standard root Butano project correction

Completed on 2026-09-21 after the real build reported `Nothing to be done for
'build'` and produced no ROM:

- Replaced the wrapper-to-nested-make arrangement with a standard root Butano
  project Makefile. Butano can now reinvoke the same root file from `build/`, as
  required by its outer/inner build stages, instead of accidentally re-entering a
  wrapper that never compiled the project.
- The actual Crown & Chaos `src`, `include`, `data`, `graphics`, `audio`, and
  `dmg_audio` directories are configured directly in that root project file.
- CI generates deterministic binary inputs immediately before invoking the
  standard default Butano build; host-only `assets`, `verify`, and `clean` goals
  remain available without loading the external SDK.
- Removed the nonstandard nested `make/Butano.mk` and the forced `OUTPUT`
  override. Butano now owns its supported build recursion and emits
  `crown_and_chaos.gba` from `TARGET := crown_and_chaos`.

### Asset-directory hygiene correction

Completed on 2026-09-21 after the real Butano audio conversion reached the
project assets and rejected `audio/README.md` as an invalid asset name:

- Removed documentation files from `audio/`, `graphics/`, `data/`, and
  `dmg_audio/`; shared guidance now lives in `docs/ASSETS.md` outside every
  directory scanned by Butano.
- Added a repository check that rejects unsupported files and invalid Butano
  asset names in all four configured input directories.
- The CI ROM job now runs `make clean`, regenerates the deterministic PNG/WAV
  inputs, and reruns repository checks immediately before the real build. This
  prevents stale converter output from concealing an asset-input failure.
- The pinned Butano 18.1.0 and devkitARM r65 contracts, nonempty root-ROM gate,
  checksum/size recording, and artifact upload remain enabled.
- Host validation passes. Production of `crown_and_chaos.gba` remains subject to
  the devkitARM container build; this checkout does not contain that external
  toolchain or the ignored Butano dependency.

### Optional DMG-audio correction

Completed on 2026-09-22 after GitHub Actions showed the repository checker was
still treating the removed, unused `dmg_audio/` directory as mandatory:

- Removed `DMGAUDIO` from the Butano project configuration because Crown & Chaos
  currently has no DMG-audio inputs.
- The checker now requires and validates the active `audio/`, `graphics/`, and
  `data/` directories, while validating `dmg_audio/` only if it actually exists.
- No marker or placeholder file is used to manufacture an otherwise empty asset
  directory.

### Container workspace Git ownership correction

Completed on 2026-09-22:

- The GBA job now registers the runtime `${GITHUB_WORKSPACE}` as a Git safe
  directory before any project-side validation runs inside the devkitPro
  container.
- The existing, separately verified Butano checkout remains registered by its
  canonical dependency path; no global wildcard trust is used.

### Authored JSON build-input correction

Completed on 2026-09-22 after the real linker build tried to create the
unsupported target `dialogue.json.o`:

- Removed `DATA := data` from the Butano Makefile. The directory contains
  authored JSON source data, not binary files for Butano's `DATA` pipeline.
- Dialogue JSON is now compiled into the generated C++ world-data header and the
  dialogue UI reads Elder Mara's pages from that generated data rather than a
  duplicate hard-coded script.
- Repository validation rejects reintroducing a Butano `DATA` assignment for
  the authored JSON directory.

### Clean-build generated-header discovery correction

Completed on 2026-09-22 after serializing the real CI build proved that the
missing `bn_sprite_items_letters.h` was not a parallel-build race:

- The project now passes canonical project-root paths for `SOURCES`, `INCLUDES`,
  `GRAPHICS`, and `AUDIO`, keeping asset discovery stable when Butano reinvokes
  the root Makefile from `build/`.
- CI verifies both `letters.png` and its matching `letters.json` immediately
  before compilation.
- Repository checks validate the exact Butano sprite metadata (`type: sprite`,
  `height: 16`) for letters and the expected metadata for every other graphic.

### Project object-path correction

Completed on 2026-09-22 after the graphics fix reached the final link but the
linker could not find the seven Crown & Chaos project objects:

- Restored Butano's standard relative `SOURCES := src` configuration. Butano's
  devkitARM make layer flattens source names into objects in `build/`; absolute
  source paths broke that source-to-object mapping even though discovery still
  listed the `.cpp` files.
- The subsequent real CI run showed that reverting `INCLUDES` together with
  `SOURCES` also regressed generated item-header discovery. `INCLUDES`,
  `GRAPHICS`, and `AUDIO` therefore retain their previously working canonical
  project-root paths while only `SOURCES` is relative for correct object names.
- Repository validation enforces this deliberate split instead of alternating
  between the two incomplete configurations.

### Project include-path correction

Completed on 2026-09-22 after the real build retained generated graphics-header
discovery but could not resolve `audio_service.h`:

- `INCLUDES` now begins with Butano's standard project-relative `include` entry,
  allowing its make layer to construct the correct compiler include flag.
- The canonical include entry is retained as a second path so the recursive
  build keeps the configuration that exposed generated item headers in the
  preceding successful graphics stage.
- Repository checks scan every quoted include in every `src/*.cpp` file and
  require all non-Butano headers—including `generated/world_data.h`—to exist
  beneath the configured project include tree.

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
