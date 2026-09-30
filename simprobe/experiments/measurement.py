from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path

from simprobe.experiments.representation_ladder import (
    STAGES,
    Submission,
    build_pairs,
    represent_submission,
)
from simprobe.similarity.edit import normalized_levenshtein


@dataclass(frozen=True)
class MeasurementRow:
    left_submission: str
    right_submission: str
    left_family: str
    right_family: str
    left_variant: str
    right_variant: str
    pair_label: str
    representation: str
    left_length: int
    right_length: int
    edit_distance: int
    similarity: float


FIELDNAMES = tuple(MeasurementRow.__dataclass_fields__)


def measure_submissions(
    submissions: tuple[Submission, ...],
) -> tuple[MeasurementRow, ...]:
    pairs = build_pairs(submissions)

    representations: dict[tuple[str, str], tuple[str, ...]] = {}

    for submission in submissions:
        for stage in STAGES:
            representations[(submission.submission_id, stage)] = (
                represent_submission(submission, stage)
            )

    rows: list[MeasurementRow] = []

    for pair in pairs:
        for stage in STAGES:
            left_representation = representations[
                (pair.left.submission_id, stage)
            ]
            right_representation = representations[
                (pair.right.submission_id, stage)
            ]

            result = normalized_levenshtein(
                left_representation,
                right_representation,
            )

            rows.append(
                MeasurementRow(
                    left_submission=pair.left.submission_id,
                    right_submission=pair.right.submission_id,
                    left_family=pair.left.family,
                    right_family=pair.right.family,
                    left_variant=pair.left.variant,
                    right_variant=pair.right.variant,
                    pair_label=pair.label,
                    representation=stage,
                    left_length=len(left_representation),
                    right_length=len(right_representation),
                    edit_distance=result.distance,
                    similarity=result.similarity,
                )
            )

    return tuple(rows)


def validate_primary_rows(rows: tuple[MeasurementRow, ...]) -> None:
    if len(rows) != 2646:
        raise ValueError(
            f"Expected 2646 primary measurement rows, found {len(rows)}"
        )

    identities = {
        (
            row.left_submission,
            row.right_submission,
            row.representation,
        )
        for row in rows
    }

    if len(identities) != 2646:
        raise ValueError("Primary measurement rows are not unique")

    expected_representations = set(STAGES)
    actual_representations = {row.representation for row in rows}

    if actual_representations != expected_representations:
        raise ValueError(
            "Primary measurement representation set does not match R0-R6"
        )

    for row in rows:
        if row.left_submission >= row.right_submission:
            raise ValueError(
                "Primary pair ordering is not lexicographically increasing"
            )

        expected_label = (
            "related"
            if row.left_family == row.right_family
            else "control"
        )

        if row.pair_label != expected_label:
            raise ValueError(
                f"Incorrect pair label for "
                f"{row.left_submission} / {row.right_submission}"
            )

        if row.left_length < 0 or row.right_length < 0:
            raise ValueError("Representation length cannot be negative")

        if row.edit_distance < 0:
            raise ValueError("Edit distance cannot be negative")

        if not 0.0 <= row.similarity <= 1.0:
            raise ValueError("Similarity must be between 0 and 1")


def write_measurements_csv(
    rows: tuple[MeasurementRow, ...],
    destination: Path,
) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()

        for row in rows:
            writer.writerow(asdict(row))
