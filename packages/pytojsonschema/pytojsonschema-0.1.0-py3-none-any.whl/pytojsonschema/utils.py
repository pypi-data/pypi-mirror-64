import ast
import typing

from .common import InvalidTypeAnnotation


def get_ast_attribute_string(ast_element: typing.Union[ast.Name, ast.Attribute]) -> str:
    if isinstance(ast_element, ast.Name):
        return ast_element.id
    elif isinstance(ast_element.value, ast.Name):
        return f"{ast_element.value.id}.{ast_element.attr}"
    else:
        return f"{get_ast_attribute_string(ast_element.value)}.{ast_element.attr}"


def get_ast_annotation_str(
    ast_element: typing.Union[ast.Constant, ast.Name, ast.Attribute, ast.Subscript, ast.Tuple]
) -> str:
    if isinstance(ast_element, ast.Constant):
        return str(ast_element.value)
    elif isinstance(ast_element, (ast.Name, ast.Attribute)):
        return get_ast_attribute_string(ast_element)
    elif isinstance(ast_element, ast.Subscript):
        return f"{get_ast_attribute_string(ast_element.value)}[{get_ast_annotation_str(ast_element.slice.value)}]"
    elif isinstance(ast_element, ast.Tuple):
        return ", ".join((get_ast_annotation_str(element) for element in ast_element.elts))
    else:
        raise InvalidTypeAnnotation(f"Unknown ast element '{type(ast_element)}' for a type annotation")
