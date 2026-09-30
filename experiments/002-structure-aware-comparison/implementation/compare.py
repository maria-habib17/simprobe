"""Experiment 002 frozen comparison engine.

This module implements the comparison rules frozen in
MEASUREMENT_SPECIFICATION.md.

It deliberately contains no primary-fixture measurement runner.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re
from typing import Sequence


JAVA_KEYWORDS = frozenset(
    """
    abstract assert boolean break byte case catch char class const continue
    default do double else enum extends final finally float for goto if
    implements import instanceof int interface long native new package private
    protected public return short static strictfp super switch synchronized
    this throw throws transient try void volatile while true false null
    """.split()
)


MULTI_OPERATORS = (
    ">>>=",
    "<<=",
    ">>=",
    ">>>",
    "...",
    "->",
    "::",
    "++",
    "--",
    "==",
    "!=",
    "<=",
    ">=",
    "&&",
    "||",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "&=",
    "|=",
    "^=",
    "<<",
    ">>",
)


SINGLE_SYMBOLS = frozenset(
    "{}()[];,.=+-*/%<>!&|^~?:@"
)


IDENT_RE = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
INT_RE = re.compile(
    r"""
    (?:
        0[xX][0-9A-Fa-f_]+
        |
        0[bB][01_]+
        |
        0[0-7_]+
        |
        [0-9][0-9_]*
    )
    [lL]?
    """,
    re.VERBOSE,
)


@dataclass(frozen=True)
class LexToken:
    kind: str
    value: str
    start: int
    end: int


@dataclass(frozen=True)
class MethodUnit:
    relative_path: str
    source_start: int
    tokens: tuple[str, ...]


@dataclass(frozen=True)
class MatchingResult:
    total_weight: float
    assignment: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class C0Result:
    left_token_count: int
    right_token_count: int
    edit_distance: int
    similarity: float


@dataclass(frozen=True)
class C1Result:
    left_method_count: int
    right_method_count: int
    matched_method_count: int
    matched_similarity_sum: float
    similarity: float
    assignment: tuple[tuple[int, int], ...]


def lex_java(source: str) -> list[LexToken]:
    """Lex the Java subset required by the frozen Experiment 002 fixture."""

    tokens: list[LexToken] = []
    i = 0
    n = len(source)

    while i < n:
        ch = source[i]

        if ch.isspace():
            i += 1
            continue

        if source.startswith("//", i):
            newline = source.find("\n", i + 2)
            i = n if newline == -1 else newline + 1
            continue

        if source.startswith("/*", i):
            close = source.find("*/", i + 2)
            if close == -1:
                raise ValueError("Unterminated block comment.")
            i = close + 2
            continue

        if ch == '"':
            start = i
            i += 1
            escaped = False

            while i < n:
                current = source[i]

                if escaped:
                    escaped = False
                    i += 1
                    continue

                if current == "\\":
                    escaped = True
                    i += 1
                    continue

                if current == '"':
                    i += 1
                    break

                i += 1
            else:
                raise ValueError("Unterminated string literal.")

            tokens.append(LexToken("STRING", source[start:i], start, i))
            continue

        if ch == "'":
            start = i
            i += 1
            escaped = False

            while i < n:
                current = source[i]

                if escaped:
                    escaped = False
                    i += 1
                    continue

                if current == "\\":
                    escaped = True
                    i += 1
                    continue

                if current == "'":
                    i += 1
                    break

                i += 1
            else:
                raise ValueError("Unterminated character literal.")

            tokens.append(LexToken("CHAR", source[start:i], start, i))
            continue

        ident_match = IDENT_RE.match(source, i)
        if ident_match is not None:
            value = ident_match.group(0)
            kind = "KEYWORD" if value in JAVA_KEYWORDS else "IDENT"
            tokens.append(
                LexToken(kind, value, ident_match.start(), ident_match.end())
            )
            i = ident_match.end()
            continue

        int_match = INT_RE.match(source, i)
        if int_match is not None:
            value = int_match.group(0)
            tokens.append(
                LexToken("INT", value, int_match.start(), int_match.end())
            )
            i = int_match.end()
            continue

        matched_operator = None
        for operator in MULTI_OPERATORS:
            if source.startswith(operator, i):
                matched_operator = operator
                break

        if matched_operator is not None:
            tokens.append(
                LexToken(
                    "SYMBOL",
                    matched_operator,
                    i,
                    i + len(matched_operator),
                )
            )
            i += len(matched_operator)
            continue

        if ch in SINGLE_SYMBOLS:
            tokens.append(LexToken("SYMBOL", ch, i, i + 1))
            i += 1
            continue

        raise ValueError(
            f"Unsupported Java lexical character {ch!r} at offset {i}."
        )

    return tokens


def normalize_token(token: LexToken) -> str:
    if token.kind == "KEYWORD":
        return token.value
    if token.kind == "IDENT":
        return "<IDENT>"
    if token.kind == "INT":
        return "<INT>"
    if token.kind == "STRING":
        return "<STRING>"
    if token.kind == "CHAR":
        return "<CHAR>"
    if token.kind == "SYMBOL":
        return token.value
    raise ValueError(f"Unknown token kind: {token.kind}")


def normalized_tokens(source: str) -> tuple[str, ...]:
    return tuple(normalize_token(token) for token in lex_java(source))


def levenshtein_distance(
    left: Sequence[str],
    right: Sequence[str],
) -> int:
    """Standard unit-cost token Levenshtein distance."""

    if len(left) < len(right):
        left, right = right, left

    previous = list(range(len(right) + 1))

    for i, left_token in enumerate(left, start=1):
        current = [i]

        for j, right_token in enumerate(right, start=1):
            substitution = previous[j - 1] + (
                0 if left_token == right_token else 1
            )
            insertion = current[j - 1] + 1
            deletion = previous[j] + 1

            current.append(min(substitution, insertion, deletion))

        previous = current

    return previous[-1]


def normalized_similarity(
    left: Sequence[str],
    right: Sequence[str],
) -> tuple[int, float]:
    if not left and not right:
        return 0, 1.0

    if not left or not right:
        return max(len(left), len(right)), 0.0

    distance = levenshtein_distance(left, right)
    similarity = 1.0 - distance / max(len(left), len(right))
    return distance, similarity


def _posix_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def java_files(submission: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in submission.rglob("*")
            if path.is_file() and path.suffix == ".java"
        ),
        key=lambda path: _posix_relative(path, submission),
    )


def c0_sequence(submission: Path) -> tuple[str, ...]:
    sequence: list[str] = []
    files = java_files(submission)

    for index, path in enumerate(files):
        if index:
            sequence.append("<FILE_BOUNDARY>")

        sequence.extend(
            normalized_tokens(path.read_text(encoding="utf-8"))
        )

    return tuple(sequence)


def compare_c0(left: Path, right: Path) -> C0Result:
    left_tokens = c0_sequence(left)
    right_tokens = c0_sequence(right)

    distance, similarity = normalized_similarity(
        left_tokens,
        right_tokens,
    )

    return C0Result(
        left_token_count=len(left_tokens),
        right_token_count=len(right_tokens),
        edit_distance=distance,
        similarity=similarity,
    )


def _matching_pairs(
    tokens: Sequence[LexToken],
    open_value: str,
    close_value: str,
) -> dict[int, int]:
    stack: list[int] = []
    pairs: dict[int, int] = {}

    for index, token in enumerate(tokens):
        if token.value == open_value:
            stack.append(index)
        elif token.value == close_value:
            if not stack:
                raise ValueError(
                    f"Unbalanced delimiter {close_value!r}."
                )

            opening = stack.pop()
            pairs[opening] = index

    if stack:
        raise ValueError(f"Unbalanced delimiter {open_value!r}.")

    return pairs


def _previous_boundary(tokens: Sequence[LexToken], index: int) -> int:
    """Return the first token index of the declaration containing index."""

    cursor = index - 1

    while cursor >= 0:
        value = tokens[cursor].value
        if value in {";", "{", "}"}:
            return cursor + 1
        cursor -= 1

    return 0


def _is_method_candidate(
    tokens: Sequence[LexToken],
    name_index: int,
    open_paren_index: int,
    close_paren_index: int,
    open_brace_index: int,
) -> bool:
    name = tokens[name_index]

    if name.kind != "IDENT":
        return False

    # Calls such as object.method(...) and Type.method(...) are not
    # declarations.
    if name_index > 0 and tokens[name_index - 1].value == ".":
        return False

    # Control-flow constructs are keywords and already rejected above.
    # A declaration must have something before its name in the same
    # declaration segment: return type, modifier + return type, etc.
    start = _previous_boundary(tokens, name_index)

    if start >= name_index:
        return False

    prefix = tokens[start:name_index]

    # Assignment/new-expression contexts are not method declarations.
    if any(
        token.value in {
            "=",
            "new",
            "return",
            "throw",
            "?",
            ":",
        }
        for token in prefix
    ):
        return False

    # Method declarations in the frozen subset proceed directly from the
    # parameter close to either "throws ..." or the body brace.
    between = tokens[close_paren_index + 1 : open_brace_index]

    if between:
        if between[0].value != "throws":
            return False

        if any(
            token.kind not in {"KEYWORD", "IDENT"}
            and token.value not in {".", ","}
            for token in between
        ):
            return False

    # The opening parenthesis must immediately follow the candidate name.
    if open_paren_index != name_index + 1:
        return False

    return True


def extract_method_units(
    source: str,
    relative_path: str,
) -> list[MethodUnit]:
    tokens = lex_java(source)

    if not tokens:
        return []

    parens = _matching_pairs(tokens, "(", ")")
    braces = _matching_pairs(tokens, "{", "}")

    units: list[MethodUnit] = []

    for open_paren, close_paren in sorted(parens.items()):
        name_index = open_paren - 1

        if name_index < 0:
            continue

        cursor = close_paren + 1

        # Optional throws clause.
        if cursor < len(tokens) and tokens[cursor].value == "throws":
            cursor += 1

            while cursor < len(tokens) and tokens[cursor].value != "{":
                cursor += 1

        if cursor >= len(tokens) or tokens[cursor].value != "{":
            continue

        open_brace = cursor

        if open_brace not in braces:
            raise ValueError("Method body brace has no matching close.")

        if not _is_method_candidate(
            tokens,
            name_index,
            open_paren,
            close_paren,
            open_brace,
        ):
            continue

        close_brace = braces[open_brace]
        start_index = _previous_boundary(tokens, name_index)

        unit_tokens = tuple(
            normalize_token(token)
            for token in tokens[start_index : close_brace + 1]
        )

        units.append(
            MethodUnit(
                relative_path=relative_path,
                source_start=tokens[start_index].start,
                tokens=unit_tokens,
            )
        )

    # Nested calls inside method bodies may look superficially method-like
    # under malformed input. Deduplicate exact source starts defensively.
    unique: dict[tuple[str, int], MethodUnit] = {}

    for unit in units:
        unique[(unit.relative_path, unit.source_start)] = unit

    return sorted(
        unique.values(),
        key=lambda unit: (unit.relative_path, unit.source_start),
    )


def submission_method_units(submission: Path) -> list[MethodUnit]:
    units: list[MethodUnit] = []

    for path in java_files(submission):
        relative = _posix_relative(path, submission)
        source = path.read_text(encoding="utf-8")
        units.extend(extract_method_units(source, relative))

    return sorted(
        units,
        key=lambda unit: (unit.relative_path, unit.source_start),
    )


def maximum_weight_matching(
    weights: Sequence[Sequence[float]],
) -> MatchingResult:
    """Exact deterministic maximum-weight matching.

    The returned assignment always uses row indices from the original matrix
    as its first coordinate and column indices as its second coordinate.

    Among exactly equal total weights, the lexicographically smallest tuple
    of original-coordinate pairs is selected.
    """

    rows = len(weights)

    if rows == 0:
        return MatchingResult(0.0, ())

    columns = len(weights[0])

    if any(len(row) != columns for row in weights):
        raise ValueError("Weight matrix is ragged.")

    if columns == 0:
        return MatchingResult(0.0, ())

    if rows <= columns:
        matrix = tuple(tuple(row) for row in weights)

        @lru_cache(maxsize=None)
        def solve(
            row: int,
            used_columns: int,
        ) -> tuple[float, tuple[tuple[int, int], ...]]:
            if row == rows:
                return 0.0, ()

            best_weight = float("-inf")
            best_assignment: tuple[tuple[int, int], ...] | None = None

            for column in range(columns):
                bit = 1 << column

                if used_columns & bit:
                    continue

                tail_weight, tail_assignment = solve(
                    row + 1,
                    used_columns | bit,
                )

                candidate_weight = matrix[row][column] + tail_weight
                candidate_assignment = (
                    (row, column),
                ) + tail_assignment

                if (
                    candidate_weight > best_weight
                    or (
                        candidate_weight == best_weight
                        and (
                            best_assignment is None
                            or candidate_assignment < best_assignment
                        )
                    )
                ):
                    best_weight = candidate_weight
                    best_assignment = candidate_assignment

            assert best_assignment is not None
            return best_weight, best_assignment

        total, assignment = solve(0, 0)
        return MatchingResult(total, assignment)

    # More rows than columns: assign every column to one unique row.
    matrix = tuple(tuple(row) for row in weights)

    @lru_cache(maxsize=None)
    def solve_columns(
        column: int,
        used_rows: int,
    ) -> tuple[float, tuple[tuple[int, int], ...]]:
        if column == columns:
            return 0.0, ()

        best_weight = float("-inf")
        best_assignment: tuple[tuple[int, int], ...] | None = None

        for row in range(rows):
            bit = 1 << row

            if used_rows & bit:
                continue

            tail_weight, tail_assignment = solve_columns(
                column + 1,
                used_rows | bit,
            )

            candidate_weight = matrix[row][column] + tail_weight
            candidate_assignment = tuple(
                sorted(
                    ((row, column),) + tail_assignment
                )
            )

            if (
                candidate_weight > best_weight
                or (
                    candidate_weight == best_weight
                    and (
                        best_assignment is None
                        or candidate_assignment < best_assignment
                    )
                )
            ):
                best_weight = candidate_weight
                best_assignment = candidate_assignment

        assert best_assignment is not None
        return best_weight, best_assignment

    total, assignment = solve_columns(0, 0)
    return MatchingResult(total, assignment)


def compare_method_units(
    left_units: Sequence[MethodUnit],
    right_units: Sequence[MethodUnit],
) -> C1Result:
    m = len(left_units)
    n = len(right_units)

    if m == 0 and n == 0:
        return C1Result(
            left_method_count=0,
            right_method_count=0,
            matched_method_count=0,
            matched_similarity_sum=0.0,
            similarity=1.0,
            assignment=(),
        )

    if m == 0 or n == 0:
        return C1Result(
            left_method_count=m,
            right_method_count=n,
            matched_method_count=0,
            matched_similarity_sum=0.0,
            similarity=0.0,
            assignment=(),
        )

    weights: list[list[float]] = []

    for left_unit in left_units:
        row: list[float] = []

        for right_unit in right_units:
            _, similarity = normalized_similarity(
                left_unit.tokens,
                right_unit.tokens,
            )
            row.append(similarity)

        weights.append(row)

    matching = maximum_weight_matching(weights)

    return C1Result(
        left_method_count=m,
        right_method_count=n,
        matched_method_count=min(m, n),
        matched_similarity_sum=matching.total_weight,
        similarity=matching.total_weight / max(m, n),
        assignment=matching.assignment,
    )


def compare_c1(left: Path, right: Path) -> C1Result:
    return compare_method_units(
        submission_method_units(left),
        submission_method_units(right),
    )
