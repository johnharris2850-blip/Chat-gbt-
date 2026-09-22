# Asset directories

Butano scans the directories configured by `AUDIO`, `GRAPHICS`, `DATA`, and
`DMGAUDIO` as build inputs. Do not place documentation, marker files, or other
non-assets in those directories: even a `README.md` is treated as an asset and
causes Butano's converters to reject its filename.

The tracked JSON files in `audio/` and `graphics/` are Butano metadata for the
generated assets with the same stem. The generated PNG and WAV files are
intentionally ignored by Git and are recreated deterministically by
`tools/generate_placeholder_assets.py` before compilation. The JSON files in
`data/` are authored JSON inputs consumed by the deterministic generator and
host tests; they are not passed to Butano's binary `DATA` pipeline. DMG audio is
not currently configured; a future
`dmg_audio/` directory is optional and must contain only valid Butano DMG-audio
assets if the build enables it.

Run `make -f make/host.mk assets` to generate binary inputs,
`make -f make/host.mk verify` to check asset directory hygiene and content, and
`make -f make/host.mk clean` to remove generated inputs and all ROM build output.
