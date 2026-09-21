#include "input.h"

#include "bn_keypad.h"

namespace crown
{
    Input read_input()
    {
        return Input {
            bn::keypad::start_pressed(),
            bn::keypad::a_pressed(),
            bn::keypad::b_pressed(),
            bn::keypad::left_held(),
            bn::keypad::right_held(),
            bn::keypad::up_held(),
            bn::keypad::down_held()
        };
    }
}
