# Experiment 003 Primary Fixture Specification

## Status

Frozen before implementation of Experiment 003 Java submissions and before similarity measurement.

## Fixture Design

- 12 independently constructed provenance families
- 4 submissions per family
- 48 submissions total
- 3 declared behavioral tests per family
- 36 declared tests total
- 144 behavioral executions across all four variants

Each family contains BASE, METHOD_REORDER, CLASS_SPLIT, and IDENTIFIER_RENAME.

Each BASE contains one public entry class, main, and at least four behavior-relevant helper methods.

METHOD_REORDER changes helper declaration order without intentional logic changes.

CLASS_SPLIT adds exactly one top-level helper class and moves at least two behavior-relevant helper methods into it.

IDENTIFIER_RENAME renames the entry class, helper methods, parameters, and local variables while preserving behavior.

# Family A: Temperature Summary

## Task

Read n integer temperatures. Print minimum, maximum, spread, and number of nonnegative temperatures.

## Declared Tests

### A1

Input: 5 -3 7 0 12 -8

Expected: min=-8; max=12; spread=20; nonnegative=3

### A2

Input: 4 -9 -2 -7 -1

Expected: min=-9; max=-1; spread=8; nonnegative=0

### A3

Input: 1 6

Expected: min=6; max=6; spread=0; nonnegative=1

# Family B: Word Length Profile

## Task

Read one line of space-separated words. Print word count, shortest length, longest length, and even-length word count.

## Declared Tests

### B1

Input: red green blue

Expected: words=3; shortest=3; longest=5; even=1

### B2

Input: Java makes tools useful

Expected: words=4; shortest=4; longest=6; even=3

### B3

Input: code

Expected: words=1; shortest=4; longest=4; even=1

# Family C: Digit Balance

## Task

Read one digit-only string. Print even/odd counts and sums. Zero is even.

## Declared Tests

### C1

Input: 120345

Expected: even=3; odd=3; evenSum=6; oddSum=9

### C2

Input: 86420

Expected: even=5; odd=0; evenSum=20; oddSum=0

### C3

Input: 97531

Expected: even=0; odd=5; evenSum=0; oddSum=25

# Family D: Grid Row Occupancy

## Task

Read r, c, and r binary rows. Print total ones, nonempty rows, full rows, and maximum row occupancy.

## Declared Tests

### D1

Input: 3 4 / 1100 / 0000 / 1110

Expected: ones=5; nonemptyRows=2; fullRows=0; maxRow=3

### D2

Input: 2 3 / 111 / 101

Expected: ones=5; nonemptyRows=2; fullRows=1; maxRow=3

### D3

Input: 1 2 / 00

Expected: ones=0; nonemptyRows=0; fullRows=0; maxRow=0

---

# Family E: Number Sign Transitions

## Task

Read n nonzero integers. Print positive count, negative count, adjacent sign-change count, and sum of absolute values.

## Declared Tests

### E1

Input: 5 3 -2 -4 7 -1

Expected: positive=2; negative=3; changes=3; absSum=17

### E2

Input: 4 -1 -2 -3 -4

Expected: positive=0; negative=4; changes=0; absSum=10

### E3

Input: 3 5 6 7

Expected: positive=3; negative=0; changes=0; absSum=18

---

# Family F: Vowel Pattern

## Task

Read one nonempty lowercase ASCII word. Print length, vowel count, maximal contiguous vowel-run count, and whether the first character is a vowel.

## Declared Tests

### F1

Input: education

Expected: length=9; vowels=5; runs=4; startsVowel=1

### F2

Input: strength

Expected: length=8; vowels=1; runs=1; startsVowel=0

### F3

Input: queue

Expected: length=5; vowels=4; runs=1; startsVowel=0

---

# Family G: Prefix Sum Peaks

## Task

Read n integers. Print final cumulative sum, maximum processed-prefix sum, minimum processed-prefix sum, and number of strictly positive processed prefixes.

## Declared Tests

### G1

Input: 5 3 -1 4 -8 5

Expected: final=3; maxPrefix=6; minPrefix=-2; positivePrefixes=4

### G2

Input: 3 -2 -3 -1

Expected: final=-6; maxPrefix=-2; minPrefix=-6; positivePrefixes=0

### G3

Input: 4 2 2 2 2

Expected: final=8; maxPrefix=8; minPrefix=2; positivePrefixes=4

---

# Family H: Character Frequency Extremes

## Task

Read one nonempty lowercase ASCII word. Print distinct-letter count, highest frequency, lowest positive frequency, and number of distinct letters occurring more than once.

## Declared Tests

### H1

Input: banana

Expected: distinct=3; maxFreq=3; minFreq=1; repeated=2

### H2

Input: abcd

Expected: distinct=4; maxFreq=1; minFreq=1; repeated=0

### H3

Input: mississippi

Expected: distinct=4; maxFreq=4; minFreq=1; repeated=3

---

# Family I: Matrix Diagonal Report

## Task

Read n and an n-by-n integer matrix. Print main-diagonal sum, anti-diagonal sum, number of row indices where the two diagonal positions contain equal values, and the center value when n is odd or zero otherwise.

## Declared Tests

### I1

Input: 3 / 1 2 3 / 4 5 6 / 7 8 9

Expected: main=15; anti=15; equalPositions=1; center=5

### I2

Input: 2 / 1 4 / 3 2

Expected: main=3; anti=7; equalPositions=0; center=0

### I3

Input: 1 / 8

Expected: main=8; anti=8; equalPositions=1; center=8

---

# Family J: Sorted Difference Report

## Task

Read n integers in nondecreasing order. Print adjacent duplicate count, positive-gap count, largest adjacent gap or zero for n=1, and total span.

## Declared Tests

### J1

Input: 6 1 1 3 7 7 10

Expected: duplicates=2; positiveGaps=3; maxGap=4; span=9

### J2

Input: 4 -5 -2 0 9

Expected: duplicates=0; positiveGaps=3; maxGap=9; span=14

### J3

Input: 1 12

Expected: duplicates=0; positiveGaps=0; maxGap=0; span=0

---

# Family K: Direction Walk

## Task

Read a nonempty string containing N, E, S, and W. Starting at the origin, print final x, final y, Manhattan distance from the origin, and number of processed prefixes returning exactly to the origin.

## Declared Tests

### K1

Input: NESW

Expected: x=0; y=0; distance=0; returns=1

### K2

Input: NNESW

Expected: x=0; y=1; distance=1; returns=0

### K3

Input: NSNS

Expected: x=0; y=0; distance=0; returns=2

---

# Family L: Divisibility Profile

## Task

Read positive integer n. For integers 1 through n inclusive, print counts divisible by 2, divisible by 3, divisible by both, and divisible by neither.

## Declared Tests

### L1

Input: 12

Expected: div2=6; div3=4; divBoth=2; neither=4

### L2

Input: 5

Expected: div2=2; div3=1; divBoth=0; neither=2

### L3

Input: 1

Expected: div2=0; div3=0; divBoth=0; neither=1

---

# Pre-implementation Freeze Rule

At specification freeze:

- no Experiment 003 Java submission may exist;
- no Experiment 003 similarity CSV may exist;
- no Experiment 003 similarity measurement may have been generated or inspected.

The 12 family tasks, 36 declared behavioral tests, family membership, variant set, and transformation requirements are fixed for the primary experiment.

A genuine specification defect discovered later must be corrected through a separate transparent correction commit before affected similarity measurements are generated.
