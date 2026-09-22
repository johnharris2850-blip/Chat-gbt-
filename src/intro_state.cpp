#include "intro_state.h"

#include "bn_bg_palettes.h"
#include "bn_color.h"
#include "bn_sprite_items_ui_panel.h"

namespace
{
    constexpr const char* pages[6][3] =
    {
        { "WELCOME TO THE WORLD", "OF CROWN & CHAOS", "" },
        { "ANCIENT CREATURES", "AND MANKIND LIVED", "SIDE BY SIDE" },
        { "FOR GENERATIONS", "BUT SOMETHING", "IS CHANGING" },
        { "OLD POWERS ARE", "BEGINNING TO AWAKEN", "" },
        { "YOUR NAME IS JOHN", "", "" },
        { "AND TODAY", "YOUR JOURNEY BEGINS", "" },
    };
}

namespace crown
{
    IntroState::IntroState()
    {
        bn::bg_palettes::set_transparent_color(bn::color(3, 5, 9));
        for(int index = 0; index < 4; ++index)
        {
            _panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96 + index * 64, 42));
        }
        render_page();
    }

    GameState IntroState::update(const Input& input)
    {
        if(input.action_pressed)
        {
            ++_page;
            if(_page == 6)
            {
                return GameState::overworld;
            }
            render_page();
        }
        return GameState::intro;
    }

    void IntroState::render_page()
    {
        _text.clear();
        for(int line = 0; line < 3; ++line)
        {
            render_text(pages[_page][line], 0, 27 + line * 16, _text);
        }
    }
}
