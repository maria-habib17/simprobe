# SimProbe

**Structural robustness in source-code similarity through controlled and external evaluation**

SimProbe is an independent research project investigating how source-code similarity measurements behave under program transformations, structural reorganization, and changes in analysis granularity.

The project studies a central distinction:

> **Similarity magnitude and evidential distinctiveness are not necessarily the same property.**

A high similarity score may reflect a meaningful relationship between two programs, but it may also arise because a representation removes distinctions that are common across a cohort.

SimProbe therefore treats similarity scores as measurements that require empirical characterization rather than as direct evidence of plagiarism, authorship, semantic equivalence, or misconduct.

---

## Research focus

SimProbe currently investigates:

1. How source-code representation choices affect transformation invariance and discrimination.
2. How token-normalized similarity responds to identifier renaming and higher-order structural reorganization.
3. Whether method-aware matching improves robustness to method reordering and class splitting.
4. Under which structural conditions method-aware matching provides information beyond token-level similarity.
5. Whether effects observed in controlled experiments persist on an external code-clone benchmark.

---

## Similarity methods

The current experiments evaluate two principal configurations.

### C0 — Token-normalized sequence similarity

C0 represents a submission as a normalized token sequence and compares representations using normalized Levenshtein similarity.

This provides a relatively simple baseline for studying the effect of source-level transformations.

### C1 — Method-aware structural matching

C1 decomposes a submission into method units, constructs a full pairwise method-similarity matrix, and performs deterministic maximum-weight one-to-one matching.

Matched similarity is aggregated across the two submissions while retaining sensitivity to ordering *within* individual methods.

This design is intended to test whether explicit method-level correspondence improves robustness to transformations that reorganize code above the method level.

---

## Experimental program

SimProbe uses a sequence of controlled and external experiments rather than relying on a single benchmark.

| Experiment | Purpose |
|---|---|
| **Exp001** | Representation and abstraction diagnostics |
| **Exp002** | Controlled comparison of C0 and C1 across structural transformations |
| **Exp003** | Larger controlled evaluation across additional program families |
| **Exp004** | Frozen external evaluation on BigCloneBench method-level fragments |

---

## Controlled evaluation

### Exp002

Exp002 evaluated **16 submissions from 4 provenance families**, producing **120 pairs per condition**.

| Configuration | Related mean | Control mean | Gap | Ordering |
|---|---:|---:|---:|---:|
| C0 | 0.743607 | 0.561939 | 0.181668 | 0.868490 |
| C1 | 0.993137 | 0.543548 | 0.449589 | 1.000000 |

For controlled method reordering:

- C0: **0.733750**
- C1: **1.000000**

For controlled class splitting:

- C0: **0.692713**
- C1: **0.986274**

Both configurations retained similarity under identifier renaming in this experiment.

---

## Scaled controlled evaluation

### Exp003

Exp003 expanded the controlled evaluation to **48 submissions across 12 provenance families**, producing **1,128 pairs per condition**.

| Configuration | Related mean | Control mean | Gap | Ordering |
|---|---:|---:|---:|---:|
| C0 | 0.669228 | 0.544525 | 0.124703 | 0.663799 |
| C1 | 0.991159 | 0.564466 | 0.426693 | 1.000000 |

Additional transformation results included:

| Transformation | C0 | C1 |
|---|---:|---:|
| Method reorder | 0.781857 | 1.000000 |
| Class split | 0.472994 | 0.982317 |

Exact-score analysis also found:

- C0 related pairs at exactly 1.0: **12**
- C0 control pairs at exactly 1.0: **0**
- C1 related pairs at exactly 1.0: **36**
- C1 control pairs at exactly 1.0: **0**

Within these controlled fixtures, method-aware matching therefore increased robustness to the structural transformations being tested while maintaining separation from the evaluated controls.

These results are specific to the experimental population and are not claims of universal superiority.

---

## External evaluation — BigCloneBench

### Exp004

To test whether the controlled C1 advantage generalized to a different setting, SimProbe performed a frozen external evaluation using **BigCloneBench-derived method-level fragments**.

The protocol was frozen before benchmark acquisition, sampling, measurement, and result inspection.

### Sample

- Requested sample: **6,000 unique pairs**
- Measurable pairs: **5,755**
- Measurement coverage: **95.9167%**
- Retained failures: **245**

