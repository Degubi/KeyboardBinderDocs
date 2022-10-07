def get_example_return_value_mappings(function_name: str, module_name: str):
    match(module_name, function_name):
        case ('Application', 'is_debug_console_enabled'): return [ 'visible' ]
        case ('Mouse', 'get_cursor_location'): return [ 'x', 'y' ]
        case ('PremierePro', 'list_sequence_names'): return [ 'sequence_names' ]
        case ('PremierePro', 'get_audio_gain_level_from_selection'): return [ 'gain_level' ]
        case ('PremierePro', 'get_selected_clip_media_paths'): return [ 'media_paths' ]
        case ('PremierePro', 'get_scale_to_frame_size_from_selection'): return [ 'scale_enabled' ]
        case ('Keyboard', 'is_alt_key_down' | 'is_ctrl_key_down' | 'is_shift_key_down'): return [ 'is_down' ]
        case ('OBS', 'get_current_scene_name'): return [ 'scene_name' ]
        case ('OBS', 'get_is_input_muted'): return [ 'is_muted' ]
        case ('OBS', 'get_input_volume'): return [ 'volume' ]
        case _: return []

def get_example_arg_mappings(function_name: str, module_name: str, overload_name: str):
    match(module_name, function_name, overload_name):
        case ('Application', 'set_debug_console_visible', _): return { 'visible': True }
        case ('Application', 'start_interaction_recorder', _): return { 'result_consumer': 'lambda result: print(\'Use result here\')' }
        case ('Application', 'wait', _): return { 'seconds': 3.5 }
        case ('Desktop', 'copy_text_to_clipboard', _): return { 'text': 'epic text' }
        case ('Desktop', 'exec_command', _): return { 'command': 'explorer https://google.com' }
        case ('Desktop', 'move_file_to_trash', _): return { 'file_path': 'pic_of_ex.png' }
        case ('Keyboard', 'hold_modifier_key' | 'release_modifier_key', _): return { 'modifiers': 1 }
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
        case ('PremierePro', 'adjust_audio_gain_level_on_selection' | 'set_audio_gain_level_on_selection', _): return { 'level': 5 }
        case ('PremierePro', 'set_scale_to_frame_size_on_selection', _): return { 'enabled': True }
        case ('PremierePro', 'add_audio_effect_to_selection', _): return { 'effect_name': 'Bass' }
        case ('PremierePro', 'add_video_effect_to_selection', _): return { 'effect_name': 'Gamma Correction' }
        case ('PremierePro', 'insert_item_at_player_position', _): return { 'item_path': 'Bin1/Bin2/ClipOrSequenceName' }
        case ('Twitch', 'create_clip', _): return { 'channel_name': 'shroud' }
        case _: return {}

def get_lambda_parameter_names(module_name: str, function_name: str, arg_name: str):
    match (module_name, function_name, arg_name):
        case ('Application', 'start_interaction_recorder', 'result_consumer'): return [ 'recording_result' ]
        case ('OBS', 'add_event_listener', 'on_change'): return [ 'new_scene_name' ]
        case _: return []