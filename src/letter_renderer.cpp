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

        if(character == '&')
        {
            return 26;
        }

        return -1;
    }
}

namespace crown
{
    void render_text(bn::string_view text, int center_x, int y, TextSprites& output)
    {
        // The generated glyph sheet uses 16x16 OBJ cells, but the actual letters are\n        // compact. Scale the cells down to a GBA-RPG dialogue size and use a tight\n        // advance so 23-character lines fit cleanly inside the dialogue panel.\n        constexpr int advance = 7;
        const int start_x = center_x - (text.size() * advance) / 2 + advance / 2;

        for(int index = 0; index < text.size(); ++index)
        {
            const int tile = graphics_index(text[index]);

            if(tile >= 0)
            {
                bn::sprite_ptr glyph = bn::sprite_items::letters.create_sprite(start_x + index * advance, y, tile);\n                glyph.set_scale(0.5);\n                output.push_back(bn::move(glyph));
            }
        }
    }
}
