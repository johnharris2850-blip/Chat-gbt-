#include "letter_renderer.h"

#include "bn_sprite_items_letters.h"

namespace
{
    [[nodiscard]] int graphics_index(char character)
    {
        constexpr char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        for(int index = 0; index < 26; ++index)
        {
            if(alphabet[index] == character)
            {
                return index;
            }
        }

        return -1;
    }
}

namespace crown
{
    void render_text(bn::string_view text, int center_x, int y, TextSprites& output)
    {
        constexpr int advance = 10;
        const int start_x = center_x - (text.size() * advance) / 2 + advance / 2;

        for(int index = 0; index < text.size(); ++index)
        {
            const int tile = graphics_index(text[index]);

            if(tile >= 0)
            {
                output.push_back(bn::sprite_items::letters.create_sprite(start_x + index * advance, y, tile));
            }
        }
    }
}
