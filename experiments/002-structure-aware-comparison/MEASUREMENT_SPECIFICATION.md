# Experiment 002 Measurement Specification

## Status

Frozen pre-measurement specification.

This document defines the Experiment 002 primary comparison conditions,
similarity functions, pair construction, output schema, and primary
descriptive analysis before primary similarity measurements are generated or
inspected.

## Frozen fixture

The primary fixture is the fixture frozen at:

`b18db86d96b0fae428cb886dcf75294610c1e409`

It contains:

- 4 provenance families;
- 4 submissions per family;
- 16 submissions total;
- 20 Java source files;
- 24 related unordered pairs;
- 96 control unordered pairs;
- 120 unordered pairs total.

The fixture must not be modified in response to measurements produced under
this specification.

## Primary comparison conditions

Experiment 002 contains exactly two primary comparison conditions:

- C0: order-sensitive abstract lexical sequence;
- C1: structure-aware method-unit matching.

Both conditions use the same frozen lexical scanner and the same primary token
normalization wherever that normalization applies.

The intended experimental contrast is global sequence order sensitivity versus
method-level structural matching.

## Java lexical scanner

A deterministic Java-oriented lexical scanner will be used.

It is required to support all syntax present in the frozen Experiment 002
fixture.

The scanner is not claimed to be a complete Java Language Specification
lexer.

The scanner must recognize at least:

- Java keywords;
- identifiers;
- integer numeric literals;
- string literals;
- character literals;
- operators;
- punctuation.

Whitespace and comments do not produce comparison tokens.

String and character literal contents are treated as single lexical tokens
before normalization.

The scanner implementation must be deterministic.

## Primary lexical normalization

The following normalization is used by both C0 and C1.

### Keywords

Java keywords are preserved by keyword value.

Examples:

`if`

`for`

`return`

`class`

`static`

### User and library identifiers

Every identifier token that is not a Java keyword is replaced by:

`<IDENT>`

This intentionally abstracts both user-defined and library identifier
spelling.

The normalization does not attempt semantic name resolution.

Therefore names such as class names, method names, variable names, `Scanner`,
`System`, `println`, and `length` are all represented as `<IDENT>` when
lexically classified as identifiers.

### Integer literals

Every integer literal is replaced by:

`<INT>`

The sign, when expressed as a separate operator token, remains an operator.

### String literals

Every string literal is replaced by:

`<STRING>`

Literal contents are not retained.

### Character literals

Every character literal is replaced by:

`<CHAR>`

Literal contents are not retained.

### Operators and punctuation

Operators and punctuation are preserved by lexical value.

Examples include:

`+`

`-`

`*`

`/`

`=`

`==`

`!=`

`<`

`>`

`++`

`(`

`)`

`{`

`}`

`[`

`]`

`;`

`,`

`.`

## Rationale for common normalization

Experiment 002 is intended to study order/structure sensitivity rather than
identifier spelling sensitivity.

Using the same normalization in C0 and C1 reduces the extent to which their
difference can be explained merely by different name abstraction.

IDENTIFIER_RENAME remains in the fixture as a transformation-specific check
that both primary conditions behave as expected under the frozen abstraction.

## Source-file discovery

For each submission, recursively discover files ending in `.java`.

Files are processed in ascending relative POSIX-path order whenever a
deterministic file order is required.

Source filenames themselves do not become lexical comparison tokens.

## C0: order-sensitive abstract lexical sequence

### Construction

For every Java source file in deterministic file order:

1. lex the complete source file;
2. discard whitespace and comments;
3. apply the primary lexical normalization;
4. append the resulting tokens to the submission sequence.

Between consecutive Java source files, append the synthetic token:

`<FILE_BOUNDARY>`

No boundary token is added before the first file or after the final file.

### C0 similarity

Let normalized token sequences be `A` and `B`.

Let `d(A, B)` be standard token-level Levenshtein edit distance with:

- insertion cost 1;
- deletion cost 1;
- substitution cost 1;
- equal-token substitution cost 0.

C0 similarity is:

`1 - d(A, B) / max(len(A), len(B))`

Edge cases:

- if both sequences are empty, similarity is `1.0`;
- if exactly one sequence is empty, similarity is `0.0`.

The result is bounded in `[0, 1]`.

C0 is intentionally order-sensitive.

## C1: structure-aware method-unit matching

### Overview

C1 represents a submission as a collection of method units rather than one
global source-order sequence.

Source declaration order does not determine unit matching.

Each extracted method becomes one structural unit.

Units are compared lexically after the same primary normalization used by C0.

Submission similarity is obtained through deterministic maximum-weight
one-to-one matching of method units, with unmatched units penalized.

## C1 structural-unit extraction

### Unit definition

A method unit is one complete Java method declaration including:

- modifiers present in source;
- return type or `void`;
- method identifier;
- parameter list;
- complete method body including outer braces.

After extraction, the complete unit text is lexed and primary lexical
normalization is applied.

The method name itself therefore becomes `<IDENT>`.

### Included methods

All method declarations with bodies in the frozen fixture are included,
including:

