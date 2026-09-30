"""Canonical primary measurement runner for Experiment 002.

This runner is intentionally separate from the frozen comparison engine.

Do not modify the frozen fixture, comparison rules, pair labels, or primary
schema in response to observed measurement results.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from compare import compare_c0, compare_c1


CONDITIONS = ("C0", "C1")

FAMILIES = (
    "family-a",
    "family-b",
    "family-c",
    "family-d",
)

VARIANTS = (
    "BASE",
    "CLASS_SPLIT",
    "IDENTIFIER_RENAME",
    "METHOD_REORDER",
)

FIELDNAMES = (
    "left_submission",
    "right_submission",
    "left_family",
    "right_family",
    "left_variant",
    "right_variant",
    "pair_label",
    "condition",
    "left_token_count",
    "right_token_count",
    "edit_distance",
    "left_method_count",
    "right_method_count",
    "matched_method_count",
    "matched_similarity_sum",
    "similarity",
)


@dataclass(frozen=True)
class Submission:
    family: str
    variant: str
    path: Path

    @property
    def identifier(self) -> str:
        return f"{self.family}/{self.variant}"


@dataclass(frozen=True)
class Pair:
    left: Submission
    right: Submission

    @property
    def pair_label(self) -> str:
        if self.left.family == self.right.family:
            return "related"
        return "control"


def experiment_root() -> Path:
    return Path(__file__).resolve().parent.parent


def fixture_root() -> Path:
    return experiment_root() / "fixtures" / "primary"


def default_output_path() -> Path:
    return experiment_root() / "results" / "experiment-002-primary-measurements.csv"


def enumerate_submissions(root: Path) -> tuple[Submission, ...]:
    submissions: list[Submission] = []

    for family in FAMILIES:
        for variant in VARIANTS:
            path = root / family / variant

            if not path.is_dir():
                raise FileNotFoundError(
                    f"Missing frozen submission directory: {path}"
                )

            java_files = tuple(
                sorted(
                    candidate
                    for candidate in path.rglob("*.java")
                    if candidate.is_file()
                )
            )

            expected_files = 2 if variant == "CLASS_SPLIT" else 1

            if len(java_files) != expected_files:
                raise RuntimeError(
                    f"{family}/{variant} expected {expected_files} "
                    f"Java file(s), found {len(java_files)}."
                )

            submissions.append(
                Submission(
                    family=family,
                    variant=variant,
                    path=path,
                )
            )

    if len(submissions) != 16:
        raise RuntimeError(
            f"Expected 16 submissions, found {len(submissions)}."
        )

    return tuple(submissions)


def enumerate_pairs(
    submissions: tuple[Submission, ...],
) -> tuple[Pair, ...]:
    pairs: list[Pair] = []

    for left_index in range(len(submissions)):
        for right_index in range(left_index + 1, len(submissions)):
            pairs.append(
                Pair(
                    left=submissions[left_index],
                    right=submissions[right_index],
                )
            )

    if len(pairs) != 120:
        raise RuntimeError(
            f"Expected 120 unordered pairs, found {len(pairs)}."
        )

    related = sum(pair.pair_label == "related" for pair in pairs)
    control = sum(pair.pair_label == "control" for pair in pairs)

    if related != 24:
        raise RuntimeError(
            f"Expected 24 related pairs, found {related}."
        )

    if control != 96:
        raise RuntimeError(
            f"Expected 96 control pairs, found {control}."
        )

    return tuple(pairs)


def c0_row(pair: Pair) -> dict[str, object]:
    result = compare_c0(pair.left.path, pair.right.path)

    return {
        "left_submission": pair.left.identifier,
        "right_submission": pair.right.identifier,
        "left_family": pair.left.family,
        "right_family": pair.right.family,
        "left_variant": pair.left.variant,
        "right_variant": pair.right.variant,
        "pair_label": pair.pair_label,
        "condition": "C0",
        "left_token_count": result.left_token_count,
        "right_token_count": result.right_token_count,
        "edit_distance": result.edit_distance,
        "left_method_count": "",
        "right_method_count": "",
        "matched_method_count": "",
        "matched_similarity_sum": "",
        "similarity": result.similarity,
    }


def c1_row(pair: Pair) -> dict[str, object]:
    result = compare_c1(pair.left.path, pair.right.path)

    return {
        "left_submission": pair.left.identifier,
        "right_submission": pair.right.identifier,
        "left_family": pair.left.family,
        "right_family": pair.right.family,
        "left_variant": pair.left.variant,
        "right_variant": pair.right.variant,
        "pair_label": pair.pair_label,
        "condition": "C1",
        "left_token_count": "",
        "right_token_count": "",
        "edit_distance": "",
        "left_method_count": result.left_method_count,
        "right_method_count": result.right_method_count,
        "matched_method_count": result.matched_method_count,
        "matched_similarity_sum": result.matched_similarity_sum,
        "similarity": result.similarity,
    }


def measurement_rows(
    pairs: tuple[Pair, ...],
) -> Iterator[dict[str, object]]:
    # Frozen row ordering: all C0 rows, then all C1 rows.
    for pair in pairs:
        yield c0_row(pair)

    for pair in pairs:
        yield c1_row(pair)


def validate_row(row: dict[str, object]) -> None:
    if tuple(row.keys()) != FIELDNAMES:
        raise RuntimeError("Measurement row schema mismatch.")

    if row["pair_label"] not in {"related", "control"}:
        raise RuntimeError("Invalid pair label.")

    if row["condition"] not in CONDITIONS:
        raise RuntimeError("Invalid comparison condition.")

    similarity = float(row["similarity"])

    if similarity < 0.0 or similarity > 1.0:
        raise RuntimeError(
            f"Similarity outside [0, 1]: {similarity}"
        )

    if row["condition"] == "C0":
        for field in (
            "left_token_count",
            "right_token_count",
            "edit_distance",
        ):
            if row[field] == "":
                raise RuntimeError(
                    f"C0 field unexpectedly empty: {field}"
                )

        for field in (
            "left_method_count",
            "right_method_count",
            "matched_method_count",
            "matched_similarity_sum",
        ):
            if row[field] != "":
                raise RuntimeError(
                    f"C0 field unexpectedly populated: {field}"
                )

    else:
        for field in (
            "left_token_count",
            "right_token_count",
            "edit_distance",
        ):
            if row[field] != "":
                raise RuntimeError(
                    f"C1 field unexpectedly populated: {field}"
                )

        for field in (
            "left_method_count",
            "right_method_count",
            "matched_method_count",
            "matched_similarity_sum",
        ):
            if row[field] == "":
                raise RuntimeError(
                    f"C1 field unexpectedly empty: {field}"
                )


def run(output: Path) -> None:
    root = fixture_root()
    submissions = enumerate_submissions(root)
    pairs = enumerate_pairs(submissions)

    rows = list(measurement_rows(pairs))

    if len(rows) != 240:
        raise RuntimeError(
            f"Expected 240 measurement rows, found {len(rows)}."
        )

    c0_count = sum(row["condition"] == "C0" for row in rows)
    c1_count = sum(row["condition"] == "C1" for row in rows)

    if c0_count != 120 or c1_count != 120:
        raise RuntimeError(
            f"Expected C0=120 and C1=120; "
            f"found C0={c0_count}, C1={c1_count}."
        )

    for row in rows:
        validate_row(row)

    output.parent.mkdir(parents=True, exist_ok=True)

    # newline="" gives csv.writer control of CSV record terminators.
    with output.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=FIELDNAMES,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the canonical Experiment 002 primary "
            "measurement CSV."
        )
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=default_output_path(),
        help="Measurement CSV output path.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run(args.output)


if __name__ == "__main__":
    main()
