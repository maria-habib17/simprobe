# SimProbe Related Work and Contribution Boundary

## Status

Pre-implementation related-work map.

This document records the research areas most closely related to SimProbe and
defines claims that the project must not make without stronger evidence.

It is not intended to be a complete systematic literature review.

## 1. Source-code similarity measurement

Source-code similarity has been studied using textual, token-based,
tree/structural, metric-based, semantic, and learned representations.

Large empirical comparisons have shown that similarity tools can behave
differently across datasets, transformations, configurations, and similarity
techniques.

Therefore SimProbe does not claim that representation choice affects similarity
measurement for the first time.

## 2. Robustness to program transformations

Clone and plagiarism detectors have been evaluated under source-code
transformations and obfuscations.

Prior research has studied whether detectors retain similarity when programs
are renamed, reformatted, structurally modified, obfuscated, compiled,
decompiled, or otherwise transformed.

Therefore SimProbe does not claim that the robustness of similarity detectors
to transformations is a new research problem.

## 3. Normalization

Normalization is an established technique for making similarity comparison less
sensitive to selected syntactic differences.

Identifier normalization, structural normalization, token normalization, and
related abstraction techniques occur throughout the code-similarity and clone
detection literature.

JPlag also provides normalization functionality for supported languages.

Therefore SimProbe does not claim to invent source-code normalization.

## 4. False positives and clone validation

Code clone and similarity detectors may return irrelevant or false-positive
matches depending on the intended clone definition, dataset, configuration, and
use case.

Prior research has investigated automatic and manual validation of reported
clones.

Therefore SimProbe does not claim that high similarity can produce false
positives for the first time.

SimProbe also avoids automatically calling a high-similarity control pair a
"false positive" unless the experimental ground truth and decision rule justify
that terminology.

## 5. Cohort and frequency information

Program-similarity analysis is not necessarily restricted to interpreting each
pair in isolation.

JPlag compares submissions within a collection and supports frequency analysis
that can identify and weight rare matches.

Consequently, SimProbe must not claim that cohort frequency, match rarity, or
collection-level context are new ideas.

The distinction under investigation is narrower: whether properties describing
the degeneracy or distinctiveness of the representation and similarity result
within its surrounding cohort provide a useful measurement dimension separate
from similarity magnitude.

## 6. Similarity score distributions

Similarity systems may expose distributions, rankings, clusters, thresholds,
or multiple similarity measures.

A high pairwise score therefore must not be presented by SimProbe as if prior
systems provide no surrounding context.

The research question is instead whether cohort-conditioned representation
ambiguity can be explicitly defined, measured, and evaluated as a property of
the evidence produced by different representations.

## 7. Current JPlag boundary

JPlag is an important comparison system for SimProbe.

Current JPlag functionality includes pairwise program comparison, configurable
minimum token matches, normalization for supported languages, clustering,
match merging, CSV export, and frequency-based analysis.

SimProbe must not characterize JPlag as a filename-only, class-name-only, or
pure textual comparison system.

SimProbe must also avoid treating a JPlag similarity value as mathematically
equivalent to a SimProbe similarity value.

The intended comparison concerns empirical behavior under controlled
representations, transformations, and cohort composition.

## 8. SimProbe's current research gap

The working gap is intentionally narrow.

SimProbe investigates whether the following should be treated as different
properties:

1. pairwise similarity magnitude;
2. transformation invariance of the representation;
3. discriminative capacity of the representation within a cohort; and
4. cohort-conditioned distinctiveness of a particular similarity result.

The central empirical question is whether a high similarity result can remain
numerically unchanged while its distinctiveness changes substantially as:

- the surrounding cohort changes;
- the representation becomes more abstract;
- representation collisions increase; or
- high-similarity neighborhoods become denser.

The project will test whether measurements such as representation multiplicity,
score ties, neighborhood density, rank separation, and representation entropy
provide useful information beyond the pairwise similarity value.

## 9. What would count as a contribution

A defensible contribution could consist of one or more of the following:

- a reproducible methodology for measuring the invariance-discrimination
  trade-off across source-code representations;
- empirical evidence showing when maximal or high similarity values are
  distinctive versus common within a cohort;
- a cohort-perturbation methodology that holds a target pair fixed while
  varying its surrounding comparison population;
- measurements that characterize representation degeneracy without converting
  similarity into a plagiarism probability;
- a cross-system empirical study showing where these phenomena generalize or
  fail to generalize.

Whether any of these are scientifically novel remains subject to further
literature review.

## 10. Claims SimProbe must not make

Without substantially stronger evidence, SimProbe must not claim:

- to be the first uncertainty-aware code-similarity system;
- to be the first cohort-aware similarity system;
- to invent rarity or frequency analysis;
- to invent code normalization;
- to solve false positives;
- to detect plagiarism more accurately than established systems;
- to prove that a high-similarity pair is independently written;
- to prove that a representation collision is a false positive;
- to establish a universal similarity threshold;
- to establish that one representation is universally superior;
- to establish that similarity magnitude has no evidential value;
- to establish novelty solely because an identical implementation was not found.

## 11. Literature-review requirements before publication

Before a paper or preprint makes a novelty claim, the related-work search must
be expanded systematically across at least:

- source-code similarity measurement;
- clone detection and validation;
- plagiarism detection;
- similarity calibration and confidence;
- normalization and abstraction;
- information-theoretic program representations;
- cohort-relative and frequency-based similarity;
- anomaly and neighborhood measures;
- representation collisions;
- ranking and score-distribution analysis.

Search queries, databases, inclusion criteria, exclusion criteria, dates, and
candidate papers should be recorded.

## Initial references

Ragkhitwetsagul, C., Krinke, J., and Clark, D.
"A Comparison of Code Similarity Analysers."
Empirical Software Engineering.

JPlag project documentation and current usage documentation.
Karlsruhe Institute of Technology / JPlag contributors.

"A machine learning based framework for code clone validation."
Journal of Systems and Software, 2020.

"A systematic literature review on source code similarity measurement and
clone detection: Techniques, applications, and challenges."
Journal of Systems and Software, 2023.

Additional primary references will be added and verified before publication.