import csv
import hashlib
import heapq
import os
import sys
from collections import defaultdict

SEED = "SIMPROBE-EXP004|20261002"
TARGET = 1000
KEEP = 2500
STRATA = [
    "TYPE1",
    "TYPE2",
    "VST3_90_100",
    "ST3_70_90",
    "MT3_50_70",
    "WT3_T4_0_50",
]

COMPARE_FIELDS = [
    "STRATUM", "FUNCTION_ID_ONE", "FUNCTION_ID_TWO",
    "PAIR_TYPE", "SYNTACTIC_TYPE", "SIMILARITY_LINE",
    "SIMILARITY_TOKEN", "PAIR_INTERNAL",
    "F1_TYPE", "F1_NAME", "F1_STARTLINE", "F1_ENDLINE",
    "F1_PROJECT", "F1_INTERNAL",
    "F2_TYPE", "F2_NAME", "F2_STARTLINE", "F2_ENDLINE",
    "F2_PROJECT", "F2_INTERNAL"
]

def selection_key(stratum, f1, f2):
    a, b = sorted((int(f1), int(f2)))
    pair = f"{a}:{b}"
    payload = f"{SEED}|{stratum}|{pair}"
    key = hashlib.sha256(payload.encode("ascii")).hexdigest().upper()
    return key, pair

def count_lines(path):
    count = 0
    last = b""
    with open(path, "rb") as fh:
        while True:
            block = fh.read(1024 * 1024)
            if not block:
                break
            count += block.count(b"\n")
            last = block[-1:]
    if os.path.getsize(path) > 0 and last != b"\n":
        count += 1
    return count

def source_check(dataset, typ, name, start, end):
    path = os.path.join(dataset, typ, name)
    if not os.path.isfile(path):
        return False, "SOURCE_FILE_MISSING", ""
    try:
        start = int(start)
        end = int(end)
    except Exception:
        return False, "INVALID_LINE_METADATA", ""
    if start < 1:
        return False, "STARTLINE_LT_1", ""
    if end < start:
        return False, "ENDLINE_LT_STARTLINE", ""
    try:
        lines = count_lines(path)
    except Exception as exc:
        return False, "SOURCE_READ_FAILURE:" + type(exc).__name__, ""
    if end > lines:
        return False, "ENDLINE_GT_FILE_LINES", str(lines)
    return True, "", str(lines)

def signature(row):
    return tuple(row.get(f, "") for f in COMPARE_FIELDS)

