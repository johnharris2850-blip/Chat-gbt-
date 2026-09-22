#ifndef CROWN_INPUT_H
#define CROWN_INPUT_H

namespace crown
{
    struct Input
    {
        bool start_pressed = false;
        bool action_pressed = false;
        bool cancel_pressed = false;
        bool left_held = false;
        bool right_held = false;
        bool up_held = false;
        bool down_held = false;
    };

    [[nodiscard]] Input read_input();
}

#endif
