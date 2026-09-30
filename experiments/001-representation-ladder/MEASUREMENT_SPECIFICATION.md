# Experiment 001 Measurement Implementation Specification

## Status

Pre-measurement implementation specification.

This document fixes the operational representation and similarity rules used
for the Experiment 001 primary measurements.

The primary fixture was frozen before this specification was created.

No primary similarity measurements are to be generated or inspected until
this specification is committed.

## Unit of comparison

A submission is one complete program directory.

A submission may contain one or more `.java` files.

For representations that consume source text or source-derived sequences,
Java files are processed independently in ascending ordinal order of their
relative POSIX-style path within the submission.

The per-file representation sequences are joined using the synthetic token:

`<FILE_BOUNDARY>`

The boundary token is inserted only between files, never before the first file
or after the final file.

File names themselves are not emitted into the representation.

## Lexical scanner

R0 through R4 use one deterministic Java-oriented lexical scanner implemented
inside SimProbe.

The scanner recognizes:

- Java identifiers and keywords
- integer literals
- floating-point literals
- character literals
- string literals
- operators
- separators and punctuation

Line comments and block comments are recognized and discarded.

Whitespace separates tokens where necessary but is not emitted.

Quoted string and character literals are scanned as single tokens, including
their delimiters and escape sequences.

The scanner is intended for the frozen Experiment 001 fixture and is not
claimed to be a complete Java Language Specification lexer.

All 32 frozen primary Java source files must scan successfully before primary
measurements are accepted.

## R0 - Raw lexical tokens

R0 is the lexical token sequence after comments and whitespace have been
excluded.

Token values are preserved exactly.

Examples include:

- `public`
- `NumberSummary`
- `(`
- `Scanner`
- `"sum="`
- `20`

No identifier or literal abstraction is performed.

## R1 - Canonical lexical stream

For Experiment 001, R1 is intentionally identical to R0.

The scanner already excludes comments and formatting whitespace, so no
additional canonicalization is applied.

R0 and R1 therefore provide an explicit expected-equivalence check in this
experiment.

## R2 - Identifier abstraction

R2 begins with R1.

Every token classified as a Java identifier that is not a Java keyword is
replaced with:

`<IDENT>`

Java keywords remain distinct.

Literals, operators, separators, and punctuation remain unchanged.

No attempt is made at R2 to distinguish user-defined identifiers from names
originating in the Java standard library. All non-keyword identifier tokens
receive the same abstraction.

## R3 - Literal abstraction

R3 begins with R2.

Literal tokens are replaced by these categories:

- integer literal -> `<INT_LITERAL>`
- floating-point literal -> `<FLOAT_LITERAL>`
- character literal -> `<CHAR_LITERAL>`
- string literal -> `<STRING_LITERAL>`
- `true` or `false` -> `<BOOLEAN_LITERAL>`
- `null` -> `<NULL_LITERAL>`

The Java tokens `true`, `false`, and `null` are treated as literal categories
at R3 even though the lexical scanner recognizes them as reserved words.

Literal values are not retained.

All other R2 tokens are unchanged.

## R4 - Name and type abstraction

R4 begins with the R1 lexical stream rather than R3 so that identifier
categories can be assigned before identifier spelling is discarded.

Each non-keyword identifier token is classified using deterministic local
lexical context into one of the following categories:

- `<TYPE_IDENT>`
- `<METHOD_IDENT>`
- `<IDENT>`

An identifier is `<TYPE_IDENT>` when at least one of these rules applies:

1. it immediately follows `class`, `interface`, `enum`, `record`, `extends`,
   `implements`, `new`, or `instanceof`;
2. it is the identifier immediately preceding another identifier in a
   declaration-like sequence;
3. it begins with an uppercase ASCII letter.

An identifier is `<METHOD_IDENT>` when its next non-comment lexical token is
`(` and it was not classified as `<TYPE_IDENT>`.

Every remaining non-keyword identifier is `<IDENT>`.

After identifier classification, literals use the same abstraction categories
as R3.

Keywords, operators, separators, and punctuation remain distinct.

These rules are lexical heuristics. They are fixed for Experiment 001 and are
not changed in response to primary results.

## R5 - Structural syntax

R5 discards identifier spellings and literal values and emits a
syntax-oriented sequence from the lexical stream.

The emitted structural vocabulary consists of:

- `<CLASS_DECL>` for `class`
- `<IF>` for `if`
- `<ELSE>` for `else`
- `<FOR>` for `for`
- `<WHILE>` for `while`
- `<RETURN>` for `return`
- `<CONTINUE>` for `continue`
- `<BREAK>` for `break`
- `<NEW>` for `new`
- `<METHOD_LIKE>` for an identifier followed by `(`
- `<BLOCK_OPEN>` for `{`
- `<BLOCK_CLOSE>` for `}`
- `<PAREN_OPEN>` for `(`
- `<PAREN_CLOSE>` for `)`
- `<BRACKET_OPEN>` for `[`
- `<BRACKET_CLOSE>` for `]`
- `<STATEMENT_END>` for `;`
- `<COMMA>` for `,`
- `<ASSIGN>` for `=`
- `<COMPARE>` for `==`, `!=`, `<`, `>`, `<=`, or `>=`
- `<ARITH>` for `+`, `-`, `*`, `/`, or `%`
- `<LOGIC>` for `&&`, `||`, or `!`
- `<INC_DEC>` for `++` or `--`
- `<MEMBER_ACCESS>` for `.`
- `<LITERAL>` for any literal

