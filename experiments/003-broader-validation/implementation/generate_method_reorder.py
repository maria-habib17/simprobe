from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "primary"

# Explicit deterministic helper-method order for every family.
# main is always kept last and is never modified.
ORDERS = {
    "A": ["countNonnegative", "spread", "maximum", "minimum"],
    "B": ["splitWords", "evenLengthCount", "longest", "shortest"],
    "C": ["digitSum", "oddCount", "evenCount", "isEven"],
    "D": ["maxRow", "fullRows", "nonemptyRows", "totalOnes", "rowOnes"],
    "E": ["absoluteSum", "signChanges", "negativeCount", "positiveCount", "isPositive"],
    "F": ["wordLength", "startsWithVowel", "vowelRuns", "vowelCount", "isVowel"],
    "G": ["positivePrefixes", "minimumPrefix", "maximumPrefix", "finalSum"],
    "H": ["repeatedCount", "minimumPositiveFrequency", "maximumFrequency", "distinctCount", "frequencies"],
    "I": ["centerValue", "equalPositions", "antiDiagonal", "mainDiagonal"],
    "J": ["span", "maximumGap", "positiveGapCount", "duplicateCount"],
    "K": ["returnCount", "distance", "finalY", "finalX"],
    "L": ["divisibleByNeither", "divisibleByBoth", "divisibleBy3", "divisibleBy2"],
}

def find_methods(text):
    pattern = re.compile(r"(?m)^    (?:public )?static\s+[^\n{]+\s+(\w+)\s*\([^)]*\)\s*\{")
    matches = list(pattern.finditer(text))
    methods = {}
    for match in matches:
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
            raise RuntimeError(f"Unclosed method {match.group(1)}")
        while end < len(text) and text[end] in "\r\n":
            end += 1
        methods[match.group(1)] = (start, end, text[start:end].rstrip())
    return methods

for family, order in ORDERS.items():
    base_dir = ROOT / family / "BASE"
    sources = list(base_dir.glob("*.java"))
    if len(sources) != 1:
        raise RuntimeError(f"{family}: expected one BASE Java file, found {len(sources)}")

    source = sources[0]
    text = source.read_text(encoding="utf-8")
    methods = find_methods(text)

    expected = set(order) | {"main"}
    if set(methods) != expected:
        raise RuntimeError(f"{family}: method mismatch: found {sorted(methods)}, expected {sorted(expected)}")

    first = min(start for start, _, _ in methods.values())
    last = max(end for _, end, _ in methods.values())
    prefix = text[:first]
    suffix = text[last:]

    blocks = [methods[name][2] for name in order]
    blocks.append(methods["main"][2])
    transformed = prefix + "\n\n".join(blocks) + "\n" + suffix

    target = ROOT / family / "METHOD_REORDER"
    target.mkdir(parents=True, exist_ok=True)
    output = target / source.name
    output.write_text(transformed, encoding="utf-8", newline="\n")
    print(f"{family}: {source.name} -> METHOD_REORDER")

print("Generated 12 METHOD_REORDER submissions.")
