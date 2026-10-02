# Experiment 004 External Validation Analysis

## Status

Final analysis of the frozen Experiment 004 sample and measurements.

No sampled pair was replaced after observing adapter behavior or SimProbe scores.

## Realized sample

- Frozen sampled pairs: 6000
- Measured pairs: 5755 (95.9167%)
- Adapter-failure pairs: 245 (4.0833%)
- C0 measurements per measurable pair: 1
- C1 measurements per measurable pair: 1

## Overall C0/C1 result

- C0 mean similarity: 0.731551
- C1 mean similarity: 0.731574
- Mean paired delta (C1 - C0): 0.000023033
- Median paired delta: 0.000000000
- C1 > C0: 4 pairs
- C1 = C0 within 1e-12: 5745 pairs
- C1 < C0: 6 pairs
- Exact C0 similarity 1.0: 1946 pairs
- Exact C1 similarity 1.0: 1946 pairs

## Results by frozen stratum

| Stratum | Sample | Measured | Failures | Failure rate | C0 mean | C1 mean | Mean delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| MT3_50_70 | 1000 | 963 | 37 | 3.70% | 0.481267 | 0.481406 | 0.000138777 |
| ST3_70_90 | 1000 | 991 | 9 | 0.90% | 0.659696 | 0.659698 | 0.000002225 |
| TYPE1 | 1000 | 948 | 52 | 5.20% | 1.000000 | 1.000000 | 0.000000000 |
| TYPE2 | 1000 | 999 | 1 | 0.10% | 0.999993 | 0.999993 | 0.000000000 |
| VST3_90_100 | 1000 | 932 | 68 | 6.80% | 0.943404 | 0.943404 | 0.000000000 |
| WT3_T4_0_50 | 1000 | 922 | 78 | 7.80% | 0.289166 | 0.289163 | -0.000003571 |

## Adapter failures

- 82: ValueError: METHOD_UNIT_COUNT_2
- 81: ValueError: METHOD_UNIT_COUNT_6
- 36: ValueError: METHOD_UNIT_COUNT_4
- 16: ValueError: METHOD_UNIT_COUNT_0
- 13: ValueError: METHOD_UNIT_COUNT_3
- 5: ValueError: Unbalanced delimiter '{'.
- 4: ValueError: METHOD_UNIT_COUNT_12
- 2: ValueError: Unbalanced delimiter '}'.
- 2: ValueError: METHOD_UNIT_COUNT_5
- 1: ValueError: Unsupported Java lexical character 'ï¿½' at offset 31.
- 1: ValueError: Unsupported Java lexical character 'Ô´' at offset 44.
- 1: ValueError: METHOD_UNIT_COUNT_8
- 1: UnicodeDecodeError: 'utf-8' codec can't decode byte 0x83 in position 1948: invalid start byte

## Interpretation

On the measurable BigCloneBench fragment pairs, C0 and C1 produce nearly identical aggregate similarity. The overall mean paired difference is extremely small, and the stratum means are likewise nearly identical.

This external result does not reproduce the large C1-over-C0 gains observed in the controlled multi-method transformations of Experiments 002 and 003. The Experiment 004 adapter requires exactly one complete method unit per fragment, so the benchmark evaluation largely removes the cross-method structural condition under which C1 pooling and one-to-one method matching can differ substantially from flat token comparison.

Accordingly, Experiment 004 supports a boundary-condition interpretation: C1 is not an across-the-board replacement that necessarily raises similarity for method-level clone fragments. Its distinctive behavior is expected when comparison units contain multiple structural method units whose organization can change.

## Limitations and validity

- 245 frozen pairs were not representable under the pre-measurement adapter and were retained as explicit failures rather than replaced.
- BigCloneBench clone categories should not be interpreted as unrestricted semantic-equivalence labels.
- Experiment 004 operates on benchmark source fragments, whereas Experiments 002 and 003 compare whole controlled submissions.
- Therefore the external benchmark and controlled experiments test related but non-identical comparison regimes.
- No plagiarism threshold, universal clone-detection accuracy, or universal semantic-equivalence claim is established.

## Reproducibility anchors

- measurements.csv SHA-256: `0A4983E8A5FDFB4293EF5480F5BBACCDD9B8B5BF1C7C8520F66E991472C04922`
- adapter_failures.csv SHA-256: `8005CC8E823C4A3B35AC33B4E594DE576A1871697084206061EA77F55F16EB83`
- Frozen sample size: 6000 unique canonical pairs
- Frozen measurable subset: 5755 pairs
- Frozen adapter failures: 245 pairs
