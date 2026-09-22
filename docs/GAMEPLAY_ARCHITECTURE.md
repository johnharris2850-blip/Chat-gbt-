# Gameplay architecture

## Controls

- **D-pad:** walk and face in four directions.
- **A:** talk, inspect, and advance dialogue.
- **B:** close the status menu.
- **START:** open the status/objective menu; on the title screen, begin a game.

## State flow

`main.cpp` owns the top-level `TitleState`, `IntroState`, and `WorldState` flow.
The title owns its blinking prompt, the introduction owns its paged opening text,
and the world owns exploration.

## Maps and collision

Authored topology lives in `data/maps.json`. Each map defines walkable and blocked
rectangles, spawn points, and transitions. The deterministic generator converts
this into `include/generated/world_data.h`, including compact collision rows.

To add a map, add a unique JSON entry and `graphics/<map_id>.json` regular-bg
descriptor, extend `map_bmp` and `make_background`, then add its transitions.
Run `make -f make/host.mk assets` and `make -f make/host.mk verify` afterward.

## NPCs, dialogue, and objectives

`include/story_data.h` defines reusable NPC records: map, tile, graphic, and
dialogue ID. `WorldState` creates NPCs for the active map, includes them in
collision, and resolves face-and-A interaction. Add future NPCs by adding a
record, a vertically stacked sprite item, dialogue pages, and a page count.

Story outcomes use explicit save flags. This slice uses `candy_spoken` for the
Old Road objective and `demo_complete` for its finale.

## Saves

`SaveService` persists map, position, facing, and story flags in a versioned,
checksummed 32-byte SRAM record. Layout changes require a version increment.

## Graphics pipeline

Butano 18.1.0 inputs are generated as uncompressed indexed BMP files. Do not add
PNG inputs. Each BMP needs a lowercase matching JSON descriptor. Sprite items are
stacked vertically; JSON `height` is one item's height. Palette index zero is
transparent for sprites. Generated BMP/WAV files remain ignored and are recreated
before clean ROM builds.
