#include "world_state.h"

#include "bn_algorithm.h"
#include "bn_bg_palettes.h"
#include "bn_core.h"
#include "bn_regular_bg_items_crownhaven.h"
#include "bn_regular_bg_items_johns_bedroom.h"
#include "bn_regular_bg_items_johns_house.h"
#include "bn_regular_bg_items_old_road.h"
#include "bn_sprite_items_markers.h"
#include "bn_sprite_items_ui_panel.h"

#include "generated/world_data.h"
#include "story_data.h"

namespace
{
    constexpr int map_half = 124;
    constexpr int player_radius = 3;
    int tile_at(int pixel) { return (pixel + map_half) / 8; }
    int pixel_at(int tile) { return tile * 8 - map_half; }

    bn::regular_bg_ptr make_background(std::uint8_t map)
    {
        if(map == 0) return bn::regular_bg_items::johns_bedroom.create_bg(0, 0);
        if(map == 1) return bn::regular_bg_items::johns_house.create_bg(0, 0);
        if(map == 2) return bn::regular_bg_items::crownhaven.create_bg(0, 0);
        return bn::regular_bg_items::old_road.create_bg(0, 0);
    }
}

namespace crown
{
    WorldState::WorldState(SaveService& save, AudioService& audio) :
        _save(save), _audio(audio), _camera(bn::camera_ptr::create(0, 0)),
        _background(make_background(0)), _player(bn::sprite_items::markers.create_sprite(0, 0, 0))
    {
        const SaveData& data = save.data();
        _candy_spoken = data.candy_spoken;
        _demo_complete = data.demo_complete;
        _facing = static_cast<Direction>(data.facing < 4 ? data.facing : 0);
        load_map(data.map_id < generated::map_count ? data.map_id : 0, data.player_x, data.player_y);
    }

    void WorldState::update(const Input& input)
    {
        if(_shake_frames > 0)
        {
            --_shake_frames;
            _camera.set_x((_shake_frames % 2) ? 3 : -3);
            if(_shake_frames == 0) open_dialogue(4);
            return;
        }
        if(_ui_mode != UiMode::none)
        {
            if(_ui_mode == UiMode::menu)
            {
                if(input.action_pressed || input.cancel_pressed || input.start_pressed) close_ui();
            }
            else if(input.action_pressed) advance_dialogue();
            return;
        }
        if(input.start_pressed) { open_menu(); return; }
        if(input.action_pressed) { interact(); return; }
        update_movement(input);
        transition_if_needed();
        trigger_road_scene();
    }

    void WorldState::load_map(std::uint8_t map, int x, int y)
    {
        bn::bg_palettes::set_fade_intensity(0.5);
        bn::core::update();
        _map_id = map; _player_x = x; _player_y = y;
        _background = make_background(map);
        _background.set_camera(_camera);
        _player.set_camera(_camera);
        _player.set_position(x, y);
        rebuild_npcs();
        _camera.set_position(bn::clamp(x, -8, 8), bn::clamp(y, -48, 48));
        bn::bg_palettes::set_fade_intensity(0);
        persist();
    }

    void WorldState::rebuild_npcs()
    {
        _npc_sprites.clear();
        for(const story::Npc& npc : story::npcs)
        {
            if(npc.map_id == _map_id)
            {
                _npc_sprites.push_back(bn::sprite_items::markers.create_sprite(
                    pixel_at(npc.tile_x), pixel_at(npc.tile_y), npc.graphic));
                _npc_sprites.back().set_camera(_camera);
            }
        }
    }

    void WorldState::update_movement(const Input& input)
    {
        int x = _player_x, y = _player_y;
        if(input.left_held) { --x; _facing = Direction::left; }
        else if(input.right_held) { ++x; _facing = Direction::right; }
        else if(input.up_held) { --y; _facing = Direction::up; }
        else if(input.down_held) { ++y; _facing = Direction::down; }
        if((x != _player_x || y != _player_y) && can_occupy(x, y))
        {
            _player_x = x; _player_y = y; _player.set_position(x, y); _walk_frame = (_walk_frame + 1) % 24;
        }
        else if(x == _player_x && y == _player_y) _walk_frame = 0;
        _player.set_tiles(bn::sprite_items::markers.tiles_item(), static_cast<int>(_facing) * 3 + _walk_frame / 8);
        _camera.set_position(bn::clamp(_player_x, -8, 8), bn::clamp(_player_y, -48, 48));
    }

