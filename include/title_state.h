#ifndef CROWN_TITLE_STATE_H
#define CROWN_TITLE_STATE_H

#include "game_state.h"
#include "input.h"
#include "letter_renderer.h"
#include "bn_regular_bg_ptr.h"

namespace crown
{
    class TitleState
    {
    public:
        TitleState();
        [[nodiscard]] GameState update(const Input& input);

    private:
        TextSprites _sprites;
        bn::regular_bg_ptr _background;
        int _frame = 0;
    };
}

#endif
