def get_example_return_value_mappings(function_name: str, module_name: str):
    match(module_name, function_name):
        case ('KeyboardBinder', 'inject_into_process'): return [ 'injection_successful' ]
        case ('KeyboardBinder', 'connect_to_application'): return [ 'connection_successful' ]
        case ('KeyboardBinder', 'is_connected_to_application'): return [ 'is_connected' ]
        case ('KeyboardBinder', 'is_console_enabled'): return [ 'visible' ]
        case ('KeyboardBinder', 'get_active_profiles'): return [ 'active_profile_names' ]
        case ('Desktop', 'get_selected_file_paths_in_file_browser'): return [ 'file_paths' ]
        case ('Desktop', 'get_master_volume_level'): return [ 'volume_level' ]
        case ('Desktop', 'get_process_volume_level'): return [ 'volume_level' ]
        case ('Desktop', 'get_clipboard_text'): return [ 'clipboard_text' ]
        case ('Mouse', 'get_cursor_location'): return [ 'x', 'y' ]
        case ('Keyboard', 'is_modifier_key_down'): return [ 'is_down' ]
        case ('PremierePro', 'list_sequence_names'): return [ 'sequence_names' ]
        case ('PremierePro', 'get_audio_gain_level_from_selection'): return [ 'gain_level' ]
        case ('PremierePro', 'get_media_paths_from_selection'): return [ 'media_paths' ]
        case ('PremierePro', 'get_scale_to_frame_size_from_selection'): return [ 'scale_enabled' ]
        case ('PremierePro', 'get_speed_from_selection'): return [ 'speed' ]
        case ('PremierePro', 'is_track_targeted'): return [ 'is_targeted' ]
        case ('Gimp', 'create_new_image'): return [ 'image' ]
        case ('Gimp', 'load_image'): return [ 'image' ]
        case ('Gimp', 'create_new_layer'): return [ 'layer' ]
        case ('Gimp', 'get_active_layer'): return [ 'layer' ]
        case ('Gimp', 'get_image_size'): return [ 'width', 'height' ]
        case ('Gimp', 'list_displayed_images'): return [ 'images' ]
        case ('OBS', 'get_current_scene_name'): return [ 'scene_name' ]
        case ('OBS', 'get_is_input_muted'): return [ 'is_muted' ]
        case ('OBS', 'get_input_volume'): return [ 'volume' ]
        case ('VLC', 'get_playlist_items'): return [ 'item_paths' ]
        case ('VLC', 'get_player_position'): return [ 'position_seconds' ]
        case ('VLC', 'get_player_volume'): return [ 'volume_level' ]
        case ('VLC', 'is_player_paused'): return [ 'is_player_paused' ]
        case ('VLC', 'is_player_playing'): return [ 'is_player_playing' ]
        case ('VLC', 'is_player_stopped'): return [ 'is_player_stopped' ]
        case ('Youtube', 'get_player_position'): return [ 'position_seconds' ]
        case ('Youtube', 'get_player_volume'): return [ 'volume_level' ]
        case _: return []

