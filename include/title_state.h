#ifndef CROWN_TITLE_STATE_H
#define CROWN_TITLE_STATE_H

#include "game_state.h"
#include "input.h"
#include "letter_renderer.h"

namespace crown
{
    class TitleState
    {
    public:
        TitleState();
        [[nodiscard]] GameState update(const Input& input);

    private:
        TextSprites _sprites;
        int _frame = 0;
        int _prompt_start = 0;
    };
}

#endif