All other lexical tokens are omitted at R5.

Structural symbols are emitted in original source order.

R5 is a deterministic syntax proxy, not a full Java AST.

## R6 - Aggressive structural abstraction

R6 begins with R5 and maps the R5 vocabulary into a smaller alphabet:

- `<CLASS_DECL>` -> `<DECL>`
- `<METHOD_LIKE>` -> `<DECL>`
- `<IF>`, `<ELSE>`, `<FOR>`, `<WHILE>` -> `<CONTROL>`
- `<RETURN>`, `<CONTINUE>`, `<BREAK>` -> `<FLOW>`
- `<NEW>` -> `<OP>`
- `<ASSIGN>`, `<COMPARE>`, `<ARITH>`, `<LOGIC>`, `<INC_DEC>`,
  `<MEMBER_ACCESS>` -> `<OP>`
- `<BLOCK_OPEN>`, `<BLOCK_CLOSE>` -> `<BLOCK>`
- `<PAREN_OPEN>`, `<PAREN_CLOSE>`, `<BRACKET_OPEN>`,
  `<BRACKET_CLOSE>` -> `<GROUP>`
- `<STATEMENT_END>`, `<COMMA>` -> `<SEP>`
- `<LITERAL>` -> `<VALUE>`

Consecutive identical R6 symbols are collapsed to one symbol.

`<FILE_BOUNDARY>` is preserved and is never collapsed with neighboring
symbols.

R6 intentionally discards substantial information and represents the
high-invariance, high-degeneracy end of the ladder.

## Similarity function

Similarity is computed on representation token sequences using normalized
Levenshtein edit similarity.

For token sequences A and B:

`similarity(A, B) = 1 - distance(A, B) / max(len(A), len(B))`

where `distance` is Levenshtein edit distance with:

- insertion cost 1
- deletion cost 1
- substitution cost 1
- exact token equality cost 0

If both sequences are empty, similarity is defined as `1.0`.

If exactly one sequence is empty, similarity is `0.0`.

No token weighting is used.

No threshold is applied when producing raw primary measurements.

Scores are stored as full Python floating-point values and may be rounded only
for human-readable presentation.

## Pair construction

For each representation stage R0 through R6, similarities are measured for
all unordered pairs of the 28 primary submissions.

Each pair is emitted exactly once.

Pair labels are assigned from fixture provenance:

- same family, different submissions -> `related`
- different families -> `control`

Pairs are ordered deterministically by the lexicographic submission IDs.

The submission ID format is:

`<family>/<variant>`

Examples:

- `family-a/BASE`
- `family-a/IDENTIFIER_RENAME`
- `family-d/CLASS_SPLIT`

## Primary output schema

The primary measurement table contains at least:

- `left_submission`
- `right_submission`
- `left_family`
- `right_family`
- `left_variant`
- `right_variant`
- `pair_label`
- `representation`
- `left_length`
- `right_length`
- `edit_distance`
- `similarity`

The raw measurement table is retained separately from summaries or plots.

## Determinism

Given identical fixture bytes and identical SimProbe implementation, repeated
runs must produce identical:

- submission ordering
- file ordering
- representation token sequences
- representation lengths
- edit distances
- similarity scores
- pair labels
- output row ordering

## Pre-measurement validation

Before generating primary similarity results, implementation tests must cover
at least:

1. comment removal;
2. whitespace exclusion;
3. string and character literal preservation during lexical scanning;
4. R0/R1 equality;
5. R2 identifier abstraction;
6. R3 literal abstraction;
7. fixed R4 classification examples;
8. fixed R5 structural emission examples;
9. R6 category mapping and consecutive-symbol collapse;
10. deterministic multi-file ordering and file boundaries;
11. known Levenshtein distances;
12. empty-sequence similarity behavior;
13. pair labeling;
14. exactly 28 primary submissions discovered;
15. exactly 378 unordered submission pairs;
16. exactly 2,646 primary measurement rows across seven representations.

The final three counts follow from:

- 28 submissions;
- `28 * 27 / 2 = 378` unordered pairs;
- `378 * 7 = 2,646` representation-specific measurements.

## Change control

Once this specification is committed, it is part of the pre-measurement
experimental record.

Implementation defects may be corrected if they prevent the implementation
from following this specification. Such corrections must be documented and
versioned.

The representation rules, similarity function, fixture membership, pair
labels, or other measurement definitions must not be changed in response to
observed primary similarity results. Any such alternative belongs in a
separately identified follow-up analysis.