- `main`;
- private helper methods;
- package-private helper methods in CLASS_SPLIT helper classes.

Constructors are not required by the frozen fixture and are not primary C1
units.

### Excluded source

Tokens outside extracted method declarations do not become independent C1
units.

In particular, class declaration wrappers and import declarations are not
separate structural units.

Information contained inside method declarations remains represented.

### Extraction method

The implementation will use deterministic delimiter-aware source scanning over
the frozen Java subset.

It must correctly ignore braces and parentheses contained inside:

- comments;
- string literals;
- character literals.

For each candidate method declaration, the implementation must identify the
matching method-body closing brace by balanced delimiter scanning.

The implementation is not claimed to be a complete Java parser.

### Multiple files and classes

Methods are extracted from every Java file in the submission.

All extracted methods enter one submission-level unit collection.

The source filename and containing class name are not used to manually pair
units.

CLASS_SPLIT methods therefore remain eligible to match BASE methods even when
moved to a different class or source file.

## C1 method-unit similarity

For normalized method token sequences `U` and `V`, define unit similarity
using the same normalized token Levenshtein function as C0:

`unit_similarity(U, V) = 1 - d(U, V) / max(len(U), len(V))`

with the same empty-sequence edge rules.

The resulting unit score is in `[0, 1]`.

## C1 matching

Suppose submission A has `m` method units and submission B has `n` method
units.

Construct the complete `m x n` matrix of unit similarities.

Select a one-to-one matching that maximizes the sum of matched unit
similarities.

No method unit may appear in more than one matched pair.

The matching contains exactly:

`min(m, n)`

pairs when both submissions contain at least one unit.

### Matching algorithm

The implementation must compute the exact maximum total matching weight.

A deterministic dynamic-programming assignment implementation is permitted
because the frozen fixture contains small method-unit counts.

The implementation must not use manually supplied method correspondences.

### Tie handling

If multiple matchings have exactly the same maximum total similarity, choose
the lexicographically smallest assignment under deterministic unit indices.

Unit indices are assigned after deterministic extraction in:

1. ascending relative POSIX source-file path;
2. ascending source position within each file.

Tie handling affects auditability but must not change the maximum total
matching weight.

## C1 unmatched-unit penalty and aggregation

Let:

- `W` be the sum of similarities in the selected maximum-weight matching;
- `m` be the number of method units in submission A;
- `n` be the number of method units in submission B.

Define:

`C1_similarity = W / max(m, n)`

This means every unmatched method contributes an implicit score of zero.

Consequences:

- moving an existing method between classes/files need not be penalized merely
  for the move;
- adding or removing methods can reduce submission similarity;
- a submission cannot obtain full similarity by matching only a favorable
  subset while ignoring unmatched methods.

Edge cases:

- if `m = 0` and `n = 0`, similarity is `1.0`;
- if exactly one of `m` or `n` is zero, similarity is `0.0`.

The result is bounded in `[0, 1]`.

## C1 audit fields

For each C1 pair, record:

- left method count;
- right method count;
- matched method count;
- matched similarity sum;
- submission similarity.

The primary CSV need not contain the full unit-to-unit assignment, but the
implementation must expose deterministic matching information to tests or
diagnostic code so the result can be audited.

## Why C1 is not whole-stream sorting

C1 does not sort the complete lexical token stream.

Internal token order within each method remains order-sensitive.

Only the global correspondence among method units is made insensitive to
method declaration position and source-file placement.

This preserves an explicit structural boundary while addressing the primary
METHOD_REORDER question.

## Expected CLASS_SPLIT behavior under C1

CLASS_SPLIT moves behavior-relevant methods into an additional class while
preserving their method bodies except for reference changes required by the
move.

Because C1 aggregates methods across all source files and does not require
containing-class correspondence, moved methods remain eligible for matching.

C1 does not assume that CLASS_SPLIT must receive similarity `1.0`.

Reference changes, modifier changes, changed call syntax, or other lexical
differences inside method units may reduce unit similarity.

## Pair construction

Enumerate the 16 submissions in deterministic order by:

1. family ID;
2. variant name.

For every unordered pair `(i, j)` where `i < j`, produce one measurement for
C0 and one for C1.

This yields:

- 120 pairs per condition;
- 240 primary measurement rows total.

## Pair labels

If both submissions belong to the same provenance family:

`pair_label = related`

Otherwise:

`pair_label = control`

Expected counts per condition:

- 24 related rows;
- 96 control rows.

Expected counts across both conditions:

- 48 related rows;
- 192 control rows;
- 240 rows total.

## Variant names

The frozen variant names are:

- BASE
- CLASS_SPLIT
- IDENTIFIER_RENAME
- METHOD_REORDER

No additional primary variant is permitted.

## Primary measurement schema

The primary measurement CSV must contain these columns in this order:

1. `left_submission`
2. `right_submission`
3. `left_family`
4. `right_family`
5. `left_variant`
6. `right_variant`
7. `pair_label`
8. `condition`
9. `left_token_count`
10. `right_token_count`
11. `edit_distance`
12. `left_method_count`
13. `right_method_count`
14. `matched_method_count`
15. `matched_similarity_sum`
16. `similarity`

