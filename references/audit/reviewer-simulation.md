# Reviewing a draft

Assessment, not rewriting. If the output is a rewritten paragraph, the wrong
stage is running — see `references/workflow/routing.md`.

## The four questions

A CVPR-class reviewer is answering these, roughly in this order:

1. **Is the problem real?** Would anyone outside the authors' group care that
   it was solved?
2. **Is the claim supported?** Does the evidence in the paper establish what
   the abstract says?
3. **Is the comparison fair?** Matched backbone, resolution, schedule, data. Is
   the baseline current?
4. **Would I be able to reproduce this?**

Novelty is downstream of all four, and it is where weak reviews start instead
of finish.

## The report

For each of the four, a verdict and the specific evidence. Then:

- **Strengths** — three at most, each pointing at something in the paper.
- **Weaknesses** — ordered by how much they would change the decision, with
  the specific table or line. A weakness that cannot be acted on in a rebuttal
  period should be marked as such.
- **Questions** — things the authors could answer that would change your score.
  Distinguish these from weaknesses; conflating them is what produces rebuttals
  that answer everything and address nothing.
- **Score, with the sentence that would change it.** A score without that
  sentence is not useful to anyone.

## Calibration

Be explicit about what would move each way. Most unhelpful reviews fail here:
they list problems without weighting them, so the authors cannot tell which
one is load-bearing.

Separate two axes and never average them:

- **Relative progress** — is this better than what existed?
- **Absolute readiness** — is this a finished paper?

A large relative gain in an unfinished write-up is a different decision from a
small gain in a polished one, and collapsing them into one number loses the
information the AC needs.

## Before writing anything

```bash
python3 scripts/audit_paper.py paper/
```

Clears the mechanical findings — thin captions, missing sections, hedge
density, off-distribution phrasing — so the review can spend its length on the
science. Do not put "the caption is too short" in a review when the tool
already said it.

## Reviewing your own draft

Same procedure, one addition: write the review *before* you fix anything, and
keep it. The weaknesses you were willing to write down are the ones the
rebuttal will be about.
