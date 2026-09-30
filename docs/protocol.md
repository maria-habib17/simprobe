# SimProbe Research Protocol v0.1

## Status

Pre-implementation protocol.

This document defines the initial research questions, hypotheses, measurements,
evaluation design, and interpretation constraints for SimProbe before the
experimental similarity implementation is developed.

SimProbe does not classify plagiarism and does not infer author intent.

## Research objective

Source-code similarity systems usually report a pairwise similarity value.
A high similarity value, however, does not necessarily indicate that the
observed similarity is distinctive within the surrounding cohort.

SimProbe investigates the distinction between:

1. similarity magnitude; and
2. cohort-conditioned evidential distinctiveness.

The central question is:

> How does the evidential distinctiveness of a source-code similarity result
> change as representations gain transformation invariance but lose
> discriminative information within a cohort?

## Research questions

### RQ1 — Invariance and discrimination

How does increasing representation abstraction affect robustness to controlled
program transformations and discrimination among independently constructed
programs?

### RQ2 — Cohort-conditioned ambiguity

How distinctive is a high pairwise similarity result relative to the
distribution of similarities in the cohort in which it occurs?

### RQ3 — Information loss

Which representation transformations contribute most strongly to measurable
loss of discriminative information?

Candidate transformations include:

- comment and formatting removal;
- identifier normalization;
- literal normalization;
- selected name/type abstraction; and
- structural abstraction.

### RQ4 — Cross-method generality

Are observed ambiguity patterns specific to one representation or system, or
do analogous patterns occur across multiple source-code similarity methods?

## Initial hypotheses

### H1

Increasing abstraction will improve invariance to at least some controlled
transformations, but may increase similarity collisions or dense
high-similarity regions among independently constructed programs.

### H2

For some high-similarity pairs, cohort-relative measurements will reveal
substantial differences in distinctiveness that are not represented by the
pairwise similarity value alone.

### H3

Different abstraction operations will contribute unequally to representation
degeneracy and discriminative-information loss.

### H4

The invariance-discrimination trade-off will vary across datasets and
assignment characteristics.

These hypotheses are empirical claims to test, not assumptions that SimProbe
must confirm.

## Representation ladder

The initial representation ladder is:

- R0: lexical/raw token representation;
- R1: formatting and comments excluded;
- R2: identifiers normalized;
- R3: literals normalized;
- R4: selected name/type information abstracted;
- R5: structural syntax representation;
- R6: intentionally aggressive abstraction.

The exact implementation of every level must be documented before its primary
evaluation results are inspected.

Representations may be revised during development, but revisions made after
observing primary evaluation results must be recorded and evaluated separately
from the frozen primary experiment.

## Pairwise similarity

For submissions xi and xj under similarity function s:

S(i,j) = s(xi, xj)

Pairwise similarity remains a measurement of similarity only.

It must not be interpreted as a probability of plagiarism, common authorship,
or misconduct.

## Cohort-conditioned measurements

The initial measurements to investigate include:

### Exact representation multiplicity

For representation R and submission x:

M_R(x) = number of submissions in the cohort having exactly the same
representation as x.

### Score-tie multiplicity

For pair (i,j), measure how many cohort pairs receive the same similarity value
as S(i,j).

### Neighborhood density

Measure the proportion of other submissions lying within specified
high-similarity regions around a submission.

Primary analysis must not select a single favorable threshold after observing
the results. Threshold curves, rank-based alternatives, or predeclared
thresholds should be preferred.

### Rank-based distinctiveness

Measure where a pair appears in each submission's similarity neighborhood and
how separated it is from surrounding pairs.

### Representation entropy

For representation classes with empirical cohort probabilities pk:

H(R) = -sum(pk * log2(pk))

Entropy is treated as a descriptive measurement of representation diversity,
not as a direct plagiarism or confidence score.

### Information-loss proxy

For successive representations:

DeltaH(k) = H(R[k-1]) - H(R[k])

This is an exploratory measure of representation collapse. It is not assumed
in advance to measure evidential quality.

## Primary outcome dimensions

SimProbe keeps two dimensions separate.

### Transformation invariance

How well does a representation preserve high correspondence between programs
related by known controlled transformations?

