"""Frozen descriptive analysis for Experiment 002 primary measurements."""

from __future__ import annotations

import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP = HERE.parent
CSV_PATH = EXP / "results" / "experiment-002-primary-measurements.csv"
OUTPUT_PATH = EXP / "results" / "experiment-002-primary-analysis.md"

CONDITIONS = ("C0", "C1")
TRANSFORMATIONS = (
    "METHOD_REORDER",
    "CLASS_SPLIT",
    "IDENTIFIER_RENAME",
)


def load_rows():
    with CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != 240:
        raise RuntimeError(f"Expected 240 rows, found {len(rows)}.")

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

    return {
        "count": len(ordered),
        "mean": statistics.fmean(ordered),
        "median": statistics.median(ordered),
        "min": min(ordered),
        "q1": quantile(ordered, 0.25),
        "q3": quantile(ordered, 0.75),
        "max": max(ordered),
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


def is_base_transform(row, transformation):
    variants = {row["left_variant"], row["right_variant"]}

    return (
        row["pair_label"] == "related"
        and variants == {"BASE", transformation}
    )


def pair_key(row):
    return (row["left_submission"], row["right_submission"])


def fmt(value):
    return f"{value:.6f}"


def render_distribution_table(stats_by_condition):
    lines = [
        "| Condition | Label | n | Mean | Median | Min | Q1 | Q3 | Max |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for condition in CONDITIONS:
        for label in ("related", "control"):
            stats = stats_by_condition[condition][label]

            lines.append(
                "| "
                + " | ".join(
                    [
                        condition,
                        label,
                        str(stats["count"]),
                        fmt(stats["mean"]),
                        fmt(stats["median"]),
                        fmt(stats["min"]),
                        fmt(stats["q1"]),
                        fmt(stats["q3"]),
                        fmt(stats["max"]),
                    ]
                )
                + " |"
            )

    return lines


def main():
    rows = load_rows()

    by_condition = {
        condition: [
            row for row in rows
            if row["condition"] == condition
        ]
        for condition in CONDITIONS
    }

    for condition in CONDITIONS:
        if len(by_condition[condition]) != 120:
            raise RuntimeError(
                f"{condition}: expected 120 rows."
            )

    stats_by_condition = {}
    mean_gaps = {}
    ordering = {}
    exact_collisions = {}

    for condition in CONDITIONS:
        condition_rows = by_condition[condition]

        related = [
            row["similarity"]
            for row in condition_rows
            if row["pair_label"] == "related"
        ]
        control = [
            row["similarity"]
            for row in condition_rows
            if row["pair_label"] == "control"
        ]

        if len(related) != 24 or len(control) != 96:
            raise RuntimeError(
                f"{condition}: unexpected pair-label counts."
            )

        stats_by_condition[condition] = {
            "related": distribution(related),
            "control": distribution(control),
        }

        mean_gaps[condition] = (
            statistics.fmean(related)
            - statistics.fmean(control)
        )

        ordering[condition] = ordering_probability(
            related,
            control,
        )

        exact_collisions[condition] = {
            "related": sum(score == 1.0 for score in related),
            "control": sum(score == 1.0 for score in control),
        }

    retention = defaultdict(dict)

    for condition in CONDITIONS:
        for transformation in TRANSFORMATIONS:
            values = [
                row["similarity"]
                for row in by_condition[condition]
                if is_base_transform(row, transformation)
            ]

            if len(values) != 4:
                raise RuntimeError(
                    f"{condition}/{transformation}: "
                    f"expected 4 retention rows, found {len(values)}."
                )

            retention[condition][transformation] = {
                "count": len(values),
                "mean": statistics.fmean(values),
                "min": min(values),
                "max": max(values),
                "pstdev": statistics.pstdev(values),
            }

    pair_scores = defaultdict(dict)

    for row in rows:
        key = pair_key(row)

        if row["condition"] in pair_scores[key]:
            raise RuntimeError(
                f"Duplicate condition for pair: {key}"
            )

        pair_scores[key][row["condition"]] = row

    if len(pair_scores) != 120:
        raise RuntimeError("Expected 120 paired comparisons.")

    deltas = {
        "all related": [],
        "all control": [],
        "BASE-to-METHOD_REORDER": [],
        "BASE-to-CLASS_SPLIT": [],
        "BASE-to-IDENTIFIER_RENAME": [],
    }

    for key, conditions in pair_scores.items():
        if set(conditions) != {"C0", "C1"}:
            raise RuntimeError(
                f"Missing condition for pair: {key}"
            )

        c0 = conditions["C0"]
        c1 = conditions["C1"]
        delta = c1["similarity"] - c0["similarity"]

        if c0["pair_label"] != c1["pair_label"]:
            raise RuntimeError("Pair label changed by condition.")

        if c0["pair_label"] == "related":
            deltas["all related"].append(delta)
        else:
            deltas["all control"].append(delta)

        for transformation in TRANSFORMATIONS:
            if is_base_transform(c0, transformation):
                deltas[
                    f"BASE-to-{transformation}"
                ].append(delta)

    if len(deltas["all related"]) != 24:
        raise RuntimeError("Expected 24 related deltas.")

    if len(deltas["all control"]) != 96:
        raise RuntimeError("Expected 96 control deltas.")

    for transformation in TRANSFORMATIONS:
        key = f"BASE-to-{transformation}"

        if len(deltas[key]) != 4:
            raise RuntimeError(
                f"Expected 4 deltas for {key}."
            )

    lines = [
        "# Experiment 002 Primary Analysis",
        "",
        "## Provenance",
        "",
        "Canonical measurement artifact:",
        "",
        "`experiment-002-primary-measurements.csv`",
        "",
        "SHA-256:",
        "",
        "`3538FA569F6857F5E9616FB2CD52B1E58A547FD645AB1F8963707251FC485B07`",
        "",
        "Primary measurement commit:",
        "",
        "`f5217dc654a707ab207236a51c1eed7ad48bf57c`",
        "",
        "The analysis below is descriptive. Similarity values are not",
        "plagiarism probabilities, and no classification threshold is",
        "selected.",
        "",
        "## Related and control distributions",
        "",
    ]

    lines.extend(render_distribution_table(stats_by_condition))

    lines.extend(
        [
            "",
            "## Related-control mean gap",
            "",
            "| Condition | Related mean - control mean |",
            "|---|---:|",
        ]
    )

    for condition in CONDITIONS:
        lines.append(
            f"| {condition} | {fmt(mean_gaps[condition])} |"
        )

    lines.extend(
        [
            "",
            "## Empirical ordering probability",
            "",
            "Ties contribute 0.5. This is descriptive and is not a",
            "plagiarism probability.",
            "",
            "| Condition | Ordering probability |",
            "|---|---:|",
        ]
    )

    for condition in CONDITIONS:
        lines.append(
            f"| {condition} | {fmt(ordering[condition])} |"
        )

    lines.extend(
        [
            "",
            "## Exact similarity collisions",
            "",
            "| Condition | Related score = 1.0 | Control score = 1.0 |",
            "|---|---:|---:|",
        ]
    )

    for condition in CONDITIONS:
        values = exact_collisions[condition]

        lines.append(
            f"| {condition} | "
            f"{values['related']} | "
            f"{values['control']} |"
        )

    lines.extend(
        [
            "",
            "## BASE-to-transformation retention",
            "",
            "| Condition | Transformation | n | Mean | Min | Max | Population SD |",
            "|---|---|---:|---:|---:|---:|---:|",
        ]
    )

    for condition in CONDITIONS:
        for transformation in TRANSFORMATIONS:
            values = retention[condition][transformation]

            lines.append(
                f"| {condition} | {transformation} | "
                f"{values['count']} | "
                f"{fmt(values['mean'])} | "
                f"{fmt(values['min'])} | "
                f"{fmt(values['max'])} | "
                f"{fmt(values['pstdev'])} |"
            )

    lines.extend(
        [
            "",
            "## Paired C1 minus C0 changes",
            "",
            "Positive values mean the C1 structural comparison produced",
            "higher similarity for the same submission pair.",
            "",
            "| Pair group | n | Mean C1-C0 |",
            "|---|---:|---:|",
        ]
    )

    delta_order = (
        "all related",
        "all control",
        "BASE-to-METHOD_REORDER",
        "BASE-to-CLASS_SPLIT",
        "BASE-to-IDENTIFIER_RENAME",
    )

    for key in delta_order:
        values = deltas[key]

        lines.append(
            f"| {key} | {len(values)} | "
            f"{fmt(statistics.fmean(values))} |"
        )

    method_c0 = retention["C0"]["METHOD_REORDER"]["mean"]
    method_c1 = retention["C1"]["METHOD_REORDER"]["mean"]

    split_c0 = retention["C0"]["CLASS_SPLIT"]["mean"]
    split_c1 = retention["C1"]["CLASS_SPLIT"]["mean"]

    rename_c0 = retention["C0"]["IDENTIFIER_RENAME"]["mean"]
    rename_c1 = retention["C1"]["IDENTIFIER_RENAME"]["mean"]

    control_delta = statistics.fmean(deltas["all control"])
    related_delta = statistics.fmean(deltas["all related"])

    lines.extend(
        [
            "",
            "## Primary observations",
            "",
            f"- BASE-to-METHOD_REORDER mean retention changed from "
            f"{fmt(method_c0)} under C0 to {fmt(method_c1)} under C1.",
            f"- BASE-to-CLASS_SPLIT mean retention changed from "
            f"{fmt(split_c0)} under C0 to {fmt(split_c1)} under C1.",
            f"- BASE-to-IDENTIFIER_RENAME mean retention changed from "
            f"{fmt(rename_c0)} under C0 to {fmt(rename_c1)} under C1.",
            f"- Mean paired C1-C0 change across all related pairs was "
            f"{fmt(related_delta)}.",
            f"- Mean paired C1-C0 change across all control pairs was "
            f"{fmt(control_delta)}.",
            f"- The related-control mean gap changed from "
            f"{fmt(mean_gaps['C0'])} under C0 to "
            f"{fmt(mean_gaps['C1'])} under C1.",
            f"- Empirical ordering probability changed from "
            f"{fmt(ordering['C0'])} under C0 to "
            f"{fmt(ordering['C1'])} under C1.",
            f"- Exact control collisions were "
            f"{exact_collisions['C0']['control']} under C0 and "
            f"{exact_collisions['C1']['control']} under C1.",
            "",
            "These observations must be interpreted jointly. Increased",
            "transformation retention is not by itself evidence of an",
            "unqualified improvement if control similarity also increases",
            "enough to weaken related/control distinction.",
            "",
            "## Scope",
            "",
            "This experiment measures deterministic behavior on four frozen",
            "Java provenance families and three controlled transformations.",
            "It does not establish a plagiarism threshold, estimate a",
            "plagiarism probability, or establish general performance on",
            "unseen real-world submissions.",
            "",
        ]
    )

    OUTPUT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
