import ast
import os
import typing

from .common import TypingNamespace, SchemaMap, VALID_TYPES
from .jsonschema import get_json_schema_from_ast_element, get_ast_attribute_string

ANY_SCHEMA = {
    "anyOf": [
        {"type": "object"},
        {"type": "array"},
        {"type": "null"},
        {"type": "string"},
        {"type": "boolean"},
        {"type": "integer"},
        {"type": "number"},
    ]
}
BASE_SCHEMA_MAP = {
    "bool": {"type": "boolean"},
    "int": {"type": "integer"},
    "float": {"type": "number"},
    "str": {"type": "string"},
}


def init_typing_namespace() -> TypingNamespace:
    return {valid_type: set() for valid_type in VALID_TYPES}


def process_alias(ast_alias: ast.alias) -> str:
    if ast_alias.asname is None:
        return ast_alias.name
    else:
        return ast_alias.asname


def process_import(ast_import: ast.Import) -> typing.Tuple[TypingNamespace, SchemaMap]:
    typing_namespace: TypingNamespace = init_typing_namespace()
    schema_map: SchemaMap = {}
    for import_name in ast_import.names:
        if import_name.name == "typing":
            module_element = process_alias(import_name)
            for valid_type in VALID_TYPES:
                element = f"{module_element}.{valid_type}"
                typing_namespace[valid_type].add(element)
                if valid_type == "Any":
                    schema_map[element] = ANY_SCHEMA
    return typing_namespace, schema_map


def process_import_from(ast_import_from: ast.ImportFrom, base_path: str) -> typing.Tuple[TypingNamespace, SchemaMap]:
    typing_namespace: TypingNamespace = init_typing_namespace()
    schema_map: SchemaMap = {}
    # Level == 0 are absolute imports. We only follow the one that targets typing
    if ast_import_from.level == 0 and ast_import_from.module == "typing":
        for import_name in ast_import_from.names:
            if import_name.name in VALID_TYPES:
                element = process_alias(import_name)
                typing_namespace[import_name.name].add(element)
                if import_name.name == "Any":
                    schema_map[element] = ANY_SCHEMA
    # Level >= 1 are relative imports. 1 is the current directory, 2 the parent, 3 the grandparent, and so on.
    elif ast_import_from.level >= 1:
        module = f"{ast_import_from.module}.py" if ast_import_from.module else "__init__.py"
        new_base_path = base_path
        for _ in range(ast_import_from.level - 1):
            new_base_path = os.path.join(new_base_path, os.pardir)
        path = os.path.join(new_base_path, module)
        with open(path) as f:
            ast_module = ast.parse(f.read())
        for node in ast_module.body:
            if isinstance(node, ast.Import):
                new_typing_namespace, new_schema_map = process_import(node)
                typing_namespace.update(new_typing_namespace)
                schema_map.update(new_schema_map)
            elif isinstance(node, ast.ImportFrom):
                new_typing_namespace, new_schema_map = process_import_from(node, new_base_path)
                typing_namespace.update(new_typing_namespace)
                schema_map.update(new_schema_map)
            elif isinstance(node, ast.Assign) and node.targets[0].id:
                schema_map.update(process_assign(node, typing_namespace, schema_map))
            elif isinstance(node, ast.ClassDef) and node.name:
                schema_map.update(process_class_def(node, typing_namespace, schema_map))
        for import_name in ast_import_from.names:
            item = schema_map.get(import_name.name)
            if item is not None:  # Import could be something we didn't care about and hence didn't put in schema_map
                schema_map[import_name.name] = item
    return typing_namespace, schema_map


def process_class_def(
    ast_class_def: ast.ClassDef, typing_namespace: TypingNamespace, schema_map: SchemaMap
) -> SchemaMap:
    # This supports TypedDict class syntax
    new_schema_map: SchemaMap = {}
    if ast_class_def.bases and get_ast_attribute_string(ast_class_def.bases[0]) in typing_namespace.get(
        "TypedDict", set()
    ):
        properties = {}
        for index, node in enumerate(ast_class_def.body):
            if isinstance(node, ast.AnnAssign):
                properties[node.target.id] = get_json_schema_from_ast_element(
                    node.annotation, typing_namespace, schema_map
                )
        new_schema_map[ast_class_def.name] = {
            "type": "object",
            "properties": properties,
            "required": list(properties.keys()),
            "additionalProperties": False,
        }
    return new_schema_map


def process_assign(ast_assign: ast.Assign, typing_namespace: TypingNamespace, schema_map: SchemaMap) -> SchemaMap:
    new_schema_map: SchemaMap = {}
    if isinstance(ast_assign.targets[0], ast.Name) and isinstance(ast_assign.value, ast.Subscript):
        new_schema_map[ast_assign.targets[0].id] = get_json_schema_from_ast_element(
            ast_assign.value, typing_namespace, schema_map
        )
    return new_schema_map