### Discriminative loss

How strongly does the representation increase collisions, ties, dense
high-similarity neighborhoods, or similarity among independently constructed
controls?

No representation will be declared universally best solely from one of these
dimensions.

Where appropriate, the analysis will examine the Pareto relationship between
invariance and discrimination.

## Evaluation layers

### Layer A — Controlled transformations

Programs with known provenance will be subjected to documented transformations.

Candidate transformations include:

- identifier renaming;
- method reordering;
- class renaming;
- file renaming;
- method extraction;
- class splitting;
- dead-code insertion; and
- selected behavior-preserving structural rewrites.

Each transformation must be documented and its intended behavioral status
stated explicitly.

### Layer B — Independent solutions

Independently developed implementations of the same specification will be used
to study ambiguity arising from legitimate shared requirements, algorithms,
APIs, and assignment constraints.

Dataset provenance and limitations must be documented.

### Layer C — Software evolution

Later evaluation may examine real software versions to determine whether the
observed representation phenomena generalize beyond programming assignments.

Layer C is outside the minimum v0.1 implementation.

## Comparison methods

Planned comparison methods include:

- SimProbe's explicit representation ladder;
- a simple token or fingerprint/winnowing baseline;
- BehavClone representations;
- an independent AST/structural representation; and
- JPlag as an established external program-similarity system.

Learned code embeddings are not required for v0.1.

Scores from different systems must not be treated as mathematically equivalent
unless such equivalence is established.

## Cohort perturbation experiment

A key experiment will hold a target pair fixed while changing the surrounding
cohort.

The pairwise source programs remain unchanged.

The experiment will measure whether:

- pairwise similarity remains stable; while
- cohort-conditioned distinctiveness changes.

This directly tests whether pair similarity and cohort-conditioned
distinctiveness capture different properties.

Cohort construction rules must be frozen before primary results are inspected.

## Statistical reporting

Where sample size permits, reporting should include:

- full score distributions;
- medians and interquartile ranges;
- collision and tie frequencies;
- transformation-specific results;
- rank distributions;
- effect sizes where meaningful;
- uncertainty intervals or bootstrap confidence intervals where appropriate;
- sensitivity to cohort composition.

Aggregate means alone are insufficient.

## Results that would weaken the hypotheses

The project must retain negative findings.

Evidence against the proposed direction would include:

- cohort-conditioned measurements providing little information beyond the
  original pairwise similarity;
- representation abstraction producing no reproducible discriminative loss
  across sufficiently diverse datasets;
- ambiguity appearing only in BehavClone-specific representations;
- entropy or collision measurements failing to correspond to meaningful
  differences in pair distinctiveness;
- results being dominated by artifacts of synthetic fixture construction.

Such outcomes must not be removed merely because they weaken the motivating
hypothesis.

## Interpretation constraints

SimProbe does not:

- determine plagiarism;
- infer author intent;
- infer common authorship;
- convert similarity into a probability of misconduct;
- prescribe a universal similarity threshold;
- assume that high similarity is suspicious;
- assume that a representation collision is a false positive;
- assume that independently labelled programs are proof of independent
  authorship beyond what dataset provenance supports.

Similarity, representation ambiguity, and evidence interpretation remain
separate concepts.

## Reproducibility

Primary experiments should record:

- dataset source and version;
- inclusion and exclusion rules;
- transformation definitions;
- representation configuration;
- similarity configuration;
- random seeds where applicable;
- software versions;
- result-file hashes;
- exact commands required for reproduction.

Experimental protocols should be committed before the corresponding primary
measurements whenever practical.

## Initial scope

SimProbe v0.1 will:

- use Python for orchestration and analysis;
- initially study Java source code;
- provide command-line research tooling;
- avoid an LLM dependency;
- avoid a graphical interface;
- avoid automatic plagiarism classification;
- keep raw measurements available for independent analysis.

## Research positioning

The initial contribution under investigation is:

> A methodology for measuring cohort-conditioned representational ambiguity in
> source-code similarity, with particular attention to the trade-off between
> transformation invariance and discriminative information.

This is a research hypothesis and positioning statement, not a claim of
scientific novelty.

Novelty must be evaluated against related work before publication claims are
made.