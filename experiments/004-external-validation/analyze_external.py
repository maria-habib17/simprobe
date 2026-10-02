from __future__ import annotations

import csv
import hashlib
import statistics
from collections import Counter, defaultdict
from pathlib import Path

EXP = Path(__file__).resolve().parent
MEASUREMENTS = EXP / "measurements.csv"
FAILURES = EXP / "adapter_failures.csv"
MANIFEST = EXP / "sample_manifest.csv"
OUT = EXP / "ANALYSIS.md"
BY_STRATUM = EXP / "analysis_by_stratum.csv"

EXPECTED_MEASUREMENT_SHA = "0A4983E8A5FDFB4293EF5480F5BBACCDD9B8B5BF1C7C8520F66E991472C04922"
EXPECTED_FAILURE_SHA = "8005CC8E823C4A3B35AC33B4E594DE576A1871697084206061EA77F55F16EB83"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()

def read_csv(path):
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

def mean(values):
    return statistics.fmean(values) if values else float("nan")

def fmt(x):
    return f"{x:.6f}"

def main():
    if sha256(MEASUREMENTS) != EXPECTED_MEASUREMENT_SHA:
        raise RuntimeError("Measurement artifact hash mismatch.")
    if sha256(FAILURES) != EXPECTED_FAILURE_SHA:
        raise RuntimeError("Adapter-failure artifact hash mismatch.")

    rows = read_csv(MEASUREMENTS)
    failures = read_csv(FAILURES)
    manifest = read_csv(MANIFEST)

    if len(manifest) != 6000:
        raise RuntimeError(f"Expected 6000 frozen sample rows; found {len(manifest)}")
    if len(rows) != 5755:
        raise RuntimeError(f"Expected 5755 measured pairs; found {len(rows)}")
    if len(failures) != 245:
        raise RuntimeError(f"Expected 245 adapter failures; found {len(failures)}")

    measured_keys = {r["CANONICAL_PAIR_KEY"] for r in rows}
    failed_keys = {r["CANONICAL_PAIR_KEY"] for r in failures}
    sample_keys = {r["CANONICAL_PAIR_KEY"] for r in manifest}

    if measured_keys & failed_keys:
        raise RuntimeError("Pair appears in both measured and failure sets.")
    if measured_keys | failed_keys != sample_keys:
        raise RuntimeError("Measured/failure partition does not equal frozen sample.")

    strata = sorted({r["STRATUM"] for r in manifest})
    sample_count = Counter(r["STRATUM"] for r in manifest)
    failure_count = Counter(r["STRATUM"] for r in failures)
    grouped = defaultdict(list)

    for row in rows:
        grouped[row["STRATUM"]].append(row)

    c0_all = [float(r["C0_SIMILARITY"]) for r in rows]
    c1_all = [float(r["C1_SIMILARITY"]) for r in rows]
    deltas = [b - a for a, b in zip(c0_all, c1_all)]

    gt = sum(d > 1e-12 for d in deltas)
    lt = sum(d < -1e-12 for d in deltas)
    eq = len(deltas) - gt - lt

    exact_c0 = sum(abs(x - 1.0) <= 1e-12 for x in c0_all)
    exact_c1 = sum(abs(x - 1.0) <= 1e-12 for x in c1_all)

    summary_rows = []
    for stratum in strata:
        group = grouped[stratum]
        c0 = [float(r["C0_SIMILARITY"]) for r in group]
        c1 = [float(r["C1_SIMILARITY"]) for r in group]
        ds = [b - a for a, b in zip(c0, c1)]
        summary_rows.append({
            "stratum": stratum,
            "sample_n": sample_count[stratum],
            "measured_n": len(group),
            "adapter_failures": failure_count[stratum],
            "failure_rate": failure_count[stratum] / sample_count[stratum],
            "c0_mean": mean(c0),
            "c1_mean": mean(c1),
            "mean_delta": mean(ds),
            "c1_gt_c0": sum(d > 1e-12 for d in ds),
            "c1_eq_c0": sum(abs(d) <= 1e-12 for d in ds),
            "c1_lt_c0": sum(d < -1e-12 for d in ds),
        })

    fields = list(summary_rows[0])
    with BY_STRATUM.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)

    failure_types = Counter(f"{r['ERROR_TYPE']}: {r['ERROR']}" for r in failures)

    lines = []
    lines += ["# Experiment 004 External Validation Analysis", ""]
    lines += ["## Status", ""]
    lines += ["Final analysis of the frozen Experiment 004 sample and measurements.", ""]
    lines += ["No sampled pair was replaced after observing adapter behavior or SimProbe scores.", ""]

    lines += ["## Realized sample", ""]
    lines += ["- Frozen sampled pairs: 6000"]
    lines += [f"- Measured pairs: {len(rows)} ({100*len(rows)/6000:.4f}%)"]
    lines += [f"- Adapter-failure pairs: {len(failures)} ({100*len(failures)/6000:.4f}%)"]
    lines += ["- C0 measurements per measurable pair: 1"]
    lines += ["- C1 measurements per measurable pair: 1", ""]

    lines += ["## Overall C0/C1 result", ""]
    lines += [f"- C0 mean similarity: {fmt(mean(c0_all))}"]
    lines += [f"- C1 mean similarity: {fmt(mean(c1_all))}"]
    lines += [f"- Mean paired delta (C1 - C0): {mean(deltas):.9f}"]
    lines += [f"- Median paired delta: {statistics.median(deltas):.9f}"]
    lines += [f"- C1 > C0: {gt} pairs"]
    lines += [f"- C1 = C0 within 1e-12: {eq} pairs"]
    lines += [f"- C1 < C0: {lt} pairs"]
    lines += [f"- Exact C0 similarity 1.0: {exact_c0} pairs"]
    lines += [f"- Exact C1 similarity 1.0: {exact_c1} pairs", ""]

    lines += ["## Results by frozen stratum", ""]
    lines += ["| Stratum | Sample | Measured | Failures | Failure rate | C0 mean | C1 mean | Mean delta |"]
    lines += ["|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in summary_rows:
        lines += [
            f"| {r['stratum']} | {r['sample_n']} | {r['measured_n']} | "
            f"{r['adapter_failures']} | {100*r['failure_rate']:.2f}% | "
            f"{r['c0_mean']:.6f} | {r['c1_mean']:.6f} | {r['mean_delta']:.9f} |"
        ]
    lines += [""]

    lines += ["## Adapter failures", ""]
    for label, count in failure_types.most_common():
        lines += [f"- {count}: {label}"]
    lines += [""]

    lines += ["## Interpretation", ""]
    lines += [
        "On the measurable BigCloneBench fragment pairs, C0 and C1 produce nearly identical aggregate similarity. "
        "The overall mean paired difference is extremely small, and the stratum means are likewise nearly identical."
    ]
    lines += [""]
    lines += [
        "This external result does not reproduce the large C1-over-C0 gains observed in the controlled multi-method "
        "transformations of Experiments 002 and 003. The Experiment 004 adapter requires exactly one complete method "
        "unit per fragment, so the benchmark evaluation largely removes the cross-method structural condition under "
        "which C1 pooling and one-to-one method matching can differ substantially from flat token comparison."
    ]
    lines += [""]
    lines += [
        "Accordingly, Experiment 004 supports a boundary-condition interpretation: C1 is not an across-the-board "
        "replacement that necessarily raises similarity for method-level clone fragments. Its distinctive behavior "
        "is expected when comparison units contain multiple structural method units whose organization can change."
    ]
    lines += [""]

    lines += ["## Limitations and validity", ""]
    lines += [
        "- 245 frozen pairs were not representable under the pre-measurement adapter and were retained as explicit failures rather than replaced."
    ]
    lines += [
        "- BigCloneBench clone categories should not be interpreted as unrestricted semantic-equivalence labels."
    ]
    lines += [
        "- Experiment 004 operates on benchmark source fragments, whereas Experiments 002 and 003 compare whole controlled submissions."
    ]
    lines += [
        "- Therefore the external benchmark and controlled experiments test related but non-identical comparison regimes."
    ]
    lines += [
        "- No plagiarism threshold, universal clone-detection accuracy, or universal semantic-equivalence claim is established."
    ]
    lines += [""]

    lines += ["## Reproducibility anchors", ""]
    lines += [f"- measurements.csv SHA-256: `{sha256(MEASUREMENTS)}`"]
    lines += [f"- adapter_failures.csv SHA-256: `{sha256(FAILURES)}`"]
    lines += ["- Frozen sample size: 6000 unique canonical pairs"]
    lines += ["- Frozen measurable subset: 5755 pairs"]
    lines += ["- Frozen adapter failures: 245 pairs", ""]

    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(f"FROZEN_SAMPLE={len(manifest)}")
    print(f"MEASURED={len(rows)}")
    print(f"ADAPTER_FAILURES={len(failures)}")
    print(f"C0_MEAN={mean(c0_all):.9f}")
    print(f"C1_MEAN={mean(c1_all):.9f}")
    print(f"MEAN_DELTA={mean(deltas):.9f}")
    print(f"MEDIAN_DELTA={statistics.median(deltas):.9f}")
    print(f"C1_GT_C0={gt}")
    print(f"C1_EQ_C0={eq}")
    print(f"C1_LT_C0={lt}")
    print(f"ANALYSIS_SHA256={sha256(OUT)}")
    print(f"STRATUM_SHA256={sha256(BY_STRATUM)}")

if __name__ == "__main__":
    main()
