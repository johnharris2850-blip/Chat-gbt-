#ifndef CROWN_SAVE_SERVICE_H
#define CROWN_SAVE_SERVICE_H

#include <cstdint>

namespace crown
{
    struct SaveData
    {
        std::uint32_t magic = 0;
        std::uint16_t version = 0;
        std::uint16_t checksum = 0;
        std::uint32_t boot_count = 0;
        std::int16_t player_x = -4;
        std::int16_t player_y = 20;
        std::uint8_t map_id = 0;
        std::uint8_t facing = 0;
        std::uint8_t secret_discovered = 0;
        std::uint8_t elder_spoken_to = 0;
        std::uint8_t reserved[12] = {};
    };

    static_assert(sizeof(SaveData) == 32, "SaveData layout changed; add a migration before changing it");

    class SaveService
    {
    public:
        void initialize();
        void save_world(std::uint8_t map_id, std::int16_t player_x, std::int16_t player_y,
                        std::uint8_t facing, bool secret_discovered, bool elder_spoken_to);

        [[nodiscard]] const SaveData& data() const;
        [[nodiscard]] bool loaded_existing_save() const;

    private:
        void write();

        SaveData _data;
        bool _loaded_existing_save = false;
    };
}

#endif
