#ifndef CROWN_LETTER_RENDERER_H
#define CROWN_LETTER_RENDERER_H

#include "bn_string_view.h"
#include "bn_vector.h"
#include "bn_sprite_ptr.h"

namespace crown
{
    using TextSprites = bn::vector<bn::sprite_ptr, 48>;

    void render_text(bn::string_view text, int center_x, int y, TextSprites& output);
}

#endif
