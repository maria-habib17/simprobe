from pathlib import Path
import re

root = Path("experiments/003-broader-validation/fixtures/primary")
pattern = re.compile(r"(?m)^    (?:public )?static\s+[^\n{]+\s+(\w+)\s*\([^)]*\)\s*\{")

checked = 0

for family in "ABCDEFGHIJKL":
    base_files = list((root / family / "BASE").glob("*.java"))
    transformed_files = list((root / family / "METHOD_REORDER").glob("*.java"))

    if len(base_files) != 1 or len(transformed_files) != 1:
        raise RuntimeError(f"{family}: expected one BASE and one METHOD_REORDER Java file")

    base = base_files[0]
    transformed = transformed_files[0]

    b = pattern.findall(base.read_text(encoding="utf-8"))
    t = pattern.findall(transformed.read_text(encoding="utf-8"))

    if set(b) != set(t):
        raise RuntimeError(f"{family}: method set changed")

    if not b or b[-1] != "main" or t[-1] != "main":
        raise RuntimeError(f"{family}: main is not last")

    if b[:-1] == t[:-1]:
        raise RuntimeError(f"{family}: helper order did not change")

    if t[:-1] != list(reversed(b[:-1])):
        raise RuntimeError(f"{family}: helper order is not exact reversal")

    print(f"{family}: PASS")
    print("  BASE           : " + " -> ".join(b))
    print("  METHOD_REORDER : " + " -> ".join(t))
    checked += 1

if checked != 12:
    raise RuntimeError(f"Expected 12 families, checked {checked}")

print(f"\nStructural checks: {checked}/12 PASS")
