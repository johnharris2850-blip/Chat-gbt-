#ifndef CROWN_LETTER_RENDERER_H
#define CROWN_LETTER_RENDERER_H

#include "bn_string_view.h"
#include "bn_vector.h"
#include "bn_sprite_ptr.h"

namespace crown
{
    // Three 23-character dialogue lines fit beneath the GBA's 128 OBJ limit.
    using TextSprites = bn::vector<bn::sprite_ptr, 72>;

    void render_text(bn::string_view text, int center_x, int y, TextSprites& output);
}

#endif
