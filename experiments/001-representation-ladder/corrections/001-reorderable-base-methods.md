# Fixture Correction 001 - Reorderable Base Methods

## Status

Pre-measurement fixture correction.

## Problem

The initial primary BASE implementations contained only a single declared
method (`main`).

Experiment 001 defines `METHOD_REORDER` as reordering method declarations
without intentionally changing behavior. With only one method declaration,
that controlled transformation cannot be instantiated meaningfully.

## Correction

Before creating transformed variants or generating any primary similarity
measurements, each BASE implementation will be refactored to contain multiple
behavior-relevant method declarations.

The declared tasks, inputs, outputs, provenance families, and test cases in
`fixtures/primary/SPECIFICATION.md` are unchanged.

The refactored BASE implementations must pass all previously declared fixture
tests before transformed variants are created.

## Experimental impact

No primary similarity measurements have been generated or inspected.

This correction therefore addresses a fixture-construction defect rather than
responding to an observed similarity result.

The correction does not add or remove provenance families, transformation
classes, representation stages, or declared test cases.
