# Correction 002: Family C C1 Expected Output

## Status

Pre-measurement fixture-specification correction.

## Discovery

During validation of the Experiment 002 BASE implementations, Family C test C1
failed.

For input:

`111223`

the frozen fixture specification expected:

`weighted=50`

The BASE implementation produced:

`weighted=42`

No Experiment 002 similarity measurements had been generated or inspected.

## Defect

The expected value was arithmetically incorrect under the frozen definition of
`weighted`.

The specification defines `weighted` as the sum of each numeric digit value
multiplied by its one-based position.

For `111223`:

- position 1: `1 * 1 = 1`
- position 2: `1 * 2 = 2`
- position 3: `1 * 3 = 3`
- position 4: `2 * 4 = 8`
- position 5: `2 * 5 = 10`
- position 6: `3 * 6 = 18`

The total is:

`1 + 2 + 3 + 8 + 10 + 18 = 42`

Therefore the correct expected value is:

`weighted=42`

## Correction

Family C test C1 expected output is corrected from:

`weighted=50`

to:

`weighted=42`

No behavioral definition, provenance family, transformation, comparison
condition, representation rule, similarity rule, or measurement result was
changed.

This correction occurred before the BASE implementations were committed and
before any Experiment 002 similarity measurements were generated.
