from simprobe.representations.java import (
    TokenKind,
    r0,
    r1,
    r2,
    r3,
    r4,
    r5,
    r6,
    scan_java,
)


def test_scanner_removes_comments_and_whitespace() -> None:
    source = """
    int value = 1; // line comment
    /* block comment */
    value++;
    """

    assert r0(scan_java(source)) == (
        "int",
        "value",
        "=",
        "1",
        ";",
        "value",
        "++",
        ";",
    )


def test_scanner_preserves_quoted_literals_as_single_tokens() -> None:
    tokens = scan_java(r'''String s = "a // b"; char c = '\n';''')

    strings = [token for token in tokens if token.kind is TokenKind.STRING]
    characters = [token for token in tokens if token.kind is TokenKind.CHARACTER]

    assert [token.value for token in strings] == ['"a // b"']
    assert [token.value for token in characters] == [r"'\n'"]


def test_r0_and_r1_are_identical() -> None:
    tokens = scan_java("int answer = 42;")
    assert r0(tokens) == r1(tokens)


def test_r2_abstracts_non_keyword_identifiers() -> None:
    tokens = scan_java("int answer = Math.max(left, right);")

    assert r2(tokens) == (
        "int",
        "<IDENT>",
        "=",
        "<IDENT>",
        ".",
        "<IDENT>",
        "(",
        "<IDENT>",
        ",",
        "<IDENT>",
        ")",
        ";",
    )


def test_r3_abstracts_literal_categories() -> None:
    tokens = scan_java(
        """int n = 12; double x = 1.5; char c = 'z';
        String s = "hi"; boolean b = true; Object o = null;"""
    )

    representation = r3(tokens)

    assert "<INT_LITERAL>" in representation
    assert "<FLOAT_LITERAL>" in representation
    assert "<CHAR_LITERAL>" in representation
    assert "<STRING_LITERAL>" in representation
    assert "<BOOLEAN_LITERAL>" in representation
    assert "<NULL_LITERAL>" in representation


def test_r4_fixed_classification_example() -> None:
    tokens = scan_java(
        "class Example { Result build(Input value) { return new Result(value); } }"
    )

    assert r4(tokens) == (
        "class",
        "<TYPE_IDENT>",
        "{",
        "<TYPE_IDENT>",
        "<METHOD_IDENT>",
        "(",
        "<TYPE_IDENT>",
        "<IDENT>",
        ")",
        "{",
        "return",
        "new",
        "<TYPE_IDENT>",
        "(",
        "<IDENT>",
        ")",
        ";",
        "}",
        "}",
    )


def test_r5_fixed_structural_example() -> None:
    tokens = scan_java("class A { int f(int x) { if (x > 1) return x + 1; } }")

    assert r5(tokens) == (
        "<CLASS_DECL>",
        "<BLOCK_OPEN>",
        "<METHOD_LIKE>",
        "<PAREN_OPEN>",
        "<PAREN_CLOSE>",
        "<BLOCK_OPEN>",
        "<IF>",
        "<PAREN_OPEN>",
        "<COMPARE>",
        "<LITERAL>",
        "<PAREN_CLOSE>",
        "<RETURN>",
        "<ARITH>",
        "<LITERAL>",
        "<STATEMENT_END>",
        "<BLOCK_CLOSE>",
        "<BLOCK_CLOSE>",
    )


def test_r6_maps_and_collapses_consecutive_symbols() -> None:
    structural = (
        "<CLASS_DECL>",
        "<METHOD_LIKE>",
        "<PAREN_OPEN>",
        "<PAREN_CLOSE>",
        "<ARITH>",
        "<ASSIGN>",
        "<STATEMENT_END>",
        "<COMMA>",
        "<FILE_BOUNDARY>",
        "<LITERAL>",
    )

    assert r6(structural) == (
        "<DECL>",
        "<GROUP>",
        "<OP>",
        "<SEP>",
        "<FILE_BOUNDARY>",
        "<VALUE>",
    )
