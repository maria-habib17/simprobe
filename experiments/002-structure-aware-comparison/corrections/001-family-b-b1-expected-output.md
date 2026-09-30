# Correction 001: Family B B1 Expected Output

## Status

Pre-measurement fixture-specification correction.

## Discovery

During initial validation of the Experiment 002 BASE implementations, Family B
test B1 failed.

The frozen fixture specification gave this expected output:

`sameStart=1`

for input:

`Code can change`

The BASE implementation produced:

`sameStart=2`

No Experiment 002 similarity measurements had been generated or inspected.

## Defect

The expected value in the fixture specification was incorrect under the
specification's own definition of `sameStart`.

`sameStart` is the number of adjacent word pairs whose first letters are equal
ignoring ASCII case.

For:

`Code can change`

the adjacent pairs are:

- `Code` / `can`
- `can` / `change`

Both pairs begin with `c` ignoring case.

Therefore the correct value is:

`sameStart=2`

## Correction

Family B test B1 expected output is corrected from:

`sameStart=1`

to:

`sameStart=2`

No program behavior definition, provenance family, transformation, comparison
condition, representation rule, similarity rule, or measurement result was
changed.

This correction occurred before the BASE implementations were committed and
before any Experiment 002 similarity measurements were generated.
