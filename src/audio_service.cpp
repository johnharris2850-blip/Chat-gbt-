#include "audio_service.h"

#include "bn_sound_items.h"

namespace crown
{
    void AudioService::initialize()
    {
        // bn::core owns the GBA audio driver. Keeping game-facing audio state in a
        // service prevents scenes from depending directly on the mixer and music
        // implementation that later milestones will introduce.
        _initialized = true;
    }

    void AudioService::play_interaction() const
    {
        if(_initialized)
        {
            bn::sound_items::interact.play();
        }
    }

    bool AudioService::initialized() const
    {
        return _initialized;
    }
}
