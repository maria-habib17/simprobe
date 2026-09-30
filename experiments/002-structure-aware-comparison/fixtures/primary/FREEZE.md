# Experiment 002 Primary Fixture Freeze

## Status

Frozen primary fixture.

## Fixture provenance

The Experiment 002 primary fixture was completed before implementation of the
Experiment 002 comparison conditions and before generation or inspection of
primary similarity measurements.

The fixture contains four independent provenance families:

- family-a
- family-b
- family-c
- family-d

Each family contains exactly four submissions:

- BASE
- METHOD_REORDER
- CLASS_SPLIT
- IDENTIFIER_RENAME

Total submissions: 16.

Total unordered submission pairs: 120.

Pair composition:

- related same-family pairs: 24;
- control cross-family pairs: 96.

These pair counts apply independently to each comparison condition.

## Source-file composition

The fixture contains 20 Java source files.

Each BASE submission contains one Java source file.

Each METHOD_REORDER submission contains one Java source file.

Each IDENTIFIER_RENAME submission contains one Java source file.

Each CLASS_SPLIT submission contains exactly two Java source files.

## Behavioral validation

Before fixture freeze:

- every submission compiled independently;
- every submission passed all three declared tests for its family;
- 48 of 48 declared test executions passed;
- generated `.class` files were removed.

Passing tests are evidence of behavior on the declared cases and are not a
formal proof of semantic equivalence.

## Structural validation

Before fixture freeze:

- every METHOD_REORDER variant materially reordered helper declarations;
- every CLASS_SPLIT variant contained exactly one additional top-level helper
  class;
- every CLASS_SPLIT helper class was used during normal execution;
- every IDENTIFIER_RENAME variant used a renamed public entry class;
- the fixture contained exactly 16 submission directories and 20 Java source
  files.

## Pre-freeze corrections

Two fixture-specification defects were discovered during BASE validation,
before any Experiment 002 similarity measurements were generated.

### Correction 001

Family B test B1 originally specified `sameStart=1` for:

`Code can change`

Under the frozen definition both adjacent pairs have the same initial letter
ignoring case, so the correct expected value is `sameStart=2`.

The correction was recorded separately before BASE implementation freeze.

### Correction 002

Family C test C1 originally specified `weighted=50` for:

`111223`

Under the frozen positional-weight definition the correct value is
`weighted=42`.

The correction was recorded separately before BASE implementation freeze.

Neither correction changed the computational task definitions or any
similarity measurement rule.

## Relevant commits

Experiment 002 protocol:

`bcff8a7faf96b45b8679f3c8b49a26beba79311d`

Primary fixture specification:

`6db92737e772762ece0ae24b41b781ade7dc401f`

Family B B1 correction:

`8e0654b`

Family C C1 correction:

`0e49558`

BASE implementations:

`283646abb664e100671dafcc05c976d7da60d24d`

Controlled transformations:

`cae46cc744e3ff68843a2f579ecc70fc065616a5`

## Freeze rule

From this point onward, the Experiment 002 primary fixture is frozen.

Primary fixture source code, provenance-family membership, transformation
membership, declared behavioral tests, and pair labels must not be changed in
response to similarity results.

If a genuine fixture defect is discovered later, it must be:

1. documented explicitly;
2. committed as a versioned correction;
3. revalidated;
4. followed by a transparent corrected measurement run.

Any affected earlier measurement run must remain identifiable.

## Next stage

The next Experiment 002 artifact is the measurement specification.

It must freeze, before primary measurements:

- C0 order-sensitive baseline representation;
- C0 similarity function;
- C1 structural-unit extraction;
- C1 lexical normalization;
- C1 unit matching;
- C1 unmatched-unit treatment;
- C1 score aggregation;
- deterministic tie handling;
- multi-file handling;
- measurement output schema;
- primary analysis statistics.

No primary Experiment 002 similarity results may be inspected before that
measurement specification and its implementation are appropriately frozen.
