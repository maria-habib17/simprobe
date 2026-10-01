# Experiment 003 Primary Analysis

## Provenance

Canonical Experiment 003 measurement artifact:

`experiment-003-primary-measurements.csv`

SHA-256:

`D2B790A836506F371CA5E4862406CD7DE87E0BC7541F3323D3C038271B003C81`

Primary measurement commit:

`5ac08cbb02bdef56b4ab56d58d947e146b8b15ff`

Cross-experiment reference artifact:

`experiment-002-primary-measurements.csv`

Reference SHA-256:

`3538FA569F6857F5E9616FB2CD52B1E58A547FD645AB1F8963707251FC485B07`

Reference measurement commit:

`f5217dc654a707ab207236a51c1eed7ad48bf57c`

Both input hashes are verified by the analysis script before analysis.

The analysis below is descriptive. Similarity values are not
plagiarism probabilities, and no classification threshold is selected.

## Related and control distributions

| Condition | Label | n | Mean | Median | Min | Q1 | Q3 | Max |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| C0 | related | 72 | 0.669228 | 0.643749 | 0.400000 | 0.465880 | 0.812727 | 1.000000 |
| C0 | control | 1056 | 0.544525 | 0.560322 | 0.331034 | 0.440217 | 0.618557 | 0.815047 |
| C1 | related | 72 | 0.991159 | 0.997368 | 0.962981 | 0.988173 | 1.000000 | 1.000000 |
| C1 | control | 1056 | 0.564466 | 0.564147 | 0.401639 | 0.498384 | 0.620297 | 0.780059 |

## Related-control mean gap

| Condition | Related mean - control mean |
|---|---:|
| C0 | 0.124703 |
| C1 | 0.426693 |

## Empirical ordering probability

Ties contribute 0.5. This is descriptive and is not a plagiarism probability.

| Condition | Ordering probability |
|---|---:|
| C0 | 0.663799 |
| C1 | 1.000000 |

## Exact similarity collisions

| Condition | Related score = 1.0 | Control score = 1.0 |
|---|---:|---:|
| C0 | 12 | 0 |
| C1 | 36 | 0 |

## BASE-to-transformation retention

| Condition | Transformation | n | Mean | Min | Max | Population SD |
|---|---|---:|---:|---:|---:|---:|
| C0 | METHOD_REORDER | 12 | 0.781857 | 0.650273 | 0.909722 | 0.071664 |
| C0 | CLASS_SPLIT | 12 | 0.472994 | 0.414248 | 0.637224 | 0.057730 |
| C0 | IDENTIFIER_RENAME | 12 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |
| C1 | METHOD_REORDER | 12 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |
| C1 | CLASS_SPLIT | 12 | 0.982317 | 0.962981 | 0.994737 | 0.011398 |
| C1 | IDENTIFIER_RENAME | 12 | 1.000000 | 1.000000 | 1.000000 | 0.000000 |

## Paired C1 minus C0 changes

Positive values mean C1 produced higher similarity for the same pair.

| Pair group | n | Mean C1-C0 |
|---|---:|---:|
| all related | 72 | 0.321930 |
| all control | 1056 | 0.019941 |
| BASE-to-METHOD_REORDER | 12 | 0.218143 |
| BASE-to-CLASS_SPLIT | 12 | 0.509323 |
| BASE-to-IDENTIFIER_RENAME | 12 | 0.000000 |

## Control-pair C1 minus C0 distribution

| n | Mean | Median | Min | Q1 | Q3 | Max | Population SD |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1056 | 0.019941 | -0.001091 | -0.153789 | -0.057339 | 0.093401 | 0.364132 | 0.102755 |

## Family-level replication

Each row is the BASE-to-transformation score for one frozen family.

