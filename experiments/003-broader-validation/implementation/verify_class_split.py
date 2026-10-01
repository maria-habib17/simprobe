from pathlib import Path
import re

ROOT = Path("experiments/003-broader-validation/fixtures/primary")

MOVED = {
    "A": ["minimum", "maximum"],
    "B": ["shortest", "longest"],
    "C": ["isEven", "evenCount"],
    "D": ["rowOnes", "totalOnes"],
    "E": ["isPositive", "positiveCount"],
    "F": ["isVowel", "vowelCount"],
    "G": ["finalSum", "maximumPrefix"],
    "H": ["frequencies", "distinctCount"],
    "I": ["mainDiagonal", "antiDiagonal"],
    "J": ["duplicateCount", "positiveGapCount"],
    "K": ["finalX", "finalY"],
    "L": ["divisibleBy2", "divisibleBy3"],
}

PATTERN = re.compile(r"(?m)^    (?:public )?static\s+[^\n{]+\s+(\w+)\s*\([^)]*\)\s*\{")

for family in "ABCDEFGHIJKL":
    base_files = list((ROOT / family / "BASE").glob("*.java"))
    split_files = list((ROOT / family / "CLASS_SPLIT").glob("*.java"))

    if len(base_files) != 1:
        raise RuntimeError(f"{family}: expected one BASE file")
    if len(split_files) != 2:
        raise RuntimeError(f"{family}: expected two CLASS_SPLIT files")

    base = base_files[0]
    class_name = base.stem
    support_name = class_name + "Support"

    primary = ROOT / family / "CLASS_SPLIT" / base.name
    support = ROOT / family / "CLASS_SPLIT" / f"{support_name}.java"

    if not primary.exists() or not support.exists():
        raise RuntimeError(f"{family}: expected primary/support file pair missing")

    base_methods = PATTERN.findall(base.read_text(encoding="utf-8"))
    primary_methods = PATTERN.findall(primary.read_text(encoding="utf-8"))
    support_methods = PATTERN.findall(support.read_text(encoding="utf-8"))

    base_helpers = [x for x in base_methods if x != "main"]
    expected_moved = MOVED[family]
    expected_kept = [x for x in base_helpers if x not in expected_moved]

    if primary_methods != expected_kept + ["main"]:
        raise RuntimeError(
            f"{family}: primary method layout mismatch: {primary_methods}"
        )

    if support_methods != expected_moved:
        raise RuntimeError(
            f"{family}: support method layout mismatch: {support_methods}"
        )

    combined = primary_methods[:-1] + support_methods
    if set(combined) != set(base_helpers):
        raise RuntimeError(f"{family}: helper method set changed")

    if len(combined) != len(base_helpers):
        raise RuntimeError(f"{family}: duplicate or missing helper methods")

    if primary_methods.count("main") != 1:
        raise RuntimeError(f"{family}: primary must contain exactly one main")

    if "main" in support_methods:
        raise RuntimeError(f"{family}: support class unexpectedly contains main")

    print(f"{family}: PASS")
    print(f"  primary : {primary_methods}")
    print(f"  support : {support_methods}")

print("\nStructural checks: 12/12 PASS")
