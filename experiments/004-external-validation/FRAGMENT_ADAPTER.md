# Experiment 004 Fragment Adapter

Status: frozen before the first C0/C1 measurement.

## Input unit

The frozen BigCloneBench sample contains source fragments identified by dataset type, numeric source filename, STARTLINE, and ENDLINE.

## Deterministic adapter

For each side of each frozen pair:

1. Resolve the source file as corpus/ijadataset-v2/dataset/<TYPE>/<NAME>.
2. Read the source file as UTF-8.
3. Extract exactly the inclusive physical line interval STARTLINE through ENDLINE.
4. Pass the extracted text directly to the frozen Experiment 003 Java tokenizer and method-unit extractor.
5. No imports, class wrapper, package declaration, synthetic tokens, lexical repair, parser repair, or source rewriting is added.
6. A fragment is representable only when tokenization succeeds, the normalized token sequence is non-empty, and exactly one complete method unit is extracted.
7. A pair is measurable only when both fragments are representable.

## Failure handling

Unrepresentable fragments remain members of the frozen 6000-pair realized sample.

They are recorded as adapter failures and are not replaced by later candidates.

No failure is repaired using benchmark labels, SimProbe scores, clone category, similarity, functionality, or manual source modification.

## Pre-measurement validation

- frozen sample pairs: 6000
- representable pairs: 5755
- adapter-failure pairs: 245
- representable fraction: 95.9167 percent
- adapter-failure fraction: 4.0833 percent

## Measurement mapping

C0 applies the frozen normalized Java-token edit-similarity implementation directly to the two extracted fragments.

C1 applies the frozen method-unit comparison implementation to the method units extracted from the two fragments.

## Measurement boundary

- C0 measurements at adapter freeze: 0
- C1 measurements at adapter freeze: 0

No SimProbe similarity score was observed while defining or validating this adapter.