def get_example_arg_mappings(function_name: str, module_name: str, overload_name: str):
    match(module_name, function_name, overload_name):
        case ('KeyboardBinder', 'inject_into_process', _): return { 'process_name': 'notepad++.exe', 'block_keyboard_input': True, 'on_process_exit': 'lambda result: print(\'Process exited!\')' }
        case ('KeyboardBinder', 'connect_to_application', _): return { 'app_name': 'Premiere Pro' }
        case ('KeyboardBinder', 'disconnect_from_application', _): return { 'app_name': 'Premiere Pro' }
        case ('KeyboardBinder', 'is_connected_to_application', _): return { 'app_name': 'Premiere Pro' }
        case ('KeyboardBinder', 'set_console_visible', _): return { 'visible': True }
        case ('KeyboardBinder', 'start_interaction_recorder', _): return { 'result_consumer': 'lambda result: print(\'Use result here\')' }
        case ('KeyboardBinder', 'wait', _): return { 'seconds': 3.5 }
        case ('Desktop', 'set_clipboard_text', _): return { 'text': 'epic text' }
        case ('Desktop', 'exec_command', _): return { 'command': 'explorer https://google.com' }
        case ('Desktop', 'get_process_volume_level', _): return { 'process_name': 'ts3client_win64.exe' }
        case ('Desktop', 'set_master_volume_level', _): return { 'value': 50 }
        case ('Desktop', 'set_process_volume_level', _): return { 'value': 50, 'process_name': 'ts3client_win64.exe' }
        case ('Desktop', 'move_file_to_trash', _): return { 'file_path': 'pic_of_ex.png' }
        case ('Keyboard', 'hold_modifier_key' | 'release_modifier_key' | 'is_modifier_key_down', _): return { 'modifiers': 1 }
        case ('Keyboard', 'type', _): return { 'text': 'hi team' }
        case ('Keyboard', 'while_holding_modifier_key', _): return { 'modifiers': 2, 'action': 'lambda: Keyboard.type(\'S\')' }
        case ('Mouse', 'click', _): return { 'button': 1024 }
        case ('Mouse', 'hold', _): return { 'button': 4096 }
        case ('Mouse', 'set_cursor_location', _): return { 'x': 50, 'y': 50 }
        case ('Mouse', 'release', _): return { 'button': 4096 }
        case ('OBS', 'add_event_listener', 'ExitStarted'): return { 'event': 'ExitStarted', 'on_exit': 'lambda: print(\'We closin\')' }
        case ('OBS', 'add_event_listener', 'CurrentProgramSceneChanged'): return { 'event': 'CurrentProgramSceneChanged', 'on_change': 'lambda scene_name: print(\'Scene name changed\')' }
        case ('OBS', 'get_input_volume', _): return { 'input_name': 'intro-song' }
        case ('OBS', 'get_is_input_muted', _): return { 'input_name': 'outro-song' }
        case ('OBS', 'pause_media_input', _): return { 'media_input_name': 'outro-music' }
        case ('OBS', 'play_media_input', _): return { 'media_input_name': 'outro-music' }
        case ('OBS', 'restart_media_input', _): return { 'media_input_name': 'outro-music' }
        case ('OBS', 'set_current_scene', _): return { 'scene_name': 'intro_scene' }
        case ('OBS', 'set_current_scene_transition', _): return { 'transition_name': 'epic-transition' }
        case ('OBS', 'set_input_volume', _): return { 'input_name': 'intro-song', 'volume': 12 }
        case ('OBS', 'stop_media_input', _): return { 'media_input_name': 'outro-music' }
        case ('OBS', 'set_input_is_muted', _): return { 'input_name': 'epic-frag-song', 'muted': False }
        case ('PremierePro', 'apply_audio_preset_to_selection', _): return { 'preset_path': 'Presets/CoolAudio' }
        case ('PremierePro', 'apply_video_preset_to_selection', _): return { 'preset_path': 'Presets/CoolVideo' }
        case ('PremierePro', 'adjust_audio_gain_level_on_selection' | 'set_audio_gain_level_on_selection', _): return { 'level': 5 }
        case ('PremierePro', 'set_scale_to_frame_size_on_selection', _): return { 'enabled': True }
        case ('PremierePro', 'set_speed_on_selection', _): return { 'value': 42 }
        case ('PremierePro', 'is_track_targeted', _): return { 'track_name': 'Video 1' }
        case ('PremierePro', 'set_track_targeted', _): return { 'track_name': 'Video 1', 'targeted': True }
        case ('PremierePro', 'add_audio_effect_to_selection', _): return { 'effect_name': 'Unknown', 'properties': '{}' }
        case ('PremierePro', 'add_video_effect_to_selection', 'Sharpen'): return { 'effect_name': 'Sharpen', 'properties': '{}' }
        case ('PremierePro', 'add_video_effect_to_selection', _): return { 'effect_name': 'Unknown', 'properties': '{}' }
        case ('PremierePro', 'insert_item_at_player_position', _): return { 'item_path': 'Bin1/Bin2/ClipOrSequenceName' }
        case ('Gimp', 'create_new_image', _): return { 'width': 128, 'height': 128 }
        case ('Gimp', 'load_image', _): return { 'path': 'cute_cat.jpg' }
        case ('Gimp', 'create_new_layer', _): return { 'name': 'layer1', 'width': 128, 'height': 128, 'opacity': 50, 'image': '$image$' }
        case ('Gimp', 'display_image', _): return { 'image': '$image$' }
        case ('Gimp', 'insert_layer', _): return { 'layer': '$layer$', 'image': '$image$' }
        case ('Gimp', 'get_active_layer', _): return { 'image': '$image$' }
        case ('Gimp', 'get_image_size', _): return { 'image': '$image$' }
        case ('Gimp', 'apply_brightness_contrast_filter', _): return { 'brightness': 0.5, 'contrast': 0.25, 'layer': '$layer$' }
        case ('Twitch', 'create_clip', _): return { 'channel_name': 'shroud' }
        case ('VLC', 'add_item_to_playlist', _): return { 'file_path': 'C:/Users/User/Desktop/In Flames/Subterranean/Stand Ablaze.mp3' }
        case ('VLC', 'set_player_position', _): return { 'position_seconds': 69 }
        case ('VLC', 'set_player_volume', _): return { 'volume_level': 25 }
        case ('Youtube', 'load_video_by_id', _): return { 'id': 'dQw4w9WgXcQ' }
        case ('Youtube', 'set_player_position', _): return { 'position_seconds': 69 }
        case ('Youtube', 'set_player_volume', _): return { 'volume_level': 42 }
        case _: return {}

def get_lambda_parameter_names(module_name: str, function_name: str, arg_name: str):
    match (module_name, function_name, arg_name):
        case ('KeyboardBinder', 'start_interaction_recorder', 'result_consumer'): return [ 'recording_result' ]
        case ('OBS', 'add_event_listener', 'on_change'): return [ 'new_scene_name' ]
        case _: return []