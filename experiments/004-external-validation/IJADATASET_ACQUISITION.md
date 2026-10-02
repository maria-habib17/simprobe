# Experiment 004 - IJaDataset Acquisition and Compatibility

## Status

IJaDataset source corpus acquired and compatibility-checked before any C0/C1 measurement.

- Acquisition date: 2026-10-02
- C0/C1 measurements at freeze: 0
- Raw corpus is excluded from Git.

## Experiment protocol

- Protocol commit: `8227fa6a070c4822c682baf052cfb35c285c2d2e`
- Protocol SHA-256: `99662720BC351B5E1C4C353E13660BD7338E5E06508B2C6C28FF0626DF4F7170`

## Benchmark context

- Benchmark: BigCloneBench Version 2 / BigCloneEval
- Frozen BigCloneEval upstream commit: `6d393ec8adb1d71493d09881ba520659b6c2c68e`
- Previously frozen BCB V2 acquisition commit: `2bc2b30b6fbced739c689d78d56fe92ca309298d`

## IJaDataset artifact

- Downloaded filename: `dataset.tar.gz`
- Size: 2,482,066,231 bytes
- SHA-256: `657FE752838C882A6D0FA1A784608F84A4E8129C84B0504EC37D617B65F7433F`
- Archive signature begins: `1F 8B 08` (gzip)
- Extracted under ignored Experiment 004 corpus storage.

Observed archive/source layout includes:

- `dataset/default/`
- `dataset/selected/`
- `dataset/sample/`

The extracted source corpus is not committed to Git.

## BCB V2 database

- Canonical database: `bcb.h2.db`
- Canonical SHA-256: `C5453E3A7CE1604C52A35F3B931AFA9F70515B17B956A9DA472A13E2BCBAE43B`

The canonical database was never opened writable for compatibility inspection.
A disposable byte-for-byte copy was used for H2 queries and deleted after inspection.
The canonical database hash was verified unchanged before and after inspection.

## Direct source mapping checks

Initial targeted checks:

- `default/26522.java`: present
- `default/32569.java`: present

Representative database-to-source checks across all FUNCTIONS.TYPE values:

| BCB function ID | Type | Source | BCB lines | Source lines | Result |
| ---: | --- | --- | --- | ---: | --- |
| 1 | default | 32569.java | 8-9 | 10 | PASS |
| 953715 | selected | 986217.java | 18-20 | 29 | PASS |
| 6096495 | sample | MD5.java | 2-11 | 12 | PASS |

For every representative record:

1. `FUNCTIONS.TYPE` resolved to the corresponding dataset directory.
2. `FUNCTIONS.NAME` resolved to an existing Java source file.
3. `STARTLINE >= 1`.
4. `ENDLINE >= STARTLINE`.
5. `ENDLINE` did not exceed the physical source-file line count.

Result: representative BCB V2 -> IJaDataset mapping PASS for `default`, `selected`, and `sample`.

## Measurement boundary

No C0 or C1 similarity measurement was computed during acquisition, extraction, schema inspection, or compatibility checking.

The next stages remain subject to the frozen Experiment 004 protocol:

1. freeze corpus eligibility and technical exclusions;
2. freeze deterministic sampling and strata;
3. freeze/implement the minimum deterministic BCB-to-SimProbe adapter;
4. only then compute C0/C1 measurements.

This record does not establish a plagiarism threshold, universal semantic equivalence, or universal clone-detection accuracy.
