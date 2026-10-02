# BigCloneBench V2 acquisition

## Status

BigCloneBench Version 2 has been acquired and verified.

The matching IJaDataset / bcb_reduced source corpus has not yet been acquired.

No Experiment 004 C0 or C1 measurements have been performed.

## Frozen Experiment 004 context

- Protocol commit: 8227fa6a070c4822c682baf052cfb35c285c2d2e
- Protocol SHA-256: 99662720BC351B5E1C4C353E13660BD7338E5E06508B2C6C28FF0626DF4F7170
- BigCloneEval revision: 6d393ec8adb1d71493d09881ba520659b6c2c68e

## BigCloneBench V2 archive

- Artifact: BigCloneBench_BCEvalVersion.tar.gz
- Acquisition date: 2026-10-02
- Size: 682189868 bytes
- SHA-256: 0BB5F8B383B411302EF35B2D10135A048D02EC22DD365AECBFE90A31A99ED2DE
- Archive validation: passed

Archive inventory:

- bcb.h2.db
- bcb.trace.db

The archive and extracted payload are stored only under ignored Experiment 004 paths and are not committed to Git.

## Extracted canonical database

- bcb.h2.db size: 5865951232 bytes
- bcb.h2.db SHA-256: C5453E3A7CE1604C52A35F3B931AFA9F70515B17B956A9DA472A13E2BCBAE43B
- bcb.trace.db size: 33906 bytes
- bcb.trace.db SHA-256: 1DD184A16C6A4B4A2A4AE97208E1BA9E9140E007FCAC9CEE10A18702C27C3320

The canonical extracted database was not opened writable for inspection.

H2 1.3.176 required recovery when opening this PageStore database. Schema and metadata inspection therefore used a disposable byte-for-byte copy under the ignored work directory. Recovery-related mutations were confined to that disposable copy.

The canonical database and trace hashes remained unchanged after inspection.

## Database tooling

- H2 artifact: BigCloneEval/libs/h2-1.3.176.jar
- H2 SHA-256: 6096B735AC4AF70FA730E4387582C599BCC347548FD2A5C50C2E7A0B52D5D287
- Java used for inspection: OpenJDK 25.0.4.1

## Database metadata

- Database VERSION value: Version 1.0 (2016-06-19)
- FUNCTIONS rows: 22285855
- Distinct PROJECT values: 24557
- CLONES rows: 8584153
- FALSE_POSITIVES rows: 279032
- FUNCTIONALITIES rows: 43
- TOOLS rows: 0
- TOOLS_CLONES rows: 0

FUNCTIONS INTERNAL distribution:

- FALSE: 21448192
- TRUE: 837663

FUNCTIONS TYPE distribution:

- default: 764376
- sample: 107
- selected: 21521372

CLONES SYNTACTIC_TYPE distribution:

- 1: 48116
- 2: 4234
- 3: 8531803

CLONES TYPE distribution:

- sample-sample: 206
- sample-tagged: 42175
- tagged-tagged: 8541772

## Relevant schema

FUNCTIONS contains:

- NAME
- TYPE
- STARTLINE
- ENDLINE
- ID
- NORMALIZED_SIZE
- PROJECT
- TOKENS
- INTERNAL

CLONES contains:

- FUNCTION_ID_ONE
- FUNCTION_ID_TWO
- FUNCTIONALITY_ID
- TYPE
- SYNTACTIC_TYPE
- SIMILARITY_LINE
- SIMILARITY_TOKEN
- MIN_SIZE
- MAX_SIZE
- MIN_PRETTY_SIZE
- MAX_PRETTY_SIZE
- MIN_JUDGES
- MIN_CONFIDENCE
- MIN_TOKENS
- MAX_TOKENS
- INTERNAL

FALSE_POSITIVES contains benchmark-labeled rejected relations and is not assumed to define arbitrary unlisted pairs as negatives.

## Source-location interpretation

Observed FUNCTIONS records store the Java filename and project separately. For example, NAME may be 26522.java while PROJECT is ivussnakes, with STARTLINE and ENDLINE identifying the benchmark fragment.

The database alone therefore does not provide the Java source text required by SimProbe. The matching IJaDataset / bcb_reduced distribution is still required before source fragments can be resolved and measured.

No path reconstruction rule will be assumed until the matching IJaDataset layout is acquired and inspected.

## Remaining acquisition requirement

Required artifact:

- IJaDataset_BCEvalVersion.tar.gz, or an authoritative byte-equivalent/matching distribution whose provenance and compatibility can be established

Until that source corpus is acquired:

- no benchmark fragments will be extracted for SimProbe
- no sampling will be finalized from SimProbe scores
- no C0 measurements will be computed
- no C1 measurements will be computed
- no alternative corpus will be silently substituted

This document updates the earlier acquisition-blockage record. That historical record remains unchanged: at the time it was committed, neither required benchmark artifact had been successfully acquired. BigCloneBench V2 was subsequently obtained and verified on 2026-10-02.
