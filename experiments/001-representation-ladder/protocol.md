# Experiment 001 — Representation Ladder

## Status

Pre-implementation experimental protocol.

This experiment is defined before implementation of the primary representation
ladder and before inspection of its primary measurements.

## Objective

Experiment 001 investigates how progressively abstracting Java source code
changes two separate properties:

1. robustness to controlled source-code transformations; and
2. discrimination among programs with different provenance.

The experiment is designed to identify where transformation invariance is
gained and where representation or similarity ambiguity increases.

It is not designed to detect plagiarism.

## Research question

> At which representation-abstraction stages does transformation invariance
> increase, and what discriminative information is lost at those same stages?

## Hypotheses

### H1 — Transformation invariance

At least some abstraction stages will increase similarity between a base
program and its controlled transformed variants.

### H2 — Discriminative loss

At least some abstraction stages will also increase similarity, collisions,
ties, or neighborhood density among controls with different provenance.

### H3 — Unequal abstraction effects

Different abstraction operations will not contribute equally to invariance
gain or discriminative loss.

### H4 — Pair score versus cohort context

Pairs having the same or similar pairwise similarity may differ substantially
in cohort-conditioned distinctiveness.

These hypotheses may be rejected by the results.

## Subject language

Java is the only subject language in Experiment 001.

## Experimental unit

The unit of comparison is a complete program submission.

A submission may contain multiple Java source files.

File names, class names, method names, and source positions are not assumed to
correspond across submissions unless a particular representation explicitly
uses that information.

## Fixture design

The primary fixture will contain multiple independently constructed provenance
families.

Each family begins with a base implementation.

Controlled variants are generated from that family's base according to
predeclared transformation classes.

Programs derived from the same base are labelled `related` for the purpose of
this controlled experiment.

Programs belonging to different independently constructed provenance families
are labelled `control`.

These labels describe experimental provenance only. They do not represent
plagiarism or misconduct.

## Minimum primary fixture

The initial primary fixture will contain four provenance families.

Each family will contain:

- BASE
- IDENTIFIER_RENAME
- METHOD_REORDER
- CLASS_RENAME
- FILE_RENAME
- DEAD_CODE
- CLASS_SPLIT

This gives seven submissions per family and 28 submissions in the initial
primary fixture.

Additional variants must not be added to the primary fixture after inspecting
primary results unless they are reported as a separate follow-up experiment.

## Provenance-family construction

The four base families must implement intentionally different small programs or
different computational tasks.

They should differ in meaningful lexical and structural characteristics while
remaining small enough for manual inspection.

The families must be written before similarity results are inspected.

They must not be redesigned merely because a particular family produces an
unexpected collision.

Any fixture defect that requires correction must be documented.

## Controlled transformations

### T1 — IDENTIFIER_RENAME

Rename user-defined identifiers while preserving intended program behavior.

Candidate targets include:

- local variables;
- parameters;
- methods; and
- user-defined classes where appropriate.

The transformation must not intentionally alter literals, operators, or
control flow.

### T2 — METHOD_REORDER

Reorder method declarations without intentionally changing behavior.

### T3 — CLASS_RENAME

Rename one or more user-defined classes and update references accordingly.

### T4 — FILE_RENAME

Rename source files where Java naming constraints permit it, updating
corresponding declarations if required.

### T5 — DEAD_CODE

Insert code that is intended not to affect observable behavior.

The inserted code must be documented.

### T6 — CLASS_SPLIT

Move selected functionality into an additional class while preserving the
intended externally observable behavior.

This transformation intentionally changes architecture more substantially than
simple renaming.

## Behavioral validation of transformations

Controlled variants are intended to preserve behavior relative to their family
base.

Where practical, fixture tests will verify expected outputs for declared test
inputs.

Passing those tests is evidence for the tested behaviors only and is not a
formal proof of semantic equivalence.

## Representation ladder

The primary ladder is frozen conceptually as follows.

### R0 — Raw lexical tokens

Java lexical tokens with user-written token values preserved.

Comments and whitespace are not treated as semantic tokens.

### R1 — Canonical lexical stream

A deterministic lexical token stream after exclusion of comments and
formatting differences.

R0 and R1 may turn out to be equivalent under the selected lexer. If so, that
result will be retained rather than artificially creating a difference.

### R2 — Identifier normalization

R1 with user-defined identifiers mapped to an identifier category.

Keywords remain distinct.

Literals, operators, and punctuation remain preserved.

### R3 — Literal normalization

R2 with literals mapped to declared literal categories.

Examples may include:

- integer literal;
- floating-point literal;
- string literal;
- character literal;
- boolean literal;
- null literal.

Literal values are no longer preserved at this stage.

### R4 — Selected name/type abstraction

R3 with additional selected name or type information abstracted.

The exact abstraction rule must be documented in the implementation before
primary measurements are generated.