    bool WorldState::can_occupy(int x, int y) const
    {
        const int left = tile_at(x - player_radius), right = tile_at(x + player_radius);
        const int top = tile_at(y - player_radius), bottom = tile_at(y + player_radius);
        if(! generated::walkable(_map_id, left, top) || ! generated::walkable(_map_id, right, top) ||
           ! generated::walkable(_map_id, left, bottom) || ! generated::walkable(_map_id, right, bottom)) return false;
        for(const story::Npc& npc : story::npcs)
            if(npc.map_id == _map_id && tile_at(x) == npc.tile_x && tile_at(y) == npc.tile_y) return false;
        return true;
    }

    void WorldState::interact()
    {
        int x = tile_at(_player_x), y = tile_at(_player_y);
        if(_facing == Direction::left) --x; else if(_facing == Direction::right) ++x;
        else if(_facing == Direction::up) --y; else ++y;
        for(const story::Npc& npc : story::npcs)
        {
            if(npc.map_id == _map_id && npc.tile_x == x && npc.tile_y == y)
            {
                _audio.play_interaction(); open_dialogue(npc.dialogue); return;
            }
        }
    }

    void WorldState::open_dialogue(std::uint8_t id)
    {
        _dialogue = id; _page = 0; _ui_mode = UiMode::dialogue; show_page();
    }

    void WorldState::show_page()
    {
        _ui_text.clear(); _ui_panels.clear();
        for(int index = 0; index < 4; ++index) _ui_panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96 + index * 64, 48));
        for(int line = 0; line < 3; ++line) render_text(story::dialogue[_dialogue][_page][line], 0, 28 + line * 16, _ui_text);
    }

    void WorldState::advance_dialogue()
    {
        if(++_page < story::page_counts[_dialogue]) { show_page(); return; }
        if(_dialogue == 3 && ! _candy_spoken)
        {
            _candy_spoken = true; persist(); _ui_mode = UiMode::objective; _ui_text.clear();
            render_text("OBJECTIVE", 0, 30, _ui_text); render_text("MEET CANDY AT", 0, 47, _ui_text); render_text("THE OLD ROAD", 0, 64, _ui_text); return;
        }
        if(_dialogue == 4)
        {
            _demo_complete = true; persist(); _ui_mode = UiMode::finale; _ui_text.clear();
            render_text("CROWN & CHAOS", 0, 35, _ui_text); render_text("TO BE CONTINUED", 0, 57, _ui_text); return;
        }
        close_ui();
    }

    void WorldState::open_menu()
    {
        _ui_mode = UiMode::menu; _ui_text.clear(); _ui_panels.clear();
        for(int index = 0; index < 4; ++index) _ui_panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96 + index * 64, 0));
        render_text("JOHN", 0, -20, _ui_text);
        render_text(_map_id == 0 ? "BEDROOM" : _map_id == 1 ? "JOHNS HOUSE" : _map_id == 2 ? "CROWNHAVEN" : "OLD ROAD", 0, 0, _ui_text);
        render_text(_candy_spoken ? "OLD ROAD OBJECTIVE" : "EXPLORE CROWNHAVEN", 0, 20, _ui_text);
        persist();
    }

    void WorldState::close_ui() { _ui_text.clear(); _ui_panels.clear(); _ui_mode = UiMode::none; }

    void WorldState::transition_if_needed()
    {
        const int x = tile_at(_player_x), y = tile_at(_player_y);
        if(_map_id == 0 && x == 16 && y == 27) load_map(1, pixel_at(16), pixel_at(10));
        else if(_map_id == 1 && x == 16 && y == 9) load_map(0, pixel_at(16), pixel_at(25));
        else if(_map_id == 1 && x == 16 && y == 27) load_map(2, pixel_at(8), pixel_at(14));
        else if(_map_id == 2 && x == 8 && y == 12) load_map(1, pixel_at(16), pixel_at(25));
        else if(_map_id == 2 && x == 30 && y == 18 && _candy_spoken) load_map(3, pixel_at(2), pixel_at(18));
        else if(_map_id == 3 && x == 1 && y == 18) load_map(2, pixel_at(29), pixel_at(18));
    }

    void WorldState::trigger_road_scene()
    {
        if(_map_id == 3 && ! _demo_complete && tile_at(_player_x) >= 24)
        {
            _shake_frames = 24;
        }
    }

    void WorldState::persist()
    {
        _save.save_world(_map_id, _player_x, _player_y, static_cast<std::uint8_t>(_facing), _candy_spoken, _demo_complete);
    }
}
