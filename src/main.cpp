#include "bn_core.h"
#include "bn_optional.h"

#include "audio_service.h"
#include "game_state.h"
#include "input.h"
#include "save_service.h"
#include "title_state.h"
#include "world_state.h"

int main()
{
    bn::core::init();

    crown::AudioService audio;
    audio.initialize();

    crown::SaveService save;
    save.initialize();

    crown::GameState state = crown::GameState::title;
    bn::optional<crown::TitleState> title;
    bn::optional<crown::WorldState> overworld;
    title.emplace();

    while(true)
    {
        const crown::Input input = crown::read_input();

        if(state == crown::GameState::title)
        {
            const crown::GameState next_state = title->update(input);

            if(next_state != state)
            {
                title.reset();
                overworld.emplace(save, audio);
                state = next_state;
            }
        }
        else
        {
            overworld->update(input);
        }

        bn::core::update();
    }
}
