from pathlib import Path
import subprocess
import sys

ROOT = Path("experiments/003-broader-validation/fixtures/primary")
VARIANTS = ["BASE", "METHOD_REORDER", "CLASS_SPLIT", "IDENTIFIER_RENAME"]

TESTS = {
    "A": [
        ("5 -3 7 0 12 -8\n", "min=-8\nmax=12\nspread=20\nnonnegative=3"),
        ("4 -9 -2 -7 -1\n", "min=-9\nmax=-1\nspread=8\nnonnegative=0"),
        ("1 6\n", "min=6\nmax=6\nspread=0\nnonnegative=1"),
    ],
    "B": [
        ("red green blue\n", "words=3\nshortest=3\nlongest=5\neven=1"),
        ("Java makes tools useful\n", "words=4\nshortest=4\nlongest=6\neven=2"),
        ("code\n", "words=1\nshortest=4\nlongest=4\neven=1"),
    ],
    "C": [
        ("120345\n", "even=3\nodd=3\nevenSum=6\noddSum=9"),
        ("86420\n", "even=5\nodd=0\nevenSum=20\noddSum=0"),
        ("97531\n", "even=0\nodd=5\nevenSum=0\noddSum=25"),
    ],
    "D": [
        ("3 4\n1100\n0000\n1110\n", "ones=5\nnonemptyRows=2\nfullRows=0\nmaxRow=3"),
        ("2 3\n111\n101\n", "ones=5\nnonemptyRows=2\nfullRows=1\nmaxRow=3"),
        ("1 2\n00\n", "ones=0\nnonemptyRows=0\nfullRows=0\nmaxRow=0"),
    ],
    "E": [
        ("5 3 -2 -4 7 -1\n", "positive=2\nnegative=3\nchanges=3\nabsSum=17"),
        ("4 -1 -2 -3 -4\n", "positive=0\nnegative=4\nchanges=0\nabsSum=10"),
        ("3 5 6 7\n", "positive=3\nnegative=0\nchanges=0\nabsSum=18"),
    ],
    "F": [
        ("education\n", "length=9\nvowels=5\nruns=4\nstartsVowel=1"),
        ("strength\n", "length=8\nvowels=1\nruns=1\nstartsVowel=0"),
        ("queue\n", "length=5\nvowels=4\nruns=1\nstartsVowel=0"),
    ],
    "G": [
        ("5 3 -1 4 -8 5\n", "final=3\nmaxPrefix=6\nminPrefix=-2\npositivePrefixes=4"),
        ("3 -2 -3 -1\n", "final=-6\nmaxPrefix=-2\nminPrefix=-6\npositivePrefixes=0"),
        ("4 2 2 2 2\n", "final=8\nmaxPrefix=8\nminPrefix=2\npositivePrefixes=4"),
    ],
    "H": [
        ("banana\n", "distinct=3\nmaxFreq=3\nminFreq=1\nrepeated=2"),
        ("abcd\n", "distinct=4\nmaxFreq=1\nminFreq=1\nrepeated=0"),
        ("mississippi\n", "distinct=4\nmaxFreq=4\nminFreq=1\nrepeated=3"),
    ],
    "I": [
        ("3\n1 2 3\n4 5 6\n7 8 9\n", "main=15\nanti=15\nequalPositions=1\ncenter=5"),
        ("2\n1 4\n3 2\n", "main=3\nanti=7\nequalPositions=0\ncenter=0"),
        ("1\n8\n", "main=8\nanti=8\nequalPositions=1\ncenter=8"),
    ],
    "J": [
        ("6 1 1 3 7 7 10\n", "duplicates=2\npositiveGaps=3\nmaxGap=4\nspan=9"),
        ("4 -5 -2 0 9\n", "duplicates=0\npositiveGaps=3\nmaxGap=9\nspan=14"),
        ("1 12\n", "duplicates=0\npositiveGaps=0\nmaxGap=0\nspan=0"),
    ],
    "K": [
        ("NESW\n", "x=0\ny=0\ndistance=0\nreturns=1"),
        ("NNESW\n", "x=0\ny=1\ndistance=1\nreturns=0"),
        ("NSNS\n", "x=0\ny=0\ndistance=0\nreturns=2"),
    ],
    "L": [
        ("12\n", "div2=6\ndiv3=4\ndivBoth=2\nneither=4"),
        ("5\n", "div2=2\ndiv3=1\ndivBoth=0\nneither=2"),
        ("1\n", "div2=0\ndiv3=0\ndivBoth=0\nneither=1"),
    ],
}

def main_class(directory):
    files = sorted(directory.glob("*.java"))
    if not files:
        raise RuntimeError(f"No Java files in {directory}")

    for source in files:
        text = source.read_text(encoding="utf-8")
        if "public static void main" in text:
            return source.stem

    raise RuntimeError(f"No main class found in {directory}")

passed = 0
submissions = 0

try:
    for family in "ABCDEFGHIJKL":
        for variant in VARIANTS:
            directory = ROOT / family / variant

            if not directory.is_dir():
                raise RuntimeError(f"Missing submission: {family}/{variant}")

            sources = sorted(directory.glob("*.java"))

            expected_files = 2 if variant == "CLASS_SPLIT" else 1
            if len(sources) != expected_files:
                raise RuntimeError(
                    f"{family}/{variant}: expected {expected_files} Java files, "
                    f"found {len(sources)}"
                )

            compile_result = subprocess.run(
                ["javac", *[p.name for p in sources]],
                cwd=directory,
                text=True,
                capture_output=True,
            )

            if compile_result.returncode != 0:
                raise RuntimeError(
                    f"{family}/{variant}: compilation failed\n"
                    + compile_result.stderr
                )

            entry = main_class(directory)

            for index, (input_text, expected) in enumerate(TESTS[family], 1):
                result = subprocess.run(
                    ["java", entry],
                    cwd=directory,
                    input=input_text,
                    text=True,
                    capture_output=True,
                )

                if result.returncode != 0:
                    raise RuntimeError(
                        f"{family}/{variant}/test{index}: execution failed\n"
                        + result.stderr
                    )

                actual = result.stdout.replace("\r\n", "\n").strip()

                if actual != expected:
                    raise RuntimeError(
                        f"{family}/{variant}/test{index}: output mismatch\n"
                        f"EXPECTED:\n{expected}\nACTUAL:\n{actual}"
                    )

                passed += 1

            submissions += 1
            print(f"{family}/{variant}: 3/3 PASS")

finally:
    for artifact in ROOT.rglob("*.class"):
        artifact.unlink()

if submissions != 48:
    raise RuntimeError(f"Expected 48 submissions; validated {submissions}")

if passed != 144:
    raise RuntimeError(f"Expected 144 executions; passed {passed}")

java_files = list(ROOT.rglob("*.java"))
class_files = list(ROOT.rglob("*.class"))

if len(java_files) != 60:
    raise RuntimeError(f"Expected 60 Java files; found {len(java_files)}")

if class_files:
    raise RuntimeError(f"Unexpected .class files remain: {len(class_files)}")

print("\n========================================")
print("EXPERIMENT 003 PRIMARY FIXTURE VALID")
print(f"Families              : 12")
print(f"Submissions           : {submissions}")
print(f"Behavioral executions : {passed} / 144")
print(f"Java files            : {len(java_files)}")
print(f"Class files           : {len(class_files)}")
print("========================================")
