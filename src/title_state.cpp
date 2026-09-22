#include "title_state.h"

#include "bn_bg_palettes.h"
#include "bn_color.h"

namespace crown
{
    TitleState::TitleState()
    {
        bn::bg_palettes::set_transparent_color(bn::color(2, 4, 10));
        render_text("CROWN", 0, -34, _sprites);
        render_text("&", 0, -12, _sprites);
        render_text("CHAOS", 0, 10, _sprites);
        _prompt_start = _sprites.size();
        render_text("PRESS START", 0, 48, _sprites);
    }

    GameState TitleState::update(const Input& input)
    {
        ++_frame;
        const bool visible = (_frame / 30) % 2 == 0;
        for(int index = _prompt_start; index < _sprites.size(); ++index)
        {
            _sprites[index].set_visible(visible);
        }
        return input.start_pressed ? GameState::intro : GameState::title;
    }
}
