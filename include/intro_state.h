#ifndef CROWN_INTRO_STATE_H
#define CROWN_INTRO_STATE_H

#include "bn_sprite_ptr.h"
#include "bn_vector.h"

#include "game_state.h"
#include "input.h"
#include "letter_renderer.h"

namespace crown
{
    class IntroState
    {
    public:
        IntroState();
        [[nodiscard]] GameState update(const Input& input);

    private:
        void render_page();

        TextSprites _text;
        bn::vector<bn::sprite_ptr, 4> _panels;
        int _page = 0;
    };
}

#endif