The sample covered six predefined strata.

### Overall result

| Metric | C0 | C1 |
|---|---:|---:|
| Mean similarity | 0.731550971 | 0.731574004 |
| Mean difference | — | +0.000023033 |

Across the **5,755 measurable pairs**:

- C1 > C0: **4 pairs**
- C1 = C0: **5,745 pairs**
- C1 < C0: **6 pairs**
- Median C1 − C0 difference: **0**
- Exact C0 = 1.0: **1,946 pairs**
- Exact C1 = 1.0: **1,946 pairs**

The large C1 advantage observed in the controlled structural-reorganization experiments was therefore **not reproduced** on these external method-level fragments.

---

## What the external result means

This is an important boundary condition rather than an omitted or discarded negative result.

The BigCloneBench adapter used **one complete method per fragment**.

C1's principal mechanism is method-level decomposition followed by one-to-one correspondence across multiple method units. When each comparison unit already contains exactly one complete method, much of the structural condition that allows C1 to differ from C0 disappears.

The combined evidence therefore supports a bounded conclusion:

> **C1's observed benefit is structure-dependent, not universally higher similarity.**

Controlled multi-method transformations expose the mechanism. Single-method external fragments largely remove that condition.

This distinction is central to SimProbe's current research direction.

---

## Reproducibility

SimProbe emphasizes protocol-first and reproducible experimentation.

The external evaluation used:

- a predefined sampling procedure;
- deterministic pair selection;
- a frozen adapter;
- no post-result source exclusions;
- no synthetic wrappers;
- no inserted imports;
- no source repair or rewriting; and
- explicit retention of measurement failures.

The publication-source snapshot is frozen at:

```text
24baf006b4858cace1af528c28216bfb3ce03760
```

Exp004 raw measurement commit:

```text
7777db3836690e85c11d18f23f252eeeef685b5a
```

Publication-source SHA-256:

```text
C379353279C6486B5B852A77D2D065A019DA7E30DDA0ED73E75860B6F95F1363
```

These identifiers are provided so that reported results can be tied to a specific research state.

---

## Responsible interpretation

SimProbe is **not a plagiarism detector or misconduct classifier**.

Its similarity values should not be interpreted as:

- plagiarism probabilities;
- proof of common authorship;
- evidence of author intent;
- semantic-equivalence guarantees;
- universal clone-detection accuracy; or
- universal decision thresholds.

Likewise, a representation collision does not automatically constitute a false positive.

The project studies the behavior and limitations of source-code similarity measurements.

---

## Current research conclusion

The current experiments suggest that representation design and program granularity materially affect the behavior of source-code similarity systems.

In the controlled experiments, method-aware matching substantially improved robustness to method reordering and class splitting while preserving discrimination against the evaluated controls.

In the external single-method BigCloneBench evaluation, however, C0 and C1 were almost indistinguishable.

Together, these results indicate that the value of method-aware matching depends on whether the input exposes the multi-method structural organization that the method is designed to model.

---

## Development

### Requirements

- Python 3.11 or newer
- Git

Clone the repository:

```bash
git clone https://github.com/maria-habib17/simprobe.git
cd simprobe
```

Install the development environment:

```bash
pip install -e ".[dev]"
```

See the repository documentation and experiment artifacts for protocol and reproduction details.

---

## Related project

### BehavClone

SimProbe focuses on controlled and external evaluation of source-code similarity representations.

**BehavClone** explores a complementary evidence architecture for architecture-flexible programming submissions, including Tree-sitter fragment extraction, structural representations, global one-to-one correspondence, cohort-relative context, and imported behavioral evidence.

Repository:

https://github.com/maria-habib17/behavclone

---

## Research status

**Active research / experimental prototype**

The controlled and external experiments reported above have been completed and frozen for research use. The project remains under active development as the results are prepared and extended for research dissemination.

---

## Author

**Maria Habib**  
Software Engineering · Program Analysis · Code Intelligence · Empirical Software Engineering

GitHub: https://github.com/maria-habib17  
LinkedIn: https://www.linkedin.com/in/maria-habib-674508270/

For research collaboration or engineering opportunities:

**mariahabib1059@gmail.com**

---

## License

MIT License
