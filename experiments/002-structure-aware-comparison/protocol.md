# Experiment 002 Protocol: Structure-Aware Comparison

## Status

Pre-implementation experimental protocol.

This protocol must be committed before Experiment 002 fixtures,
representations, comparison implementations, or primary measurements are
constructed or inspected.

## Motivation

Experiment 001 evaluated a frozen ladder of increasingly abstract Java
representations using normalized token-sequence Levenshtein similarity.

Its corrected primary analysis found transformation-specific tradeoffs.

Name-oriented transformations became highly or exactly invariant at suitable
abstraction stages. In contrast, METHOD_REORDER remained substantially
non-invariant, and CLASS_SPLIT was the lowest-retention BASE transformation at
every representation stage.

Experiment 001 also showed that stronger abstraction can increase similarity
among cross-family control pairs. Therefore, simply discarding more
information is not sufficient evidence of improvement.

Experiment 002 tests a separate question: whether comparison methods that are
less dependent on global source order can improve robustness to structural
rearrangement while retaining distinction between independent provenance
families.

Experiment 002 does not modify or replace Experiment 001.

## Primary research question

Can a deterministic structure-aware comparison improve similarity retention
under method reordering and class splitting, relative to an order-sensitive
sequence baseline, without a corresponding collapse in cross-family
distinction on the frozen Experiment 002 fixture?

## Hypotheses

### H1: method-reordering invariance

A representation/comparison that treats method-level units independently of
their source declaration order will retain higher BASE-to-METHOD_REORDER
similarity than the order-sensitive sequence baseline.

### H2: class-split robustness

A submission-level structural comparison that aggregates information across
all source files will retain higher BASE-to-CLASS_SPLIT similarity than the
order-sensitive sequence baseline.

Exact invariance is not required.

### H3: control preservation

Any gain in related-pair invariance must be interpreted together with
cross-family control similarity.

A method is not considered descriptively improved merely because related
similarity increases if control similarity increases comparably.

### H4: transformation specificity

The effect of structure-aware comparison may differ by transformation.
METHOD_REORDER and CLASS_SPLIT will therefore be reported separately rather
than only through an aggregate related-pair statistic.

## Subject language

Java.

## Experimental unit

The experimental unit is one complete program submission.

A submission may contain one or more Java source files.

Source filenames, class names, method names, and declaration positions are not
assumed to identify provenance unless the frozen representation explicitly
uses them.

## Fixture design

Experiment 002 will use independently constructed provenance families.

Each family will contain one BASE submission and controlled transformed
variants.

The primary fixture will be frozen before primary similarity measurements are
generated.

No family or transformation may be added, removed, or rewritten in response
to primary similarity results except through an explicit documented
correction of a genuine implementation or fixture defect.

## Minimum primary fixture

The primary fixture will contain four independent provenance families.

Each family will contain:

- BASE
- METHOD_REORDER
- CLASS_SPLIT
- IDENTIFIER_RENAME

This produces five submissions per family only if an additional frozen
control transformation is specified before fixture construction; otherwise
the required set above produces four submissions per family.

The final exact submission count must be resolved and frozen in the fixture
specification before implementation.

The fixture specification must define input/output behavior and declared
behavioral tests for every provenance family.

## Required transformations

### T1: METHOD_REORDER

Reorder method declarations without intentionally changing observable program
behavior.

The transformation must change declaration order materially; a no-op reorder
is not permitted.

### T2: CLASS_SPLIT

Move selected behavior-relevant functionality into at least one additional
class while preserving intended observable behavior.

The transformation must involve actual redistribution of functionality rather
than merely adding an unused class.

### T3: IDENTIFIER_RENAME

Rename user-defined identifiers without intentionally altering literals,
operators, control flow, or program behavior.

This transformation provides a lexical/name-oriented comparison point against
the structural transformations.

## Behavioral validation

Every transformed submission is intended to preserve the externally observable
behavior of its BASE submission on the declared fixture domain.

Where practical, all BASE and transformed submissions must be compiled and run
against the same declared family tests before measurement.

Passing tests are evidence of tested behavioral preservation, not formal proof
of semantic equivalence.

## Comparison conditions

Experiment 002 must include at least two comparison conditions.

### C0: order-sensitive baseline

A deterministic sequence-based comparison condition will provide the baseline.

The exact representation and similarity function must be frozen before
primary measurements.

The baseline should preserve the relevant order sensitivity demonstrated in
Experiment 001 rather than being redesigned after Experiment 002 results.

### C1: structure-aware comparison

A deterministic comparison will represent a submission as structural units
whose global comparison is less dependent on source declaration order.

The implementation may operate on method-level, class-level, or other
syntactically defined units, but the exact extraction, normalization,
matching, aggregation, and tie-breaking rules must be documented and frozen
before primary measurements.

