#include "save_service.h"

#include "bn_sram.h"

namespace
{
    constexpr std::uint32_t save_magic = 0x434E5243; // "CRNC"
    constexpr std::uint16_t save_version = 3;

    [[nodiscard]] std::uint16_t checksum(const crown::SaveData& data)
    {
        const auto* bytes = reinterpret_cast<const std::uint8_t*>(&data);
        std::uint16_t result = 0x6D2B;

        for(unsigned index = 0; index < sizeof(data); ++index)
        {
            if(index != 6 && index != 7)
            {
                result = static_cast<std::uint16_t>((result << 5) | (result >> 11));
                result = static_cast<std::uint16_t>(result ^ bytes[index]);
            }
        }

        return result;
    }
}

namespace crown
{
    void SaveService::initialize()
    {
        SaveData stored;
        bn::sram::read(stored);

        if(stored.magic == save_magic && stored.version == save_version && stored.checksum == checksum(stored))
        {
            _data = stored;
            _loaded_existing_save = true;
        }
        else
        {
            _data = SaveData {};
            _data.magic = save_magic;
            _data.version = save_version;
        }

        ++_data.boot_count;
        write();
    }

    void SaveService::save_world(std::uint8_t map_id, std::int16_t player_x, std::int16_t player_y,
                                 std::uint8_t facing, bool candy_spoken_to, bool finale_seen)
    {
        _data.map_id = map_id;
        _data.player_x = player_x;
        _data.player_y = player_y;
        _data.facing = facing;
        _data.candy_spoken_to = candy_spoken_to;
        _data.finale_seen = finale_seen;
        write();
    }

    const SaveData& SaveService::data() const
    {
        return _data;
    }

    bool SaveService::loaded_existing_save() const
    {
        return _loaded_existing_save;
    }

    void SaveService::write()
    {
        _data.checksum = checksum(_data);
        bn::sram::write(_data);
    }
}
