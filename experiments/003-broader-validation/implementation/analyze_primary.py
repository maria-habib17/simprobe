"""Descriptive analysis for Experiment 003 broader validation."""

from __future__ import annotations

import csv
import hashlib
import math
import statistics
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP3 = HERE.parent
REPO = EXP3.parent.parent
EXP2 = REPO / "experiments" / "002-structure-aware-comparison"

CSV_PATH = EXP3 / "results" / "experiment-003-primary-measurements.csv"
OUTPUT_PATH = EXP3 / "results" / "experiment-003-primary-analysis.md"

EXP2_CSV = EXP2 / "results" / "experiment-002-primary-measurements.csv"

EXPECTED_EXP3_SHA256 = (
    "D2B790A836506F371CA5E4862406CD7DE87E0BC7541F3323D3C038271B003C81"
)

EXPECTED_EXP2_SHA256 = (
    "3538FA569F6857F5E9616FB2CD52B1E58A547FD645AB1F8963707251FC485B07"
)

EXP3_MEASUREMENT_COMMIT = (
    "5ac08cbb02bdef56b4ab56d58d947e146b8b15ff"
)

EXP2_MEASUREMENT_COMMIT = (
    "f5217dc654a707ab207236a51c1eed7ad48bf57c"
)

CONDITIONS = ("C0", "C1")
FAMILIES = tuple("ABCDEFGHIJKL")
TRANSFORMATIONS = (
    "METHOD_REORDER",
    "CLASS_SPLIT",
    "IDENTIFIER_RENAME",
)


def sha256(path):
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest().upper()


def verify_inputs():
    exp3_hash = sha256(CSV_PATH)
    exp2_hash = sha256(EXP2_CSV)

    if exp3_hash != EXPECTED_EXP3_SHA256:
        raise RuntimeError(
            f"Experiment 003 measurement hash mismatch: {exp3_hash}"
        )

    if exp2_hash != EXPECTED_EXP2_SHA256:
        raise RuntimeError(
            f"Experiment 002 measurement hash mismatch: {exp2_hash}"
        )


def load_exp3_rows():
    with CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 2256:
        raise RuntimeError(f"Expected 2256 Experiment 003 rows, found {len(rows)}.")

    for row in rows:
        row["similarity"] = float(row["similarity"])

    return rows


def load_exp2_rows():
    with EXP2_CSV.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 240:
        raise RuntimeError(f"Expected 240 Experiment 002 rows, found {len(rows)}.")

    for row in rows:
        row["similarity"] = float(row["similarity"])

    return rows


def quantile(values, p):
    """Linear interpolation equivalent to position (n-1)*p."""
    ordered = sorted(values)

    if not ordered:
        raise ValueError("Cannot calculate quantile of empty data.")

    if len(ordered) == 1:
        return ordered[0]

    position = (len(ordered) - 1) * p
    lower = math.floor(position)
    upper = math.ceil(position)

    if lower == upper:
        return ordered[lower]

    fraction = position - lower
    return (
        ordered[lower] * (1.0 - fraction)
        + ordered[upper] * fraction
    )


def distribution(values):
    ordered = sorted(values)

    if not ordered:
        raise ValueError("Cannot summarize empty data.")

    return {
        "count": len(ordered),
        "mean": statistics.fmean(ordered),
        "median": statistics.median(ordered),
        "min": min(ordered),
        "q1": quantile(ordered, 0.25),
        "q3": quantile(ordered, 0.75),
        "max": max(ordered),
        "pstdev": statistics.pstdev(ordered),
    }


def ordering_probability(related, control):
    total = 0.0
    comparisons = 0

    for related_score in related:
        for control_score in control:
            comparisons += 1

            if related_score > control_score:
                total += 1.0
            elif related_score == control_score:
                total += 0.5

    if comparisons == 0:
        raise RuntimeError("No related-control comparisons.")

    return total / comparisons


def exp3_pair_key(row):
    return (
        row["family_a"],
        row["variant_a"],
        row["family_b"],
        row["variant_b"],
    )


def exp2_pair_key(row):
    return (row["left_submission"], row["right_submission"])


def exp3_is_base_transform(row, transformation):
    return (
        row["pair_label"] == "related"
        and row["transformation"] == transformation
        and {row["variant_a"], row["variant_b"]}
        == {"BASE", transformation}
    )


