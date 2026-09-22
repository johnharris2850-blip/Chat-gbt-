#include "world_state.h"

#include "bn_algorithm.h"
#include "bn_regular_bg_items_bedroom.h"
#include "bn_regular_bg_items_house.h"
#include "bn_regular_bg_items_crownhaven.h"
#include "bn_regular_bg_items_old_road.h"
#include "bn_sprite_items_markers.h"
#include "bn_sprite_items_ui_panel.h"
#include "generated/world_data.h"
#include "npc.h"

namespace
{
    constexpr int map_half_size = 128;
    constexpr int player_radius = 3;
    constexpr crown::Npc npcs[] =
    {
        { 2, 16, 15, 12, 0, false }, { 2, 21, 19, 13, 1, false },
        { 2, 8, 20, 14, 2, false }, { 2, 27, 18, 15, 3, false },
        { 3, 26, 18, 15, 4, true }
    };

    [[nodiscard]] int tile_at(int pixel) { return (pixel + map_half_size) / 8; }
    [[nodiscard]] int pixel_at(int tile) { return tile * 8 - 124; }

    [[nodiscard]] bn::regular_bg_ptr create_background(std::uint8_t map_id)
    {
        switch(map_id)
        {
        case 0: return bn::regular_bg_items::bedroom.create_bg(0, 0);
        case 1: return bn::regular_bg_items::house.create_bg(0, 0);
        case 2: return bn::regular_bg_items::crownhaven.create_bg(0, 0);
        default: return bn::regular_bg_items::old_road.create_bg(0, 0);
        }
    }

    void dialogue(std::uint8_t id, int page, const char* const*& lines, int& count)
    {
        switch(id)
        {
        case 0: lines = crown::generated::villager_1_dialogue[page]; count = crown::generated::villager_1_page_count; break;
        case 1: lines = crown::generated::villager_2_dialogue[page]; count = crown::generated::villager_2_page_count; break;
        case 2: lines = crown::generated::villager_3_dialogue[page]; count = crown::generated::villager_3_page_count; break;
        case 3: lines = crown::generated::candy_dialogue[page]; count = crown::generated::candy_page_count; break;
        default: lines = crown::generated::finale_dialogue[page]; count = crown::generated::finale_page_count; break;
        }
    }
}

namespace crown
{
    WorldState::WorldState(SaveService& save_service, AudioService& audio_service) :
        _save_service(save_service), _audio_service(audio_service), _camera(bn::camera_ptr::create(0, 0)),
        _background(create_background(0)), _player(bn::sprite_items::markers.create_sprite(0, 0, 0))
    {
        const SaveData& save = save_service.data();
        _candy_spoken_to = save.candy_spoken_to;
        _finale_seen = save.finale_seen;
        _facing = static_cast<Direction>(save.facing < 4 ? save.facing : 0);
        const std::uint8_t map = save.map_id < generated::map_count ? save.map_id : 0;
        load_map(map, save.player_x, save.player_y);
    }

    void WorldState::update(const Input& input)
    {
        if(_shake_frames > 0)
        {
            --_shake_frames;
            _camera.set_position(bn::clamp(_player_x, -8, 8) + ((_shake_frames & 2) ? 2 : -2), bn::clamp(_player_y, -48, 48));
            if(_shake_frames == 0) show_dialogue_page();
            return;
        }
        if(_ui_mode != UiMode::none)
        {
            if(input.cancel_pressed && _ui_mode == UiMode::start_menu) close_ui();
            else if(input.action_pressed) advance_dialogue();
            return;
        }
        if(input.start_pressed) { open_start_menu(); return; }
        if(input.action_pressed) { try_interaction(); return; }
        update_movement(input);
        check_transition();
        check_finale();
    }

    void WorldState::load_map(std::uint8_t map_id, int x, int y)
    {
        _map_id = map_id; _player_x = x; _player_y = y;
        _background = create_background(map_id); _background.set_camera(_camera);
        _player.set_camera(_camera); _player.set_position(x, y);
        spawn_npcs();
        _camera.set_position(bn::clamp(x, -8, 8), bn::clamp(y, -48, 48));
        persist();
    }

