# Rebuttal

Space is tiny and reviewers skim. Structure carries more weight than prose.

## Before writing

Read all reviews once without responding, then list every point in a single
table and score each on two axes: **how much it would move the decision**, and
**whether you can address it in the rebuttal period**.

Spend the space in this order:

1. Points that would change a score and can be answered with an experiment you
   can run now.
2. Points that would change a score and can be answered by pointing at
   something already in the paper the reviewer missed.
3. Factual corrections.
4. Everything else, briefly or not at all.

A rebuttal that answers every point equally has spent its space on the points
that did not matter.

## Format

Open with the two or three new results, before any prose. Reviewers look for
numbers first.

```
R1-Q2  Comparison at matched backbone (requested): 42.1 vs 41.3 mIoU, Table A.
R2-Q1  Latency on the reviewer's hardware class: 38 ms, Table B.
R3     Typo in Eq. 4 confirmed; corrected.
```

Then per-reviewer, tagged, one short paragraph per point. Then a one-line
summary of what changed in the paper.

## Tone

Answer the question that was asked. If a reviewer misread something, the
sentence is "Section 3.2 states X; we will make this clearer in L120", not "the
reviewer is mistaken". If they are right, say so in the first clause and then
say what you did — that costs one line and buys credibility for the points you
are contesting.

Do not concede a claim you can support. Agreeing with every criticism to seem
reasonable reads as an admission and lowers scores.

## The commitments

Every "we will add" becomes a real edit in the camera-ready. Keep a ledger as
you write the rebuttal:

```
review point -> what we promised -> file and section -> done?
```

ACs do check, and for a conditional accept it is the whole basis of the
decision.

## What not to do

- New claims not in the submission.
- Results from a model you have not actually run.
- Attacking a reviewer's competence, however tempting.
- Filling the space. A short, dense rebuttal reads as confident.