The primary structure-aware method must not depend on manually supplied
correspondence between transformed and BASE methods or classes.

## Structure-aware design constraints

Before measurement, the implementation specification must state:

- how Java source is parsed or scanned;
- what constitutes a structural unit;
- which lexical information is preserved or abstracted;
- whether literals are preserved or categorized;
- whether user-defined names are preserved or abstracted;
- how units from multiple source files are combined;
- whether source filenames influence the representation;
- how units from two submissions are matched;
- how unmatched units affect similarity;
- how per-unit scores are aggregated;
- how ties are resolved;
- the exact similarity range and edge cases.

All rules must be deterministic.

## Avoiding trivial order invariance

The structure-aware condition must not achieve order invariance merely by
sorting the complete lexical token stream.

Any canonical ordering must operate on documented structural units and must
not silently discard the internal structure needed for the comparison.

## Pair construction

All unordered pairs of frozen primary submissions will be measured under every
frozen comparison condition.

Pairs from the same provenance family are labeled `related`.

Pairs from different provenance families are labeled `control`.

The primary analysis will additionally identify BASE-to-transformation pairs
for transformation-specific retention statistics.

## Primary measurements

For every submission pair and comparison condition, record at least:

- left submission ID;
- right submission ID;
- left family;
- right family;
- left variant;
- right variant;
- pair label;
- comparison condition;
- similarity;
- any deterministic component counts needed to audit the score.

The exact output schema must be frozen before primary measurement.

## Primary descriptive analysis

The primary analysis will report, for each comparison condition:

- related similarity distribution;
- control similarity distribution;
- related mean and median;
- control mean and median;
- related-minus-control mean difference;
- empirical probability that a randomly selected related score exceeds a
  randomly selected control score, with ties counted as one half;
- exact-similarity collision counts for related and control pairs.

For each required transformation, BASE-to-transformation similarity will be
reported separately across provenance families.

METHOD_REORDER and CLASS_SPLIT must not be hidden inside only an aggregate
related statistic.

## Comparison of C0 and C1

The primary comparison will describe:

- change in BASE-to-METHOD_REORDER retention;
- change in BASE-to-CLASS_SPLIT retention;
- change in IDENTIFIER_RENAME retention;
- change in control similarity;
- change in related/control distribution separation;
- change in exact control collisions.

No single statistic will define success by itself.

## No primary classification threshold

Experiment 002 will not choose a plagiarism-detection threshold from the
primary fixture.

Similarity values are experimental measurements, not plagiarism
probabilities.

No claim about real-world plagiarism classification performance follows
directly from this experiment.

## Interpretation criterion

Evidence consistent with the structure-aware approach being useful would
consist of increased robustness to METHOD_REORDER and/or CLASS_SPLIT together
with evidence that cross-family distinctions have not simply collapsed.

A gain in transformation retention accompanied by comparable or larger growth
in unrelated/control similarity must be reported as a tradeoff rather than an
unqualified improvement.

## No post-hoc tuning

After primary results are inspected, the following may not be changed in
response to those results:

- provenance families;
- required transformations;
- declared behavioral tests;
- comparison conditions;
- representation rules;
- unit matching rules;
- aggregation rules;
- similarity functions;
- pair labels;
- primary descriptive statistics.

A genuine implementation or fixture defect may be corrected only if the
correction is documented, versioned, and followed by a transparent rerun.

The original affected run must remain identifiable in the experimental
provenance.

## Reproducibility

The frozen fixture, comparison implementation, measurement runner, and
analysis procedure must be version-controlled.

Before interpretation, the primary measurement run must be repeated from the
same frozen commit and checked for deterministic byte-for-byte output where
practical.

Primary result artifacts must be identified by cryptographic hash.

## Relationship to Experiment 001

Experiment 001 remains a completed experiment and must not be altered to make
Experiment 002 results more favorable.

Experiment 002 is a follow-up motivated by the observed sensitivity of
order-based sequence similarity to METHOD_REORDER and CLASS_SPLIT.

Any comparison between experiments must account for differences in fixture
design and measurement conditions and must not treat scores from different
fixtures as directly interchangeable without justification.

## Next freeze points

After this protocol is committed, work proceeds in the following order:

1. freeze the Experiment 002 fixture specification;
2. implement and validate BASE submissions;
3. construct and validate controlled transformations;
4. freeze the complete primary fixture;
5. freeze the exact C0 and C1 measurement specification;
6. implement the comparison methods and tests;
7. freeze the primary measurement runner;
8. generate and reproduce the primary measurements;
9. record the run hashes;
10. perform the frozen descriptive analysis.

No primary similarity results should be inspected before the applicable
fixture and measurement freeze points are committed.
