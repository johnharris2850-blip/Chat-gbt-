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
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "10000", "11110", "00001", "00001", "11110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),

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
    # Butano requires 16px-high sprite items. Draw the 5x7 font at native
    # resolution inside each 8x16 cell so no runtime affine scaling is needed.
    width, height = 8, 37 * 16
    pixels = bytearray(width * height * 4)
    for glyph_index, glyph in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ&0123456789"):
        for row, bits in enumerate(GLYPHS[glyph]):
            for column, bit in enumerate(bits):
                if bit == "1":
                    x = 1 + column
                    y = glyph_index * 16 + 4 + row
                    offset = (y * width + x) * 4
                    pixels[offset:offset + 4] = bytes((240, 248, 255, 255))
    return bmp(width, height, bytes(pixels))


def markers() -> bytes:
    """John has 4x3 walking frames, followed by three villagers, Candy and Jexi."""
    width, height = 16, 17 * 16
    pixels = bytearray(width * height * 4)
    def pixel(frame, x, y, color):
        offset = ((frame * 16 + y) * width + x) * 4
        pixels[offset:offset + 4] = bytes(color)
    for frame in range(12):
        direction, step = frame // 3, frame % 3
        for y in range(2, 7):
            for x in range(4, 12):
                pixel(frame, x, y, (55, 35, 25, 255) if y < 5 else (226, 178, 132, 255))
        for y in range(7, 12):
            for x in range(3, 13):
                pixel(frame, x, y, (42, 70, 116, 255) if x not in (3,12) else (208, 158, 70, 255))
        for y in range(12, 15):
            for x in range(4, 7):
                if step != 2: pixel(frame, x - (1 if step == 1 else 0), y, (58, 42, 38, 255))
            for x in range(9, 12):
                if step != 1: pixel(frame, x + (1 if step == 2 else 0), y, (58, 42, 38, 255))
        # Directional hair/profile details.
        if direction == 1:
            for x in range(5,11): pixel(frame,x,6,(55,35,25,255))
        elif direction == 2: pixel(frame,4,6,(55,35,25,255))
        elif direction == 3: pixel(frame,11,6,(55,35,25,255))
    npc_colors = [(126,57,80,255),(53,104,65,255),(102,72,128,255),(196,72,74,255),(65,108,168,255)]
    for index, clothes in enumerate(npc_colors):
        frame = 12 + index
        hair = (245,190,72,255) if index == 3 else ((45,34,55,255) if index == 4 else ((92,65,44,255) if index else (205,205,190,255)))
        for y in range(2,6):
            for x in range(4,12): pixel(frame,x,y,hair)
        for y in range(6,9):
            for x in range(5,11): pixel(frame,x,y,(232,184,142,255))
        for y in range(9,14):
            for x in range(3,13): pixel(frame,x,y,clothes)
        if index == 3:
            pixel(frame,3,5,hair); pixel(frame,12,5,hair); pixel(frame,2,6,hair); pixel(frame,13,6,hair)
        if index == 4:
            # Jexi: Professor's assistant, dark hair and a light research coat.
            for y in range(9,13):
                pixel(frame,3,y,(225,232,236,255)); pixel(frame,12,y,(225,232,236,255))
            pixel(frame,5,7,(70,145,205,255)); pixel(frame,10,7,(70,145,205,255))
    return bmp(width, height, bytes(pixels))



