from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

from simprobe.representations.java import STAGES, represent_source

EXPECTED_FAMILIES = ("family-a", "family-b", "family-c", "family-d")
EXPECTED_VARIANTS = (
    "BASE",
    "CLASS_RENAME",
    "CLASS_SPLIT",
    "DEAD_CODE",
    "FILE_RENAME",
    "IDENTIFIER_RENAME",
    "METHOD_REORDER",
)


@dataclass(frozen=True, order=True)
class Submission:
    family: str
    variant: str
    path: Path

    @property
    def submission_id(self) -> str:
        return f"{self.family}/{self.variant}"


@dataclass(frozen=True)
class SubmissionPair:
    left: Submission
    right: Submission
    label: str


def discover_submissions(primary_root: Path) -> tuple[Submission, ...]:
    submissions: list[Submission] = []

    for family in EXPECTED_FAMILIES:
        family_root = primary_root / family

        for variant in EXPECTED_VARIANTS:
            submission_path = family_root / variant

            if not submission_path.is_dir():
                raise ValueError(f"Missing submission directory: {submission_path}")

            if not any(submission_path.glob("*.java")):
                raise ValueError(f"No Java sources in submission: {submission_path}")

            submissions.append(
                Submission(
                    family=family,
                    variant=variant,
                    path=submission_path,
                )
            )

    return tuple(sorted(submissions, key=lambda item: item.submission_id))


def java_files(submission: Submission) -> tuple[Path, ...]:
    return tuple(
        sorted(
            submission.path.glob("*.java"),
            key=lambda path: path.relative_to(submission.path).as_posix(),
        )
    )


def represent_submission(
    submission: Submission,
    stage: str,
) -> tuple[str, ...]:
    stage = stage.upper()

    if stage not in STAGES:
        raise ValueError(f"Unknown representation stage: {stage}")

    file_sequences = [
        represent_source(path.read_text(encoding="ascii"), stage)
        for path in java_files(submission)
    ]

    combined: list[str] = []

    for index, sequence in enumerate(file_sequences):
        if index:
            combined.append("<FILE_BOUNDARY>")
        combined.extend(sequence)

    if stage == "R6":
        # R6 source sequences are already collapsed individually. Re-collapse
        # across the combined stream while preserving file boundaries.
        collapsed: list[str] = []
        for symbol in combined:
            if symbol == "<FILE_BOUNDARY>" or not collapsed or collapsed[-1] != symbol:
                collapsed.append(symbol)
        return tuple(collapsed)

    return tuple(combined)


def build_pairs(submissions: tuple[Submission, ...]) -> tuple[SubmissionPair, ...]:
    pairs: list[SubmissionPair] = []

    for left, right in combinations(submissions, 2):
        label = "related" if left.family == right.family else "control"
        pairs.append(SubmissionPair(left=left, right=right, label=label))

    return tuple(pairs)
