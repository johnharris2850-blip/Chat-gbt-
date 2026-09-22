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
        enum class UiMode { none, dialogue, menu, objective, finale };
        void load_map(std::uint8_t map_id, int x, int y);
        void rebuild_npcs();
        void update_movement(const Input& input);
        void interact();
        void open_dialogue(std::uint8_t dialogue);
        void show_page();
        void advance_dialogue();
        void open_menu();
        void close_ui();
        void transition_if_needed();
        void trigger_road_scene();
        void persist();
        [[nodiscard]] bool can_occupy(int x, int y) const;

        SaveService& _save;
        AudioService& _audio;
        bn::camera_ptr _camera;
        bn::regular_bg_ptr _background;
        bn::sprite_ptr _player;
        bn::vector<bn::sprite_ptr, 6> _npc_sprites;
        TextSprites _ui_text;
        bn::vector<bn::sprite_ptr, 4> _ui_panels;
        std::uint8_t _map_id = 0;
        Direction _facing = Direction::down;
        UiMode _ui_mode = UiMode::none;
        int _player_x = 4;
        int _player_y = 36;
        int _walk_frame = 0;
        int _dialogue = 0;
        int _page = 0;
        int _shake_frames = 0;
        bool _candy_spoken = false;
        bool _demo_complete = false;
    };
}

#endif