def starters() -> bytes:
    """Three original 32x32 Crown & Chaos starter creatures: Water, Fire and Leaf."""
    width, height = 32, 32 * 3
    pixels = bytearray(width * height * 4)

    def p(frame, x, y, color):
        if 0 <= x < 32 and 0 <= y < 32:
            offset = ((frame * 32 + y) * width + x) * 4
            pixels[offset:offset + 4] = bytes(color)

    def blob(frame, cx, cy, rx, ry, color):
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if ((x-cx) * (x-cx) * ry * ry + (y-cy) * (y-cy) * rx * rx) <= rx * rx * ry * ry:
                    p(frame, x, y, color)

    # TIDELING — Water starter: round sea-drake with a finned tail and bright belly.
    navy=(25,55,91,255); blue=(47,128,190,255); aqua=(91,205,218,255); cream=(236,226,174,255)
    blob(0,15,17,9,9,navy); blob(0,15,16,8,8,blue); blob(0,15,20,5,5,aqua)
    blob(0,13,11,5,5,blue); blob(0,21,14,4,3,aqua)
    for x,y in ((10,9),(12,7),(15,6),(18,7)): p(0,x,y,aqua)
    for x in range(4,10): p(0,x,19+(x%2),navy)
    for y in range(23,28): p(0,11,y,navy); p(0,20,y,navy)
    p(0,11,11,cream); p(0,12,11,(20,24,35,255))

    # EMBEROO — Fire starter: small lion/roo creature with flame ears and tail.
    brown=(91,48,35,255); red=(188,58,42,255); orange=(238,119,44,255); gold=(250,190,67,255)
    blob(1,16,18,8,9,brown); blob(1,16,14,7,7,red); blob(1,16,20,5,5,orange)
    for x,y in ((10,7),(11,5),(12,8),(20,7),(21,5),(22,8)): p(1,x,y,gold)
    for x in range(22,29): p(1,x,20-(x%3),orange)
    p(1,29,17,gold); p(1,29,16,gold); p(1,10,13,gold); p(1,11,13,(25,22,25,255))
    for y in range(25,30): p(1,12,y,brown); p(1,20,y,brown)

    # THORNLET — Leaf starter: sturdy woodland cub with leaf crown and vine tail.
    dark=(35,78,48,255); green=(67,143,65,255); leaf=(117,181,72,255); tan=(205,177,111,255)
    blob(2,16,18,9,9,dark); blob(2,16,17,8,8,green); blob(2,16,20,5,5,tan)
    for x,y in ((16,5),(13,7),(19,7),(11,9),(21,9)): blob(2,x,y,2,3,leaf)
    for x in range(23,30): p(2,x,19+(x%2),dark)
    p(2,29,18,leaf); p(2,10,13,tan); p(2,11,13,(24,31,24,255))
    for y in range(25,30): p(2,12,y,dark); p(2,20,y,dark)

    return bmp(width, height, bytes(pixels))



def eevee() -> bytes:
    """Original 32x32 in-game sprite for John's mysterious Eevee companion."""
    width = height = 32
    pixels = bytearray(width * height * 4)

    def p(x, y, color):
        if 0 <= x < width and 0 <= y < height:
            offset = (y * width + x) * 4
            pixels[offset:offset + 4] = bytes(color)

    def blob(cx, cy, rx, ry, color):
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                if ((x-cx)*(x-cx)*ry*ry + (y-cy)*(y-cy)*rx*rx) <= rx*rx*ry*ry:
                    p(x,y,color)

    outline=(67,45,34,255); brown=(174,112,62,255); light=(226,177,105,255)
    cream=(244,224,174,255); dark=(31,28,31,255); shine=(244,248,235,255)
    blob(16,18,8,8,outline); blob(16,17,7,7,brown)
    blob(16,11,6,6,outline); blob(16,11,5,5,light)
    for x,y in ((11,5),(10,3),(9,1),(21,5),(22,3),(23,1)):
        blob(x,y,1,3,outline)
    blob(16,19,6,3,cream)
    blob(25,19,5,4,outline); blob(26,18,4,3,light); blob(29,16,2,2,cream)
    for x in range(11,14): p(x,26,outline)
    for x in range(19,22): p(x,26,outline)
    # Eevee's unmistakable blue eyes are an early visual clue that he is unusual.
    eye_blue=(64,160,224,255)
    p(13,10,eye_blue); p(19,10,eye_blue); p(13,9,shine); p(19,9,shine)
    p(16,13,dark)
    # A strange white diamond-like fur marking hints at his hidden heavenly purpose.
    for x,y in ((16,15),(15,16),(16,16),(17,16),(16,17)):
        p(x,y,shine)
    return bmp(width, height, bytes(pixels))

