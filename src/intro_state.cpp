#include "intro_state.h"

#include "bn_bg_palettes.h"
#include "bn_color.h"
#include "bn_sprite_items_ui_panel.h"

namespace
{
    constexpr int page_count = 6;
    constexpr const char* pages[page_count][3] =
    {
        { "WELCOME TO THE WORLD", "OF CROWN & CHAOS", "" },
        { "ANCIENT CREATURES AND", "MANKIND LIVED SIDE BY", "SIDE FOR GENERATIONS" },
        { "BUT SOMETHING IS", "CHANGING", "" },
        { "OLD POWERS ARE", "BEGINNING TO AWAKEN", "" },
        { "YOUR NAME IS JOHN", "", "" },
        { "AND TODAY YOUR", "JOURNEY BEGINS", "" },
    };
}

namespace crown
{
    IntroState::IntroState()
    {
        bn::bg_palettes::set_transparent_color(bn::color(1, 3, 8));
        for(int index = 0; index < 4; ++index)
        {
            _panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96 + index * 64, 0));
        }
        show_page();
    }

    GameState IntroState::update(const Input& input)
    {
        if(input.action_pressed)
        {
            ++_page;
            if(_page == page_count)
            {
                return GameState::overworld;
            }
            show_page();
        }
        return GameState::intro;
    }

    void IntroState::show_page()
    {
        _text.clear();
        for(int line = 0; line < 3; ++line)
        {
            render_text(pages[_page][line], 0, -18 + line * 18, _text);
        }
    }
}
