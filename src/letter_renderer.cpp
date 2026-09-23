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

        if(character >= '0' && character <= '9')
        {
            return 27 + character - '0';
        }

        return -1;
    }
}

namespace crown
{
    void render_text(bn::string_view text, int center_x, int y, TextSprites& output)
    {
        // The generated glyph sheet uses 16x16 OBJ cells, but the actual letters are
        // compact. Scale the cells down to a GBA-RPG dialogue size and use a tight
        // advance so 23-character lines fit cleanly inside the dialogue panel.
        constexpr int advance = 6;
        const int start_x = center_x - (text.size() * advance) / 2 + advance / 2;

        for(int index = 0; index < text.size(); ++index)
        {
            const int tile = graphics_index(text[index]);

            if(tile >= 0)
            {
                bn::sprite_ptr glyph = bn::sprite_items::letters.create_sprite(start_x + index * advance, y, tile);
                // Keep glyphs unscaled. Scaling each character consumes scarce
                // sprite affine resources on real GBA hardware/emulators.
                output.push_back(bn::move(glyph));
            }
        }
    }
}
