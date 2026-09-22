#include "world_state.h"

#include "bn_algorithm.h"
#include "bn_regular_bg_items_johns_home.h"
#include "bn_regular_bg_items_starter_area.h"
#include "bn_sprite_items_markers.h"
#include "bn_sprite_items_ui_panel.h"

#include "generated/world_data.h"

namespace
{
    constexpr int map_half_size = 128;
    // Collision uses John's feet rather than the full 16x16 placeholder sprite.
    constexpr int player_radius = 3;

    [[nodiscard]] int tile_at(int pixel)
    {
        return (pixel + map_half_size) / 8;
    }

    [[nodiscard]] bn::regular_bg_ptr create_background(std::uint8_t map_id)
    {
        return map_id == 0 ? bn::regular_bg_items::starter_area.create_bg(0, 0) :
                             bn::regular_bg_items::johns_home.create_bg(0, 0);
    }
}

namespace crown
{
    WorldState::WorldState(SaveService& save_service, AudioService& audio_service) :
        _save_service(save_service),
        _audio_service(audio_service),
        _camera(bn::camera_ptr::create(0, 0)),
        _background(create_background(save_service.data().map_id)),
        _player(bn::sprite_items::markers.create_sprite(0, 0, 0))
    {
        const SaveData& save = save_service.data();
        _secret_discovered = save.secret_discovered;
        _elder_spoken_to = save.elder_spoken_to;
        _facing = static_cast<Direction>(save.facing < 4 ? save.facing : 0);
        load_map(save.map_id < generated::map_count ? save.map_id : 0, save.player_x, save.player_y);
    }

    void WorldState::update(const Input& input)
    {
        if(_ui_mode != UiMode::none)
        {
            if(input.cancel_pressed || (_ui_mode == UiMode::start_menu && input.start_pressed))
            {
                close_ui();
            }
            else if(input.action_pressed)
            {
                advance_dialogue();
            }
            return;
        }
        if(input.start_pressed) { open_start_menu(); return; }
        if(input.action_pressed) { try_interaction(); return; }
        update_movement(input);
        check_transition();
        check_secret();
    }

    void WorldState::load_map(std::uint8_t map_id, int x, int y)
    {
        _map_id = map_id;
        _player_x = x;
        _player_y = y;
        _background = create_background(map_id);
        _background.set_camera(_camera);
        _player.set_camera(_camera);
        _player.set_position(x, y);
        _npc.reset();
        _secret_marker.reset();
        if(map_id == 0)
        {
            _npc = bn::sprite_items::markers.create_sprite(generated::elder_x, generated::elder_y, 12);
            _npc->set_camera(_camera);
            if(_secret_discovered)
            {
                _secret_marker = bn::sprite_items::markers.create_sprite(generated::secret_x, generated::secret_y, 13);
                _secret_marker->set_camera(_camera);
            }
        }
        _camera.set_position(bn::clamp(x, -8, 8), bn::clamp(y, -48, 48));
        persist();
    }

    void WorldState::update_movement(const Input& input)
    {
        int next_x = _player_x;
        int next_y = _player_y;
        if(input.left_held) { --next_x; _facing = Direction::left; }
        else if(input.right_held) { ++next_x; _facing = Direction::right; }
        else if(input.up_held) { --next_y; _facing = Direction::up; }
        else if(input.down_held) { ++next_y; _facing = Direction::down; }

        const bool moved = next_x != _player_x || next_y != _player_y;
        if(moved && can_occupy(next_x, next_y))
        {
            _player_x = next_x;
            _player_y = next_y;
            _player.set_position(_player_x, _player_y);
            _walk_frame = (_walk_frame + 1) % 24;
        }
        else if(! moved)
        {
            _walk_frame = 0;
        }

        const int direction_frame = static_cast<int>(_facing) * 3;
        _player.set_tiles(bn::sprite_items::markers.tiles_item(), direction_frame + (_walk_frame / 8));
        _camera.set_position(bn::clamp(_player_x, -8, 8), bn::clamp(_player_y, -48, 48));
    }

