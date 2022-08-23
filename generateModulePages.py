import builtins
import ast
from itertools import groupby
from os import listdir
from typing import Any, Callable

def get_example_return_value_mappings(function_name: str, module_name: str):
    match(module_name, function_name):
        case ('Mouse', 'get_cursor_location'): return [ 'x', 'y' ]
        case _: return []

def get_example_arg_mappings(function_name: str, module_name: str, overload_name: str):
    match(module_name, function_name, overload_name):
        case ('Common', 'copy_text_to_clipboard', _): return { 'text': 'epic text' }
        case ('Common', 'exec_command', _): return { 'command': 'explorer https://google.com' }
        case ('Common', 'wait', _): return { 'seconds': 3.5 }
        case ('Keyboard', 'hold_modifier_key' | 'release_modifier_key', _): return { 'modifier_key': 16 }
        case ('Keyboard', 'type', _): return { 'text': 'hi team' }
        case ('Mouse', 'click', _): return { 'button': 1024 }
        case ('Mouse', 'hold', _): return { 'button': 4096 }
        case ('Mouse', 'release', _): return { 'button': 4096 }
        case ('Mouse', 'move_cursor_to', _): return { 'x': 50, 'y': 50 }
        case ('OBS', 'add_event_listener', 'OBS.EVENT_OBS_EXIT'): return { 'event': 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY', 'on_exit': 'lambda: print(\'We closin\')' }
        case ('OBS', 'set_media_input_state', _): return { 'media_input_name': 'outro-music', 'state': 'OBS_WEBSOCKET_MEDIA_INPUT_ACTION_PLAY' }
        case ('OBS', 'set_input_is_muted', _): return { 'input_name': 'epic-frag-song', 'muted': False }
        case ('PremierePro', 'adjust_gain_level_by', _): return { 'level': 5 }
        case ('Twitch', 'create_clip', _): return { 'channel_name': 'shroud' }
        case _: return {}

def get_constant_info(constant: ast.Assign):
    constant_name: ast.Name = constant.targets[0]  # type: ignore
    constant_value: ast.Constant = constant.value  # type: ignore

    return (constant_value.value, str(constant_name.id))

def get_optional_named_parameter_value(value: Any, module_name: str, constant_value_to_names: dict[Any, str]):
    optional_constant_name = constant_value_to_names.get(value, None)

    return f'{module_name}.{optional_constant_name}' if not optional_constant_name == None else str(value)

def get_example_arg_key_value(arg_name: str, module_name: str, example_arg_value_mappings: dict[str, Any], constant_value_to_names: dict[Any, str]):
    arg_value = example_arg_value_mappings.get(arg_name, 'MISSING_ARG_VALUE')
    arg_value_type = type(arg_value)

    is_lambda_type = arg_value_type == str and arg_value.startswith('lambda')
    formatted_arg_value = f"'{arg_value}'" if arg_value_type == str and not is_lambda_type else get_optional_named_parameter_value(arg_value, module_name, constant_value_to_names)
    is_named_constant = arg_value in constant_value_to_names

    return f'{arg_name} = {module_name}.{constant_value_to_names[arg_value]}' if is_named_constant else \
           f'{arg_name} = {formatted_arg_value}' if not is_lambda_type else \
           f'{arg_name} = ' + formatted_arg_value

def syntax_highlight_python_function_call(code: str):
    function_call_ast: ast.Call = ast.parse(code).body[0].value  # type: ignore
    function_call_func: ast.Attribute = function_call_ast.func  # type: ignore
    function_call_module: ast.Name = function_call_func.value  # type: ignore
    function_call_args = function_call_ast.keywords
    function_call_args.reverse()

    for arg in function_call_args:
        arg_value_ast = arg.value
        before_part = code[0 : arg_value_ast.col_offset]
        after_part = code[arg_value_ast.end_col_offset : ]

        match arg_value_ast:
            case ast.Constant(builtins.bool(value)):  code = f'{before_part}<span style = "color: var(--boolean-literal-color)">{value}</span>{after_part}'
            case ast.Constant(builtins.str(value)):   code = f'{before_part}<span style = "color: var(--string-literal-color)">\'{value}\'</span>{after_part}'
            case ast.Constant(builtins.int(value)):   code = f'{before_part}<span style = "color: var(--number-literal-color)">{value}</span>{after_part}'
            case ast.Constant(builtins.float(value)): code = f'{before_part}<span style = "color: var(--number-literal-color)">{value}</span>{after_part}'
            case ast.Attribute(ast.Name(module), constant): code = f'{before_part}<span style = "color: var(--module-name-color)">{module}</span>.' + \
                                                                   f'<span style = "color: var(--constant-literal-color)">{constant}</span>{after_part}'
            case ast.Lambda(_, body): code = f'{before_part}<span style = "color: var(--boolean-literal-color)">lambda</span>: {code[body.col_offset : ]}'

    code = f'{code[0 : function_call_func.col_offset]}<span style = "color: var(--module-name-color)">{function_call_module.id}</span>.' + \
           f'<span style = "color: var(--function-name-color)">{function_call_func.attr}</span>{code[function_call_func.end_col_offset : ]}'

    return code


def get_function_call_example(function: ast.FunctionDef, module_name: str, constant_value_to_names: dict[Any, str]):
    function_name = function.name
    return_value_mappings = get_example_return_value_mappings(function_name, module_name)
    arg_value_mappings = get_example_arg_mappings(function_name, module_name, 'OBS.EVENT_OBS_EXIT')  # TODO: Make this not hardcoded
    args_list = (get_example_arg_key_value(k.arg, module_name, arg_value_mappings, constant_value_to_names) for k in function.args.args)
    raw_text_example = f'{", ".join(return_value_mappings)}{" = " if len(return_value_mappings) > 0 else ""}' + \
                       f'{module_name}.{function_name}' + \
                       f'({", ".join(args_list)})'

    return syntax_highlight_python_function_call(raw_text_example)

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


MODULES_DIR = '../KeyboardBinder/app/modules/keyboardBinder'
MODULE_FILES = (k for k in listdir(MODULES_DIR) if not k.startswith('_'))

for module_file in MODULE_FILES:
    module_name = module_file[0 : module_file.rindex('.')]

    with open(f'{MODULES_DIR}/{module_file}', 'r') as input_file, open(f'docs/pages/modules/{module_name.lower()}.html', 'w') as output_file:
        module_node = ast.parse(input_file.read())
        module_child_nodes = list(ast.iter_child_nodes(module_node))

        constant_defs = ( k for k in module_child_nodes if isinstance(k, ast.Assign) )
        function_defs = [ k for k in module_child_nodes if isinstance(k, ast.FunctionDef) ]
        function_defs.sort(key = lambda k: k.name)

        constant_value_to_names = dict(get_constant_info(k) for k in constant_defs if not k.targets[0].id.startswith('__'))  # type: ignore
        constant_names = list(constant_value_to_names.values())
        constant_names.sort()
        constant_groups = dict((k, list(v)) for k, v in groupby(constant_names, key = lambda k: k[0 : k.index('_')]))
        is_overload_function_filter: Callable[[ ast.FunctionDef ], bool ] = lambda fn: not any(k for k in function_defs if k != fn and k.name == fn.name and len(k.decorator_list) > 0)

        constant_group_descriptions = [ f'<h3>{" | ".join(group_items)}</h3>' for _, group_items in constant_groups.items() ]
        function_descriptions = [ get_function_description(k, module_name, constant_value_to_names) for k in function_defs if is_overload_function_filter(k) ]

        output_file.write(f'<h1>{module_name}</h1><p>{ast.get_docstring(module_node)}</p><br>' +
                         ('<h2>Constants</h2><hr>' if len(constant_group_descriptions) > 0 else '') +
                         '<hr>'.join(constant_group_descriptions) +
                         ('<br>' if len(constant_group_descriptions) > 0 else '') +
                         ('<h2>Functions</h2><hr>' if len(function_descriptions) > 0 else '') +
                         '<hr>'.join(function_descriptions))