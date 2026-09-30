import csv
from pathlib import Path

import pytest

from simprobe.experiments.measurement import (
    FIELDNAMES,
    MeasurementRow,
    measure_submissions,
    validate_primary_rows,
    write_measurements_csv,
)
from simprobe.experiments.representation_ladder import Submission


def make_submission(
    root: Path,
    family: str,
    variant: str,
    source: str,
) -> Submission:
    path = root / family / variant
    path.mkdir(parents=True)
    (path / "Program.java").write_text(source, encoding="ascii")

    return Submission(
        family=family,
        variant=variant,
        path=path,
    )


def test_measure_submissions_produces_seven_rows_per_pair(
    tmp_path: Path,
) -> None:
    left = make_submission(
        tmp_path,
        "family-a",
        "BASE",
        "class A { int f() { return 1; } }",
    )
    right = make_submission(
        tmp_path,
        "family-a",
        "IDENTIFIER_RENAME",
        "class B { int g() { return 1; } }",
    )

    rows = measure_submissions((left, right))

    assert len(rows) == 7
    assert [row.representation for row in rows] == [
        "R0",
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
    ]
    assert all(row.pair_label == "related" for row in rows)


def test_measurement_order_is_deterministic(
    tmp_path: Path,
) -> None:
    first = make_submission(
        tmp_path,
        "family-a",
        "BASE",
        "class A {}",
    )
    second = make_submission(
        tmp_path,
        "family-b",
        "BASE",
        "class B {}",
    )
    third = make_submission(
        tmp_path,
        "family-c",
        "BASE",
        "class C {}",
    )

    submissions = (first, second, third)

    first_run = measure_submissions(submissions)
    second_run = measure_submissions(submissions)

    assert first_run == second_run
    assert len(first_run) == 21


def test_cross_family_pair_is_control(
    tmp_path: Path,
) -> None:
    left = make_submission(
        tmp_path,
        "family-a",
        "BASE",
        "class A {}",
    )
    right = make_submission(
        tmp_path,
        "family-b",
        "BASE",
        "class B {}",
    )

    rows = measure_submissions((left, right))

    assert all(row.pair_label == "control" for row in rows)


def test_csv_schema_and_row_order(
    tmp_path: Path,
) -> None:
    left = make_submission(
        tmp_path,
        "family-a",
        "BASE",
        "class A {}",
    )
    right = make_submission(
        tmp_path,
        "family-b",
        "BASE",
        "class B {}",
    )

    rows = measure_submissions((left, right))
    destination = tmp_path / "measurements.csv"

    write_measurements_csv(rows, destination)

    with destination.open(
        encoding="utf-8",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)
        written = list(reader)

    assert tuple(reader.fieldnames or ()) == FIELDNAMES
    assert len(written) == 7
    assert [row["representation"] for row in written] == [
        "R0",
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
    ]


def test_primary_validator_rejects_wrong_row_count() -> None:
    with pytest.raises(
        ValueError,
        match="Expected 2646 primary measurement rows",
    ):
        validate_primary_rows(())


def test_primary_validator_rejects_bad_similarity() -> None:
    valid = MeasurementRow(
        left_submission="family-a/BASE",
        right_submission="family-b/BASE",
        left_family="family-a",
        right_family="family-b",
        left_variant="BASE",
        right_variant="BASE",
        pair_label="control",
        representation="R0",
        left_length=1,
        right_length=1,
        edit_distance=0,
        similarity=2.0,
    )

    # Pad to the required count so validation reaches the uniqueness check
    # before field validation. Duplicate identities must itself be rejected.
    rows = tuple(valid for _ in range(2646))

    with pytest.raises(ValueError, match="not unique"):
        validate_primary_rows(rows)


def test_csv_writer_creates_parent_directory(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "nested" / "measurements.csv"

    write_measurements_csv((), destination)

    assert destination.exists()
