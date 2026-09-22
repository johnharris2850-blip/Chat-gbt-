#ifndef CROWN_WORLD_STATE_H
#define CROWN_WORLD_STATE_H

#include "bn_camera_ptr.h"
#include "bn_optional.h"
#include "bn_regular_bg_ptr.h"
#include "bn_sprite_ptr.h"

#include "audio_service.h"
#include "input.h"
#include "letter_renderer.h"
#include "save_service.h"

namespace crown
{
    enum class Direction : std::uint8_t { down, up, left, right };

    class WorldState
    {
    public:
        WorldState(SaveService& save_service, AudioService& audio_service);
        void update(const Input& input);

    private:
        enum class UiMode { none, dialogue, start_menu, discovery };

        void load_map(std::uint8_t map_id, int x, int y);
        void update_movement(const Input& input);
        void try_interaction();
        void advance_dialogue();
        void show_dialogue_page();
        void open_start_menu();
        void close_ui();
        void check_transition();
        void check_secret();
        void persist();
        [[nodiscard]] bool can_occupy(int x, int y) const;

        SaveService& _save_service;
        AudioService& _audio_service;
        bn::camera_ptr _camera;
        bn::regular_bg_ptr _background;
        bn::sprite_ptr _player;
        bn::optional<bn::sprite_ptr> _npc;
        bn::optional<bn::sprite_ptr> _secret_marker;
        TextSprites _ui_sprites;
        bn::vector<bn::sprite_ptr, 4> _ui_panels;
        std::uint8_t _map_id = 0;
        Direction _facing = Direction::down;
        UiMode _ui_mode = UiMode::none;
        int _player_x = 0;
        int _player_y = 0;
        int _walk_frame = 0;
        int _dialogue_page = 0;
        bool _secret_discovered = false;
        bool _elder_spoken_to = false;
    };
}

#endif
