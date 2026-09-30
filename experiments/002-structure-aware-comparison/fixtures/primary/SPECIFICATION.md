# Experiment 002 Primary Fixture Specification

## Status

Pre-implementation primary fixture specification.

This specification resolves the primary fixture design required by the frozen
Experiment 002 protocol.

No primary similarity measurements may be generated before the complete
fixture and measurement specification are frozen.

## Fixture size

The Experiment 002 primary fixture contains four independent provenance
families.

Each family contains exactly four submissions:

- BASE
- METHOD_REORDER
- CLASS_SPLIT
- IDENTIFIER_RENAME

Therefore the primary fixture contains:

- 4 provenance families;
- 4 submissions per family;
- 16 submissions total;
- 120 unordered submission pairs.

No additional primary transformation is included.

For pair labeling:

- same-family pairs are `related`;
- cross-family pairs are `control`.

With four families of four submissions:

- related unordered pairs: 24;
- control unordered pairs: 96;
- total unordered pairs: 120.

These counts apply independently to every frozen comparison condition.

## Common execution rules

All fixture programs are Java command-line programs.

Programs:

- read from standard input;
- write to standard output;
- are deterministic;
- use no network access;
- use no filesystem access;
- use no random behavior;
- require no external libraries;
- terminate for all declared primary inputs.

Output formatting, including line order and punctuation, is part of observable
behavior.

Each submission directory is one complete program submission.

A submission may contain multiple `.java` files.

## Structural fixture requirements

Experiment 002 specifically studies method reordering and class splitting.

Therefore every BASE submission must contain:

- one public top-level entry class;
- `main`;
- at least four behavior-relevant user-defined helper methods in addition to
  `main`;
- calls among those helpers sufficient to make declaration reordering a
  material source-order transformation;
- functionality that can be moved into an additional class for CLASS_SPLIT
  without changing the declared external behavior.

METHOD_REORDER must materially change helper declaration order while preserving
method bodies and intended behavior.

CLASS_SPLIT must move behavior-relevant functionality into an additional class.
The additional class must be used during normal execution.

IDENTIFIER_RENAME must materially rename user-defined identifiers.

## Family independence

Families A through D are treated as independent provenance families.

They implement different computational tasks and are not transformations of
one another.

Cross-family pairs are controls even when generic Java syntax, library calls,
or programming idioms overlap.

## Family A: Score Statistics

### Purpose

Read a sequence of integer scores and report several statistics.

### Input

The first line contains integer `n`.

The second line contains exactly `n` space-separated integers.

Primary-domain constraints:

- `1 <= n <= 20`;
- every score is in `[-1000, 1000]`.

### Output

Exactly four lines:

`total=<value>`

`average=<value>`

`above=<value>`

`range=<value>`

Definitions:

- `total` is the sum of all scores;
- `average` is integer division of `total` by `n` using Java integer division;
- `above` is the number of scores strictly greater than `average`;
- `range` is maximum score minus minimum score.

### Declared tests

#### A1

Input:

`5`
`10 20 30 40 50`

Expected output:

`total=150`
`average=30`
`above=2`
`range=40`

#### A2

Input:

`4`
`-8 -2 -5 -1`

Expected output:

`total=-16`
`average=-4`
`above=2`
`range=7`

#### A3

Input:

`1`
`7`

Expected output:

`total=7`
`average=7`
`above=0`
`range=0`

## Family B: Sentence Shape

### Purpose

Analyze the lengths and initial letters of words in one line of text.

### Input

One nonempty line containing ASCII letters and single spaces between words.

Primary-domain constraints:

- letters are `A-Z` or `a-z`;
- words are separated by exactly one space;
- no leading or trailing spaces;
- at least one word is present.

### Output

Exactly four lines:

`words=<value>`

`characters=<value>`

`longest=<value>`

`sameStart=<value>`

Definitions:

- `words` is the number of words;
- `characters` is the number of letters, excluding spaces;
- `longest` is the maximum word length;
- `sameStart` is the number of adjacent word pairs whose first letters are
  equal ignoring ASCII case.

### Declared tests

#### B1

Input:

`Code can change`

Expected output:

`words=3`
`characters=13`
`longest=6`
`sameStart=1`

#### B2

Input:

`Java tools help students`

Expected output:

`words=4`
`characters=21`
`longest=8`
`sameStart=0`

#### B3

Input:

`Alpha apple Atom`

Expected output:

`words=3`
`characters=14`
`longest=5`
`sameStart=2`

## Family C: Digit Run Analyzer

### Purpose

Analyze contiguous runs in a nonempty decimal digit string.

### Input

One line containing only characters `0` through `9`.

Primary-domain constraints:

- length is between 1 and 100 inclusive.

### Output

Exactly four lines:

`runs=<value>`

`longest=<value>`

`changes=<value>`

`weighted=<value>`

Definitions:

