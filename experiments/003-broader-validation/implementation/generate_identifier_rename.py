from pathlib import Path
import re

ROOT = Path("experiments/003-broader-validation/fixtures/primary")

CLASS_NAMES = {
    "A": "ProgramA",
    "B": "ProgramB",
    "C": "ProgramC",
    "D": "ProgramD",
    "E": "ProgramE",
    "F": "ProgramF",
    "G": "ProgramG",
    "H": "ProgramH",
    "I": "ProgramI",
    "J": "ProgramJ",
    "K": "ProgramK",
    "L": "ProgramL",
}

METHOD_RE = re.compile(
    r"(?m)^    (?:public )?static\s+[^\n{]+\s+(\w+)\s*\([^)]*\)\s*\{"
)

IDENTIFIER_RE = re.compile(r"\b[A-Za-z_$][A-Za-z0-9_$]*\b")

def replace_code_identifiers(text, mapping):
    """Replace identifiers only in Java code, never inside strings/chars/comments."""
    out = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        # String literal
        if ch == "\"":
            start = i
            i += 1
            while i < n:
                if text[i] == "\\\\":
                    i += 2
                    continue
                if text[i] == "\"":
                    i += 1
                    break
                i += 1
            out.append(text[start:i])
            continue

        # Character literal
        if ch == chr(39):
            start = i
            i += 1
            while i < n:
                if text[i] == "\\\\":
                    i += 2
                    continue
                if text[i] == chr(39):
                    i += 1
                    break
                i += 1
            out.append(text[start:i])
            continue

        # Line comment
        if text.startswith("//", i):
            end = text.find("\n", i)
            if end == -1:
                out.append(text[i:])
                break
            out.append(text[i:end])
            i = end
            continue

        # Block comment
        if text.startswith("/*", i):
            end = text.find("*/", i + 2)
            if end == -1:
                out.append(text[i:])
                break
            end += 2
            out.append(text[i:end])
            i = end
            continue

        match = IDENTIFIER_RE.match(text, i)
        if match:
            token = match.group(0)
            out.append(mapping.get(token, token))
            i = match.end()
            continue

        out.append(ch)
        i += 1

    return "".join(out)

for family in "ABCDEFGHIJKL":
    base_dir = ROOT / family / "BASE"
    sources = list(base_dir.glob("*.java"))

    if len(sources) != 1:
        raise RuntimeError(f"{family}: expected exactly one BASE Java file")

    source = sources[0]
    text = source.read_text(encoding="utf-8")

    original_class = source.stem
    renamed_class = CLASS_NAMES[family]

    methods = METHOD_RE.findall(text)
    helpers = [name for name in methods if name != "main"]

    if "main" not in methods:
        raise RuntimeError(f"{family}: main method not found")

    mapping = {original_class: renamed_class}

    for index, method in enumerate(helpers, start=1):
        mapping[method] = f"operation{index}"

    transformed = replace_code_identifiers(text, mapping)

    target = ROOT / family / "IDENTIFIER_RENAME"
    target.mkdir(parents=True, exist_ok=True)

    # Remove stale Java files from the previous generation.
    for old in target.glob("*.java"):
        old.unlink()

    output = target / f"{renamed_class}.java"
    output.write_text(transformed, encoding="utf-8", newline="\n")

    print(f"{family}: {original_class} -> {renamed_class}")
    for old in helpers:
        print(f"  {old} -> {mapping[old]}")

print("\nRegenerated 12 IDENTIFIER_RENAME submissions safely.")