    bool WorldState::can_occupy(int x, int y) const
    {
        const int left = tile_at(x - player_radius);
        const int right = tile_at(x + player_radius);
        const int top = tile_at(y - player_radius);
        const int bottom = tile_at(y + player_radius);
        if(! generated::walkable(_map_id, left, top) || ! generated::walkable(_map_id, right, top) ||
           ! generated::walkable(_map_id, left, bottom) || ! generated::walkable(_map_id, right, bottom))
        {
            return false;
        }
        return ! (_map_id == 0 && tile_at(x) == generated::elder_tile_x && tile_at(y) == generated::elder_tile_y);
    }

    void WorldState::try_interaction()
    {
        int look_x = tile_at(_player_x);
        int look_y = tile_at(_player_y);
        if(_facing == Direction::left) --look_x;
        else if(_facing == Direction::right) ++look_x;
        else if(_facing == Direction::up) --look_y;
        else ++look_y;

        if(_map_id == 0 && look_x == generated::elder_tile_x && look_y == generated::elder_tile_y)
        {
            _elder_spoken_to = true;
            _dialogue_page = 0;
            _ui_mode = UiMode::dialogue;
            _audio_service.play_interaction();
            show_dialogue_page();
            persist();
        }
    }

    void WorldState::advance_dialogue()
    {
        if(_ui_mode == UiMode::dialogue && _dialogue_page + 1 < generated::elder_mara_page_count)
        {
            ++_dialogue_page;
            show_dialogue_page();
        }
        else
        {
            close_ui();
        }
    }

    void WorldState::show_dialogue_page()
    {
        _ui_sprites.clear();
        _ui_panels.clear();
        for(int index = 0; index < 4; ++index)
        {
            _ui_panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96 + index * 64, 48));
        }
        for(int line = 0; line < 3; ++line)
        {
            render_text(generated::elder_mara_dialogue[_dialogue_page][line], 0, 30 + line * 15, _ui_sprites);
        }
    }

    void WorldState::open_start_menu()
    {
        _ui_mode = UiMode::start_menu;
        _ui_panels.clear();
        for(int index = 0; index < 4; ++index)
        {
            _ui_panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96 + index * 64, 0));
        }
        render_text("JOHN", 0, -20, _ui_sprites);
        render_text(_map_id == 0 ? "PILGRIMS REST" : "JOHNS HOME", 0, 0, _ui_sprites);
        render_text(_secret_discovered ? "SECRET FOUND" : "SECRET UNKNOWN", 0, 20, _ui_sprites);
        persist();
    }

    void WorldState::close_ui()
    {
        _ui_sprites.clear();
        _ui_panels.clear();
        _ui_mode = UiMode::none;
    }

    void WorldState::check_transition()
    {
        const int tile_x = tile_at(_player_x);
        const int tile_y = tile_at(_player_y);
        if(_map_id == 0 && tile_x == 15 && tile_y == 14)
        {
            load_map(1, generated::home_spawn_x, generated::home_spawn_y);
        }
        else if(_map_id == 1 && tile_x == 15 && tile_y == 27)
        {
            load_map(0, generated::outside_spawn_x, generated::outside_spawn_y);
        }
    }

    void WorldState::check_secret()
    {
        if(! _secret_discovered && _map_id == 0 && tile_at(_player_x) == 7 && tile_at(_player_y) == 21)
        {
            _secret_discovered = true;
            _secret_marker = bn::sprite_items::markers.create_sprite(generated::secret_x, generated::secret_y, 13);
            _secret_marker->set_camera(_camera);
            _ui_mode = UiMode::discovery;
            _audio_service.play_interaction();
            for(int index = 0; index < 4; ++index)
            {
                _ui_panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96 + index * 64, 48));
            }
            render_text("SECRET DISCOVERED", 0, 42, _ui_sprites);
            render_text("A CROWN IN STONE", 0, 58, _ui_sprites);
            persist();
        }
    }

    void WorldState::persist()
    {
        _save_service.save_world(_map_id, _player_x, _player_y, static_cast<std::uint8_t>(_facing),
                                 _secret_discovered, _elder_spoken_to);
    }
}
