import pytest

from simprobe.similarity.edit import levenshtein_distance, normalized_levenshtein


def test_known_levenshtein_distance() -> None:
    left = ("a", "b", "c")
    right = ("a", "x", "c", "d")

    assert levenshtein_distance(left, right) == 2


def test_normalized_similarity() -> None:
    result = normalized_levenshtein(("a", "b", "c"), ("a", "x", "c"))

    assert result.distance == 1
    assert result.similarity == pytest.approx(2 / 3)


def test_empty_sequences_are_identical() -> None:
    result = normalized_levenshtein((), ())

    assert result.distance == 0
    assert result.similarity == 1.0


def test_one_empty_sequence_has_zero_similarity() -> None:
    result = normalized_levenshtein(("x",), ())

    assert result.distance == 1
    assert result.similarity == 0.0