R4 must not be changed after inspecting primary results without creating a
separate protocol revision.

### R5 — Structural syntax representation

Represent source using selected Java syntax/node categories rather than the
full lexical token stream.

The exact node inclusion/exclusion rules must be documented before primary
measurement.

### R6 — Aggressive structural abstraction

An intentionally information-poor structural representation used to examine
the high-invariance/high-degeneracy end of the representation ladder.

R6 is not assumed to be a desirable production representation.

Its purpose is experimental.

## Similarity function

Experiment 001 will initially use one deterministic, documented similarity
function across compatible representation levels wherever practical.

The similarity function must be selected and implemented before primary
results are inspected.

Changing the primary similarity function after viewing results requires a
protocol revision or separate follow-up analysis.

Similarity values are measurements only.

They must not be interpreted as probabilities of plagiarism or common
authorship.

## Primary measurements

For every representation level, record:

### Pairwise similarity

Similarity for every unordered submission pair.

### Related-pair distribution

Distribution of similarity values for pairs sharing controlled provenance.

### Control-pair distribution

Distribution of similarity values for pairs belonging to different provenance
families.

### Exact representation collisions

Number and size of groups whose complete representations are exactly equal.

### Maximal-score multiplicity

Number of pairs receiving the maximum possible similarity value where the
similarity function has a defined maximum.

### Score-tie multiplicity

Frequency and size of tied similarity values.

### Representation entropy

Empirical entropy over exact representation classes within the cohort.

### Neighborhood density

Similarity-neighborhood density evaluated across a predeclared threshold grid
or complete density curve.

A single favorable threshold must not be selected after results are observed.

### Rank-based distinctiveness

For each submission, rank other submissions by similarity and record where
related and control pairs appear.

## Derived measurements

The analysis may derive:

- change in related-pair similarity between adjacent representation stages;
- change in control-pair similarity;
- change in exact-collision frequency;
- change in entropy;
- change in tie pressure;
- change in neighborhood density.

Derived quantities must retain the underlying raw measurements.

## Primary comparison

The primary comparison is not:

> Which representation produces the highest similarity?

Instead, each stage is evaluated on two dimensions:

1. transformation invariance; and
2. discriminative loss / cohort ambiguity.

The analysis will examine the trade-off between these dimensions.

No representation will be declared universally best from this experiment.

## Cohort-perturbation subexperiment

A target pair will be selected according to a rule defined before the
subexperiment's results are inspected.

The source code and pairwise representation of the target pair will remain
unchanged.

The surrounding cohort will then be varied using predetermined additions or
removals.

For each cohort configuration record:

- target pair similarity;
- target pair ranks;
- neighborhood density;
- score-tie multiplicity where applicable;
- representation multiplicity where applicable.

The purpose is to test whether pairwise similarity can remain unchanged while
cohort-conditioned distinctiveness changes.

## No post-hoc fixture tuning

After primary results are generated:

- families must not be removed because they create inconvenient results;
- transformations must not be removed because they fail to increase
  similarity;
- controls must not be removed because they become highly similar;
- representation stages must not be silently redefined;
- thresholds must not be selected solely because they improve separation.

Corrections for genuine implementation or fixture defects must be documented,
versioned, and rerun transparently.

## Negative-result criteria

Results weakening the motivating hypothesis include:

- abstraction providing little or no transformation-invariance gain;
- abstraction producing no meaningful increase in ambiguity;
- cohort-conditioned measurements closely duplicating pairwise similarity;
- entropy changes failing to correspond to observable representation collapse;
- control behavior being dominated by one artificial fixture family;
- results being highly unstable under reasonable cohort perturbation.

These results will be retained.

## Interpretation constraints

Experiment 001 does not establish:

- plagiarism-detection accuracy;
- authorship;
- misconduct;
- a universal similarity threshold;
- superiority over JPlag;
- superiority over another detector;
- generalization to real student cohorts;
- semantic equivalence of transformed programs;
- scientific novelty of SimProbe.

The experiment is a controlled diagnostic study.

## Reproducibility requirements

The frozen experiment must record:

- source files;
- provenance labels;
- transformation labels;
- representation configuration;
- software versions;
- exact execution commands;
- complete pairwise measurements;
- analysis outputs;
- random seeds if randomness is introduced;
- cryptographic hashes of frozen primary result artifacts.

## External comparison

JPlag and additional baselines are intentionally not part of the first
measurement.

Experiment 001 first validates the representation-ladder methodology itself.

External comparison will be introduced under a separate frozen protocol so
that baseline configuration is not selected in response to Experiment 001
results.

## Success criterion

Experiment 001 is successful as a research experiment if it produces a
reproducible characterization of how the declared representation stages affect
invariance and cohort discrimination.

Confirmation of the hypotheses is not required for experimental success.