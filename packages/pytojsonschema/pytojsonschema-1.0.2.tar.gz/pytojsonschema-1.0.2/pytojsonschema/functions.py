import ast
import fnmatch
import logging
import os
import typing

from .common import TypingNamespace, SchemaMap, Schema, init_typing_namespace, init_schema_map
from .jsonschema import get_json_schema_from_ast_element, InvalidTypeAnnotation
from .types import process_import, process_import_from, process_assign, process_class_def

JSON_SCHEMA_DRAFT = "http://json-schema.org/draft-07/schema#"
LOGGER = logging.getLogger()


def process_function_def(
    ast_function_def: ast.FunctionDef, typing_namespace: TypingNamespace, schema_map: SchemaMap,
) -> Schema:
    """
    Process a function to return its json schema

    :param ast_function_def: An ast function def element
    :param typing_namespace: The current typing namespace to be read
    :param schema_map: The current schema map to be read
    :return: The json schema of the function
    """
    LOGGER.info(f"Processing function {ast_function_def.name} ...")
    # Validation of not supported: Python 3.8 positional-only arguments and *args. Reason: We pass args as key-value
    if getattr(ast_function_def.args, "posonlyargs", None):
        raise InvalidTypeAnnotation(f"Function '{ast_function_def.name}' contains positional only arguments")
    if getattr(ast_function_def.args, "vararg", None):
        raise InvalidTypeAnnotation(
            f"Function '{ast_function_def.name}' contains a variable number positional arguments i.e. *args"
        )
    schema = {
        "$schema": JSON_SCHEMA_DRAFT,
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }
    # Process **kwargs
    if ast_function_def.args.kwarg is not None:
        if ast_function_def.args.kwarg.annotation is None:
            raise InvalidTypeAnnotation(
                f"Function '{ast_function_def.name}' is missing its **{ast_function_def.args.kwarg.arg} type annotation"
            )
        schema["additionalProperties"] = get_json_schema_from_ast_element(
            ast_function_def.args.kwarg.annotation, typing_namespace, schema_map
        )
    # Positional argument defaults is a non-padded list because you cannot have defaults before non-defaulted args
    # Keyword-only arguments, on the other side, can have defaults at random positions, and the default list is padded
    positional_arg_defaults_padding = len(ast_function_def.args.args) - len(ast_function_def.args.defaults)
    padded_positional_arg_defaults = [None] * positional_arg_defaults_padding + ast_function_def.args.defaults
    for argument, default in zip(
        ast_function_def.args.args + ast_function_def.args.kwonlyargs,
        padded_positional_arg_defaults + ast_function_def.args.kw_defaults,
    ):
        if argument.annotation is None:
            raise InvalidTypeAnnotation(
                f"Function '{ast_function_def.name}' is missing type annotation for the parameter '{argument.arg}'"
            )
        schema["properties"][argument.arg] = get_json_schema_from_ast_element(
            argument.annotation, typing_namespace, schema_map
        )
        if default is None:
            schema["required"].append(argument.arg)
    return schema


def process_file(
    file_path: str,
    include_patterns: typing.Optional[typing.List[str]] = None,
    exclude_patterns: typing.Optional[typing.List[str]] = None,
) -> SchemaMap:
    """
    Process a python file and return all json schemas from the top level functions it can find.

    You can use optional include/exclude patterns to filter the functions you want to process, with the exclude pattern
    overriding the include pattern. This patterns are implemented using Python package fnmatch.

    :param file_path: The path to the file
    :param include_patterns: A list of wildcard patterns to match the function names you want to include
    :param exclude_patterns: A list of wildcard patterns to match the function names you want to exclude
    :return: A dictionary containing your function names and their json schemas
    """
    with open(file_path) as f:
        ast_body = ast.parse(f.read()).body
    schema_map = init_schema_map()
    typing_namespace = init_typing_namespace()
    function_schema_map = {}

    def _is_a_pattern(name: str, patterns: typing.List[str]):
        for pattern in patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        else:
            return False

    def _process_function(ast_function_def: ast.FunctionDef):
        is_included = True
        is_excluded = False
        if include_patterns is not None:
            is_included = _is_a_pattern(ast_function_def.name, include_patterns)
        if exclude_patterns is not None:
            is_excluded = _is_a_pattern(ast_function_def.name, exclude_patterns)
        if is_excluded or not is_included:
            LOGGER.info(f"Function {ast_function_def.name} skipped")
        else:
            function_schema_map[ast_function_def.name] = process_function_def(
                ast_function_def, typing_namespace, schema_map
            )

    for node in ast_body:
        node_type = type(node)
        process_map = {
            ast.Import: lambda: process_import(node, typing_namespace, schema_map),
            ast.ImportFrom: lambda: process_import_from(node, os.path.dirname(file_path), typing_namespace, schema_map),
            ast.Assign: lambda: process_assign(node, typing_namespace, schema_map),
            ast.ClassDef: lambda: process_class_def(node, typing_namespace, schema_map),
            ast.FunctionDef: lambda: _process_function(node),
        }
        if node_type in process_map:
            process_map[node_type]()
    return function_schema_map


def process_package(
    package_path: str,
    include_patterns: typing.Optional[typing.List[str]] = None,
    exclude_patterns: typing.Optional[typing.List[str]] = None,
) -> SchemaMap:
    """
    Recursively process a package source folder and return all json schemas from the top level functions it can find.

    You can use optional include/exclude patterns to filter the functions you want to process, with the exclude pattern
    overriding the include pattern. This patterns are implemented using Python package fnmatch.

    :param package_path: The path to the your python package
    :param include_patterns: A list of wildcard patterns to match the function names you want to include
    :param exclude_patterns: A list of wildcard patterns to match the function names you want to exclude
    :return: A dictionary containing your function names and their json schemas
    """
    norm_package_path = os.path.normpath(package_path)
    path_prefix = os.path.split(norm_package_path)[0]
    function_schema_map = {}
    for root, _, files in os.walk(norm_package_path, topdown=True):
        for file in files:
            if file.endswith(".py"):
                package_chain = root.replace(path_prefix, "", 1)
                if package_chain.startswith("/"):
                    package_chain = package_chain.replace("/", "", 1)
                package_chain = package_chain.replace(os.path.sep, ".")
                if file != "__init__.py":
                    package_chain = f"{package_chain}.{os.path.splitext(file)[0]}"
                function_schema_map.update(
                    **{
                        f"{package_chain}.{func_name}": func_schema
                        for func_name, func_schema in process_file(
                            os.path.join(root, file), include_patterns, exclude_patterns
                        ).items()
                    }
                )
    return function_schema_map
