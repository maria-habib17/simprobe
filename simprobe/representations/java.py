from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum


class TokenKind(Enum):
    KEYWORD = "keyword"
    IDENTIFIER = "identifier"
    INTEGER = "integer"
    FLOAT = "float"
    CHARACTER = "character"
    STRING = "string"
    OPERATOR = "operator"
    SEPARATOR = "separator"


@dataclass(frozen=True)
class Token:
    kind: TokenKind
    value: str


JAVA_KEYWORDS = frozenset(
    """
    abstract assert boolean break byte case catch char class const continue
    default do double else enum extends final finally float for goto if
    implements import instanceof int interface long native new package private
    protected public record return short static strictfp super switch
    synchronized this throw throws transient try void volatile while sealed
    permits non-sealed var yield
    """.split()
)

RESERVED_LITERALS = frozenset({"true", "false", "null"})

MULTI_OPERATORS = (
    ">>>=", "<<=", ">>=", "...", ">>>", "<<", ">>", "==", "!=", "<=", ">=",
    "&&", "||", "++", "--", "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=",
    "->", "::",
)

SINGLE_OPERATORS = frozenset("=><!~?:+-*/%&|^")
SEPARATORS = frozenset("(){}[];,.")

_IDENTIFIER_RE = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")

_FLOAT_PATTERNS = (
    re.compile(
        r"(?:"
        r"(?:\d[\d_]*\.[\d_]*|\.[\d_]+)(?:[eE][+-]?[\d_]+)?"
        r"|"
        r"\d[\d_]*[eE][+-]?[\d_]+"
        r")"
        r"[fFdD]?"
    ),
    re.compile(r"\d[\d_]*[fFdD]"),
)

_INTEGER_RE = re.compile(
    r"(?:"
    r"0[xX][0-9a-fA-F_]+"
    r"|0[bB][01_]+"
    r"|0[0-7_]+"
    r"|[1-9][0-9_]*"
    r"|0"
    r")[lL]?"
)


def _scan_quoted(source: str, start: int, quote: str) -> tuple[str, int]:
    index = start + 1
    escaped = False

    while index < len(source):
        char = source[index]

        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == quote:
            return source[start : index + 1], index + 1

        index += 1

    raise ValueError(f"Unterminated quoted literal at offset {start}")


def scan_java(source: str) -> tuple[Token, ...]:
    tokens: list[Token] = []
    index = 0

    while index < len(source):
        char = source[index]

        if char.isspace():
            index += 1
            continue

        if source.startswith("//", index):
            newline = source.find("\n", index + 2)
            index = len(source) if newline == -1 else newline + 1
            continue

        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end == -1:
                raise ValueError(f"Unterminated block comment at offset {index}")
            index = end + 2
            continue

        if char == '"':
            value, index = _scan_quoted(source, index, '"')
            tokens.append(Token(TokenKind.STRING, value))
            continue

        if char == "'":
            value, index = _scan_quoted(source, index, "'")
            tokens.append(Token(TokenKind.CHARACTER, value))
            continue

        identifier = _IDENTIFIER_RE.match(source, index)
        if identifier:
            value = identifier.group(0)
            kind = (
                TokenKind.KEYWORD
                if value in JAVA_KEYWORDS or value in RESERVED_LITERALS
                else TokenKind.IDENTIFIER
            )
            tokens.append(Token(kind, value))
            index = identifier.end()
            continue

        number_match = None
        for pattern in _FLOAT_PATTERNS:
            number_match = pattern.match(source, index)
            if number_match:
                tokens.append(Token(TokenKind.FLOAT, number_match.group(0)))
                index = number_match.end()
                break

        if number_match:
            continue

        integer = _INTEGER_RE.match(source, index)
        if integer:
            tokens.append(Token(TokenKind.INTEGER, integer.group(0)))
            index = integer.end()
            continue

        operator = next(
            (candidate for candidate in MULTI_OPERATORS if source.startswith(candidate, index)),
            None,
        )
        if operator is not None:
            tokens.append(Token(TokenKind.OPERATOR, operator))
            index += len(operator)
            continue

        if char in SINGLE_OPERATORS:
            tokens.append(Token(TokenKind.OPERATOR, char))
            index += 1
            continue

        if char in SEPARATORS:
            tokens.append(Token(TokenKind.SEPARATOR, char))
            index += 1
            continue

        raise ValueError(f"Unsupported Java character {char!r} at offset {index}")

    return tuple(tokens)


def r0(tokens: Iterable[Token]) -> tuple[str, ...]:
    return tuple(token.value for token in tokens)


def r1(tokens: Iterable[Token]) -> tuple[str, ...]:
    return r0(tokens)


def r2(tokens: Iterable[Token]) -> tuple[str, ...]:
    return tuple(
        "<IDENT>" if token.kind is TokenKind.IDENTIFIER else token.value
        for token in tokens
    )


def _literal_category(token: Token) -> str | None:
    if token.kind is TokenKind.INTEGER:
        return "<INT_LITERAL>"
    if token.kind is TokenKind.FLOAT:
        return "<FLOAT_LITERAL>"
    if token.kind is TokenKind.CHARACTER:
        return "<CHAR_LITERAL>"
    if token.kind is TokenKind.STRING:
        return "<STRING_LITERAL>"
    if token.value in {"true", "false"}:
        return "<BOOLEAN_LITERAL>"
    if token.value == "null":
        return "<NULL_LITERAL>"
    return None


def r3(tokens: Iterable[Token]) -> tuple[str, ...]:
    output: list[str] = []

    for token in tokens:
        literal = _literal_category(token)
        if literal is not None:
            output.append(literal)
        elif token.kind is TokenKind.IDENTIFIER:
            output.append("<IDENT>")
        else:
            output.append(token.value)

    return tuple(output)


