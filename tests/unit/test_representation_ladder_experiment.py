from pathlib import Path

from simprobe.experiments.representation_ladder import (
    Submission,
    build_pairs,
    discover_submissions,
    represent_submission,
)

PRIMARY_ROOT = Path(
    "experiments/001-representation-ladder/fixtures/primary"
)


def test_primary_fixture_has_exactly_28_submissions() -> None:
    submissions = discover_submissions(PRIMARY_ROOT)

    assert len(submissions) == 28
    assert len({submission.submission_id for submission in submissions}) == 28


def test_primary_fixture_has_exactly_378_unordered_pairs() -> None:
    submissions = discover_submissions(PRIMARY_ROOT)
    pairs = build_pairs(submissions)

    assert len(pairs) == 378
    assert len(pairs) * 7 == 2646


def test_pair_labels_follow_family_provenance() -> None:
    root = Path("unused")

    a_base = Submission("family-a", "BASE", root / "a")
    a_rename = Submission("family-a", "IDENTIFIER_RENAME", root / "b")
    b_base = Submission("family-b", "BASE", root / "c")

    related = build_pairs((a_base, a_rename))
    control = build_pairs((a_base, b_base))

    assert related[0].label == "related"
    assert control[0].label == "control"


def test_multifile_representation_uses_sorted_order_and_boundary(
    tmp_path: Path,
) -> None:
    submission_path = tmp_path / "submission"
    submission_path.mkdir()

    (submission_path / "Z.java").write_text(
        "class Z {}",
        encoding="ascii",
    )
    (submission_path / "A.java").write_text(
        "class A {}",
        encoding="ascii",
    )

    submission = Submission("family-a", "CLASS_SPLIT", submission_path)

    representation = represent_submission(submission, "R0")

    assert representation == (
        "class",
        "A",
        "{",
        "}",
        "<FILE_BOUNDARY>",
        "class",
        "Z",
        "{",
        "}",
    )


def test_all_primary_sources_scan_at_every_stage() -> None:
    submissions = discover_submissions(PRIMARY_ROOT)

    for submission in submissions:
        for stage in ("R0", "R1", "R2", "R3", "R4", "R5", "R6"):
            representation = represent_submission(submission, stage)
            assert isinstance(representation, tuple)


def test_primary_r0_and_r1_match_for_every_submission() -> None:
    submissions = discover_submissions(PRIMARY_ROOT)

    for submission in submissions:
        assert represent_submission(
            submission,
            "R0",
        ) == represent_submission(
            submission,
            "R1",
        )