def main():
    if len(sys.argv) != 5:
        raise SystemExit("usage: generate_sample.py CANDIDATES DATASET MANIFEST EXCLUSIONS")

    candidates, dataset, manifest_path, exclusion_path = sys.argv[1:]

    # Pass 1: keep deterministic low-key windows while collapsing
    # duplicate CLONES rows to one canonical pair candidate.
    retained = {s: {} for s in STRATA}
    heaps = {s: [] for s in STRATA}
    seen_rows = 0
    duplicate_rows = 0

    with open(candidates, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            s = row["STRATUM"]
            if s not in retained:
                continue

            seen_rows += 1
            key, pair = selection_key(s, row["FUNCTION_ID_ONE"], row["FUNCTION_ID_TWO"])
            funcs = {int(row["FUNCTIONALITY_ID"])}

            existing = retained[s].get(pair)
            if existing is not None:
                if signature(existing["row"]) != signature(row):
                    raise RuntimeError("Conflicting duplicate metadata for " + s + ":" + pair)
                existing["functionalities"].update(funcs)
                duplicate_rows += 1
                continue

            kval = int(key, 16)
            entry = {
                "key": key,
                "pair": pair,
                "kval": kval,
                "row": row,
                "functionalities": funcs,
            }

            if len(retained[s]) < KEEP:
                retained[s][pair] = entry
                heapq.heappush(heaps[s], (-kval, pair))
            else:
                # Remove stale heap heads if needed.
                while heaps[s] and heaps[s][0][1] not in retained[s]:
                    heapq.heappop(heaps[s])

                worst_neg, worst_pair = heaps[s][0]
                worst_kval = -worst_neg

                if kval < worst_kval:
                    heapq.heappop(heaps[s])
                    del retained[s][worst_pair]
                    retained[s][pair] = entry
                    heapq.heappush(heaps[s], (-kval, pair))

    # Pass 2: collect every functionality label for retained pairs.
    # This is necessary because a duplicate label row may occur after
    # its canonical pair was first retained.
    with open(candidates, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            s = row["STRATUM"]
            if s not in retained:
                continue
            key, pair = selection_key(s, row["FUNCTION_ID_ONE"], row["FUNCTION_ID_TWO"])
            existing = retained[s].get(pair)
            if existing is None:
                continue
            if signature(existing["row"]) != signature(row):
                raise RuntimeError("Conflicting duplicate metadata for " + s + ":" + pair)
            existing["functionalities"].add(int(row["FUNCTIONALITY_ID"]))

    selected = []
    excluded = []

    for s in STRATA:
        ranked = sorted(
            retained[s].values(),
            key=lambda e: (e["key"], e["pair"])
        )

        accepted = 0
        for candidate_rank, entry in enumerate(ranked, start=1):
            row = entry["row"]

            ok1, reason1, lines1 = source_check(
                dataset, row["F1_TYPE"], row["F1_NAME"],
                row["F1_STARTLINE"], row["F1_ENDLINE"]
            )
            ok2, reason2, lines2 = source_check(
                dataset, row["F2_TYPE"], row["F2_NAME"],
                row["F2_STARTLINE"], row["F2_ENDLINE"]
            )

            if not ok1 or not ok2:
                reasons = []
                if not ok1:
                    reasons.append("F1:" + reason1)
                if not ok2:
                    reasons.append("F2:" + reason2)
                excluded.append({
                    "STRATUM": s,
                    "CANDIDATE_RANK": str(candidate_rank),
                    "SELECTION_KEY": entry["key"],
                    "CANONICAL_PAIR_KEY": entry["pair"],
                    "FUNCTION_ID_ONE": row["FUNCTION_ID_ONE"],
                    "FUNCTION_ID_TWO": row["FUNCTION_ID_TWO"],
                    "FUNCTIONALITY_IDS": ";".join(str(x) for x in sorted(entry["functionalities"])),
                    "REASON": ";".join(reasons),
                })
                continue

            accepted += 1
            out = dict(row)
            out["SELECTION_RANK"] = str(accepted)
            out["CANDIDATE_RANK"] = str(candidate_rank)
            out["SELECTION_KEY"] = entry["key"]
            out["CANONICAL_PAIR_KEY"] = entry["pair"]
            out["FUNCTIONALITY_IDS"] = ";".join(
                str(x) for x in sorted(entry["functionalities"])
            )
            out["F1_SOURCE_LINES"] = lines1
            out["F2_SOURCE_LINES"] = lines2
            out["SOURCE_ELIGIBLE"] = "TRUE"
            selected.append(out)

            if accepted == TARGET:
                break

        if accepted != TARGET:
            raise RuntimeError(
                f"{s}: only {accepted} eligible unique pairs among {len(ranked)} retained candidates"
            )

    pair_keys = [r["CANONICAL_PAIR_KEY"] for r in selected]
    if len(pair_keys) != len(set(pair_keys)):
        raise RuntimeError("Duplicate canonical pair remains in realized sample")

    fields = [
        "STRATUM", "SELECTION_RANK", "CANDIDATE_RANK",
        "SELECTION_KEY", "CANONICAL_PAIR_KEY",
        "FUNCTION_ID_ONE", "FUNCTION_ID_TWO", "FUNCTIONALITY_IDS",
        "PAIR_TYPE", "SYNTACTIC_TYPE", "SIMILARITY_LINE",
        "SIMILARITY_TOKEN", "PAIR_INTERNAL",
        "F1_TYPE", "F1_NAME", "F1_STARTLINE", "F1_ENDLINE",
        "F1_PROJECT", "F1_INTERNAL", "F1_SOURCE_LINES",
        "F2_TYPE", "F2_NAME", "F2_STARTLINE", "F2_ENDLINE",
        "F2_PROJECT", "F2_INTERNAL", "F2_SOURCE_LINES",
        "SOURCE_ELIGIBLE"
    ]

    with open(manifest_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=fields, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        for row in selected:
            writer.writerow(row)

    exfields = [
        "STRATUM", "CANDIDATE_RANK", "SELECTION_KEY",
        "CANONICAL_PAIR_KEY", "FUNCTION_ID_ONE", "FUNCTION_ID_TWO",
        "FUNCTIONALITY_IDS", "REASON"
    ]

    with open(exclusion_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=exfields, lineterminator="\n")
        writer.writeheader()
        for row in excluded:
            writer.writerow(row)

    print("CANDIDATE_ROWS_SCANNED=" + str(seen_rows))
    print("DUPLICATE_ROWS_OBSERVED_DURING_RETAINED_SCAN=" + str(duplicate_rows))

    for s in STRATA:
        nsel = sum(1 for r in selected if r["STRATUM"] == s)
        nexc = sum(1 for r in excluded if r["STRATUM"] == s)
        multi = sum(
            1 for r in selected
            if r["STRATUM"] == s and ";" in r["FUNCTIONALITY_IDS"]
        )
        print(
            f"{s}: retained_unique={len(retained[s])} "
            f"selected={nsel} source_exclusions={nexc} "
            f"selected_multilabel={multi}"
        )

    print("TOTAL_SELECTED=" + str(len(selected)))
    print("TOTAL_SOURCE_EXCLUSIONS=" + str(len(excluded)))
    print("TOTAL_SELECTED_MULTILABEL=" + str(
        sum(1 for r in selected if ";" in r["FUNCTIONALITY_IDS"])
    ))

if __name__ == "__main__":
    main()
