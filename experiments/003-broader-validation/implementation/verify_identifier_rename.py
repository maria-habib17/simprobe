from pathlib import Path
import re

ROOT = Path("experiments/003-broader-validation/fixtures/primary")

METHOD_RE = re.compile(
    r"(?m)^    (?:public )?static\s+[^\n{]+\s+(\w+)\s*\([^)]*\)\s*\{"
)

CLASS_RE = re.compile(r"\bpublic\s+class\s+(\w+)")

checked = 0

for family in "ABCDEFGHIJKL":

    base_files = list((ROOT / family / "BASE").glob("*.java"))
    renamed_files = list((ROOT / family / "IDENTIFIER_RENAME").glob("*.java"))

    if len(base_files) != 1:
        raise RuntimeError(
            f"{family}: expected exactly one BASE Java file"
        )

    if len(renamed_files) != 1:
        raise RuntimeError(
            f"{family}: expected exactly one IDENTIFIER_RENAME Java file"
        )

    base = base_files[0]
    renamed = renamed_files[0]

    base_text = base.read_text(encoding="utf-8")
    renamed_text = renamed.read_text(encoding="utf-8")

    base_class_match = CLASS_RE.search(base_text)
    renamed_class_match = CLASS_RE.search(renamed_text)

    if not base_class_match:
        raise RuntimeError(f"{family}: BASE public class not found")

    if not renamed_class_match:
        raise RuntimeError(f"{family}: renamed public class not found")

    base_class = base_class_match.group(1)
    renamed_class = renamed_class_match.group(1)

    if base_class == renamed_class:
        raise RuntimeError(
            f"{family}: public class identifier was not renamed"
        )

    if renamed.stem != renamed_class:
        raise RuntimeError(
            f"{family}: filename/public-class mismatch: "
            f"{renamed.stem} vs {renamed_class}"
        )

    base_methods = METHOD_RE.findall(base_text)
    renamed_methods = METHOD_RE.findall(renamed_text)

    if len(base_methods) != len(renamed_methods):
        raise RuntimeError(
            f"{family}: method count changed: "
            f"{len(base_methods)} -> {len(renamed_methods)}"
        )

    if not base_methods or not renamed_methods:
        raise RuntimeError(f"{family}: methods not detected")

    if base_methods[-1] != "main":
        raise RuntimeError(f"{family}: BASE main is not final method")

    if renamed_methods[-1] != "main":
        raise RuntimeError(f"{family}: renamed main is not final method")

    base_helpers = base_methods[:-1]
    renamed_helpers = renamed_methods[:-1]

    if len(base_helpers) != len(renamed_helpers):
        raise RuntimeError(f"{family}: helper count changed")

    for old, new in zip(base_helpers, renamed_helpers):
        if old == new:
            raise RuntimeError(
                f"{family}: helper identifier not renamed: {old}"
            )

    expected_helpers = [
        f"operation{i}"
        for i in range(1, len(base_helpers) + 1)
    ]

    if renamed_helpers != expected_helpers:
        raise RuntimeError(
            f"{family}: unexpected helper rename sequence. "
            f"Found {renamed_helpers}; expected {expected_helpers}"
        )

    if renamed_methods.count("main") != 1:
        raise RuntimeError(
            f"{family}: expected exactly one main method"
        )

    print(f"{family}: PASS")
    print(f"  class   : {base_class} -> {renamed_class}")
    print(f"  helpers : {base_helpers}")
    print(f"         -> {renamed_helpers}")

    checked += 1

if checked != 12:
    raise RuntimeError(
        f"Expected 12 structural checks; completed {checked}"
    )

print(f"\nStructural checks: {checked}/12 PASS")
