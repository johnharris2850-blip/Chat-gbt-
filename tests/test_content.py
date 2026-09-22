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
    if map_data["id"] == "starter_area":
        return not inside(map_data["water"], x, y) and not inside(map_data["building"], x, y)
    return inside(map_data["room"], x, y) and not any(inside(item, x, y) for item in map_data["furniture"])


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

    def test_npc_has_an_accessible_interaction_tile(self) -> None:
        starter = MAPS[0]
        visited = reachable(starter, tuple(starter["spawn"]))
        x, y = starter["npc"]
        self.assertTrue(any(tile in visited for tile in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))))


class DialogueDataTests(unittest.TestCase):
    def test_dialogue_has_multiple_nonempty_pages_that_fit(self) -> None:
        self.assertGreaterEqual(len(DIALOGUE["elder_mara"]), 2)
        for conversation in DIALOGUE.values():
            for page in conversation:
                self.assertGreater(len(page), 0)
                self.assertLessEqual(len(page), 3)
                for line in page:
                    self.assertTrue(line)
                    self.assertLessEqual(len(line), 20)
                    self.assertRegex(line, r"^[A-Z ]+$")

    def test_elder_dialogue_is_compiled_into_generated_world_data(self) -> None:
        self.assertIn(
            f"elder_mara_page_count = {len(DIALOGUE['elder_mara'])}",
            GENERATED_WORLD,
        )
        for page in DIALOGUE["elder_mara"]:
            for line in page:
                self.assertIn(f'\"{line}\"', GENERATED_WORLD)


class GeneratedGraphicsTests(unittest.TestCase):
    def test_sprite_items_are_stacked_vertically_for_butano(self) -> None:
        from tools.generate_placeholder_assets import letters, markers

        def dimensions(data: bytes) -> tuple[int, int]:
            self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
            return struct.unpack(">II", data[16:24])

        self.assertEqual(dimensions(letters()), (16, 26 * 16))
        self.assertEqual(dimensions(markers()), (16, 14 * 16))


if __name__ == "__main__":
    unittest.main()
