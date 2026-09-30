# Experiment 002 Primary Analysis

## Provenance

Canonical measurement artifact:

`experiment-002-primary-measurements.csv`

SHA-256:

`3538FA569F6857F5E9616FB2CD52B1E58A547FD645AB1F8963707251FC485B07`

Primary measurement commit:

`f5217dc654a707ab207236a51c1eed7ad48bf57c`

The analysis below is descriptive. Similarity values are not
plagiarism probabilities, and no classification threshold is
selected.

## Related and control distributions

| Condition | Label | n | Mean | Median | Min | Q1 | Q3 | Max |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| C0 | related | 24 | 0.743607 | 0.723343 | 0.487310 | 0.696379 | 0.814792 | 1.000000 |
| C0 | control | 96 | 0.561939 | 0.583505 | 0.385787 | 0.550082 | 0.604249 | 0.656250 |
| C1 | related | 24 | 0.993137 | 0.995870 | 0.980482 | 0.986534 | 1.000000 | 1.000000 |
| C1 | control | 96 | 0.543548 | 0.524850 | 0.458604 | 0.470768 | 0.623623 | 0.666137 |

## Related-control mean gap

| Condition | Related mean - control mean |
|---|---:|
| C0 | 0.181668 |
| C1 | 0.449589 |

## Empirical ordering probability

Ties contribute 0.5. This is descriptive and is not a
plagiarism probability.

| Condition | Ordering probability |
|---|---:|
| C0 | 0.868490 |
| C1 | 1.000000 |

## Exact similarity collisions

| Condition | Related score = 1.0 | Control score = 1.0 |
|---|---:|---:|
| C0 | 4 | 0 |
| C1 | 12 | 0 |

## BASE-to-transformation retention

| Condition | Transformation | n | Mean | Min | Max | Population SD |
|---|---|---:|---:|---:|---:|---:|
| C0 | METHOD_REORDER | 4 | 0.733750 | 0.700000 | 0.798450 | 0.038620 |
| C0 | CLASS_SPLIT | 4 | 0.692713 | 0.487310 | 0.863821 | 0.134555 |
| C0 | IDENTIFIER_RENAME | 4 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |
| C1 | METHOD_REORDER | 4 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |
| C1 | CLASS_SPLIT | 4 | 0.986274 | 0.980482 | 0.991739 | 0.003986 |
| C1 | IDENTIFIER_RENAME | 4 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |

## Paired C1 minus C0 changes

Positive values mean the C1 structural comparison produced
higher similarity for the same submission pair.

| Pair group | n | Mean C1-C0 |
|---|---:|---:|
| all related | 24 | 0.249530 |
| all control | 96 | -0.018391 |
| BASE-to-METHOD_REORDER | 4 | 0.266250 |
| BASE-to-CLASS_SPLIT | 4 | 0.293561 |
| BASE-to-IDENTIFIER_RENAME | 4 | 0.000000 |

## Primary observations

- BASE-to-METHOD_REORDER mean retention changed from 0.733750 under C0 to 1.000000 under C1.
- BASE-to-CLASS_SPLIT mean retention changed from 0.692713 under C0 to 0.986274 under C1.
- BASE-to-IDENTIFIER_RENAME mean retention changed from 1.000000 under C0 to 1.000000 under C1.
- Mean paired C1-C0 change across all related pairs was 0.249530.
- Mean paired C1-C0 change across all control pairs was -0.018391.
- The related-control mean gap changed from 0.181668 under C0 to 0.449589 under C1.
- Empirical ordering probability changed from 0.868490 under C0 to 1.000000 under C1.
- Exact control collisions were 0 under C0 and 0 under C1.

These observations must be interpreted jointly. Increased
transformation retention is not by itself evidence of an
unqualified improvement if control similarity also increases
enough to weaken related/control distinction.

## Scope

This experiment measures deterministic behavior on four frozen
Java provenance families and three controlled transformations.
It does not establish a plagiarism threshold, estimate a
plagiarism probability, or establish general performance on
unseen real-world submissions.
