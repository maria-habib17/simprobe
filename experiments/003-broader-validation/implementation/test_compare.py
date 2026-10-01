import tempfile
import unittest
from pathlib import Path

from compare import (
    MethodUnit,
    compare_c0,
    compare_c1,
    compare_method_units,
    extract_method_units,
    lex_java,
    maximum_weight_matching,
    normalized_similarity,
    normalized_tokens,
)


def unit(*tokens: str) -> MethodUnit:
    return MethodUnit(
        relative_path="Synthetic.java",
        source_start=0,
        tokens=tuple(tokens),
    )


class LexerTests(unittest.TestCase):
    def test_comments_are_discarded(self):
        source = """
        // line comment
        int value = 12;
        /* block comment */
        value++;
        """

        values = [token.value for token in lex_java(source)]

        self.assertEqual(
            values,
            ["int", "value", "=", "12", ";", "value", "++", ";"],
        )

    def test_literal_braces_do_not_break_lexing(self):
        source = r'''
        String text = "{ not a body }";
        char brace = '}';
        '''

        tokens = lex_java(source)

        self.assertEqual(
            [token.kind for token in tokens],
            [
                "IDENT",
                "IDENT",
                "SYMBOL",
                "STRING",
                "SYMBOL",
                "KEYWORD",
                "IDENT",
                "SYMBOL",
                "CHAR",
                "SYMBOL",
            ],
        )

    def test_primary_normalization(self):
        source = 'int total = value + 17; System.out.println("x");'

        self.assertEqual(
            normalized_tokens(source),
            (
                "int",
                "<IDENT>",
                "=",
                "<IDENT>",
                "+",
                "<INT>",
                ";",
                "<IDENT>",
                ".",
                "<IDENT>",
                ".",
                "<IDENT>",
                "(",
                "<STRING>",
                ")",
                ";",
            ),
        )


class SimilarityTests(unittest.TestCase):
    def test_identical_sequences(self):
        distance, similarity = normalized_similarity(
            ("a", "b"),
            ("a", "b"),
        )

        self.assertEqual(distance, 0)
        self.assertEqual(similarity, 1.0)

    def test_empty_sequences(self):
        self.assertEqual(
            normalized_similarity((), ()),
            (0, 1.0),
        )

        self.assertEqual(
            normalized_similarity(("x",), ()),
            (1, 0.0),
        )

    def test_known_levenshtein(self):
        distance, similarity = normalized_similarity(
            ("a", "b", "c"),
            ("a", "x", "c"),
        )

        self.assertEqual(distance, 1)
        self.assertAlmostEqual(similarity, 2 / 3)


class MethodExtractionTests(unittest.TestCase):
    def test_extracts_main_and_helpers(self):
        source = """
        public class Example {
            public static void main(String[] args) {
                helper();
            }

            private static int helper() {
                return 3;
            }

            static int second(int value) {
                return value + 1;
            }
        }
        """

        units = extract_method_units(source, "Example.java")

        self.assertEqual(len(units), 3)

    def test_calls_are_not_methods(self):
        source = """
        public class Example {
            public static void main(String[] args) {
                System.out.println("x");
                helper();
            }

            private static void helper() {
                System.out.println("y");
            }
        }
        """

        units = extract_method_units(source, "Example.java")

        self.assertEqual(len(units), 2)

    def test_braces_inside_literals_and_comments(self):
        source = r'''
        class Example {
            static void first() {
                String text = "}";
                // }
                /* { } */
            }

            static char second() {
                return '}';
            }
        }
        '''

        units = extract_method_units(source, "Example.java")

        self.assertEqual(len(units), 2)

    def test_identifier_rename_normalizes_exactly(self):
        left = """
        class A {
            static int add(int value) {
                int result = value + 1;
                return result;
            }
        }
        """

        right = """
        class B {
            static int compute(int number) {
                int answer = number + 7;
                return answer;
            }
        }
        """

        left_units = extract_method_units(left, "A.java")
        right_units = extract_method_units(right, "B.java")

        self.assertEqual(len(left_units), 1)
        self.assertEqual(len(right_units), 1)

        # Integer values are also abstracted by the frozen normalization.
        self.assertEqual(left_units[0].tokens, right_units[0].tokens)