| Transformation | Family | C0 | C1 | C1-C0 |
|---|---|---:|---:|---:|
| METHOD_REORDER | A | 0.812274 | 1.000000 | 0.187726 |
| METHOD_REORDER | B | 0.775735 | 1.000000 | 0.224265 |
| METHOD_REORDER | C | 0.796154 | 1.000000 | 0.203846 |
| METHOD_REORDER | D | 0.814085 | 1.000000 | 0.185915 |
| METHOD_REORDER | E | 0.730263 | 1.000000 | 0.269737 |
| METHOD_REORDER | F | 0.683849 | 1.000000 | 0.316151 |
| METHOD_REORDER | G | 0.890323 | 1.000000 | 0.109677 |
| METHOD_REORDER | H | 0.746914 | 1.000000 | 0.253086 |
| METHOD_REORDER | I | 0.801609 | 1.000000 | 0.198391 |
| METHOD_REORDER | J | 0.771084 | 1.000000 | 0.228916 |
| METHOD_REORDER | K | 0.650273 | 1.000000 | 0.349727 |
| METHOD_REORDER | L | 0.909722 | 1.000000 | 0.090278 |
| CLASS_SPLIT | A | 0.424138 | 0.962981 | 0.538843 |
| CLASS_SPLIT | B | 0.451957 | 0.991667 | 0.539709 |
| CLASS_SPLIT | C | 0.464945 | 0.972383 | 0.507439 |
| CLASS_SPLIT | D | 0.516304 | 0.974772 | 0.458468 |
| CLASS_SPLIT | E | 0.637224 | 0.972445 | 0.335221 |
| CLASS_SPLIT | F | 0.420530 | 0.978781 | 0.558251 |
| CLASS_SPLIT | G | 0.476489 | 0.993750 | 0.517261 |
| CLASS_SPLIT | H | 0.462462 | 0.993464 | 0.531002 |
| CLASS_SPLIT | I | 0.437173 | 0.994737 | 0.557564 |
| CLASS_SPLIT | J | 0.472141 | 0.993750 | 0.521609 |
| CLASS_SPLIT | K | 0.414248 | 0.967775 | 0.553527 |
| CLASS_SPLIT | L | 0.498316 | 0.991304 | 0.492988 |

### Family-level direction counts

| Transformation | Positive | Zero | Negative |
|---|---:|---:|---:|
| METHOD_REORDER | 12 | 0 | 0 |
| CLASS_SPLIT | 12 | 0 | 0 |

## Cross-experiment comparison

Experiment 002 used four frozen provenance families; Experiment 003
uses twelve independently constructed frozen provenance families.
The C0/C1 comparison definitions are held fixed.

| Metric | Experiment 002 | Experiment 003 |
|---|---:|---:|
| C0 related mean | 0.743607 | 0.669228 |
| C0 control mean | 0.561939 | 0.544525 |
| C1 related mean | 0.993137 | 0.991159 |
| C1 control mean | 0.543548 | 0.564466 |
| C0 related-control mean gap | 0.181668 | 0.124703 |
| C1 related-control mean gap | 0.449589 | 0.426693 |
| C0 ordering probability | 0.868490 | 0.663799 |
| C1 ordering probability | 1.000000 | 1.000000 |
| METHOD_REORDER C0 retention | 0.733750 | 0.781857 |
| METHOD_REORDER C1 retention | 1.000000 | 1.000000 |
| CLASS_SPLIT C0 retention | 0.692713 | 0.472994 |
| CLASS_SPLIT C1 retention | 0.986274 | 0.982317 |
| IDENTIFIER_RENAME C0 retention | 1.000000 | 1.000000 |
| IDENTIFIER_RENAME C1 retention | 1.000000 | 1.000000 |
| Mean control C1-C0 | -0.018391 | 0.019941 |

## Primary observations

- BASE-to-METHOD_REORDER mean retention changed from 0.781857 under C0 to 1.000000 under C1.
- BASE-to-CLASS_SPLIT mean retention changed from 0.472994 under C0 to 0.982317 under C1.
- BASE-to-IDENTIFIER_RENAME mean retention changed from 1.000000 under C0 to 1.000000 under C1.
- METHOD_REORDER had positive C1-C0 retention change in 12 of 12 families.
- CLASS_SPLIT had positive C1-C0 retention change in 12 of 12 families.
- Mean paired C1-C0 change across all related pairs was 0.321930.
- Mean paired C1-C0 change across all control pairs was 0.019941.
- The related-control mean gap changed from 0.124703 under C0 to 0.426693 under C1.
- Empirical ordering probability changed from 0.663799 under C0 to 1.000000 under C1.
- Exact control collisions were 0 under C0 and 0 under C1.

These observations must be interpreted jointly. Increased
transformation retention is not by itself evidence of an
unqualified improvement if control similarity also increases
enough to weaken related/control distinction.

## Scope

Experiment 003 is a controlled broader validation across twelve
independently constructed frozen Java provenance families and three
controlled transformations. It broadens the controlled replication
relative to Experiment 002, but it is not external benchmark
validation and does not establish general performance on unseen
real-world submissions.

No plagiarism threshold is selected, and similarity values are not
interpreted as plagiarism probabilities.
