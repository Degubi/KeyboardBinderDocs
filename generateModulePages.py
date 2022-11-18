import builtins
import ast
from itertools import groupby
from typing import Any
from apiMappings import get_example_arg_mappings, get_example_return_value_mappings, get_lambda_parameter_names

MODULES_DIR = '../KeyboardBinder/modules/keyboardBinder'


def is_overload_function_template(function: ast.FunctionDef, function_defs: list[ ast.FunctionDef ]):
    return len(function.decorator_list) == 0 and any(k for k in function_defs if function != k and k.name == function.name)

def get_constant_info(constant: ast.Assign):
    constant_name: ast.Name = constant.targets[0]  # type: ignore
    constant_value: ast.Constant = constant.value  # type: ignore

    return (constant_value.value, str(constant_name.id))

def get_optional_named_parameter_value(value: Any, module_name: str, constant_value_to_names: dict[Any, str]):
    optional_constant_name = constant_value_to_names.get(value, None)

    return f'{module_name}.{optional_constant_name}' if not optional_constant_name == None else \
           f"'{value}'" if type(value) == str and not value.startswith('lambda') else str(value)

def get_example_arg_key_value(arg_name: str, module_name: str, function_name: str, example_arg_value_mappings: dict[str, Any], constant_value_to_names: dict[Any, str]):
    arg_value = example_arg_value_mappings.get(arg_name, 'MISSING_ARG_VALUE')
    arg_value_type = type(arg_value)

    if arg_value == 'MISSING_ARG_VALUE':
        print(f'No example arg mapping found for {module_name}.{function_name}: \'{arg_name}\'')

    is_lambda_type = arg_value_type == str and arg_value.startswith('lambda')
    formatted_arg_value = f"'{arg_value}'" if arg_value_type == str and not is_lambda_type else get_optional_named_parameter_value(arg_value, module_name, constant_value_to_names)
    is_named_constant = arg_value in constant_value_to_names

    return f'{arg_name} = {module_name}.{constant_value_to_names[arg_value]}' if is_named_constant else \
           f'{arg_name} = {formatted_arg_value}' if not is_lambda_type else \
           f'{arg_name} = ' + formatted_arg_value

def syntax_highlight_python_function_call(code: str):
    function_call_ast: ast.Call = ast.parse(code).body[0].value  # type: ignore

    def highlight_arg(code: str, arg: ast.expr):
        before_part = code[0 : arg.col_offset]
        after_part = code[arg.end_col_offset : ]

        match arg:
            case ast.Constant(builtins.bool(value)):  return f'{before_part}<py-boolean>{value}</py-boolean>{after_part}'
            case ast.Constant(builtins.str(value)):   return f'{before_part}<py-string>\'{value}\'</py-string>{after_part}'
            case ast.Constant(builtins.int(value)):   return f'{before_part}<py-number>{value}</py-number>{after_part}'
            case ast.Constant(builtins.float(value)): return f'{before_part}<py-number>{value}</py-number>{after_part}'
            case ast.Attribute(ast.Name(module), constant): return f'{before_part}<py-module>{module}</py-module>.' + \
                                                                   f'<py-constant>{constant}</py-constant>{after_part}'
            case ast.Lambda(args, body): return f'{before_part}<py-boolean>lambda</py-boolean>' + \
                                                f'{(" " if len(args.args) > 0 else "") + ", ".join(k.arg for k in args.args)}: {syntax_highlight_python_function_call(code[body.col_offset : -1])})'
            case _:
                print(f'Unknown arg type found: {arg}')
                return ''

    function_call_named_args = function_call_ast.keywords
    function_call_named_args.reverse()
    function_call_anonymus_args = function_call_ast.args
    function_call_anonymus_args.reverse()

    for arg in function_call_named_args:    code = highlight_arg(code, arg.value)
    for arg in function_call_anonymus_args: code = highlight_arg(code, arg)

    function_call_type = type(function_call_ast.func)

    if function_call_type == ast.Attribute:
        function_call_func_attr: ast.Attribute = function_call_ast.func  # type: ignore
        function_call_module: ast.Name = function_call_func_attr.value  # type: ignore

        code = f'{code[0 : function_call_func_attr.col_offset]}<py-module>{function_call_module.id}</py-module>.' + \
               f'<py-function>{function_call_func_attr.attr}</py-function>{code[function_call_func_attr.end_col_offset : ]}'
    elif function_call_type == ast.Name:
        function_call_func: ast.Name = function_call_ast.func  # type: ignore

        code = f'<py-function>{function_call_func.id}</py-function>{code[function_call_func.end_col_offset : ]}'

    return code


