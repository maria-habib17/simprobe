from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class SimilarityResult:
    distance: int
    similarity: float


def levenshtein_distance(left: Sequence[str], right: Sequence[str]) -> int:
    if len(left) < len(right):
        left, right = right, left

    previous = list(range(len(right) + 1))

    for left_index, left_token in enumerate(left, start=1):
        current = [left_index]

        for right_index, right_token in enumerate(right, start=1):
            insertion = current[right_index - 1] + 1
            deletion = previous[right_index] + 1
            substitution = previous[right_index - 1] + (left_token != right_token)

            current.append(min(insertion, deletion, substitution))

        previous = current

    return previous[-1]


def normalized_levenshtein(
    left: Sequence[str],
    right: Sequence[str],
) -> SimilarityResult:
    distance = levenshtein_distance(left, right)
    denominator = max(len(left), len(right))

    if denominator == 0:
        similarity = 1.0
    else:
        similarity = 1.0 - distance / denominator

    return SimilarityResult(distance=distance, similarity=similarity)
