# Experiment 004 - External Validation

## Status

Protocol frozen before benchmark acquisition, sampling, measurement, or result inspection.

## Purpose

Experiment 004 evaluates whether the fixed SimProbe comparison conditions from
Experiments 002 and 003 exhibit useful discrimination behavior on independently
curated Java clone data rather than only on SimProbe's controlled provenance
families.

This experiment is external validation. It is intentionally distinct from the
controlled transformation experiments.

## Research Question

When applied without tuning to externally curated Java clone pairs, how do the
fixed C0 and C1 representations behave across benchmark clone categories and
syntactic-similarity regions?

The experiment specifically asks whether the structure-aware C1 representation
retains the robustness advantage observed in the controlled experiments without
assuming that every benchmark category represents semantic equivalence.

## Benchmark

The primary external benchmark is BigCloneBench Version 2 as distributed for
BigCloneEval.

The associated IJaDataset / BigCloneEval distribution will provide the source
material and benchmark metadata.

The exact acquired artifacts, source URLs, acquisition date, archive hashes,
database hashes, and relevant repository revision identifiers must be recorded
before extraction or measurement.

No older ERA release may be silently substituted for Version 2.

## Benchmark Interpretation

BigCloneBench is used according to its intended role as a clone-detection
benchmark.

Experiment 004 does not assume that all benchmark clone categories constitute
ground truth for unrestricted semantic or functional equivalence.

In particular, weak Type-3 / Type-4-style benchmark regions must not be
reinterpreted as universal semantic-equivalence labels.

Results will therefore be stratified by the benchmark metadata available for
clone type and syntactic-similarity region whenever those fields are available
in the frozen benchmark artifact.

## Unit of Comparison

The comparison unit is a benchmark code fragment corresponding to the source
location identified by the benchmark.

This differs from Experiments 002 and 003, where the comparison unit was a
complete submission.

The difference in comparison granularity must be stated in all cross-experiment
interpretation.

Experiment 004 must not manufacture artificial whole submissions around benchmark
fragments merely to imitate the earlier fixture design.

## Fixed Comparison Conditions

C0 and C1 are frozen from Experiment 002.

C0:

- normalized Java token sequence
- order-sensitive sequence comparison
- normalized edit similarity

C1:

- complete Java method declarations as structural units
- submission-wide / comparison-unit method pooling where applicable
- full method similarity matrix
- deterministic maximum-weight one-to-one matching
- aggregation by matched similarity divided by max method count
- method-internal token order remains sensitive

Experiment 004 may add only the minimum deterministic adapter required to apply
these frozen definitions to benchmark fragments.

The adapter must not tune tokenization, matching, weighting, thresholds, or
similarity formulas in response to benchmark results.

If a benchmark fragment cannot be represented under a frozen condition, that
case must be recorded explicitly rather than silently repaired or discarded.

## No Parameter Tuning

No benchmark result may be used to tune C0 or C1.

No similarity threshold will be selected using Experiment 004.

No classifier will be trained.

No benchmark-specific weighting will be introduced.

No transformation-specific rule will be introduced.

## Corpus Acquisition Freeze

Before measurement, a separate corpus manifest must freeze:

- benchmark version
- acquisition source
- acquisition date
- upstream repository revision where applicable
- archive and/or database SHA-256 hashes
- extracted source inventory
- relevant licenses
- benchmark schema used
- source-location interpretation
- exclusions required for technical validity

Raw benchmark artifacts should not be committed to this repository when licensing,
size, or redistribution constraints make that inappropriate.

Instead, the repository must contain deterministic acquisition/setup instructions
and cryptographic hashes sufficient to identify the exact external artifacts.

## Sampling

The sampling procedure must be specified and frozen before C0/C1 similarities are
computed.

Sampling must be deterministic.

The sampling seed, eligibility rules, strata, requested sample sizes, and realized
sample sizes must be recorded.

Sampling should preserve benchmark categories needed for stratified analysis
rather than selecting examples based on SimProbe similarity.

No pair may be included or excluded because its C0 or C1 score appears favorable
or unfavorable.

## Primary Measurements

For every eligible sampled benchmark pair, record at minimum:

- stable benchmark pair identifier
- source locations for both fragments
- available benchmark clone category
- available syntactic-similarity region or value
- available functionality metadata
- C0 similarity
- C1 similarity
- C1 minus C0 paired change
- representation success/failure status

Additional provenance fields may be recorded if required to make the measurement
reproducible.

## Primary Analysis

Primary analysis will report:

1. C0 and C1 similarity distributions for the complete eligible sample.
2. Stratified distributions by benchmark clone category.
3. Stratified distributions by benchmark syntactic-similarity region when
   available.
4. Paired C1-minus-C0 changes.
5. Representation failure/exclusion counts and reasons.
6. Results by benchmark functionality where sample sizes permit descriptive
   interpretation.
7. Cross-experiment comparison with Experiments 002 and 003, explicitly noting
   the change from whole-submission controlled provenance pairs to external
   benchmark code fragments.

If suitable externally labeled negative/non-clone relations can be identified
from the frozen benchmark schema without constructing unsupported ground truth,
their analysis must be specified in a separate frozen measurement specification
before those results are computed.

They must not be invented by assuming arbitrary unlisted pairs are true
non-clones.

## BigCloneEval

Official BigCloneEval detector-recall evaluation is considered a separate
evaluation layer.

Experiment 004's primary pairwise similarity analysis does not claim official
BigCloneEval recall unless SimProbe is separately adapted to emit clone locations
and evaluated through the benchmark's coverage-based matching procedure.

Any such detector-recall extension must be frozen before execution and reported
separately from the primary similarity analysis.

## Reproducibility

All sampling, extraction, adaptation, measurement, and analysis code must be
deterministic.

Canonical generated artifacts must receive SHA-256 hashes.

The benchmark input hashes must be verified before every canonical measurement
run.

Measurement artifacts must be reproduced byte-for-byte before they are frozen.

## Scope and Claims

Experiment 004 may provide external evidence about SimProbe's behavior on the
frozen benchmark sample.

It does not by itself establish:

- a plagiarism threshold
- a plagiarism probability
- universal clone-detection accuracy
- universal semantic-equivalence detection
- performance on all programming languages
- performance on arbitrary unseen software populations

Similarity values remain descriptive measurements rather than plagiarism
probabilities.

## Decision Rule

The experiment will be interpreted from the joint behavior of robustness and
discrimination evidence.

No conclusion will be based solely on an increase in C1 similarity.

Unexpected or unfavorable results will be retained and reported rather than used
to revise the frozen C0/C1 definitions.
