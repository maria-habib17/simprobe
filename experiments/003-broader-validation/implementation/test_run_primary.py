from pathlib import Path
import unittest

import run_primary as runner


class FrozenMetadataTests(unittest.TestCase):

    def test_families(self):
        self.assertEqual(tuple("ABCDEFGHIJKL"), runner.FAMILIES)

    def test_variants(self):
        self.assertEqual(
            ("BASE", "METHOD_REORDER", "CLASS_SPLIT", "IDENTIFIER_RENAME"),
            runner.VARIANTS,
        )

    def test_conditions(self):
        self.assertEqual(("C0", "C1"), runner.CONDITIONS)

    def test_schema(self):
        self.assertEqual(
            (
                "condition",
                "family_a",
                "variant_a",
                "family_b",
                "variant_b",
                "pair_label",
                "transformation",
                "similarity",
            ),
            runner.FIELDNAMES,
        )


class PrimaryFixtureEnumerationTests(unittest.TestCase):

    def setUp(self):
        self.submissions = runner.enumerate_submissions(runner.fixture_root())
        self.pairs = runner.enumerate_pairs(self.submissions)

    def test_submission_count(self):
        self.assertEqual(48, len(self.submissions))

    def test_pair_count(self):
        self.assertEqual(1128, len(self.pairs))

    def test_submission_order(self):
        observed = [
            (submission.family, submission.variant)
            for submission in self.submissions
        ]

        expected = [
            (family, variant)
            for family in runner.FAMILIES
            for variant in runner.VARIANTS
        ]

        self.assertEqual(expected, observed)

    def test_variant_file_counts(self):
        for submission in self.submissions:
            expected = 2 if submission.variant == "CLASS_SPLIT" else 1
            self.assertEqual(
                expected,
                len(list(submission.path.glob("*.java"))),
            )

    def test_fixture_java_file_count(self):
        count = sum(
            len(list(submission.path.glob("*.java")))
            for submission in self.submissions
        )
        self.assertEqual(60, count)

    def test_pair_label_counts(self):
        related = sum(pair.pair_label == "related" for pair in self.pairs)
        controls = sum(pair.pair_label == "control" for pair in self.pairs)

        self.assertEqual(72, related)
        self.assertEqual(1056, controls)

    def test_each_related_family_has_six_pairs(self):
        counts = {family: 0 for family in runner.FAMILIES}

        for pair in self.pairs:
            if pair.pair_label == "related":
                self.assertEqual(pair.left.family, pair.right.family)
                counts[pair.left.family] += 1

        self.assertEqual(
            {family: 6 for family in runner.FAMILIES},
            counts,
        )

    def test_no_duplicate_unordered_pairs(self):
        seen = set()

        for pair in self.pairs:
            left = (pair.left.family, pair.left.variant)
            right = (pair.right.family, pair.right.variant)
            key = tuple(sorted((left, right)))

            self.assertNotIn(key, seen)
            seen.add(key)

        self.assertEqual(1128, len(seen))

    def test_every_pair_is_strictly_ordered(self):
        positions = {
            (submission.family, submission.variant): index
            for index, submission in enumerate(self.submissions)
        }

        for pair in self.pairs:
            left = (pair.left.family, pair.left.variant)
            right = (pair.right.family, pair.right.variant)
            self.assertLess(positions[left], positions[right])

    def test_base_transformation_labels(self):
        expected = {
            "METHOD_REORDER",
            "CLASS_SPLIT",
            "IDENTIFIER_RENAME",
        }

        for family in runner.FAMILIES:
            observed = set()

            for pair in self.pairs:
                if pair.left.family != family or pair.right.family != family:
                    continue

                if "BASE" in {pair.left.variant, pair.right.variant}:
                    if pair.transformation != "OTHER_RELATED":
                        observed.add(pair.transformation)

            self.assertEqual(expected, observed)


class OutputMetadataTests(unittest.TestCase):

    def test_default_output_is_inside_experiment_results(self):
        self.assertEqual(
            runner.experiment_root()
            / "results"
            / "experiment-003-primary-measurements.csv",
            runner.default_output_path(),
        )

    def test_default_output_does_not_exist_before_primary_run(self):
        self.assertFalse(runner.default_output_path().exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
