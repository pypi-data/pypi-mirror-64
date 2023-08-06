import typing

VALID_AST_SUBSCRIPTS = frozenset({"Union", "List", "Dict", "Optional"})
VALID_TYPES = VALID_AST_SUBSCRIPTS | frozenset({"TypedDict", "Any"})

TypingNamespace = typing.Dict[str, typing.Set[str]]
SchemaMap = typing.Dict[str, dict]


class InvalidTypeAnnotation(Exception):
    pass