## Condition-specific schema values

### C0

For C0:

- `left_token_count` is populated;
- `right_token_count` is populated;
- `edit_distance` is populated;
- `left_method_count` is empty;
- `right_method_count` is empty;
- `matched_method_count` is empty;
- `matched_similarity_sum` is empty.

### C1

For C1:

- `left_token_count` is empty;
- `right_token_count` is empty;
- `edit_distance` is empty;
- `left_method_count` is populated;
- `right_method_count` is populated;
- `matched_method_count` is populated;
- `matched_similarity_sum` is populated.

## Numeric serialization

Similarity values and matched similarity sums must be serialized
deterministically.

Python's deterministic decimal string representation of computed `float`
values is acceptable for the primary CSV.

No display rounding may be applied before writing primary measurements.

## Row ordering

Rows are written in this order:

1. comparison condition in order `C0`, then `C1`;
2. left submission deterministic index;
3. right submission deterministic index.

The CSV header is written once.

## Primary analysis statistics

For each condition independently, report the related and control similarity
distributions.

At minimum report:

- count;
- mean;
- median;
- minimum;
- first quartile;
- third quartile;
- maximum.

Also report:

### Mean gap

`related_mean - control_mean`

### Empirical ordering probability

For every related score and every control score:

- contribute `1` if related > control;
- contribute `0.5` if related = control;
- contribute `0` if related < control.

The ordering probability is the mean contribution over all such
related-control score comparisons.

It is descriptive and is not a plagiarism probability.

### Exact collisions

Count similarity values exactly equal to `1.0` separately for:

- related pairs;
- control pairs.

## Transformation-specific BASE retention

For each condition and each transformed variant:

- METHOD_REORDER;
- CLASS_SPLIT;
- IDENTIFIER_RENAME;

select the four BASE-to-that-transformation pairs, one per family.

Report:

- count;
- mean;
- minimum;
- maximum;
- population standard deviation.

These transformation-specific results are primary because Experiment 002 is
explicitly concerned with structural transformations.

## C1 minus C0 paired changes

For every identical submission pair, compute:

`delta = C1_similarity - C0_similarity`

Report paired deltas separately for:

- all related pairs;
- all control pairs;
- BASE-to-METHOD_REORDER pairs;
- BASE-to-CLASS_SPLIT pairs;
- BASE-to-IDENTIFIER_RENAME pairs.

At minimum report mean delta for each group.

No inferential significance test is required for the primary experiment.

## Primary interpretation

The analysis must not label C1 an improvement solely because C1 increases
related similarity.

Interpretation must jointly consider:

- METHOD_REORDER retention;
- CLASS_SPLIT retention;
- IDENTIFIER_RENAME retention;
- control similarity;
- related/control mean gap;
- empirical ordering probability;
- exact control collisions.

A rise in related similarity accompanied by comparable or greater rise in
control similarity is a tradeoff, not automatically an improvement.

## No classification threshold

No plagiarism classification threshold will be selected from the Experiment
002 primary fixture.

No primary measurement is interpreted as a plagiarism probability.

The experiment evaluates deterministic similarity behavior under controlled
transformations and controls.

## Implementation freeze

The implementation of:

- lexical scanning;
- lexical normalization;
- C0 construction;
- method extraction;
- method-unit similarity;
- exact assignment;
- deterministic tie handling;
- C1 aggregation;
- pair enumeration;
- CSV serialization;

must be tested and committed before the primary measurement run.

Implementation tests may use synthetic examples and the frozen fixture for
structural validation.

They must not be used to tune rules based on observed primary similarity
distributions.

## Measurement runner freeze

The primary measurement runner must be committed before its canonical primary
output is interpreted.

The runner must identify the frozen fixture and produce the complete 240-row
measurement CSV deterministically.

## Reproducibility

The canonical primary measurement file must be identified by SHA-256.

The primary measurement must be rerun from the same frozen implementation and
fixture state.

Where practical, the rerun must reproduce the canonical CSV byte-for-byte and
therefore reproduce its SHA-256 hash.

## Change control

After primary similarity results are inspected, the following may not be
changed in response to those results:

- C0 normalization;
- C0 sequence construction;
- C0 similarity;
- C1 method-unit definition;
- C1 extraction;
- C1 normalization;
- C1 unit similarity;
- C1 matching;
- C1 unmatched-unit penalty;
- C1 aggregation;
- pair labels;
- primary statistics.

A genuine implementation defect must be documented and versioned explicitly,
and affected measurements must be rerun transparently.

## Success and failure interpretation

Experiment 002 does not define a single binary success threshold.

Evidence supporting the usefulness of C1 would consist of increased robustness
to METHOD_REORDER and/or CLASS_SPLIT while retaining meaningful distinction
between related and control pairs under the frozen descriptive measures.

Evidence against the usefulness of C1 would include cases where structural
retention gains are absent, inconsistent, or accompanied by sufficient growth
in control similarity that provenance-family distinction is weakened.

Mixed results are valid experimental outcomes and must be reported as such.