def exp2_is_base_transform(row, transformation):
    return (
        row["pair_label"] == "related"
        and {row["left_variant"], row["right_variant"]}
        == {"BASE", transformation}
    )


def fmt(value):
    return f"{value:.6f}"


def condition_summary(rows, related_n, control_n):
    by_condition = {
        condition: [row for row in rows if row["condition"] == condition]
        for condition in CONDITIONS
    }

    stats = {}
    gaps = {}
    ordering = {}
    collisions = {}

    for condition in CONDITIONS:
        related = [
            row["similarity"]
            for row in by_condition[condition]
            if row["pair_label"] == "related"
        ]
        control = [
            row["similarity"]
            for row in by_condition[condition]
            if row["pair_label"] == "control"
        ]

        if len(related) != related_n or len(control) != control_n:
            raise RuntimeError(
                f"{condition}: unexpected related/control counts."
            )

        stats[condition] = {
            "related": distribution(related),
            "control": distribution(control),
        }

        gaps[condition] = (
            statistics.fmean(related) - statistics.fmean(control)
        )

        ordering[condition] = ordering_probability(related, control)

        collisions[condition] = {
            "related": sum(value == 1.0 for value in related),
            "control": sum(value == 1.0 for value in control),
        }

    return by_condition, stats, gaps, ordering, collisions


def retention_summary(by_condition, predicate, expected_n):
    result = defaultdict(dict)

    for condition in CONDITIONS:
        for transformation in TRANSFORMATIONS:
            values = [
                row["similarity"]
                for row in by_condition[condition]
                if predicate(row, transformation)
            ]

            if len(values) != expected_n:
                raise RuntimeError(
                    f"{condition}/{transformation}: expected {expected_n} "
                    f"BASE-to-transformation rows, found {len(values)}."
                )

            result[condition][transformation] = distribution(values)

    return result


def paired_deltas(rows, pair_key, base_predicate, related_n, control_n, transform_n):
    pair_scores = defaultdict(dict)

    for row in rows:
        key = pair_key(row)
        condition = row["condition"]

        if condition in pair_scores[key]:
            raise RuntimeError(f"Duplicate condition for pair: {key}")

        pair_scores[key][condition] = row

    deltas = {
        "all related": [],
        "all control": [],
        "BASE-to-METHOD_REORDER": [],
        "BASE-to-CLASS_SPLIT": [],
        "BASE-to-IDENTIFIER_RENAME": [],
    }

    for key, conditions in pair_scores.items():
        if set(conditions) != {"C0", "C1"}:
            raise RuntimeError(f"Missing condition for pair: {key}")

        c0 = conditions["C0"]
        c1 = conditions["C1"]

        if c0["pair_label"] != c1["pair_label"]:
            raise RuntimeError("Pair label changed by condition.")

        delta = c1["similarity"] - c0["similarity"]

        if c0["pair_label"] == "related":
            deltas["all related"].append(delta)
        else:
            deltas["all control"].append(delta)

        for transformation in TRANSFORMATIONS:
            if base_predicate(c0, transformation):
                deltas[f"BASE-to-{transformation}"].append(delta)

    if len(deltas["all related"]) != related_n:
        raise RuntimeError("Unexpected related delta count.")

    if len(deltas["all control"]) != control_n:
        raise RuntimeError("Unexpected control delta count.")

    for transformation in TRANSFORMATIONS:
        key = f"BASE-to-{transformation}"
        if len(deltas[key]) != transform_n:
            raise RuntimeError(f"Unexpected delta count for {key}.")

    return deltas


def family_replication(rows):
    pair_scores = defaultdict(dict)

    for row in rows:
        if row["transformation"] not in {
            "METHOD_REORDER",
            "CLASS_SPLIT",
        }:
            continue

        key = (row["family_a"], row["transformation"])
        pair_scores[key][row["condition"]] = row["similarity"]

    result = {}

    for transformation in ("METHOD_REORDER", "CLASS_SPLIT"):
        family_rows = []

        for family in FAMILIES:
            key = (family, transformation)
            scores = pair_scores.get(key, {})

            if set(scores) != {"C0", "C1"}:
                raise RuntimeError(
                    f"Missing family replication scores for {family}/{transformation}."
                )

            delta = scores["C1"] - scores["C0"]
            family_rows.append(
                (family, scores["C0"], scores["C1"], delta)
            )

        result[transformation] = family_rows

    return result


