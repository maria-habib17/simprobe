from __future__ import annotations

import argparse
import csv
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXP = Path(__file__).resolve().parents[1]
MANIFEST = EXP / "sample_manifest.csv"
DATASET = EXP / "corpus" / "ijadataset-v2" / "dataset"
ENGINE = ROOT / "experiments" / "003-broader-validation" / "implementation" / "compare.py"
RESULTS = EXP / "measurements.csv"
FAILURES = EXP / "adapter_failures.csv"

def load_engine():
    spec = importlib.util.spec_from_file_location("exp003_compare", ENGINE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

ENGINE_MOD = load_engine()

def fragment(row, side):
    typ = row[f"{side}_TYPE"]
    name = row[f"{side}_NAME"]
    start = int(row[f"{side}_STARTLINE"])
    end = int(row[f"{side}_ENDLINE"])
    path = DATASET / typ / name
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    return "".join(lines[start-1:end])

def adapter_check(source, label):
    tokens = ENGINE_MOD.normalized_tokens(source)
    units = ENGINE_MOD.extract_method_units(source, label)
    if not tokens:
        raise ValueError("EMPTY_TOKEN_SEQUENCE")
    if len(units) != 1:
        raise ValueError(f"METHOD_UNIT_COUNT_{len(units)}")
    return tokens, units

def c0(source_a, source_b):
    a = ENGINE_MOD.normalized_tokens(source_a)
    b = ENGINE_MOD.normalized_tokens(source_b)
    distance, similarity = ENGINE_MOD.normalized_similarity(a, b)
    return len(a), len(b), distance, similarity

def c1(source_a, source_b):
    a = ENGINE_MOD.extract_method_units(source_a, "fragment-a.java")
    b = ENGINE_MOD.extract_method_units(source_b, "fragment-b.java")
    result = ENGINE_MOD.compare_method_units(a, b)
    return (
        result.left_method_count,
        result.right_method_count,
        result.matched_method_count,
        result.matched_similarity_sum,
        result.similarity,
    )

def load_rows():
    with MANIFEST.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

def validate_only(rows):
    failures = []
    representable = 0
    for i, row in enumerate(rows, 1):
        try:
            left = fragment(row, "F1")
            right = fragment(row, "F2")
            adapter_check(left, "left.java")
            adapter_check(right, "right.java")
            representable += 1
        except Exception as exc:
            failures.append((
                row["STRATUM"], row["CANONICAL_PAIR_KEY"],
                type(exc).__name__, str(exc)
            ))
        if i % 500 == 0:
            print(f"validated={i}")
    print(f"TOTAL_PAIRS={len(rows)}")
    print(f"REPRESENTABLE_PAIRS={representable}")
    print(f"ADAPTER_FAILURE_PAIRS={len(failures)}")
    return failures

def measure(rows):
    fields = [
        "STRATUM","CANONICAL_PAIR_KEY","FUNCTIONALITY_IDS",
        "SIMILARITY_TOKEN","SIMILARITY_LINE",
        "C0_LEFT_TOKENS","C0_RIGHT_TOKENS","C0_EDIT_DISTANCE","C0_SIMILARITY",
        "C1_LEFT_METHODS","C1_RIGHT_METHODS","C1_MATCHED_METHODS",
        "C1_MATCHED_SUM","C1_SIMILARITY"
    ]
    failures = []
    measured = []
    for i, row in enumerate(rows, 1):
        try:
            left = fragment(row, "F1")
            right = fragment(row, "F2")
            adapter_check(left, "left.java")
            adapter_check(right, "right.java")
            c0v = c0(left, right)
            c1v = c1(left, right)
            measured.append({
                "STRATUM": row["STRATUM"],
                "CANONICAL_PAIR_KEY": row["CANONICAL_PAIR_KEY"],
                "FUNCTIONALITY_IDS": row["FUNCTIONALITY_IDS"],
                "SIMILARITY_TOKEN": row["SIMILARITY_TOKEN"],
                "SIMILARITY_LINE": row["SIMILARITY_LINE"],
                "C0_LEFT_TOKENS": c0v[0],
                "C0_RIGHT_TOKENS": c0v[1],
                "C0_EDIT_DISTANCE": c0v[2],
                "C0_SIMILARITY": c0v[3],
                "C1_LEFT_METHODS": c1v[0],
                "C1_RIGHT_METHODS": c1v[1],
                "C1_MATCHED_METHODS": c1v[2],
                "C1_MATCHED_SUM": c1v[3],
                "C1_SIMILARITY": c1v[4],
            })
        except Exception as exc:
            failures.append({
                "STRATUM": row["STRATUM"],
                "CANONICAL_PAIR_KEY": row["CANONICAL_PAIR_KEY"],
                "ERROR_TYPE": type(exc).__name__,
                "ERROR": str(exc),
            })
        if i % 250 == 0:
            print(f"processed={i} measured={len(measured)} failures={len(failures)}")

    with RESULTS.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(measured)

    ff = ["STRATUM","CANONICAL_PAIR_KEY","ERROR_TYPE","ERROR"]
    with FAILURES.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=ff, lineterminator="\n")
        w.writeheader()
        w.writerows(failures)

    print(f"MEASURED_PAIRS={len(measured)}")
    print(f"FAILED_PAIRS={len(failures)}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--validate-only", action="store_true")
    args = p.parse_args()
    rows = load_rows()
    if len(rows) != 6000:
        raise RuntimeError(f"Expected 6000 frozen pairs, found {len(rows)}")
    if args.validate_only:
        validate_only(rows)
    else:
        measure(rows)

if __name__ == "__main__":
    main()
