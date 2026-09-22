#!/usr/bin/env python3
"""Fast dependency-free repository checks suitable for local use and CI."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []

    # Butano enumerates every file in these configured input directories.  A
    # README or editor artifact is not ignored: it is sent to an asset tool and
    # can abort the ROM build before compilation.  Keep this allowlist aligned
    # with the source formats intentionally used by Crown & Chaos.
    required_asset_extensions = {
        "audio": {".json", ".wav"},
        "graphics": {".json", ".png"},
        "data": {".json"},
    }
    optional_asset_extensions = {
        "dmg_audio": {".mod", ".s3m", ".xm"},
    }
    valid_asset_name = re.compile(r"^[a-z0-9_]+$")
    asset_extensions = required_asset_extensions | optional_asset_extensions
    for directory, extensions in asset_extensions.items():
        asset_directory = ROOT / directory
        if not asset_directory.exists():
            if directory in required_asset_extensions:
                errors.append(f"required asset directory is missing: {directory}")
            continue
        if not asset_directory.is_dir():
            errors.append(f"asset path is not a directory: {directory}")
            continue
        for path in asset_directory.iterdir():
            if not path.is_file():
                errors.append(f"asset directory contains non-file entry: {path.relative_to(ROOT)}")
            elif path.suffix.lower() not in extensions:
                errors.append(f"non-asset file in {directory}: {path.name}")
            elif not valid_asset_name.fullmatch(path.stem):
                errors.append(f"invalid Butano asset name in {directory}: {path.name}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts or "external" in path.parts or not path.is_file():
            continue
        if path == ROOT / "crown_and_chaos.gba":
            # The clean-room output is allowed locally but remains Git-ignored.
            continue
        if path.suffix in {".gba", ".gb", ".gbc", ".nds", ".3ds", ".cia", ".ips", ".ups", ".bps", ".sav"}:
            errors.append(f"prohibited ROM/patch material: {path.relative_to(ROOT)}")

    tracked = set()
    if (ROOT / ".git/index").exists():
        import subprocess
        tracked = set(subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines())
    for pattern in ("graphics/*.png", "audio/*.wav"):
        for path in ROOT.glob(pattern):
            relative = path.relative_to(ROOT).as_posix()
            if relative in tracked:
                errors.append(f"generated binary must not be tracked: {relative}")

    for path in ROOT.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            errors.append(f"invalid JSON {path.relative_to(ROOT)}: {error}")

    for path in ROOT.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            if "://" not in target and not (path.parent / target.split("#", 1)[0]).exists():
                errors.append(f"broken link in {path.name}: {target}")

    required = {
        "README.md": ("Player: John", "John's starter: Water type", "Candy's starter: Fire type"),
        "Makefile": ("tools/generate_placeholder_assets.py", ".NOTPARALLEL:", "LIBBUTANO   := $(BUTANO)", "include $(LIBBUTANO)/butano.mak", "TARGET      := crown_and_chaos"),
        "src/main.cpp": ("bn::core::init()", "crown::read_input()"),
        "src/input.cpp": ("bn::keypad::start_pressed()", "bn::keypad::a_pressed()"),
        "src/world_state.cpp": ("check_transition()", "check_secret()", "try_interaction()"),
    }
    for filename, fragments in required.items():
        text = (ROOT / filename).read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{filename} is missing required fragment: {fragment}")

    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    if re.search(r"^DATA\s*:?=", makefile, re.MULTILINE):
        errors.append("Makefile must not pass authored JSON sources through Butano DATA")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("project checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