def get_function_call_example(function: ast.FunctionDef, module_name: str, constant_value_to_names: dict[Any, str]):
    function_name = function.name
    return_value_mappings = get_example_return_value_mappings(function_name, module_name)

    if not isinstance(function.returns, ast.Constant) and len(return_value_mappings) == 0:
        print(f'Unmapped return value found for \'{module_name}.{function.name}\'')

    overload_arg_info = function.args.args[0].annotation if len(function.args.args) > 0 else None
    overload_arg_value = overload_arg_info.slice.value if isinstance(overload_arg_info, ast.Subscript) and isinstance(overload_arg_info.slice, ast.Constant) else None

    arg_value_mappings = get_example_arg_mappings(function_name, module_name, overload_arg_value)
    args_list = (get_example_arg_key_value(k.arg, module_name, function_name, arg_value_mappings, constant_value_to_names) for k in function.args.args)
    raw_text_example = f'{", ".join(return_value_mappings)}{" = " if len(return_value_mappings) > 0 else ""}' + \
                       f'{module_name}.{function_name}' + \
                       f'({", ".join(args_list)})'

    return syntax_highlight_python_function_call(raw_text_example)

def get_function_return_type(function: ast.FunctionDef):
    match function.returns:
        case ast.Constant(value): return value
        case ast.Name(value): return value
        case ast.Subscript(ast.Name(value), ast.Name(type_args)): return f'{value}[{type_args}]'
        case None:
            print(f'Missing return type found: {function.returns} in {function.name}')
            return 'MISSING_RETURN_TYPE'
        case _:
            print(f'Unhandled return type found: {function.returns} in {function.name}')
            return 'UNKNOWN_RETURN_TYPE'

def get_dict_typing_definition_description(dict_typing_def: ast.Dict):
    return '{ ' + ', '.join(f'{dict_typing_def.keys[i].value}: {dict_typing_def.values[i].id}' for i in range(len(dict_typing_def.keys))) + ' }'  # type: ignore

def get_function_arg_description(arg: ast.arg, module_name: str, function_name: str, constant_value_to_names: dict[Any, str], dict_typing_defs: dict[str, ast.Dict]):
    arg_name = arg.arg

    match arg.annotation:
        case ast.Name(id):
            optional_dict_typing_def = dict_typing_defs.get(id, None)

            return f'{arg_name}: {id}' if optional_dict_typing_def == None else f'{arg_name}: {get_dict_typing_definition_description(optional_dict_typing_def)}'
        case ast.Subscript(_, ast.Constant(value)): return f'{arg_name}: {get_optional_named_parameter_value(value, module_name, constant_value_to_names)}'
        case ast.Subscript(_, ast.Tuple(type_params)):
            if isinstance(type_params[0], ast.List):
                function_arg_types: list[ast.Name] = type_params[0].elts  # type: ignore
                function_return_type: ast.Constant = type_params[1]  # type: ignore
                lambda_arg_names = get_lambda_parameter_names(module_name, function_name, arg_name)

                if len(lambda_arg_names) != len(function_arg_types):
                    print(f'Unmapped lambda params found in {module_name}.{function_name}, arg name: {arg_name}')

                    return f'{arg_name}: ({", ".join(f"UNKNOWN_ARG: {function_arg_types[i].id}" for i in range(0, len(function_arg_types)))}) -> {function_return_type.value}'

                return f'{arg_name}: ({", ".join(f"{lambda_arg_names[i]}: {function_arg_types[i].id}" for i in range(0, len(function_arg_types)))}) -> {function_return_type.value}'
            else:
                union_values: list[ast.Constant] = type_params  # type: ignore

                return f'{arg_name}: {" | ".join(get_optional_named_parameter_value(k.value, module_name, constant_value_to_names) for k in union_values if type(k.value) == str or k.value in constant_value_to_names)}'
        case _:
            print(f'Unknown arg type found: {arg.annotation}')
            return 'UNKNOWN_ARG_TYPE'


