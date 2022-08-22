import ast
from os import listdir
from typing import Any

def get_example_return_value_mappings(function_name: str, module_name: str):
    match(module_name, function_name):
        case ('Mouse', 'get_cursor_location'): return [ 'x', 'y' ]
        case _: return []

def get_example_arg_mappings(function_name: str, module_name: str):
    match(module_name, function_name):
        case ('Common', 'copy_text_to_clipboard'): return { 'text': 'epic text' }
        case ('Common', 'exec_command'): return { 'command': 'explorer https://google.com' }
        case ('Common', 'wait'): return { 'seconds': 3.5 }
        case ('Keyboard', 'hold_modifier_key' | 'release_modifier_key'): return { 'modifier_key': 16 }
        case ('Keyboard', 'type'): return { 'text': 'hi team' }
        case ('Mouse', 'click'): return { 'button': 1024 }
        case ('Mouse', 'hold'): return { 'button': 4096 }
        case ('Mouse', 'release'): return { 'button': 4096 }
        case ('Mouse', 'move_cursor_to'): return { 'x': 50, 'y': 50 }
        case ('OBS', 'restart_media_source' | 'stop_media_source' | 'toggle_media_source_pause' | 'toggle_source_mute'): return { 'source_name': 'background-music' }
        case ('OBS', 'set_media_source_paused'): return { 'source_name': 'outro-music', 'paused': True }
        case ('OBS', 'set_source_muted'): return { 'source_name': 'epic-frag-song', 'muted': False }
        case ('OBS', 'add_on_exit_listener'): return { 'listener': "lambda: print('OBS exit!')" }
        case ('PremierePro', 'adjust_gain_level_by'): return { 'level': 5 }
        case ('Twitch', 'create_clip'): return { 'channel_name': 'shroud' }
        case _: return {}

def get_optional_named_parameter_value(value: Any, module_name: str, constant_value_to_names: dict[Any, str]):
    optional_constant_name = constant_value_to_names.get(value, None)

    return f'{module_name}.{optional_constant_name}' if not optional_constant_name == None else str(value)

def get_example_arg_key_value(arg_name: str, module_name: str, example_arg_value_mappings: dict[str, Any], constant_value_to_names: dict[Any, str]):
    arg_value = example_arg_value_mappings.get(arg_name, 'MISSING_ARG_VALUE')
    arg_value_type = type(arg_value)
    value_color_css_var = 'number-literal' if arg_value_type in [ int, float ] else   \
                          'boolean-literal' if arg_value_type == bool else  \
                          'string-literal'

    is_lambda_type = arg_value_type == str and arg_value.startswith('lambda')
    formatted_arg_value = f"'{arg_value}'" if arg_value_type == str and not is_lambda_type else get_optional_named_parameter_value(arg_value, module_name, constant_value_to_names)
    is_named_constant = formatted_arg_value.startswith(module_name) and not is_lambda_type

    return f'{arg_name} = <span style = "color: var(--module-name-color)">{module_name}</span>.<span style = "color: var(--constant-literal-color)">{formatted_arg_value[formatted_arg_value.index(".") + 1 : ]}</span>' if is_named_constant else \
           f'{arg_name} = <span style = "color: var(--{value_color_css_var}-color)">{formatted_arg_value}</span>' if not is_lambda_type else \
           f'{arg_name} = ' + formatted_arg_value.replace('lambda', '<span style = "color: var(--boolean-literal-color)">lambda</span>')

def get_function_call_example(function: ast.FunctionDef, module_name: str, constant_value_to_names: dict[Any, str]):
    function_name = function.name
    return_value_mappings = get_example_return_value_mappings(function_name, module_name)
    arg_value_mappings = get_example_arg_mappings(function_name, module_name)
    args_list = (get_example_arg_key_value(k.arg, module_name, arg_value_mappings, constant_value_to_names) for k in function.args.args)

    return f'{", ".join(return_value_mappings)}{" = " if len(return_value_mappings) > 0 else ""}' + \
           f'<span style = "color: var(--module-name-color)">{module_name}</span>.' + \
           f'<span style = "color: var(--function-name-color)">{function_name}</span>' + \
           f'({", ".join(args_list)})'

