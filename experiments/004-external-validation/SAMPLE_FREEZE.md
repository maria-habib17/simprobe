# Experiment 004 Sample Freeze

Status: frozen before all C0/C1 measurements.

## Provenance

- sampling specification commit: 72b2fabbfc8818cc6fddd64b392293b5494a796b
- VST3 census correction commit: eee364fe5ff6f76b11b47a6b4e976a70c4db902e
- canonical-pair deduplication rule commit: 6a3711b922a27c06ef84d5e138dd72d30a4896c6
- canonical BCB database SHA-256: C5453E3A7CE1604C52A35F3B931AFA9F70515B17B956A9DA472A13E2BCBAE43B

## Realized sample

- requested pairs: 6000
- realized pairs: 6000
- unique canonical pairs: 6000
- strata: 6
- pairs per stratum: 1000
- technical source exclusions: 0
- selected multi-label pairs: 9

Strata:

- TYPE1: 1000
- TYPE2: 1000
- VST3_90_100: 1000
- ST3_70_90: 1000
- MT3_50_70: 1000
- WT3_T4_0_50: 1000

## Duplicate handling

Sampling was performed over unique canonical function pairs rather than raw CLONES row multiplicity, according to the rule frozen in SAMPLING_DEDUPLICATION.md.

During the retained-candidate scan, 22 duplicate rows were observed. All functionality labels for retained canonical pairs were collected in a second complete pass over the candidate export.

The realized sample contains 9 canonical pairs with multiple FUNCTIONALITY_ID labels. Their labels are retained in sorted semicolon-separated form.

## Validation

- independent canonical-pair-key recomputation: PASS
- independent SHA-256 selection-key recomputation: PASS
- canonical-pair uniqueness: PASS
- selection ranks 1 through 1000 in every stratum: PASS
- all realized pairs technically source-eligible: PASS
- canonical BCB database unchanged: PASS

## Frozen artifact hashes

- generate_sample.py SHA-256: C3F41D1CF6D0ED966C455ADEA87D839FC40B805FC706430FDFA62DAC663FCC78
- sample_manifest.csv SHA-256: 093808FA9EE1E4BFBFABCF169B52A06D7357AAACD1D46F6C80D8F2ADC745305B
- sampling_exclusions.csv SHA-256: 35E1A1EDDC169817E131E9FD8C3EA143047203B2011C5C1227F50B19E6C6C16A

## Measurement boundary

- C0 measurements before sample freeze: 0
- C1 measurements before sample freeze: 0

No SimProbe score was observed or used in sampling, exclusion, ranking, replacement, or validation.
