#include "save_service.h"

#include <cassert>

int main()
{
    static_assert(sizeof(crown::SaveData) == 32);
    const crown::SaveData save;
    assert(save.version == 0);
    assert(save.map_id == 0);
    assert(save.player_x == 4);
    assert(save.player_y == 36);
    assert(save.candy_spoken == 0);
    assert(save.demo_complete == 0);
}