def ui_panel() -> bytes:
    """Ornate Crown & Chaos dialogue/menu panel with a classic GBA RPG feel."""
    width = height = 64
    pixels = bytearray(width * height * 4)
    gold = (226, 194, 112, 255)
    light_gold = (250, 232, 166, 255)
    navy = (20, 35, 58, 255)
    inner = (31, 52, 76, 255)
    shadow = (9, 17, 31, 255)
    for y in range(height):
        for x in range(width):
            edge = min(x, y, width - 1 - x, height - 1 - y)
            if edge == 0:
                color = shadow
            elif edge == 1:
                color = gold
            elif edge == 2:
                color = light_gold
            elif edge == 3:
                color = navy
            else:
                color = inner if ((x // 8 + y // 8) & 1) else navy
            offset = (y * width + x) * 4
            pixels[offset:offset + 4] = bytes(color)
    # Small crown-like corner ornaments make joined panels feel bespoke.
    for ox, oy in ((5, 5), (58, 5), (5, 58), (58, 58)):
        for dx, dy in ((0, 0), (-2, 1), (2, 1), (0, 2)):
            x, y = ox + dx, oy + dy
            offset = (y * width + x) * 4
            pixels[offset:offset + 4] = bytes(light_gold)
    return bmp(width, height, bytes(pixels))


def rect_contains(rect: list[int], x: int, y: int) -> bool:
    return rect[0] <= x < rect[2] and rect[1] <= y < rect[3]


def walkable(map_data: dict, x: int, y: int) -> bool:
    if x <= 0 or y <= 0 or x >= 31 or y >= 31:
        return False
    if "room" in map_data:
        return rect_contains(map_data["room"], x, y) and not any(rect_contains(r,x,y) for r in map_data["furniture"])
    if "water" in map_data and rect_contains(map_data["water"], x, y):
        return False
    return not any(rect_contains(r,x,y) for r in map_data.get("blocked", []))


def put(pixels, x, y, color):
    if 0 <= x < 256 and 0 <= y < 256:
        offset = (y * 256 + x) * 4
        pixels[offset:offset + 4] = bytes(color)


def map_bmp(map_data: dict) -> bytes:
    pixels = bytearray(256 * 256 * 4)
    indoor = "room" in map_data
    for py in range(256):
        for px in range(256):
            tx, ty = px // 8, py // 8
            if indoor:
                color = (42,34,38,255)
                if rect_contains(map_data["room"],tx,ty):
                    color = (190,151,101,255) if (tx + ty) % 2 else (201,164,112,255)
                if any(rect_contains(r,tx,ty) for r in map_data["furniture"]):
                    color = (104,61,39,255)
                if map_data["id"] == "bedroom":
                    # Warm timber floor with a bordered royal rug for John's room.
                    if ((px // 16) + (py // 8)) % 2:
                        color = tuple(max(0, channel - 8) for channel in color[:3]) + (255,)
                    if 13 <= tx < 20 and 16 <= ty < 21:
                        border = tx in (13,19) or ty in (16,20)
                        color = (218,174,72,255) if border else (116,42,55,255)
            else:
                color = (62,137,64,255)
                if any(rect_contains(r,tx,ty) for r in map_data.get("paths",[])):
                    color = (185,151,96,255) if (px + py) % 5 else (165,130,79,255)
                if "water" in map_data and rect_contains(map_data["water"],tx,ty):
                    color = (43,102 + (ty%2)*12,174,255)
                if any(rect_contains(r,tx,ty) for r in map_data.get("blocked",[])):
                    color = (35,91,43,255)
            put(pixels,px,py,color)
    # Detailed tile-scale furniture, buildings, trees, flowers, fences and signs.
    if indoor:
        # Framed blue window with highlight, curtains and a stronger doorway.
        for x in range(108,148):
            for y in range(44,59): put(pixels,x,y,(69,45,35,255))
        for x in range(112,144):
            for y in range(47,56):
                put(pixels,x,y,(105,177,207,255) if y < 51 else (71,137,181,255))
        for x in range(126,130):
            for y in range(47,56): put(pixels,x,y,(225,207,157,255))
        if map_data["id"] == "bedroom":
            for x in list(range(104,110)) + list(range(146,152)):
                for y in range(43,64): put(pixels,x,y,(112,45,55,255))
            # Gold curtain ties and rug centre emblem.
            for x,y in ((107,55),(149,55)):
                for yy in range(y-1,y+2):
                    for xx in range(x-1,x+2): put(pixels,xx,yy,(225,181,72,255))
            for y in range(143,151):
                for x in range(128,136):
                    if abs(x-132)+abs(y-147) < 5: put(pixels,x,y,(225,181,72,255))
        for x in range(120,144):
            for y in range(214,224): put(pixels,x,y,(58,36,29,255))
        for x in range(124,140):
            for y in range(216,224): put(pixels,x,y,(102,62,39,255))
        if map_data["id"] == "house":
            # Downstairs home details: hearth, kitchen counter, shelves and a runner rug.
            for y in range(72,104):
                for x in range(52,84): put(pixels,x,y,(91,57,43,255))
            for y in range(78,98):
                for x in range(58,78): put(pixels,x,y,(42,39,38,255))
            for y in range(86,98):
                for x in range(63,73):
                    if (x+y)%3: put(pixels,x,y,(196,76,38,255))
            for y in range(68,76):
                for x in range(168,216): put(pixels,x,y,(139,94,57,255))
            for y in range(76,82):
                for x in range(168,216): put(pixels,x,y,(218,190,133,255))
            for sx in (174,190,206):
                for y in range(82,101):
                    for x in range(sx,sx+3): put(pixels,x,y,(91,57,43,255))
            for y in range(146,174):
                for x in range(112,152):
                    border = x < 115 or x >= 149 or y < 149 or y >= 171
                    put(pixels,x,y,(214,170,68,255) if border else (76,78,111,255))
    else:
        for r in map_data.get("blocked",[]):
            for tx in range(r[0],r[2]):
                for ty in range(r[1],r[3]):
                    if (tx+ty)%3 == 0:
                        cx,cy=tx*8+4,ty*8+4
                        for yy in range(-4,4):
                            for xx in range(-4,4):
                                if xx*xx+yy*yy < 16: put(pixels,cx+xx,cy+yy,(24,82,38,255))
        if map_data["id"] == "crownhaven":
            # Give Crownhaven a richer village identity: stone path edging, lampposts,
            # flower beds and varied civic/home architecture.
            for r in map_data.get("paths", []):
                for tx in range(r[0], r[2]):
                    for edge_ty in (r[1], r[3] - 1):
                        if 0 <= edge_ty < 32 and (tx + edge_ty) % 2 == 0:
                            for xx in range(tx*8, tx*8+8):
                                put(pixels,xx,edge_ty*8,(128,108,76,255))
            for lx,ly in ((10,14),(20,14),(10,23),(22,23)):
                for y in range(ly*8-9,ly*8+5):
                    for x in range(lx*8-1,lx*8+2): put(pixels,x,y,(65,55,47,255))
                for y in range(ly*8-12,ly*8-7):
                    for x in range(lx*8-4,lx*8+5):
                        if abs(x-lx*8)+abs(y-(ly*8-9)) < 7: put(pixels,x,y,(239,199,91,255))
            for fx,fy in ((8,20),(9,20),(24,18),(25,18),(18,25),(19,25)):
                for yy in range(2,7):
                    for xx in range(1,7):
                        put(pixels,fx*8+xx,fy*8+yy,(52,116,55,255))
                put(pixels,fx*8+4,fy*8+3,(235,104 if fx%2 else 181,111,255))
            for building_index, r in enumerate(map_data["blocked"]):
                for y in range(r[1]*8, r[3]*8):
                    for x in range(r[0]*8, r[2]*8):
                        roof_end = r[1]*8 + 18
                        roof_palette = ((126,55,48,255),(112,70,45,255),(74,76,104,255),(70,67,92,255))
                        wall_palette = ((220,199,151,255),(205,185,139,255),(194,181,151,255),(174,170,157,255))
                        if y < roof_end:
                            color = roof_palette[building_index % len(roof_palette)]
                            # Rows of roof tiles with a darker eave.
                            if (y-r[1]*8) % 5 == 0:
                                color = tuple(max(0,v-18) for v in color[:3]) + (255,)
                            if y >= roof_end-3:
                                color = tuple(max(0,v-28) for v in color[:3]) + (255,)
                        else:
                            color = wall_palette[building_index % len(wall_palette)]
                            # Sparse stone/timber accents stop walls looking flat.
                            if (x//8 + y//8 + building_index) % 7 == 0:
                                color = tuple(max(0,v-10) for v in color[:3]) + (255,)
                        put(pixels,x,y,color)
                center=(r[0]+r[2])*4
                for y in range(r[3]*8-14,r[3]*8):
                    for x in range(center-4,center+4): put(pixels,x,y,(75,45,31,255))
                for x in (r[0]*8+10,r[2]*8-14):
                    # Framed glass windows with bright upper panes.
                    for y in range(r[3]*8-25,r[3]*8-16):
                        for xx in range(x-1,x+6): put(pixels,xx,y,(75,55,40,255))
                    for y in range(r[3]*8-24,r[3]*8-17):
                        for xx in range(x,x+5):
                            put(pixels,xx,y,(112,178,202,255) if y < r[3]*8-21 else (67,128,169,255))
                    for y in range(r[3]*8-24,r[3]*8-17):
                        put(pixels,x+2,y,(224,205,151,255))
                # Door lintel and tiny brass/gold handle.
                for x in range(center-6,center+6):
                    put(pixels,x,r[3]*8-15,(57,42,32,255))
                put(pixels,center+2,r[3]*8-7,(224,178,70,255))
        elif map_data["id"] == "old_road":
            for tx,ty in ((14,12),(16,23),(24,9)):
                for yy in range(8):
                    for xx in range(10):
                        if (xx-5)**2 + (yy-5)**2 < 24: put(pixels,tx*8+xx,ty*8+yy,(104,105,99,255))
        for tx,ty in ((6,18),(16,18),(23,16),(28,20)):
            for yy in range(2,6):
                for xx in range(2,6): put(pixels,tx*8+xx,ty*8+yy,(235,205 if tx%2 else 90,90,255))
        # wooden sign
        for y in range(120,136):
            for x in range(56,72): put(pixels,x,y,(119,72,39,255))
    return bmp(256, 256, bytes(pixels))


def title_bmp() -> bytes:
    pixels=bytearray(256*256*4)
    for y in range(256):
        for x in range(256):
            color=(10 + y//20,18 + y//14,42 + y//10,255)
            put(pixels,x,y,color)
    # moon, distant castle, crown silhouette and ornamental border
    for y in range(20,76):
        for x in range(170,226):
            if (x-198)**2+(y-48)**2 < 750: put(pixels,x,y,(222,211,158,255))
    for x in range(72,184):
        for y in range(126,190):
            if y > 170 or (80<x<101) or (116<x<140) or (155<x<177): put(pixels,x,y,(17,17,29,255))
    for x in range(256):
        for y in (2,3,252,253): put(pixels,x,y,(185,139,56,255))
    return bmp(256,256,bytes(pixels))


def world_header(maps: list[dict], dialogue: dict[str, list[list[str]]]) -> bytes:
    rows=[[sum((1<<x) for x in range(32) if walkable(m,x,y)) for y in range(32)] for m in maps]
    lines=["#ifndef CROWN_GENERATED_WORLD_DATA_H", "#define CROWN_GENERATED_WORLD_DATA_H", "", "#include <cstdint>", "", "namespace crown::generated", "{", f"    constexpr int map_count = {len(maps)};", "    constexpr std::uint32_t collision[map_count][32] =", "    {"]
    for map_rows in rows:
        lines += ["        {"] + [f"            0x{row:08X}u," for row in map_rows] + ["        },"]
    lines += ["    };", ""]
    for name,pages in dialogue.items():
        lines += [f"    constexpr int {name}_page_count = {len(pages)};", f"    constexpr const char* {name}_dialogue[{name}_page_count][3] =", "    {"]
        for page in pages:
            page=(page+[""]*3)[:3]
            lines.append("        { " + ", ".join(f'\"{line}\"' for line in page) + " },")
        lines += ["    };", ""]
    lines += ["    [[nodiscard]] constexpr bool walkable(int map_id, int x, int y)", "    {", "        return map_id >= 0 && map_id < map_count && x >= 0 && x < 32 && y >= 0 && y < 32 &&", "               ((collision[map_id][y] >> x) & 1u) != 0;", "    }", "}", "", "#endif", ""]
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
    valid &= update(ROOT / "graphics/starters.bmp", starters(), args.check)
    valid &= update(ROOT / "graphics/eevee.bmp", eevee(), args.check)
    valid &= update(ROOT / "graphics/ui_panel.bmp", ui_panel(), args.check)
    maps = json.loads((ROOT / "data/maps.json").read_text())["maps"]
    dialogue = json.loads((ROOT / "data/dialogue.json").read_text())
    valid &= update(ROOT / "graphics/title.bmp", title_bmp(), args.check)
    for map_data in maps:
        valid &= update(ROOT / "graphics" / f"{map_data['id']}.bmp", map_bmp(map_data), args.check)
    valid &= update(ROOT / "include/generated/world_data.h", world_header(maps, dialogue), args.check)
    valid &= update(ROOT / "audio/interact.wav", interaction_wav(), args.check)
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
