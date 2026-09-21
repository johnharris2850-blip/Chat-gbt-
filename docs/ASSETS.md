# Asset directories

Butano scans the directories configured by `AUDIO`, `GRAPHICS`, `DATA`, and
`DMGAUDIO` as build inputs. Do not place documentation, marker files, or other
non-assets in those directories: even a `README.md` is treated as an asset and
causes Butano's converters to reject its filename.

The tracked JSON files in `audio/` and `graphics/` are Butano metadata for the
generated assets with the same stem. The generated PNG and WAV files are
intentionally ignored by Git and are recreated deterministically by
`tools/generate_placeholder_assets.py` before compilation. The JSON files in
`data/` are project data inputs. `dmg_audio/` is currently empty and reserved
for future valid Butano DMG-audio assets.

Run `make assets` to generate binary inputs, `make verify` to check asset
directory hygiene and content, and `make clean` to remove generated inputs and
all ROM build output.