    void WorldState::spawn_npcs()
    {
        _npcs.clear();
        for(const Npc& npc : npcs)
        {
            if(npc.map_id == _map_id && (! npc.requires_objective || _candy_spoken_to))
            {
                _npcs.push_back(bn::sprite_items::markers.create_sprite(pixel_at(npc.tile_x), pixel_at(npc.tile_y), npc.sprite_index));
                _npcs.back().set_camera(_camera);
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
        const bool moved = x != _player_x || y != _player_y;
        if(moved && can_occupy(x,y)) { _player_x=x; _player_y=y; _player.set_position(x,y); _walk_frame=(_walk_frame+1)%24; }
        else if(! moved) _walk_frame=0;
        _player.set_tiles(bn::sprite_items::markers.tiles_item(), static_cast<int>(_facing)*3 + _walk_frame/8);
        _camera.set_position(bn::clamp(_player_x,-8,8), bn::clamp(_player_y,-48,48));
    }

    bool WorldState::can_occupy(int x, int y) const
    {
        if(! generated::walkable(_map_id,tile_at(x-player_radius),tile_at(y-player_radius)) ||
           ! generated::walkable(_map_id,tile_at(x+player_radius),tile_at(y-player_radius)) ||
           ! generated::walkable(_map_id,tile_at(x-player_radius),tile_at(y+player_radius)) ||
           ! generated::walkable(_map_id,tile_at(x+player_radius),tile_at(y+player_radius))) return false;
        for(const Npc& npc : npcs)
            if(npc.map_id == _map_id && (!npc.requires_objective || _candy_spoken_to) && tile_at(x)==npc.tile_x && tile_at(y)==npc.tile_y) return false;
        return true;
    }

    void WorldState::try_interaction()
    {
        int x=tile_at(_player_x), y=tile_at(_player_y);
        if(_facing==Direction::left) --x; else if(_facing==Direction::right) ++x; else if(_facing==Direction::up) --y; else ++y;
        for(const Npc& npc : npcs)
            if(npc.map_id==_map_id && x==npc.tile_x && y==npc.tile_y && (!npc.requires_objective || _candy_spoken_to)) { begin_dialogue(npc.dialogue_id); return; }
    }

    void WorldState::begin_dialogue(std::uint8_t id)
    {
        _dialogue_id=id; _dialogue_page=0; _ui_mode=UiMode::dialogue; _audio_service.play_interaction(); show_dialogue_page();
    }

    void WorldState::advance_dialogue()
    {
        const char* const* unused=nullptr; int count=0; dialogue(_dialogue_id,_dialogue_page,unused,count);
        if(_dialogue_page+1<count)
        {
            ++_dialogue_page;
            if(_dialogue_id==4 && _dialogue_page==2) { _shake_frames=32; _ui_sprites.clear(); }
            else show_dialogue_page();
        }
        else
        {
            if(_dialogue_id==3) { _candy_spoken_to=true; spawn_npcs(); }
            if(_dialogue_id==4) _finale_seen=true;
            close_ui(); persist();
        }
    }

    void WorldState::show_dialogue_page()
    {
        _ui_sprites.clear(); _ui_panels.clear();
        for(int i=0;i<4;++i) _ui_panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96+i*64,48));
        const char* const* lines=nullptr; int count=0; dialogue(_dialogue_id,_dialogue_page,lines,count);
        for(int line=0;line<3;++line) render_text(lines[line],0,30+line*15,_ui_sprites);
    }

    void WorldState::open_start_menu()
    {
        _ui_mode=UiMode::start_menu; _ui_panels.clear();
        for(int i=0;i<4;++i) _ui_panels.push_back(bn::sprite_items::ui_panel.create_sprite(-96+i*64,0));
        constexpr const char* names[]={"JOHNS BEDROOM","JOHNS HOUSE","CROWNHAVEN","OLD ROAD"};
        render_text("JOHN",0,-20,_ui_sprites); render_text(names[_map_id],0,0,_ui_sprites);
        render_text(_candy_spoken_to ? "OLD ROAD OBJECTIVE" : "EXPLORE CROWNHAVEN",0,20,_ui_sprites); persist();
    }
    void WorldState::close_ui() { _ui_sprites.clear(); _ui_panels.clear(); _ui_mode=UiMode::none; }

    void WorldState::check_transition()
    {
        const int x=tile_at(_player_x), y=tile_at(_player_y);
        if(_map_id==0 && x==16 && y==27) load_map(1,pixel_at(16),pixel_at(8));
        else if(_map_id==1 && x==16 && y==28) load_map(2,pixel_at(12),pixel_at(17));
        else if(_map_id==2 && x==30 && y==18 && _candy_spoken_to) load_map(3,pixel_at(2),pixel_at(18));
        else if(_map_id==3 && x==1 && y==18) load_map(2,pixel_at(29),pixel_at(18));
    }

    void WorldState::check_finale()
    {
        if(_map_id==3 && _candy_spoken_to && !_finale_seen && tile_at(_player_x)>=23) begin_dialogue(4);
    }

    void WorldState::persist()
    {
        _save_service.save_world(_map_id,_player_x,_player_y,static_cast<std::uint8_t>(_facing),_candy_spoken_to,_finale_seen);
    }
}
