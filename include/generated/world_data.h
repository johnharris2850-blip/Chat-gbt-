#ifndef CROWN_GENERATED_WORLD_DATA_H
#define CROWN_GENERATED_WORLD_DATA_H

#include <cstdint>

namespace crown::generated
{
    constexpr int map_count = 4;
    constexpr std::uint32_t collision[map_count][32] =
    {
        {
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x01FFFF80u,
            0x01FFFF80u,
            0x0187E080u,
            0x0187E080u,
            0x0187E080u,
            0x01FFE080u,
            0x01FFE080u,
            0x01FFE080u,
            0x011FE080u,
            0x011FFF80u,
            0x011FFF80u,
            0x011FFF80u,
            0x011FFF80u,
            0x01FFFF80u,
            0x01FFFF80u,
            0x01FFF180u,
            0x01FFF180u,
            0x01FFF180u,
            0x01FFFF80u,
            0x01FFFF80u,
            0x01FFFF80u,
            0x01FFFF80u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
        },
        {
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x060FE060u,
            0x060FE060u,
            0x060FE060u,
            0x060FE060u,
            0x060FFFE0u,
            0x060FFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FF81E0u,
            0x07FF81E0u,
            0x078F81E0u,
            0x078F81E0u,
            0x078F81E0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x07FFFFE0u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
        },
        {
            0x00000000u,
            0x01FFFFFEu,
            0x01FFFFFEu,
            0x0101FE02u,
            0x0101FE02u,
            0x0101FE02u,
            0x0101FE02u,
            0x0101FE02u,
            0x0101FE02u,
            0x010183FEu,
            0x01FF83FEu,
            0x01FF83FEu,
            0x01FF83FEu,
            0x7FFF83FEu,
            0x7FFF83FEu,
            0x7FFF83FEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7C03FF80u,
            0x7C03FF80u,
            0x7C03FF80u,
            0x7C03FF80u,
            0x7C03FF80u,
            0x7C03FF80u,
            0x7C03FF80u,
            0x7FFFFF80u,
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
            0x7FFFFFFEu,
            0x7FFFF0FEu,
            0x7FFFF0FEu,
            0x7FFFF0FEu,
            0x7FFFF0FEu,
            0x7FFFF0FEu,
            0x7FFFF0FEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FFFFFFEu,
            0x7FC3FFFEu,
            0x7FC3FFFEu,
            0x7FC3FFFEu,
            0x7FC3FFFEu,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
            0x00000000u,
        },
    };

    constexpr int villager_1_page_count = 1;
    constexpr const char* villager_1_dialogue[villager_1_page_count][3] =
    {
        { "MORNING JOHN", "YOURE OUT EARLY", "" },
    };

    constexpr int villager_2_page_count = 2;
    constexpr const char* villager_2_dialogue[villager_2_page_count][3] =
    {
        { "PEOPLE HAVE BEEN", "TALKING ABOUT STRANGE", "" },
        { "LIGHTS BEYOND THE", "OLD ROAD", "" },
    };

    constexpr int villager_3_page_count = 1;
    constexpr const char* villager_3_dialogue[villager_3_page_count][3] =
    {
        { "YOUR FRIEND CANDY", "WAS LOOKING FOR YOU", "" },
    };

    constexpr int candy_page_count = 5;
    constexpr const char* candy_dialogue[candy_page_count][3] =
    {
        { "THERE YOU ARE", "", "" },
        { "IVE BEEN WAITING", "FOR YOU", "" },
        { "SOMETHING STRANGE", "HAPPENED NEAR THE", "OLD ROAD LAST NIGHT" },
        { "WE SHOULD GO AND SEE", "WHATS GOING ON", "" },
        { "OBJECTIVE", "MEET CANDY AT THE", "OLD ROAD" },
    };

    constexpr int finale_page_count = 4;
    constexpr const char* finale_dialogue[finale_page_count][3] =
    {
        { "JOHN LOOK", "", "" },
        { "THE GROUND IS", "SHAKING", "" },
        { "SOMETHING IS COMING", "", "" },
        { "CROWN & CHAOS", "TO BE CONTINUED", "" },
    };

    constexpr int jexi_before_candy_page_count = 2;
    constexpr const char* jexi_before_candy_dialogue[jexi_before_candy_page_count][3] =
    {
        { "JEXI HERE", "PROFESSORS ASSISTANT", "" },
        { "LOOKING FOR CANDY", "TRY EAST CROWNHAVEN", "" },
    };

    constexpr int jexi_after_candy_page_count = 2;
    constexpr const char* jexi_after_candy_dialogue[jexi_after_candy_page_count][3] =
    {
        { "LOST AGAIN JOHN", "I WAS WONDERING", "HOW LONG IT WOULD TAKE" },
        { "YOUR NEXT STOP IS", "THE OLD ROAD", "HEAD EAST" },
    };

    [[nodiscard]] constexpr bool walkable(int map_id, int x, int y)
    {
        return map_id >= 0 && map_id < map_count && x >= 0 && x < 32 && y >= 0 && y < 32 &&
               ((collision[map_id][y] >> x) & 1u) != 0;
    }
}

#endif
