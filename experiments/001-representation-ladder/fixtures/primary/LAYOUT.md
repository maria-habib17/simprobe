# Primary Fixture Layout

Each provenance family contains seven submission directories:

- `BASE`
- `IDENTIFIER_RENAME`
- `METHOD_REORDER`
- `CLASS_RENAME`
- `FILE_RENAME`
- `DEAD_CODE`
- `CLASS_SPLIT`

Each directory represents one complete program submission.

A submission may contain one or more Java source files. In particular,
`CLASS_SPLIT` uses an additional class as required by the controlled
transformation definition.

The four families are independent provenance families. Variants within a
family are controlled transformations of that family's `BASE`.

Transformation implementations must preserve the declared tested behavior in
`SPECIFICATION.md`.

`DEAD_CODE` variants must document the inserted behavior-neutral code before
primary similarity measurements are generated.
