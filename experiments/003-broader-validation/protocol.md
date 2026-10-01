# Experiment 003: Broader Validation

## Status

Protocol frozen before construction of the Experiment 003 primary fixture and
before generation or inspection of any Experiment 003 similarity measurements.

## Purpose

Experiment 003 tests whether the main Experiment 002 finding persists across a
substantially broader controlled Java fixture.

Experiment 002 found that the frozen C1 structure-aware comparison increased
robustness to METHOD_REORDER and CLASS_SPLIT relative to the frozen C0
order-sensitive sequence comparison while mean cross-family control similarity
did not increase.

Experiment 003 is a replication and broader-validation experiment.

It must not tune C0 or C1 in response to Experiment 002 or Experiment 003
results.

## Primary research question

Across a larger collection of independently constructed Java program families,
does the frozen C1 structure-aware comparison retain its advantage over the
frozen C0 order-sensitive comparison for METHOD_REORDER and CLASS_SPLIT without
a corresponding increase in cross-family control similarity?

## Hypotheses

### H1: METHOD_REORDER robustness

BASE-to-METHOD_REORDER similarity will be higher under C1 than under C0.

### H2: CLASS_SPLIT robustness

BASE-to-CLASS_SPLIT similarity will be higher under C1 than under C0.

### H3: Identifier-renaming invariance

IDENTIFIER_RENAME should remain highly invariant under both conditions because
the frozen lexical normalization abstracts identifiers.

This is primarily a validation check rather than a claimed new C1 advantage.

### H4: Control-side discrimination

Any increase in related-pair similarity under C1 must be interpreted jointly
with cross-family control similarity.

A robustness gain is not an unqualified improvement if cross-family similarity
rises enough to weaken related/control separation.

### H5: Replication of Experiment 002 direction

The direction of the following Experiment 002 observations will be checked on
the broader fixture:

- C1 improves BASE-to-METHOD_REORDER retention relative to C0.
- C1 improves BASE-to-CLASS_SPLIT retention relative to C0.
- C1 does not merely create the appearance of robustness by broadly inflating
  cross-family control similarity.
- related/control separation is evaluated jointly with transformation
  retention.

Experiment 003 does not require numerical equality with Experiment 002.

## Experimental language

Java.

## Experimental unit

One complete program submission.

A submission may contain one or more Java source files.

## Provenance-family design

The primary fixture contains exactly 12 independently constructed program
families.

Each family implements a different small deterministic programming task.

Families must not be created by mechanically renaming, lightly rewriting, or
transforming another family.

Shared Java language syntax, standard-library idioms, and ordinary programming
constructs are allowed.

Each family must be independently specified before its implementation is
frozen.

## Submissions per family

Each family contains exactly four submissions:

1. BASE
2. METHOD_REORDER
3. CLASS_SPLIT
4. IDENTIFIER_RENAME

Therefore the primary fixture contains:

- 12 families
- 4 submissions per family
- 48 submissions total

## Pair counts

All unordered submission pairs are measured under each comparison condition.

For 48 submissions:

C(48, 2) = 1128 unordered pairs per condition.

Within each family:

C(4, 2) = 6 related pairs.

Across 12 families:

12 * 6 = 72 related pairs per condition.

Therefore:

1128 - 72 = 1056 cross-family control pairs per condition.

Across C0 and C1 together:

- 2256 primary measurement rows
- 144 related rows
- 2112 control rows

These counts are frozen before measurement.

## Transformation definitions

The transformation definitions intentionally replicate Experiment 002.

### BASE

Each BASE program must contain:

- one public top-level entry class;
- `main`;
- at least four behavior-relevant user-defined helper methods in addition to
  `main`;
- calls among helpers sufficient for helper declaration order to be a
  meaningful source-order property;
- functionality that can be moved into one additional top-level class without
  changing intended program behavior.

### METHOD_REORDER

METHOD_REORDER must:

- materially change helper-method declaration order;
- preserve the public entry class;
- preserve method names;
- preserve parameters;
- preserve local identifiers;
- preserve method bodies;
- preserve literals;
- preserve operators;
- preserve calls;
- preserve intended behavior.

The transformation must not intentionally introduce unrelated edits.

### CLASS_SPLIT

CLASS_SPLIT must:

- retain the original public entry class;
- add exactly one additional user-defined top-level class;
- move at least two behavior-relevant helper methods into the additional class;
- exercise functionality in the additional class during normal execution;
- preserve intended behavior;
- make no intentional logic change beyond changes required by the structural
  move.

The additional class may be stored in a separate Java source file.

### IDENTIFIER_RENAME

IDENTIFIER_RENAME must:

- rename the public entry class and corresponding Java filename;
- rename all behavior-relevant helper methods;
- materially rename parameters and local variables;
- update all affected references;
- preserve literals;
- preserve operators;
- preserve control flow;
- preserve method declaration order;
- preserve intended behavior.

Java language and standard-library identifiers must not intentionally be
renamed.

## Behavioral validation

Each family specification must declare at least three deterministic tests.

Before the complete primary fixture is frozen:

- every submission must compile independently;
- every declared test must be executed against every submission in its family;
- stdout must match the declared expected output exactly;
- generated `.class` files must be removed.

With 12 families, four submissions per family, and three declared tests per
family, the minimum primary behavioral-validation count is:

12 * 4 * 3 = 144 executions.

More tests may be frozen in a family specification before similarity
measurement, but tests must not be added in response to observed primary
similarity results.

## Frozen comparison conditions

Experiment 003 reuses the Experiment 002 comparison conditions without
algorithmic modification.

### C0

C0 is the deterministic order-sensitive abstract lexical sequence comparison
frozen for Experiment 002.

