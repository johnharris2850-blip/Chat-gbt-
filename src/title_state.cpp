#include "title_state.h"

#include "bn_bg_palettes.h"
#include "bn_color.h"

namespace crown
{
    TitleState::TitleState()
    {
        bn::bg_palettes::set_transparent_color(bn::color(2, 4, 10));
        render_text("CROWN", 0, -34, _sprites);
        render_text("AND", 0, -12, _sprites);
        render_text("CHAOS", 0, 10, _sprites);
        render_text("PRESS START", 0, 48, _sprites);
    }

    GameState TitleState::update(const Input& input) const
    {
        return input.start_pressed ? GameState::overworld : GameState::title;
    }
}
