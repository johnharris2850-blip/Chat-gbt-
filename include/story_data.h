#ifndef CROWN_STORY_DATA_H
#define CROWN_STORY_DATA_H

#include <cstdint>

namespace crown::story
{
    struct Npc
    {
        std::uint8_t map_id;
        std::uint8_t tile_x;
        std::uint8_t tile_y;
        std::uint8_t graphic;
        std::uint8_t dialogue;
    };

    constexpr Npc npcs[] =
    {
        { 2, 14, 15, 12, 0 }, { 2, 19, 18, 13, 1 }, { 2, 11, 21, 14, 2 },
        { 2, 26, 17, 15, 3 }, { 3, 27, 18, 15, 4 },
    };

    constexpr const char* dialogue[5][4][3] =
    {
        { { "MORNING JOHN", "YOU ARE OUT EARLY", "" } },
        { { "STRANGE LIGHTS", "SHONE BEYOND THE", "OLD ROAD" } },
        { { "YOUR FRIEND CANDY", "WAS LOOKING FOR YOU", "" } },
        { { "THERE YOU ARE", "", "" }, { "I HAVE BEEN", "WAITING FOR YOU", "" },
          { "SOMETHING STRANGE", "HAPPENED NEAR THE", "OLD ROAD LAST NIGHT" },
          { "WE SHOULD GO AND", "SEE WHAT IS GOING ON", "" } },
        { { "JOHN LOOK", "", "" }, { "THE GROUND", "IS SHAKING", "" },
          { "SOMETHING IS", "COMING", "" } },
    };

    constexpr int page_counts[] = { 1, 1, 1, 4, 3 };
}

#endif
