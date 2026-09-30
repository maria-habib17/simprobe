from __future__ import annotations

from pathlib import Path

from simprobe.experiments.measurement import (
    measure_submissions,
    validate_primary_rows,
    write_measurements_csv,
)
from simprobe.experiments.representation_ladder import discover_submissions

PRIMARY_ROOT = Path(
    "experiments/001-representation-ladder/fixtures/primary"
)

OUTPUT = Path(
    "results/experiment-001-primary-measurements.csv"
)


def main() -> None:
    submissions = discover_submissions(PRIMARY_ROOT)

    if len(submissions) != 28:
        raise RuntimeError(
            f"Expected 28 primary submissions, found {len(submissions)}"
        )

    rows = measure_submissions(submissions)
    validate_primary_rows(rows)
    write_measurements_csv(rows, OUTPUT)

    print(f"submissions={len(submissions)}")
    print(f"rows={len(rows)}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