class MatchingTests(unittest.TestCase):
    def test_exact_maximum_assignment(self):
        result = maximum_weight_matching(
            (
                (0.9, 0.2),
                (0.3, 0.8),
            )
        )

        self.assertAlmostEqual(result.total_weight, 1.7)
        self.assertEqual(result.assignment, ((0, 0), (1, 1)))

    def test_global_optimum_not_greedy(self):
        result = maximum_weight_matching(
            (
                (0.9, 0.8),
                (0.85, 0.1),
            )
        )

        self.assertAlmostEqual(result.total_weight, 1.65)
        self.assertEqual(result.assignment, ((0, 1), (1, 0)))

    def test_tie_uses_lexicographically_smallest_assignment(self):
        result = maximum_weight_matching(
            (
                (1.0, 1.0),
                (1.0, 1.0),
            )
        )

        self.assertEqual(result.total_weight, 2.0)
        self.assertEqual(result.assignment, ((0, 0), (1, 1)))

    def test_more_rows_than_columns(self):
        result = maximum_weight_matching(
            (
                (0.1,),
                (0.9,),
            )
        )

        self.assertAlmostEqual(result.total_weight, 0.9)
        self.assertEqual(result.assignment, ((1, 0),))


class C1AggregationTests(unittest.TestCase):
    def test_unmatched_unit_is_zero_penalty(self):
        left = [
            unit("a"),
            unit("b"),
        ]
        right = [
            unit("a"),
        ]

        result = compare_method_units(left, right)

        self.assertEqual(result.left_method_count, 2)
        self.assertEqual(result.right_method_count, 1)
        self.assertEqual(result.matched_method_count, 1)
        self.assertEqual(result.matched_similarity_sum, 1.0)
        self.assertEqual(result.similarity, 0.5)

    def test_both_empty(self):
        result = compare_method_units([], [])

        self.assertEqual(result.similarity, 1.0)

    def test_one_empty(self):
        result = compare_method_units([unit("x")], [])

        self.assertEqual(result.similarity, 0.0)


class ConditionBehaviorTests(unittest.TestCase):
    def write_submission(
        self,
        root: Path,
        name: str,
        source: str,
    ) -> Path:
        directory = root / name
        directory.mkdir()
        (directory / "Example.java").write_text(
            source,
            encoding="utf-8",
        )
        return directory

    def test_method_reorder_changes_c0_but_not_c1(self):
        source_a = """
        public class Example {
            public static void main(String[] args) {
                first();
                second();
            }

            static int first() {
                return 1;
            }

            static int second() {
                int value = 2;
                return value;
            }
        }
        """

        source_b = """
        public class Example {
            public static void main(String[] args) {
                first();
                second();
            }

            static int second() {
                int value = 2;
                return value;
            }

            static int first() {
                return 1;
            }
        }
        """

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            left = self.write_submission(root, "left", source_a)
            right = self.write_submission(root, "right", source_b)

            c0 = compare_c0(left, right)
            c1 = compare_c1(left, right)

            self.assertLess(c0.similarity, 1.0)
            self.assertEqual(c1.similarity, 1.0)

    def test_identifier_rename_is_abstracted(self):
        source_a = """
        public class Example {
            public static void main(String[] args) {
                int value = helper(3);
                System.out.println(value);
            }

            static int helper(int value) {
                return value + 1;
            }
        }
        """

        source_b = """
        public class Renamed {
            public static void main(String[] parameters) {
                int answer = compute(9);
                System.out.println(answer);
            }

            static int compute(int number) {
                return number + 7;
            }
        }
        """

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            left = self.write_submission(root, "left", source_a)
            right = self.write_submission(root, "right", source_b)

            c0 = compare_c0(left, right)
            c1 = compare_c1(left, right)

            self.assertEqual(c0.similarity, 1.0)
            self.assertEqual(c1.similarity, 1.0)

    def test_class_split_preserves_method_collection(self):
        source_single = """
        public class Example {
            public static void main(String[] args) {
                int value = first();
                System.out.println(second(value));
            }

            static int first() {
                return 1;
            }

            static int second(int value) {
                return value + 1;
            }
        }
        """

        split_entry = """
        public class Example {
            public static void main(String[] args) {
                int value = Helper.first();
                System.out.println(Helper.second(value));
            }
        }
        """

        split_helper = """
        class Helper {
            static int first() {
                return 1;
            }

            static int second(int value) {
                return value + 1;
            }
        }
        """

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            left = root / "left"
            left.mkdir()
            (left / "Example.java").write_text(
                source_single,
                encoding="utf-8",
            )

            right = root / "right"
            right.mkdir()
            (right / "Example.java").write_text(
                split_entry,
                encoding="utf-8",
            )
            (right / "Helper.java").write_text(
                split_helper,
                encoding="utf-8",
            )

            result = compare_c1(left, right)

            self.assertEqual(result.left_method_count, 3)
            self.assertEqual(result.right_method_count, 3)

            # The moved helper methods remain exact after abstraction.
            # main changes because the calls gain Helper. qualification.
            self.assertGreater(result.similarity, 0.9)
            self.assertLess(result.similarity, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
