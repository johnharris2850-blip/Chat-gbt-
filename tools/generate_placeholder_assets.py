#!/usr/bin/env python3
"""Generate deterministic, project-original bootstrap graphics without dependencies."""

from __future__ import annotations

import argparse
import json
import math
import struct
import wave
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "J": ("00111", "00010", "00010", "00010", "10010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
}


def png(width: int, height: int, pixels: bytes) -> bytes:
    """Encode RGBA pixels as an 8-bit indexed PNG accepted by Butano/grit."""
    def chunk(kind: bytes, payload: bytes) -> bytes:
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload))

    palette: list[tuple[int, int, int, int]] = [(0, 0, 0, 0)]
    palette_indexes = {palette[0]: 0}
    indexed_pixels = bytearray(width * height)
    for pixel_index in range(width * height):
        rgba = tuple(pixels[pixel_index * 4:pixel_index * 4 + 4])
        if rgba[3] == 0:
            rgba = palette[0]
        palette_index = palette_indexes.get(rgba)
        if palette_index is None:
            if len(palette) == 256:
                raise ValueError("generated graphic exceeds the 256-color indexed PNG limit")
            palette_index = len(palette)
            palette_indexes[rgba] = palette_index
            palette.append(rgba)
        indexed_pixels[pixel_index] = palette_index

    scanlines = b"".join(
        b"\0" + indexed_pixels[y * width:(y + 1) * width]
        for y in range(height)
    )
    palette_data = bytes(channel for color in palette for channel in color[:3])
    transparency = bytes(color[3] for color in palette)
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0)) +
            chunk(b"PLTE", palette_data) + chunk(b"tRNS", transparency) +
            chunk(b"IDAT", zlib.compress(scanlines, 9)) + chunk(b"IEND", b""))


def letters() -> bytes:
    # Butano sprite items are stacked vertically; `height` in letters.json is
    # the height of each item, not the height of a horizontal strip.
    width, height = 16, 26 * 16
    pixels = bytearray(width * height * 4)
    for glyph_index, glyph in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        for row, bits in enumerate(GLYPHS[glyph]):
            for column, bit in enumerate(bits):
                if bit == "1":
                    for yy in range(2):
                        for xx in range(2):
                            x = 3 + column * 2 + xx
                            y = glyph_index * 16 + 1 + row * 2 + yy
                            offset = (y * width + x) * 4
                            pixels[offset:offset + 4] = bytes((240, 248, 255, 255))
    return png(width, height, bytes(pixels))


def markers() -> bytes:
    width, height = 16, 14 * 16
    pixels = bytearray(width * height * 4)
    for frame in range(12):
        for y in range(2, 14):
            for x in range(3, 13):
                border = x in (3, 12) or y in (2, 13)
                foot_gap = y > 10 and ((frame % 3 == 1 and x < 8) or (frame % 3 == 2 and x > 8))
                if not foot_gap:
                    color = (232, 244, 255, 255) if border else (28, 112, 216, 255)
                    offset = ((frame * 16 + y) * width + x) * 4
                    pixels[offset:offset + 4] = bytes(color)
    for frame, fill in ((12, (170, 70, 52, 255)), (13, (240, 196, 40, 255))):
        for y in range(2, 14):
            for x in range(2, 14):
                color = (250, 245, 220, 255) if x in (2, 13) or y in (2, 13) else fill
                offset = ((frame * 16 + y) * width + x) * 4
                pixels[offset:offset + 4] = bytes(color)
    return png(width, height, bytes(pixels))


def ui_panel() -> bytes:
    width = height = 64
    pixels = bytearray(width * height * 4)
    for y in range(height):
        for x in range(width):
            border = x < 2 or x >= width - 2 or y < 2 or y >= height - 2
            color = (220, 232, 245, 255) if border else (8, 18, 38, 255)
            offset = (y * width + x) * 4
            pixels[offset:offset + 4] = bytes(color)
    return png(width, height, bytes(pixels))


def rect_contains(rect: list[int], x: int, y: int) -> bool:
    return rect[0] <= x < rect[2] and rect[1] <= y < rect[3]


def walkable(map_data: dict, x: int, y: int) -> bool:
    if x <= 0 or y <= 0 or x >= 31 or y >= 31:
        return False
    if map_data["id"] == "starter_area":
        return not rect_contains(map_data["water"], x, y) and not rect_contains(map_data["building"], x, y)
    if not rect_contains(map_data["room"], x, y):
        return False
    return not any(rect_contains(item, x, y) for item in map_data["furniture"])


