# DEAD_CODE Transformation Record

## Scope

This record documents the DEAD_CODE transformation used in the Experiment 001
primary fixture.

Each DEAD_CODE submission is derived from its family BASE by inserting one
private static helper method that is never called.

No existing BASE statement, expression, literal, operator, control-flow path,
or method call is intentionally changed by this transformation.

## Family A

Inserted method:

`unusedDifference(int left, int right)`

The method returns `left - right`.

It is never invoked.

## Family B

Inserted method:

`unusedUppercase(String text)`

The method returns `text.toUpperCase()`.

It is never invoked.

## Family C

Inserted method:

`unusedEmptyCheck(String text)`

The method returns `text.isEmpty()`.

It is never invoked.

## Family D

Inserted method:

`unusedArea(int rows, int columns)`

The method returns `rows * columns`.

It is never invoked.

## Behavioral intent

The inserted methods are unreachable from each program's declared execution
path because no existing or inserted code invokes them.

They are intended to have no effect on standard input consumption, standard
output, filesystem state, network access, randomness, or termination behavior.

Behavioral preservation is additionally checked against all declared fixture
tests before the primary fixture is committed.