def get_function_return_type(function: ast.FunctionDef):
    match function.returns:
        case None: return 'MISSING_RETURN_TYPE'
        case ast.Constant(value): return value
        case ast.Name(value): return value
        case _: return 'UNKNOWN_RETURN_TYPE'


def get_function_arg_description(arg: ast.arg, module_name: str, constant_value_to_names: dict[Any, str]):
    arg_name = arg.arg

    match arg.annotation:
        case ast.Name(id): return f'{arg_name}: {id}'
        case ast.Subscript(_, ast.Constant(value)): return f'{arg_name}: {get_optional_named_parameter_value(value, module_name, constant_value_to_names)}'
        case ast.Subscript(_, ast.Tuple(type_params)):
            if isinstance(type_params[0], ast.List):
                function_arg_types: list[ast.Constant] = type_params[0].elts  # type: ignore
                function_return_type: ast.Constant = type_params[1]  # type: ignore

                return f'{arg_name}: ({", ".join(k.value for k in function_arg_types)}) -> {function_return_type.value}'
            else:
                union_values: list[ast.Constant] = type_params  # type: ignore

                return f'{arg_name}: {" | ".join(get_optional_named_parameter_value(k.value, module_name, constant_value_to_names) for k in union_values)}'
        case _: return 'UNKNOWN_ARG_TYPE'


def get_function_description(function: ast.FunctionDef, module_name: str, constant_value_to_names: dict[Any, str]):
    return f'<h3 id = "{function.name}" style = "cursor: pointer" onclick = "onAnchorClick(\'{function.name}\')" >{function.name}({", ".join(get_function_arg_description(k, module_name, constant_value_to_names) for k in function.args.args)}) -> {get_function_return_type(function)}</h3>' + \
           f'<h4>Description:</h4><p>{ast.get_docstring(function) or "MISSING_FUNCTION_DESCRIPTION"}' + \
           f'</p><h4>Example:</h4><p class = "code-example">{get_function_call_example(function, module_name, constant_value_to_names)}</p>'

def get_constant_info(constant: ast.Assign):
    constant_name: ast.Name = constant.targets[0]  # type: ignore
    constant_value: ast.Constant = constant.value  # type: ignore

    return (constant_value.value, str(constant_name.id))


MODULES_DIR = '../KeyboardBinder/app/modules/keyboardBinder'
MODULE_FILES = (k for k in listdir(MODULES_DIR) if not k.startswith('_'))

for module_file in MODULE_FILES:
    module_name = module_file[0 : module_file.rindex(".")]

    with open(f'{MODULES_DIR}/{module_file}', 'r') as input_file, open(f'docs/pages/modules/{module_name.lower()}.html', 'w') as output_file:
        module_node = ast.parse(input_file.read())
        module_child_nodes = list(ast.iter_child_nodes(module_node))

        constant_defs = ( k for k in module_child_nodes if isinstance(k, ast.Assign) )
        function_defs = [ k for k in module_child_nodes if isinstance(k, ast.FunctionDef) ]
        function_defs.sort(key = lambda k: k.name)

        constant_value_to_names = dict(get_constant_info(k) for k in constant_defs if not k.targets[0].id.startswith('__'))  # type: ignore

        module_name_header = f'<h1>{module_name}</h1><p>{ast.get_docstring(module_node)}</p><br>'
        constant_descriptions = [ f'<h3>{k[1]} = {k[0]}</h3>' for k in constant_value_to_names.items() ]
        constants_header = '<h2>Constants</h2><hr>' if len(constant_descriptions) > 0 else ''
        function_descriptions = [ get_function_description(k, module_name, constant_value_to_names) for k in function_defs ]
        functions_header = '<h2>Functions</h2><hr>' if len(function_descriptions) > 0 else ''

        output_file.write(module_name_header + constants_header + '<hr>'.join(constant_descriptions) + ('<br>' if len(constant_descriptions) > 0 else '') +
                          functions_header + '<hr>'.join(function_descriptions))