def get_function_description(function: ast.FunctionDef, module_name: str, constant_value_to_names: dict[Any, str], dict_typing_defs: dict[str, ast.Dict]):
    return f'<h3 id = "{function.name}">{function.name}({", ".join(get_function_arg_description(k, module_name, function.name, constant_value_to_names, dict_typing_defs) for k in function.args.args)}) -> {get_function_return_type(function)}</h3>' + \
           f'<h4>Description:</h4><p>{ast.get_docstring(function) or "MISSING_FUNCTION_DESCRIPTION"}' + \
           f'</p><h4>Example:</h4><div class="code-example-block">{get_function_call_example(function, module_name, constant_value_to_names)}</div>'

def generate_module_documentation(module_file: str):
    module_name = module_file[0 : module_file.rindex('.')]

    with open(f'{MODULES_DIR}/{module_file}', 'r') as input_file, open(f'docs/pages/modules/{module_name.lower()}.html', 'w') as output_file:
        module_node = ast.parse(input_file.read())
        module_child_nodes = list(ast.iter_child_nodes(module_node))
        is_dict_typedef = lambda k: isinstance(k, ast.Assign) and k.targets[0].id.startswith('__') and not k.targets[0].id == '__INTEGRATION' and k.value.func.id == '__TypedDict'  # type: ignore

        constant_defs = ( k for k in module_child_nodes if isinstance(k, ast.Assign) and not k.targets[0].id.startswith('__'))  # type: ignore
        dict_typing_defs = dict((k.targets[0].id, k.value.args[1]) for k in module_child_nodes if is_dict_typedef(k))  # type: ignore
        function_defs = [ k for k in module_child_nodes if isinstance(k, ast.FunctionDef) and not k.name.startswith('__') ]
        function_defs.sort(key = lambda k: k.name)

        constant_value_to_names = dict(get_constant_info(k) for k in constant_defs)
        constant_names = list(constant_value_to_names.values())
        constant_names.sort()
        constant_groups = dict((k, list(v)) for k, v in groupby(constant_names, key = lambda k: k[0 : k.index('_')]))

        constant_group_descriptions = [ f'<h3>{" | ".join(group_items)}</h3>' for _, group_items in constant_groups.items() ]
        function_descriptions = [ get_function_description(k, module_name, constant_value_to_names, dict_typing_defs) for k in function_defs if not is_overload_function_template(k, function_defs) ]
        module_import_text = '<div class = "code-example-block">' + \
                               '<py-keyword>from </py-keyword>' + \
                               '<py-module>keyboardBinder </py-module>' + \
                               '<py-keyword>import </py-keyword>' + \
                              f'<py-module>{module_name}</py-module>' + \
                             '</div>'

        output_file.write(f'<h1>{module_name} module</h1>\n' +
                          f'<p>{ast.get_docstring(module_node)}</p><br>\n' +
                          '<h2>Importing</h2>\n' + module_import_text + '\n' +
                          ('<h2>Constants</h2><hr>\n' if len(constant_group_descriptions) > 0 else '') +
                           '<hr>\n'.join(constant_group_descriptions) +
                          ('<br>' if len(constant_group_descriptions) > 0 else '') +
                          ('<h2>Functions</h2><hr>\n' if len(function_descriptions) > 0 else '') +
                           '<hr>\n'.join(function_descriptions))


generate_module_documentation('Application.py')
generate_module_documentation('Blender.py')
generate_module_documentation('Desktop.py')
generate_module_documentation('Keyboard.py')
generate_module_documentation('Mouse.py')
generate_module_documentation('OBS.py')
generate_module_documentation('PremierePro.py')
generate_module_documentation('Twitch.py')
generate_module_documentation('VLC.py')