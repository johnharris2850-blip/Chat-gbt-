#ifndef CROWN_AUDIO_SERVICE_H
#define CROWN_AUDIO_SERVICE_H

namespace crown
{
    class AudioService
    {
    public:
        void initialize();
        void play_interaction() const;

        [[nodiscard]] bool initialized() const;

    private:
        bool _initialized = false;
    };
}

#endif
