# Experiment 004 - External Validation Sampling Specification

## Status

This specification is frozen before pair selection and before any SimProbe C0/C1 measurement.

- C0 measurements at freeze: 0
- C1 measurements at freeze: 0
- Sampling decisions use BigCloneBench metadata only.
- SimProbe similarity scores must not influence eligibility, sampling, exclusions, or replacement.

## Frozen inputs

- Experiment protocol commit: `8227fa6a070c4822c682baf052cfb35c285c2d2e`
- BigCloneBench acquisition commit: `2bc2b30b6fbced739c689d78d56fe92ca309298d`
- IJaDataset acquisition commit: `146d67936fa97d5a22563b34afe12f34cb6525d0`
- BCB database SHA-256: `C5453E3A7CE1604C52A35F3B931AFA9F70515B17B956A9DA472A13E2BCBAE43B`
- IJaDataset archive SHA-256: `657FE752838C882A6D0FA1A784608F84A4E8129C84B0504EC37D617B65F7433F`

## Pre-sampling benchmark census

Total BCB clone pairs: 8,584,153.

Syntactic-type counts:

- Type 1: 48,116
- Type 2: 4,234
- Type 3: 8,531,803

BCB pair TYPE counts:

- sample-sample: 206
- sample-tagged: 42,175
- tagged-tagged: 8,541,772

BCB INTERNAL counts:

- false: 8,375,313
- true: 208,840

Integrity census:

- null SIMILARITY_TOKEN values: 0
- self-pairs: 0
- missing FUNCTION_ID_ONE references: 0
- missing FUNCTION_ID_TWO references: 0

## Analysis strata

The primary balanced sample uses six strata:

1. `TYPE1`: `SYNTACTIC_TYPE = 1`.
2. `TYPE2`: `SYNTACTIC_TYPE = 2`.
3. `VST3_90_100`: `SYNTACTIC_TYPE = 3` and `0.90 <= SIMILARITY_TOKEN < 1.00`.
4. `ST3_70_90`: `SYNTACTIC_TYPE = 3` and `0.70 <= SIMILARITY_TOKEN < 0.90`.
5. `MT3_50_70`: `SYNTACTIC_TYPE = 3` and `0.50 <= SIMILARITY_TOKEN < 0.70`.
6. `WT3_T4_0_50`: `SYNTACTIC_TYPE = 3` and `0.00 <= SIMILARITY_TOKEN < 0.50`.

Type-3 records with SIMILARITY_TOKEN = 1.00 are not part of the four Type-3 similarity-region strata because the documented upper boundary of the very-strong region is exclusive.
They remain part of the benchmark census but are outside this balanced primary sample unless separately accounted for before measurement.

Observed census counts using these strata:

Correction note: the initial metadata census reported 14,081 Type-3 pairs at SIMILARITY_TOKEN >= 0.90. That query omitted the frozen upper-bound condition SIMILARITY_TOKEN < 1.00. A pre-selection boundary check found 386 Type-3 pairs with SIMILARITY_TOKEN = 1.00. Therefore the corrected VST3_90_100 count is 13,695, and those 386 exact-1.00 Type-3 pairs are outside the six-stratum primary sampling universe.

- TYPE1: 48,116
- TYPE2: 4,234
- VST3_90_100: 13,695
- ST3_70_90: 161,662
- MT3_50_70: 2,535,847
- WT3_T4_0_50: 5,820,213

## Requested sample

Requested primary sample size: 1,000 pairs per stratum.

- TYPE1: 1,000
- TYPE2: 1,000
- VST3_90_100: 1,000
- ST3_70_90: 1,000
- MT3_50_70: 1,000
- WT3_T4_0_50: 1,000

Total requested primary sample: 6,000 clone pairs.

This is a balanced validation design. It deliberately does not reproduce the natural frequency of BCB categories. Therefore pooled unweighted statistics over the 6,000-pair sample must not be interpreted as population-prevalence estimates for BigCloneBench.

## Deterministic selection

Pair selection must be deterministic and independent of SimProbe scores.

For each eligible pair, construct the canonical pair key:

`min(FUNCTION_ID_ONE, FUNCTION_ID_TWO):max(FUNCTION_ID_ONE, FUNCTION_ID_TWO)`

The selection key is the uppercase hexadecimal SHA-256 digest of:

`SIMPROBE-EXP004|20261002|<STRATUM>|<canonical-pair-key>`

Within each stratum:

1. compute the selection key;
2. sort ascending by selection key;
3. use canonical pair key as the deterministic secondary sort key;
4. take the first 1,000 technically eligible pairs.

No random-number generator, database RAND function, C0 score, C1 score, or manual preference may influence selection.

## Technical eligibility

A sampled pair is technically eligible for measurement only when both referenced BCB FUNCTIONS records can be resolved deterministically to the acquired IJaDataset and their declared source intervals are valid.

For each side of a pair:

- the FUNCTIONS record must exist;
- TYPE must resolve to the corresponding acquired dataset directory;
- NAME must resolve to an existing Java source file;
- STARTLINE must be at least 1;
- ENDLINE must be at least STARTLINE;
- ENDLINE must not exceed the physical source-file line count;
- the declared fragment must be readable as bytes/text by the frozen adapter.

No pair is excluded merely because it is difficult for SimProbe, has low syntactic similarity, belongs to a particular functionality or project, is intra-project/inter-project, or has INTERNAL=true.

## Representation failures

Technical source-resolution failures are eligibility failures and must be recorded with an explicit reason.

After a technically eligible pair is selected, inability of the frozen SimProbe adapter to represent one or both fragments is a representation failure. Such a pair must remain in the realized sample and be reported as a failure; it must not be silently replaced based on the resulting SimProbe behavior.

The selection implementation may scan farther down the deterministic ordering only to obtain 1,000 technically eligible source-resolvable pairs per stratum. Every skipped candidate and reason must be recorded.

## Duplicate policy

Canonical function-pair identity is unordered.
The same canonical pair must not occur more than once in the realized primary sample.
A pair cannot belong to more than one primary stratum under the frozen rules.

## Metadata retained

The frozen sample manifest must retain at least:

- stratum
- deterministic selection rank/key
- FUNCTION_ID_ONE
- FUNCTION_ID_TWO
- canonical pair key
- FUNCTIONALITY_ID
- benchmark TYPE
- SYNTACTIC_TYPE
- SIMILARITY_LINE
- SIMILARITY_TOKEN
- INTERNAL
- source TYPE/NAME/STARTLINE/ENDLINE for both fragments
- PROJECT for both fragments
- source-resolution eligibility status
- exclusion/failure reason where applicable

## Negatives

The primary sampling procedure covers BCB CLONES only.
FALSE_POSITIVES are not treated as general negative/non-clone examples under this specification.
Any negative-pair study requires a separate frozen specification before those pairs are measured.

## Measurement boundary

Pair selection and source-resolution validation occur before C0/C1 measurement.
The realized sample manifest, realized stratum counts, exclusions, and manifest SHA-256 must be frozen in Git before the first SimProbe similarity score is computed.

No result from Experiment 004 may be used to revise C0/C1 tokenization, matching, weighting, aggregation, thresholds, sampling rules, or this specification.