Its lexical normalization, multi-file ordering, file-boundary handling,
Levenshtein distance, normalization formula, and edge cases must remain
unchanged.

### C1

C1 is the deterministic structure-aware method-unit comparison frozen for
Experiment 002.

Its method extraction, lexical normalization, unit similarity, exact
maximum-weight one-to-one matching, deterministic tie handling, unmatched-unit
penalty, aggregation formula, and edge cases must remain unchanged.

## Implementation reuse rule

The committed Experiment 002 comparison implementation is the reference
implementation for Experiment 003.

Experiment 003 must not alter the comparison algorithm to improve performance
on the new fixture.

If a genuine implementation defect prevents application to a valid frozen
fixture, the defect must be documented explicitly before correction.

A correction must not be justified merely because a resulting similarity score
is surprising or undesirable.

## No primary tuning

After Experiment 003 similarity measurements have been generated or inspected,
the following may not be changed for the primary experiment:

- family membership;
- program behavior;
- transformations;
- declared behavioral tests;
- comparison conditions;
- lexical normalization;
- structural-unit extraction;
- matching;
- aggregation;
- pair labels;
- primary statistics.

A genuine defect may be corrected only through a transparent correction record
and complete rerun.

## Pair labels

For every comparison condition:

- submissions from the same provenance family are `related`;
- submissions from different provenance families are `control`.

No additional primary pair label is used.

## Primary measurements

For every unordered pair under C0 and C1, record the same audit information
used by Experiment 002, including:

- left and right submission identifiers;
- family identifiers;
- variant identifiers;
- pair label;
- comparison condition;
- C0 token counts and edit distance where applicable;
- C1 method counts, matched count, and matched-similarity sum where applicable;
- final similarity.

Similarity remains in [0, 1].

## Primary descriptive analysis

For each condition, report related and control:

- count;
- mean;
- median;
- minimum;
- first quartile;
- third quartile;
- maximum.

Also report:

- related-control mean gap;
- empirical related-vs-control ordering probability, with ties contributing
  0.5;
- exact similarity-1.0 collisions for related and control pairs;
- BASE-to-METHOD_REORDER retention;
- BASE-to-CLASS_SPLIT retention;
- BASE-to-IDENTIFIER_RENAME retention;
- count, mean, minimum, maximum, and population standard deviation for each
  BASE-to-transformation group;
- paired C1-minus-C0 change across all related pairs;
- paired C1-minus-C0 change across all control pairs;
- paired C1-minus-C0 change for each BASE-to-transformation group.

## Family-level replication analysis

Because Experiment 003 contains 12 families, transformation effects must also
be reported at family level.

For METHOD_REORDER and CLASS_SPLIT separately, report:

- each family's C0 BASE-to-transformation similarity;
- each family's C1 BASE-to-transformation similarity;
- each family's C1-minus-C0 delta;
- number of families with positive delta;
- number with zero delta;
- number with negative delta;
- median family-level delta.

This prevents a large mean effect from hiding inconsistent behavior across
families.

## Control analysis

Control behavior must not be reduced to a single mean.

In addition to the primary control distribution, report:

- control C1-minus-C0 delta distribution;
- maximum control similarity under each condition;
- upper control quartile under each condition;
- exact control collisions;
- count and proportion of controls whose C1 similarity exceeds their C0
  similarity.

This analysis is descriptive.

## Cross-experiment comparison

After Experiment 003 primary results are frozen, compare the direction of its
findings with Experiment 002.

The comparison must distinguish:

- replication of direction;
- differences in magnitude;
- new failure cases;
- changes in control behavior.

Experiment 002 must not be retroactively modified.

## No primary classification threshold

Experiment 003 does not select or optimize a plagiarism-detection threshold.

No threshold may be chosen post hoc from the primary results and presented as
a preregistered primary result.

## No plagiarism probability

Similarity scores are not plagiarism probabilities.

Related/control ordering probability is a descriptive pair-separation
statistic and is not a probability that a submission is plagiarized.

## Reproducibility

Before interpretation:

- the fixture must be committed;
- the comparison implementation used must be identified by commit;
- the primary runner must be committed;
- the canonical primary output must be hashed with SHA-256;
- a second independent run must reproduce the canonical output byte-for-byte.

## Interpretation constraints

Experiment 003 is broader controlled validation, not universal external
validation.

Twelve independently constructed families provide stronger evidence than the
four-family Experiment 002 fixture, but they do not represent all Java
programs, educational assignments, repositories, or plagiarism strategies.

Claims must therefore remain scoped to the tested fixture and transformations.

## Relationship to real-world benchmarks

A later evaluation may use an established real-world Java clone benchmark such
as BigCloneBench.

That evaluation is separate from this controlled replication because benchmark
clone labels, fragment boundaries, and evaluation targets differ from
SimProbe's controlled whole-submission provenance-family design.

Experiment 003 must not be redesigned after measurement merely to imitate a
benchmark.

## Freeze sequence

The intended sequence is:

1. freeze this protocol;
2. freeze the 12 family specifications and declared tests;
3. implement BASE submissions;
4. implement controlled transformations;
5. behaviorally validate all submissions;
6. freeze the complete primary fixture;
7. freeze the Experiment 003 measurement/runner specification;
8. verify reuse of the frozen C0/C1 implementation;
9. commit the primary runner before execution;
10. generate the canonical primary measurements;
11. verify byte-for-byte reproducibility;
12. commit the canonical measurements;
13. perform and commit the primary analysis;
14. perform the cross-experiment interpretation.

No primary similarity measurement may be generated before the relevant fixture,
measurement rules, implementation reference, and runner are frozen.
