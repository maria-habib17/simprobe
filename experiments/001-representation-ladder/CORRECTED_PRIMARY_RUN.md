# Experiment 001 Corrected Primary Run Record

## Status

Corrected primary measurements generated after documented Fixture Correction
002.

This run is distinct from, and does not replace or erase, the original primary
measurement run.

## Reason for corrected run

After the original primary results had been generated and inspected,
BASE/DEAD_CODE pairs were observed to have exact similarity at R0 through R6.

Diagnostic investigation established that the DEAD_CODE fixture sources did
not contain the helper methods documented before primary measurement.

The defect and its correction are documented in:

`corrections/002-dead-code-fixture-omission.md`

## Correction commit

The corrected fixture state is identified by:

`822bdcb7c4d549aeca4bd31ea4d596421fd01969`

No representation rule, similarity function, provenance family,
transformation class, pair-label definition, or declared behavioral test was
changed by Correction 002.

## Original primary run retained

The original primary output remains:

`results/experiment-001-primary-measurements.csv`

SHA-256:

`38D2C00E4CD78EAF153C85B6C5AFBAEE689B0256A4ECBD5019DECC681FC91C4B`

Its run record is:

`PRIMARY_RUN.md`

The original result is retained as the historical first primary run containing
the subsequently documented DEAD_CODE fixture defect.

## Corrected primary output

The corrected output is:

`results/experiment-001-primary-measurements-corrected.csv`

SHA-256:

`30FCE0440741EE28A1B8A7D53C2605CAAA5AAD48988F1BF30516B28F247FA723`

## Structural validation

The corrected run contains:

- 28 submissions
- 378 unique unordered submission pairs
- 7 representation stages
- 2,646 pair/representation rows
- 588 related rows
- 2,058 control rows

All structural validation checks passed.

All similarity values were within `[0, 1]`.

All pair labels matched frozen family provenance.

## DEAD_CODE correction check

At R0, each corrected BASE/DEAD_CODE pair had nonzero edit distance:

- family-a: 18
- family-b: 17
- family-c: 17
- family-d: 18

Thus the corrected DEAD_CODE submissions are no longer lexically identical to
their corresponding BASE submissions.

Before this measurement run, all 28 corrected submissions compiled
independently and all 84 declared behavioral test executions passed.

## Reproducibility

The corrected measurement was generated twice from the same correction commit.

Both outputs had SHA-256:

`30FCE0440741EE28A1B8A7D53C2605CAAA5AAD48988F1BF30516B28F247FA723`

The corrected output is therefore byte-for-byte reproducible under the tested
environment.

## Interpretation boundary

No aggregate corrected-run similarity distributions were inspected before the
corrected output, its structural validation, and its reproducibility hash were
established.

Subsequent analysis should use the corrected primary output while retaining
the original run and Correction 002 as part of the experimental provenance.