def map_png(map_data: dict) -> bytes:
    width = height = 256
    pixels = bytearray(width * height * 4)
    for py in range(height):
        for px in range(width):
            tx, ty = px // 8, py // 8
            if map_data["id"] == "starter_area":
                color = (68, 146, 72, 255)
                if any(rect_contains(path, tx, ty) for path in map_data["paths"]):
                    color = (180, 150, 100, 255)
                if rect_contains(map_data["water"], tx, ty):
                    color = (42, 102 + (ty % 2) * 8, 182, 255)
                if rect_contains(map_data["building"], tx, ty):
                    color = (128, 74, 55, 255) if ty < 10 else (214, 194, 150, 255)
                if (tx, ty) == (15, 14):
                    color = (82, 48, 38, 255)
                if tx in (0, 31) or ty in (0, 31):
                    color = (28, 88, 42, 255)
                if (tx + ty) % 7 == 0 and color == (68, 146, 72, 255):
                    color = (76, 158, 78, 255)
            else:
                color = (38, 32, 40, 255)
                if rect_contains(map_data["room"], tx, ty):
                    color = (190, 158, 112, 255) if (tx + ty) % 2 else (202, 170, 120, 255)
                if any(rect_contains(item, tx, ty) for item in map_data["furniture"]):
                    color = (104, 62, 44, 255)
                if (tx, ty) == (15, 27):
                    color = (76, 48, 38, 255)
            offset = (py * width + px) * 4
            pixels[offset:offset + 4] = bytes(color)
    return png(width, height, bytes(pixels))


def world_header(maps: list[dict], dialogue: dict[str, list[list[str]]]) -> bytes:
    rows: list[list[int]] = []
    for map_data in maps:
        rows.append([sum((1 << x) for x in range(32) if walkable(map_data, x, y)) for y in range(32)])
    starter = maps[0]
    npc_x, npc_y = starter["npc"]
    secret_x, secret_y = starter["secret"]
    lines = [
        "#ifndef CROWN_GENERATED_WORLD_DATA_H", "#define CROWN_GENERATED_WORLD_DATA_H", "",
        "#include <cstdint>", "", "namespace crown::generated", "{", "    constexpr int map_count = 2;",
        f"    constexpr int elder_tile_x = {npc_x};", f"    constexpr int elder_tile_y = {npc_y};",
        f"    constexpr int elder_x = {npc_x * 8 - 124};", f"    constexpr int elder_y = {npc_y * 8 - 124};",
        f"    constexpr int secret_x = {secret_x * 8 - 124};", f"    constexpr int secret_y = {secret_y * 8 - 124};",
        "    constexpr int home_spawn_x = -4;", "    constexpr int home_spawn_y = 76;",
        "    constexpr int outside_spawn_x = -4;", "    constexpr int outside_spawn_y = -4;", "",
        "    constexpr std::uint32_t collision[map_count][32] =",
        "    {",
    ]
    for map_rows in rows:
        lines.append("        {")
        lines.extend(f"            0x{row:08X}u," for row in map_rows)
        lines.append("        },")
    elder_pages = dialogue["elder_mara"]
    lines += ["    };", "", f"    constexpr int elder_mara_page_count = {len(elder_pages)};",
              "    constexpr const char* elder_mara_dialogue[elder_mara_page_count][3] =", "    {"]
    for page in elder_pages:
        padded_page = page + [""] * (3 - len(page))
        lines.append("        { " + ", ".join(f'\"{line}\"' for line in padded_page) + " },")
    lines += [
        "    };", "", "    [[nodiscard]] constexpr bool walkable(int map_id, int x, int y)", "    {",
        "        return map_id >= 0 && map_id < map_count && x >= 0 && x < 32 && y >= 0 && y < 32 &&",
        "               ((collision[map_id][y] >> x) & 1u) != 0;", "    }", "}", "", "#endif", "",
    ]
    return "\n".join(lines).encode()


def interaction_wav() -> bytes:
    import io
    output = io.BytesIO()
    with wave.open(output, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(11025)
        samples = bytes(int(128 + 54 * math.sin(2 * math.pi * 660 * index / 11025) * (1 - index / 1102)) for index in range(1102))
        wav.writeframes(samples)
    return output.getvalue()


def update(path: Path, expected: bytes, check: bool) -> bool:
    # Binary build inputs are intentionally absent from Git. In check mode their
    # generators still execute, but only tracked text outputs are compared.
    if check and path.suffix in {".png", ".wav"}:
        return True
    if path.exists() and path.read_bytes() == expected:
        return True
    if check:
        print(f"outdated generated asset: {path.relative_to(ROOT)}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(expected)
    print(f"wrote {path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail instead of rewriting outdated files")
    args = parser.parse_args()
    valid = update(ROOT / "graphics/letters.png", letters(), args.check)
    valid &= update(ROOT / "graphics/markers.png", markers(), args.check)
    valid &= update(ROOT / "graphics/ui_panel.png", ui_panel(), args.check)
    maps = json.loads((ROOT / "data/maps.json").read_text())["maps"]
    dialogue = json.loads((ROOT / "data/dialogue.json").read_text())
    valid &= update(ROOT / "graphics/starter_area.png", map_png(maps[0]), args.check)
    valid &= update(ROOT / "graphics/johns_home.png", map_png(maps[1]), args.check)
    valid &= update(ROOT / "include/generated/world_data.h", world_header(maps, dialogue), args.check)
    valid &= update(ROOT / "audio/interact.wav", interaction_wav(), args.check)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
