#include "title_state.h"

#include "bn_bg_palettes.h"
#include "bn_color.h"
#include "bn_regular_bg_items_title.h"

namespace crown
{
    TitleState::TitleState() :
        _background(bn::regular_bg_items::title.create_bg(0, 0))
    {
        bn::bg_palettes::set_transparent_color(bn::color(2, 4, 10));
        render_text("CROWN", 0, -34, _sprites);
        render_text("&", 0, -12, _sprites);
        render_text("CHAOS", 0, 10, _sprites);
        render_text("PRESS START", 0, 48, _sprites);
    }

    GameState TitleState::update(const Input& input)
    {
        ++_frame;
        for(bn::sprite_ptr& sprite : _sprites)
        {
            if(sprite.y() == 48)
            {
                sprite.set_visible((_frame / 30) % 2 == 0);
            }
        }
        return input.start_pressed ? GameState::intro : GameState::title;
    }
}
