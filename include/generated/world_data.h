#ifndef CROWN_GENERATED_WORLD_DATA_H
#define CROWN_GENERATED_WORLD_DATA_H

#include <cstdint>

namespace crown::generated
{
    constexpr int map_count = 2;
    constexpr int elder_tile_x = 18;
    constexpr int elder_tile_y = 16;
    constexpr int elder_x = 20;
    constexpr int elder_y = 4;
    constexpr int secret_x = -68;
    constexpr int secret_y = 44;
    constexpr int home_spawn_x = -4;
    constexpr int home_spawn_y = 76;
    constexpr int outside_spawn_x = -4;
    constexpr int outside_spawn_y = -4;

    constexpr std::uint32_t collision[map_count][32] =
    {
        {
            0x00000000u,
            0x7FFFFFFEu,
            0x7FFFFE02u,
            0x7FFFFE02u,
            0x7FFFFE02u,
            0x7FFFFE02u,
            0x7FFFFE02u,
            0x7FFFFE02u,
            0x7FF80E02u,
            0x7FF80E02u,
            0x7FF80E02u,
            0x7FF80E02u,
            0x7FF80E02u,
            0x7FF80E02u,
            0x7FFFFE02u,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x00000000u,
        },
        {
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00C7C300u,
            0x00C7C300u,
            0x00C7FF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFF300u,
            0x00FFF300u,
            0x00FFF300u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00FFFF00u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
        },
    };

    constexpr int elder_mara_page_count = 2;
    constexpr const char* elder_mara_dialogue[elder_mara_page_count][3] =
    {
        { "GOOD MORNING JOHN", "THE HEADWATER PATH", "IS QUIET TODAY" },
        { "LOOK BEYOND THE", "OLD GARDEN STONES", "SECRETS REWARD CARE" },
    };

    [[nodiscard]] constexpr bool walkable(int map_id, int x, int y)
    {
        return map_id >= 0 && map_id < map_count && x >= 0 && x < 32 && y >= 0 && y < 32 &&
               ((collision[map_id][y] >> x) & 1u) != 0;
    }
}

#endif
