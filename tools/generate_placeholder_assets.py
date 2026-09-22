#!/usr/bin/env python3
"""Generate deterministic, project-original bootstrap graphics without dependencies."""

from __future__ import annotations

import argparse
import json
import math
import struct
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

GLYPHS = {
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
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


def bmp(width: int, height: int, pixels: bytes) -> bytes:
    """Encode RGBA pixels as an uncompressed 8-bit indexed BMP for grit."""
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
                raise ValueError("generated graphic exceeds the 256-color indexed BMP limit")
            palette_index = len(palette)
            palette_indexes[rgba] = palette_index
            palette.append(rgba)
        indexed_pixels[pixel_index] = palette_index

    palette.extend([(0, 0, 0, 255)] * (256 - len(palette)))
    palette_data = b"".join(bytes((blue, green, red, 0)) for red, green, blue, _alpha in palette)
    row_stride = (width + 3) & ~3
    padding = bytes(row_stride - width)
    pixel_data = b"".join(
        indexed_pixels[y * width:(y + 1) * width] + padding
        for y in range(height - 1, -1, -1)
    )
    pixel_offset = 14 + 40 + len(palette_data)
    file_size = pixel_offset + len(pixel_data)
    file_header = b"BM" + struct.pack("<IHHI", file_size, 0, 0, pixel_offset)
    dib_header = struct.pack(
        "<IiiHHIIiiII", 40, width, height, 1, 8, 0, len(pixel_data), 2835, 2835, 256, 256
    )
    return file_header + dib_header + palette_data + pixel_data


def letters() -> bytes:
    # Butano sprite items are stacked vertically; `height` in letters.json is
    # the height of each item, not the height of a horizontal strip.
    width, height = 16, 27 * 16
    pixels = bytearray(width * height * 4)
    for glyph_index, glyph in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ&"):
        for row, bits in enumerate(GLYPHS[glyph]):
            for column, bit in enumerate(bits):
                if bit == "1":
                    for yy in range(2):
                        for xx in range(2):
                            x = 3 + column * 2 + xx
                            y = glyph_index * 16 + 1 + row * 2 + yy
                            offset = (y * width + x) * 4
                            pixels[offset:offset + 4] = bytes((240, 248, 255, 255))
    return bmp(width, height, bytes(pixels))


def markers() -> bytes:
    width, height = 16, 18 * 16
    pixels = bytearray(width * height * 4)
    for frame in range(12):
        step = frame % 3
        for y in range(2, 15):
            for x in range(4, 12):
                if y < 6:
                    color = (74, 43, 28, 255) if y < 4 or x in (4, 11) else (232, 183, 142, 255)
                elif y < 11:
                    color = (38, 83, 126, 255) if x not in (4, 11) else (214, 171, 128, 255)
                else:
                    gap = (step == 1 and x < 8) or (step == 2 and x >= 8)
                    if gap and y >= 13:
                        continue
                    color = (74, 55, 46, 255)
                pixels[((frame * 16 + y) * width + x) * 4:((frame * 16 + y) * width + x) * 4 + 4] = bytes(color)
    npc_colors = ((132, 76, 48, 255), (64, 112, 72, 255), (92, 72, 132, 255), (184, 66, 92, 255))
    for frame, coat in enumerate(npc_colors, 12):
        for y in range(2, 15):
            for x in range(4, 12):
                color = (96, 54, 34, 255) if y < 5 else ((235, 188, 148, 255) if y < 8 else coat)
                pixels[((frame * 16 + y) * width + x) * 4:((frame * 16 + y) * width + x) * 4 + 4] = bytes(color)
    for frame, fill in ((16, (155, 116, 52, 255)), (17, (240, 196, 40, 255))):
        for y in range(3, 14):
            for x in range(3, 13):
                color = (245, 231, 183, 255) if x in (3, 12) or y in (3, 13) else fill
                pixels[((frame * 16 + y) * width + x) * 4:((frame * 16 + y) * width + x) * 4 + 4] = bytes(color)
    return bmp(width, height, bytes(pixels))


def ui_panel() -> bytes:
    width = height = 64
    pixels = bytearray(width * height * 4)
    for y in range(height):
        for x in range(width):
            border = x < 2 or x >= width - 2 or y < 2 or y >= height - 2
            color = (220, 232, 245, 255) if border else (8, 18, 38, 255)
            offset = (y * width + x) * 4
            pixels[offset:offset + 4] = bytes(color)
    return bmp(width, height, bytes(pixels))


def rect_contains(rect: list[int], x: int, y: int) -> bool:
    return rect[0] <= x < rect[2] and rect[1] <= y < rect[3]


def walkable(map_data: dict, x: int, y: int) -> bool:
    if x <= 0 or y <= 0 or x >= 31 or y >= 31:
        return False
    return (any(rect_contains(area, x, y) for area in map_data["walkable"]) and
            not any(rect_contains(item, x, y) for item in map_data["blocked"]))


def map_bmp(map_data: dict) -> bytes:
    width = height = 256
    pixels = bytearray(width * height * 4)
    for py in range(height):
        for px in range(width):
            tx, ty = px // 8, py // 8
            map_id = map_data["id"]
            blocked = any(rect_contains(item, tx, ty) for item in map_data["blocked"])
            if map_id in ("johns_bedroom", "johns_house"):
                color = (72, 55, 58, 255)
                if any(rect_contains(area, tx, ty) for area in map_data["walkable"]):
                    color = (191 + ((tx + ty) % 2) * 9, 157, 108, 255)
                if blocked:
                    color = (91, 58, 45, 255) if (tx + ty) % 2 else (116, 72, 51, 255)
                if ty == 5:
                    color = (153, 130, 101, 255)
                if (tx, ty) in ((16, 27), (16, 9)):
                    color = (73, 43, 33, 255)
                if map_id == "johns_bedroom" and 12 <= tx < 20 and 14 <= ty < 19:
                    color = (112, 64 + (tx % 2) * 8, 104, 255)
                if (px % 8 in (0, 7)) or (py % 8 in (0, 7)):
                    color = tuple(max(0, c - 12) for c in color[:3]) + (255,)
            elif map_id == "crownhaven":
                color = (74 + ((tx + ty) % 3) * 4, 143, 70, 255)
                if 13 <= ty <= 20 or 7 <= tx <= 10:
                    color = (184, 151, 102, 255)
                if blocked:
                    color = (48, 104, 52, 255)
                    if any(rect_contains(r, tx, ty) for r in ([4,5,12,12], [17,4,25,11], [20,21,29,29], [2,22,9,29])):
                        color = (151, 87, 62, 255) if ty % 2 else (205, 185, 142, 255)
                    if 25 <= tx and ty < 15:
                        color = (46, 105 + (ty % 2) * 8, 170, 255)
                if (tx + ty) % 11 == 0 and not blocked:
                    color = (224, 207, 88, 255)
            else:
                color = (57, 112, 55, 255)
                if 13 <= ty < 23:
                    color = (170, 132, 82, 255)
                if blocked:
                    color = (35, 82, 39, 255) if ty < 16 else (104, 101, 91, 255)
                if (tx + ty) % 9 == 0 and not blocked:
                    color = (67, 132, 62, 255)
            offset = (py * width + px) * 4
            pixels[offset:offset + 4] = bytes(color)
    return bmp(width, height, bytes(pixels))


def world_header(maps: list[dict], dialogue: dict[str, list[list[str]]]) -> bytes:
    rows: list[list[int]] = []
    for map_data in maps:
        rows.append([sum((1 << x) for x in range(32) if walkable(map_data, x, y)) for y in range(32)])
    lines = [
        "#ifndef CROWN_GENERATED_WORLD_DATA_H", "#define CROWN_GENERATED_WORLD_DATA_H", "",
        "#include <cstdint>", "", "namespace crown::generated", "{", f"    constexpr int map_count = {len(maps)};", "",
        "    constexpr std::uint32_t collision[map_count][32] =",
        "    {",
    ]
    for map_rows in rows:
        lines.append("        {")
        lines.extend(f"            0x{row:08X}u," for row in map_rows)
        lines.append("        },")
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
    if check and path.suffix in {".bmp", ".wav"}:
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
    valid = update(ROOT / "graphics/letters.bmp", letters(), args.check)
    valid &= update(ROOT / "graphics/markers.bmp", markers(), args.check)
    valid &= update(ROOT / "graphics/ui_panel.bmp", ui_panel(), args.check)
    maps = json.loads((ROOT / "data/maps.json").read_text())["maps"]
    dialogue = json.loads((ROOT / "data/dialogue.json").read_text())
    for map_data in maps:
        valid &= update(ROOT / "graphics" / f"{map_data['id']}.bmp", map_bmp(map_data), args.check)
    valid &= update(ROOT / "include/generated/world_data.h", world_header(maps, dialogue), args.check)
    valid &= update(ROOT / "audio/interact.wav", interaction_wav(), args.check)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
