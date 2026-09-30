# Experiment 001 — Primary Fixture Specification

## Status

Pre-implementation fixture specification.

This document defines the four primary provenance families before their Java
implementations, transformed variants, representations, or similarity results
are created.

The families are intentionally small enough for manual inspection while
differing in computational task and expected source structure.

The labels `related` and `control` used later describe experimental provenance
only.

## Common execution model

Each base program:

- is written in Java;
- reads input from standard input;
- writes deterministic output to standard output;
- requires no network access;
- requires no external libraries;
- uses no randomness;
- uses no filesystem state;
- must terminate on every declared fixture input.

Output formatting is part of the declared behavior.

---

## Family A — Number Summary

### Purpose

Process a sequence of integers and report basic numerical properties.

### Input

The first line contains integer `n`.

The second line contains exactly `n` space-separated integers.

For the primary fixture:

- `1 <= n <= 20`;
- each value is between `-1000` and `1000`.

### Output

Print four lines in this exact order:

1. `sum=<value>`
2. `min=<value>`
3. `max=<value>`
4. `even=<value>`

`even` is the number of input values divisible by two.

### Declared test cases

#### A1

Input:

    5
    3 8 -2 7 4

Expected output:

    sum=20
    min=-2
    max=8
    even=3

#### A2

Input:

    4
    -5 -3 -9 -1

Expected output:

    sum=-18
    min=-9
    max=-1
    even=0

#### A3

Input:

    1
    6

Expected output:

    sum=6
    min=6
    max=6
    even=1

---

## Family B — Word Profile

### Purpose

Analyze a single text line using character and word properties.

### Input

One non-empty line of ASCII text.

Words are maximal sequences separated by one or more spaces.

For the primary fixture, inputs contain letters and spaces only.

### Output

Print three lines in this exact order:

1. `words=<value>`
2. `vowels=<value>`
3. `longest=<value>`

Vowels are `a`, `e`, `i`, `o`, and `u`, case-insensitively.

`longest` is the length of the longest word.

### Declared test cases

#### B1

Input:

    code similarity matters

Expected output:

    words=3
    vowels=8
    longest=10

#### B2

Input:

    Java IS fun

Expected output:

    words=3
    vowels=4
    longest=4

#### B3

Input:

    rhythm

Expected output:

    words=1
    vowels=0
    longest=6

---

## Family C — Run-Length Encoder

### Purpose

Compress consecutive repeated characters using run-length encoding.

### Input

One non-empty string consisting only of uppercase English letters `A-Z`.

The maximum primary-fixture input length is 100 characters.

### Output

For every maximal consecutive run, output the character followed immediately
by the run length.

No separators are inserted between runs.

Print exactly one output line.

### Declared test cases

#### C1

Input:

    AAABBCCCCD

Expected output:

    A3B2C4D1

#### C2

Input:

    XYZ

Expected output:

    X1Y1Z1

#### C3

Input:

    AAAAA

Expected output:

    A5

---

## Family D — Grid Neighborhood Counter

### Purpose

Count cells in a binary grid according to their orthogonal neighborhoods.

### Input

The first line contains integers `r` and `c`.

The following `r` lines each contain exactly `c` characters, each either
`0` or `1`.

For the primary fixture:

- `1 <= r <= 10`;
- `1 <= c <= 10`.

### Output

For each cell containing `1`, compute how many orthogonally adjacent cells also
contain `1`.

Orthogonal neighbors are:

- above;
- below;
- left;
- right.

Print two lines:

1. `ones=<value>`
2. `links=<value>`

`ones` is the number of cells containing `1`.

`links` is the number of unordered orthogonally adjacent pairs in which both
cells contain `1`.

Each adjacent pair is counted exactly once.

### Declared test cases

#### D1

Input:

    3 3
    110
    010
    011

Expected output:

    ones=5
    links=4

#### D2

Input:

    2 2
    10
    01

Expected output:

    ones=2
    links=0

#### D3

Input:

    1 4
    1111

Expected output:

    ones=4
    links=3

---

## Family independence

Families A-D are separate experimental provenance families.

No family is derived by transforming another family's source code.

Later controlled transformations are performed only within each family.

Therefore:

- same-family BASE/transformation pairs are labelled `related`;
- cross-family pairs are labelled `control`.

These labels encode fixture construction and do not imply anything about
authorship or misconduct.

## Transformation rule

Each family will later receive the six transformations frozen in the
Experiment 001 protocol:

- IDENTIFIER_RENAME
- METHOD_REORDER
- CLASS_RENAME
- FILE_RENAME
- DEAD_CODE
- CLASS_SPLIT

The transformation must preserve the declared tested behavior of its base
family on all declared fixture tests.

No transformation may be selected, removed, or redesigned based solely on
observed similarity results.

## Freeze rule

Once this specification is committed, changes to task definitions, declared
inputs, expected outputs, or provenance relationships require an explicit
documented correction.

Unexpected similarity behavior is not itself grounds for changing the fixture.