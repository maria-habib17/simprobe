from pathlib import Path
import re

ROOT = Path("experiments/003-broader-validation/fixtures/primary")

# Helpers moved to the package-private Support class.
# Remaining helpers stay in the original public class with main.
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

METHOD_RE = re.compile(r"(?m)^    (?:public )?static\s+[^\n{]+\s+(\w+)\s*\([^)]*\)\s*\{")

def find_methods(text):
    matches = list(METHOD_RE.finditer(text))
    methods = []
    for match in matches:
        name = match.group(1)
        start = match.start()
        brace = text.find("{", match.start(), match.end())
        depth = 0
        end = None
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        if end is None:
            raise RuntimeError(f"Unclosed method: {name}")
        while end < len(text) and text[end] in "\r\n":
            end += 1
        methods.append((name, start, end, text[start:end].rstrip()))
    return methods

def qualify_calls(block, owner, names):
    result = block
    for name in sorted(names, key=len, reverse=True):
        result = re.sub(rf"(?<![\w.]){re.escape(name)}\s*\(", f"{owner}.{name}(", result)
    return result

for family in "ABCDEFGHIJKL":
    base_dir = ROOT / family / "BASE"
    sources = list(base_dir.glob("*.java"))
    if len(sources) != 1:
        raise RuntimeError(f"{family}: expected exactly one BASE Java file")

    source = sources[0]
    text = source.read_text(encoding="utf-8")
    methods = find_methods(text)
    names = [m[0] for m in methods]

    if "main" not in names:
        raise RuntimeError(f"{family}: main not found")

    moved = MOVED[family]
    helper_names = [n for n in names if n != "main"]

    if not set(moved).issubset(helper_names):
        raise RuntimeError(f"{family}: invalid moved-method specification")

    kept = [n for n in helper_names if n not in moved]
    class_name = source.stem
    support_name = class_name + "Support"
    method_map = {name: block for name, _, _, block in methods}

    first_method = min(start for _, start, _, _ in methods)
    last_method = max(end for _, _, end, _ in methods)

    prefix = text[:first_method]
    suffix = text[last_method:]

    # Calls from original-class methods to moved helpers need Support qualification.
    original_blocks = []
    for name in kept + ["main"]:
        block = method_map[name]
        block = qualify_calls(block, support_name, moved)
        original_blocks.append(block)

    original_text = prefix + "\n\n".join(original_blocks) + "\n" + suffix

    # Calls from Support methods back to helpers retained in the public class
    # need public-class qualification. Calls among moved methods remain local.
    support_blocks = []
    for name in moved:
        block = method_map[name]
        block = qualify_calls(block, class_name, kept)
        support_blocks.append(block)

    support_text = (
        f"class {support_name} {{\n"
        + "\n\n".join(support_blocks)
        + "\n}\n"
    )

    target = ROOT / family / "CLASS_SPLIT"
    target.mkdir(parents=True, exist_ok=True)

    (target / source.name).write_text(original_text, encoding="utf-8", newline="\n")
    (target / f"{support_name}.java").write_text(support_text, encoding="utf-8", newline="\n")

    print(f"{family}: {class_name}")
    print(f"  kept  : {kept} + main")
    print(f"  moved : {moved} -> {support_name}")

print("\nGenerated 12 CLASS_SPLIT submissions / 24 Java files.")
