import ast
import typing

from .common import TypingNamespace, SchemaMap, VALID_AST_SUBSCRIPTS, InvalidTypeAnnotation
from .utils import get_ast_attribute_string


def search_typing_namespace(subscript_string: str, typing_namespace: TypingNamespace) -> typing.Optional[str]:
    for key in VALID_AST_SUBSCRIPTS:
        if subscript_string in typing_namespace.get(key, {}):
            return key


def get_json_schema_from_ast_element(
    ast_element: typing.Union[ast.Name, ast.Constant, ast.Attribute, ast.Subscript],
    typing_namespace: TypingNamespace,
    schema_map: SchemaMap,
) -> dict:
    def _get_or_raise(element_string: str) -> dict:
        if element_string not in schema_map:
            raise InvalidTypeAnnotation(
                f"Type '{element_string}' is invalid. Base types and the ones you have imported are "
                f"{', '.join(schema_map.keys())}. Did you miss an import?"
            )
        return schema_map[element_string]

    if isinstance(ast_element, ast.Constant):
        return {"type": "null"}
    elif isinstance(ast_element, (ast.Name, ast.Attribute)):
        return _get_or_raise(get_ast_attribute_string(ast_element))
    else:  # ast.Subscript
        subscript_string = get_ast_attribute_string(ast_element.value)
        subscript_type = search_typing_namespace(subscript_string, typing_namespace)
        if subscript_type is None:
            imported_types = []
            for key in VALID_AST_SUBSCRIPTS:
                for element in typing_namespace.get(key, {}):
                    imported_types.append(element)
            if imported_types:
                error_msg = (
                    f"Type '{subscript_string}' is invalid. You have imported {', '.join(sorted(imported_types))}, and "
                    f"we allow {', '.join(sorted(list(VALID_AST_SUBSCRIPTS)))}. Did you miss an import?"
                )
            else:
                error_msg = (
                    f"Type '{subscript_string}' is invalid, but no valid types were found. Did you forget importing "
                    f"typing?"
                )
            raise InvalidTypeAnnotation(error_msg)
        if isinstance(ast_element.slice.value, (ast.Constant, ast.Name, ast.Subscript)):
            inner_schema = get_json_schema_from_ast_element(ast_element.slice.value, typing_namespace, schema_map,)
            if subscript_type == "List":
                return {"type": "array", "items": inner_schema}
            elif subscript_type == "Optional":
                return {"anyOf": [inner_schema, {"type": "null"}]}
            else:
                raise InvalidTypeAnnotation(f"{subscript_type} cannot have a single element")
        else:  # ast.Tuple
            if subscript_type == "Dict":
                if not (
                    isinstance(ast_element.slice.value.elts[0], ast.Name)
                    and ast_element.slice.value.elts[0].id == "str"
                ):
                    raise InvalidTypeAnnotation("typing.Dict keys must be strings")
                return {
                    "type": "object",
                    "additionalProperties": get_json_schema_from_ast_element(
                        ast_element.slice.value.elts[1], typing_namespace, schema_map
                    ),
                }
            else:  # Union
                return {
                    "anyOf": [
                        get_json_schema_from_ast_element(element, typing_namespace, schema_map)
                        for element in ast_element.slice.value.elts
                    ]
                }