- a run is a maximal contiguous sequence of the same digit;
- `runs` is the number of runs;
- `longest` is the length of the longest run;
- `changes` is the number of positions at which a digit differs from the
  immediately preceding digit;
- `weighted` is the sum, over all characters, of the numeric digit value
  multiplied by its one-based position in the string.

### Declared tests

#### C1

Input:

`111223`

Expected output:

`runs=3`
`longest=3`
`changes=2`
`weighted=50`

#### C2

Input:

`507`

Expected output:

`runs=3`
`longest=1`
`changes=2`
`weighted=26`

#### C3

Input:

`9999`

Expected output:

`runs=1`
`longest=4`
`changes=0`
`weighted=90`

## Family D: Binary Grid Perimeter

### Purpose

Measure occupied cells and orthogonal boundary properties of a binary grid.

### Input

The first line contains integers `r` and `c`.

The next `r` lines each contain exactly `c` characters, each `0` or `1`.

Primary-domain constraints:

- `1 <= r <= 10`;
- `1 <= c <= 10`.

### Output

Exactly four lines:

`ones=<value>`

`horizontal=<value>`

`vertical=<value>`

`perimeter=<value>`

Definitions:

- `ones` is the number of cells containing `1`;
- `horizontal` is the number of horizontally adjacent unordered `1`-`1`
  pairs;
- `vertical` is the number of vertically adjacent unordered `1`-`1` pairs;
- `perimeter` is the number of cell edges separating a `1` cell from either a
  `0` cell or the outside of the grid.

Equivalently for validation:

`perimeter = 4 * ones - 2 * horizontal - 2 * vertical`

### Declared tests

#### D1

Input:

`3 3`
`110`
`010`
`011`

Expected output:

`ones=5`
`horizontal=2`
`vertical=2`
`perimeter=12`

#### D2

Input:

`2 2`
`10`
`01`

Expected output:

`ones=2`
`horizontal=0`
`vertical=0`
`perimeter=8`

#### D3

Input:

`1 4`
`1111`

Expected output:

`ones=4`
`horizontal=3`
`vertical=0`
`perimeter=10`

## BASE implementation requirements

BASE implementations must be written before transformed variants.

Each BASE must use at least four behavior-relevant helper methods in addition
to `main`.

Helpers should represent meaningful subcomputations rather than artificial
empty wrappers.

The implementation should remain small enough for deterministic inspection and
measurement.

No BASE implementation may be changed in response to similarity measurements.

A genuine pre-measurement implementation defect may be corrected and
documented before fixture freeze.

## METHOD_REORDER construction

For each family, METHOD_REORDER is derived from BASE.

Requirements:

- preserve the entry class name;
- preserve method names;
- preserve method parameter names;
- preserve local identifiers;
- preserve method bodies;
- preserve literals;
- preserve operators;
- preserve calls;
- preserve intended observable behavior;
- materially alter declaration order of behavior-relevant helper methods.

Whitespace changes incidental to constructing the variant are permitted but
must not be the intended transformation.

## CLASS_SPLIT construction

For each family, CLASS_SPLIT is derived from BASE.

Requirements:

- preserve intended observable behavior;
- retain the original public entry class;
- add exactly one additional user-defined top-level class;
- move at least two behavior-relevant helper methods from the BASE entry class
  into the additional class;
- normal execution must call functionality in the additional class;
- update references as required;
- do not intentionally change computational logic beyond the structural move.

The additional class may reside in a separate Java source file.

## IDENTIFIER_RENAME construction

For each family, IDENTIFIER_RENAME is derived from BASE.

Requirements:

- rename the public entry class and corresponding Java source filename;
- rename all behavior-relevant user-defined helper methods;
- materially rename method parameters and local variables where present;
- update all references consistently;
- do not intentionally alter literals;
- do not intentionally alter operators;
- do not intentionally alter control flow;
- do not intentionally alter method declaration order;
- preserve intended observable behavior.

Java language/library identifiers are not intentionally renamed.

## Behavioral validation requirement

Before the primary fixture is frozen:

1. compile every submission independently;
2. execute all three declared tests for its family;
3. compare standard output exactly with the expected output;
4. require every execution to pass;
5. remove generated `.class` files from the fixture tree.

With 16 submissions and three tests per submission, successful validation
requires 48 declared test executions.

Passing these tests is evidence only for the declared behavior.

## Fixture freeze

After all 16 submissions pass validation, the complete fixture will be
committed as a frozen primary fixture.

After that freeze, fixture contents may not be changed in response to
similarity measurements.

A genuine defect may be corrected only through an explicit documented,
versioned correction followed by transparent revalidation and rerun.

## Measurement boundary

No Experiment 002 primary similarity measurements may be generated or
inspected during fixture construction.

The exact order-sensitive baseline, structure-aware representation, structural
unit extraction, matching rule, aggregation rule, output schema, and
similarity calculation will be specified and committed separately after the
fixture is frozen and before primary measurements.
