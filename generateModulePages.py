import ast
from os import listdir
from typing import Any

def get_example_arg_mappings(function_name: str, module_name: str):
    if module_name == 'Common':
        return { 'text': 'epic text' } if function_name == 'copy_text_to_clipboard' else \
               { 'command': 'explorer https://google.com' } if function_name == 'exec_command' else \
               { 'seconds': 3.5 } if function_name == 'wait' else {}
    elif module_name == 'Keyboard':
        return { 'modifier_key': 16 } if function_name in [ 'hold_modifier_key', 'release_modifier_key' ] else \
               { 'text': 'hi team' } if function_name == 'type' else {}
    elif module_name == 'Mouse':
        return { 'button': 1024 } if function_name == 'click' else \
               { 'x': 50, 'y': 50 } if function_name == 'move_cursor_to' else {}
    elif module_name == 'OBS':
        return { 'source_name': 'background-music' } if function_name in [ 'restart_media_source', 'stop_media_source', 'toggle_media_source_pause', 'toggle_source_mute' ] else \
               { 'source_name': 'outro-music', 'paused': True } if function_name == 'set_media_source_paused' else \
               { 'source_name': 'epic-frag-song', 'muted': False } if function_name == 'set_source_muted' else \
               { 'listener': "lambda: print('OBS exit!')" } if function_name == 'add_on_exit_listener' else {}
    elif module_name == 'PremierePro':
        return { 'level': 5 } if function_name == 'adjust_gain_level_by' else {}
    elif module_name == 'Twitch':
        return { 'channel_name': 'shroud' } if function_name == 'create_clip' else {}
    else:
        return {}

def get_example_arg_key_value(arg_name: str, example_arg_value_mappings: dict[str, Any]):
    arg_value = example_arg_value_mappings.get(arg_name, 'MISSING_ARG_VALUE')
    arg_value_type = type(arg_value)
    is_lambda_type = arg_value_type == str and arg_value.startswith('lambda')
    value_css_class = 'integer-param' if arg_value_type in [ int, float ] else   \
                      'enum-param' if arg_value_type == list else     \
                      'boolean-param' if arg_value_type == bool else  \
                      'enum-param' if is_lambda_type else \
                      'string-param'

    formatted_arg_value = f"'{arg_value}'" if arg_value_type == str and not is_lambda_type else arg_value

    return f'{arg_name} = <span class = "{value_css_class}">{formatted_arg_value}</span>'

def get_function_call_example(function: ast.FunctionDef, module_name: str):
    function_name = function.name
    example_arg_value_mappings = get_example_arg_mappings(function_name, module_name)
    example_args_list = ', '.join(get_example_arg_key_value(k.arg, example_arg_value_mappings) for k in function.args.args)

    return f'{module_name}.{function_name}({example_args_list})'

def get_function_return_type(function: ast.FunctionDef):
    function_return = function.returns

    if function_return == None:
        return 'MISSING_RETURN_TYPE'
    elif isinstance(function_return, ast.Constant):
        return function_return.value
    elif isinstance(function_return, ast.Subscript):
        return_type_name = function_return.value.id # type: ignore

        if return_type_name == '__Tuple':
            tuple_elements: list[ast.Name] = function_return.slice.elts  # type: ignore

            return f'({", ".join(k.id for k in tuple_elements)})'
        else:
            return 'UNKNOWN_COMPLEX_RETURN_TYPE'
    else:
        return 'UNKNOWN_RETURN_TYPE'

def get_function_arg_description(arg: ast.arg):
    arg_name = arg.arg
    arg_annotation = arg.annotation

    if isinstance(arg_annotation, ast.Name):
        return f'{arg_name}: {arg_annotation.id}'
    elif isinstance(arg_annotation, ast.Subscript):
        arg_type_params = arg_annotation.slice

        if isinstance(arg_type_params, ast.Constant):
            return f'{arg_name}: {arg_type_params.value}'
        elif isinstance(arg_type_params, ast.Tuple):
            type_params = arg_type_params.elts

            if isinstance(type_params[0], ast.List):
                function_arg_types: list[ast.Constant] = type_params[0].elts  # type: ignore
                function_return_type: ast.Constant = type_params[1]  # type: ignore

                return f'{arg_name}: ({", ".join(k.value for k in function_arg_types)}) -> {function_return_type.value}'
            else:
                union_values: list[ast.Constant] = type_params  # type: ignore

                return f'{arg_name}: {" | ".join(str(k.value) for k in union_values)}'
        else:
            return 'UNKNOWN_COMPLEX_ARG_TYPE'
    else:
        return 'UNKNOWN_ARG_TYPE'


def get_function_description(function: ast.FunctionDef, module_name: str):
    return f'<h2>{function.name}({", ".join(get_function_arg_description(k) for k in function.args.args)}) -> {get_function_return_type(function)}</h2>' + \
           f'<h4>Description:</h4><p>{ast.get_docstring(function) or "MISSING_FUNCTION_DESCRIPTION"}' + \
           f'</p><h4>Example:</h4><p class = "code-example">{get_function_call_example(function, module_name)}</p>'

def get_constant_description(constant: ast.Assign):
    constant_name: ast.Name = constant.targets[0]  # type: ignore
    constant_value: ast.Constant = constant.value  # type: ignore

    return f'<h2>{constant_name.id} = {constant_value.value}</h2>'


MODULES_DIR = '../KeyboardBinder/modules/keyboardBinder'
MODULE_FILES = (k for k in listdir(MODULES_DIR) if not k.startswith('_'))

for module_file in MODULE_FILES:
    module_name = module_file[0 : module_file.rindex(".")]

    with open(f'{MODULES_DIR}/{module_file}', 'r') as input_file, open(f'docs/pages/modules/{module_name.lower()}.html', 'w') as output_file:
        module_node = ast.parse(input_file.read())
        module_child_nodes = list(ast.iter_child_nodes(module_node))

        constant_defs = ( k for k in module_child_nodes if isinstance(k, ast.Assign) )
        function_defs = [ k for k in module_child_nodes if isinstance(k, ast.FunctionDef) ]
        function_defs.sort(key = lambda k: k.name)

        header = f'<h1>{module_name}</h1><p>{ast.get_docstring(module_node)}</p><br>'
        function_descriptions = ( get_function_description(k, module_name) for k in function_defs )
        constant_descriptions = [ get_constant_description(k) for k in constant_defs if not k.targets[0].id.startswith('__') ]  # type: ignore

        output_file.write(header + '<hr>'.join(constant_descriptions) + ('<br>' if len(constant_descriptions) > 0 else '') + '<hr>'.join(function_descriptions))