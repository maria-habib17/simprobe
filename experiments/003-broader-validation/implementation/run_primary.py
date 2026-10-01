from __future__ import annotations

import argparse
import csv
import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from compare import compare_c0, compare_c1


CONDITIONS = ("C0", "C1")
FAMILIES = tuple("ABCDEFGHIJKL")
VARIANTS = ("BASE", "METHOD_REORDER", "CLASS_SPLIT", "IDENTIFIER_RENAME")

FIELDNAMES = (
    "condition",
    "family_a",
    "variant_a",
    "family_b",
    "variant_b",
    "pair_label",
    "transformation",
    "similarity",
)


@dataclass(frozen=True)
class Submission:
    family: str
    variant: str
    path: Path


@dataclass(frozen=True)
class Pair:
    left: Submission
    right: Submission
    pair_label: str
    transformation: str


def experiment_root() -> Path:
    return Path(__file__).resolve().parent.parent


def fixture_root() -> Path:
    return experiment_root() / "fixtures" / "primary"


def default_output_path() -> Path:
    return experiment_root() / "results" / "experiment-003-primary-measurements.csv"


def enumerate_submissions(root: Path) -> tuple[Submission, ...]:
    submissions = []

    for family in FAMILIES:
        for variant in VARIANTS:
            path = root / family / variant

            if not path.is_dir():
                raise RuntimeError(f"Missing submission directory: {path}")

            java_files = sorted(path.glob("*.java"))
            expected_files = 2 if variant == "CLASS_SPLIT" else 1

            if len(java_files) != expected_files:
                raise RuntimeError(
                    f"{family}/{variant}: expected {expected_files} Java files, "
                    f"found {len(java_files)}"
                )

            submissions.append(
                Submission(
                    family=family,
                    variant=variant,
                    path=path,
                )
            )

    return tuple(submissions)


def _classify_pair(left: Submission, right: Submission) -> tuple[str, str]:
    if left.family != right.family:
        return "control", ""

    variants = {left.variant, right.variant}

    if "BASE" in variants:
        other = right.variant if left.variant == "BASE" else left.variant

        if other in {
            "METHOD_REORDER",
            "CLASS_SPLIT",
            "IDENTIFIER_RENAME",
        }:
            return "related", other

    return "related", "OTHER_RELATED"


def enumerate_pairs(
    submissions: tuple[Submission, ...],
) -> tuple[Pair, ...]:
    pairs = []

    for left, right in itertools.combinations(submissions, 2):
        pair_label, transformation = _classify_pair(left, right)

        pairs.append(
            Pair(
                left=left,
                right=right,
                pair_label=pair_label,
                transformation=transformation,
            )
        )

    return tuple(pairs)


def c0_row(pair: Pair) -> dict[str, object]:
    result = compare_c0(pair.left.path, pair.right.path)

    return {
        "condition": "C0",
        "family_a": pair.left.family,
        "variant_a": pair.left.variant,
        "family_b": pair.right.family,
        "variant_b": pair.right.variant,
        "pair_label": pair.pair_label,
        "transformation": pair.transformation,
        "similarity": result.similarity,
    }


def c1_row(pair: Pair) -> dict[str, object]:
    result = compare_c1(pair.left.path, pair.right.path)

    return {
        "condition": "C1",
        "family_a": pair.left.family,
        "variant_a": pair.left.variant,
        "family_b": pair.right.family,
        "variant_b": pair.right.variant,
        "pair_label": pair.pair_label,
        "transformation": pair.transformation,
        "similarity": result.similarity,
    }


def measurement_rows(
    pairs: tuple[Pair, ...],
) -> Iterator[dict[str, object]]:
    for pair in pairs:
        yield c0_row(pair)

    for pair in pairs:
        yield c1_row(pair)


def validate_row(row: dict[str, object]) -> None:
    if tuple(row.keys()) != FIELDNAMES:
        raise RuntimeError(f"Unexpected measurement schema: {tuple(row.keys())}")

    similarity = float(row["similarity"])

    if not 0.0 <= similarity <= 1.0:
        raise RuntimeError(f"Similarity outside [0, 1]: {similarity}")

    if row["condition"] not in CONDITIONS:
        raise RuntimeError(f"Unexpected condition: {row['condition']}")

    if row["pair_label"] not in {"related", "control"}:
        raise RuntimeError(f"Unexpected pair label: {row['pair_label']}")


def validate_enumeration(
    submissions: tuple[Submission, ...],
    pairs: tuple[Pair, ...],
) -> None:
    if len(submissions) != 48:
        raise RuntimeError(f"Expected 48 submissions; found {len(submissions)}")

    if len(pairs) != 1128:
        raise RuntimeError(f"Expected 1128 pairs; found {len(pairs)}")

    related = sum(pair.pair_label == "related" for pair in pairs)
    controls = sum(pair.pair_label == "control" for pair in pairs)

    if related != 72:
        raise RuntimeError(f"Expected 72 related pairs; found {related}")

    if controls != 1056:
        raise RuntimeError(f"Expected 1056 control pairs; found {controls}")


def run(output: Path) -> None:
    submissions = enumerate_submissions(fixture_root())
    pairs = enumerate_pairs(submissions)
    validate_enumeration(submissions, pairs)

    rows = list(measurement_rows(pairs))

    if len(rows) != 2256:
        raise RuntimeError(f"Expected 2256 measurement rows; found {len(rows)}")

    for row in rows:
        validate_row(row)

    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Rows written: {len(rows)}")
    print(f"Output: {output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=default_output_path(),
        help="Measurement CSV output path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate fixture enumeration without computing similarities.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    submissions = enumerate_submissions(fixture_root())
    pairs = enumerate_pairs(submissions)
    validate_enumeration(submissions, pairs)

    related = sum(pair.pair_label == "related" for pair in pairs)
    controls = sum(pair.pair_label == "control" for pair in pairs)

    print(f"Families: {len(FAMILIES)}")
    print(f"Submissions: {len(submissions)}")
    print(f"Pairs per condition: {len(pairs)}")
    print(f"Related pairs per condition: {related}")
    print(f"Control pairs per condition: {controls}")

    if args.dry_run:
        print("Dry run complete. No measurements generated.")
        return

    run(args.output)


if __name__ == "__main__":
    main()
