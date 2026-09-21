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
        "Makefile": ("tools/generate_placeholder_assets.py", "LIBBUTANO   := $(BUTANO)", "include $(LIBBUTANO)/butano.mak", "TARGET      := crown_and_chaos"),
        "src/main.cpp": ("bn::core::init()", "crown::read_input()"),
        "src/input.cpp": ("bn::keypad::start_pressed()", "bn::keypad::a_pressed()"),
        "src/world_state.cpp": ("check_transition()", "check_secret()", "try_interaction()"),
    }
    for filename, fragments in required.items():
        text = (ROOT / filename).read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                errors.append(f"{filename} is missing required fragment: {fragment}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("project checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
