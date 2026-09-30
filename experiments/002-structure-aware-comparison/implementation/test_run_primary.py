import unittest
from pathlib import Path

from run_primary import (
    CONDITIONS,
    FAMILIES,
    FIELDNAMES,
    VARIANTS,
    default_output_path,
    enumerate_pairs,
    enumerate_submissions,
    fixture_root,
)


class FrozenMetadataTests(unittest.TestCase):
    def test_conditions(self):
        self.assertEqual(CONDITIONS, ("C0", "C1"))

    def test_families(self):
        self.assertEqual(
            FAMILIES,
            (
                "family-a",
                "family-b",
                "family-c",
                "family-d",
            ),
        )

    def test_variants(self):
        self.assertEqual(
            VARIANTS,
            (
                "BASE",
                "CLASS_SPLIT",
                "IDENTIFIER_RENAME",
                "METHOD_REORDER",
            ),
        )

    def test_schema(self):
        self.assertEqual(
            FIELDNAMES,
            (
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
            ),
        )


class PrimaryFixtureEnumerationTests(unittest.TestCase):
    def setUp(self):
        self.root = fixture_root()
        self.submissions = enumerate_submissions(self.root)
        self.pairs = enumerate_pairs(self.submissions)

    def test_submission_count(self):
        self.assertEqual(len(self.submissions), 16)

    def test_submission_order(self):
        identifiers = tuple(
            submission.identifier
            for submission in self.submissions
        )

        self.assertEqual(
            identifiers,
            tuple(
                f"{family}/{variant}"
                for family in FAMILIES
                for variant in VARIANTS
            ),
        )

    def test_pair_count(self):
        self.assertEqual(len(self.pairs), 120)

    def test_pair_label_counts(self):
        related = sum(
            pair.pair_label == "related"
            for pair in self.pairs
        )
        control = sum(
            pair.pair_label == "control"
            for pair in self.pairs
        )

        self.assertEqual(related, 24)
        self.assertEqual(control, 96)

    def test_each_related_family_has_six_pairs(self):
        for family in FAMILIES:
            count = sum(
                pair.pair_label == "related"
                and pair.left.family == family
                and pair.right.family == family
                for pair in self.pairs
            )

            self.assertEqual(count, 6)

    def test_every_pair_is_strictly_ordered(self):
        index = {
            submission.identifier: position
            for position, submission in enumerate(self.submissions)
        }

        for pair in self.pairs:
            self.assertLess(
                index[pair.left.identifier],
                index[pair.right.identifier],
            )

    def test_no_duplicate_unordered_pairs(self):
        keys = {
            (
                pair.left.identifier,
                pair.right.identifier,
            )
            for pair in self.pairs
        }

        self.assertEqual(len(keys), 120)

    def test_fixture_java_file_count(self):
        files = tuple(
            path
            for path in self.root.rglob("*.java")
            if path.is_file()
        )

        self.assertEqual(len(files), 20)

    def test_variant_file_counts(self):
        for submission in self.submissions:
            files = tuple(
                path
                for path in submission.path.rglob("*.java")
                if path.is_file()
            )

            expected = (
                2
                if submission.variant == "CLASS_SPLIT"
                else 1
            )

            self.assertEqual(len(files), expected)


class OutputMetadataTests(unittest.TestCase):
    def test_default_output_is_inside_experiment_results(self):
        output = default_output_path()

        self.assertEqual(
            output.name,
            "experiment-002-primary-measurements.csv",
        )
        self.assertEqual(output.parent.name, "results")

    def test_default_output_does_not_exist_before_primary_run(self):
        self.assertFalse(default_output_path().exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
