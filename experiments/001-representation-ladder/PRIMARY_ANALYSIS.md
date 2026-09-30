# Experiment 001 Primary Analysis

## Analysis basis

This analysis uses the corrected primary measurement output:

`results/experiment-001-primary-measurements-corrected.csv`

SHA-256:

`30FCE0440741EE28A1B8A7D53C2605CAAA5AAD48988F1BF30516B28F247FA723`

The original defective run and Correction 002 remain part of the experiment
provenance. See `PRIMARY_RUN.md`, `CORRECTED_PRIMARY_RUN.md`, and
`corrections/002-dead-code-fixture-omission.md`.

No fixture, representation, similarity, pair-label, or threshold rule was
changed during this analysis.

## Related and control distributions

| Stage | Related mean | Control mean | Mean gap | P(related > control) |
|---|---:|---:|---:|---:|
| R0 | 0.620586 | 0.301297 | 0.319289 | 0.806710 |
| R1 | 0.620586 | 0.301297 | 0.319289 | 0.806710 |
| R2 | 0.716641 | 0.439652 | 0.276989 | 0.770327 |
| R3 | 0.716757 | 0.444683 | 0.272074 | 0.764638 |
| R4 | 0.702869 | 0.423070 | 0.279798 | 0.753179 |
| R5 | 0.698900 | 0.426645 | 0.272255 | 0.729248 |
| R6 | 0.757159 | 0.503870 | 0.253290 | 0.801101 |

The ordering probability is the empirical probability that a randomly selected
related-pair score exceeds a randomly selected control-pair score, with ties
counted as one half. It is a descriptive statistic, not a plagiarism
probability or a selected classification threshold.

R0 and R1 are intentionally identical under the frozen representation rules.

Increasing abstraction does not produce monotonic improvement in
related/control discrimination. R2 through R5 increase invariance to selected
transformations while reducing the empirical related/control ordering
probability relative to R0/R1. R6 recovers much of that ordering probability
while operating at higher similarity levels for both related and control
pairs.

## Transformation-specific behavior

Identifier abstraction has its intended effect. IDENTIFIER_RENAME has mean
similarity 0.799482 at R0/R1 and exact similarity 1.0 across all four families
from R2 through R6.

CLASS_RENAME is near-exact at R0/R1 and exactly invariant across all four
families from R2 through R6.

FILE_RENAME becomes exactly invariant across all four families at R5 and R6.

Following Correction 002, DEAD_CODE is highly similar but not identical to
BASE. Mean BASE-to-DEAD_CODE similarity ranges from approximately 0.9421 to
0.9484 across the representation ladder.

METHOD_REORDER remains substantially non-invariant. Its mean similarity rises
from 0.419707 at R0/R1 to 0.612874 at R6. At R6, the four family values range
from approximately 0.473054 to 0.821782.

CLASS_SPLIT is the lowest-retention BASE transformation at every stage. Its
mean similarity is 0.312493 at R0/R1 and reaches 0.471877 at R6. This
transformation intentionally changes program architecture more substantially
than the lexical renaming transformations.

## Exact-similarity collisions

No control pair has exact similarity 1.0 at any representation stage.

Related exact-similarity counts are:

| Stage | Exact related pairs | Total related pairs |
|---|---:|---:|
| R0 | 0 | 84 |
| R1 | 0 | 84 |
| R2 | 12 | 84 |
| R3 | 12 | 84 |
| R4 | 12 | 84 |
| R5 | 24 | 84 |
| R6 | 24 | 84 |

Thus increasing abstraction creates exact invariance for selected related
transformations in this fixture without producing exact cross-family
collisions. This does not imply that unrelated submissions remain well
separated: control similarity itself increases substantially at several
abstract stages.

## Interpretation

The primary experiment supports a transformation-specific tradeoff rather than
a universally improving abstraction ladder.

Name-oriented abstraction successfully removes differences caused by
identifier and class renaming. More architectural transformations remain
difficult: declaration reordering retains substantial sequence sensitivity,
and class splitting is the lowest-retention transformation at every stage.

R6 illustrates why invariance and discrimination must be evaluated together.
It has the highest related mean similarity, but also the highest control mean
similarity. Its related/control mean gap is smaller than R0/R1 even though its
empirical ordering probability recovers close to the R0/R1 level.

These measurements therefore do not identify a universally optimal
representation stage. They characterize how the frozen representations trade
transformation invariance against loss of distinguishing information on this
specific fixture.

## Limitations

The primary fixture contains four provenance families and six controlled
transformations per family. Results should not be generalized directly to
arbitrary Java programs or real plagiarism cases.

Behavioral preservation is supported by the declared fixture tests; it is not
a formal proof of semantic equivalence.

R5 is a deterministic syntax proxy rather than a full Java AST representation.

The normalized Levenshtein similarity is order-sensitive, which is directly
relevant to the METHOD_REORDER and CLASS_SPLIT results.

No decision threshold or plagiarism probability is inferred from these
measurements.

## Derived analysis artifacts

Tradeoff analysis:

`results/experiment-001-corrected-tradeoff.csv`

SHA-256:

`92FBC4EFC1B14CD45DA17F97BD6E8333078E3B4E8BA2041D6386F6227F213464`

Transformation summary:

`results/experiment-001-corrected-transformation-summary.csv`

SHA-256:

`4E320777B834311A75A35CC4BCE5C341925B3FDCA691F39FD44EAA9F38B6DE22`
