# Experiment 004 Sampling Deduplication Rule

Status: frozen before pair selection and before all C0/C1 measurements.

## Observed condition

The sampling unit defined in SAMPLING_SPEC.md is the canonical function pair:

min(FUNCTION_ID_ONE, FUNCTION_ID_TWO):max(FUNCTION_ID_ONE, FUNCTION_ID_TWO)

During pre-selection implementation diagnostics, repeated CLONES rows were found for some canonical pairs.

Within the deterministic retained candidate windows:

- duplicate canonical pair keys: 17
- duplicate rows: 34
- duplicate keys within the same stratum: 17
- duplicate keys crossing strata: 0
- duplicate keys differing only in FUNCTIONALITY_ID: 17
- duplicate keys with other exported metadata differences: 0

The repeated rows therefore represent the same source-function pair and clone metadata while carrying multiple functionality labels.

## Frozen rule

1. One canonical function pair is one sampling unit.
2. Repeated CLONES rows for the same canonical pair and stratum are collapsed into one sampling candidate.
3. Repeated rows do not receive additional sampling opportunities.
4. The SHA-256 selection key remains exactly as specified in SAMPLING_SPEC.md.
5. All associated FUNCTIONALITY_ID values are retained, deduplicated, numerically sorted, and recorded as a semicolon-separated multi-label field.
6. Functionality labels do not affect inclusion, exclusion, ranking, or replacement.
7. If duplicate rows conflict on non-functionality metadata or occur in different strata, sampling stops rather than resolving the conflict silently.
8. Technical source eligibility remains governed by SAMPLING_SPEC.md.

## Measurement boundary

- pairs selected: 0
- C0 measurements: 0
- C1 measurements: 0

This rule was frozen before observing any SimProbe score.