def render_distribution_table(stats_by_condition):
    lines = [
        "| Condition | Label | n | Mean | Median | Min | Q1 | Q3 | Max |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for condition in CONDITIONS:
        for label in ("related", "control"):
            stats = stats_by_condition[condition][label]
            lines.append(
                f"| {condition} | {label} | {stats['count']} | "
                f"{fmt(stats['mean'])} | {fmt(stats['median'])} | "
                f"{fmt(stats['min'])} | {fmt(stats['q1'])} | "
                f"{fmt(stats['q3'])} | {fmt(stats['max'])} |"
            )

    return lines


def main():
    verify_inputs()

    rows3 = load_exp3_rows()
    rows2 = load_exp2_rows()

    by3, stats3, gaps3, ordering3, collisions3 = condition_summary(
        rows3, 72, 1056
    )

    by2, stats2, gaps2, ordering2, collisions2 = condition_summary(
        rows2, 24, 96
    )

    retention3 = retention_summary(
        by3, exp3_is_base_transform, 12
    )

    retention2 = retention_summary(
        by2, exp2_is_base_transform, 4
    )

    deltas3 = paired_deltas(
        rows3,
        exp3_pair_key,
        exp3_is_base_transform,
        72,
        1056,
        12,
    )

    deltas2 = paired_deltas(
        rows2,
        exp2_pair_key,
        exp2_is_base_transform,
        24,
        96,
        4,
    )

    replication = family_replication(rows3)

    control_delta_stats = distribution(deltas3["all control"])

    lines = [
        "# Experiment 003 Primary Analysis",
        "",
        "## Provenance",
        "",
        "Canonical Experiment 003 measurement artifact:",
        "",
        "`experiment-003-primary-measurements.csv`",
        "",
        "SHA-256:",
        "",
        f"`{EXPECTED_EXP3_SHA256}`",
        "",
        "Primary measurement commit:",
        "",
        f"`{EXP3_MEASUREMENT_COMMIT}`",
        "",
        "Cross-experiment reference artifact:",
        "",
        "`experiment-002-primary-measurements.csv`",
        "",
        "Reference SHA-256:",
        "",
        f"`{EXPECTED_EXP2_SHA256}`",
        "",
        "Reference measurement commit:",
        "",
        f"`{EXP2_MEASUREMENT_COMMIT}`",
        "",
        "Both input hashes are verified by the analysis script before analysis.",
        "",
        "The analysis below is descriptive. Similarity values are not",
        "plagiarism probabilities, and no classification threshold is selected.",
        "",
        "## Related and control distributions",
        "",
    ]

    lines.extend(render_distribution_table(stats3))

    lines.extend([
        "",
        "## Related-control mean gap",
        "",
        "| Condition | Related mean - control mean |",
        "|---|---:|",
    ])

    for condition in CONDITIONS:
        lines.append(f"| {condition} | {fmt(gaps3[condition])} |")

    lines.extend([
        "",
        "## Empirical ordering probability",
        "",
        "Ties contribute 0.5. This is descriptive and is not a plagiarism probability.",
        "",
        "| Condition | Ordering probability |",
        "|---|---:|",
    ])

    for condition in CONDITIONS:
        lines.append(f"| {condition} | {fmt(ordering3[condition])} |")

    lines.extend([
        "",
        "## Exact similarity collisions",
        "",
        "| Condition | Related score = 1.0 | Control score = 1.0 |",
        "|---|---:|---:|",
    ])

    for condition in CONDITIONS:
        lines.append(
            f"| {condition} | {collisions3[condition]['related']} | "
            f"{collisions3[condition]['control']} |"
        )

    lines.extend([
        "",
        "## BASE-to-transformation retention",
        "",
        "| Condition | Transformation | n | Mean | Min | Max | Population SD |",
        "|---|---|---:|---:|---:|---:|---:|",
    ])

    for condition in CONDITIONS:
        for transformation in TRANSFORMATIONS:
            values = retention3[condition][transformation]
            lines.append(
                f"| {condition} | {transformation} | {values['count']} | "
                f"{fmt(values['mean'])} | {fmt(values['min'])} | "
                f"{fmt(values['max'])} | {fmt(values['pstdev'])} |"
            )

    lines.extend([
        "",
        "## Paired C1 minus C0 changes",
        "",
        "Positive values mean C1 produced higher similarity for the same pair.",
        "",
        "| Pair group | n | Mean C1-C0 |",
        "|---|---:|---:|",
    ])

    delta_order = (
        "all related",
        "all control",
        "BASE-to-METHOD_REORDER",
        "BASE-to-CLASS_SPLIT",
        "BASE-to-IDENTIFIER_RENAME",
    )

    for key in delta_order:
        values = deltas3[key]
        lines.append(
            f"| {key} | {len(values)} | {fmt(statistics.fmean(values))} |"
        )

    lines.extend([
        "",
        "## Control-pair C1 minus C0 distribution",
        "",
        "| n | Mean | Median | Min | Q1 | Q3 | Max | Population SD |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
        f"| {control_delta_stats['count']} | "
        f"{fmt(control_delta_stats['mean'])} | "
        f"{fmt(control_delta_stats['median'])} | "
        f"{fmt(control_delta_stats['min'])} | "
        f"{fmt(control_delta_stats['q1'])} | "
        f"{fmt(control_delta_stats['q3'])} | "
        f"{fmt(control_delta_stats['max'])} | "
        f"{fmt(control_delta_stats['pstdev'])} |",
        "",
        "## Family-level replication",
        "",
        "Each row is the BASE-to-transformation score for one frozen family.",
        "",
        "| Transformation | Family | C0 | C1 | C1-C0 |",
        "|---|---|---:|---:|---:|",
    ])

    for transformation in ("METHOD_REORDER", "CLASS_SPLIT"):
        for family, c0, c1, delta in replication[transformation]:
            lines.append(
                f"| {transformation} | {family} | {fmt(c0)} | "
                f"{fmt(c1)} | {fmt(delta)} |"
            )

    lines.extend([
        "",
        "### Family-level direction counts",
        "",
        "| Transformation | Positive | Zero | Negative |",
        "|---|---:|---:|---:|",
    ])

    for transformation in ("METHOD_REORDER", "CLASS_SPLIT"):
        values = [row[3] for row in replication[transformation]]
        positive = sum(value > 0.0 for value in values)
        zero = sum(value == 0.0 for value in values)
        negative = sum(value < 0.0 for value in values)
        lines.append(
            f"| {transformation} | {positive} | {zero} | {negative} |"
        )

    lines.extend([
        "",
        "## Cross-experiment comparison",
        "",
        "Experiment 002 used four frozen provenance families; Experiment 003",
        "uses twelve independently constructed frozen provenance families.",
        "The C0/C1 comparison definitions are held fixed.",
        "",
        "| Metric | Experiment 002 | Experiment 003 |",
        "|---|---:|---:|",
        f"| C0 related mean | {fmt(stats2["C0"]["related"]["mean"])} | {fmt(stats3["C0"]["related"]["mean"])} |",
        f"| C0 control mean | {fmt(stats2["C0"]["control"]["mean"])} | {fmt(stats3["C0"]["control"]["mean"])} |",
        f"| C1 related mean | {fmt(stats2["C1"]["related"]["mean"])} | {fmt(stats3["C1"]["related"]["mean"])} |",
        f"| C1 control mean | {fmt(stats2["C1"]["control"]["mean"])} | {fmt(stats3["C1"]["control"]["mean"])} |",
        f"| C0 related-control mean gap | {fmt(gaps2["C0"])} | {fmt(gaps3["C0"])} |",
        f"| C1 related-control mean gap | {fmt(gaps2["C1"])} | {fmt(gaps3["C1"])} |",
        f"| C0 ordering probability | {fmt(ordering2["C0"])} | {fmt(ordering3["C0"])} |",
        f"| C1 ordering probability | {fmt(ordering2["C1"])} | {fmt(ordering3["C1"])} |",
        f"| METHOD_REORDER C0 retention | {fmt(retention2["C0"]["METHOD_REORDER"]["mean"])} | {fmt(retention3["C0"]["METHOD_REORDER"]["mean"])} |",
        f"| METHOD_REORDER C1 retention | {fmt(retention2["C1"]["METHOD_REORDER"]["mean"])} | {fmt(retention3["C1"]["METHOD_REORDER"]["mean"])} |",
        f"| CLASS_SPLIT C0 retention | {fmt(retention2["C0"]["CLASS_SPLIT"]["mean"])} | {fmt(retention3["C0"]["CLASS_SPLIT"]["mean"])} |",
        f"| CLASS_SPLIT C1 retention | {fmt(retention2["C1"]["CLASS_SPLIT"]["mean"])} | {fmt(retention3["C1"]["CLASS_SPLIT"]["mean"])} |",
        f"| IDENTIFIER_RENAME C0 retention | {fmt(retention2["C0"]["IDENTIFIER_RENAME"]["mean"])} | {fmt(retention3["C0"]["IDENTIFIER_RENAME"]["mean"])} |",
        f"| IDENTIFIER_RENAME C1 retention | {fmt(retention2["C1"]["IDENTIFIER_RENAME"]["mean"])} | {fmt(retention3["C1"]["IDENTIFIER_RENAME"]["mean"])} |",
        f"| Mean control C1-C0 | {fmt(statistics.fmean(deltas2["all control"]))} | {fmt(statistics.fmean(deltas3["all control"]))} |",
    ])

    method_values = [row[3] for row in replication["METHOD_REORDER"]]
    split_values = [row[3] for row in replication["CLASS_SPLIT"]]

    lines.extend([
        "",
        "## Primary observations",
        "",
        f"- BASE-to-METHOD_REORDER mean retention changed from "
        f"{fmt(retention3["C0"]["METHOD_REORDER"]["mean"])} under C0 to "
        f"{fmt(retention3["C1"]["METHOD_REORDER"]["mean"])} under C1.",
        f"- BASE-to-CLASS_SPLIT mean retention changed from "
        f"{fmt(retention3["C0"]["CLASS_SPLIT"]["mean"])} under C0 to "
        f"{fmt(retention3["C1"]["CLASS_SPLIT"]["mean"])} under C1.",
        f"- BASE-to-IDENTIFIER_RENAME mean retention changed from "
        f"{fmt(retention3["C0"]["IDENTIFIER_RENAME"]["mean"])} under C0 to "
        f"{fmt(retention3["C1"]["IDENTIFIER_RENAME"]["mean"])} under C1.",
        f"- METHOD_REORDER had positive C1-C0 retention change in "
        f"{sum(value > 0.0 for value in method_values)} of 12 families.",
        f"- CLASS_SPLIT had positive C1-C0 retention change in "
        f"{sum(value > 0.0 for value in split_values)} of 12 families.",
        f"- Mean paired C1-C0 change across all related pairs was "
        f"{fmt(statistics.fmean(deltas3["all related"]))}.",
        f"- Mean paired C1-C0 change across all control pairs was "
        f"{fmt(statistics.fmean(deltas3["all control"]))}.",
        f"- The related-control mean gap changed from {fmt(gaps3["C0"])} "
        f"under C0 to {fmt(gaps3["C1"])} under C1.",
        f"- Empirical ordering probability changed from "
        f"{fmt(ordering3["C0"])} under C0 to {fmt(ordering3["C1"])} under C1.",
        f"- Exact control collisions were {collisions3["C0"]["control"]} "
        f"under C0 and {collisions3["C1"]["control"]} under C1.",
        "",
        "These observations must be interpreted jointly. Increased",
        "transformation retention is not by itself evidence of an",
        "unqualified improvement if control similarity also increases",
        "enough to weaken related/control distinction.",
        "",
        "## Scope",
        "",
        "Experiment 003 is a controlled broader validation across twelve",
        "independently constructed frozen Java provenance families and three",
        "controlled transformations. It broadens the controlled replication",
        "relative to Experiment 002, but it is not external benchmark",
        "validation and does not establish general performance on unseen",
        "real-world submissions.",
        "",
        "No plagiarism threshold is selected, and similarity values are not",
        "interpreted as plagiarism probabilities.",
        "",
    ])

    OUTPUT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
