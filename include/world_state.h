#ifndef CROWN_WORLD_STATE_H
#define CROWN_WORLD_STATE_H

#include "bn_camera_ptr.h"
#include "bn_regular_bg_ptr.h"
#include "bn_sprite_ptr.h"
#include "bn_vector.h"
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
        enum class UiMode { none, dialogue, start_menu, starter_scene, party, battle };
        void load_map(std::uint8_t map_id, int x, int y);
        void spawn_npcs();
        void update_movement(const Input& input);
        void try_interaction();
        void begin_dialogue(std::uint8_t dialogue_id);
        void advance_dialogue();
        void show_dialogue_page();
        void open_start_menu();
        void show_starter_scene();
        void show_party();
        void start_first_battle();
        void show_battle();
        void choose_battle_move(const Input& input);
        void close_ui();
        void check_transition();
        void check_finale();
        void persist();
        [[nodiscard]] bool can_occupy(int x, int y) const;

        SaveService& _save_service;
        AudioService& _audio_service;
        bn::camera_ptr _camera;
        bn::regular_bg_ptr _background;
        bn::sprite_ptr _player;
        bn::vector<bn::sprite_ptr, 8> _npcs;
        TextSprites _ui_sprites;
        bn::vector<bn::sprite_ptr, 4> _ui_panels;
        bn::vector<bn::sprite_ptr, 2> _creature_sprites;
        std::uint8_t _map_id = 0;
        std::uint8_t _dialogue_id = 0;
        Direction _facing = Direction::down;
        UiMode _ui_mode = UiMode::none;
        int _player_x = 0;
        int _player_y = 0;
        int _walk_frame = 0;
        int _dialogue_page = 0;
        int _shake_frames = 0;
        bool _candy_spoken_to = false;
        bool _finale_seen = false;
        bool _first_battle_seen = false;
        int _tideling_hp = 20;
        int _wild_hp = 16;
        int _battle_turn = 0;
        int _battle_move = 0;
        int _tideling_exp = 0;
        int _tideling_level = 5;
    };
}

#endif
