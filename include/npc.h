#ifndef CROWN_NPC_H
#define CROWN_NPC_H

#include <cstdint>

namespace crown
{
    struct Npc
    {
        std::uint8_t map_id;
        std::uint8_t tile_x;
        std::uint8_t tile_y;
        std::uint8_t sprite_index;
        std::uint8_t dialogue_id;
        bool requires_objective;
    };
}

#endif
