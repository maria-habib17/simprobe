# Fixture Correction 002 - Dead-Code Fixture Omission

## Status

Post-primary-measurement fixture correction.

## Discovery

After the first Experiment 001 primary measurement run was generated and its
structural and reproducibility checks had passed, descriptive analysis showed
that every BASE/DEAD_CODE pair had similarity `1.0` at R0 through R6.

Because R0 preserves lexical token values, an actually inserted dead-code
helper cannot leave the R0 token sequence identical to BASE.

A subsequent diagnostic confirmed that the frozen DEAD_CODE submissions did
not contain the dead-code additions documented in
`fixtures/primary/DEAD_CODE.md`.

The first primary run had already been inspected when this defect was
discovered.

## Original primary run

The affected original primary run is permanently identified by:

- pre-measurement implementation/runner commit:
  `4042b61b78244b9001a0713525756e8b76beb9d2`
- primary-run record commit:
  `c58827dd9680f4111981473d16a33c9f4130a694`
- canonical output SHA-256:
  `38D2C00E4CD78EAF153C85B6C5AFBAEE689B0256A4ECBD5019DECC681FC91C4B`

That run is retained as the original primary run and is not silently replaced.

## Defect

The DEAD_CODE transformation was documented before measurement, but its
intended helper methods were absent from the committed DEAD_CODE Java source
files.

Behavioral fixture validation did not reveal this omission because the
transformation is specifically intended not to affect observable behavior.

## Correction

The DEAD_CODE submissions are changed only by inserting the helper methods
already documented before the first primary measurement:

- family-a: `unusedDifference(int left, int right)` returning `left - right`
- family-b: `unusedUppercase(String text)` returning `text.toUpperCase()`
- family-c: `unusedEmptyCheck(String text)` returning `text.isEmpty()`
- family-d: `unusedArea(int rows, int columns)` returning `rows * columns`

These methods are not invoked.

No provenance family, transformation class, declared behavioral test,
representation stage, representation rule, similarity function, pair label,
or analysis threshold is changed.

## Validation requirement

After correction:

1. all 28 submissions must compile independently;
2. all 84 declared behavioral test executions must pass;
3. no compiled `.class` artifacts may remain;
4. each DEAD_CODE source must differ lexically from its corresponding BASE;
5. each documented dead-code helper must occur in its intended DEAD_CODE
   source.

A corrected primary measurement run must be generated and identified
separately from the original primary run.
