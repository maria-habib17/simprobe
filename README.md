# SimProbe

**Cohort-conditioned diagnostics for source-code similarity**

SimProbe is an independent research project investigating when a high
source-code similarity score is actually distinctive within the cohort in
which it occurs.

The project starts from a simple distinction:

> Similarity magnitude and evidential distinctiveness are not necessarily the
> same property.

Two programs may receive a very high similarity score because they share an
unusual relationship. The same score may also occur in a representation where
many otherwise distinct programs collapse into identical or near-identical
forms.

SimProbe studies how that distinction changes as source-code representations
become increasingly invariant to transformations such as identifier renaming
and structural variation.

## Research questions

SimProbe initially investigates:

1. How increasing representation abstraction affects transformation invariance
   and discrimination among independently constructed programs.
2. Whether cohort-relative measurements reveal differences between
   high-similarity results that have the same pairwise score.
3. Which abstraction operations contribute most strongly to measurable
   representation degeneracy.
4. Whether these effects generalize across different similarity methods and
   systems.

## Planned measurements

The pre-implementation protocol defines measurements including:

- pairwise similarity;
- exact representation multiplicity;
- score-tie multiplicity;
- neighborhood density;
- rank-based distinctiveness;
- representation entropy; and
- information-loss proxies between representation stages.

These measurements are research variables. SimProbe does not currently combine
them into a confidence or plagiarism score.

## Evaluation strategy

The planned evaluation separates:

- controlled transformations;
- independently developed solutions;
- cohort-perturbation experiments; and
- later cross-system evaluation.

JPlag is planned as an established external comparison system. SimProbe does
not assume that scores produced by different systems are mathematically
equivalent.

## Research status

SimProbe is currently at the **pre-implementation protocol stage**.

The research questions, hypotheses, negative-result criteria, interpretation
constraints, and initial related-work boundary were documented before the
primary experimental implementation.

See:

- `docs/protocol.md`
- `docs/related-work.md`

Implementation and primary measurements will follow the frozen protocol.

## Responsible interpretation

SimProbe is not a plagiarism detector or misconduct classifier.

A high similarity value does not by itself establish plagiarism, common
authorship, or author intent. Likewise, a representation collision does not by
itself establish a false positive.

The project studies properties of similarity evidence, not academic-misconduct
verdicts.

## Development

Requirements:

- Python 3.11 or newer

Install the development environment:

```bash
pip install -e ".[dev]"