_TYPE_PREDECESSORS = frozenset(
    {"class", "interface", "enum", "record", "extends", "implements", "new", "instanceof"}
)


def _is_declaration_type(tokens: tuple[Token, ...], index: int) -> bool:
    if index + 1 >= len(tokens):
        return False

    current = tokens[index]
    following = tokens[index + 1]

    if current.kind is not TokenKind.IDENTIFIER:
        return False

    return following.kind is TokenKind.IDENTIFIER


def r4(tokens: Iterable[Token]) -> tuple[str, ...]:
    token_list = tuple(tokens)
    output: list[str] = []

    for index, token in enumerate(token_list):
        literal = _literal_category(token)
        if literal is not None:
            output.append(literal)
            continue

        if token.kind is not TokenKind.IDENTIFIER:
            output.append(token.value)
            continue

        previous_value = token_list[index - 1].value if index > 0 else None
        next_value = token_list[index + 1].value if index + 1 < len(token_list) else None

        if (
            previous_value in _TYPE_PREDECESSORS
            or _is_declaration_type(token_list, index)
            or token.value[:1].isupper()
        ):
            output.append("<TYPE_IDENT>")
        elif next_value == "(":
            output.append("<METHOD_IDENT>")
        else:
            output.append("<IDENT>")

    return tuple(output)


_R5_KEYWORDS = {
    "class": "<CLASS_DECL>",
    "if": "<IF>",
    "else": "<ELSE>",
    "for": "<FOR>",
    "while": "<WHILE>",
    "return": "<RETURN>",
    "continue": "<CONTINUE>",
    "break": "<BREAK>",
    "new": "<NEW>",
}

_R5_SYMBOLS = {
    "{": "<BLOCK_OPEN>",
    "}": "<BLOCK_CLOSE>",
    "(": "<PAREN_OPEN>",
    ")": "<PAREN_CLOSE>",
    "[": "<BRACKET_OPEN>",
    "]": "<BRACKET_CLOSE>",
    ";": "<STATEMENT_END>",
    ",": "<COMMA>",
    "=": "<ASSIGN>",
    "++": "<INC_DEC>",
    "--": "<INC_DEC>",
    ".": "<MEMBER_ACCESS>",
}

_COMPARE = frozenset({"==", "!=", "<", ">", "<=", ">="})
_ARITH = frozenset({"+", "-", "*", "/", "%"})
_LOGIC = frozenset({"&&", "||", "!"})


def r5(tokens: Iterable[Token]) -> tuple[str, ...]:
    token_list = tuple(tokens)
    output: list[str] = []

    for index, token in enumerate(token_list):
        literal = _literal_category(token)
        if literal is not None:
            output.append("<LITERAL>")
            continue

        keyword_symbol = _R5_KEYWORDS.get(token.value)
        if keyword_symbol is not None:
            output.append(keyword_symbol)
            continue

        if (
            token.kind is TokenKind.IDENTIFIER
            and index + 1 < len(token_list)
            and token_list[index + 1].value == "("
        ):
            output.append("<METHOD_LIKE>")
            continue

        symbol = _R5_SYMBOLS.get(token.value)
        if symbol is not None:
            output.append(symbol)
        elif token.value in _COMPARE:
            output.append("<COMPARE>")
        elif token.value in _ARITH:
            output.append("<ARITH>")
        elif token.value in _LOGIC:
            output.append("<LOGIC>")

    return tuple(output)


_R6_MAP = {
    "<CLASS_DECL>": "<DECL>",
    "<METHOD_LIKE>": "<DECL>",
    "<IF>": "<CONTROL>",
    "<ELSE>": "<CONTROL>",
    "<FOR>": "<CONTROL>",
    "<WHILE>": "<CONTROL>",
    "<RETURN>": "<FLOW>",
    "<CONTINUE>": "<FLOW>",
    "<BREAK>": "<FLOW>",
    "<NEW>": "<OP>",
    "<ASSIGN>": "<OP>",
    "<COMPARE>": "<OP>",
    "<ARITH>": "<OP>",
    "<LOGIC>": "<OP>",
    "<INC_DEC>": "<OP>",
    "<MEMBER_ACCESS>": "<OP>",
    "<BLOCK_OPEN>": "<BLOCK>",
    "<BLOCK_CLOSE>": "<BLOCK>",
    "<PAREN_OPEN>": "<GROUP>",
    "<PAREN_CLOSE>": "<GROUP>",
    "<BRACKET_OPEN>": "<GROUP>",
    "<BRACKET_CLOSE>": "<GROUP>",
    "<STATEMENT_END>": "<SEP>",
    "<COMMA>": "<SEP>",
    "<LITERAL>": "<VALUE>",
}


def r6(r5_tokens: Iterable[str]) -> tuple[str, ...]:
    output: list[str] = []

    for symbol in r5_tokens:
        mapped = "<FILE_BOUNDARY>" if symbol == "<FILE_BOUNDARY>" else _R6_MAP[symbol]

        if mapped == "<FILE_BOUNDARY>" or not output or output[-1] != mapped:
            output.append(mapped)

    return tuple(output)


def represent_source(source: str, stage: str) -> tuple[str, ...]:
    tokens = scan_java(source)
    stage = stage.upper()

    functions = {
        "R0": r0,
        "R1": r1,
        "R2": r2,
        "R3": r3,
        "R4": r4,
        "R5": r5,
    }

    if stage == "R6":
        return r6(r5(tokens))

    try:
        function = functions[stage]
    except KeyError as exc:
        raise ValueError(f"Unknown representation stage: {stage}") from exc

    return function(tokens)


STAGES = ("R0", "R1", "R2", "R3", "R4", "R5", "R6")
