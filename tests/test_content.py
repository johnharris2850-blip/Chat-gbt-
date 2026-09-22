from __future__ import annotations

import json
import struct
import unittest
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPS = json.loads((ROOT / "data/maps.json").read_text(encoding="utf-8"))["maps"]
DIALOGUE = json.loads((ROOT / "data/dialogue.json").read_text(encoding="utf-8"))
GENERATED_WORLD = (ROOT / "include/generated/world_data.h").read_text(encoding="utf-8")


def inside(rect: list[int], x: int, y: int) -> bool:
    return rect[0] <= x < rect[2] and rect[1] <= y < rect[3]


def walkable(map_data: dict, x: int, y: int) -> bool:
    if x <= 0 or y <= 0 or x >= map_data["width"] - 1 or y >= map_data["height"] - 1:
        return False
    if "room" in map_data:
        return inside(map_data["room"], x, y) and not any(inside(item, x, y) for item in map_data["furniture"])
    if "water" in map_data and inside(map_data["water"], x, y):
        return False
    return not any(inside(item, x, y) for item in map_data.get("blocked", []))


def reachable(map_data: dict, start: tuple[int, int]) -> set[tuple[int, int]]:
    visited = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for candidate in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if candidate not in visited and walkable(map_data, *candidate):
                visited.add(candidate)
                queue.append(candidate)
    return visited


class MapDataTests(unittest.TestCase):
    def test_ids_and_dimensions_are_unique_and_supported(self) -> None:
        self.assertEqual(len({entry["id"] for entry in MAPS}), len(MAPS))
        self.assertTrue(all((entry["width"], entry["height"]) == (32, 32) for entry in MAPS))

    def test_spawns_transitions_and_secret_are_reachable(self) -> None:
        for map_data in MAPS:
            start = tuple(map_data["spawn"])
            self.assertTrue(walkable(map_data, *start), map_data["id"])
            visited = reachable(map_data, start)
            for transition in map_data["transitions"]:
                self.assertIn(tuple(transition["at"]), visited, map_data["id"])
            if "secret" in map_data:
                self.assertIn(tuple(map_data["secret"]), visited)

    def test_transitions_target_known_maps_and_safe_spawns(self) -> None:
        by_id = {entry["id"]: entry for entry in MAPS}
        for map_data in MAPS:
            for transition in map_data["transitions"]:
                target = by_id[transition["to"]]
                self.assertTrue(walkable(target, *transition["spawn"]))

    def test_vertical_slice_contains_all_four_maps(self) -> None:
        self.assertEqual([entry["id"] for entry in MAPS], ["bedroom", "house", "crownhaven", "old_road"])


class DialogueDataTests(unittest.TestCase):
    def test_dialogue_has_multiple_nonempty_pages_that_fit(self) -> None:
        self.assertGreaterEqual(len(DIALOGUE["candy"]), 5)
        for conversation in DIALOGUE.values():
            for page in conversation:
                self.assertGreater(len(page), 0)
                self.assertLessEqual(len(page), 3)
                self.assertTrue(any(page))
                for line in page:
                    self.assertLessEqual(len(line), 23)
                    self.assertRegex(line, r"^[A-Z &]*$")

    def test_all_dialogue_is_compiled_into_generated_world_data(self) -> None:
        for name, conversation in DIALOGUE.items():
            self.assertIn(f"{name}_page_count = {len(conversation)}", GENERATED_WORLD)
            for page in conversation:
                for line in page:
                    self.assertIn(f'\"{line}\"', GENERATED_WORLD)


class GeneratedGraphicsTests(unittest.TestCase):
    def test_sprite_items_are_stacked_vertically_for_butano(self) -> None:
        from tools.generate_placeholder_assets import letters, markers

        def bmp_info(data: bytes) -> tuple[int, int, int, int]:
            self.assertEqual(data[:2], b"BM")
            width, height = struct.unpack("<ii", data[18:26])
            planes, bit_depth, compression = struct.unpack("<HHI", data[26:34])
            return width, height, planes, bit_depth if compression == 0 else -1

        self.assertEqual(bmp_info(letters()), (16, 27 * 16, 1, 8))
        self.assertEqual(bmp_info(markers()), (16, 16 * 16, 1, 8))


if __name__ == "__main__":
    unittest.main()
