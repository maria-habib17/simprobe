# Experiment 001 Primary Run Record

## Status

Primary measurements generated.

This record documents the first primary measurement run after the fixture,
measurement specification, implementation, and runner were frozen.

## Frozen pre-measurement commit

`4042b61b78244b9001a0713525756e8b76beb9d2`

Relevant preceding boundaries:

- primary fixture freeze: `ccbc013fd058714ae813136a1044e498799c6835`
- measurement specification freeze: `9330bf270be347d22fa1b33cc1da6c90c4d18e1d`
- representation implementation freeze: `32fbb6af1f2d06f7c6694495b6c8c04a13a89f93`
- primary runner freeze: `4042b61b78244b9001a0713525756e8b76beb9d2`

## Canonical output

Path:

`results/experiment-001-primary-measurements.csv`

SHA-256:

`38D2C00E4CD78EAF153C85B6C5AFBAEE689B0256A4ECBD5019DECC681FC91C4B`

## Structural validation

The first primary run produced:

- 28 submissions
- 378 unique unordered submission pairs
- 7 representation stages
- 2,646 pair/representation rows
- 588 related rows
- 2,058 control rows

The output schema matched the frozen measurement specification.

All similarity values were within `[0, 1]`.

All edit distances and representation lengths were nonnegative.

All pair labels matched frozen family provenance.

## Reproducibility check

The frozen runner was executed a second time without changing the repository.

The second output SHA-256 was:

`38D2C00E4CD78EAF153C85B6C5AFBAEE689B0256A4ECBD5019DECC681FC91C4B`

The two CSV files were therefore byte-for-byte identical.

The first-run output was restored as the canonical output after this check.

## Interpretation boundary

No substantive similarity-score interpretation was performed before the
structural and reproducibility checks documented above.

Any later correction to the fixture, representation implementation,
measurement implementation, or experimental definitions must be documented
and versioned rather than silently replacing this primary run.
